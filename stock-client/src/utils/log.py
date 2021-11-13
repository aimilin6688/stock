# -*- coding:utf-8 -*-
import logging
import logging.handlers
from logging import Formatter
import os


def init_log(file_name="stock_client.log", log_name="stock_client", level=logging.DEBUG):
    fmt = Formatter('%(asctime)s %(levelname)s [%(filename)s %(funcName)s:%(lineno)d]-%(thread)d: %(message)s ')

    pwd = os.path.dirname(os.path.split(os.path.realpath(__file__))[0])
    path = os.path.join(os.path.split(pwd)[0], 'logs/%s'%file_name)

    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))

    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(fmt)

    file_handler = logging.handlers.TimedRotatingFileHandler(path, when="D", backupCount=30, encoding="utf-8")
    file_handler.setLevel(level)
    file_handler.setFormatter(fmt)

    log = logging.getLogger(log_name)
    log.addHandler(console_handler)
    log.addHandler(file_handler)
    log.setLevel(level)
    return log


def is_exists_log(file_name):
    pwd = os.path.split(os.path.realpath(__file__))[0]
    path = os.path.join(os.path.split(pwd)[0], 'logs/%s' % file_name)
    if os.path.exists(path) and os.path.isfile(path):
        return True
    return False

