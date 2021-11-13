import win32api, win32gui, win32con, win32clipboard
import time
from enum import Enum

VK_CODE = {'backspace': 0x08,
           'tab': 0x09,
           'clear': 0x0C,
           'enter': 0x0D,
           'shift': 0x10,
           'ctrl': 0x11,
           'alt': 0x12,
           'pause': 0x13,
           'caps_lock': 0x14,
           'esc': 0x1B,
           'spacebar': 0x20,
           'page_up': 0x21,
           'page_down': 0x22,
           'end': 0x23,
           'home': 0x24,
           'left_arrow': 0x25,
           'up_arrow': 0x26,
           'right_arrow': 0x27,
           'down_arrow': 0x28,
           'select': 0x29,
           'print': 0x2A,
           'execute': 0x2B,
           'print_screen': 0x2C,
           'ins': 0x2D,
           'del': 0x2E,
           'help': 0x2F,
           '0': 0x30,
           '1': 0x31,
           '2': 0x32,
           '3': 0x33,
           '4': 0x34,
           '5': 0x35,
           '6': 0x36,
           '7': 0x37,
           '8': 0x38,
           '9': 0x39,
           'a': 0x41,
           'b': 0x42,
           'c': 0x43,
           'd': 0x44,
           'e': 0x45,
           'f': 0x46,
           'g': 0x47,
           'h': 0x48,
           'i': 0x49,
           'j': 0x4A,
           'k': 0x4B,
           'l': 0x4C,
           'm': 0x4D,
           'n': 0x4E,
           'o': 0x4F,
           'p': 0x50,
           'q': 0x51,
           'r': 0x52,
           's': 0x53,
           't': 0x54,
           'u': 0x55,
           'v': 0x56,
           'w': 0x57,
           'x': 0x58,
           'y': 0x59,
           'z': 0x5A,
           'numpad_0': 0x60,
           'numpad_1': 0x61,
           'numpad_2': 0x62,
           'numpad_3': 0x63,
           'numpad_4': 0x64,
           'numpad_5': 0x65,
           'numpad_6': 0x66,
           'numpad_7': 0x67,
           'numpad_8': 0x68,
           'numpad_9': 0x69,
           'multiply_key': 0x6A,
           'add_key': 0x6B,
           'separator_key': 0x6C,
           'subtract_key': 0x6D,
           'decimal_key': 0x6E,
           'divide_key': 0x6F,
           'F1': 0x70,
           'F2': 0x71,
           'F3': 0x72,
           'F4': 0x73,
           'F5': 0x74,
           'F6': 0x75,
           'F7': 0x76,
           'F8': 0x77,
           'F9': 0x78,
           'F10': 0x79,
           'F11': 0x7A,
           'F12': 0x7B,
           'F13': 0x7C,
           'F14': 0x7D,
           'F15': 0x7E,
           'F16': 0x7F,
           'F17': 0x80,
           'F18': 0x81,
           'F19': 0x82,
           'F20': 0x83,
           'F21': 0x84,
           'F22': 0x85,
           'F23': 0x86,
           'F24': 0x87,
           'num_lock': 0x90,
           'scroll_lock': 0x91,
           'left_shift': 0xA0,
           'right_shift ': 0xA1,
           'left_control': 0xA2,
           'right_control': 0xA3,
           'left_menu': 0xA4,
           'right_menu': 0xA5,
           'browser_back': 0xA6,
           'browser_forward': 0xA7,
           'browser_refresh': 0xA8,
           'browser_stop': 0xA9,
           'browser_search': 0xAA,
           'browser_favorites': 0xAB,
           'browser_start_and_home': 0xAC,
           'volume_mute': 0xAD,
           'volume_Down': 0xAE,
           'volume_up': 0xAF,
           'next_track': 0xB0,
           'previous_track': 0xB1,
           'stop_media': 0xB2,
           'play/pause_media': 0xB3,
           'start_mail': 0xB4,
           'select_media': 0xB5,
           'start_application_1': 0xB6,
           'start_application_2': 0xB7,
           'attn_key': 0xF6,
           'crsel_key': 0xF7,
           'exsel_key': 0xF8,
           'play_key': 0xFA,
           'zoom_key': 0xFB,
           'clear_key': 0xFE,
           '+': 0xBB,
           ',': 0xBC,
           '-': 0xBD,
           '.': 0xBE,
           '/': 0xBF,
           '`': 0xC0,
           ';': 0xBA,
           '[': 0xDB,
           '\\': 0xDC,
           ']': 0xDD,
           "'": 0xDE,
           '`': 0xC0}
