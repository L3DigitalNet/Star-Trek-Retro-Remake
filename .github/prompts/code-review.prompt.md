---
description: "Comprehensive code review following repository guidelines"
mode: "agent"
---

# Comprehensive Code Review

Perform a complete code review of the project following repository guidelines.

## General Guidelines

- **MANDATORY**: Do not change any code logic or implementation, only suggest improvements
- **MANDATORY**: Follow all repository guidelines in ![copilot-instructions.md](../.github/copilot-instructions.md)
- **MANDATORY**: Code and design should reflect the project's overall design goals in ![DESIGN.md](../.github/DESIGN.md):

## CRITICAL: Linux Environment Only

- **IMPORTANT**: This repository is designed for **Linux environments ONLY**

## Core Standards

- **Python 3.14+ REQUIRED**: Minimum version with latest language features
- **Type hints MANDATORY**: ALL functions, methods, variables, constants, data structures, collections
- **PEP 8 compliance**: Strict formatting and style requirements
- **File headers**: Full docstring format with shebang, encoding, and complete metadata
- **Streamlined docstrings**: Brief descriptions, 80-char limit, leverage type hints

## Architecture

**Pattern:** Hybrid State Machine + Game Object + Component + MVC
- **NOT full ECS** - Use Game Object with Component composition (simpler for turn-based games)
- **pygame-ce** for rendering (game view) - Community Edition with Python 3.14+ support
- **PySide6** for UI (menus, dialogs, settings)
- **MVC separation** - Game logic independent of UI/rendering
- **Object pooling** for projectiles, effects, temporary entities

## Tooling

- **GUI Design:** Qt Designer for all UI layouts
- **Testing:** pytest framework for unit and integration tests

## Clean & Confident Design (Highest Priority)

- **PREFER confident, clean code** over defensive programming patterns
- **AVOID unnecessary null/None checks** when program flow guarantees valid values
- **PREFER explicit initialization** and clear program flow over defensive conditionals
- **Remove "just in case" code** that handles scenarios that shouldn't occur
- **Use architectural solutions** over scattered defensive checks
- **Precise types**: Use types that reflect actual program constraints, avoid defensive Optional
- **Linear flow**: Confident execution paths with proper initialization order

## Version-Aware Approach

- **BEFORE v1.0.0 (current)**: Focus on core functionality and clean architecture
- **DEFER comprehensive error handling** until v1.0.0 - use architectural solutions instead
- **NEVER** use bare `except:` statements in any version

## Game-Specific Review Checklist

### Hybrid Architecture Compliance
- [ ] **MVC Separation**: Models have no pygame/rendering code
- [ ] **State Machine**: Proper state transitions (GALAXY_MAP → SECTOR_MAP → COMBAT)
- [ ] **GameObject Pattern**: Entities use composition, not deep inheritance
- [ ] **Component Systems**: Ship systems (weapons, shields, engines) properly composed
- [ ] **Object Pooling**: Projectiles/effects use pooling, not constant instantiation

### Turn-Based Mechanics
- [ ] **Turn Consumption**: All actions advance turn counter
- [ ] **Initiative System**: Action order respects initiative values
- [ ] **Sequential Processing**: Actions processed one at a time
- [ ] **Turn State**: Game state properly saved/restored between turns

### 3D Grid System
- [ ] **3D Coordinates**: All positions use `(x, y, z)` tuples
- [ ] **Distance Calculations**: Include z-component in all distance checks
- [ ] **Range Validation**: Weapon/sensor range considers 3D space
- [ ] **Bounds Checking**: Grid validation for all 3 dimensions

### Framework Separation
- [ ] **pygame-ce**: Only in View layer (rendering)
- [ ] **PySide6**: Only for menus, dialogs, settings (not game rendering)
- [ ] **Game Logic**: No direct pygame Surface or PySide6 widget references in models
- [ ] **Event Handling**: Controller processes input, delegates to models

### Code Quality Standards
- [ ] **Type Hints**: ALL functions, variables, constants have type annotations
- [ ] **Modern Syntax**: Use `str | None`, `list[int]`, not old typing module syntax
- [ ] **File Headers**: Complete docstring with all required metadata
- [ ] **Inline Comments**: Significant code blocks documented
- [ ] **Docstrings**: Brief, leverage type hints (no redundant type documentation)

### Game-Specific Patterns

**✅ Good Examples:**
```python
# Clear MVC separation
class WeaponSystem:  # Model
    def calculate_damage(self, distance: int) -> int:
        return max(0, self.base_damage - distance * 2)

class WeaponRenderer:  # View
    def render_weapon_fire(self, start: tuple[int, int, int],
                          end: tuple[int, int, int]) -> None:
        # pygame rendering only
        pass

# Component composition
ship = Starship()
ship.add_component(WeaponSystem(damage=50))
weapons = ship.get_component(WeaponSystem)

# 3D positioning
def move_to(self, target: tuple[int, int, int]) -> None:
    self.position = target  # (x, y, z)
```

**❌ Common Issues:**
```python
# ❌ Rendering in model
class WeaponSystem:
    def fire(self):
        pygame.draw.line(...)  # Wrong layer!

# ❌ Deep inheritance
class FederationHeavyCruiser(ArmedShip(Ship(Entity))):
    pass  # Use composition!

# ❌ 2D coordinates
def distance(self, p1: tuple[int, int]) -> float:
    # Missing z-coordinate!
```

## Summary of Changes and Recommendations

After completing the code review, provide:

1. **Architecture Compliance**: Assessment of MVC/State Machine/Component adherence
2. **Game Mechanics**: Turn-based and 3D grid system correctness
3. **Code Quality**: Type hints, documentation, style compliance
4. **Framework Separation**: pygame-ce and PySide6 usage correctness
5. **Recommendations**: Prioritized improvements with examples
