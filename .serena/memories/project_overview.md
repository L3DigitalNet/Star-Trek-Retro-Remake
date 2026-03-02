# STRR — Project Overview

## Purpose
Turn-based, grid-based Star Trek strategy game. v0.0.x pre-alpha infrastructure; not yet playable end-to-end. See docs/ROADMAP.md for milestone plan.

## Tech Stack
- Python 3.14, pygame-ce (game surface), PySide6 (menus/dialogs/settings)
- Testing: pytest with markers (-m unit for no-display tests)
- Type checking: mypy
- Linting: Ruff

## Architecture — Hybrid State Machine + MVC + Component
- `STRR/src/game/model.py` — pure game logic, no UI imports
- `STRR/src/game/view.py` — PySide6 window + pygame-ce rendering surface
- `STRR/src/game/controller.py` — input handling, state coordination
- `STRR/src/game/states/` — state machine (sector map, galaxy map, combat)
- `STRR/src/game/entities/` — Starship, SpaceStation, etc.
- `STRR/src/game/components/` — ShipSystems, MissionManager
- `STRR/src/engine/` — Config, paths, isometric grid, pygame-ce compat

## Rendering
pygame-ce handles game surface (grid, ships, combat). PySide6 handles menus, dialogs, settings. Single process; pygame surface embedded in QLabel inside PySide6 main window.

## Config
All TOML in `STRR/config/`: game_settings.toml, game_data.toml, key_bindings.toml.
Must call `initialize_config_manager(config_dir)` before use.

## Import Paths
pyproject.toml sets `pythonpath = ["STRR"]`. Use `from src.game...` (not `from STRR.src.game...`).
