package com.ruoyi.stock.domain;

import java.math.BigDecimal;
import java.util.Date;
import com.fasterxml.jackson.annotation.JsonFormat;
import com.ruoyi.stock.domain.vo.SimpleAccountVo;
import com.ruoyi.stock.service.IAccountFiller;
import lombok.Data;
import com.ruoyi.common.annotation.Excel;
import com.ruoyi.common.core.domain.BaseEntity;
import org.springframework.data.annotation.Version;

/**
 * 用户委托信息对象 stock_entrust_user
 * 
 * @author jonk
 * @date 2021-01-08
 */
@Data
public class StockEntrustUser extends BaseEntity implements IAccountFiller
{
    private static final long serialVersionUID = 1L;

    /** $column.columnComment */
    private Long id;

    /** 消息Id */
    @Excel(name = "消息Id")
    private Long messageId;

    /** 账号Id */
    @Excel(name = "账号Id")
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

    /** 委托数量 */
    @Excel(name = "委托数量")
    private Long num;

    /** 委托仓位 */
    @Excel(name = "委托仓位")
    private BigDecimal position;

    /** 委托价格 */
    @Excel(name = "委托价格")
    private BigDecimal price;

    /** 委托类型， 1：买入，0：卖出 */
    @Excel(name = "委托类型， 1：买入，0：卖出")
    private Integer type;

    /** 委托编号 */
    @Excel(name = "委托编号")
    private String entrustNo;

    /** 委托时间 */
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    @Excel(name = "委托时间", width = 60, dateFormat = "yyyy-MM-dd HH:mm:ss")
    private Date entrustTime;

    /** 委托异常*/
    @Excel(name = "委托异常")
    private String entrustError;

    /** 状态1：委托中，2：已委托, 3:部分成交. 4:全部成交，-1：撤单，-2：部分撤单， -3 委托异常 */
    @Excel(name = "状态1：委托中，2：已委托, 3:部分成交. 4:全部成交，-1：撤单，-2：部分撤单， -3 委托异常")
    private Integer status;

    /** 撤销数量 */
    @Excel(name = "撤销数量")
    private Long cancelNum;

    /** 成交数量 */
    @Excel(name = "成交数量")
    private Long dealNum;

    /** 成交时间 */
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    @Excel(name = "成交时间", width = 60, dateFormat = "yyyy-MM-dd HH:mm:ss")
    private Date dealTime;

    /** 成交编号 */
    @Excel(name = "成交编号")
    private String dealNo;

    /** 数据版本号 */
    @Version
    @Excel(name = "数据版本号")
    private Long version;

    /** 账户信息 */
    private SimpleAccountVo account;
}
