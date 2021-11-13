package com.ruoyi.stock.service;

import java.util.List;
import com.ruoyi.stock.domain.StockBroker;

/**
 * 券商Service接口
 * 
 * @author jonk
 * @date 2021-01-06
 */
public interface IStockBrokerService 
{
    /**
     * 查询券商
     * 
     * @param id 券商ID
     * @return 券商
     */
    public StockBroker selectStockBrokerById(Long id);

    /**
     * 查询券商列表
     * 
     * @param stockBroker 券商
     * @return 券商集合
     */
    public List<StockBroker> selectStockBrokerList(StockBroker stockBroker);

    /**
     * 新增券商
     * 
     * @param stockBroker 券商
     * @return 结果
     */
    public int insertStockBroker(StockBroker stockBroker);

    /**
     * 修改券商
     * 
     * @param stockBroker 券商
     * @return 结果
     */
    public int updateStockBroker(StockBroker stockBroker);

    /**
     * 批量删除券商
     * 
     * @param ids 需要删除的券商ID
     * @return 结果
     */
    public int deleteStockBrokerByIds(Long[] ids);

    /**
     * 删除券商信息
     * 
     * @param id 券商ID
     * @return 结果
     */
    public int deleteStockBrokerById(Long id);

    public Long selectIdByName(String name);
}
