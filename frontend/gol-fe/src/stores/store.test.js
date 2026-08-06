import { describe, it, expect, beforeEach, vi } from 'vitest'
import { useSimulationStore } from './store'
import { cantor_calcul } from '../utils/common'

describe('useSimulationStore', () => {
  beforeEach(() => {
    useSimulationStore.setState(useSimulationStore.getInitialState(), true)
  })

  it('has the expected default state', () => {
    const state = useSimulationStore.getState()
    expect(state.generation).toBe(0)
    expect(state.isRunning).toBe(false)
    expect(state.currentGrid.size).toBe(0)
    expect(state.rules).toEqual({ birth: [3], survive: [2, 3] })
  })

  it('setSend stores the send function', () => {
    const send = vi.fn()
    useSimulationStore.getState().setSend(send)
    expect(useSimulationStore.getState().send).toBe(send)
  })

  it('setGeneration and setIsRunning update the state', () => {
    useSimulationStore.getState().setGeneration(5)
    useSimulationStore.getState().setIsRunning(true)
    expect(useSimulationStore.getState().generation).toBe(5)
    expect(useSimulationStore.getState().isRunning).toBe(true)
  })

  it('setNumberCellWidth and setNumberCellHeight update grid dimensions', () => {
    useSimulationStore.getState().setNumberCellWidth(20)
    useSimulationStore.getState().setNumberCellHeight(30)
    expect(useSimulationStore.getState().numberCellWidth).toBe(20)
    expect(useSimulationStore.getState().numberCellHeight).toBe(30)
  })

  it('setFullGrid replaces the grid and sets the generation', () => {
    useSimulationStore.getState().setFullGrid(
      [
        [1, 2],
        [3, 4],
      ],
      7
    )

    const { currentGrid, generation } = useSimulationStore.getState()
    expect(generation).toBe(7)
    expect(currentGrid.size).toBe(2)
    expect(currentGrid.get(cantor_calcul(1, 2))).toEqual({ tick: 7, x: 1, y: 2 })
  })

  it('applyBirthDeath adds born cells and removes dead cells', () => {
    useSimulationStore.getState().setFullGrid([[1, 1]], 1)
    useSimulationStore.getState().applyBirthDeath([[2, 2]], [[1, 1]], 2)

    const { currentGrid, generation } = useSimulationStore.getState()
    expect(generation).toBe(2)
    expect(currentGrid.has(cantor_calcul(1, 1))).toBe(false)
    expect(currentGrid.get(cantor_calcul(2, 2))).toEqual({ tick: 2, x: 2, y: 2 })
  })

  it('resetLocal clears the grid, generation and running state', () => {
    useSimulationStore.getState().setFullGrid([[1, 1]], 3)
    useSimulationStore.getState().setIsRunning(true)

    useSimulationStore.getState().resetLocal()

    const state = useSimulationStore.getState()
    expect(state.currentGrid.size).toBe(0)
    expect(state.generation).toBe(0)
    expect(state.isRunning).toBe(false)
  })

  it('start sends a start message', () => {
    const send = vi.fn()
    useSimulationStore.getState().setSend(send)
    useSimulationStore.getState().start()
    expect(send).toHaveBeenCalledWith({ type: 'start' })
  })

  it('stop sends a stop message', () => {
    const send = vi.fn()
    useSimulationStore.getState().setSend(send)
    useSimulationStore.getState().stop()
    expect(send).toHaveBeenCalledWith({ type: 'stop' })
  })

  it('reset sends a reset message and clears local state', () => {
    const send = vi.fn()
    useSimulationStore.getState().setSend(send)
    useSimulationStore.getState().setFullGrid([[1, 1]], 3)

    useSimulationStore.getState().reset()

    expect(send).toHaveBeenCalledWith({ type: 'reset' })
    expect(useSimulationStore.getState().currentGrid.size).toBe(0)
  })

  it('toggleCell sends a toggle_cell message with coordinates', () => {
    const send = vi.fn()
    useSimulationStore.getState().setSend(send)
    useSimulationStore.getState().toggleCell(4, 5)
    expect(send).toHaveBeenCalledWith({ type: 'toggle_cell', x: 4, y: 5 })
  })

  it('setTickRate sends a set_speed message', () => {
    const send = vi.fn()
    useSimulationStore.getState().setSend(send)
    useSimulationStore.getState().setTickRate(2)
    expect(send).toHaveBeenCalledWith({ type: 'set_speed', speed: 2 })
  })

  it('setGridSize sends a grid_size message', () => {
    const send = vi.fn()
    useSimulationStore.getState().setSend(send)
    useSimulationStore.getState().setGridSize(50, 60)
    expect(send).toHaveBeenCalledWith({ type: 'grid_size', width: 50, height: 60 })
  })

  it('setRules updates the local rules state', () => {
    useSimulationStore.getState().setRules({ birth: [3, 6], survive: [2] })
    expect(useSimulationStore.getState().rules).toEqual({ birth: [3, 6], survive: [2] })
  })

  it('setSimulationRules sends a set_rules message', () => {
    const send = vi.fn()
    useSimulationStore.getState().setSend(send)
    useSimulationStore.getState().setSimulationRules([3], [2, 3])
    expect(send).toHaveBeenCalledWith({ type: 'set_rules', birth: [3], survive: [2, 3] })
  })

  it('does nothing when sending without a registered send function', () => {
    expect(() => useSimulationStore.getState().start()).not.toThrow()
  })
})
