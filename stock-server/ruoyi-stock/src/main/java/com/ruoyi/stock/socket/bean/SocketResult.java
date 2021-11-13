package com.ruoyi.stock.socket.bean;

import com.alibaba.fastjson.JSONObject;
import lombok.AllArgsConstructor;
import lombok.Data;
import org.apache.poi.ss.formula.functions.T;

import java.io.Serializable;

@Data
@AllArgsConstructor
public class SocketResult implements Serializable {
    private static final long serialVersionUID = 1L;
    private int code;
    /**
     * code 名称
     */
    private String name;
    /**
     * 信息详细
     */
    private String msg;
    // 消息数据，一般是 StockMessage类型
    private Object data;
    private boolean success;

    public SocketResult(SocketStatusEnums status, Object data){
        this.code = status.getCode();
        this.name = status.name();
        this.msg = status.getMessage();
        this.data = data;
    }

    /**
     * 将数据转换成指定类型
     * @param clazz 需要转换的类
     * @param <R> 目标类
     * @return 结果
     */
    @SuppressWarnings({"unchecked"})
    public <R> R dataToType(Class<R> clazz){
        return dataToType(this.data, clazz);
    }

    public static <R> R dataToType(Object obj,Class<R> clazz){
        if(obj.getClass().equals(clazz)){
            return (R) obj;
        }
        if(obj instanceof JSONObject){
            JSONObject json = (JSONObject)obj;
            return json.toJavaObject(clazz);
        }
        if(obj instanceof  String){
            String dataStr = obj.toString();
            return JSONObject.parseObject(dataStr, clazz);
        }
        return (R) obj;
    }

    public static SocketResult status(SocketStatusEnums statusEnums){
        return new SocketResult(statusEnums, "");
    }

    public static SocketResult success(Object data){
        return new SocketResult(SocketStatusEnums.SUCCESS, data);
    }

    public static SocketResult fail(Object data){
        return new SocketResult(SocketStatusEnums.FAIL, data);
    }

    public boolean isSuccess() {
        return code == SocketStatusEnums.SUCCESS.getCode();
    }
}
