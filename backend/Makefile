.PHONY: lint format format-check test migrate

lint:
	PYTHONPATH=.:app pylint app

format:
	black .

format-check:
	black --check .

test:
	PYTHONPATH=.:app pytest app --cov=app --cov-report=term-missing

migrate:
	alembic upgrade head
