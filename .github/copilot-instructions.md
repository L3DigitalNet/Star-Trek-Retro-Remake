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
- Include shebang (`#!/usr/bin/env python3`) and encoding (`# -*- coding: utf-8 -*-`)
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
21. **Header Compliance:** All files have proper shebang, encoding, and complete docstring headers

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
