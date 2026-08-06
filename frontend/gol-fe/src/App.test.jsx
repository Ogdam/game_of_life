import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'

const connect = vi.fn()
const send = vi.fn()

vi.mock('./hooks/socket', () => ({
  socket: { connect, send },
}))

vi.mock('./stores/subscribe', () => ({
  default: vi.fn(),
}))

vi.mock('./components/grid', () => ({
  default: () => <div data-testid="grid-stub" />,
}))

const { default: App } = await import('./App')

describe('App', () => {
  it('connects the socket and registers the send function on load', () => {
    const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    expect(connect).toHaveBeenCalledWith(`${wsProtocol}//${window.location.host}/ws`)
  })

  it('renders the sidebar and the grid', () => {
    render(<App />)
    expect(screen.getByText('Cornwell Game Of Life')).toBeInTheDocument()
    expect(screen.getByTestId('grid-stub')).toBeInTheDocument()
  })
})
