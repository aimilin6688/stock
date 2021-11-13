package com.ruoyi.stock.mapper;

import java.util.List;
import com.ruoyi.stock.domain.StockBroker;
import org.apache.ibatis.annotations.Select;

/**
 * 券商Mapper接口
 * 
 * @author jonk
 * @date 2021-01-06
 */
public interface StockBrokerMapper 
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
     * 查询券商列表
     *
     * @param clientId clientId
     * @return 券商集合
     */
    public List<StockBroker> selectStockBrokerListByClientId(Long clientId);

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
     * 删除券商
     * 
     * @param id 券商ID
     * @return 结果
     */
    public int deleteStockBrokerById(Long id);

    /**
     * 批量删除券商
     * 
     * @param ids 需要删除的数据ID
     * @return 结果
     */
    public int deleteStockBrokerByIds(Long[] ids);

    @Select("select id from stock_broker where name =#{name}")
    Long selectIdByName(String name);
}
