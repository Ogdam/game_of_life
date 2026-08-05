.PHONY: lint format format-check test

lint:
	PYTHONPATH=.:app pylint app

format:
	black .

format-check:
	black --check .

test:
	cd app && pytest
