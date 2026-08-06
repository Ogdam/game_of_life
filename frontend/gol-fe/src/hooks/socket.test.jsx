import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest'

class MockWebSocket {
  static instances = []

  constructor(url) {
    this.url = url
    this.readyState = MockWebSocket.OPEN
    this.onopen = null
    this.onmessage = null
    this.onclose = null
    this.onerror = null
    this.sent = []
    MockWebSocket.instances.push(this)
  }

  send(data) {
    this.sent.push(data)
  }

  close() {
    this.onclose?.()
  }
}
MockWebSocket.OPEN = 1
MockWebSocket.CLOSED = 3

describe('socket', () => {
  let socket

  beforeEach(async () => {
    vi.resetModules()
    vi.useFakeTimers()
    vi.stubGlobal('WebSocket', MockWebSocket)
    MockWebSocket.instances = []
    localStorage.clear()
    ;({ socket } = await import('./socket'))
  })

  afterEach(() => {
    vi.useRealTimers()
    vi.unstubAllGlobals()
  })

  it('generates and persists a client id on connect', () => {
    socket.connect('ws://localhost:8000/ws')
    const id = localStorage.getItem('gol_client_id')
    expect(id).toBeTruthy()
    expect(MockWebSocket.instances[0].url).toContain(encodeURIComponent(id))
  })

  it('reuses an existing client id', () => {
    localStorage.setItem('gol_client_id', 'existing-id')
    socket.connect('ws://localhost:8000/ws')
    expect(MockWebSocket.instances[0].url).toContain('existing-id')
  })

  it('notifies subscribers when a message is received', () => {
    socket.connect('ws://localhost:8000/ws')
    const listener = vi.fn()
    socket.subscribe(listener)

    MockWebSocket.instances[0].onmessage({ data: JSON.stringify({ tick: 1 }) })

    expect(listener).toHaveBeenCalledWith({ tick: 1 })
  })

  it('updates the stored client id when the server sends one', () => {
    socket.connect('ws://localhost:8000/ws')
    MockWebSocket.instances[0].onmessage({ data: JSON.stringify({ client_id: 'server-id' }) })
    expect(localStorage.getItem('gol_client_id')).toBe('server-id')
  })

  it('unsubscribe stops notifying the listener', () => {
    socket.connect('ws://localhost:8000/ws')
    const listener = vi.fn()
    const unsubscribe = socket.subscribe(listener)
    unsubscribe()

    MockWebSocket.instances[0].onmessage({ data: JSON.stringify({ tick: 1 }) })

    expect(listener).not.toHaveBeenCalled()
  })

  it('sends a message when the socket is open', () => {
    socket.connect('ws://localhost:8000/ws')
    socket.send({ type: 'start' })
    expect(MockWebSocket.instances[0].sent).toEqual([JSON.stringify({ type: 'start' })])
  })

  it('does not send a message when the socket is closed', () => {
    socket.connect('ws://localhost:8000/ws')
    MockWebSocket.instances[0].readyState = MockWebSocket.CLOSED
    socket.send({ type: 'start' })
    expect(MockWebSocket.instances[0].sent).toEqual([])
  })

  it('reconnects with backoff after the socket closes', () => {
    socket.connect('ws://localhost:8000/ws')
    expect(MockWebSocket.instances.length).toBe(1)

    MockWebSocket.instances[0].onclose()
    vi.advanceTimersByTime(1000)

    expect(MockWebSocket.instances.length).toBe(2)
  })

  it('closes the socket on error', () => {
    socket.connect('ws://localhost:8000/ws')
    const instance = MockWebSocket.instances[0]
    const closeSpy = vi.spyOn(instance, 'close')

    instance.onerror()

    expect(closeSpy).toHaveBeenCalled()
  })
})
