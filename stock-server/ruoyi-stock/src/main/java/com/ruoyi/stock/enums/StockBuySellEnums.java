package com.ruoyi.stock.enums;

import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor
public enum StockBuySellEnums {
    SELL(0,"卖出"),
    BUY(1, "买入"),
    UNKNOWN(-1, "未知");
    private int code;
    private String message;
}
