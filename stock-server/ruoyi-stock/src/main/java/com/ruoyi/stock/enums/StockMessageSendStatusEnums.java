package com.ruoyi.stock.enums;

import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor
public enum StockMessageSendStatusEnums {
    UN_SEND(0,"未发送"),
    SEND_ED(1, "已发送"),
    SING_EN(2, "已签收"),
    DISCARD(3, "已丢弃");
    private int code;
    private String message;
}
