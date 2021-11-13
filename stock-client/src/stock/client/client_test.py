from src.stock.bean.stock_bean import PositionType, StockInfo, StockResult
from src.stock.client.base_client import WindowType, WithLogin
from src.stock.load.data_loader import DataLoader

# 执行测试
def operation():
    """
    银河证券   孙胜河   97
    @return:
    """
    account = DataLoader.load_account(1)
    with WithLogin(account) as l:
        operation = l.operation

        # 买入测试
        for i in range(1):
            stock_list = [
                StockInfo("000585", 1, price="1.62", number=100),
                StockInfo("601700", 1, price="4.09", number=100),
                StockInfo("600653", 1, price="1.53", number=100)
            ]
            with operation.open_window(WindowType.W_BUY):
                for x in stock_list:
                    print(operation.buy(x))
                operation.cancel(stock_codes=[c.code for c in stock_list[1:2]], cancel_type=StockInfo.TYPE_BUY)
        operation.cancel_buy()

        # 卖出测试
        for i in range(1):
            with operation.open_window(WindowType.W_SELL):
                print(operation.sell(StockInfo("601398", 0, price="3.08", number=101)))
                print(operation.sell(StockInfo("600778", 0, price="5.15", number=102)))
            operation.cancel_sell()
        print(operation.sell(StockInfo("600778", 1, price="5.15", number=103)))
        print(operation.money())
        print(operation.position(PositionType.POSITION))
        print(operation.position(PositionType.DEAL))
        print(operation.position(PositionType.ENTRUST))
        operation.cancel_sell()
        print(operation.__dict__)


if __name__ == '__main__':
    from src.utils.log import init_log
    init_log()
    operation()

