import time

from src.utils.config import conf
from src.stock.client.base_client_ths import BaseClientTHS


# 中信建投
class ClientZxjt(BaseClientTHS):
    """
    1. 买入卖出价、数量设置为空
    2. 持仓列表，
        a. 将“当前可拥股数”移到前面，“资讯”移到最后一列
        b. 隐藏“可申赎数量”，“股票余额”，“买入成本价”
        c. 显示“序号”列
    3. 快速交易：
        委托成功后是否弹出提示框：是，
        切换页面清空代码：是，
        撤单前是否需要确认：否，
        自动弹出窗口停留时间：1,

    4. 界面设置：界面不操作超时分：9999， 解锁密码连续几次错误程序退出:100
    """

    def _get_title(self):
        return "网上股票交易系统5.0"

    def _get_code_edit(self, login_window):
        return login_window["验 证 码(&V):Edit1"]

    def _before_code_refresh(self, login_window):
        login_window['刷新'].click()
        time.sleep(0.5)

    def _get_code_img(self, login_window):
        return login_window['验 证 码(&V):Static']

    @staticmethod
    def support_brokers():
        return ["中信建投"]
