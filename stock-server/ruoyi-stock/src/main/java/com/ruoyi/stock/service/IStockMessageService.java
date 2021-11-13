package com.ruoyi.stock.service;

import java.util.List;

import com.ruoyi.stock.domain.StockMessage;
import com.ruoyi.stock.domain.vo.BaseMessageSendVo;

/**
 * 消息Service接口
 * 
 * @author jonk
 * @date 2021-01-08
 */
public interface IStockMessageService 
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
     * 批量删除消息
     * 
     * @param ids 需要删除的消息ID
     * @return 结果
     */
    public int deleteStockMessageByIds(Long[] ids);

    /**
     * 删除消息信息
     * 
     * @param id 消息ID
     * @return 结果
     */
    public int deleteStockMessageById(Long id);

    /**
     * 发送基础消息
     * @param messageSendVo 消息内容
     * @return 发送结果描述
     */
    String sendBase(BaseMessageSendVo messageSendVo);

    /**
     * 更新消息状态为已发送
     * @param id
     * @return
     */
    int updateStatusSend(Long id);
}
