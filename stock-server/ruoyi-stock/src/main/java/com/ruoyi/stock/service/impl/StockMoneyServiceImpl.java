package com.ruoyi.stock.service.impl;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.Date;
import java.util.List;
import java.util.Objects;

import cn.hutool.core.date.DatePattern;
import cn.hutool.core.date.DateUtil;
import com.ruoyi.stock.domain.StockAccountInit;
import com.ruoyi.stock.excetion.NotFoundInitMoneyException;
import com.ruoyi.stock.mapper.StockTradeDateMapper;
import com.ruoyi.stock.service.IStockAccountInitService;
import com.ruoyi.stock.service.IStockMoneyService;
import com.ruoyi.stock.utils.MaxDrawdownUtils;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.stock.mapper.StockMoneyMapper;
import com.ruoyi.stock.domain.StockMoney;

/**
 * 账户资金Service业务层处理
 * 
 * @author jonk
 * @date 2021-01-08
 */
@Service
@Slf4j
public class StockMoneyServiceImpl implements IStockMoneyService
{
    @Autowired
    private StockMoneyMapper stockMoneyMapper;
    @Autowired
    private AccountFillerService accountFillerService;
    @Autowired
    private AccountService accountService;
    @Autowired
    private IStockAccountInitService stockAccountInitService;
    @Autowired
    private StockTradeDateMapper stockTradeDateMapper;
    /**
     * 查询账户资金
     * 
     * @param id 账户资金ID
     * @return 账户资金
     */
    @Override
    public StockMoney selectStockMoneyById(Long id)
    {
        return accountFillerService.fill(stockMoneyMapper.selectStockMoneyById(id));
    }

    /**
     * 查询账户资金列表
     * 
     * @param stockMoney 账户资金
     * @return 账户资金
     */
    @Override
    public List<StockMoney> selectStockMoneyList(StockMoney stockMoney)
    {
        return accountFillerService.fill(stockMoneyMapper.selectStockMoneyList(stockMoney));
    }

    /**
     * 新增账户资金
     * 
     * @param stockMoney 账户资金
     * @return 结果
     */
    @Override
    public int insertStockMoney(StockMoney stockMoney)
    {
        Long accountId = stockMoney.getAccountId();
        // 必须有账户号
        Objects.requireNonNull(accountId);
        stockMoney.setInsertTime(new Date());
        // 设置账户净值
        StockAccountInit accountInit = stockAccountInitService.selectByAccountId(accountId);
        if(accountInit != null){
            stockMoney.setNetValue(stockMoney.getTotal().divide(accountInit.getInitMoney(), 5, RoundingMode.HALF_UP));
        }
        // 计算增长率
        String lastTradeDate = stockTradeDateMapper.getTradeDate(stockMoney.getDate(), -1);
        BigDecimal lastMoney = accountService.queryMoney(accountId,lastTradeDate);
        if(lastMoney != null && accountInit != null){
            BigDecimal increase = stockMoney.getTotal().divide(lastMoney, 5, RoundingMode.HALF_UP).subtract(new BigDecimal(1));
            stockMoney.setIncrease(increase);

            // 计算最大回测，从账户测试日期
            String startDate = DateUtil.format(accountInit.getInitDate(), DatePattern.NORM_DATE_FORMAT);
            List<Double> increaseList =  stockMoneyMapper.queryIncrease(accountId, startDate, lastTradeDate);
            increaseList.add(increase.doubleValue());
            stockMoney.setMaxDrawdown(BigDecimal.valueOf(MaxDrawdownUtils.calculateByIncrease(increaseList)));
        }else{
            stockMoney.setIncrease(BigDecimal.ZERO);
            stockMoney.setMaxDrawdown(BigDecimal.ZERO);
        }
        log.debug("账户：{}，上个交易日：{}，上个交易日资金：{}，保存资金信息：{}", accountId, lastTradeDate,lastMoney, stockMoney);
        return stockMoneyMapper.insertStockMoney(stockMoney);
    }

    /**
     * 修改账户资金
     * 
     * @param stockMoney 账户资金
     * @return 结果
     */
    @Override
    public int updateStockMoney(StockMoney stockMoney)
    {
        return stockMoneyMapper.updateStockMoney(stockMoney);
    }

    /**
     * 批量删除账户资金
     * 
     * @param ids 需要删除的账户资金ID
     * @return 结果
     */
    @Override
    public int deleteStockMoneyByIds(Long[] ids)
    {
        return stockMoneyMapper.deleteStockMoneyByIds(ids);
    }

    /**
     * 删除账户资金信息
     * 
     * @param id 账户资金ID
     * @return 结果
     */
    @Override
    public int deleteStockMoneyById(Long id)
    {
        return stockMoneyMapper.deleteStockMoneyById(id);
    }

    @Override
    public Integer positionToNumber(Long accountId, BigDecimal position, BigDecimal price) {
        if(position == null){
            throw new RuntimeException("指定仓位不能为空");
        }
        if(position.floatValue() <= 0 || position.floatValue() > 100){
            throw new RuntimeException("指定仓位必须大于0小于100");
        }
        // 查询账户资金信息
        BigDecimal money = accountService.queryMoney(accountId,null);
        if(money == null){
            throw new NotFoundInitMoneyException("账户："+ accountService.queryName(accountId) + ",没有初始资金！");
        }

        // 可用资金
        BigDecimal useMoney = money.multiply(position.add(new BigDecimal(0.5))).divide(new BigDecimal(100),5, BigDecimal.ROUND_HALF_UP);

        // 股数 = (int)(资金 * ((仓位 + 0.5)/100) / 价格 / 100) * 100
        return  useMoney.divide(price,5, BigDecimal.ROUND_HALF_UP ).divide(new BigDecimal(100),5, BigDecimal.ROUND_HALF_UP).intValue() * 100;
    }

    @Override
    public int deleteByAccountIdAndDate(Long accountId, Date date) {
        return stockMoneyMapper.deleteByAccountIdAndDate(accountId, date);
    }
}
