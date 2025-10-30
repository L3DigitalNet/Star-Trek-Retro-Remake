#!/bin/bash
# Star Trek Retro Remake - Test Runner Script

set -e

echo "🧪 Running Star Trek Retro Remake Tests..."
echo ""

cd star_trek_retro_remake

# Run tests with coverage
python -m pytest tests/ -v --cov=src --cov-report=term-missing --cov-report=html

echo ""
echo "✅ Tests complete!"
echo ""
echo "📊 Coverage report generated:"
echo "   Open htmlcov/index.html in your browser to view"
