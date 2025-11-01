# Star Trek Retro Remake - Development Instructions

## ⚠️ CRITICAL: BRANCH PROTECTION POLICY ⚠️

**STRICTLY ENFORCED RULE - NO EXCEPTIONS:**

- **NEVER make code changes to the `main` branch**
- **ALL code changes MUST be made to the `testing` branch**
- Before making ANY code modifications, verify the current branch
- If on `main` branch, **STOP** and inform the user that changes cannot be made
- Only documentation-only changes (e.g., README updates) may be considered for `main` after explicit user approval
- This rule applies to ALL AI agents and ALL code modifications

**Verification Required:**
- Check current branch before every code change
- If current branch is `main`: HALT and request user switch to `testing`
- Only proceed with code changes when on `testing` branch

## Overview

Turn-based strategy game set in Kirk-era Star Trek universe. Features grid-based space exploration with 3D z-levels, tactical combat, and starship management.

**Key References:**

- Architecture details: `/docs/ARCHITECTURE.md`
- Game design: `/docs/DESIGN.md`
- Python 3.14+ stdlib: https://docs.python.org/3.14/

## Architecture

**Pattern:** Hybrid State Machine + Game Object + Component + MVC
- **NOT full ECS** - Use Game Object with Component composition (simpler for turn-based games)
- **pygame-ce** for rendering (game view) - Community Edition with Python 3.14+ support
- **PySide6** for UI (menus, dialogs, settings)
- **MVC separation** - Game logic independent of UI/rendering
- **Object pooling** for projectiles, effects, temporary entities

**Game States:**
- `MAIN_MENU` → `GALAXY_MAP` → `SECTOR_MAP` → `COMBAT`
- `SETTINGS` and `PAUSED` accessible from any state

**Core Mechanics:**
- Turn-based (all actions consume turns, initiative-based)
- 3D grid system (x, y, z coordinates for space positioning)
- Fixed timestep game loop: input → update → render

## Development Standards

**Environment:**
- Linux-only target platform
- Python 3.14+ (use latest stdlib features)

**Code Quality:**
- Type hints everywhere: functions, variables, constants, collections
- Modern syntax: `str | None`, `list[str]`, `dict[str, int]`, `Final`, `Protocol`, `TypedDict`
- Strict PEP 8, f-strings only
- Functions: max 20 lines, max 3 nesting levels
- Standard library first, justify external dependencies

**Version Strategy:**
- Format: MAJOR.MINOR.PATCH (currently at v0.0.10)
- AI can freely increment PATCH by 0.0.1 for any non-trivial changes
- Must update: `pyproject.toml`, modified file `__version__`, `CHANGELOG.md`, file "Date Changed"
- Increment rules:
  - Bug fixes, refactoring, small features: +0.0.1 (PATCH)
  - New major features or subsystems: +0.1.0 (MINOR) - requires approval
  - Breaking changes or complete rewrites: +1.0.0 (MAJOR) - requires approval
- All modified core modules get current version number
- Supporting modules can stay at lower versions until modified
- Defer error handling until v1.0.0
- Focus: clean architecture, core game logic, state transitions

## File Structure

```python
#!/usr/bin/env python3
"""
Star Trek Retro Remake - [Module Name]

Description:
    What this game module does and why.

Author: [Full Name or Team Name]
Email: [email@domain.com]
GitHub: [https://github.com/username]
Date Created: [MM-DD-YYYY]
Date Changed: [MM-DD-YYYY]
License: [License Type]

Features:
    - Turn-based game mechanics with initiative system
    - State machine for MAIN_MENU, GALAXY_MAP, SECTOR_MAP, COMBAT, SETTINGS, PAUSED
    - Game Object pattern with Component composition for ship systems
    - MVC architecture for clean separation of concerns
    - Object pooling for efficient memory management
    - 3D grid system with z-levels for space representation
    - Separated game logic from rendering for testability
    - pygame-ce (Community Edition) for game rendering, PySide6 for UI/menus/dialogs
    - Standard library first approach
    - Clean confident design patterns

Requirements:
    - Linux environment
    - Python 3.14+ for latest language features
    - pygame-ce (Community Edition) for game engine rendering (replaces pygame for Python 3.14+ compatibility)
    - PySide6 for UI, menus, settings, and dialogs

Known Issues:
    - Current limitations or known problems
    - Areas that need improvement or attention

Planned Features:
    - Future enhancement 1
    - Future enhancement 2
    - Additional planned improvements

Classes:
    - Class1: Brief description
    - Class2: Brief description

Functions:
    - function1(): Brief description
    - function2(): Brief description
"""
```

