package com.ruoyi.stock.socket.bean;

import cn.hutool.core.date.DateUtil;
import com.alibaba.fastjson.JSONObject;
import com.fasterxml.jackson.annotation.JsonFormat;
import com.ruoyi.common.annotation.Excel;
import lombok.Data;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.StringUtils;

import java.io.Serializable;
import java.util.Date;

@Data
@Slf4j
public class Message implements Serializable {
    private  Long msgId;
    private Long accountId;
    private Long clientId;
    private Integer type;
    private String subject;
    private Integer weight;
    private String time;
    private Object data;
    // 状态信息，主要时执行结果, 成功：true， 失败：false
    private Boolean status;


    /**
     * 获取消息日期，不存在返回当前时间
     * @return Date
     */
    public Date getDate(){
        try {
            if(StringUtils.isBlank(time)) {
                return new Date();
            }else{
                return DateUtil.parse(time);
            }
        } catch (Exception e) {
            log.warn("日期转换异常：{}, 使用当前时间！", this.time);
            return new Date();
        }
    }
}
