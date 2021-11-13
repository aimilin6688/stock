import re
import logging
import enum
import copy
import json
from pandas import DataFrame
from collections import OrderedDict
from src.stock.client.exceptions import AccountInitError

log = logging.getLogger("stock_client")


def remove_code_prefix(code) -> str:
    """
    股票移除前缀，并保证股票代码为6位
    :param code: 股票代码
    :return:
    """
    code = str(code)
    if len(code) == 8:
        return code[2:]
    if len(code) < 6:
        return "{:0>6}".format(code)
    return code[-6:]


def add_code_prefix(code) -> str:
    """
    股票代码添加前缀，并保证股票代码为8位
    :param code:股票代码
    :return:
    """
    prefix_map = {"600": "sh", "601": "sh", "603": "sh", "000": "sz", "001": "sz", "002": "sz", "300": "sz", "399": "sz", "159": "sz"}
    code = str(code)
    if len(code) == 8:
        return code
    if len(code) < 6:
        code = "{:0>6}".format(code)
    if len(code) == 6:
        if code[0:3] in prefix_map:
            return prefix_map[code[0:3]] + code
        else:
            return code
    return code[0:8]


def operation_type(operation) -> int:
    """
    根据操作描述设置操作类型
    :param operation: 操作类型字符串
    :return: 1：buy， 0：sell
    """
    from src.stock.client.exceptions import UnknownOperationType
    if str(operation).find("买") != -1:
        return StockInfo.TYPE_BUY
    if str(operation).find("卖") != -1:
        return StockInfo.TYPE_SELL
    raise UnknownOperationType(operation)


def _repr(obj) -> str:
    """
    打印对象详细信息
    :param obj:
    :return:
    """
    return "%s{%s}" % (obj.__class__.__name__, ', '.join(['%s:%s' % item for item in obj.__dict__.items()]))


# 资金
class Money(object):
    """
    账户资金信息
    """

    def __init__(self, total=.0, available=.0, balance=.0, market=.0, withdraw=.0, profitLoss=.0, **kwargs):
        """
        资产信息
        :param total: 账户总资产
        :param available:  账户可以金额
        :param balance: 资金余额
        :param market: 股票市值
        :param withdraw: 可取资金
        :param profitLoss: 盈亏
        :param kwargs: 其他参数，可自行传递
        """
        self.total = float(total)
        self.available = float(available)
        self.balance = float(balance)
        self.market = float(market)
        self.withdraw = float(withdraw)
        self.profitLoss = float(profitLoss)
        self.kwargs = kwargs

    def __repr__(self) -> str:
        return _repr(self)


# 持仓类型
class PositionType(enum.Enum):
    POSITION = (0, "持仓")  # 持仓
    DEAL = (1, "成交")  # 成交
    ENTRUST = (2, "委托")  # 委托
    MONEY = (3, "资金")  # 资金

    def __init__(self, code, msg):
        self._value_ = code
        self.msg = msg


# 基础类
class BaseStock:
    """
    股票信息基类
    """

    def __init__(self, stockCode=None, stockName=None):
        self.stockCode = stockCode
        self.stockName = stockName

    @staticmethod
    def add_code_prefix(obj):
        if isinstance(obj, list):
            for o in obj:
                BaseStock.add_code_prefix(o)
        if obj and isinstance(obj, BaseStock):
            obj.stockCode = add_code_prefix(obj.stockCode)
        return obj

    @staticmethod
    def remove_code_prefix(obj):
        if isinstance(obj, list):
            for o in obj:
                BaseStock.remove_code_prefix(o)
        if obj and isinstance(obj, BaseStock):
            obj.stockCode = remove_code_prefix(obj.stockCode)
        return obj

    @staticmethod
    def read(df: DataFrame, conf) -> []:
        # 获取属性对应的字段名称
        def get_attr_columns():
            error_columns = set()
            attr_columns = {}
            for k, v in conf['map'].items():
                try:
                    if isinstance(v, list):
                        v = list(set(v) & set(columns))[0]
                    attr_columns[k] = v
                except IndexError as e:
                    error_columns.add("%s - %s" % (conf['type'].__name__, k))
                    continue
            # 打印设置失败的属性
            for index, item in enumerate(error_columns):
                log.warning("设置：%s 失败，请注意查看配置是否正常！", item)
                if index == len(error_columns) - 1:
                    log.warning("列详细：\n%s", columns)
            return attr_columns

        result = list()
        columns = df.columns.to_list()
        attr_columns = get_attr_columns()
        for index, row in df.iterrows():
            obj = conf['type']()
            obj.__setattr__("index", index)  # 为对象设置索引号，方便取出去定位
            for k, v in attr_columns.items():
                if k == "stockCode":
                    obj.__setattr__(k, remove_code_prefix(row[v]))
                else:
                    obj.__setattr__(k, row[v])
            result.append(obj)
        return result

    def __repr__(self) -> str:
        return _repr(self)

    @staticmethod
    def is_position_type(result: dict, position_type: PositionType):
        """
        判断数据是否是指定类型
        @param result: 数据结果， Stock.read 方法返回值, {'sh600365':[xxx,xxx]}
        @param position_type:  仓位类型，持仓：cost_price， 成交：deal_time， 委托：entrust_time
        @return: True 数据符合类型，False 不符合
        """
        if result is None or len(result) == 0:
            return True

        obj = list(result.values())[0]
        obj = obj[0] if isinstance(obj, list) else obj

        if position_type == PositionType.CHI_CHANG:
            if hasattr(obj, 'cost_price') and obj.cost_price:
                return True
        if position_type == PositionType.CHENG_JIAO:
            if hasattr(obj, 'deal_time') and obj.deal_time:
                return True
        if position_type == PositionType.WEI_TUO:
            if hasattr(obj, 'entrust_time') and obj.entrust_time:
                return True
        return False


