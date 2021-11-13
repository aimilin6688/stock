package com.ruoyi.web.controller.stock;

import java.util.List;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import com.ruoyi.common.annotation.Log;
import com.ruoyi.common.core.controller.BaseController;
import com.ruoyi.common.core.domain.AjaxResult;
import com.ruoyi.common.enums.BusinessType;
import com.ruoyi.stock.domain.StockDeal;
import com.ruoyi.stock.service.IStockDealService;
import com.ruoyi.common.utils.poi.ExcelUtil;
import com.ruoyi.common.core.page.TableDataInfo;

/**
 * 成交Controller
 * 
 * @author jonk
 * @date 2021-01-08
 */
@RestController
@RequestMapping("/stock/deal")
public class StockDealController extends BaseController
{
    @Autowired
    private IStockDealService stockDealService;

    /**
     * 查询成交列表
     */
    @PreAuthorize("@ss.hasPermi('stock:deal:list')")
    @GetMapping("/list")
    public TableDataInfo list(StockDeal stockDeal)
    {
        startPage();
        List<StockDeal> list = stockDealService.selectStockDealList(stockDeal);
        return getDataTable(list);
    }

    /**
     * 导出成交列表
     */
    @PreAuthorize("@ss.hasPermi('stock:deal:export')")
    @Log(title = "成交", businessType = BusinessType.EXPORT)
    @GetMapping("/export")
    public AjaxResult export(StockDeal stockDeal)
    {
        List<StockDeal> list = stockDealService.selectStockDealList(stockDeal);
        ExcelUtil<StockDeal> util = new ExcelUtil<StockDeal>(StockDeal.class);
        return util.exportExcel(list, "deal");
    }

    /**
     * 获取成交详细信息
     */
    @PreAuthorize("@ss.hasPermi('stock:deal:query')")
    @GetMapping(value = "/{id}")
    public AjaxResult getInfo(@PathVariable("id") Long id)
    {
        return AjaxResult.success(stockDealService.selectStockDealById(id));
    }
}
