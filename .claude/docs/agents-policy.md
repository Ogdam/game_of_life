# Politique des agents

## Agents autorisés (liste fermée)
coordinateur, back, front, dev-ops, ticket-doc

## Règles strictes
- Interdiction de créer un nouvel agent
- Interdiction de dupliquer un agent existant (même nom modifié)
- Interdiction d'invoquer un agent hors de cette liste
- Toute tâche hors périmètre des 5 agents → traitée par le coordinateur directement, sans délégation

## Répartition
- coordinateur : orchestration, répartition des tâches, pas d'écriture de code
- back : API, BDD, services serveur
- front : UI, composants, state management
- dev-ops : CI/CD, déploiement, infra
- ticket-doc : rédaction tickets, documentation, changelog