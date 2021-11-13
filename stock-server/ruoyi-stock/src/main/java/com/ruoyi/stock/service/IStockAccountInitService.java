package com.ruoyi.stock.service;

import java.math.BigDecimal;
import java.util.List;

import com.ruoyi.stock.domain.StockAccountInit;
import org.apache.ibatis.annotations.Param;

/**
 * 账户初始信息Service接口
 * 
 * @author jonk
 * @date 2021-01-08
 */
public interface IStockAccountInitService 
{
    /**
     * 查询账户初始信息
     * 
     * @param id 账户初始信息ID
     * @return 账户初始信息
     */
    public StockAccountInit selectStockAccountInitById(Long id);

    /**
     * 通过账户Id查询
     * @param accountId 账户Id
     * @return StockAccountInit
     */
    public StockAccountInit selectByAccountId(Long accountId);

    /**
     * 查询账户初始信息列表
     * 
     * @param stockAccountInit 账户初始信息
     * @return 账户初始信息集合
     */
    public List<StockAccountInit> selectStockAccountInitList(StockAccountInit stockAccountInit);

    /**
     * 新增账户初始信息
     * 
     * @param stockAccountInit 账户初始信息
     * @return 结果
     */
    public int insertStockAccountInit(StockAccountInit stockAccountInit);

    /**
     * 修改账户初始信息
     * 
     * @param stockAccountInit 账户初始信息
     * @return 结果
     */
    public int updateStockAccountInit(StockAccountInit stockAccountInit);

    /**
     * 批量删除账户初始信息
     * 
     * @param ids 需要删除的账户初始信息ID
     * @return 结果
     */
    public int deleteStockAccountInitByIds(Long[] ids);

    /**
     * 删除账户初始信息信息
     * 
     * @param id 账户初始信息ID
     * @return 结果
     */
    public int deleteStockAccountInitById(Long id);

    /**
     * 查询账户初始资金
     * @param accountId 账户ID
     * @return 初始资金
     */
    public BigDecimal queryInitMoney(Long accountId);
}
