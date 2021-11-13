# socket 服务类
import logging

from src.stock.socket.socket_exceptions import NeedAccount
from src.stock.socket.socket_message_handler import SocketMessageHandler
from src.utils.config import conf
from src.stock.socket.socket_result_bean import SocketMessageType, SocketMessage, SocketResult
log = logging.getLogger("stock_client")


class SocketService:

    @staticmethod
    def support_brokers():
        """
        支持的券商，返回SocketResult对象
        :return: SocketResult
        """
        # {"clientId": 1, brokerName: ['中信建投', '银河证券']}
        data = {"clientId": conf.client_id, "brokerNames": conf.support_brokers}
        msg = SocketMessage(data, typeEnum=SocketMessageType.H_SUPPORT_BROKER)
        return SocketResult.send_success(msg)

    @staticmethod
    def handler_message(ws, message:str):
        """
        处理websocket消息
        :param message: 消息
        :return:
        """
        result = SocketResult.parse(message)
        if not result.success:
            log.error("异常消息不处理：{}", message)
            return
        msg = result.data
        msg_type = SocketMessageType.parse(msg.type)
        # 签收消息不做处理
        if msg_type == SocketMessageType.SIGN:
            log.debug("签收消息，不处理！消息Id:%d,主题：【%s】", msg.msgId, msg.subject)
            return

        # 非当前客户端不处理
        if str(msg.clientId) != str(conf.client_id):
            log.debug("客户端错误，当前客户端：%s，消息客户端：%s", msg.clientId, conf.client_id)
            return

        # 其他消息先直接签收，之后在做处理
        SocketService.message_sign(ws, msg)

        try:
            return_result = None
            message_handler = SocketMessageHandler(msg)
            if msg_type == SocketMessageType.LOGIN:
                return_result = message_handler.login()
            if msg_type == SocketMessageType.LOGOUT:
                return_result = message_handler.logout()
            if msg_type == SocketMessageType.DEAL:
                return_result = message_handler.deal()
            if msg_type == SocketMessageType.ENTRUST:
                return_result = message_handler.entrust()
            if msg_type == SocketMessageType.POSITION:
                return_result = message_handler.position()
            if msg_type == SocketMessageType.MONEY:
                return_result = message_handler.money()
            if msg_type == SocketMessageType.BUY:
                return_result = message_handler.buy()
            if msg_type == SocketMessageType.SELL:
                return_result = message_handler.sell()
            if msg_type == SocketMessageType.CANCEL:
                return_result = message_handler.cancel()
            if msg_type == SocketMessageType.CLEAR:
                return_result = message_handler.clear()
            if msg_type == SocketMessageType.ACCOUNT_INFO:
                return_result = message_handler.account_info()

            ws.send(SocketResult.send_success(return_result).to_json())
        except NeedAccount as e1:
            log.warning("缺少账户信息：AccountId: %s", e1.accountId)
            ws.send(SocketResult.send_success(SocketMessage(
                accountId=e1.accountId, clientId=conf.client_id, typeEnum=SocketMessageType.I_ACCOUNT_INFO)).to_json())
        except Exception as e:
            log.exception(e)
            ws.send(SocketResult.send_fail(str(e)).to_json())

    @staticmethod
    def message_sign(ws, msg: SocketMessage):
        """
        发送消息签收
        :param ws: webscoket对象
        :param msg: 消息
        :return: None
        """
        sign_msg = SocketMessage(msgId=msg.msgId,
                                 typeEnum=SocketMessageType.SIGN,
                                 clientId=msg.clientId,
                                 accountId=msg.accountId,
                                 subject="签收：" + msg.subject)
        log.debug("发送签收消息：%s", msg)
        ws.send(SocketResult.send_success(sign_msg).to_json())
