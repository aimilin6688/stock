# -*- encoding: utf8 -*-
import abc
import logging
import os
import threading
import time
from enum import Enum
from abc import abstractmethod
from collections import OrderedDict

from src.stock.bean.stock_bean import PositionType, StockEntrust, Account, StockInfo
from src.stock.client.client import Client
from src.utils.ding_utls import send_ding_msg
from src.utils.time_utils import fn_timer
from src.stock.client.exceptions import LoginException

log = logging.getLogger("stock_client")
lock = threading.Lock()
try:
    import win32con
    from pywinauto.findwindows import ElementNotFoundError
    from pywinauto.application import WindowSpecification
    from src.img_code.img_predict import ImgType
except Exception as e:
    log.exception(e)


class WindowType(Enum):
    """
    可以打开的窗口类型
    """
    W_BUY = "_buy"
    W_SELL = "_sell"
    W_MONEY = "_money"
    W_CANCEL = "_cancel"
    W_DEAL = "_deal"
    W_ENTRUST = "_entrust"
    W_POSITION = "_position"


class BaseClient(Client, metaclass=abc.ABCMeta):
    handle_count = {}

    def __init__(self, account: Account = None):
        self.account = account
        self._after_init()

    def login_retry(self, account, retry=3, exception_callback=None) -> bool:
        """
        多次尝试自动登录
        :param account: 需要登录的账户
        :param retry: 尝试次数，默认为3吃
        :param exception_callback 发生异常之后回调
        :return:True 登录成功，False 登录失败
        """

        def reset(ex):
            # 登录失败之后重置客户端
            try:
                send_ding_msg("账户：%s，登录失败，尝试：%d/%d, 原因：%s" % (account, i + 1, retry, str(ex)))
                if hasattr(self, "_app"):
                    self._app.kill()
                self._after_init()
            except Exception as e:
                log.exception(e)

        exception_msg = None
        for i in range(retry):
            try:
                is_login = self.login(account)
                if is_login:
                    log.info("账户：%s，登录成功！", account)
                    return True
                else:
                    reset("未知！")
            except Exception as e:
                exception_msg = str(e)
                log.exception(e)
                reset(e)

        if callable(exception_callback) and exception_msg:
            exception_callback(exception_msg)
        return False

    def logout(self, account: Account, **kwargs) -> bool:
        """
        退出登录
        :param account: 需要退出登录的账户
        :return: True 退出登录成功，False 退出登录失败
        """
        if hasattr(self, "_app"):
            from src.stock.load.data_loader import DataLoader
            log.info("账号：%s,退出登录！", account)
            DataLoader.remove_client(account)
            return self._app.kill()
        return False

    def open_window(self, w_type: WindowType):
        """
        使用with 方式打开窗口，窗口只会被打开一次
        :param w_type:
        :return:
        """
        return WithOpenWindow(self, w_type)

    def get_account(self) -> Account:
        """
        获取当前账户信息
        :return: Account 当前客户端显示账户
        """
        return self.account

    @abstractmethod
    def _after_init(self):
        """
        初始化之后的一些重置工作
        :return:
        """
        pass

    def _select_open_window(self, w_type: WindowType, retry=1):
        """
        选择并打开界面
        :param w_type: 界面类型,将类定义类属性 W_xxx
        :param retry: 重试打开次数
        :return:
        """
        self._close_popup_windows()  # 切换窗口关闭弹框
        for i in range(retry):
            if hasattr(self, "w_type") and hasattr(self, "%s_window" % w_type.value):
                if self.w_type == w_type.value:
                    if self._is_window(getattr(self, "%s_window" % w_type.value), w_type):
                        log.debug("已经打开窗口%s，不需要重复打开！", w_type)
                        break
                delattr(self, "w_type")  # 删除打开窗口的属性
            self._select_window(w_type)

    @abstractmethod
    def _select_window(self, w_type: WindowType):
        """
        打开某个具体窗口，需要之类实现，实现类需要设置w_type 和 "%s_window" % w_type.value 属性，表示打开
        :param w_type: 窗口类型
        :return:
        """
        pass

    def _is_window(self, _window, w_type: WindowType) -> bool:
        """
        # 判断窗口类型是否为需要打开的窗口，只关心买入和卖出窗口
        :param _window: 当前窗口
        :param w_type: 窗口类型
        :return:
        """
        if w_type == WindowType.W_BUY:  # 买界面
            return _window.child_window(title_re="^买入价格:?", class_name="Static").exists()
        if w_type == WindowType.W_SELL:  # 卖界面
            return _window.child_window(title_re="^卖出价格:?", class_name="Static").exists()
        return True

    @staticmethod
    def _is_cancel(stock_entrusts: [StockEntrust], stock_codes: [] = None, entrust_nos: [] = None, cancel_type=None) -> [StockEntrust]:
        """
        是否撤销委托
        :param stock_entrust: 全部委托对象
        :param stock_codes: 需要撤销的股票列表，如果为空则撤销全部
        :param entrust_nos: 需要撤销委托单号，为空则撤销全部
        :param cancel_type: 需要撤销的股票类型
        :return: 返回能够撤销列表信息
        """
        cancel_entrusts = list(stock_entrusts)
        if cancel_type is not None:
            cancel_entrusts = [item for item in cancel_entrusts if StockInfo.operation_value(item.type) == cancel_type]

        if stock_codes is not None:
            cancel_entrusts = [item for item in cancel_entrusts if item.stockCode in stock_codes]

        if entrust_nos is not None:
            cancel_entrusts = [item for item in cancel_entrusts if item.entrustNo in entrust_nos]

        return cancel_entrusts

    @fn_timer
    def _max_window(self):
        """
        最大化窗口
        """
        try:
            if hasattr(self, "_main_window"):
                window = self._main_window
                if isinstance(window, WindowSpecification) and window.exists():
                    window = window.wrapper_object()
                if window.get_show_state() != win32con.SW_MAXIMIZE:
                    window.maximize()
                window.set_focus()
        except ElementNotFoundError as e1:
            log.exception(e1)
            self.logout(self.account)
        except Exception as e2:
            log.exception(e2)

    @fn_timer
    def _min_window(self):
        """
        最小化窗体
        """
        if hasattr(self, "_main_window"):
            window = self._main_window
            if isinstance(window, WindowSpecification):
                window = window.wrapper_object()
            if window.get_show_state() != win32con.SW_MINIMIZE:
                window.minimize()

    @fn_timer
    def _set_focus(self):
        """
        设置窗口为焦点窗口
        :return:
        """
        try:
            if hasattr(self, "_main_window"):
                self._main_window.set_focus()
        except Exception as e:
            log.exception(e)

    @fn_timer
    def _read_file(self, file_path, head_line, position_type: PositionType, encoding="GBK", pre_callback=None, **pd_kwargs):
        """
        读取保存出来的txt文件
        @param file_path:
        @param head_line:第几行未标题，索引为0
        @param position_type:
        @param encoding:文件编码
        @param pre_callback: 参数：contents, head_line, position_type，返回True 则直接返回{}，否则继续执行
        @return:df对象
        """
        import pandas as pd
        from io import StringIO
        from src.utils.file_utils import remove_space
        if os.path.exists(file_path):
            # pandas 参数
            pd_args = {"sep": "\s+", "engine": "python"}
            pd_args.update(**pd_kwargs)

            with open(file_path, "r", encoding=encoding) as f:
                contents = f.readlines()
                if callable(pre_callback) and pre_callback(contents, head_line, position_type):
                    return pd.DataFrame()
                try:
                    log.info("获取账户(%s),%s信息：\n%s", self.account, position_type.name, "".join(contents[head_line:]))
                    df = pd.read_csv(StringIO("".join(contents[head_line:])), **pd_args)
                except Exception as e:
                    log.warning("账户：%s，解析%s信息异常！去除中文间空格再次尝试！", self.account, position_type.name)
                    log.exception(e)
                    # 移除中文字符之间的所有空格，不包括标题行
                    result = remove_space(contents[head_line + 1:])
                    result.insert(0, contents[head_line])
                    try:
                        log.info("账户：%s,获取%s信息：\n%s", self.account, position_type.name, "".join(result))
                        df = pd.read_csv(StringIO("".join(result)), **pd_args)
                    except Exception as e2:
                        log.exception(e2)
                        df = pd.read_csv(StringIO("".join(contents[head_line:])), error_bad_lines=False, **pd_args)
                        send_ding_msg("账号:%s, %s信息解析异常，将忽略错误行，请查看详细日志！" % (self.account, position_type.name))
                return df
        else:
            raise FileNotFoundError("文件：%s不存在！", file_path)

    @fn_timer
    def _close_popup_windows(self, timeout: float = 0.6, handle_map=None, close_foreach: bool = True) -> dict:
        """
        关闭多个弹出窗口
        :param timeout, 关闭弹窗之后等待多长时间不弹出就退出， 单位秒
        :return: dict {handle:{count:0, text:''}}, 窗口句柄，关闭次数，窗口内容
        """
        self.__close_team_viewer_dialog()  # 关闭TeamViewer弹出框
        handle_map = OrderedDict() if handle_map is None else handle_map
        try:
            # 关闭循环式弹出窗口，设定主窗口弹框为最后一个，否则会提前结束执行
            while self._close_popup_window(handle_map=handle_map):
                time.sleep(0.15)

            # 关闭目前仍然没有关闭的弹框
            if hasattr(self, "_app") and close_foreach:
                dws = self._app.windows(class_name="#32770", top_level_only=True, visible_only=True)
                for dw in dws:
                    self._close_popup_window(popup_hwnd=dw.handle, handle_map=handle_map)

            # 弹框等待时间
            if timeout > 0:
                start = time.time()
                while (time.time() - start) < timeout:
                    s = self._close_popup_window(handle_map=handle_map)
                    if s == False:
                        time.sleep(0.2)
                    else:
                        break

            if handle_map:
                log.info("弹框结果：%s", handle_map)
        except Exception as e:
            log.exception(e)
        return handle_map

    def _close_popup_window(self, popup_hwnd=None, btn_name=None, handle_map=None, title=None, ignore_count=-1):
        """
        关闭一个弹窗。需要包含：_main_window 和 _app 两个属性
        :param popup_hwnd: 弹出窗口句柄
        :param btn_name: 关闭按钮的名称
        :param handle_map: 主要用来记录弹框关闭的次数，以及关闭弹窗内容
        :param title: 需要关闭的弹框标题
        :param ignore_count: 弹框操作多少次将忽略，默认-1，尝试关闭所有
        :return: 如果有弹出式对话框，返回True，否则返回False
        """
        try:
            if hasattr(self, "_main_window") and hasattr(self, "_app"):
                if popup_hwnd is None:
                    popup_hwnd = self._main_window.popup_window()
                if popup_hwnd:
                    # 如果弹框等于顶层窗口
                    if popup_hwnd in self._exclude_popup_handles():
                        log.debug("顶层窗口，非弹框句柄：%x" % popup_hwnd)
                        return False

                    # 弹框总次数不能超过指定次数
                    handle_count = BaseClient.handle_count
                    if ignore_count > 0 and handle_count.get(popup_hwnd, 0) >= ignore_count:
                        log.debug("多次(%d)未关闭弹框:%x，将直接忽略!", handle_count.get(popup_hwnd, 0), popup_hwnd)
                        return False

                    popup_window = self._app.window(handle=popup_hwnd)
                    # 已经关闭多次则停止关闭
                    if handle_map is not None:
                        handle_map.setdefault(popup_hwnd, {"count": 0})
                        if handle_map[popup_hwnd]['count'] >= 3:
                            handle_count[popup_hwnd] = handle_count.get(popup_hwnd, 0) + 1
                            log.warning("弹框:%x 关闭超过3次，不再关闭！", popup_hwnd)
                            self.__force_close_popup(popup_window, popup_hwnd)
                            return False
                        else:
                            handle_map[popup_hwnd]['count'] += 1

                    if title and popup_window.window_text() != title:
                        log.debug("弹框(%x)标题不匹配：标题：%s，弹框标题：%s", popup_hwnd, title, popup_window.window_text())
                        return True

                    popup_window.set_focus()
                    self.__debug_popup(popup_window, handle_map)  # 打印弹框日志信息

                    if btn_name is not None:
                        btn_names = btn_name if btn_name is list else [btn_name]
                    else:
                        btn_names = ["是", "确定", ""]
                    for btn in btn_names:
                        b = popup_window["%sButton" % btn]
                        if b.exists() and b.is_enabled() and b.is_visible():
                            b.click()
                            break
                    else:
                        self.__force_close_popup(popup_window, popup_hwnd)
                    return True
        except Exception as e:
            log.exception(e)
        return False

    def _get_popup_title(self, popup_window):
        """
        获取弹框标题，有些客户端比较怪异，这里抽出方法单独处理
        :param popup_window:
        :return:
        """
        return popup_window.window_text()

    def _exclude_popup_handles(self):
        """
        需要排除的弹框句柄，如果对象包含：_main_hwnd，_main_dialog_handles属性将会直接添加到忽略列表中
        如果包含：_exclude_handles属性，则直接使用该值
        :return:
        """
        if hasattr(self, "_exclude_handles"):
            return self._exclude_handles
        else:
            exclude_handles = []
            if hasattr(self, "_main_hwnd"):
                exclude_handles.append(self._main_hwnd)
            if hasattr(self, "_main_dialog_handles"):
                exclude_handles.extend(self._main_dialog_handles)
            log.debug("需要忽略的弹框：%s", ["%x" % x for x in exclude_handles])
            self._exclude_handles = exclude_handles
        return self._exclude_handles

    def __debug_popup(self, popup_window, handle_map=None):
        """
        打印弹出框内容信息，截取委托编号等信息
        :param popup_window:
        :param handle_map:
        :return:
        """
        def __get_text(text: str):
            if not isinstance(text, str) or not text:
                return text
            removes = ["现有成交价格预警服务,点击此处前去开通~报告问题", "非交易用户只提供查询功能支持HTML的提示信息"]
            for x in removes:
                text = text.replace(x, "")
            return text

        try:
            handle = popup_window.handle
            if handle_map is None:
                return

            # 初始化
            if handle not in handle_map:
                handle_map.setdefault(handle, {"text": "", "title": ""})
            elif "text" not in handle_map[handle]:
                handle_map[handle]['text'] = ""

            log.debug("账户：%s, 弹框：%x-----------开始", self.account, handle)
            title, text = self._get_popup_info(popup_window)
            if title or text:
                handle_map[handle]['title'] = title
                handle_map[handle]['text'] = __get_text(text)
            log.debug("账户：%s, 弹框：%x-----------结束", self.account, handle)
        except Exception as e:
            log.exception(e)

    def _get_popup_info(self, popup_window):
        """
        获取弹框消息内容
        @param popup_window:
        @return: title, content
        """
        content = ""
        for static in popup_window.iter_children(class_name="Static", visible_only=False):
            text = static.window_text()
            if text:
                content += text
                log.debug(text)
        return self._get_popup_title(popup_window), content

    def __force_close_popup(self, popup_window, popup_hwnd):
        # 强制关闭弹窗
        try:
            if not popup_window.force_close():
                popup_window.close()
                log.debug("弹窗:%x，强制关闭！", popup_hwnd)
        except:
            pass

    def __close_team_viewer_dialog(self):
        # 关闭TeamViewer新特性弹出框
        from pywinauto.findwindows import find_windows
        from pywinauto.controls.hwndwrapper import DialogWrapper
        try:
            ds = find_windows(class_name="#32770", title="TeamViewer", visible_only=True)
            for x in ds:
                DialogWrapper(x).close()
                log.debug("关闭TeamViewer弹出框：%x", x)
        except:
            pass


class WithLogin(object):
    """
    使用with语句登录之后做一些事情
    不要嵌套是使用，会死锁
    """

    def __init__(self, account: Account):
        self.account = account

    def __enter__(self):
        if lock.acquire():
            from src.stock.load.data_loader import DataLoader
            self.operation = DataLoader.load_client(self.account)
            if self.operation.login_retry(self.account):
                return self
            else:
                send_ding_msg("账号:%s，登录失败！" % self.account)
                raise LoginException("账号:%s，登录失败！" % self.account)

    def __exit__(self, exc_type, exc_value, traceback):
        lock.release()
        del self.operation


class WithOpenWindow(object):
    """
    使用with方式打开界面，不需要重复打开一个界面
    """

    def __init__(self, operation, w_type: WindowType):
        self.operation = operation
        self.w_type = w_type

    def __enter__(self):
        self.operation.w_type = self.w_type
        self.operation._select_open_window(self.w_type)
        log.debug("打开窗口：%s", self.operation.w_type)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if hasattr(self.operation, "w_type"):
            log.debug("关闭窗口：%s", self.operation.w_type)
            self.operation.w_type = None
            delattr(self.operation, "w_type")
