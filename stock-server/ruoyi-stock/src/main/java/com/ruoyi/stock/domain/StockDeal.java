package com.ruoyi.stock.domain;

import com.alibaba.fastjson.annotation.JSONField;
import com.fasterxml.jackson.annotation.JsonFormat;
import com.ruoyi.common.annotation.Excel;
import com.ruoyi.common.core.domain.BaseEntity;
import com.ruoyi.stock.domain.vo.SimpleAccountVo;
import com.ruoyi.stock.service.IAccountFiller;
import com.ruoyi.stock.utils.StockBuySellUtils;
import lombok.Data;

import java.math.BigDecimal;
import java.util.Date;

/**
 * 成交对象 stock_deal
 * 
 * @author jonk
 * @date 2021-01-08
 */
@Data
public class StockDeal extends BaseEntity implements IAccountFiller
{
    private static final long serialVersionUID = 1L;

    /** $column.columnComment */
    private Long id;

    /** 账号Id */
    @Excel(name = "账号Id")
    private Long accountId;

    /** 时间 */
    @JsonFormat(pattern = "yyyy-MM-dd")
    @Excel(name = "时间", width = 30, dateFormat = "yyyy-MM-dd")
    private Date date;

    /** 证券代码 */
    @Excel(name = "证券代码")
    private String stockCode;

    /** 证券名称 */
    @Excel(name = "证券名称")
    private String stockName;

    /** 成交日期 */
    @Excel(name = "成交日期")
    private String dealDate;


    /** 成交时间 */
    @Excel(name = "成交时间")
    private String dealTime;

    /** 成交数量 */
    @Excel(name = "成交数量")
    private Long num;

    /**  成交价格 */
    @Excel(name = " 成交价格")
    private BigDecimal price;

    /** 成交金额 */
    @Excel(name = "成交金额")
    private BigDecimal money;

    /** 买卖标志 */
    @Excel(name = "买卖标志")
    @JSONField(deserializeUsing= StockBuySellUtils.class)
    private Integer type;

    /** 成交编号 */
    @Excel(name = "成交编号")
    private String dealNo;

    /** 委托编号 */
    @Excel(name = "委托编号")
    private String entrustNo;

    /** 股东代码 */
    @Excel(name = "股东代码")
    private String stockHolder;

    /**# 交易市场*/
    @Excel(name = "交易市场")
    private String tradingMarket;

    /** 账户信息 */
    private SimpleAccountVo account;
}
