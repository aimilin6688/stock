package com.ruoyi.stock.domain;

import java.math.BigDecimal;
import java.util.Date;
import com.fasterxml.jackson.annotation.JsonFormat;
import com.ruoyi.stock.domain.vo.SimpleAccountVo;
import com.ruoyi.stock.service.IAccountFiller;
import lombok.Data;
import com.ruoyi.common.annotation.Excel;
import com.ruoyi.common.core.domain.BaseEntity;

/**
 * 账户资金对象 stock_money
 * 
 * @author jonk
 * @date 2021-01-08
 */
@Data
public class StockMoney extends BaseEntity implements IAccountFiller
{
    private static final long serialVersionUID = 1L;

    /** 主键 */
    private Long id;

    /** 账户Id */
    @Excel(name = "账户Id")
    private Long accountId;

    /** 日期 */
    @JsonFormat(pattern = "yyyy-MM-dd")
    @Excel(name = "日期", width = 30, dateFormat = "yyyy-MM-dd")
    private Date date;

    /** 总资金 */
    @Excel(name = "总资金")
    private BigDecimal total;

    /** 可用资金 */
    @Excel(name = "可用资金")
    private BigDecimal available;

    /** 资金余额 */
    @Excel(name = "资金余额")
    private BigDecimal balance;

    /** 股票市值 */
    @Excel(name = "股票市值")
    private BigDecimal market;

    /** 可取资金 */
    @Excel(name = "可取资金")
    private BigDecimal withdraw;

    /** 净值 */
    @Excel(name = "净值")
    private BigDecimal netValue;

    /** 最大回测 */
    @Excel(name = "最大回测")
    private BigDecimal maxDrawdown;

    /** 增长率 */
    @Excel(name = "增长率")
    private BigDecimal increase;

    /** 插入日期 */
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    @Excel(name = "插入日期", width = 60, dateFormat = "yyyy-MM-dd HH:mm:ss")
    private Date insertTime;

    /** 账户信息 */
    private SimpleAccountVo account;
}
