# Choix Techniques - Game of Life Fullstack

## 1. Format de Grille
**Decision: Coords actives (Array de `[x, y]`)**

```javascript
// Format: Array de coordonnées [x, y]
grid = [
  [1, 0],   // cellule vivante à ligne 1, colonne 0
  [1, 1],   // cellule vivante à ligne 1, colonne 1
  [0, 1]    // cellule vivante à ligne 0, colonne 1
]
```

## 2. État Global (Application State)

```javascript
{
  grid: [[x1, y1], [x2, y2], ...],  // coords actives
  width: 100,                        // dimensions
  height: 100,
  tick: 0,                           // numéro génération
  status: "paused",                  // "running" | "paused"
  speed: 300                         // ms entre générations
}
```

---

## 3. Architecture Frontend (React + TypeScript)

- **Vite** (build tool - plus rapide que CRA)
- **React 18+** (UI)
- **TypeScript** (typage)
- **Zustand** (state management léger)
- **Canvas** (rendu grille, pas DOM)

---

## 4. Architecture Backend (Python)

- **FastAPI** (API REST + WebSocket)
- **Python 3.9+**

---

## 5. Communication Front ↔ Back

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
  "width": 100,
  "height": 100
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

---

## 7. Structure Dossiers

```
game-of-life/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Grid.tsx
│   │   │   └── Controls.tsx
│   │   ├── services/
│   │   │   └── websocket.ts
│   │   ├── store/
│   │   │   └── gameStore.ts (Zustand)
│   │   └── App.tsx
│   ├── vite.config.ts
│   └── package.json
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── engine/
│   │   │   ├── rules.py
│   │   │   └── grid.py
│   │   └── routes/
│   │       └── websocket.py
│   ├── requirements.txt
│   └── Dockerfile
│
└── docker-compose.yml
```

---

## 8. API Endpoints (Backend)

```
POST   /api/reset           → crée grille vide
POST   /api/set_pattern     → place un pattern (Glider, etc)
GET    /api/state           → récupère état courant
WebSocket /ws               → connexion permanente
```

---

## 9. Performance Targets

- Grille max: 200×200
- Tick rate: 50-500ms (configurable)
- Latence WebSocket: <100ms
- Canvas render: 60 FPS

---

## 10. Stack Résumé

| Aspect | Tech |
|--------|------|
| Frontend Build | Vite |
| Frontend UI | React 18 + TypeScript |
| State Mgmt | Zustand |
| Rendering | Canvas API |
| Backend | FastAPI |
| Real-time | WebSocket |
| Containerization | Docker + docker-compose |
| Deployment | (TBD) |

---