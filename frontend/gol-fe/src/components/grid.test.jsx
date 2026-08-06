import { describe, it, expect, beforeEach, vi } from 'vitest'
import { render, act } from '@testing-library/react'
import { useSimulationStore } from '../stores/store'

class MockGraphics {
  constructor() {
    this.x = 0
    this.y = 0
    this.destroy = vi.fn()
    this.clear = vi.fn(() => this)
    this.rect = vi.fn(() => this)
    this.fill = vi.fn(() => this)
  }
}

const applicationInstances = []

class MockApplication {
  constructor() {
    this.canvas = document.createElement('canvas')
    this.screen = {}
    this.stage = {
      eventMode: null,
      hitArea: null,
      on: vi.fn(),
      addChild: vi.fn(),
      removeChild: vi.fn(),
    }
    applicationInstances.push(this)
  }
  async init(options) {
    this.width = options.width
    this.height = options.height
  }
  destroy() {}
}

vi.mock('pixi.js', () => ({
  Application: MockApplication,
  Graphics: MockGraphics,
}))

const { default: Grid } = await import('./grid')

async function renderGrid(props = {}) {
  let utils
  await act(async () => {
    utils = render(<Grid gridWidth={100} gridHeight={100} {...props} />)
  })
  return utils
}

function getPointerDownHandler() {
  const app = applicationInstances.at(-1)
  const call = app.stage.on.mock.calls.find(([event]) => event === 'pointerdown')
  return call[1]
}

describe('Grid', () => {
  beforeEach(() => {
    applicationInstances.length = 0
    useSimulationStore.setState(useSimulationStore.getInitialState(), true)
  })

  it('mounts the pixi canvas into the container', async () => {
    const { container } = await renderGrid()
    expect(container.querySelector('canvas')).toBeTruthy()
    expect(applicationInstances).toHaveLength(1)
  })

  it('toggles the cell under the pointer using the current cell size', async () => {
    useSimulationStore.getState().setNumberCellWidth(10)
    useSimulationStore.getState().setNumberCellHeight(10)
    const toggleCell = vi.fn()
    useSimulationStore.setState({ toggleCell })

    await renderGrid()
    const handler = getPointerDownHandler()

    handler({ global: { x: 35, y: 12 } })

    expect(toggleCell).toHaveBeenCalledWith(3, 1)
  })

  it('creates and fills a graphics object for each cell in the store', async () => {
    useSimulationStore.getState().setNumberCellWidth(10)
    useSimulationStore.getState().setNumberCellHeight(10)

    await renderGrid()

    await act(async () => {
      useSimulationStore.getState().setFullGrid([[1, 1]], 1)
    })

    const app = applicationInstances.at(-1)
    expect(app.stage.addChild).toHaveBeenCalledTimes(1)
    const cell = app.stage.addChild.mock.calls[0][0]
    expect(cell.fill).toHaveBeenCalled()
    expect(cell.x).toBe(10)
    expect(cell.y).toBe(10)
  })

  it('removes graphics for cells that disappeared from the store', async () => {
    await renderGrid()

    await act(async () => {
      useSimulationStore.getState().setFullGrid([[1, 1]], 1)
    })

    const app = applicationInstances.at(-1)
    const cell = app.stage.addChild.mock.calls[0][0]

    await act(async () => {
      useSimulationStore.getState().applyBirthDeath([], [[1, 1]], 2)
    })

    expect(app.stage.removeChild).toHaveBeenCalledWith(cell)
    expect(cell.destroy).toHaveBeenCalled()
  })

  it('destroys the pixi application on unmount', async () => {
    const { unmount } = await renderGrid()
    const app = applicationInstances.at(-1)
    const destroySpy = vi.spyOn(app, 'destroy')

    unmount()

    expect(destroySpy).toHaveBeenCalled()
  })
})
