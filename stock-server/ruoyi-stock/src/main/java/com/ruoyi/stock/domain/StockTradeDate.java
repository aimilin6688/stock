package com.ruoyi.stock.domain;

import com.baomidou.mybatisplus.annotation.TableId;
import lombok.Data;

import java.io.Serializable;
import java.util.Date;
import com.fasterxml.jackson.annotation.JsonFormat;
import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;
import com.ruoyi.common.annotation.Excel;
import com.ruoyi.common.core.domain.BaseEntity;

/**
 * 交易日对象 stock_trade_date
 * 
 * @author jonk
 * @date 2021-01-15
 */
@Data
public class StockTradeDate implements Serializable
{
    private static final long serialVersionUID = 1L;

    @TableId
    private String tradeDate;

    /** 1：开市，0：闭市 */
    @Excel(name = "1：开市，0：闭市")
    private Integer isOpen;

}