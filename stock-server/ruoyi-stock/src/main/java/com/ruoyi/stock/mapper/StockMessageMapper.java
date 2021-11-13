package com.ruoyi.stock.mapper;

import java.util.List;

import com.ruoyi.stock.domain.StockMessage;

/**
 * 消息Mapper接口
 * 
 * @author jonk
 * @date 2021-01-08
 */
public interface StockMessageMapper 
{
    /**
     * 查询消息
     * 
     * @param id 消息ID
     * @return 消息
     */
    public StockMessage selectStockMessageById(Long id);

    /**
     * 查询消息列表
     * 
     * @param stockMessage 消息
     * @return 消息集合
     */
    public List<StockMessage> selectStockMessageList(StockMessage stockMessage);

    /**
     * 新增消息
     * 
     * @param stockMessage 消息
     * @return 结果
     */
    public int insertStockMessage(StockMessage stockMessage);

    /**
     * 修改消息
     * 
     * @param stockMessage 消息
     * @return 结果
     */
    public int updateStockMessage(StockMessage stockMessage);

    /**
     * 删除消息
     * 
     * @param id 消息ID
     * @return 结果
     */
    public int deleteStockMessageById(Long id);

    /**
     * 批量删除消息
     * 
     * @param ids 需要删除的数据ID
     * @return 结果
     */
    public int deleteStockMessageByIds(Long[] ids);
}
