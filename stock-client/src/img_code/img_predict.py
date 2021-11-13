import os
import logging
import numpy as np
from PIL import Image
import joblib

from .cut_image import img_cut, img_labels, ImgType
from src.utils.config import conf

log = logging.getLogger("stock_client")

clf_map = {}


def __get_clf(img_type: ImgType):
    name = img_type.name
    if name in clf_map:
        return clf_map[name]
    clf = joblib.load(os.path.join(conf.root_path, "img_code", "model", "%s.pkl" % name))
    clf_map[name] = clf
    return clf


def __img_to_str(img: Image, img_type: ImgType):
    """
    通达信验证码识别
    :param img:
    :return:
    """
    try:
        img_array = np.array(img)
        ic = img_cut(img_array, img_type=img_type)

        pre_text = []
        for i in range(4):
            # 图片转换成1维后，变成[[图片数组]]，2维的输入变量x
            im_temp = ic[i]
            # print type(im_temp)
            image = im_temp.reshape(-1)
            # print image.shape
            tmp = []
            tmp.append(list(image))
            x = np.array(tmp)

            pre_y = __get_clf(img_type).predict(x)
            pre_index = np.argmax(pre_y[0])
            pre_text.append(str(img_labels(img_type)[pre_index]))
        pre_text = ''.join(pre_text)
        log.info("KNN识别验证码为：%s, 类型：%s", pre_text, img_type.name)
        return pre_text
    except Exception as e:
        log.exception(e)
        return ""


def tdx_img_to_str(img: Image):
    # 通达信验证码类型
    return __img_to_str(img, ImgType.tdx)


def ths_img_to_str(img: Image):
    # 同花顺验证码
    return __img_to_str(img, ImgType.ths)


def ghzq_img_to_str(img: Image):
    # 同花顺验证码
    return __img_to_str(img, ImgType.ghzq)
