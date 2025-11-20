# Piggy_game - Cross-platform Makefile

# Detect Python executable
PYTHON := python3
ifeq ($(OS),Windows_NT)
	PYTHON := python
endif

# Paths
PACKAGE := Piggy_game
TEST_DIR := test

# Helper vars for PYTHONPATH setting
ifeq ($(OS),Windows_NT)
    # Windows (CMD / PowerShell)
    SET_PYTHONPATH := set PYTHONPATH=.
    AND := &&
else
    # macOS / Linux
    SET_PYTHONPATH := PYTHONPATH=.
    AND := 
endif


# ========================= RUN GAME =========================
.PHONY: run
run:
	@echo "Starting Piggy Game..."
	$(PYTHON) -m main


# ========================= INSTALL ==========================
.PHONY: install
install:
	@echo "Installing dependencies..."
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt


# ========================= UNIT TESTS ========================
.PHONY: test
test:
	@echo "Running ALL tests (pytest + unittest)..."
	$(SET_PYTHONPATH) $(AND) $(PYTHON) -m pytest
	$(SET_PYTHONPATH) $(AND) $(PYTHON) -m unittest discover -s test -p "test_*.py" -t .


# ========================= COVERAGE =========================
.PHONY: coverage
coverage:
	@echo "Running coverage report..."
	$(SET_PYTHONPATH) $(AND) $(PYTHON) -m pytest --cov=package --cov-report=term-missing --cov-report=html


# ========================= LINTING ==========================
.PHONY: lint
lint:
	@echo "Running flake8..."
	flake8 package test main.py
	@echo "Running pylint..."
	$(SET_PYTHONPATH) $(AND) pylint package test main.py || true


# ========================= DOCUMENTATION =====================
.PHONY: doc
doc:
	@echo "Building Sphinx documentation..."
	mkdir -p doc/api
	sphinx-build -b html doc/source doc/api
	@echo "Docs generated at doc/api"


# ========================= UML DIAGRAMS ======================
.PHONY: uml
uml:
	@echo "Generating UML diagrams..."
	mkdir -p doc/uml
	pyreverse -o png -p $(PACKAGE) $(PACKAGE)
	@echo "Moving UML diagrams..."
	- mv classes_$(PACKAGE).png doc/uml/class_diagram.png 2>/dev/null || true
	- mv packages_$(PACKAGE).png doc/uml/package_diagram.png 2>/dev/null || true
	@echo "UML diagrams saved to doc/uml"


# ========================= CLEAN =============================
.PHONY: clean
clean:
	@echo "Cleaning cached files..."
	- find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	- find . -name "*.pyc" -delete 2>/dev/null || true
	- rm -rf htmlcov .pytest_cache doc/api doc/uml 2>/dev/null || true
	@echo "Cleanup completed."


# ========================= RUN ALL TASKS =====================
.PHONY: all
all: install test coverage doc uml lint
	@echo "All tasks completed successfully!"
