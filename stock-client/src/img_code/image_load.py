import pywinauto as pw
from pywinauto import keyboard
from src.utils.config import conf
from src.utils.win32_utils import get_handle
import win32api, win32gui, win32con, win32process
from src.utils import windows_utils as wu
from PIL import ImageGrab
import time
import os
from PIL import Image
from .img_predict import ths_img_to_str, ghzq_img_to_str


def tdx_code():
    title = "大通证券金融终端"
    main_hwnd = get_handle(title, conf.exe_dtzq)
    thread_id, processId = win32process.GetWindowThreadProcessId(main_hwnd)
    app = pw.Application(backend="win32").connect(process=processId)
    print("启动%s，句柄：%x,进程ID:%x", title, main_hwnd, processId)
    main_window = app.window(title_re="%s.+" % title)

    for i in range(1000):
        codeEdit = main_window.Edit3
        codeEdit.set_focus()
        codeEdit.set_text("")
        wu.press(*"111")
        rect = codeEdit.rectangle()

        pos = (rect.right + 3, rect.top, rect.right + 60, rect.bottom)
        img = ImageGrab.grab(pos)
        img.save("./img_train_cut/%d.png" % i)
        main_window.type_keys("{ENTER}")
        time.sleep(0.5)


def _close_popup_window(_main_window, _app):
    popup_hwnd = _main_window.popup_window()
    print("%x" % popup_hwnd)
    popup_window = _app.window(handle=popup_hwnd)
    btn = popup_window.Button
    btn.click()


def ths_code():
    title = "网上股票交易系统5.0"
    _main_hwnd = get_handle(title, conf.exe_yhzq)
    _app = pw.Application(backend="win32").connect(handle=_main_hwnd)
    _main_window = _app.window(title=title)

    login_window = _app.用户登录
    login_window.Edit1.set_edit_text("ddddd")
    login_window.Edit2.set_edit_text("dddd")
    for i in range(1000):
        codeEdit = login_window.Edit3
        codeEdit.set_focus()
        codeEdit.set_text("")
        wu.press(*"1")
        rect = login_window.Static1.rectangle()
        pos = (rect.left, rect.top, rect.right, rect.bottom)
        img = ImageGrab.grab(pos)
        # code = ths_img_to_str(img)
        code = i
        img.save("./img_data/%s.png" % code)
        login_window['确定(&Y)'].click()
        time.sleep(0.1)
        print("验证码：%d" % i)
        _close_popup_window(login_window, _app)


def ghzq_code():
    title = "金贝壳网上交易系统"
    _main_hwnd = get_handle(title, conf.exe_ghzq)
    _app = pw.Application(backend="win32").connect(handle=_main_hwnd)
    _main_window = _app.window(title=title, class_name="TfrmLoginBaseEx")

    def close():
        try:
            d = _app.windows(title="错误", class_name="TfrmDialogs")[0]
            popup_window = _app.window(handle=d.handle)
            popup_window.Button.click()
        except:
            pass

    for i in range(300):
        codeEdit = _main_window.Edit2
        codeEdit.set_text("1")
        rect = codeEdit.rectangle()
        pos = (rect.right + 10, rect.top, rect.right + 76, rect.bottom)
        print(pos)
        img = ImageGrab.grab(pos)
        code = ghzq_img_to_str(img)
        # code = i
        img.save("./img_data/%s.png" % code)
        _main_window['登录'].click()
        time.sleep(0.1)
        print("验证码：%d" % i)
        close()


if __name__ == '__main__':
    # tdx_code()
    # ths_code()
    ghzq_code()
