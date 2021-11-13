import os
from configparser import ConfigParser
import datetime


class LazyProperty(object):
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            value = self.func(instance)
            setattr(instance, self.func.__name__, value)
            return value


class GetConfig(object):
    """
    to get config from config.ini
    """
    LOAD_FROM_DB = "db"
    LOAD_FROM_FILE = "file"

    def __init__(self):
        self.pwd = os.path.split(os.path.realpath(__file__))[0]
        self.root_path = os.path.dirname(os.path.split(self.pwd)[0])
        self.config_path = os.path.join(self.root_path, 'config.ini')
        self.config_file = ConfigParser()
        self.config_file.read(self.config_path, encoding="UTF-8")

    # client
    @LazyProperty
    def client_id(self):
        return self.get('client', 'client_id')

    @LazyProperty
    def client_token(self):
        return self.get('client', 'client_token')

    @LazyProperty
    def ws_url(self):
        return self.get('client', 'ws_url')

    @LazyProperty
    def http_url(self):
        return self.get('client', 'http_url')

    @LazyProperty
    def support_brokers(self):
        brokers = self.get('client', 'support_brokers').replace("，", ",")
        return brokers.split(",")

    @LazyProperty
    def root_path(self):
        return self.root_path

    @LazyProperty
    def ding_access_token(self):
        return self.get('client', 'ding_access_token')

    @LazyProperty
    def show_method_exe_time(self):
        return self.config_file.getboolean('client', 'show_method_exe_time')

    @property
    def now(self):
        return datetime.datetime.now().strftime("%Y%m%d")

    def get(self, section, option):
        return self.config_file.get(section, option)


conf = GetConfig()

if __name__ == '__main__':
    import time
    gg = GetConfig()
    print("client_id:", gg.client_id)
    print("root_path:", gg.root_path)
    print("ws_url:", gg.ws_url)
    print("now: ", gg.now)
    print("support_brokers: ", gg.support_brokers)
