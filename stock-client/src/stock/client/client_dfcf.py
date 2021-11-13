
from pywinauto import timings
from src.stock.client.base_client_tdx import BaseClientTDX, conf, log, WindowType


# 东方财富
class ClientDfcf(BaseClientTDX):
    """
    注意：
        1. 持仓，需要调整列属性，空列排在最后，不能在中间任何位置(两个中文列不能放一起)
        2. 撤单，调整列顺序，证券代码放第一行,空列排在最后(两个中文列不能放一起)
        3. 成交, 调整列顺序，证券代码放第一行,空列排在最后(两个中文列不能放一起)
        4. 闲置时间修改为999
        5. 仓位策略：买入卖出委托数量：自填
        6. 委托,成交：两个中文列不能放在一起
        7. 快速成交：【勾选】委托成功之后保留对话框的弹出
    取消自动升级：
        1. 安装目录中，找到文件 AutoupEx.exe 随便重命名，新建txt文件，并命名为AutoupEx.exe
    """
    def _after_init(self):
        self._reset("东方财富通达信V1", conf.exe_dfcf)

    def _refresh_window(self):
        super()._refresh_window()

        titles = ["自选股迁移"]
        for title in titles:
            msg_dialog = self._app.window(title=title)
            if msg_dialog.exists() and msg_dialog.is_visible():
                msg_dialog.close()
                log.debug("关闭【%s】---弹框！", title)

        # 自身不需要关闭的弹框
        try:
            self._main_dialog_handles = [x.handle for x in self._app.windows(class_name="#32770", visible_only=True, title="")]
        except:
            self._main_dialog_handles = []

    @staticmethod
    def support_brokers() -> list:
        return ["东方财富"]

    def _is_ok_code(self) -> bool:
        try:
            self._main_window.type_keys("{ENTER}")
            timings.wait_until(10, 0.5, lambda: self._trade_window.exists() and self._trade_window.is_visible())
            return True
        except Exception as e:
            log.exception(e)
        return False

    def _code_edit(self):
        return self._main_window.Edit4

    def _get_window_conf(self):
        return { WindowType.W_BUY: {"item": [0]},
                 WindowType.W_SELL: {"item": [1]},
                 WindowType.W_CANCEL: {"item": [8]},
                 WindowType.W_POSITION: {"item": [9, 0]},
                 WindowType.W_DEAL: {"item": [9, 2]},
                 WindowType.W_ENTRUST: {"item": [8]},
                 }

    def _close_popup_window(self, popup_hwnd=None, btn_name=None, handle_map=None, title=None, ignore_count=3):
        return super()._close_popup_window(popup_hwnd=popup_hwnd,
                                           btn_name=btn_name,
                                           handle_map=handle_map,
                                           title=title,
                                           ignore_count=ignore_count)

    def _get_contract_regex(self):
        return "委托已(成功提交)!"

