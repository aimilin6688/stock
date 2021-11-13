import os
import time
import re
import pywinauto as pw
import pandas as pd
from pandas.errors import EmptyDataError

from pywinauto.findwindows import WindowNotFoundError, ElementAmbiguousError
from pywinauto import clipboard, timings
from src.utils.config import conf
from src.stock.client.base_client import BaseClient, log, LoginException, ImgType, fn_timer, logging, WindowType
from src.stock.bean.stock_bean import PositionType, Money, BaseStock, remove_code_prefix, Account, StockInfo, StockResult, PopupResult
from src.utils.win32_utils import find_window_by_thread, get_handle
from src.stock.bean.position_type_conf import get_brokers_conf
from src.utils.code_utils import code_to_str
from src.stock.client.exceptions import SaveFileSuccess
from tenacity import retry, retry_if_result, stop_after_attempt, after_log
from collections import OrderedDict


class Client10jqka(BaseClient):
    """
    1. 买入卖出价、数量设置为空
    2. 快速交易：委托成功后是否弹出提示框：是， 切换页面清空代码：是，撤单前是否需要确认：否
    3. 界面设置：最小化窗口到：任务栏，是否悬浮工具栏：否
    4. 多账户下拉列表中，编辑账户 -> 启用账户备注方案（勾选）,注意：备注名称要与nickname名称一致
    5. 中信证券持仓中，将"成本价1" -> "买入成本价"
    """

    @fn_timer
    def _after_init(self):
        self.title = "网上股票交易系统5.0"
        self._main_hwnd = get_handle(self.title, self._get_exe())
        self._app = pw.Application(backend="win32").connect(handle=self._main_hwnd)
        log.info("启动同花顺下单客户端，句柄：%x", self._main_hwnd)

        self._main_window = self._app.window(title=self.title)
        try:
            # 悬浮工具条窗口句柄, 这个需要在设置中取消
            self._main_dialog_handles = [x.handle for x in self._app.windows(class_name="#32770", visible_only=True)]
        except:
            self._main_dialog_handles = []

    # 可执行文件路径
    def _get_exe(self):
        return self.account.exePath

    def _get_trade_window(self):
        return self._main_window.window(class_name="AfxMDIFrame42s", top_level_only=False, found_index=0)

    @fn_timer
    def _refresh_hwnd(self):
        # 依次打开其他界面
        self._trade_window = self._get_trade_window()

        # 需要重新初始化窗口句柄
        for w in [WindowType.W_BUY.value, WindowType.W_SELL.value, WindowType.W_MONEY.value]:
            if hasattr(self, "%s_window" % w):
                delattr(self, "%s_window" % w)

    @fn_timer
    def login(self, account: Account) -> bool:
        self.account = account
        if self._is_login(account):
            # 如果已经登录过直接切换账户
            return self._change_account(account)
        else:
            # 没有这添加账户
            return self._login_account(account)

    def __reset(self, window):
        # 重置输入的信息
        if hasattr(self, window):
            reset_btn = getattr(self, window)['重填']
            try:
                reset_btn.wait("enabled", timeout=5)
                reset_btn.click()
            except Exception as e:  # 元素可能不可用，或者没有找到该元素
                log.exception(e)
                delattr(self, window)  # 删除页面属性，重新获取属性
                self._close_popup_windows()  # 关闭所有弹框
                self._select_open_window(WindowType.W_BUY)
                self._refresh_position()
                reset_btn.click()

    @fn_timer
    def buy(self, stock_info: StockInfo) -> StockResult:
        """
        买入
        :param stock_info:
        :return:
        """
        try:
            self._select_open_window(WindowType.W_BUY)
            if hasattr(self, "_buy_window"):
                self.__reset("_buy_window")
                time.sleep(0.1)
                self._buy_window.Edit1.type_keys(remove_code_prefix(stock_info.code))

                time.sleep(0.2)  # 主要是加载股票信息
                self._buy_window.Edit2.type_keys(stock_info.price)
                self._buy_window.Edit3.type_keys(int(stock_info.number))
                time.sleep(0.2)
                self._buy_window.Edit3.type_keys("{ENTER}")

                # 关闭确认买入对话框
                p = self.__popup_result()
                log.info("账号：%s，委托买入，股票：%s，价格:%.2f, 股数：%d, 合同编号：%s, 结果：%s",
                         self.account, stock_info.code, stock_info.price, stock_info.number, p.contract, p.texts)
                return StockResult.result_ok(p.contract, stock_info=stock_info) if p.is_success() else StockResult.result_error(p.text, stock_info=stock_info)
            else:
                raise AttributeError("%s 没有属性：%s", self.__class__.__name__, "_buy_window")
        except Exception as e:
            log.exception(e)
            delattr(self, "_buy_window")  # 删除页面属性，重新获取属性
            return StockResult.result_error(str(e), stock_info=stock_info)

    def __popup_result(self) -> PopupResult:
        # 关闭确认买入对话框, # 中信证券弹出确定，没有点击问题
        p = PopupResult(self._close_popup_windows())
        for i in range(3):
            if p and p.title == "委托确认":
                p = PopupResult(self._close_popup_windows())
            else:
                break
        return p

    @fn_timer
    @retry(stop=stop_after_attempt(1),
           retry=retry_if_result(lambda x: x.state == StockResult.ERROR),
           after=after_log(log, logging.WARNING),
           retry_error_callback=lambda x: x.result())
    def sell(self, stock_info: StockInfo) -> StockResult:
        """
        卖出
        :param stock_info:
        :return:
        """
        try:
            self._select_open_window(WindowType.W_SELL)
            if hasattr(self, "_sell_window"):
                self.__reset("_sell_window")
                time.sleep(0.1)
                self._sell_window.Edit1.type_keys(remove_code_prefix(stock_info.code))

                time.sleep(0.2)
                self._sell_window.Edit2.type_keys(stock_info.price)

                sellEdit = self._sell_window.Edit3
                if sellEdit.is_enabled():  # 有可能卖出被锁定，锁定则不设置卖出仓位，直接卖
                    sellEdit.type_keys(int(stock_info.number))
                sellEdit.type_keys("{ENTER}")
                time.sleep(0.2)

                # 关闭确认买入对话框
                p = self.__popup_result()
                log.info("账号：%s，委托卖出，股票：%s，价格:%.2f, 股数：%d, 合同编号：%s, 结果：%s",
                         self.account, stock_info.code, stock_info.price, stock_info.number, p.contract, p.texts)
                return StockResult.result_ok(p.contract, stock_info=stock_info) if p.is_success() else StockResult.result_error(p.text, stock_info=stock_info)
            else:
                raise AttributeError("%s 没有属性：%s", self.__class__.__name__, "_sell_window")
        except Exception as e:
            log.exception(e)
            delattr(self, "_sell_window")  # 删除页面属性，重新获取属性
            return StockResult.result_error(str(e), stock_info=stock_info)

    @fn_timer
    def money(self, retry=2, exception_callback=None, **kwargs) -> Money:
        exception_msg = None
        for i in range(retry):
            try:
                self._select_open_window(WindowType.W_MONEY)
                self._refresh_position()  # 刷新界面，防止获取不到资金信息
                money = Money()
                if hasattr(self, "_money_window"):
                    # 可用资金
                    money.available = float(self._money_window.child_window(control_id=0x3F8).window_text())
                    # 总资金
                    money.total = float(self._money_window.child_window(control_id=0x3F7).window_text())
                    try:
                        # 资金余额
                        money.balance = float(self._money_window.child_window(control_id=0x3F4).window_text())
                        # 股票市值
                        money.market = float(self._money_window.child_window(control_id=0x3F6).window_text())
                        # 可取资金
                        money.withdraw = float(self._money_window.child_window(control_id=0x3F9).window_text())
                        # 盈亏
                        money.profitLoss = float(self._money_window.child_window(control_id=0x403).window_text())
                    except:
                        pass
                    log.info("账户：%s, 总资金：%.2f, 可用资金: %.2f", self.account, money.total, money.available)
                else:
                    log.error("%s 没有属性：%s", self.__class__.__name__, "_money_window")
                return money
            except Exception as e:
                exception_msg = str(e)
                delattr(self, "_money_window")
                log.error("账户：%s，获取资金信息异常，%s", self.account, str(e))
                log.exception(e)
        if exception_msg and callable(exception_callback):
            exception_callback(exception_msg)
        return Money()

    def _get_position_key(self):
        # 仓位切换快捷键
        return {PositionType.POSITION: "{F6}", PositionType.DEAL: "{F7}", PositionType.ENTRUST: "{F8}"}

    @fn_timer
    def position(self, position_type: PositionType, retry: int = 2, exception_callback=None, **kwargs) -> list:
        exception_msg = None
        for i in range(retry):
            try:
                self._select_open_window(WindowType.W_BUY)
                if hasattr(self, "_buy_window"):
                    key = self._get_position_key()
                    self._buy_window.send_keystrokes(key[position_type])
                    time.sleep(0.3)
                    self._refresh_position()
                result = self._get_position_data(position_type)
                if result and len(result) > 0 and BaseStock.is_position_type(result, position_type):
                    return result
            except Exception as e:
                exception_msg = str(e)
                log.warning("账号：%s，获取：%s失败，重试：%d/%d", self.account, position_type.name, i + 1, retry)
                log.exception(e)
        if exception_msg and callable(exception_callback):
            exception_callback(exception_msg)
        log.warning("账号：%s，获取：%s失败!", self.account, position_type.name)
        return []

    @fn_timer
    def cancel_buy(self) -> bool:
        return self._cancel("撤买")

    @fn_timer
    def cancel_sell(self) -> bool:
        return self._cancel("撤卖")

    @fn_timer
    def cancel_all(self) -> bool:
        return self._cancel("全撤")

    @staticmethod
    def support_brokers():
        return ["模拟炒股", "平安证券", "长城证券", "恒泰证券", "光大证券", "中信证券", "海通证券", "东莞证券"]

    @fn_timer
    @retry(stop=stop_after_attempt(2),
           retry=retry_if_result(lambda x: x == False),
           after=after_log(log, logging.WARNING),
           retry_error_callback=lambda x: x.result())
    def cancel(self, stock_codes: [] = None, entrust_nos: [] = None, cancel_type=None, exception_callback=None, **kwargs) -> bool:
        try:
            p_list = self.position(PositionType.ENTRUST, exception_callback=exception_callback)
            if p_list and hasattr(self, "_buy_window"):
                list_view = self._buy_window.CVirtualGridCtrl
                select_indexs = []
                for obj in self._is_cancel(p_list, stock_codes, entrust_nos, cancel_type):
                    select_indexs.append(obj.index)
                    log.info("账号：%s，准备撤销：%s", self.account, obj)

                log.debug("账号：%s，需要撤销的委托数量为：%d", self.account, len(select_indexs))
                for index in select_indexs:
                    top = index * self._cancel_line_height() + int(self._cancel_line_height() / 2) + self._cancel_top_offset()
                    list_view.click(coords=(5, top))
                if len(select_indexs) > 0:
                    time.sleep(0.1)
                    cancel_btn = self._buy_window['撤单']
                    for i in range(3):  # 这里点击一次可能不管用,采用多次点击,超时就取消
                        try:
                            cancel_btn.wait("enabled", timeout=1)
                            cancel_btn.click()
                            time.sleep(0.5)
                        except pw.timings.TimeoutError as e:
                            break
                    self._close_popup_windows()
                else:
                    log.debug("账号：%s，没有需要撤销的委托!", self.account)
            return True
        except Exception as e:
            exception_msg = str(e)
            log.error("账户：%s，撤销stock_codes：%s，entrust_nos: %s,类型：%s，异常！",
                      self.account, stock_codes, entrust_nos, StockInfo.operation_name(cancel_type))
            log.exception(e)
        if exception_msg and callable(exception_callback):
            exception_callback(exception_msg)
        return False

    def _cancel_line_height(self) -> int:
        """
        撤销委托行高
        @return:
        """
        return 16

    def _cancel_top_offset(self) -> int:
        """
        撤销委托第一行离上方高度
        @return:
        """
        return 22

    @fn_timer
    def _refresh_position(self, count=1, sleep=0.1):
        tool_bar = self._main_window.ToolbarWindow32

        # 使用工具栏刷新功能
        if tool_bar.button_count() >= 4:
            # 点击刷新按钮
            refresh_btn = tool_bar.button(3)
        else:  # 使用持仓界面刷新功能
            if hasattr(self, "_buy_window"):
                refresh_btn = self._buy_window.child_window(control_id=0x8016, visible_only=True, found_index=0)
            else:
                raise AttributeError("证券：%s，没有属性：_buy_window！" % self.support_brokers())

        if refresh_btn.is_enabled():
            for i in range(count):
                time.sleep(sleep)
                refresh_btn.click()
                try:
                    timings.wait_until(10, 0.1, lambda: refresh_btn.is_enabled())
                except timings.TimeoutError as e:
                    log.warn("刷新按钮等待超时！")

    def _is_login(self, account: Account) -> bool:
        """
        判断账户是否已经登录，主要看是否在已登录列表中
        :param account:
        :return:
        """
        return self._match_account(account, is_selected=True)

    @fn_timer
    def _match_account(self, account: Account, is_selected=False) -> bool:
        """
        匹配并选择账户
        :param account: 需要匹配或者选择的账户
        :param is_selected: 是否切换账户，True 切换，False 不切换
        :return: True 已登录，False 未登录
        """
        if not self._main_window.exists() or not self._main_window.is_visible():
            # 主窗口界面没有打开
            return False
        # 主窗口最大化
        self._max_window()
        account_combo_box = self._main_window.ToolbarWindow32.child_window(control_id=0x912, visible_only=False)
        result_text = None
        items = account_combo_box.item_texts()

        for index, text in enumerate(items):
            if self._select_account(account.broker, account.nickname, text):
                result_text = text
                if is_selected and account_combo_box.is_visible():
                    account_combo_box.select(text)
                    self._main_window.type_keys("%%%d" % (index + 1))
                    log.info("切换账号：%s", text)
                else:
                    log.info("账号：%s已登录无需切换！", account)
                break
        return result_text is not None

    def _select_account(self, broker, nickname, text) -> bool:
        if nickname == text:
            return True

        if broker == "模拟炒股":
            nickname = nickname if nickname.startswith("UID_") else "UID_" + nickname
            if nickname.replace("UID_", "") == text:
                return True
            if "%s-%s**%s" % (broker, nickname[0:2], nickname[-2:]) == text:
                return True

        if len(nickname) == 2:  # 中文两个字名字
            pattern = "^%s-%s[*]$" % (broker, nickname[0])
        else:
            pattern = "^%s-%s(.*)+%s$" % (broker, nickname[0], nickname[-1])
        return re.match(pattern, text) is not None

    @fn_timer
    def _login_account(self, account: Account) -> bool:
        """
        添加账户
        :param account: True 添加账户成功，False 添加账户失败
        :return:
        """
        try:
            log.debug("账户：%s, 准备登录!", account)
            if self._main_window != None and self._main_window.is_visible():
                self.__main_window = self._app.window(title=self.title).ToolbarWindow32.child_window(control_id=0x69B).click()
                log.debug("同花顺----点击增加账户按钮！")
                time.sleep(1.5)

            # 查找登录窗口句柄
            login_hwnd = find_window_by_thread(self._main_hwnd, titles=["登录", "保存密码", "自动登录"])
            if login_hwnd is None:
                log.error("同花顺，没有查找到登录窗口！")
                raise WindowNotFoundError("主窗口句柄(%x)，登录窗口没有找到！" % self._main_hwnd)

            login_window = self._app.window(handle=login_hwnd, visible_only=False, top_level_only=True)
            # 确认同花顺是否支持证券公司
            if account.broker not in login_window.ComboBox1.item_texts():
                log.error("同花顺请添加证券公司！%s", account.broker)
                raise LoginException("请在同花顺中添加证券公司:%s" % account.broker)

            # 选择证券公司
            login_window.ComboBox1.select(account.broker)
            time.sleep(0.4)

            login_window.Edit1.set_text("")
            login_window.Edit1.type_keys(account.username)
            self._reset_username(login_window, account)
            login_window.Edit2.set_text("")
            login_window.Edit2.type_keys(account.password)
            time.sleep(0.3)

            handle_map = OrderedDict()
            # 确认验证码是否需要输入
            for i in range(5):
                if i > 0:
                    self._close_popup_windows(handle_map=handle_map)

                codeEdit = pw.findwindows.find_element(parent=login_hwnd, top_level_only=False, visible_only=False, control_id=0x3EB)
                if codeEdit.visible:
                    codeImg = pw.findwindows.find_element(parent=login_hwnd, top_level_only=False, visible_only=False, control_id=0x5DB)
                    code = code_to_str(codeImg.rectangle, img_type=ImgType.ths)
                    login_window.window(handle=codeEdit.handle).type_keys(code)
                    log.info("同花顺---自动识别验证码:%s", code)

                # 模拟盘通信密码
                if account.broker in ["模拟炒股", "海通证券"]:
                    login_window.Edit3.set_text("")
                    if hasattr(account, "com_password") and account.com_password:
                        login_window.Edit3.type_keys(account.com_password)
                    else:
                        login_window.Edit3.type_keys(account.password)

                time.sleep(0.8)
                login_window['登录'].click()
                time.sleep(5)
                self.__close_popup_window(account)
                if self._is_login(account):
                    break
                log.info("同花顺---账号：%s，尝试登录：%d/%d次", account, i + 1, 5)
            else:
                log.error("同花顺---自动登录失败，账号：%s,原因：%s", account, handle_map.values())
                raise LoginException("%s" % (PopupResult(handle_map).texts))

            self._close_popup_windows()
            log.info("同花顺---账号：%s，登录成功!", account)
            time.sleep(1.5)
            # 刷新界面句柄
            self._refresh_hwnd()
        except Exception as e:
            raise e
        return True

    def __close_popup_window(self, account: Account):
        """
        关闭登录之后的弹框
        """
        if account.broker in ["海通证券"]:
            self._close_popup_windows(btn_name="以后再说")
            time.sleep(3)
            self._close_popup_windows(btn_name="以后再说")

    def _reset_username(self, login_window, account: Account):
        """
        设置用户名，如果存在类似会自动选择，这个方法特殊处理
        :param login_window:
        :param account:
        :return:
        """
        texts = login_window.ComboBox3.item_texts()
        # 如果账号在登陆列表中，直接选择
        if account.username in texts:
            login_window.ComboBox3.select(account.username)
        else:
            for t in texts:
                if t in account.username:
                    login_window.Edit1.type_keys("{VK_END}" + account.username[len(t):])

    def _change_account(self, account: Account) -> bool:
        """
        已经登录则直接改变账户就好
        :param account:
        :return: True 改变账户成功，False 改变账户失败
        """
        # 刷新界面句柄
        self._refresh_hwnd()
        return True

    @fn_timer
    def _cancel(self, name) -> bool:
        """
        撤单
        :param name: 按钮名称
        :return: None
        """
        try:
            self._select_open_window(WindowType.W_BUY)
            if hasattr(self, "_buy_window"):
                btn = self._buy_window.child_window(title_re=name + ".*?")
                if btn.exists() and btn.is_enabled():
                    btn.click()
                    time.sleep(0.8)
                    self._close_popup_windows()
                else:
                    log.info("账户：%s，没有需要【%s】的股票！", self.account, name)
                return True
        except Exception as e:
            log.exception(e)
        return False

    def _get_trade_active_window(self):
        return self._app.window(handle=self._trade_window.window(class_name="#32770", visible_only=True, found_index=0).handle)

    @fn_timer
    def _select_window(self, w_type: WindowType):
        """
        选中某个界面
        1. 如果子类有方法，_select_buy, _select_sell, _select_money 将会直接调用子类方法
        :param type: B(buy), S(sell), M(money) 分别对应，买入，卖出，资金界面
        :return:
        """

        def _select():
            window_attr = "%s_window" % w_type.value
            if not hasattr(self, window_attr):
                setattr(self, window_attr, self._get_trade_active_window())
                log.debug("%s界面句柄：%x", w_type, getattr(self, window_attr).handle)

        if w_type == WindowType.W_BUY:
            if hasattr(self, "_select_buy") and callable(self._select_buy):
                self._select_buy()
            else:
                self._main_window.type_keys("{F1}")  # 跳转到买入页面
            _select()
        elif w_type == WindowType.W_SELL:
            if hasattr(self, "_select_sell") and callable(self._select_sell):
                self._select_sell()
            else:
                self._main_window.type_keys("{F2}")  # 跳转到卖出页面
            _select()
        elif w_type == WindowType.W_MONEY:
            if hasattr(self, "_select_money") and callable(self._select_money):
                self._select_money()
            else:
                self._main_window.type_keys("{F4}")  # 跳转到资金页面
            _select()

    @fn_timer
    def _get_position_data(self, position_type):
        """
        获取持仓数据
        :param position_type: 仓位类型
        :return:
        """
        if hasattr(self, "_buy_window"):
            # 如果是委托需要设置为只显示可撤销的委托
            if position_type == PositionType.ENTRUST:
                ke_ce = self._buy_window.child_window(control_id=0x96A)
                if ke_ce.exists() and ke_ce.is_visible():
                    ke_ce.select("可撤")
                ke_ce = self._buy_window.child_window(control_id=0xDDF)
                if ke_ce.exists() and ke_ce.is_visible():
                    ke_ce.check_by_click()

            # 多次尝试从剪切板中获取数据，失败会重试
            for i in range(3):
                try:
                    clipboard.EmptyClipboard()
                    time.sleep(0.1)
                    self._buy_window.CVirtualGridCtrl.type_keys("^c")
                    self._close_copy_code()
                    data = pd.read_clipboard(sep="\t")
                    log.info("账户：%s,获取%s信息：\n%s", self.account, position_type.name, data)
                    break
                except EmptyDataError as e:
                    log.warning("没有从剪切板中获取到任何数据，将重试：%d/%d", i + 1, 3)
            else:
                data = pd.DataFrame()
            return BaseStock.read(data, get_brokers_conf(self.account.broker, position_type))
        else:
            raise AttributeError("%s 没有属性：%s", self.__class__.__name__, "_buy_window")

    @fn_timer
    def _save_as_data(self, save_as_func,
                      position_type: PositionType,
                      pd_kvargs=None,
                      before_read=None,
                      read_func=None,
                      after_read=None,
                      sleep_time=0.1,
                      file_postfix='txt'):
        """
        通过另存为保存数据
        :param save_as_func: 触发文件另存为弹框的函数
        :param position_type: 持仓类型
        :param pd_kvargs: dict pd.read_csv 中可以指定的任意常数
        :param read_func: callable, 数据读取方法，传入file_path绝对路径，返回DataFrame对象
        :param before_read: callable, 数据pandas读取之前预处理，参数，file_path绝对路径
        :param after_read: callable, 数据读取之后的预处理, 该方法接受 data:DataFrame 参数，并返回 data 参数
        :return:
        """
        for i in range(3):
            try:
                self._close_save_as()
                save_as_func()
                time.sleep(sleep_time)
                file_name = "%s_%s_%s.%s" % (position_type.name, self.account.username, conf.now, file_postfix)
                file_path = os.path.join(conf.root_path, "data", "position", file_name)
                self._save_file(file_path)
                time.sleep(sleep_time)

                # 读取之前文件预处理
                if callable(before_read):
                    before_read(file_path)  # 数据预处理

                # 自定义数据读取方法
                if callable(read_func):
                    data = read_func(file_path, position_type, **pd_kvargs)
                else:
                    # 从文件中读取数据
                    default_kvargs = {"sep": "\t", "encoding": "GBK", "error_bad_lines": False}
                    if pd_kvargs:
                        default_kvargs.update(**pd_kvargs)
                    data = pd.read_csv(file_path, **default_kvargs)

                # 读取之后数据处理
                if callable(after_read):
                    data = after_read(data)

                if position_type == PositionType.MONEY:  # 如果是资金则直接返回原始DataFrame
                    return data
                log.info("账户：%s,获取%s信息：\n%s", self.account, position_type.name, data)
                return BaseStock.read(data, get_brokers_conf(self.account.broker, position_type))
            except ElementAmbiguousError as e:
                log.warn("多个另存为窗口被打开！账号：%s, %s", self.account, str(e))
                self._close_save_as()
            except SaveFileSuccess as e:  # 抛出该异常则不再执行文件保存，认为文件操作成功
                log.warning("确认文件是否保存成功！%s", str(e))
                break
            except Exception as e:
                log.exception(e)
            log.info("账号：%s，保存文件失败,仓位类型：%s，重试:%d/%d", self.account, position_type.name, i + 1, 3)
        return {}

    @fn_timer
    def _save_file(self, file_path):
        """
        另存为 弹框，将数据另存为文件。 这个方法需要另行捕获异常信息
        :param file_path: 文件路径
        :return:
        """
        # 如果文件存在
        if os.path.exists(file_path):
            os.remove(file_path)
            log.debug("保存文件----删除文件路径：%s", os.path.basename(file_path))

        file_dialog = self._app.window(title="另存为", top_level_only=True, visible_only=True)
        if not file_dialog.exists():
            raise WindowNotFoundError("账户：%s，【另存为】弹框不存在！" % self.account)
        file_dialog.Edit1.set_text(file_path)
        file_dialog.type_keys("%s")  # 保存
        time.sleep(0.1)
        confirm_dialog = self._app.window(title="确认另存为", top_level_only=True, visible_only=True)
        if confirm_dialog.exists():
            confirm_dialog.type_keys("%y")  # 确认覆盖

    @fn_timer
    def _close_save_as(self):
        # 关闭另存为窗口
        try:
            file_dialogs = self._app.windows(title="另存为", top_level_only=True)
            for fd in file_dialogs:
                fd.close()
        except:
            pass

    def _get_popup_title(self, popup_window):
        # 获取弹框的标题
        try:
            return popup_window.child_window(control_id=0x555).window_text()
        except Exception as e:
            log.exception(e)
            return super()._get_popup_title(popup_window)
    
    def _close_copy_code(self, retry=0):
        # 同花顺复制数据需要输入验证码，这里关闭验证码弹框
        if retry > 0:
            log.info("同花顺---数据复制验证码重试：%s", retry)
        if retry >= 10:
            log.info("同花顺---数据复制验证码以达到最大重试次数：%s", retry)
            return
        code_dialogs = self._app.window(
            class_name="#32770", visible_only=True, top_level_only=True)
        try:
            code_dialogs.wait("visible", timeout=0.5)
            if code_dialogs and code_dialogs.visible:
                code_dialogs['Edit'].type_keys("{BACKSPACE}"*8)
                code_img = code_dialogs.child_window(control_id=0x965)
                code_img.click()
                code = code_to_str(code_img.rectangle(), img_type=ImgType.ths)
                log.info("同花顺---自动识别复制验证码:%s", code)
                code_dialogs['Edit'].type_keys(code+"{ENTER}")
                time.sleep(0.1)
                self._close_copy_code(retry=retry + 1)
        except pw.timings.TimeoutError as e:
            log.info("同花顺---无数据复制验证码弹框")
