package com.ruoyi.stock.enums;

import com.ruoyi.stock.excetion.UnknownMessageBaseTypeException;
import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor
public enum SocketMessageServerTypeEnums {
    SIGN(1, "签收"),
    LOGIN(2,"登录"),
    LOGOUT(3, "退出登录"),
    MONEY(4, "资金查询"),
    BUY(5,"买入"),
    SELL(6, "卖出"),
    POSITION(7, "持仓查询"),
    DEAL(8,"成交查询"),
    ENTRUST(9, "委托查询"),
    CANCEL(10, "撤销委托"),
    CLEAR(11, "清仓"),
    ERROR(-1, "异常"),

    // 客户端需要获取账户信息时返回消息类型
    ACCOUNT_INFO(12, "账户信息");

    private int code;
    private String message;


    public static SocketMessageServerTypeEnums parse(int code){
        for (SocketMessageServerTypeEnums type : SocketMessageServerTypeEnums.values()) {
            if(type.code == code){
                return type;
            }
        }
        throw new UnknownMessageBaseTypeException("未知的消息类型："+code);
    }
}
