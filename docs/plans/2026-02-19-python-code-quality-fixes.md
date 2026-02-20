# Python Code Quality Fixes Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Fix all 18 issues found in the Python skills code review (anti-patterns, type safety, testing, design, observability, style).

**Architecture:** All changes are isolated fixes within existing files — no new modules, no refactoring of architecture. MVC boundaries remain unchanged. Each task targets one concern.

**Tech Stack:** Python 3.14, pygame-ce, PySide6, mypy, ruff, pytest

**Working directory:** `/home/chris/projects/Star-Trek-Retro-Remake/.worktrees/code-quality`
**Branch:** `fix/python-code-quality`
**Run tests:** `uv run pytest STRR/tests/ -q` (expect 441+ passing)
**Type check:** `uv run mypy STRR/src/`
**Lint:** `uv run ruff check STRR/src/ STRR/tests/`

---

## Context

All source files have this structure at the top:
- Shebang: `#!/usr/bin/env python3`
- Full docstring block
- `__version__: Final[str] = "X.Y.Z"` constant
- `logger = logging.getLogger(__name__)`

Current version is `0.0.30`. Every file modified must have its `__version__` updated to `0.0.31` and "Date Changed" in the docstring updated to the current date.

---

### Task 1: Fix bare `except Exception: pass` in ship_systems.py

**Context:** `ResourceManager._load_config` (line ~927) and `CrewManager._load_config` (line ~1184) silently swallow ALL exceptions including `NameError`. This is the most dangerous issue — a config failure produces no error, no log, and broken state.

**Files:**
- Modify: `STRR/src/game/components/ship_systems.py`

**Step 1: Find the exact lines**

```bash
grep -n "except Exception" STRR/src/game/components/ship_systems.py
grep -n "import tomllib\|from pathlib" STRR/src/game/components/ship_systems.py | head -5
```

Note the line numbers — they'll be around 927 and 1184. Also check if `tomllib` and `Path` are already imported at module level.

**Step 2: Verify `tomllib` and `Path` are in the file's imports**

Read the top of the file (lines 1-60). `tomllib` should be a stdlib import. `Path` from `pathlib` should already be there since the project uses it widely.

**Step 3: Fix the two `_load_config` methods**

Replace both bare `except Exception: pass` blocks. The pattern in each method looks like:

```python
# WRONG — silent failure:
try:
    ...load config...
except Exception:
    pass

# CORRECT — specific exceptions with logging:
except (OSError, tomllib.TOMLDecodeError) as e:
    logger.warning("Failed to load resource config: %s", e)
```

If `tomllib` is not already imported at module top, add it to the stdlib imports block:
```python
import tomllib
```

**Step 4: Run tests**

```bash
uv run pytest STRR/tests/test_ship_systems.py -q
```
Expected: all pass.

**Step 5: Update version + commit**

Update `__version__` to `"0.0.31"` and "Date Changed" in ship_systems.py header.

```bash
git add STRR/src/game/components/ship_systems.py
git commit -m "fix: catch specific exceptions in ResourceManager and CrewManager _load_config"
```

---

### Task 2: Remove redundant `register_entity` call in `process_ai_turn`

**Context:** `GameModel.process_ai_turn` calls `self.turn_manager.register_entity(ship)` after every AI action. The ship is already registered. This triggers an unnecessary O(n log n) re-sort of all entities. The line should simply be deleted.

**Files:**
- Modify: `STRR/src/game/model.py`

**Step 1: Find the exact lines**

```bash
grep -n "process_ai_turn\|register_entity" STRR/src/game/model.py
```

The method will look like:
```python
def process_ai_turn(self, ship: Starship) -> None:
    if ship.ai_controller:
        ship.ai_controller.update(self)
        self.turn_manager.register_entity(ship)  # ← DELETE THIS LINE
```

**Step 2: Delete the `register_entity` call**

