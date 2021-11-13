package com.ruoyi.stock.domain;

import java.io.Serializable;
import java.util.Date;
import java.util.List;

import com.fasterxml.jackson.annotation.JsonFormat;
import lombok.Data;
import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;
import com.ruoyi.common.annotation.Excel;
import com.ruoyi.common.core.domain.BaseEntity;

/**
 * 下单客户端对象 stock_client
 * 
 * @author jonk
 * @date 2021-01-06
 */
@Data
public class StockClient implements Serializable
{
    private static final long serialVersionUID = 1L;

    /** $column.columnComment */
    private Long id;

    /** 客户端Id */
    @Excel(name = "客户端Id")
    private String clientToken;

    /** 主机IP */
    @Excel(name = "主机IP")
    private String hostIp;

    /** 主机名称 */
    @Excel(name = "主机名称")
    private String hostName;

    /** 显示名称 */
    @Excel(name = "显示名称")
    private String name;

    /** 最后登录时间 */
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    @Excel(name = "最后登录时间", width = 30, dateFormat = "yyyy-MM-dd HH:mm:ss")
    private Date lastConnectTime;

    /** 在线状态 */
    @Excel(name = "在线状态")
    private Integer onLine;

    /** 状态 */
    @Excel(name = "状态")
    private Long status;

    /** 备注 */
    @Excel(name = "备注")
    private String remark;
}
