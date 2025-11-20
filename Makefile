# Piggy_game - Makefile

# Python executable
PYTHON := python3
ifeq ($(OS),Windows_NT)
	PYTHON := python
endif

# Paths
PACKAGE := Piggy_game
TEST_DIR := test

# RUN GAME
.PHONY: run
run:
	@echo "Starting Piggy Game..."
	$(PYTHON) -m main

# INSTALL DEPENDENCIES
.PHONY: install
install:
	@echo "Installing dependencies..."
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt

# UNIT TESTS
.PHONY: test
test:
	@echo "Running ALL tests (pytest + unittest)..."
	PYTHONPATH=. python3 -m pytest
	PYTHONPATH=. python3 -m unittest discover -s test -p "test_*.py" -t .

# COVERAGE
.PHONY: coverage
coverage:
	@echo "Running coverage report..."
	PYTHONPATH=. python3 -m pytest --cov=package --cov-report=term-missing --cov-report=html

# LINTING
.PHONY: lint
lint:
	@echo "Running flake8..."
	flake8 Piggy_game --select=D
	@echo "Running pylint..."
	PYTHONPATH=. pylint Piggy_game || true

# DOCUMENTATION (SPHINX)
.PHONY: doc
doc:
	@echo "Building Sphinx documentation..."
	mkdir -p doc/api
	sphinx-build -b html doc/source doc/api
	@echo "Docs generated at doc/api"

# UML DIAGRAMS
.PHONY: uml
uml:
	@echo "Generating UML diagrams..."
	mkdir -p doc/uml
	pyreverse -o png -p Piggy_game $(PACKAGE)
	@echo "Moving UML diagrams..."
	- mv classes_piggy_game.png doc/uml/class_diagram.png 2>/dev/null || true
	- mv packages_piggy_game.png doc/uml/package_diagram.png 2>/dev/null || true
	@echo "UML diagrams saved to doc/uml"


# CLEAN BUILD ARTIFACTS
.PHONY: clean
clean:
	@echo "Cleaning cached files..."
	- find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	- find . -name "*.pyc" -delete 2>/dev/null || true
	- rm -rf htmlcov .pytest_cache doc/api doc/uml 2>/dev/null || true
	@echo "Cleanup completed."

# RUN EVERYTHING
.PHONY: all
all: install lint test coverage doc uml
	@echo "All tasks completed successfully!"
