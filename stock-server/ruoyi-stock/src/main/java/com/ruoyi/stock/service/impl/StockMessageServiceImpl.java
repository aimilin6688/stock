package com.ruoyi.stock.service.impl;

import com.ruoyi.stock.domain.StockAccount;
import com.ruoyi.stock.domain.StockEntrustUser;
import com.ruoyi.stock.domain.StockMessage;
import com.ruoyi.stock.domain.vo.BaseMessageSendVo;
import com.ruoyi.stock.enums.*;
import com.ruoyi.stock.mapper.StockMessageMapper;
import com.ruoyi.stock.service.IStockAccountService;
import com.ruoyi.stock.service.IStockEntrustUserService;
import com.ruoyi.stock.service.IStockMessageService;
import com.ruoyi.stock.service.IStockMoneyService;
import com.ruoyi.stock.socket.StockWebSocketServer;
import com.ruoyi.stock.socket.bean.BuyOrSell;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.BeanUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.*;
import java.util.stream.Collectors;

/**
 * 消息Service业务层处理
 *
 * @author jonk
 * @date 2021-01-08
 */
@Slf4j
@Service
public class StockMessageServiceImpl implements IStockMessageService {
    @Autowired
    private StockMessageMapper stockMessageMapper;
    @Autowired
    private AccountFillerService accountFillerService;
    @Autowired
    private IStockAccountService stockAccountService;
    @Autowired
    private IStockMoneyService stockMoneyService;
    @Autowired
    private IStockEntrustUserService stockEntrustUserService;

    /**
     * 查询消息
     *
     * @param id 消息ID
     * @return 消息
     */
    @Override
    public StockMessage selectStockMessageById(Long id) {
        return accountFillerService.fill(stockMessageMapper.selectStockMessageById(id));
    }

    /**
     * 查询消息列表
     *
     * @param stockMessage 消息
     * @return 消息
     */
    @Override
    public List<StockMessage> selectStockMessageList(StockMessage stockMessage) {
        return accountFillerService.fill(stockMessageMapper.selectStockMessageList(stockMessage));
    }

    /**
     * 新增消息
     *
     * @param stockMessage 消息
     * @return 结果
     */
    @Override
    public int insertStockMessage(StockMessage stockMessage) {
        stockMessage.setCreateTime(new Date());
        return stockMessageMapper.insertStockMessage(stockMessage);
    }

    /**
     * 修改消息
     *
     * @param stockMessage 消息
     * @return 结果
     */
    @Override
    public int updateStockMessage(StockMessage stockMessage) {
        return stockMessageMapper.updateStockMessage(stockMessage);
    }

    /**
     * 批量删除消息
     *
     * @param ids 需要删除的消息ID
     * @return 结果
     */
    @Override
    public int deleteStockMessageByIds(Long[] ids) {
        return stockMessageMapper.deleteStockMessageByIds(ids);
    }

    /**
     * 删除消息信息
     *
     * @param id 消息ID
     * @return 结果
     */
    @Override
    public int deleteStockMessageById(Long id) {
        return stockMessageMapper.deleteStockMessageById(id);
    }

    /**
     * 发送基础消息
     *
     * @param messageSendVo 消息内容
     * @return
     */
    @Override
    @Transactional(rollbackFor = Exception.class)
    public String sendBase(BaseMessageSendVo messageSendVo) {
        log.debug("发送消息：{}", messageSendVo);
        try {
            //1. 数据库先添加消息发送日志
            SocketMessageServerTypeEnums type = SocketMessageServerTypeEnums.parse(messageSendVo.getType());
            // 过滤掉不符合条件的账户ID
            this.fillAccount(messageSendVo);
            List<StockMessage> stockMessages = null;
            switch (type) {
                case SIGN:
                    return "签收消息不下发！";
                case LOGIN:
                    stockMessages = this.sendLogin(messageSendVo);
                    break;
                case LOGOUT:
                case MONEY:
                case POSITION:
                case DEAL:
                case ENTRUST:
                case CLEAR:
                    stockMessages = this.sendAction(messageSendVo);
                    break;
                case BUY:
                case SELL:
                    stockMessages = this.sendBuyOrSell(messageSendVo);
                    break;
                case CANCEL:
                    stockMessages = this.sendEntrustCancel(messageSendVo);
                    break;
                case ACCOUNT_INFO:
                    stockMessages = this.sendAccountInfo(messageSendVo);
                    break;
            }
            // 将消息实例化到数据库中
            this.batchSave(stockMessages);
            //2. 调用websocket先指定客户端发送消息
            StockWebSocketServer.sendMessage(stockMessages);
            return "操作成功！";
        } catch (Exception e) {
            log.error(e.getMessage(), e);
            return "操作失败，原因：" + e.getMessage();
        }
    }

    // 发送账户信息
    private List<StockMessage> sendAccountInfo(BaseMessageSendVo messageSendVo) {
        List<StockMessage> messages = createMessageList(messageSendVo);
        messages.forEach(c->{
            c.setData(messageSendVo.getAccountMap().get(c.getAccountId()));
        });
        return messages;
    }

    @Override
    public int updateStatusSend(Long id) {
        StockMessage stockMessage = new StockMessage();
        stockMessage.setId(id);
        stockMessage.setUpdateTime(new Date());
        stockMessage.setSendTime(new Date());
        stockMessage.setStatus(StockMessageSendStatusEnums.SEND_ED.getCode());
        return this.updateStockMessage(stockMessage);
    }

