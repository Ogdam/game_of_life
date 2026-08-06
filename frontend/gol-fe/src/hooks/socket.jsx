const CLIENT_ID_KEY = 'gol_client_id'

function getOrCreateClientId() {
  let id = localStorage.getItem(CLIENT_ID_KEY)
  if (!id) {
    id = crypto.randomUUID()
    localStorage.setItem(CLIENT_ID_KEY, id)
  }
  return id
}

class useGameSocket {
  ws = null
  listeners = new Set()
  url = null
  reconnectAttempts = 0
  reconnectTimer = null

  connect(url) {
    this.url = url
    this._open()
  }

  _open() {
    const clientId = getOrCreateClientId()
    const wsUrl = `${this.url}?client_id=${encodeURIComponent(clientId)}`
    this.ws = new WebSocket(wsUrl)

    this.ws.onopen = () => {
      this.reconnectAttempts = 0
    }

    this.ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      if (data.client_id) {
        localStorage.setItem(CLIENT_ID_KEY, data.client_id)
      }
      this.listeners.forEach((fn) => fn(data))
    }

    this.ws.onclose = () => {
      this._scheduleReconnect()
    }

    this.ws.onerror = () => {
      this.ws?.close()
    }
  }

  _scheduleReconnect() {
    clearTimeout(this.reconnectTimer)
    const delay = Math.min(1000 * 2 ** this.reconnectAttempts, 15000)
    this.reconnectAttempts += 1
    this.reconnectTimer = setTimeout(() => this._open(), delay)
  }

  subscribe(fn) {
    this.listeners.add(fn)
    return () => this.listeners.delete(fn)
  }

  send(msg) {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(msg))
    }
  }
}

export const socket = new useGameSocket()
