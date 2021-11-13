package com.ruoyi.stock.service.impl;

import com.ruoyi.stock.domain.StockAccount;
import com.ruoyi.stock.domain.vo.SimpleAccountVo;
import com.ruoyi.stock.mapper.StockAccountMapper;
import com.ruoyi.stock.service.IAccountFiller;
import org.apache.commons.collections4.CollectionUtils;
import org.apache.commons.collections4.MapUtils;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;
import java.util.Arrays;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Service
public class AccountFillerService {
    @Resource
    private StockAccountMapper stockAccountMapper;


    /**
     * 填充账号信息
     * @param account
     * @param <T>
     * @return
     */
    public <T extends IAccountFiller>  T fill(T account){
        if(account == null){
            return account;
        }
        return this.fill(Arrays.asList(account)).get(0);
    }

    /**
     * 填充账号信息
     * @param accounts
     * @param <T>
     * @return
     */
    public <T extends IAccountFiller>  List<T> fill(List<T> accounts){
        if(CollectionUtils.isEmpty(accounts)){
            return accounts;
        }
        List<Long> accountIds = accounts.stream().map(IAccountFiller::getAccountId).collect(Collectors.toList());
        StockAccount account = new StockAccount();
        account.getParams().put("accountIds", accountIds);
        List<SimpleAccountVo> accountList =  stockAccountMapper.selectSimpleVoList(account);
        Map<Long, SimpleAccountVo> accountMap = accountList.stream().collect(Collectors.toMap(SimpleAccountVo::getId, c->c));
        accounts.forEach(c->{
            Long accountId = c.getAccountId();
            c.setAccount(MapUtils.getObject(accountMap, accountId, new SimpleAccountVo()));
        });
        return accounts;
    }
}
