package com.ruoyi.stock.service.impl;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.math.BigDecimal;

import static org.springframework.boot.test.context.SpringBootTest.WebEnvironment.RANDOM_PORT;


@SpringBootTest(webEnvironment=RANDOM_PORT)
public class StockAccountServiceTest {
    @Autowired
    private AccountService stockAccountService;

    @Test
    public void queryMoney() {
        BigDecimal total = stockAccountService.queryMoney(1L, null);
        System.out.println(total);
    }
}