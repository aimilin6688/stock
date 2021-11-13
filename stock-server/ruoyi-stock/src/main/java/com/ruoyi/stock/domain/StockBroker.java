package com.ruoyi.stock.domain;

import com.fasterxml.jackson.annotation.JsonFormat;
import lombok.Data;
import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;
import com.ruoyi.common.annotation.Excel;
import com.ruoyi.common.core.domain.BaseEntity;

import java.io.Serializable;
import java.util.Date;

/**
 * 券商对象 stock_broker
 * 
 * @author jonk
 * @date 2021-01-06
 */
@Data
public class StockBroker implements Serializable
{
    private static final long serialVersionUID = 1L;

    /** $column.columnComment */
    private Long id;

    /** 券商 */
    @Excel(name = "券商")
    private String name;

    /** 类型 */
    @Excel(name = "类型")
    private Integer type;

    /** 可执行文件路径 */
    @Excel(name = "可执行文件路径")
    private String exePath;

    /** 创建时间 */
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private Date createTime;

}
