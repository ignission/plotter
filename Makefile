.PHONY: all clean test card wedge drawer format lint help

PYTHON := uv run python
BUILD_DIR := build

help:
	@echo "PLOTTER build targets:"
	@echo "  make all       - Build all parts (cards + wedge + drawer)"
	@echo "  make card      - Build all card variants"
	@echo "  make wedge     - Build wedge body"
	@echo "  make drawer    - Build drawer"
	@echo "  make test      - Run pytest"
	@echo "  make format    - Format code with ruff"
	@echo "  make lint      - Lint code with ruff"
	@echo "  make clean     - Remove build artifacts"

all: card wedge drawer

card: $(BUILD_DIR)
	$(PYTHON) parts/card_standard.py
	$(PYTHON) parts/card_wide.py
	$(PYTHON) parts/card_thickness_test.py

wedge: $(BUILD_DIR)
	$(PYTHON) parts/wedge.py

drawer: $(BUILD_DIR)
	$(PYTHON) parts/drawer.py

test:
	uv run pytest

format:
	uv run ruff format src/ parts/ tests/ assemblies/

lint:
	uv run ruff check src/ parts/ tests/ assemblies/

clean:
	rm -rf $(BUILD_DIR)/*.stl $(BUILD_DIR)/*.step $(BUILD_DIR)/*.3mf

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)
