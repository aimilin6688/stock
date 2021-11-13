package com.ruoyi.stock.domain.vo;

import lombok.Builder;
import lombok.Data;

@Data
public class SimpleAccountVo {
    private Long id;
    private String nickname;
    private String reportName;
    private String brokerName;
    private String clientName;
    private Long clientId;
    private Long brokerId;
    public String getName(){
        return String.format("%s (%s - %s)", nickname, brokerName, clientName);
    }
}
