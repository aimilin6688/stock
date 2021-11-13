import request from '@/utils/request'

// 查询下单账户列表
export function listAccount(query) {
  return request({
    url: '/stock/account/list',
    method: 'get',
    params: query
  })
}

export function listAccountSimple(query) {
  return request({
    url: '/stock/account/list/simple',
    method: 'get',
    params: query
  })
}

// 查询下单账户详细
export function getAccount(id) {
  return request({
    url: '/stock/account/' + id,
    method: 'get'
  })
}

// 新增下单账户
export function addAccount(data) {
  return request({
    url: '/stock/account',
    method: 'post',
    data: data
  })
}

// 修改下单账户
export function updateAccount(data) {
  return request({
    url: '/stock/account',
    method: 'put',
    data: data
  })
}

// 删除下单账户
export function delAccount(id) {
  return request({
    url: '/stock/account/' + id,
    method: 'delete'
  })
}

// 导出下单账户
export function exportAccount(query) {
  return request({
    url: '/stock/account/export',
    method: 'get',
    params: query
  })
}
