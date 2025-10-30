.PHONY: help install install-dev test test-cov clean lint format run check pre-commit-install

# Default target
help:
	@echo "Star Trek Retro Remake - Development Makefile"
	@echo ""
	@echo "Available targets:"
	@echo "  install            Install the package"
	@echo "  install-dev        Install package with development dependencies"
	@echo "  test               Run tests"
	@echo "  test-cov           Run tests with coverage report"
	@echo "  clean              Remove build artifacts and cache files"
	@echo "  lint               Run linting checks (ruff, mypy)"
	@echo "  format             Format code with ruff"
	@echo "  run                Run the game"
	@echo "  check              Run all checks (lint, test)"
	@echo "  pre-commit-install Install pre-commit hooks"

# Installation targets
install:
	pip install -e .

install-dev:
	pip install -e .[dev]

# Testing targets
test:
	cd star_trek_retro_remake && python -m pytest tests/ -v

test-cov:
	cd star_trek_retro_remake && python -m pytest tests/ -v --cov=src --cov-report=term-missing --cov-report=html
	@echo "Coverage report generated in star_trek_retro_remake/htmlcov/index.html"

# Cleaning targets
clean:
	@echo "Cleaning build artifacts..."
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name .ruff_cache -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@find . -type f -name ".coverage" -delete 2>/dev/null || true
	@rm -rf htmlcov/ dist/ build/ 2>/dev/null || true
	@echo "Clean complete!"

# Code quality targets
lint:
	@echo "Running ruff..."
	ruff check star_trek_retro_remake/src/ star_trek_retro_remake/tests/
	@echo "Running mypy..."
	mypy star_trek_retro_remake/src/

format:
	@echo "Formatting code with ruff..."
	ruff format star_trek_retro_remake/src/ star_trek_retro_remake/tests/
	ruff check --fix star_trek_retro_remake/src/ star_trek_retro_remake/tests/

# Run the game
run:
	cd star_trek_retro_remake && python main.py

# Combined checks
check: lint test
	@echo "All checks passed!"

# Pre-commit setup
pre-commit-install:
	pre-commit install
	@echo "Pre-commit hooks installed!"
