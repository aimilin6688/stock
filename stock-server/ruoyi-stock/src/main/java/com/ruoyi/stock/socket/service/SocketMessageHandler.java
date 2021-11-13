package com.ruoyi.stock.socket.service;

import cn.hutool.core.collection.CollectionUtil;
import cn.hutool.core.date.DateUtil;
import com.alibaba.fastjson.JSONObject;
import com.ruoyi.common.utils.DateUtils;
import com.ruoyi.stock.domain.*;
import com.ruoyi.stock.domain.vo.BaseMessageSendVo;
import com.ruoyi.stock.enums.*;
import com.ruoyi.stock.service.*;
import com.ruoyi.stock.socket.StockWebSocketMonitor;
import com.ruoyi.stock.socket.StockWebSocketServer;
import com.ruoyi.stock.socket.bean.ClientSupportBrokers;
import com.ruoyi.stock.socket.bean.EntrustUserResult;
import com.ruoyi.stock.socket.bean.Message;
import com.ruoyi.stock.socket.bean.SocketResult;
import com.ruoyi.stock.utils.StockCodeUtils;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.collections4.CollectionUtils;
import org.apache.commons.lang3.StringUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;

import java.util.Arrays;
import java.util.Date;
import java.util.List;
import java.util.Objects;

@Component
@Slf4j
public class SocketMessageHandler {
    @Autowired
    private IStockMessageService stockMessageService;
    @Autowired
    private IStockAccountService stockAccountService;
    @Autowired
    private IStockEntrustService stockEntrustService;
    @Autowired
    private IStockPositionService stockPositionService;
    @Autowired
    private IStockMoneyService stockMoneyService;
    @Autowired
    private IStockDealService stockDealService;
    @Autowired
    private IStockClientBrokersService stockClientBrokersService;
    @Autowired
    private IStockEntrustUserService stockEntrustUserService;

    @Transactional(rollbackFor = Exception.class)
    public void handler(String message) {
        SocketResult socketResult = JSONObject.parseObject(message, SocketResult.class);
        if (!socketResult.isSuccess()) {
            log.warn("接受消息状态错误：{}", message);
            String errorMsg = socketResult.getMsg() + (socketResult.getData() instanceof String ? socketResult.getData():"");
            StockWebSocketMonitor.fail(errorMsg);
            return;
        }
        // 默认发送消息类型
        Message msg = socketResult.dataToType(Message.class);
        try {
            SocketMessageClientTypeEnums msgType = SocketMessageClientTypeEnums.parse(msg.getType());
            // 签收类型消息
            switch (msgType) {
                case SIGN:
                    this.signMessage(msg);
                    break;
                case R_LOGIN:
                case R_LOGOUT:
                case R_CANCEL:
                case R_CLEAR:
                case R_ACCOUNT_INFO:
                    // 通知类型，直接发送结果通知即可
                    this.updateExecuted(msg);
                    break;
                case R_MONEY:
                    this.saveMoney(msg);
                    break;
                case R_BUY:
                case R_SELL:
                    this.saveBuyOrSell(msg);
                    break;
                case R_POSITION:
                    this.savePosition(msg);
                    break;
                case R_DEAL:
                    this.saveDeal(msg);
                    break;
                case R_ENTRUST:
                    this.saveEntrust(msg);
                    break;
                case H_SUPPORT_BROKER:
                    this.supperBroker(msg);
                    break;
                case I_ACCOUNT_INFO:
                    this.accountInfo(msg.getAccountId());
                    break;
            }
            sendSign(msg);
        } catch (Exception e) {
            sendError(msg, e);
            throw e;
        }
    }

    /**
     * 发送账户信息，客户端需要时发送该请求。账户更新时也发送该请求
     * @param accountId 账户Id
     */
    public void accountInfo(Long accountId) {
        BaseMessageSendVo sendVo = new BaseMessageSendVo();
        sendVo.setAccountIds(Arrays.asList(accountId));
        sendVo.setType(SocketMessageServerTypeEnums.ACCOUNT_INFO.getCode());
        stockMessageService.sendBase(sendVo);
    }

    // 发送异常消息
    private void sendError(Message msg, Exception e) {
        StockMessage message  = StockMessage.parse(msg);
        message.setType(SocketMessageServerTypeEnums.ERROR.getCode());
        message.setSubject("异常："+e.getMessage());
        StockWebSocketServer.sendMessage(message);
    }

