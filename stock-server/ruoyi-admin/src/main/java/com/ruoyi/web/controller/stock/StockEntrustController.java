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
import com.ruoyi.stock.domain.StockEntrust;
import com.ruoyi.stock.service.IStockEntrustService;
import com.ruoyi.common.utils.poi.ExcelUtil;
import com.ruoyi.common.core.page.TableDataInfo;

/**
 * 账户每日客户端导出委托数据Controller
 * 
 * @author jonk
 * @date 2021-01-08
 */
@RestController
@RequestMapping("/stock/entrust")
public class StockEntrustController extends BaseController
{
    @Autowired
    private IStockEntrustService stockEntrustService;

    /**
     * 查询账户每日客户端导出委托数据列表
     */
    @PreAuthorize("@ss.hasPermi('stock:entrust:list')")
    @GetMapping("/list")
    public TableDataInfo list(StockEntrust stockEntrust)
    {
        startPage();
        List<StockEntrust> list = stockEntrustService.selectStockEntrustList(stockEntrust);
        return getDataTable(list);
    }

    /**
     * 导出账户每日客户端导出委托数据列表
     */
    @PreAuthorize("@ss.hasPermi('stock:entrust:export')")
    @Log(title = "账户每日客户端导出委托数据", businessType = BusinessType.EXPORT)
    @GetMapping("/export")
    public AjaxResult export(StockEntrust stockEntrust)
    {
        List<StockEntrust> list = stockEntrustService.selectStockEntrustList(stockEntrust);
        ExcelUtil<StockEntrust> util = new ExcelUtil<StockEntrust>(StockEntrust.class);
        return util.exportExcel(list, "entrust");
    }

    /**
     * 获取账户每日客户端导出委托数据详细信息
     */
    @PreAuthorize("@ss.hasPermi('stock:entrust:query')")
    @GetMapping(value = "/{id}")
    public AjaxResult getInfo(@PathVariable("id") Long id)
    {
        return AjaxResult.success(stockEntrustService.selectStockEntrustById(id));
    }

}