# 持仓
class StockPosition(BaseStock):
    """
    股票持仓信息
    """

    def __init__(self,
                 stockCode=None,
                 stockName=None,
                 totalNum=0,
                 sellNum=0,
                 freezeNum=0,
                 costPrice=.0,
                 currentPrice=.0,
                 marketValue=.0,
                 profitLoss=.0,
                 profitLossRatio=.0,
                 todayProfitLoss=.0,
                 todayProfitLossRatio=.0,
                 stockHolder="",
                 tradingMarket="",
                 **kwargs):
        super().__init__(stockCode=stockCode, stockName=stockName)
        self.totalNum = totalNum  # 总数量
        self.sellNum = sellNum  # 可卖数量
        self.freezeNum = freezeNum  # 冻结数量
        self.costPrice = costPrice  # 成本价
        self.currentPrice = currentPrice  # 市场价、当前价
        self.marketValue = marketValue  # 市值
        self.profitLoss = profitLoss  # 盈亏
        self.profitLossRatio = profitLossRatio  # 盈亏比
        self.todayProfitLoss = todayProfitLoss  # 当日盈亏
        self.todayProfitLossRatio = todayProfitLossRatio  # 当日盈亏比
        self.stockHolder = stockHolder  # 股东代码
        self.tradingMarket = tradingMarket  # 交易市场
        if kwargs:
            for k, v in kwargs.items():
                self.__setattr__(k, v)

    def __repr__(self) -> str:
        return _repr(self)


# 成交
class StockDeal(BaseStock):
    """
    股票成交信息
    """

    def __init__(self,
                 stockCode=None,
                 stockName=None,
                 dealDate=None,
                 dealTime=None,
                 num=0,
                 price=.0,
                 money=.0,
                 type=None,
                 dealNo=.0,
                 entrustNo=0,
                 stockHolder="",
                 tradingMarket="",
                 **kwargs):
        super().__init__(stockCode=stockCode, stockName=stockName)
        self.dealDate = dealDate # 成交日期
        self.dealTime = dealTime  # 成交时间
        self.num = num  # 成交数量
        self.price = price  # 成交价格
        self.money = float(money.strip()) if isinstance(money, str) else money  # 成交金额
        self.type = type  # 买卖标志
        self.dealNo = dealNo  # 成交编号
        self.entrustNo = entrustNo  # 委托编号
        self.stockHolder = stockHolder  # 股东代码
        self.tradingMarket = tradingMarket   # 交易市场
        if kwargs:
            for k, v in kwargs.items():
                self.__setattr__(k, v)

    def __repr__(self) -> str:
        return _repr(self)

    @property
    def operation_type(self):
        return operation_type(self.type)


