package com.ruoyi.stock.enums;

import lombok.AllArgsConstructor;
import lombok.Getter;
@Getter
@AllArgsConstructor
public enum StockMessageExeResultEnums {
    UN_EXE(0,"未执行"),
    EXECUTED(1, "已执行");
    private int code;
    private String message;
}
