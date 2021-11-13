package com.ruoyi.common.core.page;

import com.ruoyi.common.utils.StringUtils;

/**
 * 分页数据
 * 
 * @author ruoyi
 */
public class PageDomain
{
    /** 当前记录起始索引 */
    private Integer pageNum;

    /** 每页显示记录数 */
    private Integer pageSize;

    /** 排序列 */
    private String orderBy;

    public String getOrderBy()
    {
        if (StringUtils.isEmpty(orderBy))
        {
            return "";
        }
        StringBuffer sb = new StringBuffer();
        if(StringUtils.containsAny(this.orderBy, " ,")){
            String[] orderBys = StringUtils.split(this.orderBy,',');
            for (int i = 0; i < orderBys.length; i++) {
                String columns[] = StringUtils.split(orderBys[i],' ');
                sb.append(StringUtils.toUnderScoreCase(columns[0]));
                if(columns.length >= 2){
                    sb.append(" ").append(columns[1]);
                }
                if(i < orderBys.length -1){
                    sb.append(",");
                }
            }
            return sb.toString();
        }
        return StringUtils.toUnderScoreCase(orderBy) + " desc";
    }

    public Integer getPageNum()
    {
        return pageNum;
    }

    public void setPageNum(Integer pageNum)
    {
        this.pageNum = pageNum;
    }

    public Integer getPageSize()
    {
        return pageSize;
    }

    public void setPageSize(Integer pageSize)
    {
        this.pageSize = pageSize;
    }

    public void setOrderBy(String orderBy)
    {
        this.orderBy = orderBy;
    }
}