## Project Organization

**Directory Structure:**
- `star_trek_retro_remake/src/` - Game modules
- `star_trek_retro_remake/tests/` - All test files
- `star_trek_retro_remake/assets/` - Data, graphics, audio
- `star_trek_retro_remake/config/` - Configuration files
- `star_trek_retro_remake/docs/` - PROJECT-DOC.md, CHANGELOG.md

**Testing (pytest):**
- AAA pattern (Arrange-Act-Assert)
- 80%+ coverage for critical paths
- Test behavior, not implementation
- Use fixtures, parametrize, descriptive names

**Version Management:**
- AI increments version by 0.0.1 for any non-trivial change
- Update all modified files: `pyproject.toml`, file `__version__`, "Date Changed" header
- Update `/docs/CHANGELOG.md` with new version entry
- Categorize changes: Added/Changed/Fixed/Removed
- Version consistency: All core modules use current project version
- Supporting/unchanged modules keep their existing version numbers

**Documentation Standard:**
- Every `.py` file in `STRR/` has a matching `_doc.md` file in the same directory
- Naming: `application.py` → `application_doc.md`
- Content: Comprehensive module documentation (purpose, architecture, usage, examples)
- General/cross-cutting docs go in `/docs/` root folder
- See `/docs/DOCUMENTATION_STANDARDS.md` for template and guidelines
- **MANDATORY**: All documentation must reflect **Linux-only compatibility**
- **NO Windows references** - document Linux paths, commands, system requirements only
- **Python 3.14+ REQUIRED**: Document latest language features and requirements

**File Header Standards:**
- All files must have proper headers following repository standards
- Include shebang (`#!/usr/bin/env python3`) - no encoding declaration needed (Python 3 default is UTF-8)
- Complete docstring format with Description, Author, Email, GitHub, Date Created, Date Changed, License, Features, Requirements, Known Issues, Planned Features, Classes, Functions
- Header content must reflect current code implementation
- Update "Date Changed" to current date when modified

**Docstring Format:**
- All docstrings follow repository's specified format (see file header example above)
- **Do not specify types in docstrings** - rely on type hints instead
- Docstring content must reflect current code state
- Use consistent formatting throughout the project

**Inline Documentation:**
- Inline comments for each significant code block for readability and AI autocompletion context
- Comments at the top of code blocks, briefly explaining purpose (preferably one line)
- Add/update inline comments for complex logic, Linux-specific implementations, and important decisions

**Minimal .md File Creation:**
- **IMPORTANT**: Only create/update README.md, PROJECT-DOC.md, CHANGELOG.md as needed
- Exception: auto-generated API docs in library folders (common_lib/docs/)
- Per-file `_doc.md` files required for all `.py` files in `STRR/` directory

## AI Code Generation Rules

