package com.ruoyi.stock.service.impl;

import java.util.Date;
import java.util.List;
import com.ruoyi.common.utils.DateUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.stock.mapper.StockEntrustUserMapper;
import com.ruoyi.stock.domain.StockEntrustUser;
import com.ruoyi.stock.service.IStockEntrustUserService;

/**
 * 用户委托信息Service业务层处理
 * 
 * @author jonk
 * @date 2021-01-08
 */
@Service
public class StockEntrustUserServiceImpl implements IStockEntrustUserService 
{
    @Autowired
    private StockEntrustUserMapper stockEntrustUserMapper;
    @Autowired
    private AccountFillerService accountFillerService;
    /**
     * 查询用户委托信息
     * 
     * @param id 用户委托信息ID
     * @return 用户委托信息
     */
    @Override
    public StockEntrustUser selectStockEntrustUserById(Long id)
    {
        return accountFillerService.fill(stockEntrustUserMapper.selectStockEntrustUserById(id));
    }

    /**
     * 查询用户委托信息列表
     * 
     * @param stockEntrustUser 用户委托信息
     * @return 用户委托信息
     */
    @Override
    public List<StockEntrustUser> selectStockEntrustUserList(StockEntrustUser stockEntrustUser)
    {
        return accountFillerService.fill(stockEntrustUserMapper.selectStockEntrustUserList(stockEntrustUser));
    }

    /**
     * 新增用户委托信息
     * 
     * @param stockEntrustUser 用户委托信息
     * @return 结果
     */
    @Override
    public int insertStockEntrustUser(StockEntrustUser stockEntrustUser)
    {
        stockEntrustUser.setCreateTime(new Date());
        return stockEntrustUserMapper.insertStockEntrustUser(stockEntrustUser);
    }

    /**
     * 修改用户委托信息
     * 
     * @param stockEntrustUser 用户委托信息
     * @return 结果
     */
    @Override
    public int updateStockEntrustUser(StockEntrustUser stockEntrustUser)
    {
        stockEntrustUser.setUpdateTime(new Date());
        return stockEntrustUserMapper.updateStockEntrustUser(stockEntrustUser);
    }

    /**
     * 批量删除用户委托信息
     * 
     * @param ids 需要删除的用户委托信息ID
     * @return 结果
     */
    @Override
    public int deleteStockEntrustUserByIds(Long[] ids)
    {
        return stockEntrustUserMapper.deleteStockEntrustUserByIds(ids);
    }

    /**
     * 删除用户委托信息信息
     * 
     * @param id 用户委托信息ID
     * @return 结果
     */
    @Override
    public int deleteStockEntrustUserById(Long id)
    {
        return stockEntrustUserMapper.deleteStockEntrustUserById(id);
    }

    @Override
    public int updateEntrustResult(StockEntrustUser stockEntrustUser) {
        return stockEntrustUserMapper.updateEntrustResult(stockEntrustUser);
    }
}
