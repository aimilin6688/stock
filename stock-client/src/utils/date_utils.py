import datetime


def now() -> str:
    """
    日期时间格式：'%Y-%m-%d %H:%M:%S'
    :return: '%Y-%m-%d %H:%M:%S'
    """
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def now_date() -> str:
    """
    日期格式：%Y-%m-%d
    :return: %Y-%m-%d
    """
    return datetime.datetime.now().strftime('%Y-%m-%d')


def now_time() -> str:
    """
    时间格式：%H:%M:%S
    :return: %H:%M:%S
    """
    return datetime.datetime.now().strftime('%H:%M:%S')


def add_days(date:str, offset_days=0) -> str:
    """
    日期加减
    @param date:日期, 日期字符串：'%Y-%m-%d' 或者时间对象
    @param offset_days: 加减日期
    @return: %Y-%m-%d
    """
    if isinstance(date, str):
        date = datetime.datetime.strptime(date, '%Y-%m-%d')
    return (date + datetime.timedelta(days=offset_days)).strftime('%Y-%m-%d')


def format_date(date_str, from_format, to_format):
    """
    格式化日期字符串
    :param date_str: 日期字符串
    :param from_format: 日期字符串格式
    :param to_format: 转换到格式
    :return:
    """
    date = datetime.datetime.strptime(date_str, from_format)
    return date.strftime(to_format)