Remove only `self.turn_manager.register_entity(ship)`. Do not change anything else in the method.

**Step 3: Run tests**

```bash
uv run pytest STRR/tests/ -q
```
Expected: 441+ passing.

**Step 4: Update version + commit**

Update `__version__` to `"0.0.31"` in model.py.

```bash
git add STRR/src/game/model.py
git commit -m "fix: remove redundant register_entity call in process_ai_turn"
```

---

### Task 3: Fix `get_turn_status` return type with TypedDict

**Context:** `GameModel.get_turn_status()` returns `dict[str, int | str]`. The caller in `controller.py:467-469` unpacks it directly into `update_turn_info(turn_number=..., action_points=..., phase=...)` which expects `int, int, str`. mypy flags this as a type error. Fix: change the return type to a `TypedDict` so mypy knows exactly what's in each key.

**Files:**
- Modify: `STRR/src/game/model.py` (define TypedDict, update return type)
- Modify: `STRR/src/game/controller.py` (update call site if needed)

**Step 1: Find current `get_turn_status` definition**

```bash
grep -n "get_turn_status\|TurnStatus" STRR/src/game/model.py
```

It currently returns `dict[str, int | str]` and produces keys `"turn_number"`, `"action_points"`, `"current_phase"`.

**Step 2: Define a TypedDict in `model.py`**

Add near the top of `model.py` (after imports, before the class definitions):

```python
from typing import TypedDict

class TurnStatus(TypedDict):
    """Typed return value for GameModel.get_turn_status()."""
    turn_number: int
    action_points: int
    current_phase: str
```

**Step 3: Update `get_turn_status` return type**

Change the method signature:
```python
def get_turn_status(self) -> TurnStatus:
```

The return value (a dict literal) already satisfies this type because `TypedDict` is structurally compatible with dict literals.

**Step 4: Verify mypy passes on these two files**

```bash
uv run mypy STRR/src/game/model.py STRR/src/game/controller.py
```

The `int | str` errors on controller.py lines 467-469 should be gone.

**Step 5: Run tests**

```bash
uv run pytest STRR/tests/ -q
```
Expected: 441+ passing.

**Step 6: Update version + commit**

Update `__version__` in both modified files.

```bash
git add STRR/src/game/model.py STRR/src/game/controller.py
git commit -m "fix: use TypedDict for get_turn_status return type, fixing mypy errors in controller"
```

---

### Task 4: Fix `view.py` shield access and untyped signatures

**Context:** Two issues in `view.py`:
1. `ship.systems["shields"]` direct dict access — raises `KeyError` if shields absent, and bypasses the `get_system()` accessor
2. Several public methods lack type annotations (mypy errors)

**Files:**
- Modify: `STRR/src/game/view.py`

**Step 1: Find the shield dict access**

```bash
grep -n 'systems\["shields"\]' STRR/src/game/view.py
```

It looks like:
```python
shields_pct = (
    ship.systems["shields"].total_shield_strength
    / ship.systems["shields"].max_shield_strength
) * 100
```

**Step 2: Replace with safe `get_system()` call**

The safe pattern (using the existing accessor and proper type narrowing):

```python
from .components.ship_systems import ShieldSystems  # add if not present

shield_system = ship.get_system("shields")
if isinstance(shield_system, ShieldSystems):
    shields_pct = (
        shield_system.total_shield_strength
        / shield_system.max_shield_strength
    ) * 100
else:
    shields_pct = 0.0
```

Check if `ShieldSystems` is already imported in view.py's TYPE_CHECKING block. If so, add a local runtime import inside the method (following the project's established pattern for isinstance checks — see CLAUDE.md).

**Step 3: Find and annotate untyped public methods**

```bash
uv run mypy STRR/src/game/view.py 2>&1 | grep "error:" | head -20
```

