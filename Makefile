# Piggy_game - Cross-platform Makefile

# Detect Python executable
PYTHON := python3
ifeq ($(OS),Windows_NT)
	PYTHON := python
endif

# Paths
PACKAGE := Piggy_game
TEST_DIR := test
VENV_DIR := venv

# Helper vars for PYTHONPATH setting
ifeq ($(OS),Windows_NT)
	PY := $(VENV_DIR)\Scripts\python.exe
	SET_PYTHONPATH := set PYTHONPATH=.
	AND := &&
else
	PY := $(VENV_DIR)/bin/python
	SET_PYTHONPATH := PYTHONPATH=.
	AND :=
endif

# ========================= VIRTUAL ENVIRONMENT =====================
.PHONY: venv
venv:
	@echo "Creating virtual environment..."
ifeq ($(OS),Windows_NT)
	@if not exist "$(VENV_DIR)" (
		$(PYTHON) -m venv $(VENV_DIR)
	) else (
		echo "Virtual environment already exists."
	)
	@echo "To activate the venv in CMD:"
	@echo "    $(VENV_DIR)\\Scripts\\activate.bat"
	@echo "Or in PowerShell:"
	@echo "    $(VENV_DIR)\\Scripts\\Activate.ps1"
else
	@if [ ! -d "$(VENV_DIR)" ]; then \
		$(PYTHON) -m venv $(VENV_DIR); \
	else \
		echo "Virtual environment already exists."; \
	fi
	@echo "To activate the venv, run:"
	@echo "    source $(VENV_DIR)/bin/activate"
endif
	@echo "Then install dependencies with:"
	@echo "    make install"

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
	flake8 package test main.py --ignore=E501
	@echo "Running pylint..."
	$(SET_PYTHONPATH) $(AND) pylint package test main.py --max-line-length=120 


# ========================= DOCUMENTATION =====================
.PHONY: doc
doc:
	@echo "Building Sphinx documentation..."
	$(SET_PYTHONPATH) $(AND) $(PYTHON) scripts/doc.py

# ========================= UML DIAGRAMS ======================
.PHONY: uml
uml:
	@echo "Generating UML diagrams..."
	$(SET_PYTHONPATH) $(AND) $(PYTHON) scripts/uml.py


# ========================= CLEAN =============================
.PHONY: clean
clean:
	@echo "Cleaning cached files..."
	$(SET_PYTHONPATH) $(AND) $(PYTHON) scripts/clean.py	

# ========================= RUN ALL TASKS =====================
.PHONY: all
all: install clean test coverage doc uml lint 
	@echo "All tasks completed successfully!"
