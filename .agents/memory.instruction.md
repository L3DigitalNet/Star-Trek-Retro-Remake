---
applyTo: '**'
---

# Coding Preferences - Star Trek Retro Remake Game

## ⚠️ CRITICAL: Branch Protection Rules (MANDATORY FOR ALL AI AGENTS)

**BEFORE ANY FILE MODIFICATIONS, AI AGENTS MUST:**

1. **Check current Git branch** using: `git branch --show-current`
2. **Verify branch is NOT 'main'** (unless explicitly authorized for merge assistance)
3. **Run branch protection check**: `python .agents/branch_protection.py`

### Branch Usage Rules

- **testing branch**: All development, modifications, and commits happen here
- **main branch**: PROTECTED - Only for merges from testing (human-approved only)

### AI Agent Restrictions

❌ **NEVER** make file changes on the 'main' branch
❌ **NEVER** commit to the 'main' branch
❌ **NEVER** suggest changes to files when on 'main' branch
✅ **ALWAYS** verify branch before any file operations
✅ **ONLY** assist with merges when human gives explicit permission

### Exception: Merge Assistance

When human explicitly requests merge assistance:

1. Human must be on 'main' branch
2. Human must explicitly say "help me merge" or similar authorization
3. AI can guide through: `git merge testing`
4. After merge, AI must remind human to switch back: `git checkout testing`

### Enforcement

The following protections are in place:

- Git pre-commit hook: Blocks commits to main
- Git post-checkout hook: Warns when switching to main
- Git post-merge hook: Reminds to switch back to testing
- Python script: `.agents/branch_protection.py` - AI agents should check this before modifications

**If AI agent detects it's on 'main' branch without explicit merge authorization, it must:**

1. Refuse to make any file changes
2. Inform human of the protection violation
3. Suggest switching to testing: `git checkout testing`

## Architecture Mandates

### Hybrid Architecture (Non-Negotiable)

- **State Machine**: MAIN_MENU, GALAXY_MAP, SECTOR_MAP, COMBAT, SETTINGS, PAUSED
- **Game Object Pattern**: Ships, stations, planets as game objects
- **Component Composition**: WeaponSystems, ShieldSystems, EngineSystems as components
- **MVC Separation**: Game logic (Model) independent from rendering (View) and input/state (Controller)
- **NOT Full ECS**: Use simpler Game Object + Component for turn-based game

### SOLID Principles (Required)

- Single Responsibility: One class = one purpose
- Open/Closed: Extend via inheritance/composition, not modification
- Liskov Substitution: Subtypes must be substitutable
- Interface Segregation: Small, focused interfaces using Protocol
- Dependency Inversion: Depend on abstractions, inject dependencies

## Technology Stack

### Required Technologies

- **Python**: 3.14+ only (use latest language features)
- **Platform**: Linux only (no Windows/macOS support)
- **Game Engine**: pygame-ce (Community Edition) for rendering
- **UI Framework**: PySide6 for menus, dialogs, settings
- **Testing**: pytest with fixtures and parametrize

### Framework Usage

- **pygame-ce**: Game rendering, sprite management, game loop
- **PySide6**: Main window, menus, dialogs, settings screens
- **Standard Library**: Prefer stdlib over external dependencies

## Code Organization Standards

### File Structure (Strict)

```
STRR/
├── main.py               # Entry point
├── assets/               # Game assets
├── config/               # Configuration files
├── src/
│   ├── game/            # Game logic (Models)
│   │   ├── application.py
│   │   ├── model.py
│   │   ├── commands.py
│   │   └── events.py
│   ├── engine/          # Core engine systems
│   │   ├── entities/    # Game objects
│   │   ├── components/  # Ship systems
│   │   ├── state/       # State machine
│   │   └── maps/        # Grid/sector systems
│   └── ui/              # PySide6 UI components
│       ├── controller.py
│       └── view.py
└── tests/
    ├── conftest.py
    └── test_*.py
```

### Naming Conventions

- **Files**: `snake_case.py`
- **Classes**: `PascalCase`
- **Functions/Methods**: `snake_case`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private**: `_leading_underscore`

## Game-Specific Coding Patterns

### State Machine Pattern

```python
from enum import Enum, auto

class GameState(Enum):
    MAIN_MENU = auto()
    GALAXY_MAP = auto()
    SECTOR_MAP = auto()
    COMBAT = auto()
    SETTINGS = auto()
    PAUSED = auto()

class StateMachine:
    def __init__(self):
        self._state = GameState.MAIN_MENU

    def transition_to(self, new_state: GameState) -> None:
        """Transition to new game state."""
        self._state = new_state
```

