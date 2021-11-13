package com.ruoyi.stock.service;

import com.ruoyi.stock.domain.vo.SimpleAccountVo;

public interface IAccountFiller {

    /**
     * 获取账户Id
     * @return
     */
    Long getAccountId();

    /**
     * 设置账户信息
     * @param account
     */
    void setAccount(SimpleAccountVo account);
}
