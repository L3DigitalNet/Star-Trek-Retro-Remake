# Star Trek Retro Remake — Full Reset Design

**Date:** 2026-02-19
**Version target:** v0.0.30 (cleanup) → v0.1.0 (playable)
**Status:** Approved

## Context

The project reached v0.0.29 with a solid architectural foundation but accumulated
structural debt: sidecar doc files, duplicate UI assets, broken test imports, and a
game that cannot actually launch. This design covers the reset plan.

## Decision: Keep pygame-ce + PySide6 Hybrid

pygame-ce handles the game grid and rendering; PySide6 handles menus, dialogs, and
settings. This dual-framework approach is intentional and should not be simplified away.

## Four-Phase Plan

---

### Phase 1: File Cleanup

**Goal:** Delete noise without touching any Python logic.

**Delete:**
- All `*_doc.md` sidecar files throughout `STRR/src/` (~15 files)
- `QT Designer Files/` at project root (duplicate of `STRR/src/ui/designer/`)
- `INTEGRATION_SUMMARY.md` at project root (stale)
- `setup-branch-protection.sh` at project root (replaced by git hooks)
- `star_trek_retro_remake.egg-info/` (stale build artifact)
- `STRR/src/ui/designer/main_window.ui` + `main_window_ui.py` (superseded by `main_window_complete*`)

**Add:**
- `CLAUDE.md` at project root with: build commands, test commands, architecture summary,
  branch protection rules

**Preserve:**
- All `docs/` folder contents
- All `STRR/src/**/*.py` files (no code changes in Phase 1)
- `STRR/src/ui/designer/main_window_complete.ui` and compiled variant

**Commit:** `chore: phase 1 cleanup - remove sidecar docs and duplicate files`

---

### Phase 2: Fix Imports and Tests

**Goal:** Get all 17 test files to at least collect; fix the 3 root causes of test failure.

**Problem 1 — Import path inconsistency:**
- Tests use `from STRR.src.game.application import ...`
- `pyproject.toml` sets `pythonpath = ["STRR"]`, so correct path is `from src.game.application import ...`
- Fix: Update all 10 broken test files to use the `src.*` import path

**Problem 2 — pygame-ce import in tests:**
- `test_state_machine.py` and others `import pygame` directly which fails without a display
- Fix: Mock pygame in `conftest.py` for tests that don't need rendering, using the
  existing `STRR/src/engine/compat.py` layer

**Problem 3 — ConfigManager not initialized:**
- `get_config_manager()` throws `ConfigurationError` before tests initialize it
- Fix: Add autouse fixture in `conftest.py` that calls `initialize_config_manager()`
  with the test config path before each test module

**Commit:** `fix: phase 2 - fix test import paths and test infrastructure`

---

### Phase 3: Get the Game Running

**Goal:** `uv run python -m STRR.main` launches to a visible sector map (even placeholder).

**Problems to fix:**
- `main.py` uses `sys.path.insert` hack which is fragile; standardize to package imports
- `ConfigManager` must initialize before any module-level code accesses it
- pygame + QApplication startup sequence must not crash on a headless or first-run system
- Sector map must render (even a blank grid) without errors

**Success criteria:** Game window opens, shows the isometric grid, does not crash.

**Commit:** `fix: phase 3 - fix startup sequence, get game to launch`

---

### Phase 4: Development Roadmap

**Goal:** Written roadmap in `docs/ROADMAP.md` covering the path to a playable game.

**Milestones:**
- **v0.1.0** — Playable sector map: ship renders, player can move it, turn counter advances
- **v0.2.0** — Combat prototype: fire phasers, apply damage, win/lose condition
- **v0.3.0** — Galaxy map + sector travel: navigate between sectors
- **v0.4.0** — Mission system: accept, track, and complete missions
- **v0.5.0** — Save/load: persist game state between sessions

**Commit:** `docs: add ROADMAP.md and CLAUDE.md`

---

## Architecture Constraints (unchanged)

- Python 3.14+
- pygame-ce for game surface rendering
- PySide6 for menus, dialogs, settings
- MVC pattern: Model (pure game logic), View (pygame + Qt rendering), Controller (input + coordination)
- TOML for all config files
- pytest for all tests, no GUI display required for unit tests
- `testing` branch for development, protected `main`

## File Structure After Reset

```
Star-Trek-Retro-Remake/
├── CLAUDE.md               ← NEW: build/test commands, architecture summary
├── CONTRIBUTING.md
├── LICENSE
├── Makefile
├── README.md
├── pyproject.toml
├── uv.lock
├── docs/
│   ├── plans/              ← NEW: design docs go here
│   ├── ARCHITECTURE.md
│   ├── CHANGELOG.md
│   ├── DESIGN.md
│   ├── PROJECT-DOC.md
│   └── ROADMAP.md          ← NEW in Phase 4
└── STRR/
    ├── main.py
    ├── assets/
    ├── config/
    ├── src/
    │   ├── engine/         ← no *_doc.md files
    │   ├── game/           ← no *_doc.md files
    │   └── ui/
    │       ├── compiled/
    │       └── designer/   ← only main_window_complete*
    └── tests/
```
