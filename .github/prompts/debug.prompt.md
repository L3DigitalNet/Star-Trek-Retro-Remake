---
description: "Analyze code for bugs and potential issues"
mode: "agent"
---

# Analyze and Debug Code

Analyze the code in ${file} or project to identify bugs, issues, and potential improvements.

## General Guidelines

- **IMPORTANT**: This is not a comprehensive code review or unit testing. Focus on identifying bugs, logical errors, performance issues, and potential improvements.
- **MANDATORY**: Code utilizes Python 3.14+ features and standard library where applicable. #fetch <https://docs.python.org/3.14/index.html> for latest stdlib documentation.
- **MANDATORY**: Follow repository guidelines in ![copilot-instructions.md](./copilot-instructions.md)
- **MANDATORY**: All code is designed for Linux environments only. Do not suggest Windows-specific solutions.
- **IMPORTANT**: Error handling is deferred until v1.0.0. Focus on clean architecture and core functionality first. Do not add error handling unless absolutely necessary to fix a bug.

## Game-Specific Debugging Focus

### Architecture Violations to Check

**MVC Separation Issues:**
- ❌ Rendering code (pygame-ce) in Models
- ❌ Game logic in Views
- ❌ Direct UI dependencies in game logic modules

**State Machine Issues:**
- ❌ Invalid state transitions (e.g., COMBAT → GALAXY_MAP without SECTOR_MAP)
- ❌ Missing state enter/exit handlers
- ❌ State not properly initialized

**Component System Issues:**
- ❌ Deep inheritance instead of composition
- ❌ Components with circular dependencies
- ❌ Missing component type checks

### Turn-Based Mechanics Bugs

**Common Issues:**
- ❌ Actions not consuming turns
- ❌ Turn counter not incrementing
- ❌ Initiative order not respected
- ❌ Multiple actions in single turn without cost

**Example Bug:**
```python
# ❌ BAD: Action doesn't advance turn
def fire_weapon(self, target):
    damage = self.weapon.calculate_damage()
    target.take_damage(damage)
    # Missing: self.turn_manager.advance_turn()

# ✅ GOOD: Turn properly consumed
def fire_weapon(self, target):
    damage = self.weapon.calculate_damage()
    target.take_damage(damage)
    self.turn_manager.advance_turn()
```

### 3D Grid System Bugs

**Common Issues:**
- ❌ Using 2D coordinates instead of 3D (x, y, z)
- ❌ Incorrect distance calculations (missing z-component)
- ❌ Range checks ignoring vertical positioning
- ❌ Grid bounds not validated for all 3 dimensions

**Example Bug:**
```python
# ❌ BAD: 2D distance only
def in_range(self, pos1: tuple[int, int], pos2: tuple[int, int]) -> bool:
    dist = math.sqrt((pos2[0]-pos1[0])**2 + (pos2[1]-pos1[1])**2)
    return dist <= self.weapon_range

# ✅ GOOD: Full 3D distance
def in_range(self, pos1: tuple[int, int, int], pos2: tuple[int, int, int]) -> bool:
    dx, dy, dz = pos2[0]-pos1[0], pos2[1]-pos1[1], pos2[2]-pos1[2]
    dist = math.sqrt(dx*dx + dy*dy + dz*dz)
    return dist <= self.weapon_range
```

### pygame-ce Integration Issues

**Common Issues:**
- ❌ pygame initialization in game logic (should be in view only)
- ❌ Direct screen.blit() calls in models
- ❌ Event handling mixed with game state updates
- ❌ Frame rate dependencies (use delta_time)

### Type Hint Validation

**Check for:**
- Missing type hints on functions/methods
- Incorrect collection types (use `list[str]` not `List[str]`)
- Missing `| None` for optional returns
- Outdated typing imports (use `from typing import Protocol`, not old syntax)

## Summary

Provide a concise summary of the project including bugs, issues, areas for improvement, and recommended changes. Focus specifically on:

1. **Architecture violations** (MVC separation, state machine, components)
2. **Turn-based mechanics** issues (turn consumption, initiative)
3. **3D positioning** bugs (coordinate handling, distance calculations)
4. **Type safety** problems (missing hints, incorrect types)
5. **Framework separation** issues (pygame in models, logic in views)
