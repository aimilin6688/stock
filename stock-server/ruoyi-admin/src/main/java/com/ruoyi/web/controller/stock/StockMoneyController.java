package com.ruoyi.web.controller.stock;

import com.ruoyi.common.annotation.Log;
import com.ruoyi.common.core.controller.BaseController;
import com.ruoyi.common.core.domain.AjaxResult;
import com.ruoyi.common.core.page.TableDataInfo;
import com.ruoyi.common.enums.BusinessType;
import com.ruoyi.common.utils.poi.ExcelUtil;
import com.ruoyi.stock.domain.StockMoney;
import com.ruoyi.stock.service.IStockMoneyService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

/**
 * 账户资金Controller
 * 
 * @author jonk
 * @date 2021-01-08
 */
@RestController
@RequestMapping("/stock/money")
public class StockMoneyController extends BaseController
{
    @Autowired
    private IStockMoneyService stockMoneyService;

    /**
     * 查询账户资金列表
     */
    @PreAuthorize("@ss.hasPermi('stock:money:list')")
    @GetMapping("/list")
    public TableDataInfo list(StockMoney stockMoney)
    {
        startPage();
        List<StockMoney> list = stockMoneyService.selectStockMoneyList(stockMoney);
        return getDataTable(list);
    }

    /**
     * 导出账户资金列表
     */
    @PreAuthorize("@ss.hasPermi('stock:money:export')")
    @Log(title = "账户资金", businessType = BusinessType.EXPORT)
    @GetMapping("/export")
    public AjaxResult export(StockMoney stockMoney)
    {
        List<StockMoney> list = stockMoneyService.selectStockMoneyList(stockMoney);
        ExcelUtil<StockMoney> util = new ExcelUtil<StockMoney>(StockMoney.class);
        return util.exportExcel(list, "money");
    }

    /**
     * 获取账户资金详细信息
     */
    @PreAuthorize("@ss.hasPermi('stock:money:query')")
    @GetMapping(value = "/{id}")
    public AjaxResult getInfo(@PathVariable("id") Long id)
    {
        return AjaxResult.success(stockMoneyService.selectStockMoneyById(id));
    }

}
