# config_loader.py - Configuration Loader Module

## Overview

The `config_loader.py` module provides a generic, reusable configuration loader with caching for all game systems. It eliminates the duplicated configuration loading patterns found throughout the codebase and provides a clean, consistent interface.

## Purpose

This module solves the problem of repeated configuration loading code with inconsistent patterns. Before this module, configuration loading was duplicated across 5+ files with manual caching, path calculations, and error handling. Benefits include:

1. **DRY Principle** - Eliminates ~150 lines of duplicated code
2. **Consistent Pattern** - Same approach everywhere
3. **Better Testability** - Easy to mock for testing
4. **Centralized Error Handling** - Single place to handle config errors
5. **Type-Safe Access** - Generic type parameter for type hints
6. **Automatic Caching** - Built-in performance optimization

## Module Structure

### Classes

#### ConfigLoader[T]

Generic configuration loader with lazy initialization and caching.

**Type Parameter:**
- `T` - Expected type of configuration values (typically `dict`)

**Attributes:**
- `config_file` - Configuration filename (without .toml extension)
- `section` - Section path within config (dot notation)
- `_cache` - Internal cache for loaded data

**Properties:**
- `data` - Lazy-loaded configuration dictionary

**Methods:**
- `get(key, default)` - Get configuration value with default
- `refresh()` - Clear cache and reload

### Helper Functions

- `get_combat_config()` - Get combat configuration loader
- `get_display_config()` - Get display configuration loader
- `get_audio_config()` - Get audio configuration loader

### Version

Current version: 0.0.29 (matches project version)

## Usage

### Basic Usage with ConfigLoader

```python
from ...engine.config_loader import ConfigLoader

# Create loader for combat config section
combat_config = ConfigLoader[dict]("game_settings", "game.combat")

# Get values with defaults
weapon_range = combat_config.get("weapon_range", 5)
accuracy_base = combat_config.get("weapon_accuracy_base", 0.85)
```

### Using Helper Functions (Recommended)

```python
from ...engine.config_loader import get_combat_config

# Get combat config (cached)
config = get_combat_config()

# Access values
weapon_range = config.get("weapon_range", 5)
firing_arc = config.get("weapon_firing_arc", 270)
```

### Example: Ship Systems

**Before (Duplicated Pattern):**
```python
class WeaponSystems(ShipSystem):
    _combat_config: dict[str, float] | None = None
    
    @classmethod
    def _load_combat_config(cls) -> dict[str, float]:
        if cls._combat_config is None:
            try:
                import tomllib
                from pathlib import Path
                
                config_path = (
                    Path(__file__).parent.parent.parent
                    / "config"
                    / "game_settings.toml"
                )
                with open(config_path, "rb") as f:
                    settings = tomllib.load(f)
                    cls._combat_config = settings.get("game", {}).get("combat", {})
            except Exception:
                cls._combat_config = {}
        return cls._combat_config
    
    def __init__(self):
        super().__init__("Weapons", 1.0)
        config = self._load_combat_config()
        self.firing_arc = config.get("weapon_firing_arc", 270)
```

**After (Using ConfigLoader):**
```python
from ...engine.config_loader import get_combat_config

class WeaponSystems(ShipSystem):
    def __init__(self):
        super().__init__("Weapons", 1.0)
        
        config = get_combat_config()
        self.firing_arc = config.get("weapon_firing_arc", 270)
        self.accuracy_base = config.get("weapon_accuracy_base", 0.85)
```

## Implementation Details

### Lazy Loading

The `data` property implements lazy loading:
1. On first access, loads configuration via ConfigManager
2. Caches the result in `_cache`
3. Subsequent accesses return cached data
4. Call `refresh()` to clear cache and reload

### Integration with ConfigManager

ConfigLoader builds on top of ConfigManager:
- Uses `get_config_manager()` to access the global instance
- Delegates to `load_config()` or `get_config_value()` methods
- Inherits ConfigManager's error handling

### Helper Function Caching

