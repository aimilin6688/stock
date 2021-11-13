package com.ruoyi.stock.socket;

import com.alibaba.fastjson.JSONObject;
import com.ruoyi.stock.domain.StockMessage;
import com.ruoyi.stock.enums.SocketMessageServerTypeEnums;
import com.ruoyi.stock.excetion.SendMessageException;
import com.ruoyi.stock.service.IStockAccountService;
import com.ruoyi.stock.service.IStockClientService;
import com.ruoyi.stock.service.IStockMessageService;
import com.ruoyi.stock.socket.bean.SocketResult;
import com.ruoyi.stock.socket.bean.SocketStatusEnums;
import com.ruoyi.stock.socket.service.SocketMessageHandler;
import com.ruoyi.stock.socket.service.StockSocketService;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.collections4.CollectionUtils;
import org.springframework.beans.BeansException;
import org.springframework.context.ApplicationContext;
import org.springframework.context.ApplicationContextAware;
import org.springframework.stereotype.Component;

import javax.websocket.*;
import javax.websocket.server.PathParam;
import javax.websocket.server.ServerEndpoint;
import java.io.IOException;
import java.util.Arrays;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicInteger;

@Slf4j
@Component
@ServerEndpoint(value = "/ws/{clientId}")
public class StockWebSocketServer implements ApplicationContextAware {
    public static final String TOKEN = "token";
    private static ApplicationContext applicationContext;
    private static AtomicInteger onlineNum = new AtomicInteger();
    private static ConcurrentHashMap<Long, Session> sessionMap = new ConcurrentHashMap<>();

    //建立连接成功调用
    @OnOpen
    public void onOpen(Session session, @PathParam(value = "clientId") Long clientId) {
        Map<String, List<String>> params = session.getRequestParameterMap();
        if (params.containsKey(TOKEN)
                && applicationContext.getBean(StockSocketService.class).auth(clientId, params.get(TOKEN).get(0))) {
            sessionMap.put(clientId, session);
            onlineNum.incrementAndGet();
            this.sendMessage(session, SocketResult.success(StockMessage.sign(0l,"登录成功！").toMessage()));
            applicationContext.getBean(IStockClientService.class).onLine(clientId);
            log.info("客户端：{}，加入,当前在线：{}", clientId, onlineNum.get());
        } else {
            this.sendMessage(session, SocketResult.status(SocketStatusEnums.AUTH_FAIL));
            this.close(session);
        }
    }

    //关闭连接时调用
    @OnClose
    public void onClose(@PathParam(value = "clientId") Long clientId) {
        sessionMap.remove(clientId);
        if (onlineNum.get() > 0) {
            onlineNum.decrementAndGet();
        }
        applicationContext.getBean(IStockClientService.class).offLine(clientId);
        log.info("客户端：{}，断开链接，当前在线：{}", clientId, onlineNum.get());
    }

    //收到客户端信息
    @OnMessage
    public void onMessage(String message) throws IOException {
        try {
            log.debug("接收到消息：{}", message);
            applicationContext.getBean(SocketMessageHandler.class).handler(message);
        } catch (Exception e) {
            log.error(e.getMessage(), e);
            StockWebSocketMonitor.fail("消息接受异常："+e.getMessage());
        }
    }

    //错误时调用
    @OnError
    public void onError(Session session, Throwable throwable) {
        log.error("发生异常:"+throwable.getMessage(), throwable);
        throwable.printStackTrace();
    }

    // 发送消息
    public static void sendMessage(Session session, SocketResult result) {
        if(session == null || !session.isOpen()){
            throw new SendMessageException("客户端连接异常");
        }
        try {
            session.getBasicRemote().sendText(JSONObject.toJSONString(result));
        } catch (IOException e) {
            throw new SendMessageException(e);
        }
    }

    public static void sendMessage(StockMessage message){
        StockWebSocketServer.sendMessage(Arrays.asList(message));
    }

    // 先所有账户发送同样的消息
    public static void sendMessage(List<StockMessage> messageList){
        if(CollectionUtils.isEmpty(messageList)){
            log.debug("需要发送的消息为空，不能下发！");
            StockWebSocketMonitor.fail("需要发送的消息为空，不能下发！");
            return;
        }
        IStockAccountService stockAccountService = applicationContext.getBean(IStockAccountService.class);
        IStockClientService stockClientService = applicationContext.getBean(IStockClientService.class);
        IStockMessageService stockMessageService = applicationContext.getBean(IStockMessageService.class);
        for (StockMessage msg : messageList){
            try {
                Long clientId = msg.getClientId();
                if(clientId == null){
                    String fail = String.format("账户：%s,没有配置客户端！", stockAccountService.selectSimpleVoById(msg.getAccountId()).getName());
                    log.warn(fail);
                    StockWebSocketMonitor.fail(fail);
                }else {
                    Session session = sessionMap.get(clientId);
                    if(session == null || !session.isOpen()){
                        throw new SendMessageException(String.format("客户端：%s,已断开连接！", stockClientService.selectNameById(clientId)));
                    }else {
                        sendMessage(session, SocketResult.success(msg.toMessage()));
                        stockMessageService.updateStatusSend(msg.getId());
                    }
                }
            } catch (Exception e) {
                log.error(e.getMessage(), e);
                String error = String.format("账户：%s,发送%s消息失败！原因：%s", stockAccountService.selectSimpleVoById(msg.getAccountId()).getName(),
                        SocketMessageServerTypeEnums.parse(msg.getType()).getMessage(), e.getMessage());
                log.error(error);
                StockWebSocketMonitor.fail(error);
            }
        }
    }

    // 关闭链接
    private void close(Session session) {
        try {
            if (session.isOpen()) {
                session.close();
            }
        } catch (IOException e) {
            log.error(e.getMessage(), e);
        }
    }

    // 注入applicationContext
    public void setApplicationContext(ApplicationContext applicationContext) throws BeansException {
        StockWebSocketServer.applicationContext = applicationContext;
    }
}