from src.stock.bean.stock_bean import PositionType, Money
from src.stock.client.base_client_ths import BaseClientTHS, log, conf, fn_timer, WindowType


# 银河证券
class ClientYhzq(BaseClientTHS):
    """
    1. 系统设置：是否弹出消息推送提示框：否，
    2. 交易设置：买入、卖出价格：空，
    3. 快速交易：委托成功后是否弹出提示框；是， 切换页面清空代码：是，撤单前是否需要确认：否
    4. 界面设置：界面不操作超时时间分：9999
    5. 委托列，增加“撤销数量”
    """

    def _get_title(self):
        return "网上股票交易系统5.0"


    @staticmethod
    def support_brokers():
        return ["银河证券"]

    def _login_click(self, login_window):
        """
        登录事件
        :param login_window:
        :return:
        """
        login_window.Button1.click()

    def _cancel_line_height(self):
        """
        撤销委托行高
        @return:
        """
        return 24

    def _cancel_top_offset(self):
        """
        撤销委托第一行离上方高度
        @return:
        """
        return 24

    @fn_timer
    def money(self) -> Money:
        try:
            self._select_open_window(WindowType.W_MONEY)
            df = self._save_as_data(lambda: self._money_window.HexinScrollWnd22.CVirtualGridCtrl.send_keystrokes("^s"), PositionType.MONEY)
            money = Money(total=df.loc[0, "总资产"], available=df.loc[0, "可用金额"])
            try:
                money.balance = df.loc[0, "资金余额"]
                money.market = df.loc[0, "总市值"]
            except:
                pass
            log.info("账户：%s, 总资金：%.2f, 可用资金: %.2f", self.account.username, money.total, money.available)
            return money
        except Exception as e:
            log.exception(e)
        return Money(.0, .0)