### Game Object with Components

```python
from typing import Protocol

class Component(Protocol):
    """Base component protocol."""
    def update(self, delta_time: float) -> None:
        ...

class GameObject:
    """Game object with component composition."""
    def __init__(self):
        self.components: dict[type, Component] = {}

    def add_component(self, component: Component) -> None:
        """Add component to game object."""
        self.components[type(component)] = component

    def get_component(self, component_type: type) -> Component | None:
        """Get component by type."""
        return self.components.get(component_type)
```

### MVC Pattern for Game

```python
# Model - Game logic only, no rendering
class GameModel:
    def __init__(self):
        self.entities: list[GameObject] = []

    def update(self, delta_time: float) -> None:
        """Update game logic."""
        for entity in self.entities:
            entity.update(delta_time)

# View - Rendering only, no logic
class GameView:
    def render(self, model: GameModel) -> None:
        """Render game state."""
        for entity in model.entities:
            self._render_entity(entity)

# Controller - Input and state management
class GameController:
    def __init__(self, model: GameModel):
        self.model = model

    def handle_input(self, event) -> None:
        """Handle player input."""
        pass
```

## Testing Standards

### Test Structure (Required)

```python
# Arrange-Act-Assert pattern
def test_ship_takes_damage():
    # Arrange
    ship = Starship(shields=100)

    # Act
    ship.take_damage(25)

    # Assert
    assert ship.shields == 75
```

### Test Coverage Requirements

- Game logic (Models): 90%+ coverage
- Core systems (Components, State): 85%+ coverage
- Integration tests for state transitions
- Test turn-based mechanics thoroughly

### Fixtures for Game Testing

```python
import pytest

@pytest.fixture
def starship():
    """Create test starship."""
    return Starship(name="Enterprise", shields=100)

@pytest.fixture
def game_state():
    """Create test game state."""
    return GameState.SECTOR_MAP
```

## Game Loop and Turn-Based Mechanics

### Fixed Timestep Game Loop

```python
def run(self) -> None:
    """Main game loop with fixed timestep."""
    delta_time = 1.0 / 60.0  # 60 FPS

    while self.running:
        self._handle_input()
        self._update(delta_time)
        self._render()
```

### Turn-Based Action Processing

```python
class TurnManager:
    def __init__(self):
        self.turn_count: int = 0

    def process_turn(self, action: Action) -> None:
        """Process action and advance turn."""
        action.execute()
        self.turn_count += 1
```

## Type Hints (Mandatory)

### Standard Usage

```python
from typing import Protocol, Final
from collections.abc import Sequence

GRID_SIZE: Final[int] = 10

def move_ship(
    ship: GameObject,
    destination: tuple[int, int, int],
    obstacles: Sequence[GameObject]
) -> bool:
    """Move ship to destination if path is clear."""
    return True

class ShipSystem(Protocol):
    def activate(self) -> None:
        ...
```

## Documentation Requirements

### Docstring Format (Game Module Standard)

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Star Trek Retro Remake - Ship Systems

Description:
    Component-based ship systems for weapons, shields, engines.

Author: Star Trek Retro Remake Development Team
Email: development@star-trek-retro-remake.org
GitHub: https://github.com/L3Digital-Net/Star-Trek-Retro-Remake
Date Created: MM-DD-YYYY
Date Changed: MM-DD-YYYY
License: MIT

Features:
    - Component composition for ship systems
    - Turn-based action processing
    - Energy management and power distribution
    - Damage and repair mechanics

Requirements:
    - Linux environment
    - Python 3.14+
    - pygame-ce for rendering
    - PySide6 for UI

Known Issues:
    - [List current issues]

Planned Features:
    - [List planned features]
