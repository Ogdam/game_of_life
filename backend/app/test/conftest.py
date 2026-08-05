import sys
from pathlib import Path

# Les modules sous app/ (ex: engine/session_manager.py) importent leurs
# dépendances via `from app.xxx import ...` (convention du projet). Il faut
# donc que `backend/` soit sur sys.path en plus de `app/` (déjà ajouté par
# pytest via app/test/__init__.py) pour que ces imports absolus résolvent.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
