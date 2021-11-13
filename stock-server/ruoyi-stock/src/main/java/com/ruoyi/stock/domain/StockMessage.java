package com.ruoyi.stock.domain;

import cn.hutool.core.date.DateUtil;
import com.alibaba.fastjson.JSONObject;
import com.alibaba.fastjson.annotation.JSONField;
import com.fasterxml.jackson.annotation.JsonFormat;
import com.fasterxml.jackson.annotation.JsonIgnore;
import com.ruoyi.common.annotation.Excel;
import com.ruoyi.common.core.domain.BaseEntity;
import com.ruoyi.stock.domain.vo.SimpleAccountVo;
import com.ruoyi.stock.enums.SocketMessageServerTypeEnums;
import com.ruoyi.stock.service.IAccountFiller;
import com.ruoyi.stock.socket.bean.Message;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.Date;

/**
 * 消息对象 stock_message
 * 
 * @author jonk
 * @date 2021-01-08
 */
@Data
@NoArgsConstructor
public class StockMessage extends BaseEntity implements IAccountFiller
{
    private static final long serialVersionUID = 1L;

    /** 消息标题 */
    private Long id;

    /** 账户ID */
    @Excel(name = "账户ID")
    private Long accountId;

    /** 客户端Id */
    @Excel(name = "客户端ID")
    private Long clientId;

    /** 消息内容 */
    @JsonIgnore
    @JSONField(serialize = false)
    private String body;

    /** 消息类型,参考{@link SocketMessageServerTypeEnums} */
    @Excel(name = "消息类型")
    private Integer type;

    /** 消息标题 */
    @Excel(name = "消息标题")
    private String subject;

    /** 签收时间 */
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    @Excel(name = "签收时间", width = 60, dateFormat = "yyyy-MM-dd HH:mm:ss")
    private Date signTime;

    /** 下发时间 */
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    @Excel(name = "签收时间", width = 60, dateFormat = "yyyy-MM-dd HH:mm:ss")
    private Date sendTime;

    /** 签收客户端ID */
    @Excel(name = "签收客户端ID")
    private Long signClientId;

    /** 消息权重 */
    @Excel(name = "消息权重")
    private Integer weight;

    /** 消息状态：0：未发送，1:已发送, 2:已签收 */
    @Excel(name = "消息状态：0：未发送，1:已发送, 2:已签收")
    private Integer status;

    /** 是否已经执行，1：已执行，0:未执行 */
    @Excel(name = "是否已经执行，1：已执行，0:未执行")
    private Integer executed;

    /** 执行完成时间 */
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    @Excel(name = "执行完成时间", width = 60, dateFormat = "yyyy-MM-dd HH:mm:ss")
    private Date executedTime;

    /** 执行结果简单描述 */
    @Excel(name = "执行结果简单描述")
    private String executedResult;

    /** 执行状态 */
    @Excel(name = "执行状态")
    private Boolean executedStatus;

    @JsonIgnore
    @JSONField(serialize = false, deserialize = false)
    private Object data;
    /** 客户端 */
    @Excel(name = "客户端")
    private String clientName;

    // 设置消息内容，序列化反序列化都会忽略
    public void setData(Object data) {
        this.data = data;
        this.body = JSONObject.toJSONString(data);
    }

    /**
     * 将数据库中的消息类型转换成需要下发的消息内容
     * @return
     */
    public Message toMessage(){
        Message message = new Message();
        message.setMsgId(this.getId());
        message.setAccountId(this.getAccountId());
        message.setClientId(this.getClientId());
        message.setType(this.getType());
        message.setSubject(this.getSubject());
        message.setWeight(this.getWeight());
        message.setTime(DateUtil.now());
        message.setData(this.data);
        message.setStatus(true);
        return message;
    }

    public static StockMessage  parse(Message msg){
        StockMessage message = new StockMessage();
        message.setId(msg.getMsgId());
        message.setAccountId(msg.getAccountId());
        message.setClientId(msg.getClientId());
        message.setType(msg.getType());
        message.setSubject(msg.getSubject());
        message.setWeight(msg.getWeight());
        return message;
    }

    public StockMessage(SocketMessageServerTypeEnums typeEnums, Object data){
        this.type = typeEnums.getCode();
        this.subject = typeEnums.getMessage();
        this.data = data;
        this.body = JSONObject.toJSONString(data);
    }

    // 签收消息
    public static StockMessage sign(Long msgId, Object data){
        StockMessage msg =  new StockMessage(SocketMessageServerTypeEnums.SIGN, data);
        msg.setId(msgId);
        return msg;
    }

    public static StockMessage sign(Message msg){
        StockMessage message =  parse(msg);
        message.setType(SocketMessageServerTypeEnums.SIGN.getCode());
        message.setSubject("签收：" + message.getSubject());
        return message;
    }

    /** 账户信息 */
    private SimpleAccountVo account;
}
