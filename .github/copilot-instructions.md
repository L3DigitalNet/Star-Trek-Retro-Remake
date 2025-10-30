# Star Trek Retro Remake - Development Instructions

## Overview

Turn-based strategy game set in Kirk-era Star Trek universe. Features grid-based space exploration with 3D z-levels, tactical combat, and starship management.

**Key References:**

- Architecture details: `/docs/ARCHITECTURE.md`
- Game design: `/GDD/DESIGN.md`
- Python 3.14+ stdlib: https://docs.python.org/3.14/

## Architecture

**Pattern:** Hybrid State Machine + Game Object + Component + MVC
- **NOT full ECS** - Use Game Object with Component composition (simpler for turn-based games)
- **PyGame** for rendering (game view)
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
- Format: MAJOR.MINOR.PATCH (start 0.0.1)
- Defer error handling until v1.0.0
- Focus: clean architecture, core game logic, state transitions

## File Structure

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
    - PyGame for game rendering, PySide6 for UI/menus/dialogs
    - Standard library first approach
    - Clean confident design patterns

Requirements:
    - Linux environment
    - Python 3.14+ for latest language features
    - PyGame for game engine rendering
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
- Update `docs/CHANGELOG.md` on version changes
- Update "Date Changed" in file headers
- Categorize: Added/Changed/Fixed/Removed

## AI Code Generation Rules

1. **Dependencies:** Standard library first, justify external dependencies
2. **Reuse:** Check existing codebase, consolidate duplicates
3. **Quality:** Complete examples, type hints for ALL elements, proper headers
4. **Architecture:** Follow Hybrid State Machine + Game Object + Component + MVC, SOLID principles
5. **Game Systems:** Ship systems as components (WeaponSystems, ShieldSystems) not full ECS
6. **State Machine:** Use specific modes (GALAXY_MAP, SECTOR_MAP, COMBAT) not generic states
7. **Grid Logic:** 3D positioning (x, y, z) for all spatial calculations
8. **Turn-Based:** All actions advance turn counter, support initiative
9. **Framework Separation:** PyGame rendering separate from PySide6 UI
10. **Confident Design:** Architectural solutions over defensive checks
11. **Version Aware:** Defer error handling until v1.0.0
12. **Documentation:** Minimize .md creation, single PROJECT-DOC.md
13. **Testing:** pytest for business logic, AAA pattern
14. **Versioning:** Update CHANGELOG.md on changes
15. **Comments:** Inline for significant blocks
16. **Type Safety:** Runtime matches annotations
17. **Separation:** Clear component boundaries
18. **Pooling:** Reuse projectiles, effects, temporary objects

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
