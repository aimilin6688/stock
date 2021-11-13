import websocket
import logging
import time
import threading
from src.utils.config import conf
from src.stock.socket.socket_service import SocketService


log = logging.getLogger("stock_client")
# 重新连接上锁
lock_reconnect = False


def on_open(ws):
    log.debug("客户端:%s,打开WebSocket连接！", conf.client_id)
    # 上传支持的券商
    ws.send(SocketService.support_brokers().to_json())


def on_message(ws, message):
    log.debug("接收到消息：%s", message)
    SocketService.handler_message(ws, message)


def on_error(ws, error):
    log.error("异常：{}", error)


def on_close(ws):
    log.debug("客户端：%s，WebSocket断开连接！", conf.client_id)


def reopen():
    global lock_reconnect
    if lock_reconnect:
        return
    lock_reconnect = True
    websocket.enableTrace(True)

    def run():
        while True:
            global lock_reconnect
            ws = websocket.WebSocketApp("%s%s?token=%s" % (conf.ws_url, conf.client_id, conf.client_token),
                                        on_open=on_open,
                                        on_message=on_message,
                                        on_error=on_error,
                                        on_close=on_close)
            ws.run_forever()
            time.sleep(2)
            lock_reconnect = False
    thread1 = threading.Thread(target=run)
    thread1.start()
    return thread1


if __name__ == '__main__':
    from src.utils.log import init_log
    init_log()
    t1 = reopen()
    t1.join()

