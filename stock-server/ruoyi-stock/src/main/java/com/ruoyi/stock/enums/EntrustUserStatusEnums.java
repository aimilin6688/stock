package com.ruoyi.stock.enums;

import com.ruoyi.stock.excetion.UnknownMessageBaseTypeException;
import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor
// 1：委托中，2：已委托, 3:部分成交. 4:全部成交，-1：撤单，-2：部分撤单
public enum EntrustUserStatusEnums {
    ENTRUST_ING(1, "委托中"),
    ENTRUST_ED(2,"已委托"),
    DEAL_PART(3, "部分成交"),
    DEAL_ALL(4, "全部成交"),
    ENTRUST_CANCEL(-1,"撤单"),
    ENTRUST_CANCEL_PART(-2, "部分撤单"),
    ENTRUST_ERROR(-3, "委托异常");


    private int code;
    private String message;


    public static EntrustUserStatusEnums parse(int code){
        for (EntrustUserStatusEnums type : EntrustUserStatusEnums.values()) {
            if(type.code == code){
                return type;
            }
        }
        throw new UnknownMessageBaseTypeException("未知的消息类型："+code);
    }
}
