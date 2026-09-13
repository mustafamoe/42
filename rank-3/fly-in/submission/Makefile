PYTHON := python3.10
MAP ?= map.txt

.PHONY: install run debug clean lint

install:
	$(PYTHON) -m pip install flake8 mypy

run:
	$(PYTHON) fly_in.py $(MAP)

debug:
	$(PYTHON) -m pdb fly_in.py $(MAP)

clean:
	find . -type d \( -name __pycache__ -o -name .mypy_cache \) \
		-prune -exec rm -rf {} +
	find . -type f \( -name '*.pyc' -o -name '*.pyo' \) -delete

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