# 委托
class StockEntrust(BaseStock):
    def __init__(self,
                 stockCode=None,
                 stockName=None,
                 entrustNo=None,
                 entrustDate=None,
                 entrustTime=None,
                 type=None,
                 num=0,
                 price=.0,
                 dealNum=0,
                 dealPrice=.0,
                 stockHolder=None,
                 tradingMarket=None,
                 cancelNum=0,
                 remark=None,
                 **kwargs):
        super().__init__(stockCode=stockCode, stockName=stockName)
        self.entrustNo = entrustNo  # 委托编号
        self.entrustDate = entrustDate  # 委托日期
        self.entrustTime = entrustTime  # 委托时间
        self.type = type  # 委托类型
        self.num = num  # 委托数量
        self.price = price  # 委托价格
        self.dealNum = dealNum  # 成交数量
        self.dealPrice = dealPrice  # 成交均价
        self.stockHolder = stockHolder  # 股东代码
        self.tradingMarket = tradingMarket  # 交易市场
        self.cancelNum = cancelNum  # 撤单数量
        self.remark = remark  # 状态说明

        if kwargs:
            for k, v in kwargs.items():
                self.__setattr__(k, v)

    def __repr__(self) -> str:
        return _repr(self)

    @property
    def operation_type(self):
        return operation_type(self.type)


# 股票买入卖出对象
class StockInfo(object):
    """
    操作股票的信息，买入或者卖出的信息
    """

    TYPE_BUY = 1  # 股票类型买入
    TYPE_SELL = 0  # 卖出股票

    def __init__(self, code=None, operation=None, name="", price=None, number=None, check_exception=True, **kwargs):
        """
        初始化股票买入或者卖出信息
        :param code: 股票代码
        :param price: 买入或者卖出价格
        :param operation: 类型， 1 买入，0 卖出
        :param number: 买入或者卖出股数
        :param check_exception: 是否检测异常，不是类的属性
        """
        self.code = code
        self.name = name
        self.price = float(price) if price else None
        self.number = int(number) if number else None
        self.operation = int(operation) if operation is not None else None

        if kwargs:
            for k, v in kwargs.items():
                setattr(self, k, v)

        if self.operation is None or "" == self.operation:
            raise Exception("请指定股票操作类型!code:%s" % code)

        if len(self.code) < 6 and check_exception:
            raise Exception("证券代码：%s 有误!" % code)

        if self.operation == StockInfo.TYPE_BUY and check_exception:
            if self.number is None:
                raise Exception("买入股数必须设置！code:%s" % code)
            if self.price is None:
                raise Exception("买入价格必须设置! code:%s" % code)

        if self.operation == StockInfo.TYPE_SELL:
            if self.price == .0:
                self.price = None

    def __eq__(self, o: object) -> bool:
        if isinstance(o, self.__class__):
            return remove_code_prefix(self.code) == remove_code_prefix(o.code) and self.operation == o.operation
        else:
            return False

    def __hash__(self) -> int:
        return hash("%s_%s" % (remove_code_prefix(self.code), self.operation))

    def __repr__(self) -> str:
        return _repr(self)

    @property
    def operation_str(self):
        return self.operation_name(self.operation)

    @staticmethod
    def operation_name(opt_type):
        # 操作类型的名字
        return "卖" if opt_type == StockInfo.TYPE_SELL else "买"

    @staticmethod
    def operation_value(opt_name):
        # 操作类型的值
        if "卖" in opt_name:
            return StockInfo.TYPE_SELL
        if "买" in opt_name:
            return StockInfo.TYPE_BUY
        log.error("不支持的委托类型：%s", opt_name)
        raise NotImplemented("不支持的委托类型：%s" % opt_name)

    def remove_prefix(self, clone=False):
        """
        移除股票代码前缀，
        :param clone: 是否复制对象，默认为False
        :return: self
        """
        obj = self
        if clone:
            obj = self.clone()
        obj.code = remove_code_prefix(obj.code)
        return obj

    def add_prefix(self, clone=False):
        """
        添加前缀
        :param clone: 是否复制对象，默认为False
        :return:
        """
        obj = self
        if clone:
            obj = self.clone()
        obj.code = add_code_prefix(obj.code)
        return obj

    def clone(self):
        return copy.deepcopy(self)

    @staticmethod
    def parse(json_str):
        if type(json_str) == dict:
            return StockInfo(**json_str)
        return StockInfo(**json.loads(json_str))


# 结果状态类
class StockResult:
    OK = "OK"
    ERROR = "ERROR"

    def __init__(self, state, data, stock_info: StockInfo = None, **kwargs):
        self.state = state
        self.data = data
        self.stock_info = stock_info
        if kwargs:
            for k, v in kwargs.items():
                setattr(self, k, v)

    @staticmethod
    def result_ok(data=None, stock_info: StockInfo = None, **kwargs):
        return StockResult(StockResult.OK, data, stock_info=stock_info, **kwargs)

    @staticmethod
    def result_error(data=None, stock_info: StockInfo = None, **kwargs):
        return StockResult(StockResult.ERROR, data, stock_info=stock_info, **kwargs)

    @property
    def is_ok(self):
        return self.state == StockResult.OK

    @property
    def is_error(self):
        return self.state == StockResult.ERROR

    def __repr__(self):
        return "{'state':%s,'data':%s, 'stock_info': %s}" % (self.state, self.data, self.stock_info)


