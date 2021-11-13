package com.ruoyi.stock.socket.bean;

import com.alibaba.fastjson.annotation.JSONField;
import lombok.Data;

// 买入卖出结果信息
@Data
public class EntrustUserResult {
    public static final String OK ="OK";
    public static final String ERROR ="ERROR";
    // {"data":"1881356729","stock_info":{"number":100,"code":"600365","price":2.36,"name":"","operation":1},"state":"OK"}
    private String state;
    private String date;
    @JSONField(name = "stock_info")
    private BuyOrSell stockInfo;
}
