package com.ruoyi.stock.service.impl;

import com.ruoyi.common.utils.DateUtils;
import com.ruoyi.stock.mapper.StockAccountInitMapper;
import com.ruoyi.stock.mapper.StockMoneyMapper;
import com.ruoyi.stock.service.IStockAccountService;
import org.apache.commons.lang3.StringUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;

@Service
public class AccountService {
    @Autowired
    private StockMoneyMapper stockMoneyMapper;
    @Autowired
    private StockAccountInitMapper stockAccountInitMapper;
    @Autowired
    private IStockAccountService iStockAccountService;

    /**
     * 查询账户名称
     * @param accountId 账户Id
     * @return
     */
    public String queryName(Long accountId){
        return iStockAccountService.selectNameById(accountId);
    }


    /**
     * 查询账户资金信息
     * @param accountId 账户Id
     * @param date 日期，可以为空，为空则查询当前交易日资金信息， yyyy-MM-dd
     * @return 资金
     */
    public BigDecimal queryMoney(Long accountId, String date){
        if(StringUtils.isBlank(date)){
            date = DateUtils.getDate();
        }
        // 1. 查询账户总资产
        BigDecimal total = stockMoneyMapper.queryTotal(accountId, date);
        if(total == null){
            // 2. 查询账户初始资金
            total = stockAccountInitMapper.queryInitMoney(accountId);
        }
        return total;
    }
}
