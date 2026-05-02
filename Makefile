.PHONY: all clean test card body base assembly clearance format lint help

PYTHON := uv run python
BUILD_DIR := build

help:
	@echo "PLOTTER build targets:"
	@echo "  make all       - Build all parts (STL + STEP)"
	@echo "  make card      - Build all card variants (standard / wide / thickness test)"
	@echo "  make body      - Build body panel"
	@echo "  make base      - Build all base variants (75/60/90)"
	@echo "  make clearance - Build tenon clearance test print"
	@echo "  make assembly  - Build full assembly preview"
	@echo "  make test      - Run pytest"
	@echo "  make format    - Format code with ruff"
	@echo "  make lint      - Lint code with ruff"
	@echo "  make clean     - Remove build artifacts"

all: card body base assembly

card: $(BUILD_DIR)
	$(PYTHON) parts/card_standard.py
	$(PYTHON) parts/card_wide.py
	$(PYTHON) parts/card_thickness_test.py

body: $(BUILD_DIR)
	$(PYTHON) parts/body_6row.py

base: $(BUILD_DIR)
	$(PYTHON) parts/base_75.py
	$(PYTHON) parts/base_60.py
	$(PYTHON) parts/base_90.py

clearance: $(BUILD_DIR)
	$(PYTHON) tests/tenon_clearance_test.py

assembly: $(BUILD_DIR)
	$(PYTHON) assemblies/full_assembly.py

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