1. **Branch Protection:** NEVER make code changes to `main` branch - ALL code changes go to `testing` branch ONLY
2. **Dependencies:** Standard library first, justify external dependencies
3. **Reuse:** Check existing codebase, consolidate duplicates
4. **Quality:** Complete examples, type hints for ALL elements, proper headers with complete docstrings
5. **Architecture:** Follow Hybrid State Machine + Game Object + Component + MVC, SOLID principles
6. **Game Systems:** Ship systems as components (WeaponSystems, ShieldSystems) not full ECS
7. **State Machine:** Use specific modes (GALAXY_MAP, SECTOR_MAP, COMBAT) not generic states
8. **Grid Logic:** 3D positioning (x, y, z) for all spatial calculations
9. **Turn-Based:** All actions advance turn counter, support initiative
10. **Framework Separation:** pygame-ce rendering separate from PySide6 UI
11. **Confident Design:** Architectural solutions over defensive checks
12. **Version Aware:** Defer error handling until v1.0.0
13. **Documentation:** Every `.py` file has matching `_doc.md` in same directory with comprehensive module docs
14. **Testing:** pytest for business logic, AAA pattern
15. **Versioning:** Increment by 0.0.1 for changes, update pyproject.toml, __version__, Date Changed, CHANGELOG.md
16. **Comments:** Inline for significant blocks, explain complex logic and design decisions
17. **Type Safety:** Runtime matches annotations, no types in docstrings (use type hints)
18. **Separation:** Clear component boundaries
19. **Pooling:** Reuse projectiles, effects, temporary objects
20. **Linux-Only:** All code, docs, and examples must target Linux exclusively
21. **Header Compliance:** All files have proper shebang and complete docstring headers (no encoding declaration needed)

## Decision Framework

**Solution Priority:**
1. Python stdlib → 2. Existing code → 3. Generalize → 4. External dependency

**Avoid:**

- Duplicate logic, hardcoded values, functions >20 lines
- Missing type hints (functions, variables, constants, collections)
- External libraries when stdlib works
- Defensive programming (scattered checks)
- Full ECS when Game Object + Component fits better
- Real-time logic in turn-based game
- UI dependencies in game logic (MVC violation)
- 2D positioning (use 3D: x, y, z)

## Code Examples

### Preferred Type Hint Patterns

```python
# Modern Python 3.14+ syntax - Use this
from typing import Final, Protocol

def calculate_damage(
    base_damage: int,
    multiplier: float,
    targets: list[str]
) -> dict[str, int]:
    """Calculate damage for multiple targets."""
    return {target: int(base_damage * multiplier) for target in targets}

# Constants with type hints
MAX_SHIELD_STRENGTH: Final[int] = 100
SHIP_TYPES: Final[list[str]] = ["cruiser", "destroyer", "frigate"]

# Protocol for component interfaces
class Component(Protocol):
    """Protocol defining component interface."""
    
    def update(self, delta_time: float) -> None:
        """Update component state."""
        ...
```

### Game Object + Component Pattern

```python
# Prefer this: Game Object with Component composition
class Starship:
    """Starship entity with component-based systems."""
    
    def __init__(self, ship_id: str, position: tuple[int, int, int]) -> None:
        self.id: str = ship_id
        self.position: tuple[int, int, int] = position  # 3D coordinates (x, y, z)
        
        # Components
        self.weapons: WeaponSystem = WeaponSystem(self)
        self.shields: ShieldSystem = ShieldSystem(self)
        self.engines: EngineSystem = EngineSystem(self)
    
    def update(self, delta_time: float) -> None:
        """Update all ship systems."""
        self.weapons.update(delta_time)
        self.shields.update(delta_time)
        self.engines.update(delta_time)

# Component interface
class WeaponSystem:
    """Weapon system component."""
    
    def __init__(self, ship: Starship) -> None:
        self.ship: Starship = ship
        self.energy: int = 100
    
    def fire(self, target: tuple[int, int, int]) -> bool:
        """Fire at target coordinates."""
        if self.energy < 10:
            return False
        self.energy -= 10
        return True
    
    def update(self, delta_time: float) -> None:
        """Recharge weapons."""
        self.energy = min(100, self.energy + 1)
```

### State Machine Pattern

