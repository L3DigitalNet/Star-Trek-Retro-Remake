# Configuration Manager Documentation

**File:** `STRR/src/engine/config_manager.py`
**Version:** 0.0.1
**Last Updated:** 10-30-2025

---

## Purpose

Manages loading and saving of configuration files. Supports **TOML** (primary) and **JSON** (fallback) formats. Provides centralized configuration access throughout the game.

---

## Classes

### ConfigManager

**Purpose:** Load, save, and manage configuration files

**Key Methods:**

- `load_config(filename, use_cache=True) -> dict`: Load TOML/JSON config
- `save_config(filename, data)`: Save config as TOML
- `migrate_json_to_toml(filename, remove_json=False) -> bool`: Convert JSON to TOML
- `get_config_value(filename, key_path, default=None)`: Get nested value using dot notation
- `set_config_value(filename, key_path, value)`: Set nested value
- `clear_cache()`: Clear cached configs

**Example:**

```python
from engine.config_manager import ConfigManager
from pathlib import Path

# Initialize
config_dir = Path("config")
manager = ConfigManager(config_dir)

# Load config
settings = manager.load_config("game_settings")
width = settings["display"]["width"]

# Get value with dot notation
width = manager.get_config_value("game_settings", "display.width", 1024)

# Set value
manager.set_config_value("game_settings", "display.fullscreen", True)

# Save changes
manager.save_config("game_settings", settings)
```

---

## Global Functions

Convenience functions for global configuration access:

- `initialize_config_manager(config_dir)`: Setup global manager
- `get_config_manager()`: Get global instance
- `load_config(filename)`: Load using global manager
- `save_config(filename, data)`: Save using global manager
- `get_config_value(filename, key_path, default)`: Get value
- `set_config_value(filename, key_path, value)`: Set value

---

## Format Support

**TOML (Primary):**

- Uses Python 3.14+ `tomllib` for reading
- Uses `tomli_w` for writing

**JSON (Fallback):**

- Supports legacy JSON configs
- Can migrate to TOML format

---

## Integration Points

**Dependencies:**

- `tomllib` (stdlib) - TOML reading
- `tomli_w` - TOML writing
- `json` (stdlib) - JSON support

**Used by:**

- `game.application.StarTrekRetroRemake` - Load game settings
- Any module needing configuration

---

## Change History

- **10-30-2025** - Documentation created
- **10-29-2025** - Configuration manager implemented
