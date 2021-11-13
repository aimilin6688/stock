package com.ruoyi.stock.mapper;

import cn.hutool.core.date.DatePattern;
import cn.hutool.core.date.DateUtil;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.ruoyi.stock.domain.StockTradeDate;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import java.util.Date;

@Mapper
public interface StockTradeDateMapper extends BaseMapper<StockTradeDate> {

    /**
     * 查询n个交易日之后的交易日
     * @param date 日期 yyyy-MM-dd
     * @param n 天数,为正数
     * @return StockTradeDate
     */
    public StockTradeDate queryAfter(@Param("date") String date, @Param("n") int n);

    /**
     * 查询n个交易日之前的交易日
     * @param date 日期 yyyy-MM-dd
     * @param n 天数。为正数
     * @return StockTradeDate
     */
    public StockTradeDate queryBefore(@Param("date") String date, @Param("n") int n);

    /**
     * 判断指定的日期是否时交易日
     * @param date 日期 yyyy-MM-dd
     * @return true 交易日，false 非交易日
     */
    public boolean isTradeDate(@Param("date") String date);

    /**
     * 判断指定的日期是否时交易日
     * @param date 日期
     * @return true 交易日，false 非交易日
     */
    public default boolean isTradeDate(Date date){
        String dateStr = DateUtil.format(date, DatePattern.NORM_DATE_FORMAT);
        return this.isTradeDate(dateStr);
    }

    public default String getTradeDate(String date, int n){
        return n >= 0 ? queryAfter(date, n).getTradeDate():queryBefore(date, -n).getTradeDate();
    }

    public default String getTradeDate(Date date, int n){
        String dateStr = DateUtil.format(date, DatePattern.NORM_DATE_FORMAT);
        return n >= 0 ? queryAfter(dateStr, n).getTradeDate():queryBefore(dateStr, -n).getTradeDate();
    }
}