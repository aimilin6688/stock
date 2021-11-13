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
import com.ruoyi.stock.domain.StockClient;
import com.ruoyi.stock.service.IStockClientService;
import com.ruoyi.common.utils.poi.ExcelUtil;
import com.ruoyi.common.core.page.TableDataInfo;

/**
 * 下单客户端Controller
 * 
 * @author jonk
 * @date 2021-01-06
 */
@RestController
@RequestMapping("/stock/client")
public class StockClientController extends BaseController
{
    @Autowired
    private IStockClientService stockClientService;

    /**
     * 查询下单客户端列表
     */
    @PreAuthorize("@ss.hasPermi('stock:client:list')")
    @GetMapping("/list")
    public TableDataInfo list(StockClient stockClient)
    {
        startPage();
        List<StockClient> list = stockClientService.selectStockClientList(stockClient);
        return getDataTable(list);
    }

    /**
     * 查询下单客户端列表
     */
    @PreAuthorize("@ss.hasPermi('stock:client:list')")
    @GetMapping("/list/broker")
    public AjaxResult listByBrokerId(Long brokerId)
    {
        return AjaxResult.success(stockClientService.selectStockClientListByBrokerId(brokerId));
    }

    /**
     * 导出下单客户端列表
     */
    @PreAuthorize("@ss.hasPermi('stock:client:export')")
    @Log(title = "下单客户端", businessType = BusinessType.EXPORT)
    @GetMapping("/export")
    public AjaxResult export(StockClient stockClient)
    {
        List<StockClient> list = stockClientService.selectStockClientList(stockClient);
        ExcelUtil<StockClient> util = new ExcelUtil<StockClient>(StockClient.class);
        return util.exportExcel(list, "client");
    }

    /**
     * 获取下单客户端详细信息
     */
    @PreAuthorize("@ss.hasPermi('stock:client:query')")
    @GetMapping(value = "/{id}")
    public AjaxResult getInfo(@PathVariable("id") Long id)
    {
        return AjaxResult.success(stockClientService.selectStockClientById(id));
    }

    /**
     * 新增下单客户端
     */
    @PreAuthorize("@ss.hasPermi('stock:client:add')")
    @Log(title = "下单客户端", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody StockClient stockClient)
    {
        return toAjax(stockClientService.insertStockClient(stockClient));
    }

    /**
     * 修改下单客户端
     */
    @PreAuthorize("@ss.hasPermi('stock:client:edit')")
    @Log(title = "下单客户端", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody StockClient stockClient)
    {
        return toAjax(stockClientService.updateStockClient(stockClient));
    }

    /**
     * 删除下单客户端
     */
    @PreAuthorize("@ss.hasPermi('stock:client:remove')")
    @Log(title = "下单客户端", businessType = BusinessType.DELETE)
	@DeleteMapping("/{ids}")
    public AjaxResult remove(@PathVariable String[] ids)
    {
        return toAjax(stockClientService.deleteStockClientByIds(ids));
    }
}
