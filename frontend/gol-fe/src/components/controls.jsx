import './controls.css'
import { useState, useEffect } from 'react'
import { useSimulationStore } from '../stores/store'

function parseRuleInput(value) {
  return value.split(',').map(Number).filter(Number.isInteger)
}

function Controls() {
  const start = useSimulationStore((s) => s.start)
  const stop = useSimulationStore((s) => s.stop)
  const reset = useSimulationStore((s) => s.reset)
  const isRunning = useSimulationStore((s) => s.isRunning)
  const setGridSize = useSimulationStore((s) => s.setGridSize)
  const setTickRate = useSimulationStore((s) => s.setTickRate)
  const numberCellWidth = useSimulationStore((s) => s.numberCellWidth)
  const numberCellHeight = useSimulationStore((s) => s.numberCellHeight)
  const rules = useSimulationStore((s) => s.rules)
  const setSimulationRules = useSimulationStore((s) => s.setSimulationRules)

  const [width, setWidth] = useState(numberCellWidth)
  const [height, setHeight] = useState(numberCellHeight)
  const [speed, setSpeed] = useState(1)
  const [birthInput, setBirthInput] = useState(rules.birth.join(','))
  const [surviveInput, setSurviveInput] = useState(rules.survive.join(','))

  useEffect(() => {
    const onKeyDown = (e) => {
      if (e.code !== 'Space') return

      e.preventDefault()

      const { isRunning, start, stop } = useSimulationStore.getState()
      if (isRunning) stop()
      else start()
    }

    window.addEventListener('keydown', onKeyDown)
    return () => window.removeEventListener('keydown', onKeyDown)
  }, [])

  useEffect(() => {
    const onKeyDown = (e) => {
      if (e.key.toLowerCase() === 'r') {
        e.preventDefault()
        const { reset } = useSimulationStore.getState()
        reset()
      }
    }

    window.addEventListener('keydown', onKeyDown)
    return () => window.removeEventListener('keydown', onKeyDown)
  }, [reset])

  return (
    <div className="d-flex flex-column gap-4 p-2">
      {/* 1. PLAY CONTROLS */}
      <div className="d-flex flex-column gap-2">
        <button className="btn btn-success" onClick={start} disabled={isRunning}>
          <i className="bi bi-play-fill"></i> Start
        </button>

        <button className="btn btn-warning" onClick={stop} disabled={!isRunning}>
          <i className="bi bi-pause-fill"></i> Pause
        </button>

        <button className="btn btn-danger" onClick={reset}>
          <i className="bi bi-arrow-counterclockwise"></i> Reset
        </button>
      </div>

      {/* 2. GRID SIZE */}
      <div className="d-flex flex-row gap-2">
        <input
          type="number"
          className="form-control"
          value={width}
          onChange={(e) => {
            setWidth(Number(e.target.value))
            setGridSize(Number(e.target.value), height)
          }}
          placeholder="Width"
        />

        <input
          type="number"
          className="form-control"
          value={height}
          onChange={(e) => {
            setHeight(Number(e.target.value))
            setGridSize(width, Number(e.target.value))
          }}
          placeholder="Height"
        />
      </div>

      {/* 3. SPEED */}
      <div className="d-flex flex-column gap-2">
        <label className="form-label">
          {(1 / speed).toFixed(2)} tick per second ({speed.toFixed(1)})
        </label>

        <input
          type="range"
          min="0.5"
          max="3"
          step="0.1"
          value={speed}
          onChange={(e) => {
            setSpeed(Number(e.target.value))
            setTickRate(1 / Number(e.target.value))
          }}
        />
      </div>

      {/* 4. RULES */}
      <div className="d-flex flex-column gap-2">
        <label className="form-label">Naissance (voisins)</label>
        <input
          type="text"
          className="form-control"
          value={birthInput}
          onChange={(e) => {
            setBirthInput(e.target.value)
            setSimulationRules(parseRuleInput(e.target.value), parseRuleInput(surviveInput))
          }}
          placeholder="ex: 3"
        />

        <label className="form-label">Survie (voisins)</label>
        <input
          type="text"
          className="form-control"
          value={surviveInput}
          onChange={(e) => {
            setSurviveInput(e.target.value)
            setSimulationRules(parseRuleInput(birthInput), parseRuleInput(e.target.value))
          }}
          placeholder="ex: 2,3"
        />
      </div>
    </div>
  )
}

export default Controls
