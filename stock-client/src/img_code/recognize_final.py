# -*-coding:utf-8 -*-
from __future__ import division

import os

import cv2
import numpy as np

from .cut_image import img_cut, img_type, img_labels


def predict(image, img_name):
    im_cut = img_cut(image, img_type=img_type)
    pre_text = []
    for i in range(4):
        # 图片转换成1维后，变成[[图片数组]]，2维的输入变量x
        im_temp = im_cut[i]
        # print type(im_temp)
        image = im_temp.reshape(-1)
        # print image.shape
        tmp = []
        tmp.append(list(image))
        x = np.array(tmp)

        pre_y = clf.predict(x)
        pre_y = np.argmax(pre_y[0])
        pre_text.append(str(img_labels(img_type)[pre_y]))
    # print pre_text
    pre_text = ''.join(pre_text)
    if pre_text != img_name:
        print('label:%s'%(img_name),'predict:%s'%(pre_text),'\t','false')
        return 0
    else:
        print('label:%s'%(img_name),'predict:%s'%(pre_text))
        return 1


if __name__ == '__main__':
    from sklearn.externals import joblib  # 这里使用的时 sklearn 0.21.3
    img_dir = './img_test'
    img_name = os.listdir(img_dir)  # 列出文件夹下所有的目录与文件
    right = 0
    global clf
    clf = joblib.load('knn.pkl')
    for i in range(len(img_name)):
        path = os.path.join(img_dir, img_name[i])
        image = cv2.imread(path)
        name_list = list(img_name[i])[:4]
        name = ''.join(name_list)
        pre = predict(image, name)
        right += pre
    accuracy = (right/len(img_name))*100
    print(u'准确率为：%s%%,一共%s张验证码，正确：%s,错误：%s'%(accuracy,len(img_name),right,len(img_name)-right))



