package com.ruoyi.stock.mapper;

import java.util.List;
import com.ruoyi.stock.domain.StockAccount;
import com.ruoyi.stock.domain.vo.SimpleAccountVo;

/**
 * 下单账户Mapper接口
 * 
 * @author jonk
 * @date 2021-01-06
 */
public interface StockAccountMapper 
{
    /**
     * 查询下单账户
     * 
     * @param id 下单账户ID
     * @return 下单账户
     */
    public StockAccount selectStockAccountById(Long id);


    /**
     * 下拉列表要展示的信息
     * @param stockAccount
     * @return
     */
    public List<SimpleAccountVo> selectSimpleVoList(StockAccount stockAccount);

    /**
     * 查询下单账户列表
     * 
     * @param stockAccount 下单账户
     * @return 下单账户集合
     */
    public List<StockAccount> selectStockAccountList(StockAccount stockAccount);

    /**
     * 新增下单账户
     * 
     * @param stockAccount 下单账户
     * @return 结果
     */
    public int insertStockAccount(StockAccount stockAccount);

    /**
     * 修改下单账户
     * 
     * @param stockAccount 下单账户
     * @return 结果
     */
    public int updateStockAccount(StockAccount stockAccount);

    /**
     * 删除下单账户
     * 
     * @param id 下单账户ID
     * @return 结果
     */
    public int deleteStockAccountById(Long id);

    /**
     * 批量删除下单账户
     * 
     * @param ids 需要删除的数据ID
     * @return 结果
     */
    public int deleteStockAccountByIds(Long[] ids);
}
