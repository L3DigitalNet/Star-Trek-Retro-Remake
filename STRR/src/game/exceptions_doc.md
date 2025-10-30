# Exceptions Documentation

**File:** `STRR/src/game/exceptions.py`
**Version:** 0.0.1
**Last Updated:** 10-30-2025

---

## Purpose

Defines custom exception classes for game-specific error handling. Provides a hierarchical exception structure for clear error communication and debugging.

---

## Architecture

### Exception Hierarchy

```
Exception (Python base)
    └── GameError (base for all game exceptions)
        ├── InvalidMoveError
        ├── InsufficientResourcesError
        ├── SystemOfflineError
        ├── CombatError
        ├── ConfigurationError
        ├── SaveLoadError
        ├── StateTransitionError
        └── EntityNotFoundError
```

---

## Classes

### GameError

**Purpose:** Base exception for all game-related errors

**Attributes:**

- `message` (str): Error description
- `details` (dict): Additional context

**Usage:**

```python
raise GameError("Something went wrong", {"context": "value"})
```

---

### InvalidMoveError

**When to raise:** Invalid movement attempts (out of bounds, obstacles)

**Example:**

```python
raise InvalidMoveError(
    "Cannot move there",
    position=destination,
    reason="Out of bounds"
)
```

---

### InsufficientResourcesError

**When to raise:** Action requires more resources than available

**Example:**

```python
raise InsufficientResourcesError(
    resource_type="fuel",
    required=50.0,
    available=25.0
)
# Message: "Insufficient fuel: required 50.0, available 25.0"
```

---

### SystemOfflineError

**When to raise:** Attempting to use an offline/destroyed ship system

**Example:**

```python
raise SystemOfflineError("weapons")
# Message: "System 'weapons' is offline"
```

---

### CombatError

**When to raise:** Combat action fails (out of range, invalid target)

**Example:**

```python
raise CombatError(
    "Cannot fire weapons",
    reason="Target out of range",
    distance=12
)
```

---

### ConfigurationError

**When to raise:** Configuration file issues

**Example:**

```python
raise ConfigurationError(
    config_name="game_settings",
    message="Missing required field 'display.width'"
)
```

---

### SaveLoadError

**When to raise:** Save/load operation failures

**Example:**

```python
raise SaveLoadError(
    operation="save",
    filepath="/path/to/save.json",
    message="Permission denied"
)
```

---

### StateTransitionError

**When to raise:** Invalid game state transition

**Example:**

```python
raise StateTransitionError(
    from_state="COMBAT",
    to_state="MAIN_MENU",
    message="Cannot return to menu during combat"
)
```

---

### EntityNotFoundError

**When to raise:** Entity doesn't exist or can't be located

**Example:**

```python
raise EntityNotFoundError(entity_id="ship-12345")
# Message: "Entity with ID 'ship-12345' not found"
```

---

## Usage Patterns

### Pattern 1: Try-Catch with Specific Exceptions

```python
try:
    model.execute_move(ship, destination)
except InvalidMoveError as e:
    print(f"Move failed: {e.message}")
    print(f"Details: {e.details}")
except InsufficientResourcesError as e:
    print(f"Not enough resources: {e.message}")
```

### Pattern 2: Catch All Game Errors

```python
try:
    perform_game_action()
except GameError as e:
    logger.error(f"Game error: {e.message}", extra=e.details)
    show_error_dialog(e.message)
```

### Pattern 3: Re-raising with Context

```python
try:
    load_config_file(path)
except FileNotFoundError:
    raise ConfigurationError(
        "game_settings",
        message=f"Config file not found: {path}"
    )
```

---

## Integration Points

**Used by:** All game modules for error signaling

**Dependencies:** None (standard library only)

---

## Notes

- All exceptions include `details` dict for structured error information
- Use specific exceptions for catch-able error types
- Use base `GameError` for generic game errors

---

## Change History

- **10-30-2025** - Documentation created
- **10-29-2025** - Exception hierarchy implemented