VK_SHIFT_CODE = {
    "~": "`",
    "!": "1",
    "@": "2",
    "#": "3",
    "$": "4",
    "%": "5",
    "^": "6",
    "&": "7",
    "*": "8",
    "(": "9",
    ")": "0",
    "_": "-",
    "+": "=",
    "Q": "q",
    "W": "w",
    "E": "e",
    "R": "r",
    "T": "t",
    "Y": "y",
    "U": "u",
    "I": "i",
    "O": "o",
    "P": "p",
    "A": "a",
    "S": "s",
    "D": "d",
    "F": "f",
    "G": "g",
    "H": "h",
    "J": "j",
    "K": "k",
    "L": "l",
    ":": ";",
    "\"": "'",
    "Z": "z",
    "X": "x",
    "C": "c",
    "V": "v",
    "B": "b",
    "N": "n",
    "M": "m",
    "<": ",",
    ">": ".",
    "?": "/",
    "{": "[",
    "}": "]",
    "|": "\\",
}


class Lan(Enum):
    """
    语言代码值参考：https://msdn.microsoft.com/en-us/library/cc233982.aspx
    """
    EN = 0x4090409
    ZH = 0x8040804


def change_lan(lan: Lan):
    """
    修改当前激活窗口输入法
    :param lan: 语言类型
    :return: True 修改成功，False 修改失败
    """
    # 获取系统输入法列表
    hwnd = win32gui.GetForegroundWindow()
    im_list = win32api.GetKeyboardLayoutList()
    im_list = list(map(hex, im_list))

    # 加载输入法
    if hex(lan.value) not in im_list:
        win32api.LoadKeyboardLayout('0000' + hex(lan.value)[-4:], 1)

    result = win32api.SendMessage(
        hwnd,
        win32con.WM_INPUTLANGCHANGEREQUEST,
        0,
        lan.value)
    if result == 0:
        print('设置%s键盘成功！' % lan.name)
    return result == 0


def click(click_type, x_position=None, y_position=None, double_click=False, sleep=0.):
    """
    鼠标点击事件
    :param click_type: 类型，left, right
    :param x_position: 可选
    :param y_position: 可选
    :param double_click: True 双击，False 点击
    :param sleep: 点击之后暂停时间
    :return:
    """
    if click_type not in ["left", "right"]:
        click_type = "left"

    if click_type == "left":
        down, up = win32con.MOUSEEVENTF_LEFTDOWN, win32con.MOUSEEVENTF_LEFTUP
    else:
        down, up = win32con.MOUSEEVENTF_RIGHTDOWN, win32con.MOUSEEVENTF_RIGHTUP

    if x_position is not None and y_position is not None:
        move(x_position, y_position, sleep=sleep)

    win32api.mouse_event(down, 0, 0, 0, 0)
    win32api.mouse_event(up, 0, 0, 0, 0)
    if double_click:
        win32api.mouse_event(down, 0, 0, 0, 0)
        win32api.mouse_event(up, 0, 0, 0, 0)

    if sleep > 0:
        time.sleep(sleep)


def move(x_position, y_position, sleep=0.):
    """
    鼠标移动到指定位置
    :param x_position:
    :param y_position:
    :param sleep:
    :return:
    """
    win32api.SetCursorPos((x_position, y_position))
    if sleep > 0:
        time.sleep(sleep)


def click_left(x_position=None, y_position=None, sleep=0.):
    """
    鼠标左键点击指定坐标
    :param x_position: x 点
    :param y_position: y 点
    :param sleep: 点击之后暂停时间
    :return: None
    """
    click("left", x_position=x_position, y_position=y_position, sleep=sleep)


