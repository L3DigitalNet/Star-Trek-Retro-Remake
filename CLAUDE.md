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

```
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
