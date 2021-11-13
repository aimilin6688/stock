import request from '@/utils/request'

// 查询成交列表
export function listDeal(query) {
  return request({
    url: '/stock/deal/list',
    method: 'get',
    params: query
  })
}

// 查询成交详细
export function getDeal(id) {
  return request({
    url: '/stock/deal/' + id,
    method: 'get'
  })
}


// 导出成交
export function exportDeal(query) {
  return request({
    url: '/stock/deal/export',
    method: 'get',
    params: query
  })
}
