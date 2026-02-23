# Agent Instructions for Star Trek Retro Remake Game Development

## Quick Reference

**Game Architecture:** Hybrid State Machine + Game Object + Component + MVC
**Platform:** Linux only
**Language:** Python 3.14+
**Game Engine:** pygame-ce (Community Edition)
**UI Framework:** PySide6 (menus, dialogs, settings)
**Testing:** pytest with 85%+ coverage

## Essential Files

- `.github/copilot-instructions.md` - Comprehensive GitHub Copilot instructions
- `.agents/memory.instruction.md` - Coding preferences and game patterns
- `.agents/branch_protection.py` - Branch protection checker for AI agents
- `docs/ARCHITECTURE.md` - Detailed architecture documentation
- `docs/DESIGN.md` - Game design document
- This file (AGENTS.md) - Quick agent reference

## ⚠️ CRITICAL: Branch Protection (AI Agents)

**BEFORE ANY FILE MODIFICATION, RUN:**

```bash
python .agents/branch_protection.py
```

**Rules:**

- ❌ NEVER modify files on `main` branch
- ✅ ALWAYS work on `testing` branch
- ✅ ONLY assist with merges when human explicitly authorizes
- ✅ After merge assistance, remind human to switch back to `testing`

## Development Checklist

### Starting a New Feature

- [ ] Verify on `testing` branch
- [ ] Identify State/GameObject/Component responsibilities
- [ ] Write tests first (TDD approach)
- [ ] Implement Model (game logic, no rendering)
- [ ] Implement View (rendering, no logic)
- [ ] Implement Controller (input/state management)
- [ ] Update version numbers if non-trivial
- [ ] Update `_doc.md` file for modified modules
- [ ] Run full test suite
- [ ] Verify type hints with mypy

### Code Review Checklist

- [ ] Hybrid architecture maintained (State Machine + GameObject + Component + MVC)
- [ ] SOLID principles followed
- [ ] Type hints on all functions/methods/variables
- [ ] Docstrings with proper header format
- [ ] Tests written and passing (85%+ coverage)
- [ ] No rendering code in Models
- [ ] No game logic in Views
- [ ] Turn-based mechanics (all actions consume turns)
- [ ] 3D positioning (x, y, z coordinates)
- [ ] Dependencies justified (standard library first)
- [ ] pygame-ce for rendering, PySide6 for UI
- [ ] Linux-only, Python 3.14+ features used
- [ ] Version numbers updated
- [ ] `_doc.md` updated

## Architecture Rules (Non-Negotiable)

### Game States (State Machine)

```python
MAIN_MENU → GALAXY_MAP → SECTOR_MAP → COMBAT
         ↓                           ↓
      SETTINGS ←─────────────────→ PAUSED
```

### Game Object Pattern

- **GameObject**: Ships, stations, planets
- **Components**: WeaponSystems, ShieldSystems, EngineSystems
- **NOT full ECS**: Simpler composition for turn-based game

### MVC Separation

- **Model**: Game logic only (no pygame, no rendering)
- **View**: Rendering only (pygame-ce, no logic)
- **Controller**: Input and state management (PySide6/pygame events)

### Turn-Based Mechanics

- All actions consume turns
- Initiative-based turn order
- Fixed timestep game loop (60 FPS)
- Sequential action processing

### 3D Grid System

- Always use (x, y, z) coordinates
- Z-levels for vertical positioning in space
- 3D distance calculations for range

## Common Tasks

### Add New Game State

```python
# 1. Add to GameState enum
class GameState(Enum):
    NEW_STATE = auto()

# 2. Add transition logic
def enter_new_state(self):
    """Enter new state."""
    pass

# 3. Add update logic
def update_new_state(self, delta_time: float):
    """Update new state."""
    pass

# 4. Add render logic
def render_new_state(self):
    """Render new state."""
    pass
```

### Add Ship System Component

```python
# 1. Create component class
class NewSystem:
    def __init__(self):
        self.power_level: int = 0

    def update(self, delta_time: float) -> None:
        """Update system."""
        pass

# 2. Add to ship
ship.add_component(NewSystem())

# 3. Use in game logic
system = ship.get_component(NewSystem)
system.power_level = 100
```

