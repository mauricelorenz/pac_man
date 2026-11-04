PYTHON = python3
MAIN = pac-man.py
SRC = src
CONFIG = config.json

install:
	uv sync

run:
	uv run $(PYTHON) $(MAIN) $(CONFIG)

debug:
	uv run $(PYTHON) -m pdb $(MAIN) $(CONFIG)

clean:
	find . -type d -name "__pycache__" -not -path "./.venv/*" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -not -path "./.venv/*" -exec rm -rf {} +
	find . -name "*.pyc" -not -path "./.venv/*" -delete

lint:
	uv run flake8 $(SRC) $(MAIN)
	uv run mypy $(SRC) $(MAIN) --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	uv run flake8 $(SRC) $(MAIN)
	uv run mypy $(SRC) $(MAIN) --strict

.PHONY: install run debug clean lint lint-strict
