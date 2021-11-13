import request from '@/utils/request'

// 查询券商列表
export function listBroker(query) {
  return request({
    url: '/stock/broker/list',
    method: 'get',
    params: query
  })
}

// 查询券商列表
export function listBrokerByClientId(clientId) {
  return request({
    url: '/stock/broker/list/client',
    method: 'get',
    params: {clientId}
  })
}


// 查询券商详细
export function getBroker(id) {
  return request({
    url: '/stock/broker/' + id,
    method: 'get'
  })
}

// 新增券商
export function addBroker(data) {
  return request({
    url: '/stock/broker',
    method: 'post',
    data: data
  })
}

// 修改券商
export function updateBroker(data) {
  return request({
    url: '/stock/broker',
    method: 'put',
    data: data
  })
}

// 删除券商
export function delBroker(id) {
  return request({
    url: '/stock/broker/' + id,
    method: 'delete'
  })
}

// 导出券商
export function exportBroker(query) {
  return request({
    url: '/stock/broker/export',
    method: 'get',
    params: query
  })
}
