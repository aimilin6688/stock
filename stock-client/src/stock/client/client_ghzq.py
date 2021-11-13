import os
import time

import pywinauto as pw
import win32api
import win32con
from pywinauto import timings
from pywinauto.timings import TimeoutError
from pywinauto.base_wrapper import ElementNotEnabled
from pywinauto.findwindows import WindowNotFoundError, ElementNotFoundError
from src.utils.config import conf
from src.stock.client.client_10jqka import Client10jqka, ImgType, LoginException, logging, fn_timer, log, WindowType
from src.stock.bean.stock_bean import PositionType, Money, remove_code_prefix, Account,StockInfo, StockResult,PopupResult
from src.utils import windows_utils as wu
from src.utils.code_utils import code_to_str
from src.utils.win32_utils import get_handle
from tenacity import retry, retry_if_result, stop_after_attempt, after_log
from collections import OrderedDict


# 国海证券
class ClientGhzq(Client10jqka):
    """
    1. 系统参数：列表框账户：资金账号+姓名，锁屏账户信息：资金账号+姓名，闲时锁定：999
    2. 普通交易：
        普通策略：
            （不选中）委托成功提示，
            （不选中）撤单确认提示，
            （不选中）撤单成功提示，
        量价策略：默认买入价格：空，默认卖出价格：空，默认买入、卖出数量：固定数量：0
    3. 注意：委托、成交、持仓：不要将两列中文放一起
    """

    def _after_init(self):
        title = "金贝壳网上交易系统"
        self._main_hwnd = get_handle(title, conf.exe_ghzq)
        self._app = pw.Application(backend="win32").connect(handle=self._main_hwnd)
        self._main_window = self._app.window(title=title, class_name="TfrmForexMainGUIHSINFO")
        self._close_save_as()

    def _match_account(self, account, is_selected=False) -> bool:
        self._unlock()
        if not self._main_window.exists():
            return False

        # 主窗口最大化
        self._max_window()
        account_combo_box = self._main_window.TImagePanel.child_window(class_name="THSComboBox", visible_only=False)
        result_text = None
        for text in account_combo_box.item_texts():
            if text.find(account.username) != -1:
                result_text = text
                if is_selected and account_combo_box.is_visible():
                    account_combo_box.select(text)
                    log.info("切换账号：%s", text)
                else:
                    log.info("账号：%s(%s)已登录无需切换！", account.broker, account.nickname)
                break
        return result_text is not None

    def _login_account(self, account: Account) -> bool:
        try:
            self.account = account

            login_window = self._app.window(class_name="TfrmLoginBaseEx")

            # 账户
            try:
                login_window.ComboBox3.wrapper_object().select("资金-%s" % account.username)
            except ValueError as e:
                login_window.Edit4.set_focus()
                login_window.Edit4.type_keys(account.username)
            codeEdit = login_window.Edit2
            handle_map = OrderedDict()
            # 自动登录5次
            for i in range(7):
                self._close_popup_windows(handle_map=handle_map)
                # 每次都自动输入密码，防止密码输入错误
                login_window.Edit3.set_focus()
                login_window.Edit3.type_keys("{BACKSPACE}")
                wu.press(*account.password)
                if codeEdit.is_visible():
                    rect = codeEdit.rectangle()
                    pos = (rect.right + 10, rect.top, rect.right + 76, rect.bottom)
                    code = code_to_str(pos, img_type=ImgType.ghzq)
                    codeEdit.set_focus()
                    codeEdit.type_keys("{BACKSPACE}")
                    wu.press(*code)
                    log.info("国海证券----自动识别验证码:%s", code)

                login_window['登录'].click()
                try:
                    result = self._close_public_info()
                    if result == -1:
                        raise timings.TimeoutError("验证码错误！")
                    timings.wait_until(15, 0.5, lambda: self._main_window.exists() and self._main_window.is_visible())
                    break
                except timings.TimeoutError as e:
                    log.warning(str(e))
                    log.info("国海证券----尝试登录第：%d/%d次", i + 1, 7)
                    continue
            else:
                log.error("国海证券---自动登录失败，账号：%s,原因：%s", account, handle_map.values())
                raise LoginException("%s" % (PopupResult(handle_map).texts))
            time.sleep(1)
            self._close_popup_windows()
            log.info("国海证券----账号：%s，登录成功!", account)
            # 刷新界面句柄
            self._refresh_hwnd()
        except Exception as e:
            raise e
        return True

    def _select_money(self):
        frm_window = self._main_window.window(class_name="TfrmBizContnr", title="frmBizContnr")
        tree_view = frm_window.window(class_name="TTreeView", found_index=0)
        tree_view.item([7]).click_input()

    def _get_trade_window(self):
        return self._main_window.window(title="plTrade", class_name="TPanel")

    def _get_trade_active_window(self):
        return self._main_window.window(title="pnlBottom", class_name="TPanel")

    def _is_window(self, _window, w_type: WindowType) -> bool:
        try:
            if w_type == WindowType.W_BUY:  # 买界面
                w_window = _window.child_window(class_name="TFrmBuyStock")
                return w_window.exists(timeout=0.5) and w_window.is_visible()
            if w_type == WindowType.W_SELL:  # 卖界面
                w_window = _window.child_window(class_name="Tfrm2007")
                return w_window.exists(timeout=0.5) and w_window.is_visible()
        except ElementNotFoundError as e:
            log.warning(str(e))
        return True

    def _get_position_key(self):
        return {PositionType.POSITION: "{F6}", PositionType.DEAL: "{F8}", PositionType.ENTRUST: "{F7}"}

    def __close_popup_window(self, popup_hwnd=None, btn_name=None, handle_map=None, title=None, ignore_count=-1):
        try:
            popup_window = self._app.window(class_name="TfrmDialogs", visible_only=True, found_index=0)
            if not popup_window.exists():
                return False

            # 记录弹框总数
            if handle_map is not None:
                handle_map.setdefault(popup_window.handle, {"count": 0, "text": ""})
                handle_map[popup_window.handle]['count'] += 1

            # 记录警告和提示信息
            self.__popup_text(handle_map, popup_window)

            for btn in ["是(&Y)", "确定(&O)"]:
                b = popup_window["%sButton" % btn]
                if b.exists() and b.is_enabled() and b.is_visible():
                    b.click()
                    break
            else:
                popup_window.Button.click()
            return True
        except Exception as e:
            log.exception(e)
            return False

    def __popup_text(self, handle_map, popup_window):
        title = popup_window.window_text()
        if title in ["警告", "提示", "错误"]:
            panel = popup_window.window(class_name="TPanel", found_index=0)
            # 主要为了突出显示
            panel.set_focus()
            panel.click()
            rect = panel.rectangle()
            pos = (rect.left + 50, rect.top, rect.right, rect.bottom)
            text = code_to_str(pos, ImgType.text, lang="chi_sim")
            log.debug("账户:%s, %s:%s", self.account, title, text)
            if handle_map:
                handle_map[popup_window.handle]['text'] = text
        return handle_map

    def _select_window(self, type):
        try:
            return super()._select_window(type)
        except ElementNotEnabled:
            for i in range(3):
                try:
                    self._close_notepad()
                    self._close_popup_windows()
                    time.sleep(5)
                    return super()._select_window(type)
                except Exception as e:
                    log.warning("切换窗口类型失败，重试：%d/%d", i + 1, 3)
                    log.exception(e)

    def _is_lock(self) -> bool:
        lock_window = self._app.window(title="锁定", class_name="TfrmLock")
        return lock_window.exists() and lock_window.is_visible()

    def _unlock(self):
        if not self._is_lock():
            return
        count = 0
        while self._is_lock() and count <= 5:
            self._close_popup_window()
            lock_window = self._app.window(title="锁定", class_name="TfrmLock")
            if lock_window.exists() and lock_window.is_visible():
                lock_window.Edit.set_focus()

                # 这里输入第一次的时候光标会错位，所以需要输入两次重新定位光标
                lock_window.Edit.set_text(self.account.password)
                lock_window.Edit.set_text("")
                wu.press(*self.account.password)
                lock_window['确定'].click()
                count += 1
                time.sleep(3)

    @staticmethod
    def support_brokers():
        return ['国海证券']

    # 数据读取使用Excel方式，不再使用csv方式
    def __read_data(self, file_path, position_type, **pd_kvargs):
        return self._read_file(file_path, 0, position_type=position_type, **pd_kvargs)

    def _get_position_data(self, position_type):
        buy_panel = self._buy_window.TFrmBuyStock
        cw = buy_panel.child_window(class_name="TPanel", found_index=1)

        def save_btn():
            cw.child_window(title="输出", class_name="TBitBtn").click()

        after_read = None
        if position_type == PositionType.ENTRUST:
            cancel_element = cw.child_window(title="仅显示可撤", class_name="TCheckBox")
            if cancel_element.exists() and cancel_element.is_visible():
                cancel_element.check_by_click()
            after_read = lambda x: x[~x['委托状态'].isin(['废单', "已撤", "已成"])]

        return self._save_as_data(save_btn, position_type,
                                  pd_kvargs=dict(skipfooter=2),
                                  read_func=self.__read_data,
                                  after_read=after_read,
                                  sleep_time=0.8,
                                  file_postfix="TXT")

    def _refresh_position(self):
        try:
            cw = self._buy_window.TFrmBuyStock
            cw = cw.child_window(class_name="TPanel", found_index=1)
            cw.child_window(title="刷新", class_name="TBitBtn").click()
        except:
            pass

    def money(self, **kwargs) -> Money:
        def save_money():
            control_window = self._money_window.window(class_name="TPanel", found_index=1)
            tp = control_window.Tfrm3533
            tp.child_window(title="刷新[F5]", class_name="TButton").click()
            tp.child_window(title="输出", class_name="TButton").click()

        try:
            self._select_open_window(WindowType.W_MONEY)
            df = self._save_as_data(save_money, PositionType.MONEY,
                                    read_func=self.__read_data,
                                    pd_kvargs={"nrows": 1},
                                    file_postfix="TXT")
            money = Money(total=df.loc[0, "资产总值"], available=df.loc[0, "可用资金"])
            try:
                # 资金余额
                money.balance = df.loc[0, "资金余额"]
                # 股票市值
                money.market = df.loc[0, "总市值"]
                # 可取资金
                money.withdraw = df.loc[0, "可取资金"]
                # 可取资金
                money.profitLoss = df.loc[0, "盈亏"]
            except:
                pass
            log.info("账户：%s, 总资金：%.2f, 可用资金: %.2f", self.account.username, money.total, money.available)
            return money
        except Exception as e:
            delattr(self, "_money_window")
            log.exception(e)
        return Money(.0, .0)

    @fn_timer
    # 这里不需要重复尝试，防止买入重复
    def buy(self, stock_info: StockInfo) -> StockResult:
        try:
            self._select_open_window(WindowType.W_BUY)
            if hasattr(self, "_buy_window"):
                time.sleep(0.3)
                cw = self._buy_window.TFrmBuyStock
                cw = cw.child_window(class_name="TPanel", found_index=2)
                cw.Edit2.set_text(remove_code_prefix(stock_info.code))
                cw.Edit2.type_keys("{ENTER}")
                time.sleep(0.8)

                cw.Edit3.set_text(stock_info.price)
                cw.Edit1.set_text("")
                cw.Edit1.set_focus()
                wu.press(*str(int(stock_info.number)))
                time.sleep(0.5)

                # 委托按钮点击
                buy_btn = cw.child_window(title="委托[F3]", class_name="TButton")
                buy_btn.wait("enabled", timeout=5)
                buy_btn.click()
                time.sleep(0.3)
                # 关闭确认买入对话框
                p = PopupResult(self._close_popup_windows(), regex=".*编号[: ]*(\d+).*")
                log.info("账户：%s, 委托买入，股票：%s，价格:%.2f, 股数：%d, 合同编号：%s, 结果：%s",
                         self.account, stock_info.code, stock_info.price, stock_info.number, p.contract, p.texts)
                return StockResult.result_ok(p.contract, stock_info=stock_info) if p.is_success() else StockResult.result_error(p.text, stock_info=stock_info)
            else:
                raise AttributeError("%s 没有属性：%s", self.__class__.__name__, "_buy_window")
        except Exception as e:
            delattr(self, "_buy_window")
            log.exception(e)
            return StockResult.result_error(str(e), stock_info=stock_info)

    @fn_timer
    @retry(stop=stop_after_attempt(2),
           retry=retry_if_result(lambda x: x.state == StockResult.ERROR),
           after=after_log(log, logging.WARNING),
           retry_error_callback=lambda x: x.result())
    def sell(self, stock_info: StockInfo) -> StockResult:
        try:
            self._select_open_window(WindowType.W_SELL)
            if hasattr(self, "_sell_window"):
                time.sleep(0.3)
                cw = self._sell_window.Tfrm2007
                cw = cw.child_window(class_name="TPanel", found_index=2)

                cw.Edit2.set_text(remove_code_prefix(stock_info.code))
                cw.Edit2.type_keys("{ENTER}")
                time.sleep(0.8)
                cw.Edit3.set_text(stock_info.price)
                cw.Edit1.set_text("")
                cw.Edit1.set_focus()
                wu.press(*str(int(stock_info.number)))

                # 委托按钮点击
                buy_btn = cw.child_window(title="委托[F3]", class_name="TButton")
                buy_btn.wait("enabled", timeout=5)
                buy_btn.click()
                time.sleep(0.3)
                # 关闭确认买入对话框
                p = PopupResult(self._close_popup_windows(), regex=".*编号[: ]*([?|\d]+).*")
                log.info("账户：%s, 委托卖出，股票：%s，价格:%.2f, 股数：%d, 合同编号：%s, 结果：%s",
                         self.account, stock_info.code, stock_info.price, stock_info.number, p.contract, p.texts)
                return StockResult.result_ok(p.contract, stock_info=stock_info) if p.is_success() else StockResult.result_error(p.text, stock_info=stock_info)
            else:
                raise AttributeError("%s 没有属性：%s", self.__class__.__name__, "_sell_window")
        except Exception as e:
            delattr(self, "_sell_window")
            log.exception(e)
            return StockResult.result_error(str(e), stock_info=stock_info)

    def cancel_buy(self) -> bool:
        return self.cancel(cancel_type=StockInfo.TYPE_BUY)

    def cancel_sell(self) -> bool:
        return self.cancel(cancel_type=StockInfo.TYPE_SELL)

    @fn_timer
    @retry(stop=stop_after_attempt(2),
           retry=retry_if_result(lambda x: x == False),
           after=after_log(log, logging.WARNING),
           retry_error_callback=lambda x: x.result())
    def cancel(self, stock_codes: [] = None, entrust_nos: [] = None, cancel_type=None, exception_callback=None, **kwargs) -> bool:
        self._main_window.send_keystrokes("{F4}")
        if not hasattr(self, "_cancel_window"):
            self._cancel_window = self._get_trade_active_window()
            log.debug("撤单界面句柄：%x", self._cancel_window.handle)
        try:
            main_window = self._cancel_window.TFrmBatchWithDraw
            ctrl_window = main_window.child_window(class_name="TPanel", found_index=0)

            # 清除选中状态
            ctrl_window.child_window(title="全清", class_name="TButton").click()
            # 输出
            save_btn = lambda: ctrl_window.child_window(title="输出", class_name="TButton").click()
            wei_tuo = self._save_as_data(save_btn, PositionType.ENTRUST,
                                         pd_kvargs=dict(skipfooter=2),
                                         read_func=self.__read_data,
                                         file_postfix="TXT")
            if wei_tuo:
                list_window = main_window.child_window(class_name="TAdvStringGrid", found_index=0)
                select_indexs = []
                for obj in self._is_cancel(wei_tuo, stock_codes, entrust_nos, cancel_type):
                    select_indexs.append(obj.index)
                    log.debug("账号：%s，准备撤销：%s", self.account, obj)

                log.debug("账号：%s，需要撤销的委托数量为：%d", self.account, len(select_indexs))
                for index in select_indexs:
                    list_window.click(coords=(5, (index + 1) * 18 + 9))
                if len(select_indexs) > 0:
                    ctrl_window.child_window(title="撤单(F3)", class_name="TButton").click()
                    time.sleep(0.5)
                    self._close_popup_windows()
            return True
        except Exception as e:
            exception_msg = str(e)
            log.error("账户：%s，撤销：%s，类型：%s，异常！", self.account, stock_codes, StockInfo.operation_name(cancel_type))
            log.exception(e)
        if exception_msg and callable(exception_callback):
            exception_callback(exception_msg)
        return False

    def cancel_all(self) -> bool:
        try:
            self._main_window.send_keystrokes("{F4}")
            if not hasattr(self, "_cancel_window"):
                self._cancel_window = self._get_trade_active_window()
                log.debug("撤单界面句柄：%x", self._cancel_window.handle)

            # 撤销全部
            self._cancel_window.send_keystrokes("{F7}")
            time.sleep(0.5)
            self._close_popup_windows()
            return True
        except Exception as e:
            log.exception(e)
        return False

    def _save_file(self, file_path):
        """
        另存为 弹框，将数据另存为文件。 这个方法需要另行捕获异常信息
        :param file_path: 文件路径
        :return:
        """
        # 如果文件存在
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                self._close_notepad(file_path)

        file_dialog = self._app.window(title="输出选择", top_level_only=True, visible_only=True)
        if not file_dialog.exists(timeout=3):
            log.warning("国海证券----输出数据到文件，没有弹出选择文件弹框！文件：%s", os.path.basename(file_path))
            raise WindowNotFoundError("国海证券-----没有输出弹框！")

        # 多次点击输出框
        out_file = file_dialog['输出到文件']
        txt = file_dialog['文本']
        for i in range(3):
            try:
                out_file.check_by_click()
                pw.timings.wait_until(5, 0.1, lambda: txt.is_enabled())
                txt.check_by_click()
                break
            except TimeoutError as e:
                self._close_notepad(file_path)

        file_dialog.Edit1.set_text(file_path)
        file_dialog['确定(&O)'].click()
        time.sleep(0.3)
        confirm_dialog = self._app.window(title="确认", top_level_only=True)
        if confirm_dialog.exists():
            confirm_dialog['是'].click()
        self._close_notepad(file_path)

    def _close_notepad(self, file_path=None):
        try:
            if file_path is None:
                os.system("taskkill /T /F /IM notepad.exe")
            else:
                # 关闭输出弹框
                notepads = pw.findwindows.find_windows(title="%s - 记事本" % (os.path.basename(file_path).upper()))
                if notepads:
                    for notepad in notepads:
                        win32api.SendMessage(notepad, win32con.WM_CLOSE, 0, 0)
        except Exception as e:
            log.exception(e)

    def _close_save_as(self):
        # 关闭另存为窗口
        try:
            file_dialogs = self._app.windows(title="输出选择", top_level_only=True)
            for fd in file_dialogs:
                fd.close()
        except:
            pass

    def _close_public_info(self):
        code = 1
        # 关闭公告弹框
        for name in ["TfrmDialogs", "TfrmShowPublicInfo"]:
            try:
                info_window = self._app.window(class_name=name)
                info_window.wait("visible", timeout=5)
                if info_window.is_visible():
                    if info_window.window_text() == "错误":  # 错误提示信息
                        code = -1
                    if info_window['TCheckBox'].exists(timeout=1):
                        info_window['TCheckBox'].check_by_click()
                    if info_window['TButton'].exists(timeout=1):
                        info_window['TButton'].click()
                    elif info_window['确定(&O)'].exists(timeout=1):
                        info_window['确定(&O)'].click()
                time.sleep(1)
            except TimeoutError as e:
                log.debug("国海证券----没有显示公告窗口！")
            except Exception as e:
                log.exception(e)
        return code


