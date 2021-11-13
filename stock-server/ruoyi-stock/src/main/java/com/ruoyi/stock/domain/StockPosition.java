package com.ruoyi.stock.domain;

import com.ruoyi.stock.domain.vo.SimpleAccountVo;
import com.ruoyi.stock.service.IAccountFiller;
import lombok.Data;
import java.math.BigDecimal;
import java.util.Date;
import com.fasterxml.jackson.annotation.JsonFormat;
import com.ruoyi.common.annotation.Excel;
import com.ruoyi.common.core.domain.BaseEntity;

/**
 * 持仓对象 stock_position
 * 
 * @author ruoyi
 * @date 2021-01-11
 */
@Data
public class StockPosition extends BaseEntity implements IAccountFiller
{
    private static final long serialVersionUID = 1L;

    /** $column.columnComment */
    private Long id;

    /** 账户Id */
    @Excel(name = "账户Id")
    private Long accountId;

    /** 持仓日期 */
    @JsonFormat(pattern = "yyyy-MM-dd")
    @Excel(name = "持仓日期", width = 30, dateFormat = "yyyy-MM-dd")
    private Date date;

    /** 证券代码 */
    @Excel(name = "证券代码")
    private String stockCode;

    /** 证券名称 */
    @Excel(name = "证券名称")
    private String stockName;

    /** 总数量 */
    @Excel(name = "总数量")
    private Long totalNum;

    /** 可卖数量 */
    @Excel(name = "可卖数量")
    private Long sellNum;

    /** 冻结数量 */
    @Excel(name = "冻结数量")
    private Long freezeNum;

    /** 成本价 */
    @Excel(name = "成本价")
    private BigDecimal costPrice;

    /** 市场价、当前价 */
    @Excel(name = "市场价、当前价")
    private BigDecimal currentPrice;

    /** 市值 */
    @Excel(name = "市值")
    private BigDecimal marketValue;

    /** 盈亏 */
    @Excel(name = "盈亏")
    private BigDecimal profitLoss;

    /** 盈亏比 */
    @Excel(name = "盈亏比")
    private BigDecimal profitLossRatio;

    /** 当日盈亏 */
    @Excel(name = "当日盈亏")
    private BigDecimal todayProfitLoss;

    /** 当日盈亏比 */
    @Excel(name = "当日盈亏比")
    private BigDecimal todayProfitLossRatio;


    /**   # 股东代码 */
    @Excel(name = "股东代码")
    private String stockHolder;

    /**# 交易市场*/
    @Excel(name = "交易市场")
    private String tradingMarket;

    /** 账户信息 */
    private SimpleAccountVo account;
}
