PYTHON ?= python3.10
CONFIG ?= config.txt

.PHONY: install run debug clean lint test package

install:
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install build flake8 mypy

run:
	$(PYTHON) a_maze_ing.py $(CONFIG)

debug:
	$(PYTHON) -m pdb a_maze_ing.py $(CONFIG)

clean:
	rm -rf __pycache__ .mypy_cache .pytest_cache build dist *.egg-info
	rm -f maze.txt mazegen-*.tar.gz mazegen-*.whl
	find . -name __pycache__ -type d -prune -exec rm -rf {} +
	find . -name '*.pyc' -type f -delete

lint:
	flake8 .
	mypy . --strict

test:
	$(PYTHON) -m unittest discover -s tests

package:
	$(PYTHON) -m build
	cp dist/mazegen-*.tar.gz .
	cp dist/mazegen-*.whl .
	rm -rf build dist *.egg-info
