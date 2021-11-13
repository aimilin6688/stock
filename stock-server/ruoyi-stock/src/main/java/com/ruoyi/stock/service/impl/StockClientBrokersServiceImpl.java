package com.ruoyi.stock.service.impl;

import java.util.List;

import com.ruoyi.stock.excetion.UnSupportBrokerException;
import com.ruoyi.stock.mapper.StockBrokerMapper;
import com.ruoyi.stock.mapper.StockClientBrokersMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.stock.domain.StockClientBrokers;
import com.ruoyi.stock.service.IStockClientBrokersService;
import org.springframework.transaction.annotation.Transactional;

/**
 * 券商与客户端关联Service业务层处理
 * 
 * @author jonk
 * @date 2021-01-07
 */
@Service
public class StockClientBrokersServiceImpl implements IStockClientBrokersService 
{
    @Autowired
    private StockClientBrokersMapper stockClientBrokersMapper;
    @Autowired
    private StockBrokerMapper stockBrokerMapper;

    /**
     * 查询券商与客户端关联
     * 
     * @param clientsId 券商与客户端关联ID
     * @return 券商与客户端关联
     */
    @Override
    public StockClientBrokers selectStockClientBrokersById(Long clientsId)
    {
        return stockClientBrokersMapper.selectStockClientBrokersById(clientsId);
    }

    /**
     * 查询券商与客户端关联列表
     * 
     * @param stockClientBrokers 券商与客户端关联
     * @return 券商与客户端关联
     */
    @Override
    public List<StockClientBrokers> selectStockClientBrokersList(StockClientBrokers stockClientBrokers)
    {
        return stockClientBrokersMapper.selectStockClientBrokersList(stockClientBrokers);
    }

    /**
     * 新增券商与客户端关联
     * 
     * @param stockClientBrokers 券商与客户端关联
     * @return 结果
     */
    @Override
    public int insertStockClientBrokers(StockClientBrokers stockClientBrokers)
    {
        return stockClientBrokersMapper.insertStockClientBrokers(stockClientBrokers);
    }

    /**
     * 修改券商与客户端关联
     * 
     * @param stockClientBrokers 券商与客户端关联
     * @return 结果
     */
    @Override
    public int updateStockClientBrokers(StockClientBrokers stockClientBrokers)
    {
        return stockClientBrokersMapper.updateStockClientBrokers(stockClientBrokers);
    }

    /**
     * 批量删除券商与客户端关联
     * 
     * @param clientsIds 需要删除的券商与客户端关联ID
     * @return 结果
     */
    @Override
    public int deleteStockClientBrokersByIds(Long[] clientsIds)
    {
        return stockClientBrokersMapper.deleteStockClientBrokersByIds(clientsIds);
    }

    /**
     * 删除券商与客户端关联信息
     * 
     * @param clientsId 券商与客户端关联ID
     * @return 结果
     */
    @Override
    public int deleteStockClientBrokersById(Long clientsId)
    {
        return stockClientBrokersMapper.deleteStockClientBrokersById(clientsId);
    }

    @Override
    public int deleteByClientId(Long clientId) {
        return stockClientBrokersMapper.deleteByClientId(clientId);
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public int insert(Long clientId, List<String> brokerNames) {
        int result = 0;
        // 根据券商名字查询券商ID
        for (String name : brokerNames){
            Long brokerId = stockBrokerMapper.selectIdByName(name);
            if(brokerId == null){
                throw new UnSupportBrokerException("不支持的券商："+name);
            }else{
                StockClientBrokers cb = new StockClientBrokers();
                cb.setClientsId(clientId);
                cb.setBrokersId(brokerId);
                result += this.insertStockClientBrokers(cb);
            }
        }
        return result;
    }
}
