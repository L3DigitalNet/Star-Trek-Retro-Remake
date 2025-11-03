---
description: "Code Refactoring and Optimization following repository guidelines"
mode: "agent"
---

# Code Refactoring and Optimization

Perform comprehensive refactoring of ${file} or project following repository guidelines and clean architecture principles.

Follow [repository guidelines](../copilot-instructions.md).

## Core Refactoring Principles

### DRY (Don't Repeat Yourself) - HIGH PRIORITY
- **MUST** eliminate ALL code duplication through abstraction and modularization
- **MUST** maintain single source of truth for all data structures and business logic
- **MUST** centralize constants and configuration in dedicated modules
- **MUST** extract common patterns into base classes or utility functions
- **MUST** consolidate similar logic into unified implementations

### Python Standard Library First - MANDATORY
- **MUST** use Python standard library solutions before considering external dependencies
- **MUST** leverage built-in modules: `pathlib`, `json`, `csv`, `datetime`, `collections`, `itertools`, `functools`
- **ONLY** add external dependencies when standard library cannot reasonably solve the problem
- **MUST** justify external dependencies with comments explaining why standard library is insufficient
- **MUST** replace existing external dependencies with standard library equivalents where possible

### Clean Code and Confident Design - ESSENTIAL
- **PREFER** confident, clean code over defensive programming patterns
- **AVOID** unnecessary null/None checks when program flow guarantees valid values
- **PREFER** explicit initialization and clear program flow over defensive conditionals
- **MUST** design code that reflects actual program behavior and constraints
- **MUST** order functions and classes to reflect logical flow and dependencies; classes always listed first
- **AVOID** excessive defensive checks that add noise without meaningful protection
- **PREFER** early validation and fail-fast approaches over scattered defensive checks
- **MUST** use type hints to document and enforce design assumptions
- **PREFER** clear, linear program flow with proper initialization order
- **AVOID** "just in case" code that handles scenarios that shouldn't occur in correct usage

## Type Hints and Documentation

### Type Hint Requirements
- **MUST** include type hints for ALL functions, methods, variables, constants, and data structures
- **MUST** use modern union syntax: `str | None` not `Optional[str]`
- **MUST** use collection types: `list[str]`, `dict[str, int]`, `set[int]`
- **MUST** use `Final` for constants, `ClassVar` for class variables, `TypedDict` for structured dicts
- **MUST** use `Protocol` for interfaces, `TypeVar`/`Generic` for reusable components
- **AVOID** `Any` type - use specific types or protocols

### Documentation Standards
- Follow repository docstring standards as per [copilot-instructions.md](../copilot-instructions.md)
- **MUST** include docstrings for ALL public functions, methods, and classes
- **MUST** follow specific docstring format patterns
- **MUST** maintain 80 character limit for docstring lines
- **STREAMLINED** approach: Brief descriptions with types in hints, examples only for complex logic

## Architectural Improvements

### Single Responsibility Principle
- **MUST** keep functions focused (single responsibility)
- **MUST** ensure each class has clear, cohesive purpose
- **MUST** organize code into focused, single-purpose modules
- **MUST** separate business logic, data access, and presentation layers
- **AVOID** deep nesting (max 3 levels)
- **AVOID** complex conditional statements

### Clean Architecture Patterns
- **MUST** implement proper separation of concerns
- **MUST** create clear interfaces and boundaries between components
- **MUST** design for composition over inheritance
- **MUST** follow SOLID principles in class design
- **MUST** implement clear dependency management

## Code Quality Standards

### Function and Class Design
- **MUST** use descriptive, self-documenting names for all elements
- **MUST** follow strict PEP 8 compliance
- **MUST** use f-string formatting (never `.format()` or `%` formatting)
- **MUST** list function arguments on separate lines when more than two arguments
- **MUST** align arguments with opening parenthesis or use hanging indent (4 spaces)

### Performance and Maintainability
- **MUST** optimize for readability and maintainability over premature optimization
- **MUST** reduce complexity through clear design patterns
- **MUST** use built-in functions and data structures for better performance
- **MAY** suggest external libraries ONLY when they provide significant, justified benefits
- **PREFER** eliminate performance bottlenecks through proper algorithm and data structure choices if this does not compromise code clarity

## Version-Aware Refactoring Strategy

### Pre-v1.0.0 Focus (Current Phase)
- **DEFER** comprehensive error handling until v1.0.0
- **FOCUS** on clean architecture, confident design patterns
- **PRIORITIZE** core functionality and clear program flow
- **IMPLEMENT** proper initialization sequences that guarantee valid state
- **AVOID** excessive defensive programming patterns

