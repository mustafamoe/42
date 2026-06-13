install:
	pip install build .
 
run:
	python3 a_maze_ing.py config.txt
 
debug:
	python3 -m pdb a_maze_ing.py config.txt
 
lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
 
lint-strict:
	flake8 .
	mypy . --strict
 
clean:
	rm -rf __pycache__ src/__pycache__ mazegen/__pycache__
	rm -rf .mypy_cache
	rm -rf *.egg-info dist build
 