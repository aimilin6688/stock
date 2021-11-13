package com.ruoyi.web.controller.stock;

import com.ruoyi.common.annotation.Log;
import com.ruoyi.common.core.controller.BaseController;
import com.ruoyi.common.core.domain.AjaxResult;
import com.ruoyi.common.core.page.TableDataInfo;
import com.ruoyi.common.enums.BusinessType;
import com.ruoyi.common.utils.poi.ExcelUtil;
import com.ruoyi.stock.domain.StockPosition;
import com.ruoyi.stock.service.IStockPositionService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

/**
 * 持仓Controller
 * 
 * @author ruoyi
 * @date 2021-01-11
 */
@RestController
@RequestMapping("/stock/position")
public class StockPositionController extends BaseController
{
    @Autowired
    private IStockPositionService stockPositionService;

    /**
     * 查询持仓列表
     */
    @PreAuthorize("@ss.hasPermi('stock:position:list')")
    @GetMapping("/list")
    public TableDataInfo list(StockPosition stockPosition)
    {
        startPage();
        List<StockPosition> list = stockPositionService.selectStockPositionList(stockPosition);
        return getDataTable(list);
    }

    /**
     * 导出持仓列表
     */
    @PreAuthorize("@ss.hasPermi('stock:position:export')")
    @Log(title = "持仓", businessType = BusinessType.EXPORT)
    @GetMapping("/export")
    public AjaxResult export(StockPosition stockPosition)
    {
        List<StockPosition> list = stockPositionService.selectStockPositionList(stockPosition);
        ExcelUtil<StockPosition> util = new ExcelUtil<StockPosition>(StockPosition.class);
        return util.exportExcel(list, "position");
    }

    /**
     * 获取持仓详细信息
     */
    @PreAuthorize("@ss.hasPermi('stock:position:query')")
    @GetMapping(value = "/{id}")
    public AjaxResult getInfo(@PathVariable("id") Long id)
    {
        return AjaxResult.success(stockPositionService.selectStockPositionById(id));
    }

}
