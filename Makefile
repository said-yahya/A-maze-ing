PYTHON       = python3
PIP          = pip3
MAIN_SRC     = a_maze_ing.py
CONFIG       = config.txt

GREEN        = \033[1;32m
YELLOW       = \033[1;33m
RED          = \033[1;31m
RESET        = \033[0m


all: check run

run:
	@echo "$(GREEN)==== Running Maze Generator ==== $(RESET)"
	@$(PYTHON) $(MAIN_SRC) $(CONFIG)

check:
	@echo "$(YELLOW)==== Checking Code Style (flake8) ==== $(RESET)"
	@flake8 --max-line-length=110 $(MAIN_SRC) || (echo "$(RED)Flake8 errors detected!$(RESET)"; exit 1)
	@echo "$(GREEN)Flake8: OK$(RESET)"
	@echo "$(YELLOW)==== Checking Type Hints (mypy) ==== $(RESET)"
	@mypy --strict $(MAIN_SRC) || (echo "$(RED)Mypy errors detected!$(RESET)"; exit 1)
	@echo "$(GREEN)Mypy: OK$(RESET)"

clean:
	@echo "$(YELLOW)==== Cleaning __pycache__ and internal caches ==== $(RESET)"
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete
	@rm -rf .mypy_cache .pytest_cache

fclean: clean
	@echo "$(YELLOW)==== Full Project Cleanup ==== $(RESET)"
	@rm -f $$(ls *.txt | grep -v '$(CONFIG)')
	@echo "$(GREEN)Cleanup finished!$(RESET)"

re: fclean all

help:
	@echo "Available commands:"
	@echo "  make        - Check style compliance, static types, and run the project"
	@echo "  make run    - Fast execution of the project without linter checks"
	@echo "  make check  - Run static analysis checks via flake8 and mypy"
	@echo "  make clean  - Remove __pycache__ directories and intermediate cache files"
	@echo "  make fclean - Execute full cleanup (removes caches and generated text outputs)"
	@echo "  make re     - Perform a complete reset (fclean) and re-run all steps"


.PHONY: all run check clean fclean re help