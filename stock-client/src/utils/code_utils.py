"""
验证码自动识别
"""

import logging

from PIL import Image, ImageEnhance
import pytesseract
from PIL import ImageGrab
from pywinauto.win32structures import RECT
from src.utils.config import conf, os
from src.img_code.img_predict import __img_to_str, ImgType

log = logging.getLogger("stock_client")


def img_to_str(img, img_type: ImgType = None, length=4, enhance=2, lang=None):
    if isinstance(img, str):
        img = Image.open(img)
    imgry = img.convert('L')  # 图像加强，二值化
    sharpness = ImageEnhance.Contrast(imgry)  # 对比度增强
    imgry = sharpness.enhance(enhance)
    code = pytesseract.image_to_string(imgry, lang=lang)
    if img_type and img_type == ImgType.text:
        return code
    if (code == "" or len(code) != length or not code.isdigit()) and img_type is not None:
        code = __img_to_str(img, img_type=img_type)
        if log.isEnabledFor(logging.DEBUG):
            img.save(os.path.join(conf.root_path, "data", "images", "%s.png" % code))
    log.debug("识别的验证码为:%s", code)
    return code


def code_to_str(position, img_type: ImgType = None, length=4, enhance=2, lang=None):
    if isinstance(position, RECT):
        position = (position.left, position.top, position.right, position.bottom)
        log.debug("验证码位置：%s", position)
    img = ImageGrab.grab(position)
    return img_to_str(img, img_type, length=length, enhance=enhance, lang=lang)


if __name__ == '__main__':
    img_path = "../img_code/img/1667.png"
    img = Image.open(img_path)
    print(img_to_str(img))  # print ocr text from image
