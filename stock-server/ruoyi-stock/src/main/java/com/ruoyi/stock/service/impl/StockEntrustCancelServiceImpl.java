package com.ruoyi.stock.service.impl;

import java.util.Date;
import java.util.List;
import com.ruoyi.common.utils.DateUtils;
import com.ruoyi.stock.service.IStockEntrustCancelService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.stock.mapper.StockEntrustCancelMapper;
import com.ruoyi.stock.domain.StockEntrustCancel;

/**
 * 委托撤销Service业务层处理
 * 
 * @author jonk
 * @date 2021-01-13
 */
@Service
public class StockEntrustCancelServiceImpl implements IStockEntrustCancelService
{
    @Autowired
    private StockEntrustCancelMapper stockEntrustCancelMapper;

    /**
     * 查询委托撤销
     * 
     * @param id 委托撤销ID
     * @return 委托撤销
     */
    @Override
    public StockEntrustCancel selectStockEntrustCancelById(Long id)
    {
        return stockEntrustCancelMapper.selectStockEntrustCancelById(id);
    }

    /**
     * 查询委托撤销列表
     * 
     * @param stockEntrustCancel 委托撤销
     * @return 委托撤销
     */
    @Override
    public List<StockEntrustCancel> selectStockEntrustCancelList(StockEntrustCancel stockEntrustCancel)
    {
        return stockEntrustCancelMapper.selectStockEntrustCancelList(stockEntrustCancel);
    }

    /**
     * 新增委托撤销
     * 
     * @param stockEntrustCancel 委托撤销
     * @return 结果
     */
    @Override
    public int insertStockEntrustCancel(StockEntrustCancel stockEntrustCancel)
    {
        stockEntrustCancel.setCreateTime(new Date());
        return stockEntrustCancelMapper.insertStockEntrustCancel(stockEntrustCancel);
    }

    /**
     * 修改委托撤销
     * 
     * @param stockEntrustCancel 委托撤销
     * @return 结果
     */
    @Override
    public int updateStockEntrustCancel(StockEntrustCancel stockEntrustCancel)
    {
        return stockEntrustCancelMapper.updateStockEntrustCancel(stockEntrustCancel);
    }

    /**
     * 批量删除委托撤销
     * 
     * @param ids 需要删除的委托撤销ID
     * @return 结果
     */
    @Override
    public int deleteStockEntrustCancelByIds(Long[] ids)
    {
        return stockEntrustCancelMapper.deleteStockEntrustCancelByIds(ids);
    }

    /**
     * 删除委托撤销信息
     * 
     * @param id 委托撤销ID
     * @return 结果
     */
    @Override
    public int deleteStockEntrustCancelById(Long id)
    {
        return stockEntrustCancelMapper.deleteStockEntrustCancelById(id);
    }
}
