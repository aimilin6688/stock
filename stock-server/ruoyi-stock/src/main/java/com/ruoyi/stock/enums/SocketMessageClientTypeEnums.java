package com.ruoyi.stock.enums;

import com.ruoyi.stock.excetion.UnknownMessageBaseTypeException;
import lombok.AllArgsConstructor;
import lombok.Getter;

/**
 * 客户端请求消息类型
 */
@Getter
@AllArgsConstructor
public enum SocketMessageClientTypeEnums {
    // 客户端发送请求类型,H(handle):需要服务端处理数据，I(info):需要服务端提供数据,R(result):执行结果
    SIGN(1, "签收"),
    R_LOGIN(102, "登录结果"),
    R_LOGOUT(103, "退出登录结果"),
    R_MONEY(104, "资金查询结果"),
    R_BUY(105,"买入结果"),
    R_SELL(106,"卖出结果"),
    R_POSITION(107, "持仓查询结果"),
    R_DEAL(108,"成交查询结果"),
    R_ENTRUST(109, "委托查询结果"),
    R_CANCEL(110, "撤销委托结果"),
    R_CLEAR(111, "清仓结果"),
    R_ACCOUNT_INFO(112, "账户信息结果"),

    H_SUPPORT_BROKER(200, "支持券商"),
    I_ACCOUNT_INFO(201, "账户信息");


    private int code;
    private String message;


    public static SocketMessageClientTypeEnums parse(int code){
        for (SocketMessageClientTypeEnums type : SocketMessageClientTypeEnums.values()) {
            if(type.code == code){
                return type;
            }
        }
        throw new UnknownMessageBaseTypeException("未知的消息类型："+code);
    }
}
