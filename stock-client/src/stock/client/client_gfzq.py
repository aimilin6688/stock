from src.stock.client.base_client_ths import BaseClientTHS, conf, Account


# 广发证券
class ClientGfzq(BaseClientTHS):
    """
    1. 交易设置：
        买入，卖出价格设置为空
    2. 快速交易：
        是否弹出成交回报提示窗口：否，
        切换页面清空代码：是，
        撤单前是否需要确认：否，
        自动弹出窗口停留时间：1,
        委托成功后是否弹出提示框: 是，
    3. 界面设置：
        界面不操作超时时间（分）：999999
    4. 持仓，成交，委托，两个中文列不能放到一起
    """

    def _get_title(self):
        return "核新网上交易系统7.71"

    def _get_code_img(self, login_window):
        return login_window.Static2

    def _get_code_str(self, login_window, length=5):
        return super()._get_code_str(login_window, length=length)

    def _is_select_account(self, account: Account, text) -> bool:
        acc_map = {"012399977759": "6514854"}
        return "%s" % (acc_map[account.username]) == text

    # 刷新使用多次重复刷新，防止1次没有刷新出来
    def _refresh_position(self, count=6, sleep=0.3):
        super(ClientGfzq, self)._refresh_position(count, sleep)

    @staticmethod
    def support_brokers():
        return ["广发证券"]