    // 发送签收类型消息
    private void sendSign(Message msg) {
        SocketMessageClientTypeEnums msgType = SocketMessageClientTypeEnums.parse(msg.getType());
        // 接收到的消息返回签收消息
        if (SocketMessageClientTypeEnums.SIGN.equals(msgType)) {
            log.debug("签收类型消息不需要处理：msgId:{}", msg.getMsgId());
            return;
        }
        StockWebSocketServer.sendMessage(StockMessage.sign(msg));
    }

    // 客户端上报支持的券商
    private void supperBroker(Message msg) {
        // {"clientId":1, brokerNames:['中信建投','银河证券']}
        // 删除当前支持的，添加新支持的
        int result = stockClientBrokersService.deleteByClientId(msg.getClientId());
        log.debug("删除客户端（{}）支持的券商条数：{}", msg.getClientId(), result);
        ClientSupportBrokers clientSupportBrokers = JSONObject.parseObject(JSONObject.toJSONString(msg.getData()), ClientSupportBrokers.class);
        List<String> brokerNames = clientSupportBrokers.getBrokerNames();
        stockClientBrokersService.insert(msg.getClientId(), brokerNames);
        log.debug("客户端：{}，支持的券商：{}", msg.getClientId(), brokerNames);
    }

    // 保存委托
    private void saveEntrust(Message msg) {
        int result = 0;
        List<StockEntrust> positionList = JSONObject.parseArray(JSONObject.toJSONString(msg.getData()), StockEntrust.class);
        if(CollectionUtils.isEmpty(positionList)){
            log.debug("账户：{}，没有需要保存的委托数据！",  msg.getAccountId());
            msg.setSubject(msg.getSubject()+"--暂无数据！");
            this.updateExecuted(msg);
            return;
        }
        int dResult = stockEntrustService.deleteByAccountIdAndDate(msg.getAccountId(), DateUtil.parse(msg.getTime()));
        log.debug("账户：{}，删除委托{}条数据！日期：{}", msg.getAccountId(), dResult, msg.getTime());
        for (StockEntrust p : positionList) {
            p.setAccountId(msg.getAccountId());
            p.setDate(msg.getDate());
            p.setStockCode(StockCodeUtils.formatCode(p.getStockCode()));
            p.setCreateTime(new Date());
            result += stockEntrustService.insertStockEntrust(p);
        }
        log.info("账户：{}，保存委托条数：{}", msg.getAccountId(), result);
        this.updateExecuted(msg);
    }

    // 保存成交
    private void saveDeal(Message msg) {
        int result = 0;
        List<StockDeal> positionList = JSONObject.parseArray(JSONObject.toJSONString(msg.getData()), StockDeal.class);
        if(CollectionUtils.isEmpty(positionList)){
            log.debug("账户：{}，没有需要保存的成交数据！",  msg.getAccountId());
            msg.setSubject(msg.getSubject()+"--暂无数据！");
            this.updateExecuted(msg);
            return;
        }
        int dResult = stockDealService.deleteByAccountIdAndDate(msg.getAccountId(), DateUtil.parse(msg.getTime()));
        log.debug("账户：{}，删除成交{}条数据！日期：{}", msg.getAccountId(), dResult, msg.getTime());
        for (StockDeal p : positionList) {
            p.setAccountId(msg.getAccountId());
            p.setDate(msg.getDate());
            p.setStockCode(StockCodeUtils.formatCode(p.getStockCode()));
            p.setCreateTime(new Date());
            result += stockDealService.insertStockDeal(p);
        }
        log.info("账户：{}，保存成交条数：{}", msg.getAccountId(), result);
        this.updateExecuted(msg);
    }

