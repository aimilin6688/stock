package com.ruoyi.stock.mapper;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.util.ArrayList;
import java.util.List;

import static org.springframework.boot.test.context.SpringBootTest.WebEnvironment.RANDOM_PORT;

@SpringBootTest(webEnvironment=RANDOM_PORT)
public class StockTradeDateMapperTest {
    @Autowired
    private StockTradeDateMapper stockTradeDateMapper;

    @Test
    public void test01(){
        List< String> dates = new ArrayList<>();
        dates.add("2020-11-12");
        System.out.println(stockTradeDateMapper.selectBatchIds(dates));
        System.out.println(stockTradeDateMapper.queryBefore("2020-11-12", 2));
        System.out.println(stockTradeDateMapper.queryAfter("2020-11-12", 20));
        System.out.println(stockTradeDateMapper.getTradeDate("2020-11-12", 20));
    }
}
