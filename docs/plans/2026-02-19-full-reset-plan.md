# Star Trek Retro Remake — Full Reset Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Clean up file clutter, fix all broken tests, and get the game to launch to a visible sector map.

**Architecture:** pygame-ce renders the game grid; PySide6 handles menus/dialogs. MVC pattern: `GameModel` (pure logic), `GameView` (rendering), `GameController` (input + coordination). Config loaded from TOML files via `ConfigManager`.

**Tech Stack:** Python 3.14, pygame-ce, PySide6, pytest, uv, ruff, mypy

---

## Context: What Is Broken and Why

Before touching anything, understand these three root causes:

**Root Cause 1 — Wrong import paths in 9 test files:**
`pyproject.toml` sets `pythonpath = ["STRR"]`, so the Python path root is `STRR/`. That means
`from src.game.application import ...` is correct. But 9 test files use `from STRR.src.game...`
which adds a second `STRR` prefix that doesn't exist on the path.

**Root Cause 2 — `import pygame` fails in test collection:**
`pygame-ce` may install as `pygame_ce` in newer versions, but our source uses `import pygame`.
We need to verify the actual installed module name and either fix the import or mock it.
Tests that don't render anything should mock pygame entirely.

**Root Cause 3 — ConfigManager not initialized in tests:**
`conftest.py` never calls `initialize_config_manager()`. Any test that directly or transitively
imports something that calls `get_config_manager()` at module level will crash at collection.
Fix: add an autouse `session`-scoped fixture that initializes config before anything else.

---

## Phase 1: File Cleanup

### Task 1: Delete sidecar `*_doc.md` files

**Files to delete (22 files):**
```
STRR/src/engine/compat_doc.md
STRR/src/engine/config_loader_doc.md
STRR/src/engine/config_manager_doc.md
STRR/src/engine/isometric_grid_doc.md
STRR/src/engine/paths_doc.md
STRR/src/game/ai/ship_ai_doc.md
STRR/src/game/application_doc.md
STRR/src/game/commands_doc.md
STRR/src/game/components/mission_manager_doc.md
STRR/src/game/components/ship_systems_doc.md
STRR/src/game/controller_doc.md
STRR/src/game/entities/base_doc.md
STRR/src/game/entities/starship_doc.md
STRR/src/game/events_doc.md
STRR/src/game/exceptions_doc.md
STRR/src/game/maps/galaxy_doc.md
STRR/src/game/maps/sector_doc.md
STRR/src/game/model_doc.md
STRR/src/game/states/sector_state_doc.md
STRR/src/game/states/state_machine_doc.md
STRR/src/game/ui/mission_dialogs_doc.md
STRR/src/game/view_doc.md
```

**Step 1: Delete all sidecar files**
```bash
find STRR/src -name "*_doc.md" -delete
```

**Step 2: Verify none remain**
```bash
find STRR/src -name "*_doc.md"
```
Expected: no output.

---

### Task 2: Delete root-level duplicate and stale files

**Files/dirs to delete:**
- `QT Designer Files/` — duplicated in `STRR/src/ui/designer/`
- `INTEGRATION_SUMMARY.md` — stale root-level doc
- `setup-branch-protection.sh` — replaced by git hooks
- `star_trek_retro_remake.egg-info/` — stale setuptools artifact
- `STRR/src/ui/designer/main_window.ui` — superseded by `main_window_complete.ui`
- `STRR/src/ui/designer/main_window_ui.py` — superseded by `main_window_complete_ui.py`

**Step 1: Delete**
```bash
rm -rf "QT Designer Files/"
rm -f INTEGRATION_SUMMARY.md
rm -f setup-branch-protection.sh
rm -rf star_trek_retro_remake.egg-info/
rm -f STRR/src/ui/designer/main_window.ui
rm -f STRR/src/ui/designer/main_window_ui.py
```

