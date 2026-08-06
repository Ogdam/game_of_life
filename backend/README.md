# Backend

## Development

Créer un environnement virtuel et installer les dépendances de développement :

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

Commandes disponibles :

```bash
make lint           # Pylint
make format          # Black (reformate)
make format-check    # Black (vérification sans modification)
make test            # pytest
```
