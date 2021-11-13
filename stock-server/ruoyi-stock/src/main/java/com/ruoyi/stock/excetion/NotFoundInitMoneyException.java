package com.ruoyi.stock.excetion;

public class NotFoundInitMoneyException extends RuntimeException{
    public NotFoundInitMoneyException() {
    }

    public NotFoundInitMoneyException(String message) {
        super(message);
    }

    public NotFoundInitMoneyException(String message, Throwable cause) {
        super(message, cause);
    }

    public NotFoundInitMoneyException(Throwable cause) {
        super(cause);
    }

    public NotFoundInitMoneyException(String message, Throwable cause, boolean enableSuppression, boolean writableStackTrace) {
        super(message, cause, enableSuppression, writableStackTrace);
    }
}
