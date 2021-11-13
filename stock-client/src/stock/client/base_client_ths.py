import time
import pywinauto as pw
from pywinauto import timings
from abc import abstractmethod
from src.utils.config import conf
from src.stock.client.base_client import log, fn_timer, ImgType, LoginException, WindowType
from src.stock.client.client_10jqka import Client10jqka
from src.utils.code_utils import code_to_str
from src.utils.win32_utils import get_handle
from src.stock.bean.stock_bean import PositionType,Account,PopupResult
from collections import OrderedDict


class BaseClientTHS(Client10jqka):
    """
    同花顺--基类
    """
    @fn_timer
    def _after_init(self):
        title = self._get_title()
        self._main_hwnd = get_handle(title, self._get_exe())
        self._app = pw.Application(backend="win32").connect(handle=self._main_hwnd)
        self._main_window = self._app.window(title=title)

    @fn_timer
    def _match_account(self, account: Account, is_selected=False) -> bool:
        if not self._main_window.exists() or not self._main_window.is_visible():
            return False

        self._close_save_as()
        self._max_window()  # 主窗口最大化
        account_combo_box = self._get_account_combobox()
        result_text = None
        for text in account_combo_box.item_texts():
            if self._is_select_account(account, text):
                result_text = text
                if is_selected and account_combo_box.is_visible():
                    account_combo_box.select(text)
                    log.info("切换账号：%s", text)
                else:
                    log.info("账号：%s(%s)已登录无需切换！", account.broker, account.nickname)
                break
        return result_text is not None

    @fn_timer
    def _login_account(self, account: Account, retry=7) -> bool:
        try:
            broker = self.support_brokers()
            log.info("启动%s下单客户端，句柄：%x", self.support_brokers(), self._main_hwnd)
            login_window = self._get_login_window()
            codeEdit = self._get_code_edit(login_window)

            trade_window = self._get_trade_window()
            handle_map = OrderedDict()
            # 自动登录5次
            for i in range(retry):
                if i > 0:
                    self._close_popup_windows(handle_map=handle_map)
                self._set_account(login_window, account)
                if codeEdit and codeEdit.is_visible():
                    self._before_code_refresh(login_window)
                    code = self._get_code_str(login_window)
                    codeEdit.set_text(code)
                    log.info("%s----自动识别验证码:%s", broker, code)

                self._login_click(login_window)
                try:
                    timings.wait_until(8, 0.3, lambda: trade_window.exists() and trade_window.is_visible())
                except timings.TimeoutError as e:
                    log.info("%s----尝试登录第：%d/%d次", broker, i + 1, retry)
                    continue
                else:
                    break
            else:
                log.error("%s----自动登录失败，账号：%s, 结果：%s", broker, account, handle_map)
                raise LoginException("%s" % (PopupResult(handle_map).texts))
            time.sleep(3)
            self._close_popup_windows()
            log.info("%s----账号：%s，登录成功!", broker, account)
            self._max_window()
            # 刷新界面句柄
            self._refresh_hwnd()
        except Exception as e:
            raise e
        return True

    @abstractmethod
    def _get_title(self):
        pass

    def _get_account_combobox(self):
        """
        获取账户选择下拉框
        :return:
        """
        return self._main_window.ToolbarWindow32.child_window(control_id=0x6af, visible_only=False, found_index=0)

    def _is_select_account(self, account: Account, text) -> bool:
        """
        当前账户是否选中
        :param account:
        :param text:
        :return:
        """
        return "%s" % (account.username) == text

    def _get_login_window(self):
        """
        获取登录窗口对象
        :return:
        """
        return self._app.用户登录

    def _set_account(self, login_window, account):
        """
        根据登录窗口设置用户名和密码
        :param login_window: 登录窗口
        :param account: 账号信息
        :return:
        """
        login_window.Edit.set_edit_text(account.username)

        # 清空之前已经输入的密码
        login_window.Edit2.type_keys("{BACKSPACE}" * 8)
        login_window.Edit2.set_edit_text("")  # 清空
        login_window.Edit2.set_edit_text(account.password)

    def _get_code_edit(self, login_window):
        """
        验证码输入框
        :param login_window: 登录窗口
        :return:
        """
        return login_window.Edit3

    def _get_code_img(self, login_window):
        """
        图形验证码对象，主要用户获取屏幕位置
        :param login_window:
        :return:
        """
        return login_window.Static1

    def _get_code_str(self, login_window, length=4):
        return code_to_str(self._get_code_img(login_window).rectangle(), img_type=ImgType.ths, length=length)

    def _login_click(self, login_window):
        """
        登录事件
        :param login_window:
        :return:
        """
        login_window['确定(&Y)'].click()

    def _before_code_refresh(self, login_window):
        """
        验证码刷新之前做的事儿
        :param login_window: 登录窗口
        :return:
        """
        pass

    def _get_trade_window(self):
        """
        交易主窗口
        :return:
        """
        return self._main_window.window(class_name="AfxMDIFrame42s")

    def _get_trade_active_window(self):
        """
        交易当前激活的窗口
        :return:
        """
        return self._app.window(handle=self._trade_window.window(class_name="#32770", visible_only=True, found_index=0).handle)

    def _get_position_key(self):
        """
        仓位快捷键
        :return:
        """
        return {PositionType.POSITION: "W", PositionType.DEAL: "E", PositionType.ENTRUST: "R"}

    def _get_position_data(self, position_type):
        """
        获取仓位数据，采用另存为方式
        :param position_type:
        :return:
        """
        def _save_as_func():
            self._buy_window.CVirtualGridCtrl.send_keystrokes("^s")
            self._close_copy_code()

        if hasattr(self, "_buy_window"):
            return self._save_as_data(save_as_func=_save_as_func, position_type=position_type)
        raise AttributeError("证券：%s, 没有_buy_window属性！" % self.support_brokers())
