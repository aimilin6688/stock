package com.ruoyi.common.utils;

import com.ruoyi.common.config.RuoYiConfig;
import com.ruoyi.common.utils.http.HttpUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.HashMap;

public class DingUtils {
    private static final Logger log = LoggerFactory.getLogger(DingUtils.class);

    public static void sendDing(String msg) {
        try {
            String url = "https://oapi.dingtalk.com/robot/send?access_token="+ RuoYiConfig.getDingAccessToken();
			String params = String.format("{\"msgtype\": \"text\", \"text\": {\"content\": \"%s\n%s\"}}",DateUtils.now(), msg);
			HashMap<String, String> headers = new HashMap<>();
			headers.put("Content-Type","application/json");
			String response = HttpUtils.sendPost(url, params,headers);
            log.info("发送钉钉消息：{}，结果：{}", msg, response);
        } catch (Exception e) {
            log.error(e.getMessage(), e);
        }
    }
}
