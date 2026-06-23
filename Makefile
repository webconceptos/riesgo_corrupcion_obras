.PHONY: venv install lint test serve fmt

venv:
	python -m venv .venv

install:
	pip install --upgrade pip wheel
	pip install -r requirements.txt
	[ -f requirements-dev.txt ] && pip install -r requirements-dev.txt || true

lint:
	ruff check .

fmt:
	ruff format .

test:
	PYTHONPATH=. pytest -q

serve:
	uvicorn src.api.main:app --reload --port 8000

all: install serve
