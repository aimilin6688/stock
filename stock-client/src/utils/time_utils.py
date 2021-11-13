import time
from src.utils.config import conf


def fn_timer(f):
    # *args：接收多个参数；**kwargs：关键字传参，接收多个参数
    def wrapper(*args, **kwargs):
        if not conf.show_method_exe_time:
            return f(*args, **kwargs)
        else:
            start_time = time.time()  # 函数开始运行时间
            res = f(*args, **kwargs)
            end_time = time.time()  # 函数结束时间
            print("%30s ------- %.8f" % (f.__name__, end_time - start_time))
            return res  # 返回函数运行结果
    return wrapper
