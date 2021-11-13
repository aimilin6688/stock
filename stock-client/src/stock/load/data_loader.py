import requests
import json
from src.stock.bean.stock_bean import Account, log
from src.utils.config import conf


class DataLoader:
    operation_client = {}

    @staticmethod
    def load_client(account: Account):
        from src.stock.client.client_10jqka import Client10jqka
        from src.stock.client.client_zxjt import ClientZxjt
        from src.stock.client.client_dtzq import ClientDtzq
        from src.stock.client.client_yhzq import ClientYhzq
        from src.stock.client.client_zszq import ClientZszq
        from src.stock.client.client_ghzq import ClientGhzq
        from src.stock.client.client_gfzq import ClientGfzq
        from src.stock.client.client_dfcf import ClientDfcf
        from src.stock.client.client_htzq import ClientHtzq
        from src.stock.client.client_ydzq import ClientYdzq
        from src.stock.client.client_gtja import ClientGtja
        """
        加载股票实际操作客户端
        :param account:
        :return:
        """
        if account.broker in DataLoader.operation_client:
            return DataLoader.operation_client[account.broker]
        else:
            operations = [Client10jqka,  # 同花顺
                          ClientZxjt,  # 中信建投
                          ClientDtzq,  # 大通证券
                          ClientYhzq,  # 银河证券
                          ClientZszq,  # 招商证券
                          ClientGhzq,  # 国海证券
                          ClientGfzq,  # 广发证券
                          ClientDfcf,  # 东方财富
                          ClientHtzq,  # 华泰证券
                          ClientYdzq,  # 英大证券
                          ClientGtja,  # 国泰君安
                          ]
            for operation in operations:
                if operation is None or account.broker not in operation.support_brokers():
                    continue
                obj = operation(account=account)
                for b in operation.support_brokers():
                    DataLoader.operation_client[b] = obj

        return DataLoader.operation_client[account.broker]

    @staticmethod
    def remove_client(account: Account):
        """
        删除加载器
        :param account:
        :return:
        """
        if account.broker in DataLoader.operation_client:
            DataLoader.operation_client.pop(account.broker)

    @staticmethod
    def load_account(id: int = 0):
        result = requests.get("%s/stock/account/detail/%d?clientId=%s&token=%s" % (conf.http_url, id, conf.client_id, conf.client_token))
        obj = json.loads(result.text)
        if obj['code'] == 200:
            return Account.parse(obj['data'])
        else:
            log.error("加载账户：%d,失败，原因：%s", id, obj['msg'])
            return None


if __name__ == '__main__':
    from src.utils.log import init_log

    init_log()
    account = DataLoader.load_account(1)
    print(account)
    print(DataLoader.load_client(account))
