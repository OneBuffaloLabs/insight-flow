# Define environment variables
VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip
STREAMLIT = $(VENV)/bin/streamlit

# .PHONY defines targets that aren't files
.PHONY: all help install run clean lint format fix

# Default target: prompts the user
all: help

# Help command to display available targets
help:
	@echo "----------------------------------------------------------------------"
	@echo "                      INSIGHT FLOW MAKEFILE"
	@echo "----------------------------------------------------------------------"
	@echo "Make commands:"
	@echo "  make install   - Create venv and install dependencies"
	@echo "  make run       - Run the Streamlit application (Port 3000)"
	@echo "  make clean     - Remove venv and compiled Python files"
	@echo "  make lint      - Run static code analysis (Ruff)"
	@echo "  make format    - Auto-format code (Ruff)"
	@echo "  make fix       - Auto-fix linting issues (Ruff)"
	@echo "----------------------------------------------------------------------"

# Create virtual environment and install dependencies
install:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	$(PIP) install ruff
	@echo "Dependencies installed successfully."

# Run the app (using the venv's streamlit binary directly)
run:
	$(STREAMLIT) run app.py --server.port 3000

# Clean up environment
clean:
	rm -rf $(VENV)
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	@echo "Cleaned up project environment."

# Run static code analysis
lint:
	$(VENV)/bin/python -m ruff check .

# Auto-format code
format:
	$(VENV)/bin/python -m ruff format .

# Auto-fix linting issues
fix:
	$(VENV)/bin/python -m ruff check --fix .