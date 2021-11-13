package com.ruoyi.stock.mapper;

import java.util.List;
import com.ruoyi.stock.domain.StockEntrustCancel;

/**
 * 委托撤销Mapper接口
 * 
 * @author jonk
 * @date 2021-01-13
 */
public interface StockEntrustCancelMapper 
{
    /**
     * 查询委托撤销
     * 
     * @param id 委托撤销ID
     * @return 委托撤销
     */
    public StockEntrustCancel selectStockEntrustCancelById(Long id);

    /**
     * 查询委托撤销列表
     * 
     * @param stockEntrustCancel 委托撤销
     * @return 委托撤销集合
     */
    public List<StockEntrustCancel> selectStockEntrustCancelList(StockEntrustCancel stockEntrustCancel);

    /**
     * 新增委托撤销
     * 
     * @param stockEntrustCancel 委托撤销
     * @return 结果
     */
    public int insertStockEntrustCancel(StockEntrustCancel stockEntrustCancel);

    /**
     * 修改委托撤销
     * 
     * @param stockEntrustCancel 委托撤销
     * @return 结果
     */
    public int updateStockEntrustCancel(StockEntrustCancel stockEntrustCancel);

    /**
     * 删除委托撤销
     * 
     * @param id 委托撤销ID
     * @return 结果
     */
    public int deleteStockEntrustCancelById(Long id);

    /**
     * 批量删除委托撤销
     * 
     * @param ids 需要删除的数据ID
     * @return 结果
     */
    public int deleteStockEntrustCancelByIds(Long[] ids);
}
