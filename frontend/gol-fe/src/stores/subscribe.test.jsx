import { describe, it, expect, beforeEach, vi } from 'vitest'

const listeners = []

vi.mock('../hooks/socket', () => ({
  socket: {
    subscribe: (fn) => listeners.push(fn),
  },
}))

import initSocketBridge from './subscribe'
import { useSimulationStore } from './store'
import { cantor_calcul } from '../utils/common'

function emit(message) {
  listeners[0](message)
}

describe('initSocketBridge', () => {
  beforeEach(() => {
    useSimulationStore.setState(useSimulationStore.getInitialState(), true)
    listeners.length = 0
    initSocketBridge()
  })

  it('updates generation and running status from a message', () => {
    emit({ tick: 5, status: 'running', grid: { grid: [] } })

    const state = useSimulationStore.getState()
    expect(state.generation).toBe(5)
    expect(state.isRunning).toBe(true)
  })

  it('defaults the generation to 0 when tick is missing', () => {
    emit({ status: 'stopped', grid: { grid: [] } })
    expect(useSimulationStore.getState().generation).toBe(0)
  })

  it('applies a full grid update when no birth/death diff is present', () => {
    emit({ tick: 2, grid: { grid: [[1, 1]], width: 10, height: 20 } })

    const state = useSimulationStore.getState()
    expect(state.currentGrid.size).toBe(1)
    expect(state.numberCellWidth).toBe(10)
    expect(state.numberCellHeight).toBe(20)
  })

  it('applies a birth/death diff when present', () => {
    emit({ tick: 1, grid: { grid: [[1, 1]], width: 10, height: 10 } })
    emit({ tick: 2, grid: { birth: [[2, 2]], death: [[1, 1]] } })

    const state = useSimulationStore.getState()
    expect(state.currentGrid.has(cantor_calcul(1, 1))).toBe(false)
    expect(state.currentGrid.has(cantor_calcul(2, 2))).toBe(true)
    expect(state.generation).toBe(2)
  })

  it('updates the rules when present in the message', () => {
    emit({ tick: 1, grid: { grid: [] }, rules: { birth: [3, 6], survive: [2] } })
    expect(useSimulationStore.getState().rules).toEqual({ birth: [3, 6], survive: [2] })
  })

  it('leaves rules untouched when absent from the message', () => {
    emit({ tick: 1, grid: { grid: [] } })
    expect(useSimulationStore.getState().rules).toEqual({ birth: [3], survive: [2, 3] })
  })
})
