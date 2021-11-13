package com.ruoyi.web.controller.stock;

import java.util.List;

import com.ruoyi.common.annotation.AnonymousAccess;
import com.ruoyi.stock.domain.vo.SimpleAccountVo;
import com.ruoyi.stock.socket.service.StockSocketService;
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
import com.ruoyi.stock.domain.StockAccount;
import com.ruoyi.stock.service.IStockAccountService;
import com.ruoyi.common.utils.poi.ExcelUtil;
import com.ruoyi.common.core.page.TableDataInfo;

/**
 * 下单账户Controller
 * 
 * @author jonk
 * @date 2021-01-06
 */
@RestController
@RequestMapping("/stock/account")
public class StockAccountController extends BaseController
{
    @Autowired
    private IStockAccountService stockAccountService;
    @Autowired
    private StockSocketService stockSocketService;

    /**
     * 查询下单账户列表
     */
    @PreAuthorize("@ss.hasPermi('stock:account:list')")
    @GetMapping("/list")
    public TableDataInfo list(StockAccount stockAccount)
    {
        startPage();
        List<StockAccount> list = stockAccountService.selectStockAccountList(stockAccount);
        return getDataTable(list);
    }


    /**
     * 查询下单账户列表
     */
    @PreAuthorize("@ss.hasPermi('stock:account:list')")
    @GetMapping("/list/simple")
    public TableDataInfo listSimple(StockAccount stockAccount)
    {
        startPage();
        List<SimpleAccountVo> list = stockAccountService.selectSimpleVoList(stockAccount);
        return getDataTable(list);
    }

    /**
     * 导出下单账户列表
     */
    @PreAuthorize("@ss.hasPermi('stock:account:export')")
    @Log(title = "下单账户", businessType = BusinessType.EXPORT)
    @GetMapping("/export")
    public AjaxResult export(StockAccount stockAccount)
    {
        List<StockAccount> list = stockAccountService.selectStockAccountList(stockAccount);
        ExcelUtil<StockAccount> util = new ExcelUtil<StockAccount>(StockAccount.class);
        return util.exportExcel(list, "account");
    }

    /**
     * 获取下单账户详细信息
     */
    @PreAuthorize("@ss.hasPermi('stock:account:query')")
    @GetMapping(value = "/{id}")
    public AjaxResult getInfo(@PathVariable("id") Long id)
    {
        return AjaxResult.success(stockAccountService.selectStockAccountById(id));
    }

    /**
     * 新增下单账户
     */
    @PreAuthorize("@ss.hasPermi('stock:account:add')")
    @Log(title = "下单账户", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody StockAccount stockAccount)
    {
        return toAjax(stockAccountService.insertStockAccount(stockAccount));
    }

    /**
     * 修改下单账户
     */
    @PreAuthorize("@ss.hasPermi('stock:account:edit')")
    @Log(title = "下单账户", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody StockAccount stockAccount)
    {
        return toAjax(stockAccountService.updateStockAccount(stockAccount));
    }

    /**
     * 删除下单账户
     */
    @PreAuthorize("@ss.hasPermi('stock:account:remove')")
    @Log(title = "下单账户", businessType = BusinessType.DELETE)
	@DeleteMapping("/{ids}")
    public AjaxResult remove(@PathVariable Long[] ids)
    {
        return toAjax(stockAccountService.deleteStockAccountByIds(ids));
    }



    /**
     * 获取账户详细信息，客户端测试使用
     */
    @AnonymousAccess
    @Log(title = "下单账户查询", businessType = BusinessType.OTHER)
    @GetMapping("/detail/{id}")
    public AjaxResult remove(@PathVariable Long id, Long clientId, String token)
    {
        if(stockSocketService.auth(clientId, token)) {
            return AjaxResult.success(stockAccountService.selectStockAccountById(id));
        }else{
            return AjaxResult.error("token无效！");
        }
    }
}
