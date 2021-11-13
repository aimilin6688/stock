package com.ruoyi.stock.domain;

import com.alibaba.fastjson.annotation.JSONField;
import com.baomidou.mybatisplus.annotation.TableField;
import com.fasterxml.jackson.annotation.JsonFormat;
import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.Data;
import com.ruoyi.common.annotation.Excel;
import com.ruoyi.common.core.domain.BaseEntity;

import java.io.Serializable;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;

/**
 * 下单账户对象 stock_account
 * 
 * @author jonk
 * @date 2021-01-06
 */
@Data
public class StockAccount implements Serializable
{
    private static final long serialVersionUID = 1L;

    /** $column.columnComment */
    private Long id;

    /** 用户名 */
    @Excel(name = "用户名")
    private String username;

    /** 密码 */
    private String password;

    /** 通信密码 */
    private String comPassword;

    /** 昵称 */
    @Excel(name = "昵称")
    private String nickname;

    /** 报告名称 */
    @Excel(name = "报告名称")
    private String reportName;

    /** 债券状态 */
    @Excel(name = "债券状态")
    private Integer creditorStatus;

    /** 下单状态 */
    @Excel(name = "下单状态")
    private Integer orderStatus;

    /** 报告状态 */
    @Excel(name = "报告状态")
    private Integer reportStatus;

    /** 状态 */
    @Excel(name = "状态")
    private Integer status;

    /** 账户类型 */
    @Excel(name = "账户类型")
    private Integer type;

    /** 客户端 */
    @Excel(name = "客户端")
    private Long clientId;

    /** 券商 */
    @Excel(name = "券商")
    private Long brokerId;

    /** 排序，越大越靠前 */
    @Excel(name = "排序，越大越靠前")
    private Long sort;

    /** 置顶，决定报告顺序 */
    @Excel(name = "置顶，决定报告顺序")
    private Integer top;

    /** 创建时间 */
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private Date createTime;

    /** 更新时间 */
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private Date updateTime;
    /**
     * 券商
     */
    private StockBroker broker;
    /**
     * 所在客户端
     */
    private StockClient client;

    public String getName(){
        String brokerName = broker == null ? "" : broker.getName();
        String clientName = client == null ? "" : client.getName();
        return String.format("%s (%s - %s)", nickname, brokerName, clientName);
    }

    /** 请求参数 */
    @JsonIgnore
    @JSONField(serialize=false,deserialize = false)
    private Map<String, Object> params = new HashMap<>();
}
