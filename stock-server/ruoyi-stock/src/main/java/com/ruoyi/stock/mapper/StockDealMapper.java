package com.ruoyi.stock.mapper;

import java.util.Date;
import java.util.List;
import com.ruoyi.stock.domain.StockDeal;
import org.apache.ibatis.annotations.Param;

/**
 * 成交Mapper接口
 * 
 * @author jonk
 * @date 2021-01-08
 */
public interface StockDealMapper 
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
     * 删除成交
     * 
     * @param id 成交ID
     * @return 结果
     */
    public int deleteStockDealById(Long id);

    /**
     * 批量删除成交
     * 
     * @param ids 需要删除的数据ID
     * @return 结果
     */
    public int deleteStockDealByIds(Long[] ids);

    int deleteByAccountIdAndDate(@Param("accountId") Long accountId,@Param("date") Date date);
}
