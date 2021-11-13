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
 * 账户每日客户端导出委托数据对象 stock_entrust
 * 
 * @author jonk
 * @date 2021-01-08
 */
@Data
public class StockEntrust extends BaseEntity implements IAccountFiller
{
    private static final long serialVersionUID = 1L;

    /** $column.columnComment */
    @Excel(name = "${comment}", readConverterExp = "$column.readConverterExp()")
    private Long id;

    /** 账户Id */
    @Excel(name = "账户Id")
    private Long accountId;

    /** 委托日期 */
    @JsonFormat(pattern = "yyyy-MM-dd")
    @Excel(name = "委托日期", width = 30, dateFormat = "yyyy-MM-dd")
    private Date date;

    /** 证券代码 */
    @Excel(name = "证券代码")
    private String stockCode;

    /** 证券名称 */
    @Excel(name = "证券名称")
    private String stockName;

    /** 委托编号 */
    @Excel(name = "委托编号")
    private String entrustNo;

    /** 委托日期 */
    @Excel(name = "委托日期")
    private String entrustDate;

    /** 委托时间 */
    @Excel(name = "委托时间")
    private String entrustTime;

    /** 委托类型 */
    @Excel(name = "委托类型")
    @JSONField(deserializeUsing= StockBuySellUtils.class)
    private Integer type;

    /** 委托数量 */
    @Excel(name = "委托数量")
    private Long num;

    /** 委托价格 */
    @Excel(name = "委托价格")
    private BigDecimal price;

    /** 成交数量 */
    @Excel(name = "成交数量")
    private Long dealNum;

    /** 成交均价 */
    @Excel(name = "成交均价")
    private BigDecimal dealPrice;

    /** 股东代码 */
    @Excel(name = "股东代码")
    private String stockHolder;

    /** 交易市场 */
    @Excel(name = "交易市场")
    private String tradingMarket;

    /** 账户信息 */
    private SimpleAccountVo account;

}
