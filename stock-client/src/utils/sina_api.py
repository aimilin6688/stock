import requests
import logging
import time
from enum import Enum
from decimal import Decimal, ROUND_HALF_UP

log = logging.getLogger("xiadan")


class StockType(Enum):
    TYPE_STOCK = 0  # 股票行情
    TYPE_TAGS = 1  # 债券行情


def query_tags(stock_codes, retry=3):
    """
    查询债券实时价格
    :param stock_codes:
    :param retry:
    :return:
    """
    return __query(StockType.TYPE_TAGS, stock_codes, retry=retry)


def query_stock(stock_codes, retry=3):
    """
    查询股票实时价格
    :param stock_codes:
    :param retry:
    :return:
    """
    return __query(StockType.TYPE_STOCK, stock_codes, retry=retry)


def __query(stock_type: StockType, stock_codes, retry=3):
    """
    股票代码列表，需要指定股票代码前缀
    :param stock_codes:
    :return: [StockDetail]
    """
    if not stock_codes:
        return None
    for i in range(retry):
        for api in [SinaAPI, QQAPI]:
            try:
                result = requests.get(api.get_url(stock_type, stock_codes))
                log.debug("%s实时股票数据：\n%s", api.__name__, result.text[0:100])
                result = api.parse(stock_type, result.text)
                if result:
                    return result
            except Exception as e:
                log.warning("查询%s行情数据异常：%s", api.__name__, str(e))
        log.warning("查询%s行情数据异常,重试:%d/%d", stock_type.name, i + 1, retry)
    return None


# 保留2位小数
def _round_2(price) -> float:
    return Decimal(str(price)).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP).__float__()


def _get_stock_codes(stock_codes):
    """
    移除非法的股票代码
    @param stock_codes:
    @return:
    """
    if stock_codes is None:
        return stock_codes
    stock_codes = [stock_codes] if isinstance(stock_codes, str) else stock_codes
    codes = set()
    for code in stock_codes:
        if len(code) == 8:
            codes.add(code)
    return ",".join(codes)


class QueryStockException(Exception):
    """
    股票信息查询异常
    """
    pass


class SinaAPI:
    STOCK_URL = "https://hq.sinajs.cn/?_=%s&list=%s"
    TAGS_URL = "https://hq.sinajs.cn/etag.php/?_=%s&list=%s"

    @staticmethod
    def parse(stock_type: StockType, sina_str):
        if "hq_str_sys_auth" in sina_str:
            log.debug("查询股票实时信息异常,请检查股票代码！")
            raise QueryStockException(sina_str)
        results = {}
        for line in sina_str.strip().split("\n"):
            if "\"\"" in line:
                results[line[11:19]] = {}
            else:
                infos = line.split(",")
                obj = {
                    "code": infos[0][11:19],
                    "name": infos[0][21:],
                    "open": infos[1],
                    "last_close": infos[2],
                    "price": infos[3],
                    "high": infos[4],
                    "low": infos[5],
                    "volume": infos[8],
                    "money": infos[9],
                    "buy_1": infos[10],
                    "buy_1_price": infos[11],
                    "buy_2": infos[12],
                    "buy_2_price": infos[13],
                    "buy_3": infos[14],
                    "buy_3_price": infos[15],
                    "buy_4": infos[16],
                    "buy_4_price": infos[17],
                    "buy_5": infos[18],
                    "buy_5_price": infos[19],
                    "sell_1": infos[20],
                    "sell_1_price": infos[21],
                    "sell_2": infos[22],
                    "sell_2_price": infos[23],
                    "sell_3": infos[24],
                    "sell_3_price": infos[25],
                    "sell_4": infos[26],
                    "sell_4_price": infos[27],
                    "sell_5": infos[28],
                    "sell_5_price": infos[29],
                    "date": infos[30],
                    "time": infos[31],
                }

                # 设置跌停价
                down = 0.95 if "ST" in obj['name'] else 0.9
                obj['down_price'] = _round_2(Decimal(obj['last_close']) * Decimal(down))

                # 设置涨停价
                up = 1.05 if "ST" in obj['name'] else 1.1
                obj['up_price'] = _round_2(Decimal(obj['last_close']) * Decimal(up))

                results[obj["code"]] = obj
        log.debug("股票实时数据查询结果：长度：%d，股票代码：%s", len(results), results.keys())
        return results

    @staticmethod
    def get_url(stock_type: StockType, stock_codes):
        if stock_type == StockType.TYPE_TAGS:
            url = SinaAPI.TAGS_URL
        else:
            url = SinaAPI.STOCK_URL
        return url % (time.time(), _get_stock_codes(stock_codes))


