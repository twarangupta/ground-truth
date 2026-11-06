# GroundTruth task runner. Run `make help` to list targets.
# Recipes avoid shell-specific syntax so they work in cmd.exe (Windows) and sh (Linux CI).

.DEFAULT_GOAL := help
.PHONY: help setup env db-up db-down db-logs dev test test-integration lint format typecheck check

COMPOSE := docker compose -f infra/docker-compose.yml --env-file .env

help:
	@echo Targets:
	@echo   setup             create .env from .env.example if missing, install Python deps
	@echo   db-up             start Postgres + pgvector and wait until healthy
	@echo   db-down           stop Postgres, data is kept in a Docker volume
	@echo   db-logs           show Postgres logs
	@echo   dev               start Postgres, then the API with auto-reload on port 8000
	@echo   test              unit tests, no database needed
	@echo   test-integration  tests against the real Postgres, run db-up first
	@echo   lint              ruff lint and format check
	@echo   format            auto-format with ruff
	@echo   typecheck         mypy strict type check
	@echo   check             lint + typecheck + unit tests, same as CI
	@echo Note: echo text avoids parentheses and quotes so it works in both cmd.exe and sh.

setup: env
	cd api && uv sync

# Copy .env.example to .env only if .env does not exist yet. Python keeps this cross-platform.
env:
	uv run --no-project python -c "import pathlib, shutil; p = pathlib.Path('.env'); p.exists() or shutil.copy('.env.example', p)"

db-up: env
	$(COMPOSE) up -d --wait

db-down:
	$(COMPOSE) down

db-logs:
	$(COMPOSE) logs postgres

dev: db-up
	cd api && uv run uvicorn groundtruth.main:app --reload --port 8000

test:
	cd api && uv run pytest -m "not integration"

test-integration:
	cd api && uv run pytest -m integration

lint:
	cd api && uv run ruff check . && uv run ruff format --check .

format:
	cd api && uv run ruff format . && uv run ruff check --fix .

typecheck:
	cd api && uv run mypy

check: lint typecheck test