### Add Turn-Based Action

```python
# 1. Create action class
@dataclass
class NewAction:
    actor: GameObject
    target: GameObject | None

    def execute(self) -> None:
        """Execute action."""
        pass

# 2. Process in turn manager
turn_manager.process_action(new_action)
```

## Quick Patterns

### Dependency Injection Setup

```python
# In main.py
def create_application():
    # Create model (game logic)
    game_model = GameModel()

    # Create view (rendering)
    game_view = GameView()

    # Create controller (input/state)
    game_controller = GameController(game_model)

    # Create application
    app = StarTrekRetroRemake(game_model, game_view, game_controller)

    return app
```

### Event Communication Pattern

```python
# Model emits events
class GameModel:
    def __init__(self):
        self.events: list[GameEvent] = []

    def fire_weapon(self, weapon: Weapon, target: GameObject):
        damage = weapon.calculate_damage()
        target.take_damage(damage)
        self.events.append(WeaponFiredEvent(weapon, target, damage))

# Controller processes events
class GameController:
    def update(self, delta_time: float):
        for event in self.model.events:
            self._process_event(event)
        self.model.events.clear()

# View renders based on model state
class GameView:
    def render(self, model: GameModel):
        for entity in model.entities:
            self._render_entity(entity)
```

### Testing Pattern

```python
def test_ship_fires_weapon(starship, target):
    # Arrange
    weapon = starship.get_component(WeaponSystem)
    initial_shields = target.shields

    # Act
    weapon.fire(target)

    # Assert
    assert target.shields < initial_shields
```

## Troubleshooting

### Import Errors

```bash
# Verify Python path
export PYTHONPATH="${PYTHONPATH}:${PWD}/STRR/src"

# Or add to main.py
sys.path.insert(0, str(Path(__file__).parent / "src"))
```

### Pygame-CE Not Found

```bash
# Install pygame-ce (Community Edition)
pip install pygame-ce

# Verify installation
python -c "import pygame; print(pygame.version.ver)"
```

### PySide6 Issues

```bash
# Install PySide6
pip install PySide6

# Verify installation
python -c "from PySide6.QtWidgets import QApplication; print('OK')"
```

### Test Failures

```bash
# Run with verbose output
pytest -v STRR/tests/

# Run specific test
pytest STRR/tests/test_state_machine.py::test_transition -v

# Run with coverage
pytest --cov=STRR/src --cov-report=html STRR/tests/
```

## File Templates

### Model Template (Game Logic)

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Star Trek Retro Remake - [Module Name]

Description:
    [What this module does]

Author: Star Trek Retro Remake Development Team
Email: development@star-trek-retro-remake.org
GitHub: https://github.com/L3Digital-Net/Star-Trek-Retro-Remake
Date Created: MM-DD-YYYY
Date Changed: MM-DD-YYYY
License: MIT

Features:
    - [Feature 1]
    - [Feature 2]

Requirements:
    - Linux environment
    - Python 3.14+
    - pygame-ce for rendering
    - PySide6 for UI

Known Issues:
    - [Current issues]

Planned Features:
    - [Planned features]

Classes:
    - ClassName: Brief description

Functions:
    - function_name(): Brief description
