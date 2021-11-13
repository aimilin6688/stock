package com.ruoyi.stock.utils;

import com.alibaba.fastjson.parser.DefaultJSONParser;
import com.alibaba.fastjson.parser.JSONToken;
import com.alibaba.fastjson.parser.deserializer.ObjectDeserializer;
import com.ruoyi.stock.enums.StockBuySellEnums;
import org.apache.commons.lang3.StringUtils;

import java.lang.reflect.Type;

/**
 * 买入卖出类型转换
 */
public class StockBuySellUtils implements ObjectDeserializer {

    @Override
    @SuppressWarnings("unchecked")
    public <T> T deserialze(DefaultJSONParser parser, Type type, Object fieldName) {
        String value = parser.parseObject(String.class);
        return (T)getBuySell(value);
    }


    public static Integer getBuySell(String typeStr){
        if(StringUtils.containsAny(typeStr, "买")){
            return  StockBuySellEnums.BUY.getCode();
        }
        if(StringUtils.containsAny(typeStr, "卖")){
            return  StockBuySellEnums.SELL.getCode();
        }
        return StockBuySellEnums.UNKNOWN.getCode();
    }

    @Override
    public int getFastMatchToken() {
        return JSONToken.LITERAL_INT;
    }
}