For each untyped function (e.g. `render_sector_map`, `show_combat_dialog`, `show_ship_status`, `_render_game_object`), add annotations. Common types:
- `sector_map: SectorMap | None`
- `game_objects: list[GameObject]`
- `result: CombatResult`
- `ship: Starship`
- `obj: GameObject`
- Event handler parameters: use `pygame.event.Event` for pygame events, Qt events use their specific type

For `_render_game_object`, annotate as `obj: GameObject` — the method already uses `hasattr` guards for rendering-specific attributes.

**Step 4: Verify mypy errors reduce significantly**

```bash
uv run mypy STRR/src/game/view.py
```

**Step 5: Run tests**

```bash
uv run pytest STRR/tests/ -q
```
Expected: 441+ passing.

**Step 6: Update version + commit**

```bash
git add STRR/src/game/view.py
git commit -m "fix: use get_system() for shield access and add type annotations to view.py"
```

---

### Task 5: Fix remaining mypy errors in application.py and commands.py

**Context:** `application.py` has a missing `-> None` on `__init__`. `commands.py` has ~8 errors from accessing `ShipSystem` subtype attributes through the base type without narrowing.

**Files:**
- Modify: `STRR/src/game/application.py`
- Modify: `STRR/src/game/commands.py` (if it exists — check first)

**Step 1: Check what files have mypy errors**

```bash
uv run mypy STRR/src/ 2>&1 | grep "error:" | grep -v "test_\|compiled"
```

List all files with errors. For each:

**application.py:** Add `-> None` to `__init__`:
```python
def __init__(self, ...) -> None:
```

**commands.py (or similar):** For ShipSystem attribute access errors, use `isinstance` narrowing. Pattern:
```python
# WRONG — type error: ShipSystem has no attribute 'phaser_range'
weapon_sys = ship.get_system("weapons")
range = weapon_sys.phaser_range

# CORRECT — narrow to the specific subtype first
from .components.ship_systems import WeaponSystems
weapon_sys = ship.get_system("weapons")
if isinstance(weapon_sys, WeaponSystems):
    range = weapon_sys.phaser_range
```

**Step 2: Run mypy to confirm 0 errors**

```bash
uv run mypy STRR/src/
```
Target: 0 errors. If any remain, fix them before committing.

**Step 3: Run tests**

```bash
uv run pytest STRR/tests/ -q
```

**Step 4: Update versions + commit**

Update `__version__` in all modified files.

```bash
git add STRR/src/game/application.py STRR/src/game/commands.py
git commit -m "fix: resolve all mypy errors — add return types and narrow ShipSystem subtypes"
```

---

### Task 6: Replace legacy `typing` imports with modern syntax

