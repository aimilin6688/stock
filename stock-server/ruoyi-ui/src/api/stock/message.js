import request from '@/utils/request'

// 查询消息列表
export function listMessage(query) {
  return request({
    url: '/stock/message/list',
    method: 'get',
    params: query
  })
}

// 查询消息详细
export function getMessage(id) {
  return request({
    url: '/stock/message/' + id,
    method: 'get'
  })
}

// 导出消息
export function exportMessage(query) {
  return request({
    url: '/stock/message/export',
    method: 'get',
    params: query
  })
}



// 发送基础消息
export function sendBaseMessage(data) {
  return request({
    url: '/stock/message/send/base',
    method: 'post',
    data: data
  })
}
