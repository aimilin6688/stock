package com.ruoyi.stock.service.impl;

import java.math.BigDecimal;
import java.util.Date;
import java.util.List;
import com.ruoyi.common.utils.DateUtils;
import com.ruoyi.stock.domain.StockAccountInit;
import com.ruoyi.stock.mapper.StockAccountInitMapper;
import com.ruoyi.stock.service.IStockAccountInitService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

/**
 * 账户初始信息Service业务层处理
 * 
 * @author jonk
 * @date 2021-01-08
 */
@Service
public class StockAccountInitServiceImpl implements IStockAccountInitService
{
    @Autowired
    private StockAccountInitMapper stockAccountInitMapper;
    @Autowired
    private AccountFillerService accountFillerService;

    /**
     * 查询账户初始信息
     * 
     * @param id 账户初始信息ID
     * @return 账户初始信息
     */
    @Override
    public StockAccountInit selectStockAccountInitById(Long id)
    {
        return stockAccountInitMapper.selectStockAccountInitById(id);
    }

    @Override
    public StockAccountInit selectByAccountId(Long accountId) {
        return stockAccountInitMapper.selectByAccountId(accountId);
    }

    /**
     * 查询账户初始信息列表
     * 
     * @param stockAccountInit 账户初始信息
     * @return 账户初始信息
     */
    @Override
    public List<StockAccountInit> selectStockAccountInitList(StockAccountInit stockAccountInit)
    {
        List<StockAccountInit> accountInits = stockAccountInitMapper.selectStockAccountInitList(stockAccountInit);
        accountFillerService.fill(accountInits);
        return accountInits;
    }

    /**
     * 新增账户初始信息
     * 
     * @param stockAccountInit 账户初始信息
     * @return 结果
     */
    @Override
    public int insertStockAccountInit(StockAccountInit stockAccountInit)
    {
        return stockAccountInitMapper.insertStockAccountInit(stockAccountInit);
    }

    /**
     * 修改账户初始信息
     * 
     * @param stockAccountInit 账户初始信息
     * @return 结果
     */
    @Override
    public int updateStockAccountInit(StockAccountInit stockAccountInit)
    {
        stockAccountInit.setUpdateTime(new Date());
        return stockAccountInitMapper.updateStockAccountInit(stockAccountInit);
    }

    /**
     * 批量删除账户初始信息
     * 
     * @param ids 需要删除的账户初始信息ID
     * @return 结果
     */
    @Override
    public int deleteStockAccountInitByIds(Long[] ids)
    {
        return stockAccountInitMapper.deleteStockAccountInitByIds(ids);
    }

    /**
     * 删除账户初始信息信息
     * 
     * @param id 账户初始信息ID
     * @return 结果
     */
    @Override
    public int deleteStockAccountInitById(Long id)
    {
        return stockAccountInitMapper.deleteStockAccountInitById(id);
    }

    @Override
    public BigDecimal queryInitMoney(Long accountId) {
        return stockAccountInitMapper.queryInitMoney(accountId);
    }
}
