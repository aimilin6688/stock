import request from '@/utils/request'

// 查询持仓列表
export function listPosition(query) {
  return request({
    url: '/stock/position/list',
    method: 'get',
    params: query
  })
}

// 查询持仓详细
export function getPosition(id) {
  return request({
    url: '/stock/position/' + id,
    method: 'get'
  })
}

// 导出持仓
export function exportPosition(query) {
  return request({
    url: '/stock/position/export',
    method: 'get',
    params: query
  })
}
