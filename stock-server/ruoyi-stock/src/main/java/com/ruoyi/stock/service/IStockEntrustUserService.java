package com.ruoyi.stock.service;

import java.util.List;
import com.ruoyi.stock.domain.StockEntrustUser;

/**
 * 用户委托信息Service接口
 * 
 * @author jonk
 * @date 2021-01-08
 */
public interface IStockEntrustUserService 
{
    /**
     * 查询用户委托信息
     * 
     * @param id 用户委托信息ID
     * @return 用户委托信息
     */
    public StockEntrustUser selectStockEntrustUserById(Long id);

    /**
     * 查询用户委托信息列表
     * 
     * @param stockEntrustUser 用户委托信息
     * @return 用户委托信息集合
     */
    public List<StockEntrustUser> selectStockEntrustUserList(StockEntrustUser stockEntrustUser);

    /**
     * 新增用户委托信息
     * 
     * @param stockEntrustUser 用户委托信息
     * @return 结果
     */
    public int insertStockEntrustUser(StockEntrustUser stockEntrustUser);

    /**
     * 修改用户委托信息
     * 
     * @param stockEntrustUser 用户委托信息
     * @return 结果
     */
    public int updateStockEntrustUser(StockEntrustUser stockEntrustUser);

    /**
     * 批量删除用户委托信息
     * 
     * @param ids 需要删除的用户委托信息ID
     * @return 结果
     */
    public int deleteStockEntrustUserByIds(Long[] ids);

    /**
     * 删除用户委托信息信息
     * 
     * @param id 用户委托信息ID
     * @return 结果
     */
    public int deleteStockEntrustUserById(Long id);

    public int updateEntrustResult(StockEntrustUser stockEntrustUser);
}
