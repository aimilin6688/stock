# socket 结果对象
import json

from src.utils.date_utils import now
from src.utils.config import conf
from enum import Enum


class SocketResult(object):
    """
    socket 结果对象
    """

    def __init__(self, code: int = 0, name: str = "", msg: str = "", data: "SocketMessage" = None):
        """
        socket结果对象
        :param code: 状态码
        :param name: code名称
        :param msg: 消息
        :param data: 数据
        """
        self.code = code
        self.name = name
        self.msg = msg
        self.data = data
        self.success = self.code == 1

    @staticmethod
    def send_success(data):
        return SocketResult(1, name="SUCCESS", msg="成功", data=data)

    @staticmethod
    def send_fail(data):
        return SocketResult(0, name="FAIL", msg="失败", data=data)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    @staticmethod
    def parse(msg: str) -> "SocketResult":
        result = SocketResult()
        result.__dict__ = json.loads(msg)
        message = SocketMessage()
        message.__dict__ = result.data
        result.data = message
        return result


class SocketMessage(object):
    """
    具体websocket传递的消息对象
    """
    EXE_ERROR = 0
    EXE_SUCCESS = 1

    def __init__(self, data: object = None, msgId: int = -1, accountId: int = -1, clientId: int = -1, type: int = -1, subject: str = "", weight: int = 0,
                 typeEnum: "SocketMessageType" = None, status: bool = None, **kwargs):
        """
        :param data: 数据
        :param msgId: 消息Id
        :param accountId: 账户Id
        :param clientId: 客户端Id
        :param type: 消息类型
        :param subject: 消息主题
        :param weight: 消息权重
        :param status: 状态 true：成功，false 失败
        :param kwargs: 字典类型的参数，将直接设值
        """
        self.data = data
        self.msgId = msgId
        self.accountId = accountId
        self.clientId = clientId
        self.type = type
        self.subject = subject
        self.weight = weight
        self.status = status
        self.time = now()

        if isinstance(self.type, SocketMessageType):
            self.type = self.type.code

        if typeEnum:
            self.type = typeEnum.code
            self.subject = typeEnum.message

        if kwargs:
            for k, v in kwargs.items():
                self.__setattr__(k, v)

        if self.clientId is None or self.clientId == -1:
            self.clientId = conf.client_id

    def set_data(self, data):
        self.data = data

    @property
    def status_name(self):
        return "成功" if self.status else "失败"

    def __repr__(self) -> str:
        return "{msgId:%s, subject:%s, accountId:%s, clientId:%s, type:%s, weight:%s}" % (
            self.msgId, self.subject, self.accountId, self.clientId, self.type, self.weight if hasattr(self, "weight") else 0
        )


class SocketMessageType(Enum):
    """
    socket传递消息类型
    """
    SIGN = (1, "签收")
    LOGIN = (2, "登录")
    LOGOUT = (3, "退出登录")
    MONEY = (4, "资金查询")
    BUY = (5, "买入")
    SELL = (6, "卖出")
    POSITION = (7, "持仓查询")
    DEAL = (8, "成交查询")
    ENTRUST = (9, "委托查询")
    CANCEL = (10, "撤销委托")
    CLEAR = (11, "清仓")

    # 客户端需要获取账户信息时返回消息类型
    ACCOUNT_INFO = (12, "账户信息")

    # 以下是返回给服务端类型
    R_LOGIN = (102, "登录结果")
    R_LOGOUT = (103, "退出登录结果")
    R_MONEY = (104, "资金查询结果")
    R_BUY = (105, "买入结果")
    R_SELL = (106, "卖出结果")
    R_POSITION = (107, "持仓查询结果")
    R_DEAL = (108, "成交查询结果")
    R_ENTRUST = (109, "委托查询结果")
    R_CANCEL = (110, "撤销委托结果")
    R_CLEAR = (111, "清仓结果")
    R_ACCOUNT_INFO = (112, "账户信息结果")

    H_SUPPORT_BROKER = (200, "支持券商")
    I_ACCOUNT_INFO = (201, "账户信息")

    def __init__(self, code, message):
        self.code = code
        self.message = message
        self._value_ = code

    def to_position_type(self):
        from src.stock.bean.stock_bean import PositionType
        if self.code == self.R_POSITION.code:
            return PositionType.POSITION
        if self.code == self.R_DEAL.code:
            return PositionType.DEAL
        if self.code == self.R_ENTRUST.code:
            return PositionType.ENTRUST
        if self.code == self.R_MONEY.code:
            return PositionType.MONEY
        return None

    @staticmethod
    def parse(code):
        for k, v in SocketMessageType.__members__.items():
            if v.value == code:
                return v
