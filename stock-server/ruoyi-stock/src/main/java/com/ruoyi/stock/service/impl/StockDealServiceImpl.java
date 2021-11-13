package com.ruoyi.stock.service.impl;

import java.util.Date;
import java.util.List;
import com.ruoyi.common.utils.DateUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.stock.mapper.StockDealMapper;
import com.ruoyi.stock.domain.StockDeal;
import com.ruoyi.stock.service.IStockDealService;

/**
 * 成交Service业务层处理
 * 
 * @author jonk
 * @date 2021-01-08
 */
@Service
public class StockDealServiceImpl implements IStockDealService 
{
    @Autowired
    private StockDealMapper stockDealMapper;
    @Autowired
    private AccountFillerService accountFillerService;
    /**
     * 查询成交
     * 
     * @param id 成交ID
     * @return 成交
     */
    @Override
    public StockDeal selectStockDealById(Long id)
    {
        return accountFillerService.fill(stockDealMapper.selectStockDealById(id));
    }

    /**
     * 查询成交列表
     * 
     * @param stockDeal 成交
     * @return 成交
     */
    @Override
    public List<StockDeal> selectStockDealList(StockDeal stockDeal)
    {
        return accountFillerService.fill(stockDealMapper.selectStockDealList(stockDeal));
    }

    /**
     * 新增成交
     * 
     * @param stockDeal 成交
     * @return 结果
     */
    @Override
    public int insertStockDeal(StockDeal stockDeal)
    {
        stockDeal.setCreateTime(new Date());
        return stockDealMapper.insertStockDeal(stockDeal);
    }

    /**
     * 修改成交
     * 
     * @param stockDeal 成交
     * @return 结果
     */
    @Override
    public int updateStockDeal(StockDeal stockDeal)
    {
        return stockDealMapper.updateStockDeal(stockDeal);
    }

    /**
     * 批量删除成交
     * 
     * @param ids 需要删除的成交ID
     * @return 结果
     */
    @Override
    public int deleteStockDealByIds(Long[] ids)
    {
        return stockDealMapper.deleteStockDealByIds(ids);
    }

    /**
     * 删除成交信息
     * 
     * @param id 成交ID
     * @return 结果
     */
    @Override
    public int deleteStockDealById(Long id)
    {
        return stockDealMapper.deleteStockDealById(id);
    }

    /**
     * 通过账户Id和时间删除
     * @param accountId 账户Id
     * @param date 日期
     * @return
     */
    public int deleteByAccountIdAndDate(Long accountId, Date date){
        return stockDealMapper.deleteByAccountIdAndDate(accountId, date);
    }
}
