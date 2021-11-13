package com.ruoyi.stock.socket.bean;

import lombok.Data;

import java.math.BigDecimal;

@Data
public class BuyOrSell {
    private String code;
    private String name;
    private Integer operation;
    private BigDecimal price;
    private Integer number;
    private BigDecimal position;
}