"""
from typing import Final

__version__: Final[str] = "0.0.10"


class MyModel:
    """Game logic class with no rendering dependencies."""

    def __init__(self):
        """Initialize model."""
        pass

    def update(self, delta_time: float) -> None:
        """Update game logic."""
        pass
```

### Component Template

```python
"""Ship system component."""
from typing import Protocol


class ShipSystemComponent(Protocol):
    """Protocol for ship system components."""

    def activate(self) -> None:
        """Activate system."""
        ...

    def deactivate(self) -> None:
        """Deactivate system."""
        ...

    def update(self, delta_time: float) -> None:
        """Update system."""
        ...


class WeaponSystem:
    """Weapon system component."""

    def __init__(self, damage: int, range: int):
        """Initialize weapon system."""
        self.damage = damage
        self.range = range
        self.active = False

    def activate(self) -> None:
        """Activate weapon."""
        self.active = True

    def deactivate(self) -> None:
        """Deactivate weapon."""
        self.active = False

    def update(self, delta_time: float) -> None:
        """Update weapon system."""
        if self.active:
            # Update weapon state
            pass

    def fire(self, target) -> int:
        """Fire weapon at target."""
        if self.active:
            return self.damage
        return 0
```

### View Template (Rendering)

```python
"""Game rendering view."""
import pygame


class GameView:
    """Handles all game rendering."""

    def __init__(self, screen: pygame.Surface):
        """Initialize view."""
        self.screen = screen

    def render(self, model) -> None:
        """Render game state."""
        self.screen.fill((0, 0, 0))
        self._render_entities(model.entities)
        pygame.display.flip()

    def _render_entities(self, entities) -> None:
        """Render game entities."""
        for entity in entities:
            self._render_entity(entity)

    def _render_entity(self, entity) -> None:
        """Render single entity."""
        # Rendering code here
        pass
```

### Test Template

```python
"""Tests for MyModel."""
import pytest
from src.game.my_model import MyModel


class TestMyModel:
    """Test suite for MyModel."""

    @pytest.fixture
    def model(self):
        """Create model instance for testing."""
        return MyModel()

    def test_model_initializes_correctly(self, model):
        """Test that model initializes with correct state."""
        # Arrange
        # (model fixture is already arranged)

        # Act
        # (no action needed for initialization test)

        # Assert
        assert model is not None

    def test_model_updates_state(self, model):
        """Test that model updates state correctly."""
        # Arrange
        initial_state = model.state
        delta_time = 1.0 / 60.0

        # Act
        model.update(delta_time)

        # Assert
        assert model.state != initial_state
```

## Resources

### Key Documentation

- [pygame-ce Documentation](https://pyga.me/)
- [PySide6 Documentation](https://doc.qt.io/qtforpython/)
- [Python 3.14 Documentation](https://docs.python.org/3.14/)
- [pytest Documentation](https://docs.pytest.org/)

### Project Setup Commands

```bash
# Create virtual environment
python3.14 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run game
python STRR/main.py

# Run tests
pytest STRR/tests/

# Run with coverage
pytest --cov=STRR/src --cov-report=html STRR/tests/

# Type check
mypy STRR/src/

# Format code
black STRR/

# Lint code
ruff check STRR/
```

## AI Agent Workflow

When an AI agent is working on this codebase:

1. **Verify branch**: Check on `testing` branch (run `.agents/branch_protection.py`)
2. **Read memory first**: Check `.agents/memory.instruction.md` for preferences
3. **Follow hybrid architecture**: State Machine + GameObject + Component + MVC
4. **Write tests first**: TDD approach is preferred
5. **Use type hints**: Always include type annotations
6. **Inject dependencies**: Never create dependencies inside classes
7. **Document decisions**: Update `_doc.md` files
8. **Run tests after changes**: Verify nothing breaks
9. **Update version**: Increment version for non-trivial changes
10. **Update memory**: Add new patterns or solutions discovered

## Remember

- **Branch protection is sacred**: testing branch only!
- **Hybrid architecture**: State Machine + GameObject + Component + MVC
- **NOT full ECS**: Simpler composition for turn-based game
- **Type hints everywhere**: Functions, variables, constants
- **Turn-based mechanics**: All actions consume turns
- **3D positioning**: Always use (x, y, z) coordinates
- **MVC separation**: No rendering in Models, no logic in Views
- **pygame-ce for rendering**: Community Edition for Python 3.14+
- **PySide6 for UI**: Menus, dialogs, settings
- **Standard library first**: Justify external dependencies
- **Test thoroughly**: 85%+ coverage for game logic
- **Linux only**: No Windows/macOS support
- **Python 3.14+ only**: Use latest language features
- **Version updates**: Increment for non-trivial changes
- **Document everything**: `_doc.md` files for all modules
