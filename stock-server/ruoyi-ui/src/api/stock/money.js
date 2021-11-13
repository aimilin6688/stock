import request from '@/utils/request'

// 查询资金列表
export function listMoney(query) {
  return request({
    url: '/stock/money/list',
    method: 'get',
    params: query
  })
}

// 查询资金详细
export function getMoney(id) {
  return request({
    url: '/stock/money/' + id,
    method: 'get'
  })
}


// 导出资金
export function exportMoney(query) {
  return request({
    url: '/stock/money/export',
    method: 'get',
    params: query
  })
}