"""
```

### Per-File Documentation

Every `.py` file in `STRR/` has a matching `_doc.md` file:

- Naming: `application.py` → `application_doc.md`
- Content: Comprehensive module documentation
- Location: Same directory as source file

## Version Management

### Version Increment Rules

- **Current version**: Check `pyproject.toml` and `main.py`
- **Patch increment** (+0.0.1): Bug fixes, small features, refactoring
- **Minor increment** (+0.1.0): Major features, new subsystems (requires approval)
- **Major increment** (+1.0.0): Breaking changes, rewrites (requires approval)

### Files to Update

When changing version:

1. `pyproject.toml` - Project version
2. Modified file's `__version__` variable
3. Modified file's "Date Changed" header
4. `docs/CHANGELOG.md` - Add entry with changes

## Error Handling Strategy

### Current Policy (Pre-v1.0.0)

- **Defer comprehensive error handling until v1.0.0**
- Focus on clean architecture and core functionality
- Handle critical errors only (file I/O, system resources)
- Use assertions for development-time checks

### Post-v1.0.0 Strategy

```python
class GameError(Exception):
    """Base exception for game errors."""
    pass

class InvalidMoveError(GameError):
    """Raised when move is invalid."""
    pass
```

## 3D Grid System

### Z-Level Positioning

```python
@dataclass
class Position:
    """3D position in space."""
    x: int
    y: int
    z: int  # Z-level for vertical positioning

def calculate_distance(pos1: Position, pos2: Position) -> float:
    """Calculate 3D distance between positions."""
    dx = pos1.x - pos2.x
    dy = pos1.y - pos2.y
    dz = pos1.z - pos2.z
    return (dx**2 + dy**2 + dz**2) ** 0.5
```

## Object Pooling

### Pooling for Effects

```python
class ProjectilePool:
    """Object pool for projectiles."""
    def __init__(self, size: int = 50):
        self.pool: list[Projectile] = [
            Projectile() for _ in range(size)
        ]
        self.available: list[Projectile] = list(self.pool)

    def get(self) -> Projectile | None:
        """Get projectile from pool."""
        if self.available:
            return self.available.pop()
        return None

    def return_to_pool(self, projectile: Projectile) -> None:
        """Return projectile to pool."""
        projectile.reset()
        self.available.append(projectile)
```

## Quick Reference Commands

### Running the Game

```bash
python STRR/main.py              # Run game
```

### Testing

```bash
pytest STRR/tests/               # All tests
pytest -v STRR/tests/            # Verbose output
pytest --cov=STRR/src STRR/tests/  # With coverage
```

### Development Tools

```bash
mypy STRR/src/                   # Type checking
black STRR/                      # Code formatting
ruff check STRR/                 # Linting
```

## Development Workflow

1. **Verify branch**: Ensure on `testing` branch
2. **Design**: Identify State, GameObject, Component responsibilities
3. **Test First**: Write failing test for new feature
4. **Implement**: Make test pass
5. **Refactor**: Improve while keeping tests green
6. **Document**: Update `_doc.md` files
7. **Version**: Update version numbers if significant changes
8. **Verify**: Run full test suite

## Anti-Patterns to Avoid

❌ **DON'T**: Mix rendering code with game logic
✅ **DO**: Keep Model/View/Controller separated

❌ **DON'T**: Use full ECS for turn-based game
✅ **DO**: Use Game Object + Component composition

❌ **DON'T**: Implement real-time logic in turn-based game
✅ **DO**: Process turns sequentially with initiative

❌ **DON'T**: Hardcode game data in code
✅ **DO**: Load from TOML config files

❌ **DON'T**: Create 2D-only positioning
✅ **DO**: Use 3D coordinates (x, y, z) for space

❌ **DON'T**: Block UI with long operations
✅ **DO**: Use threading for long operations if needed

## Solutions Repository

### Common Game Patterns

#### State Transition with Validation

```python
def transition_to(self, new_state: GameState) -> bool:
    """Transition to new state with validation."""
    if self._can_transition(new_state):
        self._exit_current_state()
        self._state = new_state
        self._enter_new_state()
        return True
    return False
```

#### Initiative-Based Turn Order

```python
def calculate_turn_order(self, entities: list[GameObject]) -> list[GameObject]:
    """Calculate turn order by initiative."""
    return sorted(
        entities,
        key=lambda e: e.get_component(InitiativeComponent).value,
        reverse=True
    )
```

#### Energy Distribution

```python
def distribute_power(self, ship: Starship, allocations: dict[str, int]) -> None:
    """Distribute ship power to systems."""
    total = sum(allocations.values())
    if total <= ship.reactor_output:
        for system_name, power in allocations.items():
            system = ship.get_system(system_name)
            system.set_power(power)
```

## Remember

- Branch protection is sacred (testing only!)
- Hybrid architecture: State Machine + Game Object + Component + MVC
- Type hints are not optional
- Turn-based mechanics: all actions consume turns
- 3D positioning: always use (x, y, z) coordinates
- pygame-ce for rendering, PySide6 for UI/menus
- Standard library first, justify dependencies
- Test game logic thoroughly (90%+ coverage)
- Version updates for non-trivial changes
- Linux-only platform, Python 3.14+ only
