#!/bin/bash
# Star Trek Retro Remake - Development Setup Script

set -e

echo "🚀 Setting up Star Trek Retro Remake development environment..."
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Install package in editable mode with dev dependencies
echo ""
echo "Installing package with development dependencies..."
pip install -e .[dev]

# Install pre-commit hooks
echo ""
echo "Installing pre-commit hooks..."
pre-commit install

# Create directories
echo ""
echo "Creating necessary directories..."
mkdir -p star_trek_retro_remake/logs
mkdir -p star_trek_retro_remake/saves
mkdir -p star_trek_retro_remake/screenshots

echo ""
echo "✅ Development environment setup complete!"
echo ""
echo "Available commands:"
echo "  make test       - Run tests"
echo "  make test-cov   - Run tests with coverage"
echo "  make lint       - Run linting checks"
echo "  make format     - Format code"
echo "  make run        - Run the game"
echo "  make clean      - Clean build artifacts"
echo ""
echo "Happy coding! 🖖"
