# Quick Start Guide - Star Trek Retro Remake

Get up and running with Star Trek Retro Remake development in under 10 minutes.

## Prerequisites (2 minutes)

- **Linux** (Ubuntu 22.04+ or similar)
- **Python 3.14+** (required for latest language features)
- **Git**

Verify your setup:

```bash
python3.14 --version  # Should be 3.14.x
git --version         # Should be 2.x+
```

## Initial Setup (3 minutes)

### 1. Clone and Setup

```bash
# Clone repository
git clone https://github.com/L3DigitalNet/Star-Trek-Retro-Remake.git
cd Star-Trek-Retro-Remake

# Ensure on testing branch
git checkout testing

# Create virtual environment
python3.14 -m venv .venv

# Activate environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Verify Installation

```bash
# Run tests
pytest STRR/tests/

# Expected: All tests pass
```

### 3. Run the Game

```bash
python STRR/main.py
```

You should see the game window open with the main menu.

## Project Structure (2 minutes)

### Key Directories

```
STRR/
├── main.py              # Start here - game entry point
├── src/
│   ├── game/           # Game logic (Models) - no rendering
│   │   ├── application.py
│   │   ├── model.py
│   │   └── commands.py
│   ├── engine/         # Core systems
│   │   ├── entities/   # Game objects (ships, stations)
│   │   ├── components/ # Ship systems (weapons, shields)
│   │   └── state/      # State machine
│   └── ui/             # PySide6 UI
│       ├── controller.py
│       └── view.py
└── tests/              # pytest test suite
```

### Look at the Architecture

```bash
# Main entry point
cat STRR/main.py

# Game model (logic)
cat STRR/src/game/model.py

# State machine
cat STRR/src/engine/state/state_machine.py
```

## Understanding the Code (2 minutes)

### Architecture Pattern

**Hybrid: State Machine + GameObject + Component + MVC**

```
State Machine          GameObject           Components
┌────────────┐        ┌──────────┐         ┌──────────────┐
│ MAIN_MENU  │        │ Starship │◄────────│ WeaponSystem │
│ GALAXY_MAP │        │          │         │ ShieldSystem │
│ SECTOR_MAP │        │          │         │ EngineSystem │
│   COMBAT   │        └──────────┘         └──────────────┘
│  SETTINGS  │
│   PAUSED   │        MVC Pattern
└────────────┘        Model (logic) + View (rendering) + Controller (input)
```

### Key Concepts

1. **Turn-Based**: All actions consume turns, initiative-based
2. **3D Grid**: Space uses (x, y, z) coordinates
3. **Component Composition**: Ships have systems as components
4. **MVC Separation**: Logic separate from rendering

## Making Your First Change (1 minute)

### Example: Add a Test Ship

1. Open `STRR/src/engine/entities/starship.py`
2. Add test data
3. Run tests
4. Commit changes

```bash
# Make changes on testing branch
git checkout testing

# Run tests
pytest STRR/tests/test_entities.py -v

# Commit if tests pass
git add .
git commit -m "feat: add test ship configuration"
```

## Daily Development Workflow

### Before Starting Work

```bash
# Always work on testing branch
git checkout testing

# Pull latest changes
git pull origin testing

# Activate environment
source .venv/bin/activate
```

### During Development

```bash
# Run specific test
pytest STRR/tests/test_your_feature.py -v

# Run all tests
pytest STRR/tests/

# Type check
mypy STRR/src/

# Format code
black STRR/
```

### After Making Changes

```bash
# Run full test suite
pytest --cov=STRR/src STRR/tests/

# Check coverage report
open htmlcov/index.html  # View in browser

# Commit changes
git add .
git commit -m "feat: your change description"
git push origin testing
```

## Common Commands

```bash
# Run game
python STRR/main.py

# Run tests
pytest STRR/tests/ -v                    # Verbose output
pytest --cov=STRR/src STRR/tests/        # With coverage
pytest -k "ship" STRR/tests/             # Filter by name

# Code quality
mypy STRR/src/                           # Type check
black STRR/                              # Format code
ruff check STRR/                         # Lint code

# Git workflow
git checkout testing                     # Switch to dev branch
git status                               # Check changes
git add .                                # Stage changes
git commit -m "feat: description"        # Commit
git push origin testing                  # Push to remote
```

## Key Files to Review

### For Development

- `AGENTS.md` - Quick reference and patterns
- `.github/copilot-instructions.md` - Comprehensive guidelines
- `CONTRIBUTING.md` - Contribution guidelines
- `docs/ARCHITECTURE.md` - Architecture details
- `docs/DESIGN.md` - Game design document

### For Configuration

- `pyproject.toml` - Python project configuration
- `requirements.txt` - Dependencies
- `STRR/config/game_settings.toml` - Game settings

## Testing Examples

### Run Specific Tests

```bash
# Test starship functionality
pytest STRR/tests/test_entities.py::test_starship_initialization -v

# Test state machine
pytest STRR/tests/test_state_machine.py -v

# Test game model
pytest STRR/tests/test_game_model.py -v
```

### Writing a Test

```python
def test_ship_fires_weapon():
    # Arrange
    ship = Starship(name="Enterprise")
    weapon = WeaponSystem(damage=50, range=10)
    ship.add_component(weapon)
    target = Starship(name="Enemy", shields=100)

    # Act
    weapon.fire(target)

    # Assert
    assert target.shields < 100
```

## Next Steps

1. **Read the architecture docs**:
   - `docs/ARCHITECTURE.md` - System design
   - `docs/DESIGN.md` - Game mechanics

2. **Explore the code**:
   - Run the game and play around
   - Read the example implementations
   - Look at tests to understand patterns

3. **Make your first contribution**:
   - Pick an issue from GitHub
   - Write tests for your changes
   - Follow the hybrid architecture
   - Submit a pull request

4. **Get help**:
   - Check `AGENTS.md` for common patterns
   - Review `.github/copilot-instructions.md`
   - Open an issue if stuck

## Tips

1. **Always work on `testing` branch** - Never commit directly to `main`
2. **Write tests first** - TDD helps design better systems
3. **Follow architecture** - Hybrid State Machine + GameObject + Component + MVC
4. **Use type hints** - Makes code self-documenting
5. **3D coordinates** - Always use (x, y, z) for positions
6. **MVC separation** - Keep logic out of rendering, rendering out of logic
7. **Run tests frequently** - Catch issues early

## Troubleshooting

### Python Version Issues

```bash
# Check Python version
python3.14 --version

# If not installed, install Python 3.14
sudo apt update
sudo apt install python3.14 python3.14-venv python3.14-dev
```

### Import Errors

```bash
# Ensure virtual environment is activated
source .venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Test Failures

```bash
# Run tests with more detail
pytest STRR/tests/ -vv

# Run specific failing test
pytest STRR/tests/test_file.py::test_name -vv
```

### Game Won't Start

```bash
# Check pygame-ce installation
python -c "import pygame; print(pygame.version.ver)"

# Check PySide6 installation
python -c "from PySide6.QtWidgets import QApplication; print('OK')"

# Reinstall if needed
pip install pygame-ce PySide6 --force-reinstall
```

## Resources

- **Project Documentation**: `docs/` directory
- **API Reference**: See `_doc.md` files alongside source files
- **pygame-ce Docs**: <https://pyga.me/>
- **PySide6 Docs**: <https://doc.qt.io/qtforpython/>
- **Python 3.14 Docs**: <https://docs.python.org/3.14/>

---

**Welcome to Star Trek Retro Remake development! 🚀**

Explore strange new worlds, seek out new code patterns, and boldly refactor what no one has refactored before!
