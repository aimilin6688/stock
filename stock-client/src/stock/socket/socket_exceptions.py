

class NeedAccount(Exception):
    """
    需要账户信息
    """
    def __init__(self, accountId, msg, *args, **kwargs):
        self.accountId = accountId
        self.msg = msg

    def __repr__(self):
        return self.msg + ", AccountId: " + self.accountId