# 账户信息
class Account(object):
    """
    账户信息
    """

    def __init__(self, account_id, username, password, con_password, broker, nickname, exePath, name, **kwargs):
        """
        初始化
        :param account_id: 账户Id
        :param username: 用户名
        :param password: 密码
        :param con_password: 通信密码
        :param broker: 券商名称
        :param nickname: 账户昵称，方便切换账户
        :param kwargs: 其他类型的参数可以自定义传入
        :return:
        """
        self.account_id = account_id
        self.username = username
        self.password = password
        self.con_password = con_password
        self.broker = broker
        self.nickname = nickname
        self.exePath = exePath
        self.name = name
        self.kwargs = kwargs
        if not username or not password or not nickname or not broker:
            raise AccountInitError("账户信息不完整，账户:%s" % username)

        # 设置其他属性
        if kwargs:
            for k, v in kwargs.items():
                setattr(self, k, v)

    def __eq__(self, o: object) -> bool:
        if isinstance(o, self.__class__):
            return self.broker == o.broker and self.username == o.username
        else:
            return False

    def __hash__(self) -> int:
        return hash("%s_%s" % (self.broker, self.username))

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return "%s{%s}" % (self.__class__.__name__, ', '.join(['%s:%s' % item for item in self.__dict__.items() if item[0] != "password"]))

    def to_json(self):
        return {k: v for k, v in self.__dict__.items() if k not in ["password", "kwargs"]}

    @staticmethod
    def parse(obj):
        import json
        """
        将json字符串或者dict 转换成对象
        :param obj:
        :return:
        """
        d = json.loads(obj) if isinstance(obj, str) else obj
        return Account(
            account_id=d["id"],
            username=d['username'],
            password=d['password'],
            con_password=d['comPassword'],
            broker=d['broker']['name'],
            nickname=d['nickname'],
            exePath=d['broker']['exePath'],
            name=d['name']
        )


# 弹框结果
class PopupResult(object):
    # 弹框结果
    def __init__(self, popup_result, regex=None):
        """
        解析弹框内容
        @param popup_result: 弹框结果:{"text":"","title":"","count":}
        @param regex: 合同编码正则匹配规则
        """
        self.popup_result = popup_result
        self.regex = regex
        self.__titles, self.__texts, self.__contracts = self.__parse()

    @property
    def contract(self) -> str:
        return self.__contracts[-1] if self.__contracts else ""

    @property
    def title(self) -> str:
        return self.__titles[-1] if self.__titles else ""

    @property
    def text(self) -> str:
        for i in range(len(self.__texts) - 1, -1, -1):
            text = self.__texts[i]
            if str(text).strip():
                return text
        return ""

    @property
    def texts(self):
        return self.__texts

    @property
    def titles(self):
        return self.__titles

    @property
    def contracts(self):
        return self.__contracts

    def is_success(self, has_contract=True, last_title="提示"):
        """
        判断下单是否成功，两种情况，1. 合同编号获取成功，则直接成功
        2. 没有合同号，根据最后一个弹框类型判断
        @param has_contract:
        @param last_title: 最后一个弹框类型如果为指定内容则认为不成功
        @return:
        """
        # 必须包含合同编号
        if has_contract:
            return self.contract is not None and self.contract != ""

        # 有合同编号直接返回成功
        if self.contract:
            return True
        if last_title == self.title:
            return False
        # 为避免重复下达，其他情况都是成功
        return True

    def __parse(self):
        """
        标题列表，内容列表，合同列表
        @return:
        """
        if not self.popup_result:
            return [], [], []

        if self.regex is None:
            self.regex = ".*合同编号：(\\d+)。.*"

        titles, texts, contracts = [], [], []
        for x, v in self.popup_result.items():
            if "text" in v:
                texts.append(v['text'])
                res = re.match(self.regex, v['text'], re.S)  # 使 . 匹配包括换行在内的所有字符
                if res:
                    contracts.append(res.group(1))
            if "title" in v:
                titles.append(v['title'])
        return titles, texts, contracts
