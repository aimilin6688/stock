package com.ruoyi.stock.service;

import java.math.BigDecimal;
import java.util.Date;
import java.util.List;
import com.ruoyi.stock.domain.StockMoney;

/**
 * 账户资金Service接口
 * 
 * @author jonk
 * @date 2021-01-08
 */
public interface IStockMoneyService 
{
    /**
     * 查询账户资金
     * 
     * @param id 账户资金ID
     * @return 账户资金
     */
    public StockMoney selectStockMoneyById(Long id);

    /**
     * 查询账户资金列表
     * 
     * @param stockMoney 账户资金
     * @return 账户资金集合
     */
    public List<StockMoney> selectStockMoneyList(StockMoney stockMoney);

    /**
     * 新增账户资金
     * 
     * @param stockMoney 账户资金
     * @return 结果
     */
    public int insertStockMoney(StockMoney stockMoney);

    /**
     * 修改账户资金
     * 
     * @param stockMoney 账户资金
     * @return 结果
     */
    public int updateStockMoney(StockMoney stockMoney);

    /**
     * 批量删除账户资金
     * 
     * @param ids 需要删除的账户资金ID
     * @return 结果
     */
    public int deleteStockMoneyByIds(Long[] ids);

    /**
     * 删除账户资金信息
     * 
     * @param id 账户资金ID
     * @return 结果
     */
    public int deleteStockMoneyById(Long id);

    /**
     * 将仓位转换成股数
     * @param accountId 账户ID
     * @param position 仓位信息
     * @param price 价格信息
     * @return 买入股数，手数的整数倍
     */
    public Integer positionToNumber(Long accountId, BigDecimal position, BigDecimal price);
    /**
     * 通过账户Id和时间删除
     * @param accountId 账户Id
     * @param date 日期
     * @return
     */
    public int deleteByAccountIdAndDate(Long accountId, Date date);
}
