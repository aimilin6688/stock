package com.ruoyi.stock.socket.bean;

import lombok.Data;

import java.util.List;

@Data
public class ClientSupportBrokers {
    private Long clientId;
    private List<String> brokerNames;
}
