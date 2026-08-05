'use client'

import { useEffect, useRef } from 'react'
import { Application, Graphics } from 'pixi.js'
import { getCellColor } from '../utils/common'
import { useSimulationStore } from '../stores/store'

export default function Grid(props) {
  const toggleCell = useSimulationStore((s) => s.toggleCell)
  const currentGrid = useSimulationStore((s) => s.currentGrid)
  const generation = useSimulationStore((s) => s.generation)
  const numberCellHeight = useSimulationStore((s) => s.numberCellHeight)
  const numberCellWidth = useSimulationStore((s) => s.numberCellWidth)

  const containerRef = useRef(null)
  const appRef = useRef(null)
  const renderedCells = useRef(new Map())

  // 1. Calcul des dimensions actuelles
  const cellHeight = props.gridHeight / numberCellHeight
  const cellWidth = props.gridWidth / numberCellWidth

  // 2. Stockage des dimensions dans des refs pour qu'elles soient accessibles partout sans closure obsolète
  const cellDimensionsRef = useRef({ cellWidth, cellHeight })

  // On met à jour les refs à chaque rendu pour qu'elles soient toujours clean
  useEffect(() => {
    cellDimensionsRef.current = { cellWidth, cellHeight }
  }, [cellWidth, cellHeight])

  // INIT ONCE
  useEffect(() => {
    let isDestroyed = false

    ;(async () => {
      const app = new Application()

      await app.init({
        width: props.gridWidth,
        height: props.gridHeight,
        background: '#222',
      })

      if (isDestroyed) {
        app.destroy(true, { children: true, texture: true, context: true })
        return
      }

      app.stage.eventMode = 'static'
      app.stage.hitArea = app.screen

      appRef.current = app
      containerRef.current?.appendChild(app.canvas)

      app.stage.on('pointerdown', (event) => {
        const pos = event.global

        // 3. On utilise les valeurs de la ref ici !
        const currentWidth = cellDimensionsRef.current.cellWidth
        const currentHeight = cellDimensionsRef.current.cellHeight

        const x = Math.floor(pos.x / currentWidth)
        const y = Math.floor(pos.y / currentHeight)
        toggleCell(x, y)
      })
    })()

    return () => {
      isDestroyed = true

      if (appRef.current) {
        appRef.current.destroy(true, {
          children: true,
          texture: true,
          context: true,
        })
        appRef.current = null
      }
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []) // On garde le tableau vide pour ne pas recréer l'application Pixi

  // RENDER / UPDATE CELLS
  useEffect(() => {
    const app = appRef.current
    if (!app) return

    const map = renderedCells.current

    // ADD / UPDATE
    for (const [id, data] of currentGrid) {
      let cell = map.get(id)

      if (!cell) {
        cell = new Graphics()
        map.set(id, cell)
        app.stage.addChild(cell)
      }

      // On redessine et repositionne avec les tailles actuelles
      cell.clear()
      cell.rect(0, 0, cellWidth, cellHeight)
      cell.x = data.x * cellWidth
      cell.y = data.y * cellHeight
      cell.fill(getCellColor(generation, data.tick))
    }

    // REMOVE
    for (const [id, cell] of map.entries()) {
      if (currentGrid.has(id)) continue

      app.stage.removeChild(cell)
      cell.destroy()
      map.delete(id)
    }

    // 4. On ajoute cellWidth et cellHeight aux dépendances pour redessiner la grille si la taille change
  }, [currentGrid, generation, cellWidth, cellHeight])

  return <div ref={containerRef} />
}
