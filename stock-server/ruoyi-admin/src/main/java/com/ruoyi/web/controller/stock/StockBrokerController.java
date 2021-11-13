package com.ruoyi.web.controller.stock;

import java.util.List;

import com.ruoyi.stock.mapper.StockBrokerMapper;
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
import com.ruoyi.stock.domain.StockBroker;
import com.ruoyi.stock.service.IStockBrokerService;
import com.ruoyi.common.utils.poi.ExcelUtil;
import com.ruoyi.common.core.page.TableDataInfo;

/**
 * 券商Controller
 * 
 * @author jonk
 * @date 2021-01-06
 */
@RestController
@RequestMapping("/stock/broker")
public class StockBrokerController extends BaseController
{
    @Autowired
    private IStockBrokerService stockBrokerService;
    @Autowired
    private StockBrokerMapper stockBrokerMapper;

    /**
     * 查询券商列表
     */
    @PreAuthorize("@ss.hasPermi('stock:broker:list')")
    @GetMapping("/list")
    public TableDataInfo list(StockBroker stockBroker)
    {
        startPage();
        List<StockBroker> list = stockBrokerService.selectStockBrokerList(stockBroker);
        return getDataTable(list);
    }

    /**
     * 查询券商列表
     */
    @PreAuthorize("@ss.hasPermi('stock:broker:list')")
    @GetMapping("/list/client")
    public AjaxResult listByClientId(Long  clientId)
    {
        List<StockBroker> list = stockBrokerMapper.selectStockBrokerListByClientId(clientId);
        return AjaxResult.success(list);
    }

    /**
     * 导出券商列表
     */
    @PreAuthorize("@ss.hasPermi('stock:broker:export')")
    @Log(title = "券商", businessType = BusinessType.EXPORT)
    @GetMapping("/export")
    public AjaxResult export(StockBroker stockBroker)
    {
        List<StockBroker> list = stockBrokerService.selectStockBrokerList(stockBroker);
        ExcelUtil<StockBroker> util = new ExcelUtil<StockBroker>(StockBroker.class);
        return util.exportExcel(list, "broker");
    }

    /**
     * 获取券商详细信息
     */
    @PreAuthorize("@ss.hasPermi('stock:broker:query')")
    @GetMapping(value = "/{id}")
    public AjaxResult getInfo(@PathVariable("id") Long id)
    {
        return AjaxResult.success(stockBrokerService.selectStockBrokerById(id));
    }

    /**
     * 新增券商
     */
    @PreAuthorize("@ss.hasPermi('stock:broker:add')")
    @Log(title = "券商", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody StockBroker stockBroker)
    {
        return toAjax(stockBrokerService.insertStockBroker(stockBroker));
    }

    /**
     * 修改券商
     */
    @PreAuthorize("@ss.hasPermi('stock:broker:edit')")
    @Log(title = "券商", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody StockBroker stockBroker)
    {
        return toAjax(stockBrokerService.updateStockBroker(stockBroker));
    }

    /**
     * 删除券商
     */
    @PreAuthorize("@ss.hasPermi('stock:broker:remove')")
    @Log(title = "券商", businessType = BusinessType.DELETE)
	@DeleteMapping("/{ids}")
    public AjaxResult remove(@PathVariable Long[] ids)
    {
        return toAjax(stockBrokerService.deleteStockBrokerByIds(ids));
    }
}
