package com.ruoyi.web.controller.stock;

import java.util.List;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import com.ruoyi.common.annotation.Log;
import com.ruoyi.common.core.controller.BaseController;
import com.ruoyi.common.core.domain.AjaxResult;
import com.ruoyi.common.enums.BusinessType;
import com.ruoyi.stock.domain.StockAccountInit;
import com.ruoyi.stock.service.IStockAccountInitService;
import com.ruoyi.common.utils.poi.ExcelUtil;
import com.ruoyi.common.core.page.TableDataInfo;

/**
 * 账户初始信息Controller
 * 
 * @author jonk
 * @date 2021-01-08
 */
@RestController
@RequestMapping("/stock/account_init")
public class StockAccountInitController extends BaseController
{
    @Autowired
    private IStockAccountInitService stockAccountInitService;

    /**
     * 查询账户初始信息列表
     */
    @PreAuthorize("@ss.hasPermi('stock:account_init:list')")
    @GetMapping("/list")
    public TableDataInfo list(StockAccountInit stockAccountInit)
    {
        startPage();
        List<StockAccountInit> list = stockAccountInitService.selectStockAccountInitList(stockAccountInit);
        return getDataTable(list);
    }

    /**
     * 导出账户初始信息列表
     */
    @PreAuthorize("@ss.hasPermi('stock:account_init:export')")
    @Log(title = "账户初始信息", businessType = BusinessType.EXPORT)
    @GetMapping("/export")
    public AjaxResult export(StockAccountInit stockAccountInit)
    {
        List<StockAccountInit> list = stockAccountInitService.selectStockAccountInitList(stockAccountInit);
        ExcelUtil<StockAccountInit> util = new ExcelUtil<StockAccountInit>(StockAccountInit.class);
        return util.exportExcel(list, "account_init");
    }

    /**
     * 获取账户初始信息详细信息
     */
    @PreAuthorize("@ss.hasPermi('stock:account_init:query')")
    @GetMapping(value = "/{id}")
    public AjaxResult getInfo(@PathVariable("id") Long id)
    {
        return AjaxResult.success(stockAccountInitService.selectStockAccountInitById(id));
    }

    /**
     * 新增账户初始信息
     */
    @PreAuthorize("@ss.hasPermi('stock:account_init:add')")
    @Log(title = "账户初始信息", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody StockAccountInit stockAccountInit)
    {
        return toAjax(stockAccountInitService.insertStockAccountInit(stockAccountInit));
    }

    /**
     * 修改账户初始信息
     */
    @PreAuthorize("@ss.hasPermi('stock:account_init:edit')")
    @Log(title = "账户初始信息", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody StockAccountInit stockAccountInit)
    {
        return toAjax(stockAccountInitService.updateStockAccountInit(stockAccountInit));
    }

    /**
     * 删除账户初始信息
     */
    @PreAuthorize("@ss.hasPermi('stock:account_init:remove')")
    @Log(title = "账户初始信息", businessType = BusinessType.DELETE)
	@DeleteMapping("/{ids}")
    public AjaxResult remove(@PathVariable Long[] ids)
    {
        return toAjax(stockAccountInitService.deleteStockAccountInitByIds(ids));
    }
}
