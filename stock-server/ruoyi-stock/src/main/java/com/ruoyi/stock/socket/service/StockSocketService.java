package com.ruoyi.stock.socket.service;

import com.ruoyi.stock.domain.StockClient;
import com.ruoyi.stock.service.IStockClientService;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.collections4.CollectionUtils;
import org.apache.commons.lang3.StringUtils;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;
import java.util.List;

@Service
@Slf4j
public class StockSocketService {
    @Resource
    private IStockClientService stockClientService;
    /**
     * 客户端登录
     * @param clientId 客户端
     * @param token token
     * @return true 登录成功，false 登录失败
     */
    public boolean auth(Long clientId, String token){
        if(clientId == null || StringUtils.isBlank(token)){
            return false;
        }
        try {
            StockClient c = new StockClient();
            c.setClientToken(token);
            c.setId(clientId);
            List<StockClient> clientList = stockClientService.selectStockClientList(c);
            return CollectionUtils.isNotEmpty(clientList);
        } catch (NumberFormatException e) {
            log.warn("ClientId:{},不能格式化为数字！", clientId);
           return false;
        }
    }
}