    // 批量插入到数据库中
    private void batchSave(List<StockMessage> stockMessages) {
        int result = 0;
        for(StockMessage msg : stockMessages){
            result += this.insertStockMessage(msg);
            this.insertStockEntrustUser(msg);
        }
        log.info("消息添加个数:{}", result);
    }

    // 买入或者卖出需要保存委托信息
    private void insertStockEntrustUser(StockMessage msg) {
        SocketMessageServerTypeEnums typeEnums = SocketMessageServerTypeEnums.parse(msg.getType());
        if((SocketMessageServerTypeEnums.BUY.equals(typeEnums) || SocketMessageServerTypeEnums.SELL.equals(typeEnums))
                && msg.getData() instanceof BuyOrSell){
            BuyOrSell buyOrSell = (BuyOrSell)msg.getData();
            StockEntrustUser entrustUser = new StockEntrustUser();
            entrustUser.setMessageId(msg.getId());
            entrustUser.setAccountId(msg.getAccountId());
            entrustUser.setDate(new Date());
            entrustUser.setStockCode(buyOrSell.getCode());
            entrustUser.setStockName(buyOrSell.getName());
            entrustUser.setNum(Long.valueOf(buyOrSell.getNumber()));
            entrustUser.setPosition(buyOrSell.getPosition());
            entrustUser.setPrice(buyOrSell.getPrice());
            entrustUser.setType(buyOrSell.getOperation());
            entrustUser.setStatus(EntrustUserStatusEnums.ENTRUST_ING.getCode());
            entrustUser.setCreateTime(new Date());
            entrustUser.setUpdateTime(new Date());
            stockEntrustUserService.insertStockEntrustUser(entrustUser);
        }
    }

    /**
     * 取消被禁用账户，添加账户信息
     * @param messageSendVo      messageSendVo
     */
    private void fillAccount(BaseMessageSendVo messageSendVo) {
        List<Long> accountIds =  messageSendVo.getAccountIds();
        List<StockAccount> accountList = stockAccountService.selectListByIds(accountIds);
        Collections.sort(accountList, Comparator.comparing(StockAccount::getSort));// 排序
        Collections.reverse(accountList);// 从大到小排列

        // 重置账户Id
        messageSendVo.setAccountIds(accountList.stream().map(StockAccount::getId).collect(Collectors.toList()));
        Map<Long, StockAccount> accountMap = accountList.stream().collect(Collectors.toMap(StockAccount::getId, c -> c));
        messageSendVo.setAccountMap(accountMap);
    }

    // 撤销买入或者卖出
    private List<StockMessage> sendEntrustCancel(BaseMessageSendVo messageSendVo) {
        List<StockMessage> messages = createMessageList(messageSendVo);
        messages.forEach(c->{
            c.setData(messageSendVo.getEntrustCancel());
        });
        return messages;
    }

    // 买入或者卖出股票信息
    private List<StockMessage> sendBuyOrSell(BaseMessageSendVo messageSendVo) {
        List<StockMessage> result = new ArrayList<>();
        for (StockMessage message:  createMessageList(messageSendVo)){
            for (BuyOrSell buyOrSell: messageSendVo.getBuyOrSellList()){
                StockMessage clone = new StockMessage();
                BeanUtils.copyProperties(message, clone);
                // 将仓位转换成股数
                if(buyOrSell.getPosition() != null && buyOrSell.getNumber() == null){
                    Integer number = stockMoneyService.positionToNumber(clone.getAccountId(), buyOrSell.getPosition(), buyOrSell.getPrice());
                    buyOrSell.setNumber(number);
                }
                // 转换消息类型
                if(StockBuySellEnums.BUY.getCode() ==  buyOrSell.getOperation()){
                    clone.setType(SocketMessageServerTypeEnums.BUY.getCode());
                }else if(StockBuySellEnums.SELL.getCode() ==  buyOrSell.getOperation()){
                    clone.setType(SocketMessageServerTypeEnums.SELL.getCode());
                }
                clone.setData(buyOrSell);
                result.add(clone);
            }
        }
        return result;
    }

    /**
     * 先指定账户发送一个动作,消息体为空
     * @param messageSendVo messageSendVo
     */
    private List<StockMessage> sendAction(BaseMessageSendVo messageSendVo) {
        return createMessageList(messageSendVo);
    }

    /**
     * 账户登录信息
     * @param messageSendVo messageSendVo
     */
    private List<StockMessage> sendLogin(BaseMessageSendVo messageSendVo) {
        List<StockMessage> messages = createMessageList(messageSendVo);
        messages.forEach(c->{
            StockAccount account = messageSendVo.getAccountMap().get(c.getAccountId());
            account.setClient(null);
            c.setData(account);
        });
        return messages;
    }

    private List<StockMessage> createMessageList(BaseMessageSendVo messageSendVo){
        List<StockMessage> messages = new ArrayList<>();
        for (Long accountId : messageSendVo.getAccountIds()){
            StockAccount account = messageSendVo.getAccountMap().get(accountId);
            messages.add(createMessage(account, messageSendVo.getType()));
        }
        return messages;
    }

    private StockMessage createMessage(StockAccount account,Integer messageType) {
        StockMessage msg  = new StockMessage();
        msg.setAccountId(account.getId());
        msg.setClientId(account.getClientId());
        msg.setType(messageType);
        msg.setSubject(SocketMessageServerTypeEnums.parse(messageType).getMessage());
        msg.setWeight(account.getSort().intValue());
        msg.setStatus(StockMessageSendStatusEnums.UN_SEND.getCode());
        msg.setExecuted(StockMessageExeResultEnums.UN_EXE.getCode());
        msg.setCreateTime(new Date());
        msg.setUpdateTime(new Date());
        return msg;
    }
}
