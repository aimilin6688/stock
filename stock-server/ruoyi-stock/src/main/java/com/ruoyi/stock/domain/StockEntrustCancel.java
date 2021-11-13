package com.ruoyi.stock.domain;

import lombok.Data;
import java.util.Date;
import com.fasterxml.jackson.annotation.JsonFormat;
import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;
import com.ruoyi.common.annotation.Excel;
import com.ruoyi.common.core.domain.BaseEntity;

/**
 * 委托撤销对象 stock_entrust_cancel
 * 
 * @author jonk
 * @date 2021-01-13
 */
@Data
public class StockEntrustCancel extends BaseEntity
{
    private static final long serialVersionUID = 1L;

    /** 主键 */
    private Long id;

    /** 账户Id */
    @Excel(name = "账户Id")
    private Long accountId;

    /** 撤销委托类型 */
    @Excel(name = "撤销委托类型")
    private Long type;

    /** 股票代码 */
    @Excel(name = "股票代码")
    private String codes;

    /** 委托单号 */
    @Excel(name = "委托单号")
    private String entrustNos;

    /** 执行结果 */
    @Excel(name = "执行结果")
    private String exeResult;

    /** 执行时间 */
    @JsonFormat(pattern = "yyyy-MM-dd")
    @Excel(name = "执行时间", width = 30, dateFormat = "yyyy-MM-dd")
    private Date exeTime;


}
