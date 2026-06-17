PYTHON       = python3
PIP          = pip3
MAIN_SRC     = a_maze_ing.py
CONFIG       = config.txt
VENV_DIR     = venv
VENV_ACTIVATE = $(VENV_DIR)/bin/activate

GREEN        = \033[1;32m
YELLOW       = \033[1;33m
RED          = \033[1;31m
RESET        = \033[0m

.PHONY: all run check debug clean fclean re help install


all: lint run

install:
	@echo "$(YELLOW)==== Setting up Virtual Environment (venv) ==== $(RESET)"
	@if [ ! -d "$(VENV_DIR)" ]; then \
		$(PYTHON) -m venv $(VENV_DIR); \
		echo "$(GREEN)Virtual environment created successfully.$(RESET)"; \
	else \
		echo "$(GREEN)Virtual environment already exists.$(RESET)"; \
	fi
	@echo "$(YELLOW)==== Installing Dependencies & Build Tools ==== $(RESET)"
	@$(VENV_DIR)/bin/pip install --upgrade -r requirements.txt
	@echo "$(YELLOW)CRITICAL STEP REQUIRED:$(RESET)"
	@echo "To activate the virtual environment, you MUST run this command manually:"
	@echo "$(YELLOW)   source $(VENV_DIR)/bin/activate$(RESET)"
	@echo "$(GREEN)==================================================$(RESET)"

run:
	@echo "$(GREEN)==== Running Maze Generator ==== $(RESET)"
	@if [ -f "$(VENV_DIR)/bin/python" ]; then \
		$(VENV_DIR)/bin/python $(MAIN_SRC) $(CONFIG); \
	else \
		$(PYTHON) $(MAIN_SRC) $(CONFIG); \
	fi

build:
	@echo "$(YELLOW)==== Building the Wheel Distribution Package ==== $(RESET)"
	@if [ -f "$(VENV_DIR)/bin/python" ]; then \
		$(VENV_DIR)/bin/python -m build; \
	else \
		$(PYTHON) -m build; \
	fi
	@echo "$(YELLOW)==== Copying Package to Root Repository ==== $(RESET)"
	@if [ -d "dist" ]; then \
		cp dist/mazegen-1.0.0-py3-none-any.whl ./mazegen-1.0.0-py3-none-any.whl; \
		echo "$(GREEN)Package copied to root successfully.$(RESET)"; \
	fi
	@echo "$(YELLOW)==== Installing the Generated Package ==== $(RESET)"
	@if [ -f "$(VENV_DIR)/bin/pip" ]; then \
		$(VENV_DIR)/bin/pip install --force-reinstall ./mazegen-1.0.0-py3-none-any.whl; \
	else \
		$(PIP) install --force-reinstall ./mazegen-1.0.0-py3-none-any.whl; \
	fi
	@echo "$(GREEN)[+] Package compiled and installed successfully!$(RESET)"

debug:
	@echo "$(YELLOW)==== Launching Python Debugger (pdb) ==== $(RESET)"
	@echo "$(GREEN)Commands: 'c' to continue, 'n' for next line, 'l' to list code, 'q' to quit.$(RESET)"
	@if [ -f "$(VENV_DIR)/bin/python" ]; then \
		$(VENV_DIR)/bin/python -m pdb $(MAIN_SRC) $(CONFIG); \
	else \
		$(PYTHON) -m pdb $(MAIN_SRC) $(CONFIG); \
	fi

lint:
	@echo "$(YELLOW)==== Checking Code Style (flake8) ==== $(RESET)"
	@if [ -f "$(VENV_DIR)/bin/flake8" ]; then \
		$(VENV_DIR)/bin/flake8 . --exclude $(VENV_DIR);\
	else \
		flake8 . --exclude $(VENV_DIR);\
	fi || (echo "$(RED)Flake8 errors detected!$(RESET)"; exit 1)
	@echo "$(GREEN)Flake8: OK$(RESET)"
	@echo "$(YELLOW)==== Checking Type Hints (mypy) ==== $(RESET)"
	@if [ -f "$(VENV_DIR)/bin/mypy" ]; then \
		$(VENV_DIR)/bin/mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs; \
	else \
		mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs; \
	fi || (echo "$(RED)Mypy errors detected!$(RESET)"; exit 1)
	@echo "$(GREEN)Mypy: OK$(RESET)"

clean:
	@echo "$(YELLOW)==== Cleaning __pycache__ and internal caches ==== $(RESET)"
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete
	@rm -rf .mypy_cache .pytest_cache mazegen.egg-info

fclean: clean
	@echo "$(YELLOW)==== Full Project Cleanup ==== $(RESET)"
	@rm -rf $(VENV_DIR) dist
	@rm -f $$(ls *.txt 2>/dev/null | grep -v -E "($(CONFIG)|requirements.txt)")
	@rm -f *.whl
	@echo "$(GREEN)Cleanup finished! venv and packages removed.$(RESET)"

re: fclean install

help:
	@echo "Available commands:"
	@echo "  make        - Check style compliance, static types, and run the project"
	@echo "  make install - Setup venv and install required development dependencies"
	@echo "  make build   - Compile source codes into a standard .whl package using build"
	@echo "  make run    - Fast execution of the project using venv environment"
	@echo "  make lint  - Run static analysis checks via flake8 and mypy strictly"
	@echo "  make debug  - Execute the main script in debug mode using pdb"
	@echo "  make clean  - Remove __pycache__ directories and intermediate cache files"
	@echo "  make fclean - Full reset (removes venv, builds, and generated text outputs)"