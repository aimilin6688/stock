package com.ruoyi.stock.mapper;

import java.math.BigDecimal;
import java.util.List;

import com.ruoyi.stock.domain.StockAccountInit;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;

/**
 * 账户初始信息Mapper接口
 * 
 * @author jonk
 * @date 2021-01-08
 */
public interface StockAccountInitMapper 
{
    /**
     * 查询账户初始信息
     * 
     * @param id 账户初始信息ID
     * @return 账户初始信息
     */
    public StockAccountInit selectStockAccountInitById(Long id);

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
     * 删除账户初始信息
     * 
     * @param id 账户初始信息ID
     * @return 结果
     */
    public int deleteStockAccountInitById(Long id);

    /**
     * 批量删除账户初始信息
     * 
     * @param ids 需要删除的数据ID
     * @return 结果
     */
    public int deleteStockAccountInitByIds(Long[] ids);

    // 查询账户初始资金
    @Select("select init_money from stock_account_init where account_id =#{accountId} limit 1")
    public BigDecimal queryInitMoney(@Param("accountId") Long accountId);

    /**
     * 通过账户Id查询
     * @param accountId 账户Id
     * @return
     */
    StockAccountInit selectByAccountId(Long accountId);
}
