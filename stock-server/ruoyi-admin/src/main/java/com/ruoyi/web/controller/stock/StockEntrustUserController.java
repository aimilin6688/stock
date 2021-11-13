package com.ruoyi.web.controller.stock;

import com.ruoyi.common.annotation.Log;
import com.ruoyi.common.core.controller.BaseController;
import com.ruoyi.common.core.domain.AjaxResult;
import com.ruoyi.common.core.page.TableDataInfo;
import com.ruoyi.common.enums.BusinessType;
import com.ruoyi.common.utils.poi.ExcelUtil;
import com.ruoyi.stock.domain.StockEntrustUser;
import com.ruoyi.stock.service.IStockEntrustUserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * 委托消息Controller
 *
 * @author jonk
 * @date 2021-01-11
 */
@RestController
@RequestMapping("/stock/entrust_user")
public class StockEntrustUserController extends BaseController
{
    @Autowired
    private IStockEntrustUserService stockEntrustUserService;

    /**
     * 查询委托消息列表
     */
    @PreAuthorize("@ss.hasPermi('stock:entrust_user:list')")
    @GetMapping("/list")
    public TableDataInfo list(StockEntrustUser stockEntrustUser)
    {
        startPage();
        List<StockEntrustUser> list = stockEntrustUserService.selectStockEntrustUserList(stockEntrustUser);
        return getDataTable(list);
    }

    /**
     * 导出委托消息列表
     */
    @PreAuthorize("@ss.hasPermi('stock:entrust_user:export')")
    @Log(title = "委托消息", businessType = BusinessType.EXPORT)
    @GetMapping("/export")
    public AjaxResult export(StockEntrustUser stockEntrustUser)
    {
        List<StockEntrustUser> list = stockEntrustUserService.selectStockEntrustUserList(stockEntrustUser);
        ExcelUtil<StockEntrustUser> util = new ExcelUtil<StockEntrustUser>(StockEntrustUser.class);
        return util.exportExcel(list, "entrust_user");
    }

    /**
     * 获取委托消息详细信息
     */
    @PreAuthorize("@ss.hasPermi('stock:entrust_user:query')")
    @GetMapping(value = "/{id}")
    public AjaxResult getInfo(@PathVariable("id") Long id)
    {
        return AjaxResult.success(stockEntrustUserService.selectStockEntrustUserById(id));
    }


    /**
     * 修改委托消息
     */
    @PreAuthorize("@ss.hasPermi('stock:entrust_user:edit')")
    @Log(title = "委托消息", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody StockEntrustUser stockEntrustUser)
    {
        return toAjax(stockEntrustUserService.updateStockEntrustUser(stockEntrustUser));
    }
}