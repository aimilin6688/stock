package com.ruoyi.stock.utils;

import org.apache.commons.lang3.StringUtils;

public class StockCodeUtils {
    /**
     * 格式化股票代码为6为数字码
     * <pre>
     *     1. sh600365  -> 600365
     *     2. sz300256  -> 300256
     *     3. 600365.SZ -> 600365
     *     4. 600365.SH -> 600365
     * </pre>
     * @param stockCode
     * @return
     */
    public static String formatCode(String stockCode){
        stockCode = StringUtils.removeStartIgnoreCase(stockCode, "sh");
        stockCode = StringUtils.removeStartIgnoreCase(stockCode, "sz");
        stockCode = StringUtils.removeEndIgnoreCase(stockCode, ".sh");
        stockCode = StringUtils.removeEndIgnoreCase(stockCode, ".sz");
        return StringUtils.leftPad(stockCode,6, "0");
    }
}
