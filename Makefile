SHELL := /bin/bash
PROJECT_NAME := lyvia-backend

POETRY := ~/.local/bin/poetry

launch:
	@poetry run python main.py

install:
	@poetry install
	@poetry run mypy --install-types

format:
	@poetry run autoflake --in-place --remove-all-unused-imports --recursive --remove-unused-variables \
		--ignore-init-module-imports lyvia_backend
	@poetry run isort lyvia_backend
	@poetry run black lyvia_backend
	@poetry run autoflake --in-place --remove-all-unused-imports --recursive --remove-unused-variables \
		--ignore-init-module-imports tests
	@poetry run isort tests
	@poetry run black tests

type-check:
	@poetry run mypy lyvia_backend
	@poetry run mypy tests

lint:
	@poetry run pylint lyvia_backend
	@poetry run pylint tests
	@poetry run bandit -r lyvia_backend
	@poetry run bandit -r tests

test-db:
	@poetry run pytest tests/db