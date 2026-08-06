import { describe, it, expect, beforeEach, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import Controls from './controls'
import { useSimulationStore } from '../stores/store'

describe('Controls', () => {
  beforeEach(() => {
    useSimulationStore.setState(useSimulationStore.getInitialState(), true)
  })

  it('calls start when the start button is clicked', () => {
    const send = vi.fn()
    useSimulationStore.getState().setSend(send)
    render(<Controls />)

    fireEvent.click(screen.getByRole('button', { name: /start/i }))

    expect(send).toHaveBeenCalledWith({ type: 'start' })
  })

  it('disables start while running and enables pause', () => {
    useSimulationStore.getState().setIsRunning(true)
    render(<Controls />)

    expect(screen.getByRole('button', { name: /start/i })).toBeDisabled()
    expect(screen.getByRole('button', { name: /pause/i })).toBeEnabled()
  })

  it('calls stop when the pause button is clicked', () => {
    const send = vi.fn()
    useSimulationStore.getState().setSend(send)
    useSimulationStore.getState().setIsRunning(true)
    render(<Controls />)

    fireEvent.click(screen.getByRole('button', { name: /pause/i }))

    expect(send).toHaveBeenCalledWith({ type: 'stop' })
  })

  it('calls reset when the reset button is clicked', () => {
    const send = vi.fn()
    useSimulationStore.getState().setSend(send)
    render(<Controls />)

    fireEvent.click(screen.getByRole('button', { name: /reset/i }))

    expect(send).toHaveBeenCalledWith({ type: 'reset' })
  })

  it('sends a grid_size message when width changes', () => {
    const send = vi.fn()
    useSimulationStore.getState().setSend(send)
    render(<Controls />)

    fireEvent.change(screen.getByPlaceholderText('Width'), { target: { value: '15' } })

    expect(send).toHaveBeenCalledWith({ type: 'grid_size', width: 15, height: 90 })
  })

  it('sends a set_speed message when the speed slider changes', () => {
    const send = vi.fn()
    useSimulationStore.getState().setSend(send)
    render(<Controls />)

    const slider = screen.getByRole('slider')
    fireEvent.change(slider, { target: { value: '2' } })

    expect(send).toHaveBeenCalledWith({ type: 'set_speed', speed: 0.5 })
  })

  it('sends parsed rules when the birth input changes', () => {
    const send = vi.fn()
    useSimulationStore.getState().setSend(send)
    render(<Controls />)

    fireEvent.change(screen.getByPlaceholderText('ex: 3'), { target: { value: '3,6' } })

    expect(send).toHaveBeenCalledWith({ type: 'set_rules', birth: [3, 6], survive: [2, 3] })
  })

  it('sends parsed rules when the survive input changes', () => {
    const send = vi.fn()
    useSimulationStore.getState().setSend(send)
    render(<Controls />)

    fireEvent.change(screen.getByPlaceholderText('ex: 2,3'), { target: { value: '2' } })

    expect(send).toHaveBeenCalledWith({ type: 'set_rules', birth: [3], survive: [2] })
  })

  it('toggles the simulation with the space key', () => {
    const send = vi.fn()
    useSimulationStore.getState().setSend(send)
    render(<Controls />)

    fireEvent.keyDown(window, { code: 'Space' })
    expect(send).toHaveBeenCalledWith({ type: 'start' })

    useSimulationStore.getState().setIsRunning(true)
    fireEvent.keyDown(window, { code: 'Space' })
    expect(send).toHaveBeenCalledWith({ type: 'stop' })
  })

  it('resets the simulation with the r key', () => {
    const send = vi.fn()
    useSimulationStore.getState().setSend(send)
    render(<Controls />)

    fireEvent.keyDown(window, { key: 'r' })

    expect(send).toHaveBeenCalledWith({ type: 'reset' })
  })
})
