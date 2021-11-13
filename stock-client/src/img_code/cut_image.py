# -*-coding:utf-8 -*-
from __future__ import division
import cv2
import os
from enum import Enum
import numpy as np

labels = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
ghzq_labels = [0, 1, 2, 3, 5, 6, 7, 8, 9]

class ImgType(Enum):
    # 通达信
    tdx = 0
    # 同花顺
    ths = 1
    # 国海证券
    ghzq = 2
    # 字符串
    text = -1


def tdx_img_cut(image):
    """
    大通证券----将图片按照指定像素，拆分成4个小图片
    :param image:
    :return:
    """
    im = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    im_cut_1 = im[0:20, 0:16]
    im_cut_2 = im[0:20, 13:29]
    im_cut_3 = im[0:20, 27:43]
    im_cut_4 = im[0:20, 39:55]
    im_cut = [im_cut_1, im_cut_2, im_cut_3, im_cut_4]
    return im_cut


def ths_img_cut(image):
    """
    同花顺----图片裁剪
    :param image:
    :return:
    """
    im = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    im_cut_1 = im[1:20, 0:14]
    im_cut_2 = im[1:20, 16:30]
    im_cut_3 = im[1:20, 32:46]
    im_cut_4 = im[1:20, 48:62]
    im_cut = [im_cut_1, im_cut_2, im_cut_3, im_cut_4]
    return im_cut


def ghzq_img_cut(image):
    """
    国海证券-----图片裁剪
    :param image:
    :return:
    """
    im = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 字符按照空列分隔，不是固定宽度
    black_index = np.where(np.all(im == im[0, :], axis=0) == True)
    indexs_list = black_index[0].tolist()
    index = []
    for i, item in enumerate(indexs_list):
        if i > 0 and item > indexs_list[i - 1] + 5:
            index.append(indexs_list[i - 1])
    if len(index) < 4:
        index.append(indexs_list[len(indexs_list) - 1])
    index.append(66)
    # print(index)

    # 按照列索引，计算图片的位置，固定宽度
    char_width = 14 # 图片的固定宽度
    sizes = []
    for i in range(1, len(index), 1):
        if index[i] - index[i - 1] > char_width:
            sizes.append((index[i - 1], index[i - 1] + char_width))
        elif index[i] - index[i - 1] < char_width:
            sizes.append((index[i]-char_width, index[i]))
        else:
            sizes.append((index[i-1], index[i]))
    # print(sizes)
    default_sizes = [(6,20),(21,35),(35,49),(49,63)]

    im_cut = []
    for i in range(4):
        try:
            s,e = sizes[i]
        except:
            s,e = default_sizes[i]
        im_cut.append(im[0:20, s:e])
    return im_cut


img_type = ImgType.ghzq


def img_cut(image, img_type: ImgType):
    if img_type == ImgType.tdx:
        return tdx_img_cut(image)
    elif img_type == ImgType.ths:
        return ths_img_cut(image)
    elif img_type == ImgType.ghzq:
        return ghzq_img_cut(image)


def img_labels(img_type: ImgType) -> list:
    if img_type == ImgType.ghzq:
        return ghzq_labels
    return labels


def cut_image(image, num, img_name):
    im_cut = img_cut(image, img_type=img_type)
    for i in range(4):
        cv2.imwrite('./img_cut/' + str(num) + '_' + str(i) + '_' + img_name[i] + '.jpg', im_cut[i])


if __name__ == '__main__':
    img_dir = './img'
    img_name = os.listdir(img_dir)  # 列出文件夹下所有的目录与文件
    for i in range(len(img_name)):
        path = os.path.join(img_dir, img_name[i])
        image = cv2.imread(path)
        name_list = list(img_name[i])[:4]
        # print("----------%s" % img_name[i])
        cut_image(image, i, name_list)
        print('图片%s分割完成' % (i))

    print(u'*****图片分割预处理完成！*****')
