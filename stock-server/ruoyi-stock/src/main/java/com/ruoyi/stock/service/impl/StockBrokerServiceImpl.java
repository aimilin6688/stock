package com.ruoyi.stock.service.impl;

import java.util.Date;
import java.util.List;
import com.ruoyi.common.utils.DateUtils;
import com.ruoyi.stock.mapper.StockBrokerMapper;
import com.ruoyi.stock.service.IStockBrokerService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.stock.domain.StockBroker;

/**
 * 券商Service业务层处理
 * 
 * @author jonk
 * @date 2021-01-06
 */
@Service
public class StockBrokerServiceImpl implements IStockBrokerService
{
    @Autowired
    private StockBrokerMapper stockBrokerMapper;

    /**
     * 查询券商
     * 
     * @param id 券商ID
     * @return 券商
     */
    @Override
    public StockBroker selectStockBrokerById(Long id)
    {
        return stockBrokerMapper.selectStockBrokerById(id);
    }

    /**
     * 查询券商列表
     * 
     * @param stockBroker 券商
     * @return 券商
     */
    @Override
    public List<StockBroker> selectStockBrokerList(StockBroker stockBroker)
    {
        return stockBrokerMapper.selectStockBrokerList(stockBroker);
    }

    /**
     * 新增券商
     * 
     * @param stockBroker 券商
     * @return 结果
     */
    @Override
    public int insertStockBroker(StockBroker stockBroker)
    {
        stockBroker.setCreateTime(new Date());
        return stockBrokerMapper.insertStockBroker(stockBroker);
    }

    /**
     * 修改券商
     * 
     * @param stockBroker 券商
     * @return 结果
     */
    @Override
    public int updateStockBroker(StockBroker stockBroker)
    {
        return stockBrokerMapper.updateStockBroker(stockBroker);
    }

    /**
     * 批量删除券商
     * 
     * @param ids 需要删除的券商ID
     * @return 结果
     */
    @Override
    public int deleteStockBrokerByIds(Long[] ids)
    {
        return stockBrokerMapper.deleteStockBrokerByIds(ids);
    }

    /**
     * 删除券商信息
     * 
     * @param id 券商ID
     * @return 结果
     */
    @Override
    public int deleteStockBrokerById(Long id)
    {
        return stockBrokerMapper.deleteStockBrokerById(id);
    }

    @Override
    public Long selectIdByName(String name) {
        return stockBrokerMapper.selectIdByName(name);
    }
}