    // 保存仓位
    private void savePosition(Message msg) {
        int result = 0;
        List<StockPosition> positionList = JSONObject.parseArray(JSONObject.toJSONString(msg.getData()), StockPosition.class);
        if(CollectionUtils.isEmpty(positionList)){
            log.debug("账户：{}，没有需要保存的持仓数据！",  msg.getAccountId());
            msg.setSubject(msg.getSubject()+"--暂无数据！");
            this.updateExecuted(msg);
            return;
        }
        int dResult = stockPositionService.deleteByAccountIdAndDate(msg.getAccountId(), DateUtil.parse(msg.getTime()));
        log.debug("账户：{}，删除持仓{}条数据！日期：{}", msg.getAccountId(), dResult, msg.getTime());
        for (StockPosition p : positionList) {
            p.setAccountId(msg.getAccountId());
            p.setDate(msg.getDate());
            p.setStockCode(StockCodeUtils.formatCode(p.getStockCode()));
            p.setCreateTime(new Date());
            result += stockPositionService.insertStockPosition(p);
        }
        log.info("账户：{}，保存持仓条数：{}", msg.getAccountId(), result);
        this.updateExecuted(msg);
    }

    // 保存买入和卖出结果
    private void saveBuyOrSell(Message msg) {
        // 这里需要更新委托结果信息
        StockEntrustUser update  = new StockEntrustUser();
        // {"data":"1881356729","stock_info":{"number":100,"code":"600365","price":2.36,"name":"","operation":1},"state":"OK"}
        EntrustUserResult result = JSONObject.parseObject(msg.getData().toString(), EntrustUserResult.class);
        if(StringUtils.equalsIgnoreCase(result.getState(), EntrustUserResult.OK)){
            update.setStatus(EntrustUserStatusEnums.ENTRUST_ED.getCode());
            update.setEntrustNo(result.getDate());
            update.setEntrustTime(DateUtil.parse(msg.getTime()));
        }else{
            update.setStatus(EntrustUserStatusEnums.ENTRUST_ERROR.getCode());
            update.setEntrustError(result.getDate());
            update.setEntrustTime(DateUtil.parse(msg.getTime()));
        }
        update.setMessageId(msg.getMsgId());
        update.setAccountId(msg.getAccountId());
        int updateResult = stockEntrustUserService.updateEntrustResult(update);
        log.debug("账户:{},消息：{}，更新买入卖出结果：{}",msg.getAccountId(), msg.getMsgId(), updateResult);
        this.updateExecuted(msg);
    }

    // 保存资金信息
    private void saveMoney(Message msg) {
        StockMoney money = JSONObject.parseObject(JSONObject.toJSONString(msg.getData()), StockMoney.class);
        if (money != null) {
            int dResult = stockMoneyService.deleteByAccountIdAndDate(msg.getAccountId(), DateUtil.parse(msg.getTime()));
            log.debug("账户：{}，删除资金信息{}条数据！日期：{}", msg.getAccountId(), dResult, msg.getTime());
        }
        Objects.requireNonNull(money);
        money.setAccountId(msg.getAccountId());
        money.setDate(new Date());
        int result = stockMoneyService.insertStockMoney(money);
        log.info("账户：{}，保存资金信息条数：{}", msg.getAccountId(), result);
        this.updateExecuted(msg);
    }

    // 通知类型结果
    private void updateExecuted(Message msg) {
        StockMessage sign = new StockMessage();
        sign.setId(msg.getMsgId());
        sign.setExecutedTime(DateUtil.parse(msg.getTime()));
        if(msg.getData() != null && StringUtils.isNotBlank(msg.getData().toString())) {
            sign.setExecutedResult(JSONObject.toJSONString(msg.getData()));
        }else{
            sign.setExecutedResult(msg.getSubject());
        }
        sign.setExecuted(StockMessageExeResultEnums.EXECUTED.getCode());
        sign.setExecutedStatus(msg.getStatus());
        stockMessageService.updateStockMessage(sign);
        if(msg.getStatus() != null && msg.getStatus()) {
            StockWebSocketMonitor.success(msg.getSubject());
        }else{
            StockWebSocketMonitor.fail(msg.getSubject());
        }
    }

    // 签收消息
    private void signMessage(Message msg) {
        if (msg.getMsgId() == null) {
            log.error("消息Id为空，不能签收！{}", msg);
            return;
        }
        StockMessage sign = new StockMessage();
        sign.setId(msg.getMsgId());
        sign.setSignClientId(msg.getClientId());
        sign.setSignTime(DateUtil.parse(msg.getTime()));
        sign.setStatus(StockMessageSendStatusEnums.SING_EN.getCode());
        stockMessageService.updateStockMessage(sign);
    }
}
