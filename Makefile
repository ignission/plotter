.PHONY: all clean test card wedge drawer wedge-test drawer-test test-set format lint help

PYTHON := uv run python
BUILD_DIR := build

help:
	@echo "PLOTTER build targets:"
	@echo "  make all          - Build full-size parts (cards + wedge + drawer)"
	@echo "  make card         - Build all card variants"
	@echo "  make wedge        - Build full-size wedge body"
	@echo "  make drawer       - Build full-size drawer"
	@echo "  make wedge-test   - Build half-scale wedge for prototyping"
	@echo "  make drawer-test  - Build half-scale drawer for prototyping"
	@echo "  make test-set     - Build all half-scale prototype parts"
	@echo "  make test         - Run pytest"
	@echo "  make format       - Format code with ruff"
	@echo "  make lint         - Lint code with ruff"
	@echo "  make clean        - Remove build artifacts"

all: card wedge drawer

card: $(BUILD_DIR)
	$(PYTHON) parts/card_standard.py
	$(PYTHON) parts/card_wide.py
	$(PYTHON) parts/card_thickness_test.py

wedge: $(BUILD_DIR)
	$(PYTHON) parts/wedge.py

drawer: $(BUILD_DIR)
	$(PYTHON) parts/drawer.py

wedge-test: $(BUILD_DIR)
	$(PYTHON) parts/wedge_test.py

drawer-test: $(BUILD_DIR)
	$(PYTHON) parts/drawer_test.py

test-set: wedge-test drawer-test card

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
