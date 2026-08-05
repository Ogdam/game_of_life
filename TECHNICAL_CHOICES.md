
// Format: Array de coordonnées [x, y]
grid = [
  [1, 0],   // cellule vivante à ligne 1, colonne 0
  [1, 1],   // cellule vivante à ligne 1, colonne 1
  [0, 1]    // cellule vivante à ligne 0, colonne 1
]

- **Vite** (build tool - plus rapide que CRA)
- **React 19+** (UI)
- **JavaScript** (JSX, pas de typage statique — ESLint + Prettier pour la qualité)
- **Zustand** (state management léger)
- **Canvas** (rendu grille, pas DOM)

- **FastAPI** (API REST + WebSocket)
- **Python 3.9+**


## Communication Front ↔ Back

**WebSocket messages:**

```json
// Client → Server
{"type": "start"}
{"type": "stop"}
{"type": "reset"}
{"type": "toggle_cell", "x": 5, "y": 10}
{"type": "set_speed", "speed": 200}
{"type": "grid_size", "width": 90, "height": 90}
{"type": "next_step"}

// Server → Client (broadcast après chaque message reçu, pas d'enveloppe "type")
{
  "status": "running",
  "tick": 42,
  "grid": {
    "width": 90,
    "height": 90,
    "grid": [[1, 0], [1, 1]]
  }
}
```

## API REST

**GET /status** — état global du serveur (connexions et sessions en cours) :

```json
{
  "active_connections": 3,
  "active_sessions": 3,
  "running_sessions": 1,
  "paused_sessions": 2
}
```