package com.ruoyi.stock.socket;

import com.alibaba.fastjson.JSONObject;
import com.ruoyi.stock.socket.bean.SocketResult;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import javax.websocket.OnClose;
import javax.websocket.OnOpen;
import javax.websocket.Session;
import javax.websocket.server.ServerEndpoint;
import java.io.IOException;
import java.util.concurrent.CopyOnWriteArraySet;

/**
 *  即使反馈消息给前端
 */
@Slf4j
@Component
@ServerEndpoint(value = "/ws/monitor")
public class StockWebSocketMonitor {
    private static CopyOnWriteArraySet<Session> sessionSet = new CopyOnWriteArraySet<>();

    @OnOpen
    public void onOpen(Session session) {
        sessionSet.add(session);
        log.debug("客户端链接");
    }

    @OnClose
    public void onClose(Session session) {
        sessionSet.remove(session);
        log.debug("客户端关闭");
    }

    public static void fail(String result){
        sendMessage(SocketResult.fail(result));
    }

    public static void success(String result){
        sendMessage(SocketResult.success(result));
    }

    // 只用于发送监控消息
    public static void sendMessage(SocketResult result){
        for (Session session : sessionSet) {
            try {
                if(session.isOpen()){
                    String message = JSONObject.toJSONString(result);
                    log.debug("监控发送：{}", message);
                    session.getBasicRemote().sendText(message);
                }
            } catch (IOException e) {
                log.error(e.getMessage(), e);
            }
        }
    }
}
