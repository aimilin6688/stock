package com.ruoyi.stock.excetion;

public class UnSupportBrokerException extends RuntimeException{
    public UnSupportBrokerException() {
    }

    public UnSupportBrokerException(String message) {
        super(message);
    }

    public UnSupportBrokerException(String message, Throwable cause) {
        super(message, cause);
    }

    public UnSupportBrokerException(Throwable cause) {
        super(cause);
    }

    public UnSupportBrokerException(String message, Throwable cause, boolean enableSuppression, boolean writableStackTrace) {
        super(message, cause, enableSuppression, writableStackTrace);
    }
}
