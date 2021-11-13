package com.ruoyi.stock.socket.bean;

import lombok.AllArgsConstructor;
import lombok.Getter;

@AllArgsConstructor
@Getter
public enum SocketStatusEnums {
    SUCCESS(1, "成功"),
    FAIL(0,"失败"),
    AUTH_FAIL(100, "登录认证失败");



    private int code;
    private String message;
}
