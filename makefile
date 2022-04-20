SHELL := /bin/bash

.env:
	python -m venv .env

install: .env
	source .env/bin/activate && python -m pip install -e .[dev]

pretty:
	. .env/bin/activate && \
	python -m black . && \
	isort .

.PHONY: tests
tests: install pytest isort_check black_check

pytest:
	. .env/bin/activate && \
	python -m pytest --cov=./terrapy --cov-report=term-missing tests

pytest_loud:
	. .env/bin/activate && \
	python -m pytest -s --cov=./terrapy --cov-report=term-missing tests

isort_check:
	. .env/bin/activate && \
	python -m isort --check-only .

black_check:
	. .env/bin/activate && \
	python -m black . --check
