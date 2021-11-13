package com.ruoyi.stock.mapper;

import java.util.Date;
import java.util.List;
import com.ruoyi.stock.domain.StockEntrust;
import org.apache.ibatis.annotations.Param;

/**
 * 账户每日客户端导出委托数据Mapper接口
 * 
 * @author jonk
 * @date 2021-01-08
 */
public interface StockEntrustMapper 
{
    /**
     * 查询账户每日客户端导出委托数据
     * 
     * @param id 账户每日客户端导出委托数据ID
     * @return 账户每日客户端导出委托数据
     */
    public StockEntrust selectStockEntrustById(Long id);

    /**
     * 查询账户每日客户端导出委托数据列表
     * 
     * @param stockEntrust 账户每日客户端导出委托数据
     * @return 账户每日客户端导出委托数据集合
     */
    public List<StockEntrust> selectStockEntrustList(StockEntrust stockEntrust);

    /**
     * 新增账户每日客户端导出委托数据
     * 
     * @param stockEntrust 账户每日客户端导出委托数据
     * @return 结果
     */
    public int insertStockEntrust(StockEntrust stockEntrust);

    /**
     * 修改账户每日客户端导出委托数据
     * 
     * @param stockEntrust 账户每日客户端导出委托数据
     * @return 结果
     */
    public int updateStockEntrust(StockEntrust stockEntrust);

    /**
     * 删除账户每日客户端导出委托数据
     * 
     * @param id 账户每日客户端导出委托数据ID
     * @return 结果
     */
    public int deleteStockEntrustById(Long id);

    /**
     * 批量删除账户每日客户端导出委托数据
     * 
     * @param ids 需要删除的数据ID
     * @return 结果
     */
    public int deleteStockEntrustByIds(Long[] ids);
    int deleteByAccountIdAndDate(@Param("accountId") Long accountId, @Param("date") Date date);
}
