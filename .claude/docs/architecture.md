# Objectif du projet

Créer une application web permettant aux utilisateurs de jouer au Jeu de la Vie de Conway avec des fonctionnalités avancées de personnalisation. L'utilisateur peut modifier les règles de simulation (conditions de naissance, survie et mort des cellules), placer des formes préconstruites et sauvegarder sa progression afin de reprendre une simulation ultérieurement. Le projet sépare la logique métier dans un backend dédié et l'affichage dans un frontend interactif.

# Contraintes métier

* L'utilisateur doit pouvoir retrouver ses simulations après reconnexion.
* Les règles de simulation doivent être configurables dynamiquement.
* Les formes préconstruites doivent pouvoir être ajoutées facilement.
* La logique du jeu doit rester indépendante de l'affichage.
* L'interface doit permettre une visualisation fluide des simulations.
* Les performances doivent permettre la gestion d'un grand nombre de cellules.

# Décisions d'architecture (ADR courtes)

* [2026-08-05] Séparation Frontend / Backend : choix d'une architecture découplée afin de séparer la logique métier du rendu graphique et faciliter l'évolution indépendante des deux parties.

* [2026-08-05] Backend responsable de la simulation : choix de centraliser les calculs du Jeu de la Vie dans le backend afin d'avoir une source unique de vérité pour les règles métier.

* [2026-08-05] Frontend dédié au rendu : choix de gérer uniquement l'affichage et les interactions utilisateur côté frontend afin de maintenir une séparation claire des responsabilités.

* [2026-08-05] Persistance des simulations utilisateur : choix de sauvegarder l'état des parties pour permettre une reprise de session après reconnexion.

# Contrats d'interface Front ↔ Back

## Format de la grille

```
// Format: Array de coordonnées [x, y]
grid = [
  [1, 0],   // cellule vivante à ligne 1, colonne 0
  [1, 1],   // cellule vivante à ligne 1, colonne 1
  [0, 1]    // cellule vivante à ligne 0, colonne 1
]
```

## Messages WebSocket

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

## API REST — GET /status

```json
{
  "active_connections": 3,
  "active_sessions": 3,
  "running_sessions": 1,
  "paused_sessions": 2
}
```
