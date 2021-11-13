import request from '@/utils/request'

// 查询委托消息列表
export function listEntrust_user(query) {
  return request({
    url: '/stock/entrust_user/list',
    method: 'get',
    params: query
  })
}

// 查询委托消息详细
export function getEntrust_user(id) {
  return request({
    url: '/stock/entrust_user/' + id,
    method: 'get'
  })
}


// 导出委托消息
export function exportEntrust_user(query) {
  return request({
    url: '/stock/entrust_user/export',
    method: 'get',
    params: query
  })
}
