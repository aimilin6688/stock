import request from '@/utils/request'

// 查询下单客户端列表
export function listClient(query) {
  return request({
    url: '/stock/client/list',
    method: 'get',
    params: query
  })
}

// 查询下单客户端列表
export function listClientByBrokerId(brokerId) {
  return request({
    url: '/stock/client/list/broker',
    method: 'get',
    params: {brokerId}
  })
}

// 查询下单客户端详细
export function getClient(id) {
  return request({
    url: '/stock/client/' + id,
    method: 'get'
  })
}

// 新增下单客户端
export function addClient(data) {
  return request({
    url: '/stock/client',
    method: 'post',
    data: data
  })
}

// 修改下单客户端
export function updateClient(data) {
  return request({
    url: '/stock/client',
    method: 'put',
    data: data
  })
}

// 删除下单客户端
export function delClient(id) {
  return request({
    url: '/stock/client/' + id,
    method: 'delete'
  })
}

// 导出下单客户端
export function exportClient(query) {
  return request({
    url: '/stock/client/export',
    method: 'get',
    params: query
  })
}