**Step 2: Verify what remains in designer/**
```bash
ls STRR/src/ui/designer/
```
Expected:
```
LAYOUT_REFERENCE.md
main_window_complete.ui
main_window_complete_ui.py
```

---

### Task 3: Add `CLAUDE.md` to project root

**Create:** `CLAUDE.md`

```markdown
# CLAUDE.md — Star Trek Retro Remake

## Project Overview

Turn-based, grid-based Star Trek strategy game. v0.0.x is pre-alpha infrastructure.
The game cannot yet be played end-to-end; see docs/ROADMAP.md for the milestone plan.

## Architecture

Hybrid State Machine + MVC + Component pattern:
- `STRR/src/game/model.py` — pure game logic, no UI imports
- `STRR/src/game/view.py` — PySide6 window + pygame-ce rendering surface
- `STRR/src/game/controller.py` — input handling, state coordination
- `STRR/src/game/states/` — state machine (sector map, galaxy map, combat)
- `STRR/src/game/entities/` — Starship, SpaceStation, etc.
- `STRR/src/game/components/` — ShipSystems, MissionManager
- `STRR/src/engine/` — Config, paths, isometric grid, pygame-ce compat

pygame-ce handles the game surface (grid, ships, combat). PySide6 handles all
menus, dialogs, and settings panels. They share a single process; the pygame
surface is embedded in a QLabel inside the PySide6 main window.

## Branch Rules

- Work on `testing` branch
- Never push directly to `main`
- Check branch: `git branch --show-current`

## Commands

```bash
# Run the game
uv run python -m STRR.main

# Run tests
uv run pytest STRR/tests/ -v

# Run only unit tests (no display needed)
uv run pytest STRR/tests/ -m unit -v

# Type check
uv run mypy STRR/src/

# Lint
uv run ruff check STRR/src/ STRR/tests/
```

## Config Files

All TOML, all in `STRR/config/`:
- `game_settings.toml` — display, audio, controls
- `game_data.toml` — ship classes, factions
- `key_bindings.toml` — keyboard/mouse bindings

Config must be initialized before use: `initialize_config_manager(config_dir)`.
In tests, the `config_manager` autouse fixture in `conftest.py` handles this.

## Import Paths

`pyproject.toml` sets `pythonpath = ["STRR"]`. All imports in tests and source
use `from src.game...` or `from src.engine...` (NOT `from STRR.src.game...`).
```

**Step 1: Verify the file was created with correct content**
```bash
head -5 CLAUDE.md
```
Expected: `# CLAUDE.md — Star Trek Retro Remake`

---

### Task 4: Commit Phase 1

```bash
git add -A
git status
git commit -m "chore: phase 1 cleanup - remove sidecar docs and duplicate files"
```

---

## Phase 2: Fix Imports and Tests

### Task 5: Diagnose pygame installation

Before fixing anything, confirm what module name pygame-ce installs as.

**Step 1: Check installed module**
```bash
uv run python -c "import pygame; print(pygame.__version__)" 2>&1
```

Expected success: prints version like `2.5.3`

If it fails with `No module named 'pygame'`, try:
```bash
uv run python -c "import pygame_ce; print(pygame_ce.__version__)"
```

**Step 2: If pygame works** — the test failures were a venv artifact, nothing to fix.

**Step 3: If `import pygame` fails but `import pygame_ce` works** — add to `conftest.py`:
```python
import sys
import pygame_ce
sys.modules['pygame'] = pygame_ce
```
This aliases `pygame_ce` as `pygame` for all tests.

---

### Task 6: Fix `conftest.py` — add ConfigManager autouse fixture

**Modify:** `STRR/tests/conftest.py`

Find the existing fixture block that begins:
```python
from src.game.entities.base import GridPosition
```
(around line 82)

Add **before** those imports, at the top of the fixture section:

```python
from src.engine.config_manager import initialize_config_manager

@pytest.fixture(scope="session", autouse=True)
def initialized_config():
    """Initialize ConfigManager once for the entire test session.

    Without this, any test that imports from src.game.commands (or any module
    that calls get_config_manager() at import time) will fail during collection.
    The config dir path mirrors what application.py uses at runtime.
    """
    config_dir = Path(__file__).parent.parent / "config"
    initialize_config_manager(config_dir)
```

**Step 1: Verify the fix works for commands tests**
```bash
uv run pytest STRR/tests/test_commands.py -v --tb=short 2>&1 | tail -20
```
Expected: all or most tests pass (not ConfigurationError failures).

---

### Task 7: Fix import paths in the 9 broken test files

Each of these files uses `from STRR.src.game...` or `from STRR.src.engine...`.
Replace with `from src.game...` / `from src.engine...`.

**Files and the exact bad imports to fix:**

**`STRR/tests/test_application.py` line 30:**
```python
# Before:
from STRR.src.game.application import StarTrekRetroRemake
# After:
from src.game.application import StarTrekRetroRemake
```

**`STRR/tests/test_controller.py` lines 35-38:**
```python
# Before:
from STRR.src.game.controller import GameController
from STRR.src.game.entities.base import GridPosition
from STRR.src.game.model import GameModel
from STRR.src.game.states.state_machine import GameMode
# After:
from src.game.controller import GameController
from src.game.entities.base import GridPosition
from src.game.model import GameModel
from src.game.states.state_machine import GameMode
```

**`STRR/tests/test_mission_dialogs.py` line 17:**
```python
# Before:
from STRR.src.game.components.mission_manager import (
# After:
from src.game.components.mission_manager import (
```

**`STRR/tests/test_settings_dialog.py` line 17:**
```python
# Before:
from STRR.src.game.ui.settings_dialog import (
# After:
from src.game.ui.settings_dialog import (
```

**`STRR/tests/test_sector_state.py` lines 32-33:**
```python
# Before:
from STRR.src.game.states.sector_state import SectorState
from STRR.src.game.states.state_machine import GameMode
# After:
from src.game.states.sector_state import SectorState
from src.game.states.state_machine import GameMode
```

**`STRR/tests/test_ship_systems.py` lines 34-42:**
```python
# Before:
from STRR.src.game.components.ship_systems import (
...
from STRR.src.game.entities.base import GridPosition
# After:
from src.game.components.ship_systems import (
...
from src.game.entities.base import GridPosition
```

**`STRR/tests/test_isometric_grid.py` lines 35-41:**
```python
# Before:
from STRR.src.engine.isometric_grid import (
...
from STRR.src.game.entities.base import GridPosition
# After:
from src.engine.isometric_grid import (
...
from src.game.entities.base import GridPosition
```

**`STRR/tests/test_resource_management.py` lines 31-33:**
```python
# Before:
from STRR.src.game.components.ship_systems import CrewManager, ResourceManager
from STRR.src.game.entities.base import GridPosition
from STRR.src.game.entities.starship import Starship
# After:
from src.game.components.ship_systems import CrewManager, ResourceManager
from src.game.entities.base import GridPosition
from src.game.entities.starship import Starship
```

**`STRR/tests/test_mission_manager.py` line 44:**
```python
# Before:
from STRR.src.game.components.mission_manager import (
# After:
from src.game.components.mission_manager import (
```

**Step 1: After each file edit, verify it collects**
```bash
uv run pytest STRR/tests/test_application.py --collect-only 2>&1 | tail -5
```
Expected: collected N items (no errors).

Repeat for each file.

**Step 2: After all files fixed, check full collection**
```bash
uv run pytest STRR/tests/ --collect-only 2>&1 | tail -10
```
Expected: 0 errors, all test files collected.

---

### Task 8: Fix duplicate `initialize_config_manager()` call in `application.py`

**Modify:** `STRR/src/game/application.py`

In `_initialize_systems()`, there are two calls to `initialize_config_manager()` (lines 130 and 144).
Delete lines 128-130 (the first call with the wrong path calculation):

```python
# DELETE these 3 lines (the first initialize_config_manager call):
# Initialize configuration manager FIRST (required by other systems)
config_dir = Path(__file__).parents[2] / "config"
initialize_config_manager(config_dir)
```

Keep only the second call:
```python
# Initialize configuration manager with config directory
# Path: STRR/src/game/application.py -> STRR/config/
config_dir = Path(__file__).parent.parent.parent / "config"
initialize_config_manager(config_dir)
```

**Step 1: Verify path resolves correctly**
```bash
uv run python -c "
from pathlib import Path
# Simulate __file__ = STRR/src/game/application.py
f = Path('STRR/src/game/application.py').resolve()
print('config dir:', f.parent.parent.parent / 'config')
"
```
Expected: path ending in `STRR/config`

---

### Task 9: Run full test suite and record baseline

```bash
uv run pytest STRR/tests/ -v --tb=short 2>&1 | tee /tmp/test_baseline.txt
tail -20 /tmp/test_baseline.txt
```

Expected: all tests collect (0 errors). Some tests may still fail — that's OK.
The goal for Phase 2 is: **0 collection errors**, not 0 failures.

Document which tests still fail and why. These are the Phase 3 targets.

---

### Task 10: Commit Phase 2

```bash
git add -A
git commit -m "fix: phase 2 - fix test import paths and test infrastructure"
```

---

## Phase 3: Get the Game Running

### Task 11: Audit the startup sequence

**Step 1: Try to run the game**
```bash
uv run python -m STRR.main 2>&1
```

Note the exact error (don't try to fix yet). Common issues:
- `ModuleNotFoundError` — import path problem in main.py
- `pygame.error: No video mode set` — pygame init order issue
- `QApplication must be created before...` — Qt init order issue

**Step 2: Check main.py import**

`STRR/main.py` does:
```python
sys.path.insert(0, str(Path(__file__).parent / "src"))
from src.game.application import StarTrekRetroRemake
```

This adds `STRR/src` to the path, but also adds `STRR/` via `pyproject.toml`.
The `sys.path.insert` and the package path can conflict. Remove the `sys.path.insert`
if the package is properly installed via `uv` (which it should be — `pyproject.toml`
entry point `star-trek-retro-remake = "STRR.main:main"` + `pythonpath = ["STRR"]`).

---

### Task 12: Fix `main.py` startup

**Modify:** `STRR/main.py`

The `sys.path.insert` hack conflicts with the uv-managed package path.
Since uv/pyproject.toml already sets `pythonpath = ["STRR"]`, remove it:

```python
# DELETE this block:
# Add src directory to Python path to enable module imports from STRR/src/
sys.path.insert(0, str(Path(__file__).parent / "src"))
```

And fix the import:
```python
# Before:
from src.game.application import StarTrekRetroRemake

# After (using the package-relative path):
from STRR.src.game.application import StarTrekRetroRemake
```

Wait — this conflicts with Phase 2 where we fixed tests to use `from src.game...`.
The difference is: **test runner** has `STRR/` on sys.path (from `pythonpath = ["STRR"]`),
so `from src.game...` works in tests. But **main.py** is inside `STRR/`, so it needs
either relative imports or an explicit path.

The cleanest fix: use relative imports in main.py since it's inside the package.

```python
# STRR/main.py — use relative import
from .src.game.application import StarTrekRetroRemake
```

But this only works if main.py is run as a module (`python -m STRR.main`), not as a script.
Since pyproject.toml declares `star-trek-retro-remake = "STRR.main:main"`, module execution
is correct. Verify with:

```bash
uv run python -m STRR.main 2>&1 | head -20
```

---

### Task 13: Verify config loads at startup

If the game crashes with a ConfigurationError, check `application.py` line 143:
```python
config_dir = Path(__file__).parent.parent.parent / "config"
```

From `STRR/src/game/application.py`:
- `__file__.parent` = `STRR/src/game/`
- `__file__.parent.parent` = `STRR/src/`
- `__file__.parent.parent.parent` = `STRR/`
- `STRR/ / "config"` = `STRR/config` ✓

This is correct. If it still fails, print the resolved path:
```bash
uv run python -c "
from pathlib import Path
f = Path('STRR/src/game/application.py').resolve()
print(f.parent.parent.parent / 'config')
print('exists:', (f.parent.parent.parent / 'config').exists())
"
```

---

### Task 14: Fix pygame init for headless/display issues

If the game fails with `pygame.error: No video mode set` or display issues:

In `application.py` `_initialize_systems()`, ensure pygame init comes AFTER QApplication:

```python
def _initialize_systems(self) -> None:
    # 1. Config FIRST — required by view during init
    config_dir = Path(__file__).parent.parent.parent / "config"
    initialize_config_manager(config_dir)

    # 2. Qt SECOND — must exist before pygame embeds in it
    if not QApplication.instance():
        self.qt_app = QApplication(sys.argv)
    else:
        self.qt_app = QApplication.instance()

    # 3. pygame LAST — after Qt window exists
    pygame.init()
```

**Step 1: Test**
```bash
uv run python -m STRR.main 2>&1 | head -20
```

---

### Task 15: Verify game window opens

**Success criteria:** Running `uv run python -m STRR.main` should:
1. Open a PySide6 window (the main game window)
2. Show the sector map (even if placeholder/empty)
3. Not crash within 5 seconds

If the window opens but the sector map is blank, that is acceptable for Phase 3.

**Step 1: Manual test**
```bash
uv run python -m STRR.main
```
Close the window after confirming it opens. Note any errors in the terminal.

**Step 2: Commit Phase 3**
```bash
git add -A
git commit -m "fix: phase 3 - fix startup sequence, game launches to sector map"
```

---

## Phase 4: Development Roadmap

### Task 16: Write `docs/ROADMAP.md`

Create `docs/ROADMAP.md`:

```markdown
# Star Trek Retro Remake — Development Roadmap

Current version: v0.0.30 (infrastructure baseline)

## v0.1.0 — Playable Sector Map

**Goal:** Player can actually play a turn.

- [ ] Ship renders on isometric grid at starting position
- [ ] Player clicks grid cell to move ship
- [ ] Movement validated (bounds, obstacles, fuel cost)
- [ ] Turn counter advances
- [ ] Ship stats (shields, hull) visible in side panel

## v0.2.0 — Combat Prototype

**Goal:** Ships can fight.

- [ ] Enemy ship placed in sector
- [ ] Player selects enemy as target
- [ ] Fire phasers: damage calculated and applied
- [ ] Fire torpedoes: separate damage model
- [ ] Combat log shows results
- [ ] Win condition: enemy destroyed
- [ ] Lose condition: player hull = 0

## v0.3.0 — Galaxy Map + Sector Travel

**Goal:** Multiple sectors to explore.

- [ ] Galaxy map renders (overview of sectors)
- [ ] Player ship visible on galaxy map
- [ ] Player can warp to adjacent sector
- [ ] Each sector has different composition (stars, stations, enemies)

## v0.4.0 — Mission System

**Goal:** Things to do.

- [ ] Mission briefing shown at game start
- [ ] Mission tracker shows current objective
- [ ] Complete a mission (reach location, defeat enemy)
- [ ] Mission rewards (crew XP, resources)

## v0.5.0 — Save/Load

**Goal:** Games persist between sessions.

- [ ] Save game to file (TOML)
- [ ] Load game from file
- [ ] Game over screen with restart option

## Infrastructure Debt (ongoing)

- [ ] All tests pass: `uv run pytest` green
- [ ] Type check clean: `uv run mypy STRR/src/`
- [ ] No ruff errors: `uv run ruff check STRR/`
- [ ] Graphics assets for ships (at minimum placeholder sprites)
```

**Step 1: Commit Phase 4**
```bash
git add docs/ROADMAP.md
git commit -m "docs: add ROADMAP.md with milestone plan to v0.5.0"
```

---

## Final Verification

### Task 17: End-to-end check

Run this sequence to confirm everything works:

```bash
# 1. Tests collect and (mostly) pass
uv run pytest STRR/tests/ --collect-only 2>&1 | grep "error"
# Expected: no output (zero errors)

uv run pytest STRR/tests/ -q 2>&1 | tail -5
# Expected: some passing, any failures are known/documented

# 2. Linting passes
uv run ruff check STRR/src/ 2>&1
# Expected: no output or only pre-existing warnings

# 3. Game launches
uv run python -m STRR.main
# Expected: window opens, close it, no crash on exit
```

**Commit:**
```bash
git add -A
git commit -m "chore: v0.0.30 - full reset complete, game launches, tests collect"
```
