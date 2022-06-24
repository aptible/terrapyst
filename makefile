SHELL := /bin/bash
PYTHON := . .venv/bin/activate && python

.venv:
	python -m venv .venv

install: .venv
	$(PYTHON) -m pip install -e .[dev]

pretty:
	$(PYTHON) -m black . && \
	isort .

.PHONY: tests
tests: install pytest isort_check black_check mypy_check

pytest:
	$(PYTHON) -m pytest --cov=./terrapyst --cov-report=term-missing tests

pytest_loud:
	$(PYTHON) -m pytest -s --cov=./terrapyst --cov-report=term-missing tests

isort_check:
	$(PYTHON) -m isort --check-only .

black_check:
	$(PYTHON) -m black . --check

mypy_check:
	$(PYTHON) -m mypy terrapyst