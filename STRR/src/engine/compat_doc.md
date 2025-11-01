# compat.py - Compatibility Layer Module

## Overview

The `compat.py` module provides a compatibility layer for Python 3.11+ features and external dependencies. Currently, it serves as a single import point for TOML reading functionality (tomllib).

## Purpose

This module eliminates code duplication across the codebase where try/except imports for tomllib were scattered. By centralizing the import logic, we achieve:

1. **Single Source of Truth** - One place to manage TOML library imports
2. **Cleaner Code** - No repeated try/except blocks in multiple files
3. **Easier Migration** - Future updates to import strategy only need to happen here
4. **Better Maintainability** - Clear separation of compatibility concerns

## Module Structure

### Exports

- `tomllib` - TOML reading module (from Python 3.14+ stdlib)

### Version

Current version: 0.0.29 (matches project version)

## Usage

### Basic Import

```python
from ...engine.compat import tomllib

# Use tomllib normally
with open(config_path, "rb") as f:
    config = tomllib.load(f)
```

### Example: Replacing Old Pattern

**Before (Duplicated Pattern):**
```python
try:
    import tomllib
except ImportError:
    import tomli as tomllib  # type: ignore
```

**After (Using compat):**
```python
from ...engine.compat import tomllib
```

## Implementation Details

Since this project requires Python 3.14+, we directly import `tomllib` from the standard library without fallback logic. This is intentional and aligned with the project's Linux-only, Python 3.14+ requirement.

## Related Files

- Used by: `ship_systems.py`, `ship_ai.py`, `config_manager.py`, and other configuration consumers
- Works with: `config_manager.py` for configuration loading
- Part of: Engine layer infrastructure

## Migration Path

To use this module throughout the codebase:

1. Replace all instances of `import tomllib` with `from ...engine.compat import tomllib`
2. Remove all try/except import blocks for tomllib/tomli
3. Update imports to use relative path from current module location

## Future Extensions

This module can be extended to include other compatibility shims as needed, such as:
- Type system compatibility helpers
- Platform-specific utilities
- Third-party library version compatibility

## Testing

Test that the module exports tomllib correctly:
```python
from STRR.src.engine.compat import tomllib

# Verify tomllib has expected interface
assert hasattr(tomllib, 'load')
assert hasattr(tomllib, 'loads')
```

## Standards Compliance

- **PEP 8**: All code follows Python style guidelines
- **Type Hints**: Full type coverage with `Final` for version
- **Documentation**: Complete docstrings and inline comments
- **Linux-Only**: No platform-specific workarounds needed
- **Python 3.14+**: Uses latest stdlib features
