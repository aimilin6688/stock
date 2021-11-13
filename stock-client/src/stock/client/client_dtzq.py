from src.utils.config import conf
from src.stock.client.base_client_tdx import BaseClientTDX, log, ImgType, WindowType
import time
from src.utils.code_utils import code_to_str
from src.utils import windows_utils as wu


# 大通证券
class ClientDtzq(BaseClientTDX):
    """
    1. 系统参数：闲置时间修改为最大，(选中)列表框显示登陆信息
    2. 快捷交易：(选中)普通委托和闪电委托成功后弹出提示框
    3. 仓位策略：买入委托数量：自填，卖出委托数量：自填
    4. 注意：两个中文列不能放在一起
    """
    def _after_init(self):
        self._reset("大通证券金融终端V", conf.exe_dtzq)

    @staticmethod
    def support_brokers() -> list:
        return ["大通证券"]

    def _get_window_conf(self):
        return {WindowType.W_BUY:{"item":[0]},
                WindowType.W_SELL:{"item":[1]},
                WindowType.W_CANCEL:{"item":[5]},
                WindowType.W_POSITION:{"item":[7,1]},
                WindowType.W_DEAL:{"item":[7,3]},
                WindowType.W_ENTRUST:{"item": [5]},
                }

    def _input_code(self):
        # 输入验证码校验输入
        code_dialog = self._app.window(title="请输入验证码", class_name="#32770")
        if not code_dialog.exists():
            return

        codeEdit = code_dialog.AfxWnd42
        for i in range(10):
            try:
                self._close_message_dialog()
                # 防止有多个弹框窗口存在
                if i > 0:
                    for j in range(2):
                        self._close_popup_window(title="提示")
                time.sleep(0.5)
                rect = codeEdit.rectangle()
                code = code_to_str((rect.right + 3, rect.top, rect.right + 60, rect.bottom), img_type=ImgType.tdx)
                codeEdit.set_focus()
                wu.press(*code)
                code_dialog.child_window(title="确定", class_name="Button").click()
                time.sleep(0.5)
                if not code_dialog.exists():
                    return
                log.info("输入验证码------验证码错误，准备重新尝试：%d/%d", i + 1, 10)
            except Exception as e:
                log.warning("大通证券----输入验证码异常：%s", str(e))
                log.exception(e)

    def _close_popup_windows(self, **kwargs) -> dict:
        self._input_code()
        return super()._close_popup_windows()

    def _unlock(self, retry=10):
        self._close_login_popup()
        super()._unlock(retry=retry)

    def _close_login_popup(self):
        """
        关闭账号已登录弹框
        :return:
        """
        try:
            popup = self._app.window(class_name="#32770", title="TQ")
            if not popup.exists():
                return
            popup.close()
        except Exception as e:
            log.warning("大通证券----关闭账户已登录提示失败，%s", str(e))


