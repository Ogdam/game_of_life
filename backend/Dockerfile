FROM python:3.11-slim

WORKDIR /backend

# Copie et installation des dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du reste du code
COPY ./app ./app
COPY ./alembic ./alembic
COPY alembic.ini .

# FastAPI tourne par défaut sur le port 8000
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]