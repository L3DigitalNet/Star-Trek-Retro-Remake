# Star Trek Retro Remake - Game Development Instructions

## Project Overview
This repository contains **Star Trek Retro Remake**, a single Python game project that recreates classic Star Trek gaming experiences using modern development practices.

## Notes
- Game uses Python 3.14+ features (e.g., `Path.copy()`)
- #fetch https://docs.python.org/3.14/index.html for latest stdlib documentation
- Primary frameworks: PyGame (game engine) and PyQt6 (UI/menus)

## Critical Requirements (AI Priority Order)

### 1. Environment & Dependencies
- **Linux-only:** All code for Linux environments exclusively
- **Core frameworks:** PyGame for game engine, PyQt6 for UI and menus
- **Standard library first:** Use Python stdlib before additional external dependencies
- **Justify externals:** Comment why stdlib/PyGame/PyQt6 is insufficient when adding dependencies
- **Key modules:** `pathlib`, `json`, `csv`, `datetime`, `collections`, `itertools`, `functools`

### 2. Game Architecture
- **Game pattern:** Implement ECS (Entity-Component-System) or Game Object pattern
- **Core frameworks:** PyGame for game engine, PyQt6 for UI/menus/settings
- **Game loop:** Fixed timestep input → update → render cycle
- **State management:** Game state machine (menu, playing, paused, game over)
- **Separation:** Game logic separate from rendering and UI
- **Memory management:** Object pooling for efficient resource usage
- **DRY principle:** Use shared utilities for common game functionality
- **Confident design:** Avoid defensive programming, prefer clear initialization
- **Single source of truth:** Centralize game logic, eliminate duplication
- **Type safety:** Full type hints, modern union syntax (`str | None`)

### 3. Version Strategy
- **Error handling:** Defer until v1.0.0, focus on clean game architecture first
- **Testing focus:** Game logic, state transitions, and core mechanics before v1.0.0
- **Versioning:** MAJOR.MINOR.PATCH format, start at 0.0.1

## Technical Standards

### Python & Code Quality
- **Version:** Python 3.14+ minimum
- **Style:** Strict PEP 8, f-strings only (no `.format()` or `%`)
- **Types:** Full type hints everywhere - functions, variables, constants, collections
- **Modern syntax:** `str | None`, `list[str]`, `dict[str, int]`, `Final`, `Protocol`, `TypedDict`
- **Functions:** Small, focused, descriptive names, max 3 nesting levels

### File Structure (Required)
```python
# -*- coding: utf-8 -*-
"""
Star Trek Retro Remake - [Module Name]

Description:
    What this game module does and why.

Author: [Full Name]
Email: [email@domain.com]
GitHub: [https://github.com/username]
Date Created: [MM-DD-YYYY]
Date Changed: [MM-DD-YYYY]
License: [License Type]

Features:
    - Game loop with fixed timestep for consistent physics
    - State machine for menu, playing, paused, game over states
    - ECS (Entity-Component-System) architecture for game objects
    - Object pooling for efficient memory management
    - Separated game logic from rendering for testability
    - PyGame for game engine, PyQt6 for UI/menus
    - Standard library first approach
    - Clean confident design patterns

Requirements:
    - Linux environment
    - Python 3.14+ for latest language features
    - PyGame for game engine functionality
    - PyQt6 for UI, menus, and settings
    - Custom utilities located at ../common_lib/

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

### Documentation Format
```python
class ExampleClass:
    """
    Brief description of the class purpose.

    Attributes:
        attribute1: description of first attribute
        attribute2: description of second attribute
        attribute3: description of third attribute

    Public methods:
        method1: description of first public method
        method2: description of second public method

    Private methods:
        _private_method: description of private method

    Static methods:
        static_method: description of static method
    """
```

#### Function Docstring Format:
```python
def example_function(param1: str, param2: int) -> str:
    """
    Brief description of function purpose.

    Args:
        param1: description of first parameter
        param2: description of second parameter

    Returns:
        description of return value
    """
```

## Project Organization

### Structure
- **Template:** Use `templates/my_project_folder_template/`
- **Shared code:** `projects/common_lib/` for utilities
- **Tests:** ALL test files in project's `/tests/` directory
- **Config:** Separate files, never hardcode values
- **Docs:** README.md (root), PROJECT-DOC.md & CHANGELOG.md in `/docs/`

### Testing with pytest
- **Framework:** pytest only, AAA pattern (Arrange-Act-Assert)
- **Focus:** Core functionality and happy paths before v1.0.0
- **Coverage:** 80%+ for critical paths
- **Test behavior:** Program flow, type compliance, public interfaces
- **Files:** `test_*.py` with `test_*()` functions in `/tests/`
- **Features:** Use fixtures, parametrize, markers, descriptive names

### Version Management
- **Format:** MAJOR.MINOR.PATCH (start 0.0.1, v1.0.0 = first release)
- **Changelog:** Update `/docs/CHANGELOG.md` on version increment
- **Content:** Analyze code changes, categorize (Added/Changed/Fixed/Removed)
- **Headers:** Update "Date Changed" field when version updated

## AI Code Generation Rules

When generating code:

1. **Dependencies:** Standard library first, justify external dependencies
2. **Reuse:** Check existing codebase, consolidate duplicates, use `projects/common_lib/`
3. **Quality:** Complete examples, type hints for ALL elements, streamlined docstrings, proper headers
4. **Architecture:** Follow patterns, SOLID principles, composition over inheritance
5. **Confident Design:** Avoid defensive programming, use architectural solutions over scattered checks
6. **Version Awareness:** Defer error handling/validation until v1.0.0, focus on clean architecture
7. **Documentation:** Minimize .md file creation, avoid test summary docs, use README.md and single PROJECT-DOC.md per project
8. **Testing:** Use pytest framework, write tests for all business logic, follow pytest conventions
9. **Version Management:** Update CHANGELOG.md in `/docs/` folder when incrementing versions, document all changes
10. **Inline Comments:** Include comments for each significant code block for readability and AI context
11. **Type Safety:** Verify runtime behavior matches type annotations, use contract testing
12. **Architectural Patterns:** Implement proper separation of concerns and clear component boundaries

## Decision Framework

### When choosing between solutions:
1. **First:** Can Python standard library solve this?
2. **Second:** Does similar functionality already exist in the codebase?
3. **Third:** Can this be generalized for reuse by other projects?
4. **Last:** Is an external dependency truly necessary?

### Code smell indicators to avoid:
- Duplicate logic across files
- Hardcoded values that should be configurable
- Functions longer than 20 lines
- Missing type hints for functions, variables, constants, or data structures
- Untyped constants, module variables, class attributes, or collections
- Missing or inadequate docstrings
- Import statements for external libraries when standard library suffices
- Excessive defensive programming (scattered None checks, "just in case" conditionals)
- Complex nested conditionals that could be simplified with clear initialization
- Type hints that suggest uncertainty (Optional types) when values are guaranteed