```python
# State machine for game modes
from enum import Enum, auto

class GameState(Enum):
    """Game state enumeration."""
    MAIN_MENU = auto()
    GALAXY_MAP = auto()
    SECTOR_MAP = auto()
    COMBAT = auto()
    SETTINGS = auto()
    PAUSED = auto()

class GameStateMachine:
    """Manages game state transitions."""
    
    def __init__(self) -> None:
        self.current_state: GameState = GameState.MAIN_MENU
        self.previous_state: GameState | None = None
    
    def transition_to(self, new_state: GameState) -> bool:
        """Transition to new state with validation."""
        if not self._is_valid_transition(new_state):
            return False
        
        self.previous_state = self.current_state
        self.current_state = new_state
        return True
    
    def _is_valid_transition(self, target: GameState) -> bool:
        """Validate state transition."""
        # PAUSED and SETTINGS accessible from any state
        if target in (GameState.PAUSED, GameState.SETTINGS):
            return True
        
        # Define valid transitions
        valid_transitions: dict[GameState, list[GameState]] = {
            GameState.MAIN_MENU: [GameState.GALAXY_MAP, GameState.SETTINGS],
            GameState.GALAXY_MAP: [GameState.SECTOR_MAP, GameState.MAIN_MENU],
            GameState.SECTOR_MAP: [GameState.COMBAT, GameState.GALAXY_MAP],
            GameState.COMBAT: [GameState.SECTOR_MAP],
        }
        
        return target in valid_transitions.get(self.current_state, [])
```

### MVC Separation Pattern

```python
# Model - Pure game logic (no UI dependencies)
class CombatModel:
    """Combat logic model."""
    
    def __init__(self) -> None:
        self.ships: list[Starship] = []
        self.turn_order: list[str] = []
        self.current_turn: int = 0
    
    def add_ship(self, ship: Starship) -> None:
        """Add ship to combat."""
        self.ships.append(ship)
        self._recalculate_initiative()
    
    def execute_turn(self) -> None:
        """Process one combat turn."""
        self.current_turn += 1
        # Pure logic, no rendering

# View - Rendering only (no game logic)
class CombatView:
    """Combat rendering view."""
    
    def __init__(self, model: CombatModel) -> None:
        self.model: CombatModel = model
    
    def render(self, screen: pygame.Surface) -> None:
        """Render combat state."""
        for ship in self.model.ships:
            self._draw_ship(screen, ship)

# Controller - Coordinates model and view
class CombatController:
    """Combat controller."""
    
    def __init__(self) -> None:
        self.model: CombatModel = CombatModel()
        self.view: CombatView = CombatView(self.model)
    
    def handle_input(self, event: pygame.event.Event) -> None:
        """Process user input."""
        # Translate input to model operations
        pass
```

## Common Pitfalls to Avoid

### ❌ Don't: Mix 2D and 3D positioning

```python
# Wrong - inconsistent dimensions
ship.position = (x, y)  # 2D
enemy.position = (x, y, z)  # 3D
```

**✅ Do: Always use 3D coordinates**

```python
# Correct - consistent 3D positioning
ship.position: tuple[int, int, int] = (x, y, z)
enemy.position: tuple[int, int, int] = (x, y, z)
```

### ❌ Don't: Put UI logic in game model

```python
# Wrong - model depends on rendering
class Ship:
    def update(self):
        pygame.draw.circle(screen, (255, 0, 0), self.position, 5)
```

**✅ Do: Separate model from view**

```python
# Correct - model is pure logic
class Ship:
    def update(self, delta_time: float) -> None:
        self.position = self._calculate_new_position(delta_time)

# View handles rendering
class ShipView:
    def render(self, ship: Ship, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, (255, 0, 0), ship.position[:2], 5)
```

### ❌ Don't: Use string formatting other than f-strings

```python
# Wrong - old style
message = "Ship %s at position %d, %d" % (ship.name, x, y)
message = "Ship {} at position {}".format(ship.name, x)
```

**✅ Do: Use f-strings exclusively**

```python
# Correct - f-string
message: str = f"Ship {ship.name} at position {x}, {y}, {z}"
```

### ❌ Don't: Miss type hints

```python
# Wrong - no type hints
def calculate_damage(base, modifier):
    return base * modifier

ships = []
damage = None
```

**✅ Do: Type hints everywhere**

```python
# Correct - complete type hints
def calculate_damage(base: int, modifier: float) -> int:
    return int(base * modifier)

ships: list[Starship] = []
damage: int | None = None
```

### ❌ Don't: Create functions longer than 20 lines

```python
# Wrong - too long, too complex
def process_combat_turn(ships, enemies, effects, ...):
    # 50+ lines of complex logic
    # Multiple responsibilities
    # Hard to test
    pass
```

**✅ Do: Break into smaller functions**

