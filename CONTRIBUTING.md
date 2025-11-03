# Contributing to Star Trek Retro Remake

Thank you for your interest in contributing to Star Trek Retro Remake! This guide will help you get started with game development on this project.

## Development Setup

### Prerequisites

- Python 3.14+ (required for latest language features)
- Git
- Linux operating system (Ubuntu 22.04+ or similar)
- Basic understanding of pygame-ce and PySide6
- Familiarity with turn-based game mechanics

### Initial Setup

1. Fork and clone the repository:

   ```bash
   git clone <your-fork-url>
   cd Star-Trek-Retro-Remake
   ```

2. Create and activate virtual environment:

   ```bash
   python3.14 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up branch protection:

   ```bash
   ./setup-branch-protection.sh
   ```

5. Verify setup:

   ```bash
   # Run tests
   pytest STRR/tests/

   # Run the game
   python STRR/main.py
   ```

## Architecture Guidelines

This project follows a strict architectural pattern:

### Hybrid Architecture

- **State Machine**: MAIN_MENU, GALAXY_MAP, SECTOR_MAP, COMBAT, SETTINGS, PAUSED
- **Game Object Pattern**: Ships, stations, planets
- **Component Composition**: WeaponSystems, ShieldSystems, EngineSystems
- **MVC Separation**: Model (logic), View (rendering), Controller (input/state)

### NOT Full ECS

We use simpler Game Object + Component composition optimized for turn-based gameplay.

### SOLID Principles

All code must adhere to SOLID principles:

- **S**ingle Responsibility: One class = one purpose
- **O**pen/Closed: Extend via composition, not modification
- **L**iskov Substitution: Subtypes must be substitutable
- **I**nterface Segregation: Small, focused protocols
- **D**ependency Inversion: Depend on abstractions, inject dependencies

See `.github/copilot-instructions.md` for detailed guidelines.

## Development Workflow

### 1. Create a Feature Branch

**IMPORTANT**: Always work on the `testing` branch, never on `main`.

```bash
# Ensure you're on testing
git checkout testing

# Create feature branch from testing
git checkout -b feature/your-feature-name
```

### 2. Write Tests First (TDD)

```bash
# Create test file
touch STRR/tests/test_your_feature.py

# Write tests
# Run tests (they should fail initially)
pytest STRR/tests/test_your_feature.py
```

### 3. Implement Feature

Follow the hybrid architecture:

```bash
# Create game logic (Model)
touch STRR/src/game/your_feature.py

# Create rendering (View) if needed
touch STRR/src/ui/your_feature_view.py

# Create controller logic if needed
touch STRR/src/ui/your_feature_controller.py
```

### 4. Run Tests

```bash
# All tests
pytest STRR/tests/

# With coverage
pytest --cov=STRR/src --cov-report=html STRR/tests/

# Specific test file
pytest STRR/tests/test_your_feature.py -v
```

### 5. Code Quality Checks

```bash
# Type checking
mypy STRR/src/

# Linting
ruff check STRR/

# Formatting
black STRR/
```

### 6. Commit Changes

Follow conventional commit format:

```bash
git commit -m "feat: add new ship system component"
git commit -m "fix: resolve turn order calculation bug"
git commit -m "docs: update architecture documentation"
git commit -m "test: add tests for weapon system"
```

### 7. Push and Create Pull Request

```bash
# Push to your fork
git push origin feature/your-feature-name

# Merge to testing branch (not main!)
git checkout testing
git merge feature/your-feature-name
git push origin testing
```

## Code Standards

### Type Hints

Always use type hints (Python 3.14+ syntax):

```python
def move_ship(
    ship: GameObject,
    destination: tuple[int, int, int],
    obstacles: Sequence[GameObject]
) -> bool:
    """Move ship to destination if path is clear."""
    return True
```

### Docstrings

Use the project's standard docstring format:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Star Trek Retro Remake - [Module Name]

Description:
    What this module does.

Author: [Your Name]
Email: [your.email@example.com]
GitHub: [https://github.com/yourusername]
Date Created: MM-DD-YYYY
Date Changed: MM-DD-YYYY
License: MIT

Features:
    - Feature 1
    - Feature 2

Requirements:
    - Linux environment
    - Python 3.14+
    - pygame-ce for rendering
    - PySide6 for UI
"""
```

