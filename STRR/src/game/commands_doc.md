# Commands Documentation

**File:** `STRR/src/game/commands.py`
**Version:** 0.0.1
**Last Updated:** 10-30-2025

---

## Purpose

Implements the **Command Pattern** for undoable game actions. Enables:

- Undo/redo functionality
- Command history tracking
- Macro recording (future)
- Replay systems (future)

---

## Architecture

### Command Pattern

```
User Action → Create Command → Execute → Store in History
                                          ↓
                                        Undo/Redo available
```

Each action is encapsulated as an object with `execute()` and `undo()` methods.

---

## Classes

### Command (Abstract Base)

**Purpose:** Base class for all undoable commands

**Key Methods:**

- `execute() -> bool`: Execute the command
- `undo() -> bool`: Reverse the command
- `can_execute() -> bool`: Check if executable
- `can_undo() -> bool`: Check if undoable
- `_do_execute()`: Override in subclasses
- `_do_undo()`: Override in subclasses

---

### MoveShipCommand

**Purpose:** Encapsulates ship movement with undo capability

**Stores:**

- Previous position
- Previous fuel level

**Example:**

```python
from game.commands import MoveShipCommand, CommandHistory
from game.entities.base import GridPosition

# Create and execute movement
destination = GridPosition(6, 6, 1)
cmd = MoveShipCommand(player_ship, destination)

history = CommandHistory()
history.execute(cmd)  # Move and store in history

# Undo movement
history.undo()  # Ship returns to previous position
```

---

### FireWeaponCommand

**Purpose:** Encapsulates weapon firing with undo

**Stores:**

- Target's previous hull integrity
- Damage dealt
- Ammo consumed

---

### CommandHistory

**Purpose:** Manages undo/redo stacks

**Key Attributes:**

- `command_stack`: List of executed commands
- `redo_stack`: List of undone commands
- `max_history`: Maximum stored commands (default 100)

**Key Methods:**

- `execute(command)`: Execute and store command
- `undo()`: Undo last command
- `redo()`: Redo last undone command
- `can_undo()` / `can_redo()`: Check availability
- `clear()`: Clear all history

---

## Usage Example

```python
from game.commands import CommandHistory, MoveShipCommand

# Create history manager
history = CommandHistory(max_history=50)

# Execute commands
move_cmd = MoveShipCommand(ship, new_position)
history.execute(move_cmd)

# Undo/redo
if history.can_undo():
    history.undo()

if history.can_redo():
    history.redo()
```

---

## Integration Points

**Dependencies:**

- `game.entities.starship.Starship`
- `game.entities.base.GridPosition`
- `game.exceptions.InvalidMoveError`

**Used by:**

- `game.controller.GameController` - Execute user actions as commands

---

## Change History

- **10-30-2025** - Documentation created
- **10-29-2025** - Command pattern implemented
