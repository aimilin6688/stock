package com.ruoyi.stock.service.impl;

import java.util.Date;
import java.util.List;
import com.ruoyi.common.utils.DateUtils;
import com.ruoyi.stock.domain.vo.SimpleAccountVo;
import com.ruoyi.stock.enums.StatusEnums;
import com.ruoyi.stock.socket.service.SocketMessageHandler;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.stock.mapper.StockAccountMapper;
import com.ruoyi.stock.domain.StockAccount;
import com.ruoyi.stock.service.IStockAccountService;

/**
 * 下单账户Service业务层处理
 * 
 * @author jonk
 * @date 2021-01-06
 */
@Service
public class StockAccountServiceImpl implements IStockAccountService 
{
    @Autowired
    private StockAccountMapper stockAccountMapper;
    @Autowired
    private SocketMessageHandler socketMessageHandler;


    /**
     * 查询下单账户
     * 
     * @param id 下单账户ID
     * @return 下单账户
     */
    @Override
    public StockAccount selectStockAccountById(Long id)
    {
        return stockAccountMapper.selectStockAccountById(id);
    }

    /**
     * 查询下单账户列表
     * 
     * @param stockAccount 下单账户
     * @return 下单账户
     */
    @Override
    public List<StockAccount> selectStockAccountList(StockAccount stockAccount)
    {
        return stockAccountMapper.selectStockAccountList(stockAccount);
    }

    @Override
    public List<StockAccount> selectListByIds(List<Long> ids) {
        StockAccount query = new StockAccount();
        query.getParams().put("accountIds", ids);
        query.setStatus(StatusEnums.ON.ordinal());
        return this.selectStockAccountList(query);
    }

    /**
     * 简单信息列表
     * @param stockAccount 下单账户
     * @return
     */
    @Override
    public List<SimpleAccountVo> selectSimpleVoList(StockAccount stockAccount) {
        return stockAccountMapper.selectSimpleVoList(stockAccount);
    }

    @Override
    public SimpleAccountVo selectSimpleVoById(Long id) {
        StockAccount query = new StockAccount();
        query.setId(id);
        return this.selectSimpleVoList(query).get(0);
    }

    @Override
    public String selectNameById(Long id) {
        return this.selectSimpleVoById(id).getName();
    }

    /**
     * 新增下单账户
     * 
     * @param stockAccount 下单账户
     * @return 结果
     */
    @Override
    public int insertStockAccount(StockAccount stockAccount)
    {
        stockAccount.setCreateTime(new Date());
        return stockAccountMapper.insertStockAccount(stockAccount);
    }

    /**
     * 修改下单账户
     * 
     * @param stockAccount 下单账户
     * @return 结果
     */
    @Override
    public int updateStockAccount(StockAccount stockAccount)
    {
        stockAccount.setUpdateTime(new Date());
        int result =  stockAccountMapper.updateStockAccount(stockAccount);
        if(result > 0){
            // 通知客户端账户更新
            socketMessageHandler.accountInfo(stockAccount.getId());
        }
        return result;
    }

    /**
     * 批量删除下单账户
     * 
     * @param ids 需要删除的下单账户ID
     * @return 结果
     */
    @Override
    public int deleteStockAccountByIds(Long[] ids)
    {
        return stockAccountMapper.deleteStockAccountByIds(ids);
    }

    /**
     * 删除下单账户信息
     * 
     * @param id 下单账户ID
     * @return 结果
     */
    @Override
    public int deleteStockAccountById(Long id)
    {
        return stockAccountMapper.deleteStockAccountById(id);
    }
}
