class LoginException(Exception):
    """
    登录失败异常
    """
    pass


class InputException(Exception):
    """
    输入数据有误！
    """
    pass


class AccountInitError(Exception):
    """
    账户初始化异常
    """
    pass


class AccountMoneyException(Exception):
    """
    获取账户资金异常
    """
    pass


class SaveFileSuccess(Exception):
    """
    文件保存成功
    """
    pass


class OpenWindowException(Exception):
    """
    窗口已经被打开并且没有关闭，不能重复打开另外一个窗口
    """
    pass


class UnknownOperationType(Exception):
    """
    未知操作类型异常
    """

    def __init__(self, operation):
        self.operation = operation

    def __str__(self):
        return "未知的操作类型：%s" % self.operation


class QueryPositionException(Exception):
    """
    查询仓位信息异常
    """

    def __init__(self, position_type, head_line=""):
        self.position_type = position_type
        self.head_line = head_line

    def __str__(self):
        return "查询仓位：%s,异常，首行：%s" % (self.position_type, self.head_line)
