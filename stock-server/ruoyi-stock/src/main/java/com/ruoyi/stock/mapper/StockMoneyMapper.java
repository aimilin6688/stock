package com.ruoyi.stock.mapper;

import java.math.BigDecimal;
import java.util.Date;
import java.util.List;

import com.ruoyi.stock.domain.StockMoney;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Select;

/**
 * 账户资金Mapper接口
 * 
 * @author jonk
 * @date 2021-01-08
 */
public interface StockMoneyMapper
{
    /**
     * 查询账户资金
     * 
     * @param id 账户资金ID
     * @return 账户资金
     */
    public StockMoney selectStockMoneyById(Long id);

    /**
     * 查询账户资金列表
     * 
     * @param stockMoney 账户资金
     * @return 账户资金集合
     */
    public List<StockMoney> selectStockMoneyList(StockMoney stockMoney);

    /**
     * 新增账户资金
     * 
     * @param stockMoney 账户资金
     * @return 结果
     */
    public int insertStockMoney(StockMoney stockMoney);

    /**
     * 修改账户资金
     * 
     * @param stockMoney 账户资金
     * @return 结果
     */
    public int updateStockMoney(StockMoney stockMoney);

    /**
     * 删除账户资金
     * 
     * @param id 账户资金ID
     * @return 结果
     */
    public int deleteStockMoneyById(Long id);

    /**
     * 批量删除账户资金
     * 
     * @param ids 需要删除的数据ID
     * @return 结果
     */
    public int deleteStockMoneyByIds(Long[] ids);

    @Select("select total from stock_money where account_id=#{accountId} and `date` <= #{date} order by `date` desc limit 1")
    public BigDecimal queryTotal(@Param("accountId") Long accountId,@Param("date") String date);

    int deleteByAccountIdAndDate(@Param("accountId") Long accountId,@Param("date") Date date);

    List<Double> queryIncrease(@Param("accountId")Long accountId,@Param("startDate") String startDate,@Param("endDate") String endDate);
}
