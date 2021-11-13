import logging
import requests
import getpass, socket
from src.utils.date_utils import now
from src.utils.config import conf

user_name = getpass.getuser()  # 获取当前用户名
hostname = socket.gethostname()  # 获取当前主机名

log = logging.getLogger("stock_client")


def send_ding_msg(msg):
    """
    向钉钉发送报警信息
    :param msg: 消息内容
    :return:
    """
    try:
        url = "https://oapi.dingtalk.com/robot/send?access_token="+conf.ding_access_token
        msg = "%s\n主机：%s，用户：%s\n%s" % (now(), hostname, user_name, msg)
        text = {
            "msgtype": "text",
            "text": {
                "content": msg
            },
            "at": {
                "atMobiles": [],
                "isAtAll": False
            }
        }
        log.info("ding_msg: %s", msg)
        r = requests.post(url, json=text)
        if r.status_code == requests.codes.ok:
            return True
        return False
    except Exception as e:
        log.exception(e)


if __name__ == '__main__':
    send_ding_msg("test")