```python
# Correct - focused, testable functions
def process_combat_turn(combat_state: CombatState) -> None:
    """Process one combat turn."""
    _resolve_initiative(combat_state)
    _execute_actions(combat_state)
    _apply_effects(combat_state)
    _update_turn_counter(combat_state)

def _resolve_initiative(combat_state: CombatState) -> None:
    """Calculate turn order based on initiative."""
    combat_state.turn_order = sorted(
        combat_state.ships,
        key=lambda s: s.initiative,
        reverse=True
    )
```

## Quick Reference

### Common Tasks

| Task | Command/Location |
|------|------------------|
| Run tests | `pytest tests/ -v` or `make test` |
| Run with coverage | `pytest tests/ --cov=src --cov-report=term-missing` |
| Lint code | `make lint` |
| Format code | `make format` |
| Run all checks | `make check` |
| Update version | Update `pyproject.toml`, `__version__`, CHANGELOG.md |
| View architecture | `/docs/ARCHITECTURE.md` |
| View game design | `/docs/DESIGN.md` |
| Check doc standards | `/docs/DOCUMENTATION_STANDARDS.md` |

### Version Update Checklist

When making changes:
- [ ] Update `pyproject.toml` version field
- [ ] Update `__version__` in modified Python files
- [ ] Update "Date Changed" in file headers
- [ ] Add entry to `/docs/CHANGELOG.md`
- [ ] Categorize changes (Added/Changed/Fixed/Removed)

### File Creation Checklist

For new Python files in `STRR/`:
- [ ] Add proper shebang: `#!/usr/bin/env python3`
- [ ] Complete docstring with all required sections
- [ ] Type hints for all functions, variables, constants
- [ ] Create matching `_doc.md` file in same directory
- [ ] Add inline comments for significant code blocks
- [ ] Follow max 20 lines per function
- [ ] Use 3D coordinates (x, y, z) for positions

## Key Documentation

### Essential Files
- **Architecture Guide**: `/docs/ARCHITECTURE.md` - Technical implementation details
- **Game Design**: `/docs/DESIGN.md` - Complete game design specification
- **Documentation Standards**: `/docs/DOCUMENTATION_STANDARDS.md` - Doc format and guidelines
- **Versioning Guidelines**: `/docs/VERSIONING_GUIDELINES.md` - Version management rules
- **Qt Designer Workflow**: `/docs/QT_DESIGNER_WORKFLOW.md` - UI design process
- **Change Log**: `/docs/CHANGELOG.md` - Version history

### Project Structure
- **Source Code**: `STRR/src/` - Main game modules
- **Tests**: `STRR/tests/` - pytest test suite
- **Assets**: `STRR/assets/` - Graphics, audio, data files
- **Configuration**: `STRR/config/` - TOML configuration files
- **Entry Point**: `STRR/main.py` - Game launcher

### Custom Prompts
Located in `.github/prompts/`:
- `code-review.prompt.md` - Code review guidelines
- `documentation.prompt.md` - Documentation generation
- `refactor.prompt.md` - Code refactoring rules
- `test.prompt.md` - Test creation guidelines
- `debug.prompt.md` - Debugging assistance

## Troubleshooting

### Common Issues

**Issue: Import errors with pygame**
- **Solution**: Ensure pygame-ce (Community Edition) is installed: `pip install pygame-ce>=2.5`
- **Note**: Standard pygame may not work with Python 3.14+

**Issue: Type hint errors with union types**
- **Solution**: Use modern syntax: `str | None` instead of `Optional[str]` or `Union[str, None]`
- **Requires**: Python 3.14+

**Issue: Tests failing after version update**
- **Solution**: Verify all modified files have updated version numbers
- **Check**: `pyproject.toml`, file `__version__` variables, CHANGELOG.md

**Issue: Branch protection errors**
- **Solution**: Ensure working on `testing` branch, not `main`
- **Command**: `git checkout testing` or `git branch` to verify

**Issue: Documentation out of sync**
- **Solution**: Update both `.py` file docstring AND matching `_doc.md` file
- **Location**: Each `STRR/module.py` needs `STRR/module_doc.md`
