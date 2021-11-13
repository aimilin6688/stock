import json

from src.stock.bean.stock_bean import Account, log, PositionType, StockInfo
from src.stock.client.base_client import BaseClient
from src.stock.load.data_loader import DataLoader
from src.stock.socket.socket_exceptions import NeedAccount
from src.stock.socket.socket_result_bean import SocketMessage, SocketMessageType


class SocketMessageHandler(object):
    # 账户信息缓存对象，类级别
    ACCOUNT_MAP = dict()

    def __init__(self, msg: SocketMessage):
        self.msg = msg
        self.msg_type = SocketMessageType.parse(self.msg.type)
        self.account = self.__load_account(msg.accountId)
        self.client = self.__load_client()

    def login(self) -> SocketMessage:
        msg_result = self.__copy_message()
        msg_result.type = SocketMessageType.R_LOGIN.code
        msg_result.status = self.client.login_retry(self.account, exception_callback=msg_result.set_data)
        msg_result.subject = "%s登录%s%s" % (self.account.name, msg_result.status_name, "" if msg_result.status else "，原因：" + str(msg_result.data))
        return msg_result

    def logout(self):
        msg_result = self.__copy_message()
        msg_result.type = SocketMessageType.R_LOGOUT.code
        msg_result.status = self.client.logout(self.account)
        msg_result.subject = "账户：%s，退出成功！" % self.account.name
        return msg_result

    def deal(self):
        return self.__handle_position(SocketMessageType.R_DEAL)

    def entrust(self):
        return self.__handle_position(SocketMessageType.R_ENTRUST)

    def position(self):
        return self.__handle_position(SocketMessageType.R_POSITION)

    def money(self):
        return self.__handle_position(SocketMessageType.R_MONEY)

    def buy(self):
        msg_result = self.__copy_message()
        msg_result.type = SocketMessageType.R_BUY.code
        msg_result.data = self.client.buy(stock_info=StockInfo.parse(self.msg.data))
        subject = "账户：%s，买入：%s(%s股,%.2f)成功！委托编号：%s" if msg_result.data.is_ok else "账户：%s，买入：%s(%s股,%.2f)失败！原因：%s"
        stock_info = msg_result.data.stock_info
        msg_result.subject = subject % (self.account.name, stock_info.code, stock_info.number, stock_info.price, msg_result.data.data)
        msg_result.status = msg_result.data.is_ok
        return msg_result

    def sell(self):
        msg_result = self.__copy_message()
        msg_result.type = SocketMessageType.R_SELL.code
        msg_result.data = self.client.sell(stock_info=StockInfo.parse(self.msg.data))
        subject = "账户：%s，卖出：%s(%s股,%.2f)成功！委托编号：%s" if msg_result.data.is_ok else "账户：%s，卖出：%s(%s股,%.2f)失败！原因：%s"
        stock_info = msg_result.data.stock_info
        msg_result.subject = subject % (self.account.name, stock_info.code, stock_info.number, stock_info.price, msg_result.data.data)
        msg_result.status = msg_result.data.is_ok
        return msg_result

    def cancel(self):
        def exception_callback(e_str):
            msg_result.status = msg_result.EXE_ERROR
            msg_result.subject = "账户：%s，撤销委托失败，原因：%s" % (self.account.name, e_str)

        msg_result = self.__copy_message()
        msg_result.type = SocketMessageType.R_CANCEL.code
        msg_result.status = msg_result.EXE_SUCCESS
        msg_result.subject = "账户:%s,撤销%s!" % (self.account.name, msg_result.status_name)
        cancel_obj = self.__get_cancel_obj(self.msg.data)
        self.client.cancel(stock_codes=cancel_obj.get("stockCodes", None),
                           entrust_nos=cancel_obj.get("entrustNos", None),
                           cancel_type=cancel_obj.get("type", None),
                           exception_callback=exception_callback)

        return msg_result

    def clear(self):
        pass

    # 处理持仓，委托，成交，资金查询
    def __handle_position(self, msg_type: SocketMessageType):
        position_type = msg_type.to_position_type()

        def exception_callback(e_str):
            msg_result.status = msg_result.EXE_ERROR
            msg_result.subject = "账户：%s，获取%s失败，原因：%s" % (self.account.name, position_type.msg, e_str)

        msg_result = self.__copy_message()
        msg_result.type = msg_type.code
        msg_result.status = msg_result.EXE_SUCCESS
        msg_result.subject = "账户：%s，获取%s成功！" % (self.account.name, position_type.msg)
        if msg_type == SocketMessageType.R_MONEY:
            msg_result.data = self.client.money(exception_callback=exception_callback)
        else:
            msg_result.data = self.client.position(position_type, exception_callback=exception_callback)
        return msg_result

    # 保存账户信息
    def account_info(self):
        account = Account.parse(self.msg.data)
        self.ACCOUNT_MAP[account.account_id] = account
        log.debug("保存账户信息: %s", account)
        msg_result = self.__copy_message()
        msg_result.type = SocketMessageType.R_ACCOUNT_INFO.code
        msg_result.subject = "账户：%s,保存成功！" % account.name
        msg_result.status = msg_result.EXE_SUCCESS
        return msg_result

    # 复制消息对象，主要是设置账户和客户端信息
    def __copy_message(self):
        return SocketMessage(msgId=self.msg.msgId, accountId=self.msg.accountId, clientId=self.msg.clientId)

    # 缓存中加载账户信息
    def __load_account(self, accountId) -> Account:
        # 如果是请求账户信息，则什么都不处理
        if self.msg_type == SocketMessageType.ACCOUNT_INFO:
            return None
        if accountId in self.ACCOUNT_MAP:
            return self.ACCOUNT_MAP.get(accountId)
        raise NeedAccount(accountId, "缺少账户信息!")

    # 加载客户端信息
    def __load_client(self) -> BaseClient:
        if self.msg_type == SocketMessageType.ACCOUNT_INFO:
            return None
        return DataLoader.load_client(self.account)

    # 获取撤销对象
    def __get_cancel_obj(self, data: dict) -> dict:
        # 0:撤指定，1：撤全部，2：撤销买入，3：撤销卖出
        cancel_type = data.get("type", None)
        stock_codes = data.get("stockCodes", None)
        entrust_nos = data.get("entrustNos", None)
        cancel_result = {"stockCodes": stock_codes, "entrustNos": entrust_nos}
        if cancel_type == 0:
            return cancel_result
        if cancel_type == 1:
            return {}
        if cancel_type == 2:
            cancel_result["type"] = StockInfo.TYPE_BUY
            return cancel_result
        if cancel_type == 3:
            cancel_result["type"] = StockInfo.TYPE_SELL
            return cancel_result
        return cancel_result
