package com.ruoyi.stock.mapper;

import java.util.List;
import com.ruoyi.stock.domain.StockClient;

/**
 * 下单客户端Mapper接口
 * 
 * @author jonk
 * @date 2021-01-06
 */
public interface StockClientMapper 
{
    /**
     * 查询下单客户端
     * 
     * @param id 下单客户端ID
     * @return 下单客户端
     */
    public StockClient selectStockClientById(Long id);

    /**
     * 通过brokerId查询
     * @param brokerId
     * @return
     */
    public List<StockClient> selectStockClientListByBrokerId(Long brokerId);

    public String selectNameById(Long id);

    /**
     * 查询下单客户端列表
     * 
     * @param stockClient 下单客户端
     * @return 下单客户端集合
     */
    public List<StockClient> selectStockClientList(StockClient stockClient);

    /**
     * 新增下单客户端
     * 
     * @param stockClient 下单客户端
     * @return 结果
     */
    public int insertStockClient(StockClient stockClient);

    /**
     * 修改下单客户端
     * 
     * @param stockClient 下单客户端
     * @return 结果
     */
    public int updateStockClient(StockClient stockClient);

    /**
     * 删除下单客户端
     * 
     * @param id 下单客户端ID
     * @return 结果
     */
    public int deleteStockClientById(String id);

    /**
     * 批量删除下单客户端
     * 
     * @param ids 需要删除的数据ID
     * @return 结果
     */
    public int deleteStockClientByIds(String[] ids);
}
