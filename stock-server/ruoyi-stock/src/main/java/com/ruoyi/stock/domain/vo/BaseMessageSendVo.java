package com.ruoyi.stock.domain.vo;

import com.ruoyi.stock.domain.StockAccount;
import com.ruoyi.stock.socket.bean.BuyOrSell;
import lombok.Data;

import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;
import java.io.Serializable;
import java.math.BigDecimal;
import java.util.List;
import java.util.Map;

/**
 * 基础消息发送类
 */
@Data
public class BaseMessageSendVo implements Serializable {
    @Size(min = 1, message = "请选择接受消息账户")
    private List<Long> accountIds;
    @NotNull(message = "请选择消息类型")
    private Integer type ;
    private List<BuyOrSell> buyOrSellList;
    private EntrustCancel entrustCancel;

    // 这个属性是后端填充用户使用的
    private Map<Long,StockAccount> accountMap;

    @Data
    public static class EntrustCancel{
        // 0:撤指定，1：撤全部，2：撤销买入，3：撤销卖出
        private Integer type;
        private String stockCodes;
        private String entrustNos;
    }
}
