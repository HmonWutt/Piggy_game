# Piggy_game - Makefile

# python version
PYTHON := python3

# directories
PACKAGE := piggy_game/package
TEST_DIR := piggy_game/test

# runs the game
.PHONY: run
run:
	@echo "Starting Piggy Game..."
	$(PYTHON) main.py

# installs all the dependencies
.PHONY: install
install:
	@echo "Installing dependencies..."
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt

# runsa ll the unit tests with pytest
.PHONY: test


test: pytest unittest
# Run pytest
pytest:
	@echo "Running pytest tests..."
	pytest

# Run unittest (discover all tests in the current directory)
unittest:
	@echo "Running unittest tests..."
	python -m unittest discover -s test -p "*.py"

# runs test with coverage report
.PHONY: coverage
coverage:
	@echo "Running tests with coverage..."
	pytest --cov=$(PACKAGE) --cov-report=term-missing --cov-report=html
	@echo "Coverage HTML report generated at: htmlcov/index.html"

# lint code with flake8 and pylint
.PHONY: lint
lint:
	@echo "Running flake8..."
	flake8 $(PACKAGE) --docstring-convention=google
	@echo "Running pylint..."
	pylint $(PACKAGE)

# building html doc using Sphinx
.PHONY: doc
doc:
	@echo "Building Sphinx documentation..."
	mkdir -p doc/api
	sphinx-build -b html docs/source doc/api
	@echo "Documentation generated in doc/api"

# generate uml diagrams using pyreverse
.PHONY: uml
uml:
	@echo "Generating UML diagrams..."
	mkdir -p doc/uml
	pyreverse -o png -p piggy_game $(PACKAGE)
	mv -f classes_piggy_game.png doc/uml/class_diagram.png || true
	mv -f packages_piggy_game.png doc/uml/package_diagram.png || true
	@echo "UML diagrams generated in doc/uml"

# clean all build artifacts, caches and generated files
.PHONY: clean
clean:
	@echo "Cleaning temporary files..."
	find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	rm -rf htmlcov .pytest_cache .mypy_cache doc/api doc/uml

# run everything
.PHONY: all
all: install lint test coverage doc uml
	@echo "All tasks completed successfully!"
