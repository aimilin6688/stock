package com.ruoyi.web.controller.stock;

import java.util.List;

import com.ruoyi.stock.domain.vo.BaseMessageSendVo;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import com.ruoyi.common.annotation.Log;
import com.ruoyi.common.core.controller.BaseController;
import com.ruoyi.common.core.domain.AjaxResult;
import com.ruoyi.common.enums.BusinessType;
import com.ruoyi.stock.domain.StockMessage;
import com.ruoyi.stock.service.IStockMessageService;
import com.ruoyi.common.utils.poi.ExcelUtil;
import com.ruoyi.common.core.page.TableDataInfo;

/**
 * 消息记录Controller
 * 
 * @author jonk
 * @date 2021-01-11
 */
@RestController
@RequestMapping("/stock/message")
public class StockMessageController extends BaseController
{
    @Autowired
    private IStockMessageService stockMessageService;

    /**
     * 查询消息记录列表
     */
    @PreAuthorize("@ss.hasPermi('stock:message:list')")
    @GetMapping("/list")
    public TableDataInfo list(StockMessage stockMessage)
    {
        startPage();
        List<StockMessage> list = stockMessageService.selectStockMessageList(stockMessage);
        return getDataTable(list);
    }

    /**
     * 导出消息记录列表
     */
    @PreAuthorize("@ss.hasPermi('stock:message:export')")
    @Log(title = "消息记录", businessType = BusinessType.EXPORT)
    @GetMapping("/export")
    public AjaxResult export(StockMessage stockMessage)
    {
        List<StockMessage> list = stockMessageService.selectStockMessageList(stockMessage);
        ExcelUtil<StockMessage> util = new ExcelUtil<StockMessage>(StockMessage.class);
        return util.exportExcel(list, "message");
    }

    /**
     * 获取消息记录详细信息
     */
    @PreAuthorize("@ss.hasPermi('stock:message:query')")
    @GetMapping(value = "/{id}")
    public AjaxResult getInfo(@PathVariable("id") Long id)
    {
        return AjaxResult.success(stockMessageService.selectStockMessageById(id));
    }

    /**
     * 修改参数配置
     */
    @PreAuthorize("@ss.hasPermi('stock:message:send')")
    @Log(title = "发送基础消息", businessType = BusinessType.INSERT)
    @PostMapping("/send/base")
    public AjaxResult sendBase(@Validated @RequestBody BaseMessageSendVo messageSendVo){
        try {
            return AjaxResult.success(stockMessageService.sendBase(messageSendVo));
        } catch (Exception e) {
            return AjaxResult.error(e.getMessage());
        }
    }
}