**Context:** `sector.py`, `galaxy.py`, and `state_machine.py` import `Dict`, `List`, `Optional`, `Tuple` from `typing`. Python 3.14 (this project's baseline) uses `dict[...]`, `list[...]`, `X | None`, `tuple[...]` natively.

**Files:**
- Modify: `STRR/src/game/maps/sector.py`
- Modify: `STRR/src/game/maps/galaxy.py`
- Modify: `STRR/src/game/states/state_machine.py`

**Step 1: Find and replace in each file**

For each file, check imports:
```bash
grep -n "from typing import" STRR/src/game/maps/sector.py
grep -n "from typing import" STRR/src/game/maps/galaxy.py
grep -n "from typing import" STRR/src/game/states/state_machine.py
```

Replace in usage throughout each file:
- `Dict[K, V]` → `dict[K, V]`
- `List[T]` → `list[T]`
- `Optional[T]` → `T | None`
- `Tuple[A, B]` → `tuple[A, B]`

Remove `Dict`, `List`, `Optional`, `Tuple` from the `from typing import` line. Keep `Final`, `TYPE_CHECKING`, `TypedDict`, `Protocol` etc. if used.

**Step 2: Verify with ruff and mypy**

```bash
uv run ruff check STRR/src/game/maps/ STRR/src/game/states/
uv run mypy STRR/src/game/maps/ STRR/src/game/states/
```

**Step 3: Run tests**

```bash
uv run pytest STRR/tests/ -q
```

**Step 4: Update versions + commit**

Update `__version__` in all three files.

```bash
git add STRR/src/game/maps/sector.py STRR/src/game/maps/galaxy.py STRR/src/game/states/state_machine.py
git commit -m "fix: replace legacy typing imports with modern Python 3.10+ syntax"
```

---

### Task 7: Fix ShipAI private method coupling and remove stale docstring

**Context:**
1. `ship_ai.py` calls `model._is_valid_move()` (a private method) 3 times — coupling AI to implementation details
2. Class docstring lists `_assess_threat` as a method but it doesn't exist

**Files:**
- Modify: `STRR/src/game/ai/ship_ai.py`
- Modify: `STRR/src/game/model.py` (add public method)

**Step 1: Find the private method calls**

```bash
grep -n "_is_valid_move" STRR/src/game/ai/ship_ai.py STRR/src/game/model.py
```

**Step 2: Add public `is_valid_move()` to `GameModel`**

In `model.py`, add a public wrapper that delegates to the private one:

```python
def is_valid_move(self, entity: Starship, destination: GridPosition) -> bool:
    """Check if a move is valid for the given entity (public API for AI)."""
    return self._is_valid_move(entity, destination)
```

Place it near the other public movement methods.

**Step 3: Update `ship_ai.py` to use the public method**

Replace all 3 occurrences of `model._is_valid_move(...)` with `model.is_valid_move(...)`.

**Step 4: Remove `_assess_threat` from docstring**

Find the class docstring in `ship_ai.py` and remove the line referencing `_assess_threat`.

**Step 5: Run tests**

```bash
uv run pytest STRR/tests/ -q
```

**Step 6: Update versions + commit**

```bash
git add STRR/src/game/ai/ship_ai.py STRR/src/game/model.py
git commit -m "fix: expose is_valid_move as public API and remove stale _assess_threat docstring"
```

---

### Task 8: Add pytest markers to all test files

**Context:** The CLAUDE.md documents `pytest -m unit -v` for headless CI, but NO test has any markers. Zero tests are collected when using `-m unit`. This task adds `@pytest.mark.unit` to all non-GUI tests and `@pytest.mark.gui` to tests that require a display.

**Files:**
- Modify: All files in `STRR/tests/` (except `conftest.py`)

**Step 1: Check what markers are already registered**

```bash
grep -n "markers\|filterwarnings" STRR/pyproject.toml 2>/dev/null || grep -n "markers" pyproject.toml
```

The `pyproject.toml` `[tool.pytest.ini_options]` section should have a `markers` list. If it doesn't, add:

```toml
[tool.pytest.ini_options]
markers = [
    "unit: fast unit tests, no display required",
    "gui: tests requiring a display server (Xvfb or real display)",
    "integration: integration tests",
]
```

**Step 2: Identify which tests need `gui` marker**

Tests that import or use `pygame.display`, `QApplication`, `GameDisplay`, `GameView`, or `GameController` with actual rendering need `@pytest.mark.gui`. All others get `@pytest.mark.unit`.

Known GUI test files (from collection errors without display):
- `test_application.py`
- `test_sector_state.py`
- `test_settings_dialog.py`
- `test_state_machine.py`
- `test_isometric_grid.py`
- `test_controller.py` (uses pygame)

Check each test file's imports to confirm.

**Step 3: Add markers to each file**

For unit test files, add at the class level using `pytestmark`:
```python
import pytest

pytestmark = pytest.mark.unit
```

For GUI test files:
```python
import pytest

pytestmark = pytest.mark.gui
```

Place the `pytestmark` assignment after imports, before the first test class.

**Step 4: Verify markers work**

```bash
uv run pytest STRR/tests/ -m unit --co -q 2>&1 | tail -5
```
Should show many tests collected, 0 errors.

```bash
uv run pytest STRR/tests/ -m unit -q
```
Should pass all unit tests.

**Step 5: Run full suite**

```bash
uv run pytest STRR/tests/ -q
```

**Step 6: Commit**

```bash
git add STRR/tests/ pyproject.toml
git commit -m "fix: add pytest markers (unit/gui) to all test files"
```

---

### Task 9: Fix version inconsistencies and `Final[str]` annotations

**Context:**
- `application.py` has `__version__ = "0.0.28"` (behind)
- `controller.py` has `__version__ = "0.0.26"` (behind)
- `ship_systems.py` and `ship_ai.py` have `__version__ = "0.0.30"` without `Final[str]` type annotation

All should be `0.0.31` with `Final[str]` annotation, consistent with every other file.

**Files:**
- Modify: `STRR/src/game/application.py`
- Modify: `STRR/src/game/controller.py`
- Modify: `STRR/src/game/components/ship_systems.py`
- Modify: `STRR/src/game/ai/ship_ai.py`

**Step 1: Find version lines**

```bash
grep -n "__version__" STRR/src/game/application.py STRR/src/game/controller.py STRR/src/game/components/ship_systems.py STRR/src/game/ai/ship_ai.py
```

**Step 2: Update each**

For files with missing `Final[str]`:
```python
# WRONG:
__version__ = "0.0.30"

# CORRECT:
__version__: Final[str] = "0.0.31"
```

Ensure `Final` is imported — it comes from `from typing import Final`. Most files already have this.

Also update "Date Changed" in each file's docstring header to today's date.

**Step 3: Run tests**

```bash
uv run pytest STRR/tests/ -q
```

**Step 4: Commit**

```bash
git add STRR/src/game/application.py STRR/src/game/controller.py STRR/src/game/components/ship_systems.py STRR/src/game/ai/ship_ai.py
git commit -m "chore: standardize __version__ to 0.0.31 with Final[str] annotation across all files"
```

---

### Task 10: Fix f-string logging to `%`-format

**Context:** Several spots use `logger.info(f"msg {value}")` which always evaluates the f-string. The correct pattern `logger.info("msg %s", value)` defers string interpolation — if the log level suppresses the message, no string is allocated.

**Files:**
- Modify: `STRR/src/game/view.py`
- Modify: `STRR/src/game/controller.py`

**Step 1: Find all f-string log calls**

```bash
grep -n 'logger\.\(debug\|info\|warning\|error\)(f"' STRR/src/game/view.py STRR/src/game/controller.py
```

**Step 2: Replace each**

Pattern:
```python
# WRONG:
logger.info(f"Zoom in: {self.grid_renderer.zoom_level:.2f}x")
logger.debug(f"Processing mouse click at screen position: {mouse_pos}")

# CORRECT:
logger.info("Zoom in: %.2fx", self.grid_renderer.zoom_level)
logger.debug("Processing mouse click at screen position: %s", mouse_pos)
```

Note: For format specs like `:.2f`, use `%.2f` in %-format strings.

**Step 3: Verify no f-string log calls remain**

```bash
grep -n 'logger\.\(debug\|info\|warning\|error\)(f"' STRR/src/game/view.py STRR/src/game/controller.py
```
Expected: no output.

**Step 4: Run tests**

```bash
uv run pytest STRR/tests/ -q
```

**Step 5: Commit**

```bash
git add STRR/src/game/view.py STRR/src/game/controller.py
git commit -m "fix: replace f-string logger calls with %-format for deferred interpolation"
```

---

### Task 11: Move deferred imports to module level

**Context:** `resolve_combat` in `model.py` imports `random` and `get_combat_config` inside the function body. `random` is stdlib (cheap but stylistically wrong). The config import runs on every combat resolution. These belong at module level.

Similar: `import math` deferred inside methods in other files.

**Files:**
- Modify: `STRR/src/game/model.py`
- Check and fix other files as needed

**Step 1: Find deferred stdlib/non-isinstance imports**

```bash
grep -rn "^\s*import math\|^\s*import random\|^\s*from.*import.*config" STRR/src/game/ | grep -v "TYPE_CHECKING\|isinstance"
```

Note: Local imports for `isinstance()` checks are correct and intentional (see CLAUDE.md). Only move imports that are NOT guarding `isinstance()` calls.

**Step 2: Move each to module level**

In `model.py`, the `import random` inside `resolve_combat` should move to the top imports block with other stdlib imports. Same for `from ..engine.config_loader import get_combat_config`.

Pattern:
```python
# At the TOP of the file, in the stdlib/local imports block:
import random
from ..engine.config_loader import get_combat_config

# REMOVE these lines from inside resolve_combat()
```

**Step 3: Run tests**

```bash
uv run pytest STRR/tests/ -q
```

**Step 4: Commit**

```bash
git add STRR/src/game/model.py
git commit -m "fix: move deferred stdlib and config imports to module level"
```

---

### Task 12: Fix `object` type in sector.py and galaxy.py entity maps

**Context:** `SectorMap.entities` is typed as `dict[GridPosition, object]`. Since all entities are `GameObject` subclasses, replacing `object` with `GameObject` activates type checking for all entity placement operations with no behavioral change.

**Files:**
- Modify: `STRR/src/game/maps/sector.py`
- Modify: `STRR/src/game/maps/galaxy.py`

**Step 1: Find all `object` usages in entity context**

```bash
grep -n ": object\|, object" STRR/src/game/maps/sector.py STRR/src/game/maps/galaxy.py
```

**Step 2: Replace `object` with `GameObject`**

Ensure `GameObject` is imported — it's from `..entities.base`:
```python
from ..entities.base import GameObject, GridPosition
```

Replace `object` with `GameObject` in:
- Type annotations on `entities` dict
- Method parameters (`place_entity`, `remove_entity`, `get_entity`, etc.)
- Any local variable annotations

**Step 3: Run mypy to confirm improved type coverage**

```bash
uv run mypy STRR/src/game/maps/
```

**Step 4: Run tests**

```bash
uv run pytest STRR/tests/test_maps.py -q
```

**Step 5: Update versions + commit**

```bash
git add STRR/src/game/maps/sector.py STRR/src/game/maps/galaxy.py
git commit -m "fix: type entity maps as dict[GridPosition, GameObject] instead of object"
```

---

### Task 13: Fix broken reward delivery in MissionManager

**Context:** `MissionManager.complete_mission` uses `getattr(player_ship, "resource_manager", None)` to deliver rewards. But `Starship` has no `resource_manager` attribute — it has `ship.systems["resources"]` (a `ResourceManager` component). The reward system silently does nothing.

**Files:**
- Modify: `STRR/src/game/components/mission_manager.py`

**Step 1: Find the broken getattr**

```bash
grep -n "resource_manager\|complete_mission\|reward" STRR/src/game/components/mission_manager.py
```

**Step 2: Fix the reward delivery**

Replace the broken `getattr` with the correct component access:

```python
# WRONG — attribute doesn't exist on Starship:
resource_manager = getattr(player_ship, "resource_manager", None)
if resource_manager:
    resource_manager.add_resources(...)

# CORRECT — use the ship systems dict:
from .ship_systems import ResourceManager
resource_system = player_ship.get_system("resources")
if isinstance(resource_system, ResourceManager):
    resource_system.add_resources(...)  # adjust to actual method name
```

Check `ResourceManager`'s actual API (in `ship_systems.py`) for the correct method name to add resources.

**Step 3: Add a test for reward delivery**

In `STRR/tests/test_mission_manager.py`:
```python
def test_complete_mission_delivers_rewards(self):
    """Completing a mission with resource rewards actually applies them."""
    # Arrange: mock ship with a ResourceManager system
    mock_ship = Mock(spec=Starship)
    mock_resource_sys = Mock(spec=ResourceManager)
    mock_ship.get_system.return_value = mock_resource_sys

    mission = self.manager._create_test_mission_with_reward(...)

    # Act
    self.manager.complete_mission(mission, mock_ship)

    # Assert — reward was actually delivered
    mock_resource_sys.add_resources.assert_called_once()
```

Adapt to the actual test fixture structure already in `test_mission_manager.py`.

**Step 4: Run tests**

```bash
uv run pytest STRR/tests/test_mission_manager.py -q
```

**Step 5: Update version + commit**

```bash
git add STRR/src/game/components/mission_manager.py STRR/tests/test_mission_manager.py
git commit -m "fix: correct reward delivery in complete_mission to use ship.get_system('resources')"
```

---

### Task 14: Fix CrewManager morale tick — per-frame vs per-turn

**Context:** `CrewManager.update(dt)` increments `turns_since_starbase` on every frame (60Hz), so the morale penalty counter reaches 600 per real second instead of 1 per game turn. The counter should only increment when a game turn passes, not on every physics tick.

**Files:**
- Modify: `STRR/src/game/components/ship_systems.py`

**Step 1: Find the update method**

```bash
grep -n "turns_since_starbase\|update\|dt" STRR/src/game/components/ship_systems.py | grep -A5 "class CrewManager" | head -20
```

Locate the `update(self, dt: float)` method in `CrewManager`.

**Step 2: Add a per-turn notification method**

Instead of incrementing `turns_since_starbase` in `update(dt)`, add a separate method called on each game turn:

```python
def on_turn_advanced(self) -> None:
    """Called once per game turn to update turn-based counters."""
    self._turns_since_starbase += 1
    self._calculate_morale_modifiers()
```

In `update(dt)`, remove the `turns_since_starbase` increment and `_calculate_morale_modifiers()` call. Keep only real-time effects (if any) in `update(dt)`.

**Step 3: Wire `on_turn_advanced` into `GameModel.advance_turn`**

In `model.py`, find where turns advance (likely `TurnManager.advance_turn`). After the turn advances, call `on_turn_advanced()` on each crew system:

```python
# In GameModel or TurnManager, after advancing turn:
for entity in self.turn_manager.active_entities:
    crew_sys = entity.get_system("crew") if hasattr(entity, "get_system") else None
    if isinstance(crew_sys, CrewManager):
        crew_sys.on_turn_advanced()
```

**Step 4: Write a test**

```python
def test_crew_morale_increments_once_per_turn_not_per_frame(self):
    """turns_since_starbase should only increment on turn advance, not update()."""
    crew = CrewManager()
    initial = crew._turns_since_starbase

    # Many frame updates should NOT change turn counter
    for _ in range(100):
        crew.update(0.016)  # 100 frames at 60fps

    assert crew._turns_since_starbase == initial

    # One turn advance SHOULD increment
    crew.on_turn_advanced()
    assert crew._turns_since_starbase == initial + 1
```

**Step 5: Run tests**

```bash
uv run pytest STRR/tests/test_ship_systems.py -q
```

**Step 6: Update version + commit**

```bash
git add STRR/src/game/components/ship_systems.py STRR/src/game/model.py STRR/tests/test_ship_systems.py
git commit -m "fix: move CrewManager turn counter to on_turn_advanced(), not update() frame tick"
```

---

### Final: Run full suite + mypy + ruff

After all tasks complete, verify the whole codebase is clean:

```bash
uv run pytest STRR/tests/ -q
uv run mypy STRR/src/
uv run ruff check STRR/src/ STRR/tests/
```

Expected:
- 441+ tests passing, 0 critical failures
- mypy: 0 errors
- ruff: 0 errors