### Incremental Improvement Approach
- **MUST** make small, testable improvements rather than large rewrites
- **MUST** preserve external behavior during refactoring
- **MUST** maintain or improve test coverage
- **MUST** update documentation to reflect changes

## Repository Integration

### Project Structure Compliance
- **MUST** follow Star Trek Retro Remake directory structure:
  - `STRR/src/game/` - Game logic (Models/Controllers)
  - `STRR/src/ui/` - UI components (Views)
  - `STRR/src/engine/` - Core engine utilities
  - `STRR/assets/` - Data, graphics, audio assets
  - `STRR/config/` - TOML configuration files
- **MUST** store ALL test files in `STRR/tests/` directory
- **MUST** maintain proper `__init__.py` files and package organization
- **MUST** create `_doc.md` files alongside Python modules for documentation

### Linux Environment Compliance
- **PYTHON VERSION**: Ensure compatibility with Python 3.14+.
- **IMPORTANT** All refactored code designed for Linux environments only
- **MUST** use Linux-specific paths, commands, and system calls where appropriate
- **NOT COMPATIBLE** with Windows environments

## Refactoring Decision Framework

### When refactoring, prioritize:
1. **DRY Violations**: Can this logic be unified with existing implementations?
2. **Standard Library**: Can external dependencies be replaced with built-in solutions?
3. **Type Safety**: Are all elements properly typed and documented?
4. **Confident Design**: Can defensive patterns be replaced with architectural solutions?
5. **Reusability**: Can this be generalized for use by other projects?

## Game-Specific Refactoring Patterns

### Hybrid Architecture Compliance
**State Machine + Game Object + Component + MVC**

✅ **Good - Clear Separation:**
```python
# Model (game logic only)
class WeaponSystem:
    def calculate_damage(self, target_distance: int) -> int:
        """Calculate damage based on distance."""
        return max(0, self.base_damage - (target_distance * 2))

# View (rendering only)
class WeaponRenderer:
    def render_weapon_fire(self, source: tuple[int, int, int],
                          target: tuple[int, int, int]) -> None:
        """Render weapon fire animation between 3D positions."""
        pass  # pygame-ce rendering code
```

❌ **Bad - Mixed Concerns:**
```python
class WeaponSystem:
    def fire(self, target):
        damage = self.calculate_damage()
        target.take_damage(damage)
        # ❌ Rendering in game logic!
        pygame.draw.line(self.screen, RED, self.pos, target.pos)
```

### Component System Refactoring
**GameObject composition over inheritance**

✅ **Good - Component Composition:**
```python
class Starship:
    def __init__(self):
        self.components: dict[type, Any] = {}

    def add_component(self, component: Any) -> None:
        self.components[type(component)] = component

    def get_component(self, component_type: type[T]) -> T | None:
        return self.components.get(component_type)

ship = Starship()
ship.add_component(WeaponSystem(damage=50))
ship.add_component(ShieldSystem(capacity=100))
```

❌ **Bad - Deep Inheritance:**
```python
class Entity:
    pass

class Ship(Entity):
    pass

class ArmedShip(Ship):
    pass

class FederationShip(ArmedShip):  # ❌ Too deep!
    pass
```

### 3D Grid System Refactoring
**Always use (x, y, z) coordinates**

✅ **Good - 3D Positioning:**
```python
def calculate_distance_3d(self, pos1: tuple[int, int, int],
                         pos2: tuple[int, int, int]) -> float:
    """Calculate 3D distance between positions."""
    dx = pos2[0] - pos1[0]
    dy = pos2[1] - pos1[1]
    dz = pos2[2] - pos1[2]
    return math.sqrt(dx*dx + dy*dy + dz*dz)
```

❌ **Bad - 2D Only:**
```python
def calculate_distance(self, pos1: tuple[int, int],
                       pos2: tuple[int, int]) -> float:
    # ❌ Ignores z-level!
    return math.sqrt((pos2[0]-pos1[0])**2 + (pos2[1]-pos1[1])**2)
```

### Turn-Based Mechanics Refactoring
**All actions must consume turns**

✅ **Good - Turn Consumption:**
```python
def execute_move_action(self, ship: Starship, target_pos: tuple[int, int, int]) -> None:
    """Execute movement and advance turn."""
    ship.position = target_pos
    self.turn_manager.advance_turn()  # ✅ Turn consumed
```

❌ **Bad - Forgetting Turns:**
```python
def move_ship(self, ship: Starship, target_pos: tuple[int, int, int]) -> None:
    ship.position = target_pos
    # ❌ No turn advancement!
```
