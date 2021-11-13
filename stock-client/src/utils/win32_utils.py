import win32api, win32gui, win32con, win32process
import os
import time


class CallBack:
    # 可见控件
    @staticmethod
    def handleVisible(hwnd, hwndList):
        if hwnd and win32gui.IsWindowVisible(hwnd):
            hwndList.append(hwnd)

    # 所有控件
    @staticmethod
    def handleAll(hwnd, hwndList):
        if hwnd:
            hwndList.append(hwnd)


def find_window(hwnd, titles, classes=None, callback=CallBack.handleAll):
    """
    根据名字和类名，匹配子窗口
    :param hwnd: 父窗口句柄
    :param titles: 标题名字
    :param classes: 标题对应的空间类型
    :return: 子窗口句柄
    """
    if hwnd is None:
        return None

    hwndList = []
    try:
        win32gui.EnumChildWindows(hwnd, callback, hwndList)
    except Exception as e:
        return None
    parentHwnd = {}

    def add(c_hwnd):
        p_hwnd = win32gui.GetParent(c_hwnd)
        parentHwnd.setdefault(p_hwnd, 0)
        parentHwnd[p_hwnd] += 1

    for c_hwnd in hwndList:
        winText = win32gui.GetWindowText(c_hwnd)
        # print("父句柄：%x, 子句柄：%x, 标题：%s"%(hwnd, c_hwnd, winText))
        if winText != "" and winText in titles:
            if classes is not None:
                winClass = win32gui.GetClassName(c_hwnd)
                if winClass in classes and winClass == classes.get(titles.index(winText)):
                    add(c_hwnd)
            else:
                add(c_hwnd)

    for k, v in parentHwnd.items():
        if v >= len(titles):
            return k
    return None


def find_window_by_thread(hwnd, titles, classes=None, callback=CallBack.handleVisible):
    """
    获取和当前句柄同线程的顶级窗口并且窗口需要包含指定的标题和类
    :param hwnd: 句柄
    :param titles: 标题
    :param classes: 标题对应的类
    :param callback: 遍历窗口时的回调
    :return: 子窗口句柄
    """
    thread_id, processId = win32process.GetWindowThreadProcessId(hwnd)
    hwndList = []
    win32gui.EnumThreadWindows(thread_id, callback, hwndList)
    for t_hwnd in hwndList:
        w_hwnd = find_window(t_hwnd, titles, classes=classes)
        if w_hwnd:
            return w_hwnd
    return None


def get_hwnd_path(hwnd):
    """
    根据文件句柄获取可执行文件的路径
    :param hwnd:
    :return:
    """
    thread_id, processId = win32process.GetWindowThreadProcessId(hwnd)
    py_proc = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, False, processId)
    return win32process.GetModuleFileNameEx(py_proc, None)


def find_handle(title, exe_path=""):
    """
    根据名称找窗口句柄ID号，如果根据名称没有找到，则返回第一个包含标题的句柄
    :param title: 窗口标题精确匹配或者包含
    :return: 窗口句柄ID
    """
    handle = win32gui.FindWindow(None, title)
    if handle > 0:
        if exe_path == "":
            return handle
        elif exe_path.find(get_hwnd_path(handle)) != -1:
            return handle

    handle = None
    # 遍历已经所有标题
    hWndList = []
    win32gui.EnumWindows(lambda hWnd, param: param.append(hWnd), hWndList)
    for hwnd in hWndList:
        w_title = win32gui.GetWindowText(hwnd)
        if title in w_title:
            if exe_path != "":
                if exe_path.find(get_hwnd_path(hwnd)) != -1:
                    print("找到----------%s, 句柄:%x" % (w_title, hwnd))
                    handle = hwnd
                    break
            else:
                print("找到----------%s, 句柄:%x" % (w_title, hwnd))
                handle = hwnd
                break
    return handle


def get_handle(title, exe_path=""):
    """
    打开软件，并返回软件的句柄，如果不存在则启动
    :param title: 窗口标题
    :param exe_path: 可执行文件路径，找不到窗口时尝试使用该路径打开
    :return: hwnd 窗口句柄
    """
    # 如果软件已经启动
    handle = find_handle(title, exe_path=exe_path)

    # 同花顺没有启动
    if handle is None and exe_path != "":
        os.chdir(os.path.dirname(exe_path))
        os.system("start %s" % exe_path)
        for i in range(30):
            time.sleep(1)  # 暂停1秒
            handle = find_handle(title, exe_path)
            if handle is not None:
                time.sleep(3)
                break
            print("等待软件【%s】启动----------%d" % (os.path.basename(exe_path), i))
    return handle


if __name__ == '__main__':
    d = find_window(0x7106e, ["资金余额"])
    print("%x" % d)
    d = find_window(0x7106e, ["卖出"])
    print("%x" % d)
    # d = find_window_by_thread(0xa0ad2,["交易密码:","验 证 码:","自动登录"] )
    # print("ddddddddddddddddd---%x"%d)
