# Qualité de code

## Règles strictes
- Fonctions : max 50 lignes, une seule responsabilité
- Fichiers : max 300 lignes (si dépassé, découper en modules)
- Complexité cyclomatique : max 10 (respecter le linter configuré)
- Pas de duplication : si un bloc de logique apparaît 2x, extraire une fonction/util

## Nommage
- Noms explicites, pas d'abréviations obscures (ex: calculateNextGeneration, pas calcNextGen)
- Booléens préfixés is/has/should

## Anti-patterns à éviter
- Pas de sur-abstraction (pas d'interface/factory si un seul cas d'usage existe)
- Pas de commentaires qui répètent le code ("// incrémente i" au-dessus de i++)
- Pas de magic numbers (extraire en constante nommée)

## Avant de coder
- Vérifier si un pattern similaire existe déjà dans le projet et le réutiliser
- Ne pas créer de nouvelle dépendance sans vérifier si une existante peut suffire

## Linters configurés
- Backend : Pylint (backend/pyproject.toml) + Black (backend/pyproject.toml)
- Frontend : [ex. ESLint + Prettier]
- Ces règles viennent en complément du linter, pas en remplacement