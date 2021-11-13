package com.ruoyi.stock.excetion;

public class UnknownMessageBaseTypeException extends  RuntimeException{
    public UnknownMessageBaseTypeException() {
    }

    public UnknownMessageBaseTypeException(String message) {
        super(message);
    }

    public UnknownMessageBaseTypeException(String message, Throwable cause) {
        super(message, cause);
    }

    public UnknownMessageBaseTypeException(Throwable cause) {
        super(cause);
    }

    public UnknownMessageBaseTypeException(String message, Throwable cause, boolean enableSuppression, boolean writableStackTrace) {
        super(message, cause, enableSuppression, writableStackTrace);
    }
}
