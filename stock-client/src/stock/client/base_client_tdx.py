import abc
import os
import time
from abc import abstractmethod

import pywinauto as pw
import win32api
import win32con
import win32process
from pywinauto import timings
from pywinauto.application import WindowSpecification
from pywinauto.findwindows import WindowNotFoundError
from pywinauto.timings import TimeoutError
from pywinauto.keyboard import send_keys

from src.stock.client.base_client import BaseClient, log, ImgType, fn_timer, logging, WindowType
from src.stock.bean.position_type_conf import get_brokers_conf
from src.stock.bean.stock_bean import PositionType, Money, remove_code_prefix, Account, StockInfo, StockResult, PopupResult, BaseStock
from src.stock.client.exceptions import QueryPositionException
from src.utils import windows_utils as wu
from src.utils.code_utils import code_to_str
from src.utils.config import conf
from src.utils.win32_utils import get_handle
from tenacity import retry, retry_if_result, stop_after_attempt, after_log, retry_if_exception_type


class BaseClientTDX(BaseClient, metaclass=abc.ABCMeta):
    """
    通达信----基础抽象类
    """

    @abstractmethod
    def _get_window_conf(self):
        """
        选择窗口的配置信息
        :return:
        """
        pass

    @fn_timer
    def login(self, account: Account) -> bool:
        self.account = account
        if self._is_login(account):
            # 如果已经登录过直接切换账户
            return self._change_account(account)
        else:
            # 没有这添加账户
            return self._login_account(account)

    @fn_timer
    @retry(stop=stop_after_attempt(2),
           retry=retry_if_result(lambda x: x.state == StockResult.ERROR),
           after=after_log(log, logging.WARNING),
           retry_error_callback=lambda x: x.result())
    def sell(self, stock_info: StockInfo) -> StockResult:
        try:
            self._select_open_window(WindowType.W_SELL)
            if hasattr(self, "_sell_window"):
                code_filed = self._sell_window.AfxWnd42
                code_filed.click_input()
                send_keys("{END}" + ("{BACKSPACE}" * 8))
                send_keys(remove_code_prefix(stock_info.code))
                time.sleep(0.3)
                self._sell_window.Edit1.set_edit_text(stock_info.price)
                self._sell_window.Edit2.set_edit_text(int(stock_info.number))
                time.sleep(0.3)
                # 卖出下单或者融券下单
                for x in ['卖出下单', '融券下单']:
                    try:
                        sell_btn = self._sell_window[x]
                        sell_btn.wait("exists enabled", timeout=5)
                        sell_btn.click()
                        break
                    except TimeoutError as t:
                        log.exception(t)
                time.sleep(0.2)
                p = PopupResult(self._close_popup_windows(), regex=self._get_contract_regex())
                log.info("账号：%s，委托卖出，股票：%s，价格:%.2f, 股数：%d，合同编号：%s, 结果：%s",
                         self.account, stock_info.code, stock_info.price, stock_info.amount, p.contract, p.texts)
                return StockResult.result_ok(p.contract, stock_info=stock_info) if p.is_success() else StockResult.result_error(p.text, stock_info=stock_info)
            else:
                raise AttributeError("%s 没有属性：%s", self.__class__.__name__, "_sell_window")
        except Exception as e:
            self._close_popup_windows()
            delattr(self, "_sell_window")
            log.exception(e)
            return StockResult.result_error(str(e), stock_info=stock_info)

    @fn_timer
    def buy(self, stock_info: StockInfo) -> StockResult:
        try:
            self._select_open_window(WindowType.W_BUY)
            if hasattr(self, "_buy_window"):
                code_filed = self._buy_window.AfxWnd42
                code_filed.click_input()
                send_keys("{END}" + ("{BACKSPACE}" * 8))
                send_keys(remove_code_prefix(stock_info.code))
                time.sleep(0.3)
                self._buy_window.Edit1.set_edit_text(stock_info.price)
                self._buy_window.Edit2.set_edit_text(int(stock_info.number))
                time.sleep(0.3)
                buy_btn = self._buy_window['买入下单']
                buy_btn.wait("enabled", timeout=5)  # 等待下单按钮可用
                buy_btn.click()
                time.sleep(0.2)
                p = PopupResult(self._close_popup_windows(timeout=0.5), regex=self._get_contract_regex())
                log.info("账号：%s，委托买入，股票：%s，价格:%.2f, 股数：%d，合同编号: %s, 结果：%s",
                         self.account, stock_info.code, stock_info.price, stock_info.number, p.contract, p.texts)
                if p.is_success():  # 包含合同号，处理成功
                    return StockResult.result_ok(p.contract, stock_info=stock_info)
                elif self.__has_wei_tuo(stock_info):  # 查询委托信息，确认是否委托成功
                    return StockResult.result_ok(p.contract, stock_info=stock_info)
                return StockResult.result_error(p.text, stock_info=stock_info)
            else:
                raise AttributeError("%s 没有属性：%s", self.__class__.__name__, "_buy_window")
        except Exception as e:
            self._close_popup_windows()
            delattr(self, "_buy_window")
            log.exception(e)
            return StockResult.result_error(str(e), stock_info=stock_info)

    def _get_contract_regex(self):
        """
        合同编号获取正则表达式
        """
        return ".*合同号是(\\d+).*"

    @fn_timer
    def money(self, exception_callback=None, **kwargs) -> Money:
        exception_msg = None
        try:
            file_name = "%s_%s_%s.txt" % (PositionType.MONEY.name, self.account.username, conf.now)
            file_path = os.path.join(conf.root_path, "data", "position", file_name)
            self._select_open_window(WindowType.W_POSITION)
            if self._out_data("_position_window", file_path):
                return self._get_money(file_path)
        except Exception as e:
            exception_msg = str(e)
            log.exception(e)
        if exception_msg and callable(exception_callback):
            exception_callback(exception_msg)
        return Money(.0, .0)

    @fn_timer
    def position(self, position_type: PositionType, retry=3, exception_callback=None,  **kwargs) -> list:
        exception_msg = None
        file_name = "%s_%s_%s.txt" % (position_type.name, self.account.username, conf.now)
        file_path = os.path.join(conf.root_path, "data", "position", file_name)
        # 持仓信息，需要获取三次，防止获取失败
        for i in range(retry):
            try:
                if PositionType.POSITION == position_type:
                    self._select_open_window(WindowType.W_POSITION)
                    if self._out_data("_position_window", file_path):
                        return self._get_position(file_path, position_type, head_line=3)
                elif PositionType.DEAL == position_type:
                    self._select_open_window(WindowType.W_DEAL)
                    if self._out_data("_deal_window", file_path):
                        return self._get_position(file_path, position_type, head_line=2)
                elif PositionType.ENTRUST == position_type:
                    self._select_open_window(WindowType.W_ENTRUST)
                    if self._out_data("_entrust_window", file_path):
                        return self._get_position(file_path, position_type, head_line=2)
            except Exception as e:
                if isinstance(e, QueryPositionException):  # 仓位查询太频繁
                    retry = 5
                else:
                    exception_msg = str(e)
                log.warning("账号：%s，获取：%s失败，重试：%d/%d", self.account, position_type.name, i + 1, retry)
                log.exception(e)

        if exception_msg and callable(exception_callback):
            exception_callback(exception_msg)

        log.warning("账号：%s，获取：%s失败!", self.account, position_type.name)
        return []

    @fn_timer
    def cancel_buy(self) -> bool:
        return self.cancel(cancel_type=StockInfo.TYPE_BUY)

    @fn_timer
    def cancel_sell(self) -> bool:
        return self.cancel(cancel_type=StockInfo.TYPE_SELL)

    @fn_timer
    def cancel_all(self) -> bool:
        try:
            self._select_open_window(WindowType.W_CANCEL)
            if hasattr(self, "_cancel_window"):
                opt_wd = self._cancel_window
                btns = ['刷 新', '全选中', '撤 单']
                for btn in btns:
                    refresh = opt_wd[btn]
                    refresh.wait("enabled", timeout=5)
                    refresh.click()
                time.sleep(0.5)
                self._close_popup_windows()
                log.info("账号：%s, 撤销所有委托！", self.account)
                return True
            else:
                raise AttributeError("%s 没有属性：%s", self.__class__.__name__, "_cancel_window")
        except Exception as e:
            log.exception(e)
        return False

    @fn_timer
    @retry(stop=stop_after_attempt(3),
           retry=retry_if_result(lambda x: x == False),
           after=after_log(log, logging.WARNING),
           retry_error_callback=lambda x: x.result())
    def cancel(self, stock_codes: [] = None, entrust_nos: [] = None, cancel_type=None, exception_callback=None, **kwargs) -> bool:
        exception_msg = None
        self._select_open_window(WindowType.W_CANCEL)
        if hasattr(self, "_cancel_window"):
            try:
                file_path = os.path.join(conf.root_path, "data", "position", "委托_%s_%s.txt" % (self.account.username, conf.now))
                if not self._out_data("_cancel_window", file_path):
                    return False
                p_list = self._get_position(file_path, position_type=PositionType.ENTRUST, head_line=2)
                if p_list and len(p_list) > 0:
                    list_view = self._cancel_window.SysListView32
                    select_indexs = []
                    for obj in self._is_cancel(p_list, stock_codes, entrust_nos, cancel_type):
                        select_indexs.append(obj.index)
                        log.debug("账号：%s，准备撤销：%s", self.account, obj)

                    log.debug("账号：%s，需要撤销的委托数量为：%d", self.account, len(select_indexs))
                    for index in select_indexs:
                        list_view.click(coords=(5, list_view.get_item_rect(index).top + 4))
                    if len(select_indexs) > 0:
                        self._cancel_window['撤 单'].click()
                        time.sleep(0.5)
                        self._close_popup_windows()
                return True
            except Exception as e:
                exception_msg = str(e)
                log.exception(e)
        if exception_msg and callable(exception_callback):
            exception_callback(exception_msg)
        return False

    @fn_timer
    def _get_position(self, file_path, position_type, head_line):
        """
        获取持仓信息
        :param file_path:
        :param position_type:
        :param head_line:  索引号从0开始
        :return: 返回的仓位信息不包含股票代码前缀
        """

        def pre_callback(contents, head_line, position_type) -> bool:
            start_line = str(contents[head_line + 1]).strip()
            if "没有相应的查询信息" in start_line:
                return True
            if "温馨提示" in start_line:
                raise QueryPositionException(position_type, start_line)
            return False

        df = self._read_file(file_path, head_line, position_type, pre_callback=pre_callback)
        return BaseStock.read(df, get_brokers_conf(self.account.broker, position_type))

    @fn_timer
    def _get_money(self, file_path) -> Money:
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="GBK") as f:
                content = f.readline()[5:]
                log.info("账户；%s, 资产:%s", self.account, content)
                moneys = {}
                for m in content.split("  "):
                    k, v = m.split(":")
                    moneys[k] = v
                money = Money(total=moneys['资产'], available=moneys['可用'])
                try:
                    money.balance = moneys['余额']
                    money.market = moneys['参考市值']
                    money.withdraw = moneys['可取']
                    money.profitLoss = moneys['盈亏']
                except:
                    pass
                return money
        else:
            log.warn("获取账户资金失败，文件:%s不存在！", file_path)
        return Money(total=.0, available=.0)

    @fn_timer
    @retry(stop=stop_after_attempt(2),
           retry=retry_if_exception_type(Exception),
           after=after_log(log, logging.WARNING))
    def _select_window(self, window_type: WindowType):
        self._close_popup_windows()  # 关闭所有弹框
        self._max_window()
        self._unlock()  # 防止操作界面被锁定
        w = self._get_window_conf()[window_type]
        self._select_init_window(window_type, w['item'])

    @fn_timer
    def _select_init_window(self, window_type: WindowType, item):
        tree_view = self._trade_window['SysTreeView32']
        tree_view.item(item).click_input()
        time.sleep(0.5)

        w_window = "%s_window" % window_type.value
        if not hasattr(self, w_window):
            detail_window = self._trade_window.window(control_id=0xE901)
            handle = detail_window.window(class_name="#32770", visible_only=True, found_index=0).handle
            content_window = self._app.window(handle=handle)
            self.__setattr__(w_window, content_window)
            log.debug("%s界面句柄：%x", window_type, self.__getattribute__(w_window).handle)

    @fn_timer
    def _reset(self, title, exe_path):
        self.title = title
        self._main_hwnd = get_handle(title, exe_path)
        thread_id, processId = win32process.GetWindowThreadProcessId(self._main_hwnd)
        self._app = pw.Application(backend="win32").connect(process=processId)
        log.info("启动%s，句柄：%x,进程ID:%x", title, self._main_hwnd, processId)
        self._main_window = self._app.window(title_re="%s.+" % title)
        # 网上交易主窗口
        self._trade_window = self._app.window(title_re="%s.*" % "通达信网上交易", top_level_only=False, visible_only=False)

    @fn_timer
    def _match_account(self, account, is_selected=False) -> bool:
        """
        匹配并选择账户
        :param account: 需要匹配或者选择的账户
        :param is_selected: 是否切换账户，True 切换，False 不切换
        :return: True 已登录，False 未登录
        """
        # 交易窗口不可用
        if self._trade_window.exists() and not self._trade_window.is_visible():
            log.info("交易已经最小化，按F12最大化窗口！")
            self._main_window.type_keys("{F12}")  # 交易窗口显示

        if not self._trade_window.exists() or not self._trade_window.is_visible():
            return False

        self._max_window()
        self._unlock()  # 防止操作界面被锁定
        account_ComboBox = self._trade_window.MainViewBarMHPToolBar.ComboBox
        result_text = None
        for text in account_ComboBox.item_texts():
            if text.find(account.username) != -1:
                result_text = text
                if is_selected and account_ComboBox.is_visible():
                    account_ComboBox.select(text)
                    log.info("切换账号：%s", text)
                else:
                    log.info("账号：%s已登录无需切换！", account)
                break
        return result_text is not None

    @fn_timer
    def _is_login(self, account: Account) -> bool:
        return self._match_account(account, is_selected=False)

    @fn_timer
    def _change_account(self, account: Account) -> bool:
        result = self._match_account(account, is_selected=True)
        time.sleep(0.5)
        self._refresh_window()
        return result

    @fn_timer
    def _login_add(self, account: Account) -> bool:
        # 使用添加新账户的方式，登录
        if not (self._trade_window.exists() and self._trade_window.is_visible()):
            log.info("%s-----主界面没有打开，不能添加账户！", self.support_brokers())
            return False
        return False

    @fn_timer
    def _login_account(self, account: Account) -> bool:
        # 以下代码为从初始登录页面登录，并不包含添加第二个账号
        try:
            log.info("%s----登录账户：%s", account.broker, account.username)

            # 判断是否需要已添加方式登录
            if self._login_add(account):
                return True

            for i in range(2):
                self._main_window.Edit1.set_focus()
                self._main_window.Edit1.set_text("")
                wu.press(*account.username)
                time.sleep(0.3)

                # 设置密码
                self._main_window.Edit2.set_focus()
                self._main_window.Edit2.set_text("")
                wu.press(*account.password)
                time.sleep(0.3)

                # 设置验证码
                codeEdit = self._code_edit()
                if codeEdit.exists() and codeEdit.is_visible():
                    for j in range(5):
                        rect = codeEdit.rectangle()
                        code = code_to_str((rect.right + 3, rect.top, rect.right + 60, rect.bottom), img_type=ImgType.tdx)
                        log.info("%s----自动识别验证码:%s", account.broker, code)
                        if code:
                            codeEdit.set_focus()
                            codeEdit.set_text("")
                            wu.press(*code)
                            time.sleep(0.3)
                        else:
                            log.error("%s---------识别验证码失败！", account.broker)
                        if self._is_ok_code():
                            break
                try:
                    self._main_window.type_keys("{ENTER}")
                    timings.wait_until(30, 0.5, lambda: self._trade_window.exists() and self._trade_window.is_visible())
                except Exception as e:
                    log.exception(e)

                # 再次判断是否登录成功，成功则返回
                if self._is_login(account):
                    break
                log.info("账号：%s，尝试登录：%d/%d次", account, i + 1, 3)
            self._refresh_window()
            return True
        except Exception as e:
            raise e

    def _is_ok_code(self) -> bool:
        """
        校验验证码是否合法
        """
        return True

    def _code_edit(self):
        """
        验证码输入框位置
        """
        return self._main_window.Edit3

    @fn_timer
    def _close_message_dialog(self):
        """
        关闭消息中心弹框
        :return: None
        """
        msg_dialog = self._app.window(title="%s消息中心" % self.support_brokers()[0])
        if msg_dialog.exists() and msg_dialog.is_visible():
            try:
                msg_dialog.click(coords=(msg_dialog.client_rect().right - 23, 9))
            except:
                msg_dialog.minimize()
            log.debug("关闭消息中心！")

    def login_retry(self, account, retry=5) -> bool:
        return super().login_retry(account, retry)

    @fn_timer
    def _refresh_window(self):
        windows = [WindowType.W_BUY, WindowType.W_SELL, WindowType.W_CANCEL, WindowType.W_POSITION, WindowType.W_DEAL, WindowType.W_MONEY]
        for w in windows:
            if hasattr(self, "%s_window" % w.value):
                delattr(self, "%s_window" % w.value)
        self._close_message_dialog()
        # 最大化交易窗口
        self._max_trade_window()

    @fn_timer
    def _max_trade_window(self):
        """
        最大化交易界面
        :return:
        """
        log.debug("最大化交易窗口！")
        try:
            trade_window_rect = self._trade_window.rectangle()
            if trade_window_rect.top > 50:
                tool_bar = self._trade_window.MainViewBarMHPToolBar
                if isinstance(tool_bar, WindowSpecification) and tool_bar.exists():
                    rect = tool_bar.client_rect()
                    tool_bar.click(coords=(rect.right - 26, 18))
        except Exception as e:
            log.warn("%s--------设置交易窗口最大化失败！", self.support_brokers()[0])
        log.debug("最大化交易窗口！----结束！")

    @fn_timer
    def __close_save_as(self):
        # 关闭另存为窗口
        try:
            file_dialogs = self._app.windows(title="输出", top_level_only=True)
            for fd in file_dialogs:
                fd.close()
        except:
            pass

    @fn_timer
    def _save_file(self, file_path):
        # 保存文件到指定路径
        file_dialog = self._app.window(title="输出", top_level_only=True, visible_only=True)
        if not file_dialog.exists():
            raise WindowNotFoundError("没有找到输出窗口！")

        # 如果文件存在
        if os.path.exists(file_path):
            os.remove(file_path)
            log.info("删除文件------%s", file_path)

        # 关闭记事本弹窗
        for i in range(3):
            try:
                if file_dialog.exists() and file_dialog.is_visible():
                    file_dialog['输出到文本文件'].check_by_click()
                    file_dialog.Edit1.set_text(file_path)
                    file_dialog['确 定'].click()
                    time.sleep(0.5)
                    try:
                        notepads = pw.findwindows.find_windows(title="%s - 记事本" % (os.path.basename(file_path)))
                        if notepads:
                            for notepad in notepads:
                                win32api.SendMessage(notepad, win32con.WM_CLOSE, 0, 0)
                    except Exception as e:
                        from src.utils.win32_utils import find_handle
                        handle = find_handle(title="%s - 记事本" % (os.path.basename(file_path)))
                        win32api.SendMessage(handle, win32con.WM_CLOSE, 0, 0)

                else:
                    log.warn("导出----导出弹框不可用！")
                return  # 正常情况只执行一次，记事本弹窗找不到，则再次尝试
            except WindowNotFoundError:
                log.info("没有找到需要关闭的记事本程序！重试：%d/%d", i + 1, 3)

    @fn_timer
    def _out_data(self, opt_window, file_path) -> bool:
        if hasattr(self, opt_window):
            for i in range(2):
                try:
                    self.__close_save_as()
                    opt_wd = getattr(self, opt_window)
                    refresh = opt_wd['刷 新']
                    refresh.wait("enabled", timeout=3)
                    refresh.click()
                    refresh.wait("enabled", timeout=5)

                    out = opt_wd['输 出']
                    if refresh.is_enabled() and not out.is_enabled():
                        log.info("界面：%s,刷新可用，输出不可用！", opt_window)
                        return False
                    time.sleep(1)  # 暂停1秒目的是让数据加载出来
                    out.wait("enabled", timeout=2)
                    out.click()

                    self._save_file(file_path)
                    return True
                except TimeoutError:
                    log.info("界面：%s, 刷新或者输出不可用，不能输出数据！", opt_window)
                    return False
                except Exception as e:
                    log.info("界面：%s, 导出数据异常，重试：%d/%d", opt_window, i + 1, 2)
                    log.exception(e)
        return False

    @fn_timer
    def _is_locked(self) -> bool:
        """
        判断交易界面是否被锁定了
        :return: True 锁定，False 未锁定
        """
        try:
            lock_window = self._trade_window.window(class_name="#32770", found_index=0, top_level_only=True)
            if not lock_window.exists() or not lock_window.is_visible():
                return False

            if lock_window.Static.exists():
                return "交易界面已锁定" in lock_window.Static.window_text()
            return False
        except Exception as e:
            log.exception(e)
            return False

    @fn_timer
    def _unlock(self, retry=10):
        # 交易窗口不可用
        if self._trade_window.exists() and not self._trade_window.is_visible():
            self._main_window.type_keys("{F12}")  # 交易窗口显示
        if not self._is_locked():
            return
        lock_window = self._trade_window.window(class_name="#32770", found_index=0)
        # 输入验证码，并点击确认
        codeEdit = lock_window.child_window(class_name="Edit")
        for i in range(retry):
            self._close_message_dialog()
            # 设置密码
            lock_window.AfxWnd42.set_focus()
            wu.press(*self.account.password)
            # 输入验证码
            if codeEdit.exists() and codeEdit.is_visible():
                self._close_popup_windows()
                time.sleep(0.5)
                rect = codeEdit.rectangle()
                code = code_to_str((rect.right + 3, rect.top, rect.right + 60, rect.bottom), img_type=ImgType.tdx)
                codeEdit.set_text(code)
            lock_window.child_window(title="确定", class_name="Button").click()
            time.sleep(1)
            self._close_popup_window()
            if not self._is_locked():
                return
            log.info("锁定------验证码错误，准备重新尝试：%d/%d", i + 1, retry)

    def _close_popup_windows(self, timeout: float = -0.1, handle_map=None, close_foreach=False) -> dict:
        return super()._close_popup_windows(timeout, handle_map, close_foreach=close_foreach)

    def __has_wei_tuo(self, stock_info):
        """
        查询股票是否已经在委托列表中
        :param stock_info 委托的股票信息
        """
        map_wei_tuo = self.position(PositionType.ENTRUST)
        code = remove_code_prefix(stock_info.code)
        if map_wei_tuo and code in map_wei_tuo:
            cj_list = map_wei_tuo[code]
            cj_list = cj_list if isinstance(cj_list, list) else [cj_list]
            for cj in cj_list:
                if cj.operation.find(StockInfo.operation_name(stock_info.type)) != -1:
                    return True
        return False