class QQAPI:
    STOCK_URL = "https://qt.gtimg.cn/?_=%s&q=%s"
    TAGS_URL = "https://qt.gtimg.cn/etag/?_=%s&q=%s"

    @staticmethod
    def parse(stock_type: StockType, text):
        if "v_pv_none_match" in text:
            log.info("股票代码不匹配!")
            return None
        results = {}
        for line in text.strip().split("\n"):
            if "\"\"" in line:
                results[line[2:10]] = {}
            else:
                code = line[2:10]
                infos = line.split("~")
                c_type = infos[61]
                obj = {
                    "code": code,
                    "name": infos[1],
                    "open": infos[5],
                    "last_close": infos[4],
                    "price": infos[3],
                    "high": infos[33],
                    "low": infos[34],
                    "volume": QQAPI.__file_zero(infos[36], c_type, "volume"),  # 非指数加2个0
                    "money": QQAPI.__file_zero(infos[37], c_type, "money"),
                    "buy_1": QQAPI.__file_zero(infos[10], c_type, "buy"),
                    "buy_1_price": infos[9],
                    "buy_2": QQAPI.__file_zero(infos[12], c_type, "buy"),
                    "buy_2_price": infos[11],
                    "buy_3": QQAPI.__file_zero(infos[14], c_type, "buy"),
                    "buy_3_price": infos[13],
                    "buy_4": QQAPI.__file_zero(infos[16], c_type, "buy"),
                    "buy_4_price": infos[15],
                    "buy_5": QQAPI.__file_zero(infos[18], c_type, "buy"),
                    "buy_5_price": infos[17],
                    "sell_1": QQAPI.__file_zero(infos[20], c_type, "buy"),
                    "sell_1_price": infos[19],
                    "sell_2": QQAPI.__file_zero(infos[22], c_type, "buy"),
                    "sell_2_price": infos[21],
                    "sell_3": QQAPI.__file_zero(infos[24], c_type, "buy"),
                    "sell_3_price": infos[23],
                    "sell_4": QQAPI.__file_zero(infos[26], c_type, "buy"),
                    "sell_4_price": infos[25],
                    "sell_5": QQAPI.__file_zero(infos[28], c_type, "buy"),
                    "sell_5_price": infos[27],
                    "date": format(infos[30][0:8], '%Y%m%d', '%Y-%m-%d'),
                    "time": format(infos[30][8:14], '%H%M%S', '%H:%M:%S'),
                    'down_price': float(infos[48]),
                    "up_price": float(infos[47])
                }
                results[obj["code"]] = obj
        log.debug("股票实时数据查询结果：长度：%d，股票代码：%s", len(results), results.keys())
        return results

    @staticmethod
    def __file_zero(value, c_type: str, f_type):
        """
        与新浪接口对应
        @param value: 值
        @param c_type: 数据类型：ZS:指数，GP:股票，ZQ:债券，
        @param f_type: 字段类型
        @return:
        """
        if f_type == "volume":
            if c_type.startswith("GP"):
                return value + "00"
            if c_type.startswith("ZQ"):
                return value + "0"

        if f_type == "money":
            return value + "0000"

        if f_type == "buy":
            if c_type.startswith("ZQ"):
                return value + "0"
            return value + "00"
        return value

    @staticmethod
    def get_url(stock_type: StockType, stock_codes):
        if stock_type == StockType.TYPE_TAGS:
            url = QQAPI.TAGS_URL
        else:
            url = QQAPI.STOCK_URL
        return url % (time.time(), _get_stock_codes(stock_codes))


if __name__ == '__main__':
    print(query_stock(["sh600826", 'sh601006'], retry=1))
    print(query_tags(["sh204001"]))
    print(_round_2(Decimal('5.350') * Decimal('0.9')))
