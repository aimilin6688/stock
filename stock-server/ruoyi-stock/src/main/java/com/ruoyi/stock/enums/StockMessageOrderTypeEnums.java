package com.ruoyi.stock.enums;

import com.ruoyi.stock.excetion.UnknownMessageBaseTypeException;
import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor
public enum StockMessageOrderTypeEnums {
    CREDITOR(0, "债券"),
    ORDER(1, "下单"),
    REPORT(2, "报告");
    private int code;
    private String message;

    public static StockMessageOrderTypeEnums parse(int code){
        for (StockMessageOrderTypeEnums type : StockMessageOrderTypeEnums.values()) {
            if(type.code == code){
                return type;
            }
        }
        throw new UnknownMessageBaseTypeException("未知的消息类型："+code);
    }
}
