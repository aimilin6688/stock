import abc
from abc import abstractmethod
from src.stock.bean.stock_bean import Money, PositionType, Account, StockInfo, StockResult


class Client(object, metaclass=abc.ABCMeta):
    """
    公共客户端抽象方法
    """

    @abstractmethod
    def login(self, account: Account, **kwargs) -> bool:
        """
        登录, 在调用其他方法时也会调用，方法实现需要内部判断账户是否已经登录
        :param account 登录账户信息，由于一个客户端会同时登录多个账号
        :return:True 登录成功，False登录失败
        """
        pass

    @abstractmethod
    def logout(self, account: Account, **kwargs) -> bool:
        """
        退出登录
        :return: True 退出登录成功，False 退出登录失败
        """
        pass

    @abstractmethod
    def buy(self, stock_info: StockInfo, **kwargs) -> StockResult:
        """
        买入单个股票
        :param stock_info:
        :return: 成功：{"state":OK, "data":委托编号}，失败：{"state":ERROR, "data":失败原因}
        """
        pass

    @abstractmethod
    def sell(self, stock_info: StockInfo, **kwargs) -> StockResult:
        """
        卖出单个股票
        :param stock_info:
        :return: 成功：{"state":OK, "data":委托编号}，失败：{"state":ERROR, "data":失败原因}
        """
        pass

    @abstractmethod
    def money(self, exception_callback=None, **kwargs) -> Money:
        """
        统计账户资金信息
        :param exception_callback: 发生异常之后回调该方法
        :return: Money 账户资金信息
        """
        pass

    @abstractmethod
    def position(self, position_type: PositionType, retry=0, exception_callback=None, **kwargs) -> list:
        """
        查询持仓，成交，委托详细情况，注意map {code:Stock子类}
        :param position_type: 需要查询的类型
        :param retry: 查询失败之后默认重新尝试次数, 默认0次
        :param exception_callback: 发生异常之后回调该方法
        :return: map,key-code, value:[] 结果列表
        """
        pass

    @abstractmethod
    def cancel_buy(self, **kwargs) -> bool:
        """
        撤买所有
        :return: True 撤销成功，False 撤销失败
        """
        pass

    @abstractmethod
    def cancel_sell(self, **kwargs) -> bool:
        """
        撤卖所有
        :return: True 撤销成功，False 撤销失败
        """
        pass

    @abstractmethod
    def cancel_all(self, **kwargs) -> bool:
        """
        撤掉所有买入和卖出
        :return:True 撤销成功，False撤销失败
        """
        pass

    @abstractmethod
    def cancel(self, stock_codes: [] = None, entrust_nos: [] = None, cancel_type=None, exception_callback=None, **kwargs) -> bool:
        """
        根据股票列表撤销委托:
        注意：
            stock_codes 与 entrust_nos 不设置值将会撤销所有委托
        :param stock_codes: 需要撤销的股票代码
        :param entrust_nos: 需要撤销的委托代码
        :param cancel_type: 撤销类型，如果指定则按照类型撤销，否则撤销列表中的所有匹配，
        可取值；[StockInfo.TYPE_BUY, StockInfo.TYPE_SELL]
        :param exception_callback: 异常信息设置值
        :return: True 撤销成功， False 撤销失败
        """
        pass

    @staticmethod
    def support_brokers(**kwargs) -> []:
        """
        客户端支持的券商
        :param kwargs: 任意参数
        :return: [] 支持券商名称列表
        """
        pass