### Testing

- Use Arrange-Act-Assert pattern
- One assertion per test (when possible)
- Descriptive test names: `test_should_X_when_Y`
- Mock external dependencies

Example:

```python
def test_ship_takes_damage_when_shields_down():
    # Arrange
    ship = Starship(shields=0)
    initial_hull = ship.hull_integrity

    # Act
    ship.take_damage(25)

    # Assert
    assert ship.hull_integrity < initial_hull
```

## What to Contribute

### Good Contributions

✅ Bug fixes with tests
✅ New game features following architecture
✅ Documentation improvements
✅ Test coverage improvements
✅ Performance optimizations
✅ Example implementations

### Changes That Need Discussion

⚠️ Breaking architecture changes
⚠️ New external dependencies
⚠️ Major refactoring
⚠️ Changes to game mechanics

Please open an issue first to discuss these.

## Pull Request Checklist

Before submitting a PR, ensure:

- [ ] Code follows hybrid architecture
- [ ] SOLID principles maintained
- [ ] All tests pass (`pytest STRR/tests/`)
- [ ] New features have tests (85%+ coverage)
- [ ] Code is formatted (`black STRR/`)
- [ ] Type hints added to all functions
- [ ] Docstrings added with proper header format
- [ ] No linting errors (`ruff check STRR/`)
- [ ] Type checking passes (`mypy STRR/src/`)
- [ ] Documentation updated if needed
- [ ] Version numbers updated for non-trivial changes
- [ ] `_doc.md` file created/updated for modified modules
- [ ] Commit messages follow conventional format
- [ ] Changes made to `testing` branch (not `main`)

## Running the Full Check Suite

```bash
# Run all checks before submitting
./scripts/run_tests.sh

# Or manually:
pytest --cov=STRR/src --cov-report=html STRR/tests/
mypy STRR/src/
ruff check STRR/
black --check STRR/
```

## Game-Specific Guidelines

### Turn-Based Mechanics

All actions must:

- Consume turns when executed
- Respect initiative order
- Update game state consistently

### 3D Grid System

Always use 3D coordinates:

```python
position = Position(x=5, y=10, z=2)  # ✅ Correct
position = (5, 10)                   # ❌ Wrong - missing z
```

### State Transitions

Follow state machine rules:

```python
# Valid transitions
MAIN_MENU → GALAXY_MAP
GALAXY_MAP → SECTOR_MAP
SECTOR_MAP → COMBAT

# Any state can transition to
SETTINGS, PAUSED
```

### Component Systems

Use component composition:

```python
# ✅ Correct - Component composition
ship.add_component(WeaponSystem(damage=50))
weapon = ship.get_component(WeaponSystem)

# ❌ Wrong - Inheritance
class Ship(WeaponSystem, ShieldSystem):  # Don't do this
    pass
```

## Directory Structure

```
Star-Trek-Retro-Remake/
├── STRR/                    # Main game directory
│   ├── main.py             # Entry point
│   ├── assets/             # Game assets
│   ├── config/             # Configuration files
│   ├── src/
│   │   ├── game/          # Game logic (Models)
│   │   ├── engine/        # Core engine systems
│   │   └── ui/            # PySide6 UI components
│   └── tests/             # Test suite
├── docs/                   # Documentation
├── .agents/                # AI agent memory and preferences
├── .github/                # GitHub configuration
│   └── copilot-instructions.md
└── scripts/                # Development scripts
```

## Common Patterns

See `AGENTS.md` for:

- File templates
- Testing patterns
- Component patterns
- State machine examples
- Dependency injection examples

## Getting Help

- Check `AGENTS.md` for quick reference
- Review `.github/copilot-instructions.md` for detailed guidelines
- Review existing code for patterns
- Open an issue for questions
- Join discussions in pull requests

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

Feel free to open an issue for any questions or clarifications about contributing to Star Trek Retro Remake!

---

**Remember**: This is a turn-based space strategy game following Kirk-era Star Trek universe. All contributions should maintain the spirit of tactical, thoughtful gameplay and the adventure of space exploration.
