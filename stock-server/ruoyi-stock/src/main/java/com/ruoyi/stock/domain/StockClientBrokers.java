package com.ruoyi.stock.domain;

import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;
import com.ruoyi.common.annotation.Excel;
import com.ruoyi.common.core.domain.BaseEntity;

import java.io.Serializable;

/**
 * 券商与客户端关联对象 stock_client_brokers
 * 
 * @author jonk
 * @date 2021-01-07
 */
public class StockClientBrokers implements Serializable
{
    private static final long serialVersionUID = 1L;

    /** 客户端ID */
    private Long clientsId;

    /** 券商Id */
    private Long brokersId;

    public void setClientsId(Long clientsId)
    {
        this.clientsId = clientsId;
    }

    public Long getClientsId() 
    {
        return clientsId;
    }
    public void setBrokersId(Long brokersId) 
    {
        this.brokersId = brokersId;
    }

    public Long getBrokersId() 
    {
        return brokersId;
    }

    @Override
    public String toString() {
        return new ToStringBuilder(this,ToStringStyle.MULTI_LINE_STYLE)
            .append("clientsId", getClientsId())
            .append("brokersId", getBrokersId())
            .toString();
    }
}
