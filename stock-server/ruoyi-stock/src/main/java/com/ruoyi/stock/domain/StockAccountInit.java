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
 * 账户初始信息对象 stock_account_init
 * 
 * @author jonk
 * @date 2021-01-08
 */
@Data
public class StockAccountInit  implements IAccountFiller
{
    private static final long serialVersionUID = 1L;

    /** $column.columnComment */
    private Long id;

    /** 账户ID */
    @Excel(name = "账户ID")
    private Long accountId;

    /** 初始日期 */
    @JsonFormat(pattern = "yyyy-MM-dd")
    @Excel(name = "初始日期", width = 30, dateFormat = "yyyy-MM-dd")
    private Date initDate;

    /** 初始资金 */
    @Excel(name = "初始资金")
    private BigDecimal initMoney;

    /** 运行天数 */
    @Excel(name = "运行天数")
    private Long runDay;

    /** 账户名称，数据库没有该字段 */
    @Excel(name = "账户名称")

    /** 更新时间 */
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private Date updateTime;

    /** 账户信息 */
    private SimpleAccountVo account;
}
