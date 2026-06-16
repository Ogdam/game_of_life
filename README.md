# Todo – Game of Life Fullstack (React + Python)

## 1. Refactor du projet actuel (JS pur)
- [ ] Séparer la logique du moteur de simulation
  - [ ] `engine/rules.js` → calcule uniquement la prochaine génération
  - [ ] `engine/grid.js` → gestion de la grille
- [ ] Séparer le rendu
  - [ ] `render/canvas.js` → affichage uniquement
- [ ] Séparer l’UI
  - [ ] `ui/controls.js` → play/pause, vitesse, reset
- [ ] Supprimer toute logique couplée DOM + simulation

---

## 2. Définir le contrat de données (IMPORTANT)
- [x] Définir format de grille
- [x] Définir format d’état global :
  - [x] grid
  - [x] tick
  - [x] status (running/paused)
  - [x] speed
- [x] Standardiser JSON pour communication front/back

---

## 3. Backend Python (FastAPI)
- [x] Initialiser projet FastAPI
- [x] Créer module de simulation
  - [x] fonction `next_generation(grid)`
- [x] Créer état serveur
  - [x] grille courante
  - [x] tick counter
- [x] Implémenter boucle de simulation
  - [x] tick automatique (sleep interval)
- [ ] Ajouter API REST
  - [ ] `POST /start`
  - [ ] `POST /pause`
  - [ ] `POST /reset`
  - [ ] `POST /set_speed`
- [ ] Ajouter WebSocket
  - [ ] broadcast état grille
  - [ ] réception actions client

---

## 4. Frontend React (TypeScript recommandé)
- [ ] Initialiser projet Vite + React
- [ ] Créer composant `Grid`
  - [ ] rendu canvas
  - [ ] affichage optimisé
- [ ] Créer `Controls`
  - [ ] play / pause
  - [ ] reset
  - [ ] speed slider
- [ ] Créer service WebSocket
  - [ ] connexion backend
  - [ ] réception `grid_update`
  - [ ] envoi actions utilisateur
- [ ] State management (Zustand ou Redux léger)
  - [ ] état simulation
  - [ ] état UI

---

## 5. Communication Front ↔ Back
- [ ] Définir messages WebSocket
  - [ ] `grid_update`
  - [ ] `toggle_cell`
  - [ ] `start`
  - [ ] `pause`
- [ ] Implémenter sync initial (snapshot complet)
- [ ] Gérer reconnexion WebSocket

---

## 6. Rendu & performance
- [ ] Optimiser canvas rendering
- [ ] Éviter re-render React inutile
- [ ] Gérer grille large (performance test)
- [ ] Option : Web Workers côté front (optionnel)

---

## 7. Fonctionnalités produit
- [ ] Click pour activer/désactiver cellules
- [ ] Presets (glider, oscillator, etc.)
- [ ] Reset grille
- [ ] Ajuster vitesse simulation
- [ ] Pause / resume

---

## 8. (Bonus) Fonctionnalités avancées
- [ ] Multi-user session (rooms WebSocket)
- [ ] Historique des générations (replay)
- [ ] Export / import de grille (JSON)
- [ ] Diff update (ne pas envoyer toute la grille)
- [ ] Sauvegarde côté backend

---

## 9. Infra & qualité projet
- [ ] Docker backend
- [ ] Docker frontend
- [ ] docker-compose global
- [ ] Lint frontend (ESLint)
- [ ] Format (Prettier)
- [ ] Tests backend (pytest)
- [ ] Tests engine simulation
- [ ] GitHub Actions CI

---

## 10. Finalisation GitHub (important pour ton objectif)
- [ ] README structuré
  - [ ] architecture
  - [ ] démo GIF
  - [ ] setup local
- [ ] Screenshots UI
- [ ] Schéma architecture (simple diagram)
- [ ] Démo live (optionnel mais très fort)