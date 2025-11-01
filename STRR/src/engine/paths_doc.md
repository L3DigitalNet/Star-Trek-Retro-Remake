# paths.py - Centralized Path Management Module

## Overview

The `paths.py` module provides centralized path management for all project resources. It eliminates fragile path calculations scattered throughout the codebase and serves as the single source of truth for all file locations.

## Purpose

This module solves the problem of `Path(__file__).parent.parent.parent` patterns repeated across multiple files. Benefits include:

1. **Single Source of Truth** - All paths defined in one place
2. **Maintainability** - Easy to modify project structure
3. **Type Safety** - All paths are Final[Path] with full type hints
4. **IDE Support** - Better autocomplete and navigation
5. **Testability** - Easy to mock or override for testing

## Module Structure

### Root Directories

- `PROJECT_ROOT` - Root of the STRR directory
- `SRC_ROOT` - Source code directory (STRR/src)
- `ASSETS_ROOT` - Assets directory (STRR/assets)
- `CONFIG_ROOT` - Configuration directory (STRR/config)
- `TESTS_ROOT` - Tests directory (STRR/tests)

### Asset Subdirectories

- `GRAPHICS_DIR` - Graphics assets (STRR/assets/graphics)
- `AUDIO_DIR` - Audio assets (STRR/assets/audio)
- `DATA_DIR` - Data files (STRR/assets/data)
- `MISSION_DATA_DIR` - Mission data (STRR/assets/data/missions)
- `SECTOR_DATA_DIR` - Sector data (STRR/assets/data/sectors)

### Configuration Files

- `GAME_SETTINGS_FILE` - Game settings TOML (config/game_settings.toml)
- `GAME_DATA_FILE` - Game data TOML (config/game_data.toml)
- `KEY_BINDINGS_FILE` - Key bindings TOML (config/key_bindings.toml)

### Mission Files

- `MISSION_TEMPLATES_FILE` - Mission templates TOML (assets/data/mission_templates.toml)

### Version

Current version: 0.0.29 (matches project version)

## Usage

### Basic Import

```python
from ...engine.paths import CONFIG_ROOT, GAME_SETTINGS_FILE

# Use paths directly
config_path = GAME_SETTINGS_FILE
print(f"Config at: {config_path}")
```

### Example: Replacing Old Pattern

**Before (Fragile Pattern):**
```python
from pathlib import Path

config_path = (
    Path(__file__).parent.parent.parent
    / "config"
    / "game_settings.toml"
)
```

**After (Using paths):**
```python
from ...engine.paths import GAME_SETTINGS_FILE

config_path = GAME_SETTINGS_FILE
```

### Using get_asset_path()

```python
from ...engine.paths import get_asset_path

# Get asset by category and filename
sprite_path = get_asset_path("graphics", "ship_sprite.png")
sound_path = get_asset_path("audio", "phaser_fire.wav")
mission_path = get_asset_path("data", "mission_01.toml")
```

## Implementation Details

### Path Calculation

The module calculates paths relative to itself at import time:
- Located at: `STRR/src/engine/paths.py`
- `Path(__file__)` -> `STRR/src/engine/paths.py`
- `.parents[2]` -> `STRR/` (PROJECT_ROOT)

All other paths are derived from PROJECT_ROOT, ensuring consistency.

### Type Safety

All path constants use `Final[Path]` type hints, which:
- Prevents accidental reassignment
- Provides IDE type checking and autocomplete
- Documents intent (these are constants)

## Related Files

- Used by: All modules that access configuration, assets, or data
- Works with: `config_manager.py`, `compat.py`
- Part of: Engine layer infrastructure

## Migration Path

To migrate existing code to use paths module:

1. Import relevant path constants from `...engine.paths`
2. Replace path calculations with imported constants
3. Remove local path calculation code
4. Update tests to use path constants

### Migration Example

**File: ship_systems.py**
```python
# Before
from pathlib import Path
config_path = Path(__file__).parent.parent.parent / "config" / "game_settings.toml"

# After
from ...engine.paths import GAME_SETTINGS_FILE
config_path = GAME_SETTINGS_FILE
```

## Error Handling

### get_asset_path() Validation

The `get_asset_path()` function validates the category parameter:

```python
try:
    path = get_asset_path("invalid_category", "file.txt")
except ValueError as e:
    print(f"Error: {e}")
    # Output: "Unknown asset category: invalid_category. Valid categories: graphics, audio, data"
```

## Testing

Test that paths are correctly calculated:

```python
from STRR.src.engine.paths import PROJECT_ROOT, CONFIG_ROOT, GAME_SETTINGS_FILE

# Verify path relationships
assert CONFIG_ROOT == PROJECT_ROOT / "config"
assert GAME_SETTINGS_FILE == CONFIG_ROOT / "game_settings.toml"

# Verify paths exist (in production)
assert PROJECT_ROOT.exists()
assert CONFIG_ROOT.exists()
```

## Future Extensions

Planned enhancements:
- Path validation utilities (check if files exist)
- Asset discovery functions (list all files in category)
- Dynamic path configuration (for different deployment scenarios)
- Path resolution helpers (resolve relative to project root)

## Standards Compliance

- **PEP 8**: All code follows Python style guidelines
- **Type Hints**: Full type coverage with `Final` for all constants
- **Documentation**: Complete docstrings and inline comments
- **Linux-Only**: Uses Path for cross-platform compatibility (within Linux)
- **Python 3.14+**: Uses latest pathlib features
