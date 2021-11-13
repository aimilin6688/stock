import request from '@/utils/request'

// 查询账户初始信息列表
export function listAccount_init(query) {
  return request({
    url: '/stock/account_init/list',
    method: 'get',
    params: query
  })
}

// 查询账户初始信息详细
export function getAccount_init(id) {
  return request({
    url: '/stock/account_init/' + id,
    method: 'get'
  })
}

// 新增账户初始信息
export function addAccount_init(data) {
  return request({
    url: '/stock/account_init',
    method: 'post',
    data: data
  })
}

// 修改账户初始信息
export function updateAccount_init(data) {
  return request({
    url: '/stock/account_init',
    method: 'put',
    data: data
  })
}

// 删除账户初始信息
export function delAccount_init(id) {
  return request({
    url: '/stock/account_init/' + id,
    method: 'delete'
  })
}

// 导出账户初始信息
export function exportAccount_init(query) {
  return request({
    url: '/stock/account_init/export',
    method: 'get',
    params: query
  })
}