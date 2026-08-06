.PHONY: lint format format-check test migrate

lint:
	PYTHONPATH=.:app pylint app

format:
	black .

format-check:
	black --check .

test:
	cd app && pytest

migrate:
	alembic upgrade head
