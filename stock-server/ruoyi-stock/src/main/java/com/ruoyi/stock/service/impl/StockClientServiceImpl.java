package com.ruoyi.stock.service.impl;

import java.util.Date;
import java.util.List;

import com.ruoyi.stock.service.IStockClientService;
import com.ruoyi.stock.enums.OnLineStatusEnums;
import com.ruoyi.stock.socket.StockWebSocketMonitor;
import com.ruoyi.stock.socket.bean.SocketResult;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.stock.mapper.StockClientMapper;
import com.ruoyi.stock.domain.StockClient;

/**
 * 下单客户端Service业务层处理
 * 
 * @author jonk
 * @date 2021-01-06
 */
@Service
public class StockClientServiceImpl implements IStockClientService
{
    @Autowired
    private StockClientMapper stockClientMapper;

    /**
     * 查询下单客户端
     * 
     * @param id 下单客户端ID
     * @return 下单客户端
     */
    @Override
    public StockClient selectStockClientById(Long id)
    {
        return stockClientMapper.selectStockClientById(id);
    }

    @Override
    public String selectNameById(Long id) {
        return stockClientMapper.selectNameById(id);
    }

    /**
     * 通过brokerId查询
     * @param brokerId
     * @return
     */
    @Override
    public List<StockClient> selectStockClientListByBrokerId(Long brokerId){
        return stockClientMapper.selectStockClientListByBrokerId(brokerId);
    }

    /**
     * 查询下单客户端列表
     * 
     * @param stockClient 下单客户端
     * @return 下单客户端
     */
    @Override
    public List<StockClient> selectStockClientList(StockClient stockClient)
    {
        return stockClientMapper.selectStockClientList(stockClient);
    }

    /**
     * 新增下单客户端
     * 
     * @param stockClient 下单客户端
     * @return 结果
     */
    @Override
    public int insertStockClient(StockClient stockClient)
    {
        return stockClientMapper.insertStockClient(stockClient);
    }

    /**
     * 修改下单客户端
     * 
     * @param stockClient 下单客户端
     * @return 结果
     */
    @Override
    public int updateStockClient(StockClient stockClient)
    {
        return stockClientMapper.updateStockClient(stockClient);
    }

    @Override
    public int updateOnLineStatus(Long clientId, OnLineStatusEnums onLineStatusEnums){
        StockClient stockClient = new StockClient();
        stockClient.setId(clientId);
        stockClient.setOnLine(onLineStatusEnums.ordinal());
        stockClient.setLastConnectTime(new Date());
        return this.updateStockClient(stockClient);
    }

    /**
     * 批量删除下单客户端
     * 
     * @param ids 需要删除的下单客户端ID
     * @return 结果
     */
    @Override
    public int deleteStockClientByIds(String[] ids)
    {
        return stockClientMapper.deleteStockClientByIds(ids);
    }

    /**
     * 删除下单客户端信息
     * 
     * @param id 下单客户端ID
     * @return 结果
     */
    @Override
    public int deleteStockClientById(String id)
    {
        return stockClientMapper.deleteStockClientById(id);
    }

    @Override
    public void onLine(Long clientId) {
        this.updateOnLineStatus(clientId, OnLineStatusEnums.ON_LINE);
        StockWebSocketMonitor.sendMessage(SocketResult.success(String.format("客户端：%s, 上线了!", this.selectNameById(clientId))));
    }

    @Override
    public void offLine(Long clientId) {
        this.updateOnLineStatus(clientId, OnLineStatusEnums.OFF_LINE);
        StockWebSocketMonitor.sendMessage(SocketResult.success(String.format("客户端：%s, 下线了!", this.selectNameById(clientId))));
    }
}
