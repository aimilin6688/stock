import { Message } from 'element-ui'

let websocket = null  //websocket的实例
let lockReconnect = false //避免重复连接
function startMonitor() {
  websocket = new WebSocket(process.env.VUE_APP_WEB_SOCKET_URL)
  //打开webSocket连接时，回调该函数
  websocket.onopen = function() {
    Message({ message: '连接成功', type: 'success', duration: 1000 })
  }

  //关闭webSocket连接时，回调该函数
  websocket.onclose = function() {
    //关闭连接
    Message({ message: '连接已关闭，正在重试...', type: 'error', duration: 2000 })
    reconnect()
  }

  // 异常回调
  websocket.onerror = function(event) {
    reconnect()
  }

  //接收信息
  websocket.onmessage = function(msg) {
    let data = JSON.parse(msg.data)
    if (data.success) {
      Message({ message: data.data, type: 'success', duration: 3000 })
    } else {
      Message({ message: data.data, type: 'error', duration: 3000 })
    }
  }
}

function reconnect() {
  if (lockReconnect) return;
  lockReconnect = true;
  //没连接上会一直重连，设置延迟避免请求过多
  setTimeout(function() {
    startMonitor();
    lockReconnect = false;
  }, 2000);
}

// 启动监控
reconnect()
