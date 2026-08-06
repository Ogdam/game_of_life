# Règles Git

## Branches
- Format : type/XXX-description-courte
- Exemple : feat/012-persistance-simulations, fix/027-bug-collision
- Types : feat, fix, chore, refactor, docs, test
- Une branche par ticket, jamais de commit direct sur main/develop
- Le numéro de ticket est obligatoire (récupéré via gh issue list si non fourni)

## Commits (Conventional Commits)
- Format : [#XX] description courte
- Exemple : [#12] ajoute la persistance des sauvegardes
- Un commit = une intention logique unique
- Corps optionnel si la modif est complexe
- #12 (numéro d'issue GitHub) ferme automatiquement le ticket au merge sur main

## Sous-tickets
- Un plan multi-étapes se découpe en sous-issues GitHub
- Chaque sous-issue référence le ticket parent : "Sous-tâche de #XX"
- Le ticket parent reste ouvert jusqu'à ce que toutes les sous-tâches soient fermées
- Nommage des branches : type/XX-etape (garder le numéro du sous-ticket, pas du parent)

## Pull Request
- Titre = résumé du scope
- Description = liste des changements + lien ticket
- Revue obligatoire avant merge

## Répartition des actions Git
- Créer branche / commit / push : agent responsable de la tâche (back, front, dev-ops)
- Pull Request : dev-ops
- Merge sur main/develop : validation manuelle obligatoire, jamais automatique
- Tags de release : dev-ops uniquement