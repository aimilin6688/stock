package com.ruoyi.stock.service;

import java.util.Date;
import java.util.List;
import com.ruoyi.stock.domain.StockDeal;

/**
 * 成交Service接口
 * 
 * @author jonk
 * @date 2021-01-08
 */
public interface IStockDealService 
{
    /**
     * 查询成交
     * 
     * @param id 成交ID
     * @return 成交
     */
    public StockDeal selectStockDealById(Long id);

    /**
     * 查询成交列表
     * 
     * @param stockDeal 成交
     * @return 成交集合
     */
    public List<StockDeal> selectStockDealList(StockDeal stockDeal);

    /**
     * 新增成交
     * 
     * @param stockDeal 成交
     * @return 结果
     */
    public int insertStockDeal(StockDeal stockDeal);

    /**
     * 修改成交
     * 
     * @param stockDeal 成交
     * @return 结果
     */
    public int updateStockDeal(StockDeal stockDeal);

    /**
     * 批量删除成交
     * 
     * @param ids 需要删除的成交ID
     * @return 结果
     */
    public int deleteStockDealByIds(Long[] ids);

    /**
     * 删除成交信息
     * 
     * @param id 成交ID
     * @return 结果
     */
    public int deleteStockDealById(Long id);

    /**
     * 通过账户Id和时间删除
     * @param accountId 账户Id
     * @param date 日期
     * @return
     */
    public int deleteByAccountIdAndDate(Long accountId, Date date);
}
