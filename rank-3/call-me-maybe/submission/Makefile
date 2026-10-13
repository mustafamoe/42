GOINFRE ?= $(if $(wildcard /goinfre),/goinfre/$(shell id -un)/call-me-maybe)

ifneq ($(strip $(GOINFRE)),)
export UV_CACHE_DIR := $(GOINFRE)/uv-cache
export UV_PYTHON_INSTALL_DIR := $(GOINFRE)/python
export HF_HOME := $(GOINFRE)/huggingface
endif

.PHONY: install run debug clean lint storage

install: storage
	uv sync

run: storage
	uv run python -m src

debug: storage
	uv run python -m pdb -m src

clean:
	find src -type d -name __pycache__ -prune -exec rm -rf {} +
	rm -rf .mypy_cache

lint: storage
	uv run flake8 .
	uv run mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

storage:
ifneq ($(strip $(GOINFRE)),)
	@set -eu; \
	root="$(GOINFRE)"; \
	case "$$root" in /*) ;; *) echo "GOINFRE must be an absolute path" >&2; exit 1;; esac; \
	mkdir -p "$$root"; \
	root=$$(cd "$$root" && pwd -P); \
	if [ "$$root" = "$$(pwd -P)" ]; then \
		echo "GOINFRE must differ from the project directory; use GOINFRE= to keep files here." >&2; exit 1; \
	fi; \
	for path in .venv model data/output; do \
		target="$$root/$${path##*/}"; \
		if [ -L "$$path" ] && [ "$$(readlink "$$path")" = "$$target" ]; then continue; fi; \
		if [ -L "$$path" ] || { [ -e "$$path" ] && [ ! -d "$$path" ]; }; then \
			echo "Expected a directory, refusing to move: $$path" >&2; exit 1; \
		fi; \
		if [ -e "$$target" ] || [ -L "$$target" ]; then \
			echo "Storage already exists: $$target. Use a different GOINFRE for this checkout." >&2; exit 1; \
		fi; \
	done; \
	for path in .venv model data/output; do \
		target="$$root/$${path##*/}"; \
		if [ -L "$$path" ]; then mkdir -p "$$target"; continue; fi; \
		if [ -e "$$path" ]; then mv "$$path" "$$target"; \
		else mkdir -p "$$target"; fi; \
		mkdir -p "$$(dirname "$$path")"; \
		ln -s "$$target" "$$path"; \
	done; \
	echo "Storage: $$root"
else
	@:
endif