Helper functions use `@lru_cache(maxsize=None)`:
- Returns same ConfigLoader instance on repeat calls
- Efficient for frequently-used configurations
- Thread-safe caching

## Configuration File Structure

Expected TOML structure:
```toml
[game.combat]
weapon_range = 5
weapon_firing_arc = 270
weapon_accuracy_base = 0.85
weapon_range_penalty = 0.4
critical_hit_chance = 0.1
critical_hit_multiplier = 1.5

[display]
width = 1920
height = 1080
fullscreen = false

[audio]
music_volume = 0.7
sfx_volume = 0.8
master_volume = 1.0
```

## Related Files

- Depends on: `config_manager.py` for configuration loading
- Used by: `ship_systems.py`, `ship_ai.py`, `mission_manager.py`, etc.
- Works with: `paths.py`, `compat.py`
- Part of: Engine layer infrastructure

## Migration Path

To migrate existing code to use ConfigLoader:

1. Remove manual config loading methods
2. Import `get_combat_config()` or relevant helper
3. Replace config dict access with `config.get()`
4. Remove class-level `_config` caching variables
5. Remove manual path calculations and TOML imports

### Migration Checklist

Files to migrate:
- [ ] `ship_systems.py` - WeaponSystems._load_combat_config()
- [ ] `ship_ai.py` - ShipAI class-level config loading
- [ ] `mission_manager.py` - MissionManager TOML loading
- [ ] `settings_dialog.py` - load_settings_from_toml()
- [ ] Any other files with manual config loading

## Testing

### Unit Tests

```python
from STRR.src.engine.config_loader import ConfigLoader, get_combat_config

def test_config_loader_lazy_loading():
    # Arrange
    loader = ConfigLoader("game_settings", "game.combat")
    
    # Act - data not loaded yet
    assert loader._cache is None
    
    # Access data
    data = loader.data
    
    # Assert - data now cached
    assert loader._cache is not None
    assert data is loader.data  # Same instance

def test_get_combat_config_returns_same_instance():
    # Act
    config1 = get_combat_config()
    config2 = get_combat_config()
    
    # Assert - same instance due to lru_cache
    assert config1 is config2
```

### Integration Tests

```python
def test_weapon_systems_uses_config_loader(config_manager):
    # Arrange
    from src.game.components.ship_systems import WeaponSystems
    
    # Act
    weapons = WeaponSystems()
    
    # Assert - values loaded from config
    assert weapons.firing_arc == 270  # From config
    assert weapons.accuracy_base == 0.85  # From config
```

## Error Handling

ConfigLoader delegates error handling to ConfigManager:
- Missing config files raise `ConfigurationError`
- Missing sections return empty dict `{}`
- Missing keys return specified default value

```python
config = get_combat_config()

# Safe access with defaults
weapon_range = config.get("weapon_range", 5)  # Returns 5 if not in config
```

## Performance Considerations

### Caching Strategy

1. **Instance-level cache** - Each ConfigLoader instance caches its data
2. **Helper function cache** - `@lru_cache` ensures single instance per config
3. **ConfigManager cache** - Underlying cache for loaded TOML files

This three-tier caching ensures minimal file I/O and parsing overhead.

### Memory Usage

- Each ConfigLoader instance: ~100 bytes + size of cached dict
- Helper function cache: 3 ConfigLoader instances (combat, display, audio)
- ConfigManager cache: Full TOML files

Total memory impact: Negligible (~few KB)

## Future Extensions

Planned enhancements:
- Configuration validation with schema
- Hot-reloading of configuration files
- Configuration change notifications
- Type-safe configuration access with dataclasses
- Configuration inheritance and overrides

## Standards Compliance

- **PEP 8**: All code follows Python style guidelines
- **Type Hints**: Full type coverage with Generic[T] pattern
- **Documentation**: Complete docstrings and inline comments
- **Linux-Only**: No platform-specific code
- **Python 3.14+**: Uses latest language features (Generic, Final, etc.)
