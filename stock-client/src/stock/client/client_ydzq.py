
from src.stock.client.base_client_tdx import BaseClientTDX, conf, log, WindowType


# 英大证券
class ClientYdzq(BaseClientTDX):
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
        self._reset("英大证券网上交易V", conf.exe_ydzq)

    @staticmethod
    def support_brokers() -> list:
        return ["英大证券"]

    def _get_window_conf(self):
        return { WindowType.W_BUY: {"item": [1]},
                 WindowType.W_SELL: {"item": [2]},
                 WindowType.W_CANCEL: {"item": [6]},
                 WindowType.W_POSITION: {"item": [10, 0]},
                 WindowType.W_DEAL: {"item": [10, 2]},
                 WindowType.W_ENTRUST: {"item": [10, 1]},
                 }

    def _code_edit(self):
        """
        验证码输入框位置
        """
        return self._main_window.Edit4

    def _closePopupWindow(self, popup_hwnd=None, btn_name=None, handle_map=None, title=None, ignore_count=3):
        return super()._close_popup_window(popup_hwnd=popup_hwnd,
                                           btn_name=btn_name,
                                           handle_map=handle_map,
                                           title=title,
                                           ignore_count=ignore_count)

