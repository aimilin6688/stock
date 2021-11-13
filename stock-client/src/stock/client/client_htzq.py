import time

from src.stock.client.base_client_ths import BaseClientTHS


# 华泰证券
class ClientHtzq(BaseClientTHS):
    """
    1. 买入卖出价、数量设置为空
    2. 持仓列表，
        a. 将“咨询"、”股票类别“ 隐藏
        b. 中文列不要放一起
    3. 快速交易：
        委托成功后是否弹出提示框：是，
        切换页面清空代码：是，
        撤单前是否需要确认：否，
        自动弹出窗口停留时间：1,

    4. 界面设置：界面不操作超时分：9999， 解锁密码连续几次错误程序退出:100
    """
    def _get_title(self):
        return "网上股票交易系统5.0"

    def _set_account(self, login_window, account):
        """
        根据登录窗口设置用户名和密码
        :param login_window: 登录窗口
        :param account: 账号信息
        :return:
        """
        super(ClientHtzq, self)._set_account(login_window, account)
        # 通讯密码
        login_window.Edit3.type_keys("{BACKSPACE}" * 8)
        login_window.Edit3.set_edit_text("")  # 清空
        login_window.Edit3.set_edit_text(account.com_password)

    def _get_code_edit(self, login_window):
        return None

    @staticmethod
    def support_brokers():
        return ["华泰证券"]

