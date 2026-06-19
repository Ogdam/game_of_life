
// Format: Array de coordonnées [x, y]
grid = [
  [1, 0],   // cellule vivante à ligne 1, colonne 0
  [1, 1],   // cellule vivante à ligne 1, colonne 1
  [0, 1]    // cellule vivante à ligne 0, colonne 1
]

- **Vite** (build tool - plus rapide que CRA)
- **React 18+** (UI)
- **TypeScript** (typage)
- **Zustand** (state management léger)
- **Canvas** (rendu grille, pas DOM)

- **FastAPI** (API REST + WebSocket)
- **Python 3.9+**


## Communication Front ↔ Back

**WebSocket messages:**

```json
// Client → Server
{"type": "start"}
{"type": "pause"}
{"type": "reset"}
{"type": "toggle_cell", "x": 5, "y": 10}
{"type": "set_speed", "speed": 200}

// Server → Client (broadcast)
{"type": "grid_update", "grid": [[1,0], [1,1]]}
{"type": "tick", "value": 42}
```

---

## 6. JSON Contract (IMPORTANT)

### Request body pour REST
```json
{
  "grid": [[1,0], [1,1], [0,1]],
  "width": 90,
  "height": 90
}
```

### Response body
```json
{
  "success": true,
  "data": {
    "grid": [[1,0], [1,1], [0,1]],
    "tick": 5,
    "status": "running"
  }
}
```