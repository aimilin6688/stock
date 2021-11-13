package com.ruoyi.stock.service;

import java.util.Date;
import java.util.List;
import com.ruoyi.stock.domain.StockPosition;

/**
 * 持仓Service接口
 * 
 * @author ruoyi
 * @date 2021-01-11
 */
public interface IStockPositionService 
{
    /**
     * 查询持仓
     * 
     * @param id 持仓ID
     * @return 持仓
     */
    public StockPosition selectStockPositionById(Long id);

    /**
     * 查询持仓列表
     * 
     * @param stockPosition 持仓
     * @return 持仓集合
     */
    public List<StockPosition> selectStockPositionList(StockPosition stockPosition);

    /**
     * 新增持仓
     * 
     * @param stockPosition 持仓
     * @return 结果
     */
    public int insertStockPosition(StockPosition stockPosition);

    /**
     * 修改持仓
     * 
     * @param stockPosition 持仓
     * @return 结果
     */
    public int updateStockPosition(StockPosition stockPosition);

    /**
     * 批量删除持仓
     * 
     * @param ids 需要删除的持仓ID
     * @return 结果
     */
    public int deleteStockPositionByIds(Long[] ids);

    /**
     * 删除持仓信息
     * 
     * @param id 持仓ID
     * @return 结果
     */
    public int deleteStockPositionById(Long id);
    /**
     * 通过账户Id和时间删除
     * @param accountId 账户Id
     * @param date 日期
     * @return
     */
    public int deleteByAccountIdAndDate(Long accountId, Date date);
}
