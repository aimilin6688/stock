package com.ruoyi.stock.mapper;

import java.util.List;
import com.ruoyi.stock.domain.StockClientBrokers;
import org.apache.ibatis.annotations.Param;
import org.apache.ibatis.annotations.Update;

/**
 * 券商与客户端关联Mapper接口
 * 
 * @author jonk
 * @date 2021-01-07
 */
public interface StockClientBrokersMapper 
{
    /**
     * 查询券商与客户端关联
     * 
     * @param clientsId 券商与客户端关联ID
     * @return 券商与客户端关联
     */
    public StockClientBrokers selectStockClientBrokersById(Long clientsId);

    /**
     * 查询券商与客户端关联列表
     * 
     * @param stockClientBrokers 券商与客户端关联
     * @return 券商与客户端关联集合
     */
    public List<StockClientBrokers> selectStockClientBrokersList(StockClientBrokers stockClientBrokers);

    /**
     * 新增券商与客户端关联
     * 
     * @param stockClientBrokers 券商与客户端关联
     * @return 结果
     */
    public int insertStockClientBrokers(StockClientBrokers stockClientBrokers);

    /**
     * 修改券商与客户端关联
     * 
     * @param stockClientBrokers 券商与客户端关联
     * @return 结果
     */
    public int updateStockClientBrokers(StockClientBrokers stockClientBrokers);

    /**
     * 删除券商与客户端关联
     * 
     * @param clientsId 券商与客户端关联ID
     * @return 结果
     */
    public int deleteStockClientBrokersById(Long clientsId);

    /**
     * 批量删除券商与客户端关联
     * 
     * @param clientsIds 需要删除的数据ID
     * @return 结果
     */
    public int deleteStockClientBrokersByIds(Long[] clientsIds);

    @Update("delete from stock_client_brokers where clients_id = #{clientId}")
    public int deleteByClientId(@Param("clientId") Long clientId);
}