def dclick_left(x_position=None, y_position=None, sleep=0.):
    """
    鼠标左键双击指定坐标
    :param x_position: x 点
    :param y_position: y 点
    :param sleep: 双击之后暂停时间
    :return: None
    """
    click("left", x_position=x_position, y_position=y_position, double_click=True, sleep=sleep)


def click_right(x_position=None, y_position=None, sleep=0.):
    """
    鼠标右键点击指定坐标
    :param x_position: x 点
    :param y_position: y 点
    :param sleep: 点击之后暂停时间
    :return: None
    """
    click("right", x_position=x_position, y_position=y_position, sleep=sleep)


def dclick_right(x_position=None, y_position=None, sleep=0.):
    """
    鼠标右键点击指定坐标
    :param x_position: x 点
    :param y_position: y 点
    :param sleep: 点击之后暂停时间
    :return: None
    """
    click("right", x_position=x_position, y_position=y_position, double_click=True, sleep=sleep)


def press(*args, sleep=0., pause=0.05):
    """
    顺序按下释放按键
    :param hwd:
    :param args:
    :return:
    """
    for arg in args:
        if arg in VK_SHIFT_CODE:
            press_hold_release("left_shift", VK_SHIFT_CODE[arg])
        else:
            win32api.keybd_event(VK_CODE[arg], 0, 0, 0)
            time.sleep(pause)
            win32api.keybd_event(VK_CODE[arg], 0, win32con.KEYEVENTF_KEYUP, 0)
    if sleep > 0:
        time.sleep(sleep)


def press_hold_release(*args):
    """
    组合建按下与释放
    :param args:
    :return:
    """
    for arg in args:
        win32api.keybd_event(VK_CODE[arg], 0, 0, 0)
        time.sleep(.05)

    for arg in args:
        win32api.keybd_event(VK_CODE[arg], 0, win32con.KEYEVENTF_KEYUP, 0)
        time.sleep(.05)


def set_clipboard(text, sleep=0.):
    """
    为粘贴板设置内容
    :param text:
    :return:
    """
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, text)
    win32clipboard.CloseClipboard()
    if sleep > 0:
        time.sleep(sleep)


def press_ctrl_v():
    """
    发送 ctrl + v 组合建
    :return:
    """
    press_hold_release("ctrl", "v")


def set_foreground_window(hwnd):
    """
    # https://stackoverflow.com/questions/14295337/win32gui-setactivewindow-error-the-specified-procedure-could-not-be-found/15503675#15503675
    有时候设置窗口到最前端会遇到pywintypes.error: (0, 'SetForegroundWindow', 'No error message is available')
    :param hwnd:
    :return:
    """
    # 先将置顶的窗口隐藏，否则不能将窗口放到最前端
    hide_always_on_top_windows(hwnd)
    # 首先显示窗口到桌面
    win32gui.ShowWindow(hwnd, win32con.SW_NORMAL)
    win32gui.SetForegroundWindow(hwnd)


def hide_always_on_top_windows(hwnd):
    """
    关闭置顶的窗口
    :param hwnd: 窗口句柄
    :return:
    """

    def _window_enum_callback_hide(_hwnd, unused):
        if _hwnd != hwnd:  # ignore self
            # Is the window visible and marked as an always-on-top (topmost) window?
            if win32gui.IsWindowVisible(_hwnd) and win32gui.GetWindowLong(_hwnd, win32con.GWL_EXSTYLE) & win32con.WS_EX_TOPMOST:
                # Ignore windows of class 'Button' (the Start button overlay) and
                # 'Shell_TrayWnd' (the Task Bar).
                className = win32gui.GetClassName(_hwnd)
                if className not in ['Button', 'Shell_TrayWnd', 'Shell_SecondaryTrayWnd']:
                    # Force-minimize the window.
                    # Fortunately, this seems to work even with windows that
                    # have no Minimize button.
                    # Note that if we tried to hide the window with SW_HIDE,
                    # it would disappear from the Task Bar as well.
                    win32gui.ShowWindow(_hwnd, win32con.SW_FORCEMINIMIZE)

    win32gui.EnumWindows(_window_enum_callback_hide, None)
