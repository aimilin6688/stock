package com.ruoyi.stock.service.impl;

import java.util.Date;
import java.util.List;

import com.ruoyi.stock.mapper.StockPositionMapper;
import com.ruoyi.stock.service.IStockPositionService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.stock.domain.StockPosition;

/**
 * 持仓Service业务层处理
 * 
 * @author ruoyi
 * @date 2021-01-11
 */
@Service
public class StockPositionServiceImpl implements IStockPositionService
{
    @Autowired
    private StockPositionMapper stockPositionMapper;
    @Autowired
    private AccountFillerService accountFillerService;

    /**
     * 查询持仓
     * 
     * @param id 持仓ID
     * @return 持仓
     */
    @Override
    public StockPosition selectStockPositionById(Long id)
    {
        return stockPositionMapper.selectStockPositionById(id);
    }

    /**
     * 查询持仓列表
     * 
     * @param stockPosition 持仓
     * @return 持仓
     */
    @Override
    public List<StockPosition> selectStockPositionList(StockPosition stockPosition)
    {
        List<StockPosition> positionList =  stockPositionMapper.selectStockPositionList(stockPosition);
        accountFillerService.fill(positionList);
        return positionList;
    }

    /**
     * 新增持仓
     * 
     * @param stockPosition 持仓
     * @return 结果
     */
    @Override
    public int insertStockPosition(StockPosition stockPosition)
    {
        return stockPositionMapper.insertStockPosition(stockPosition);
    }

    /**
     * 修改持仓
     * 
     * @param stockPosition 持仓
     * @return 结果
     */
    @Override
    public int updateStockPosition(StockPosition stockPosition)
    {
        return stockPositionMapper.updateStockPosition(stockPosition);
    }

    /**
     * 批量删除持仓
     * 
     * @param ids 需要删除的持仓ID
     * @return 结果
     */
    @Override
    public int deleteStockPositionByIds(Long[] ids)
    {
        return stockPositionMapper.deleteStockPositionByIds(ids);
    }

    /**
     * 删除持仓信息
     * 
     * @param id 持仓ID
     * @return 结果
     */
    @Override
    public int deleteStockPositionById(Long id)
    {
        return stockPositionMapper.deleteStockPositionById(id);
    }

    @Override
    public int deleteByAccountIdAndDate(Long accountId, Date date) {
        return stockPositionMapper.deleteByAccountIdAndDate(accountId,date);
    }
}
