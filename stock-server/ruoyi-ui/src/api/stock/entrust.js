import request from '@/utils/request'

// 查询委托列表
export function listEntrust(query) {
  return request({
    url: '/stock/entrust/list',
    method: 'get',
    params: query
  })
}

// 查询委托详细
export function getEntrust(id) {
  return request({
    url: '/stock/entrust/' + id,
    method: 'get'
  })
}


// 导出委托
export function exportEntrust(query) {
  return request({
    url: '/stock/entrust/export',
    method: 'get',
    params: query
  })
}
