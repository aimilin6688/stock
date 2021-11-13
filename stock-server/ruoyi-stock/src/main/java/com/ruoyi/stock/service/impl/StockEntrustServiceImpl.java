package com.ruoyi.stock.service.impl;

import java.util.Date;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.stock.mapper.StockEntrustMapper;
import com.ruoyi.stock.domain.StockEntrust;
import com.ruoyi.stock.service.IStockEntrustService;

/**
 * 账户每日客户端导出委托数据Service业务层处理
 * 
 * @author jonk
 * @date 2021-01-08
 */
@Service
public class StockEntrustServiceImpl implements IStockEntrustService 
{
    @Autowired
    private StockEntrustMapper stockEntrustMapper;
    @Autowired
    private AccountFillerService accountFillerService;
    /**
     * 查询账户每日客户端导出委托数据
     * 
     * @param id 账户每日客户端导出委托数据ID
     * @return 账户每日客户端导出委托数据
     */
    @Override
    public StockEntrust selectStockEntrustById(Long id)
    {
        return accountFillerService.fill(stockEntrustMapper.selectStockEntrustById(id));
    }

    /**
     * 查询账户每日客户端导出委托数据列表
     * 
     * @param stockEntrust 账户每日客户端导出委托数据
     * @return 账户每日客户端导出委托数据
     */
    @Override
    public List<StockEntrust> selectStockEntrustList(StockEntrust stockEntrust)
    {
        List<StockEntrust> stockEntrusts = stockEntrustMapper.selectStockEntrustList(stockEntrust);
        accountFillerService.fill(stockEntrusts);
        return stockEntrusts;
    }

    /**
     * 新增账户每日客户端导出委托数据
     * 
     * @param stockEntrust 账户每日客户端导出委托数据
     * @return 结果
     */
    @Override
    public int insertStockEntrust(StockEntrust stockEntrust)
    {
        return stockEntrustMapper.insertStockEntrust(stockEntrust);
    }

    /**
     * 修改账户每日客户端导出委托数据
     * 
     * @param stockEntrust 账户每日客户端导出委托数据
     * @return 结果
     */
    @Override
    public int updateStockEntrust(StockEntrust stockEntrust)
    {
        return stockEntrustMapper.updateStockEntrust(stockEntrust);
    }

    /**
     * 批量删除账户每日客户端导出委托数据
     * 
     * @param ids 需要删除的账户每日客户端导出委托数据ID
     * @return 结果
     */
    @Override
    public int deleteStockEntrustByIds(Long[] ids)
    {
        return stockEntrustMapper.deleteStockEntrustByIds(ids);
    }

    /**
     * 删除账户每日客户端导出委托数据信息
     * 
     * @param id 账户每日客户端导出委托数据ID
     * @return 结果
     */
    @Override
    public int deleteStockEntrustById(Long id)
    {
        return stockEntrustMapper.deleteStockEntrustById(id);
    }

    @Override
    public int deleteByAccountIdAndDate(Long accountId, Date date) {
        return stockEntrustMapper.deleteByAccountIdAndDate(accountId,date);
    }
}
