# State Machine Documentation

**File:** `STRR/src/game/states/state_machine.py`
**Version:** 0.0.1
**Last Updated:** 10-30-2025

---

## Purpose

Implements the **State Machine** pattern for managing game modes. Provides clean state transitions between different parts of the game (menus, exploration, combat, etc.).

---

## Architecture

### State Pattern

```
GameStateManager
    ├── Current State (e.g., SECTOR_MAP)
    ├── Previous State (for back navigation)
    └── State Registry (all available states)

State Lifecycle:
    exit current → transition → enter new
```

---

## Classes

### GameMode (Enum)

Defines all possible game states:

- `MAIN_MENU`: Title screen and menu
- `GALAXY_MAP`: Strategic galaxy view
- `SECTOR_MAP`: Tactical sector view
- `COMBAT`: Active combat mode
- `SETTINGS`: Settings/options
- `PAUSED`: Paused game

---

### GameState (Abstract Base)

**Purpose:** Base class for implementing specific game states

**Must implement:**

- `enter()`: Called when entering state (setup)
- `exit()`: Called when leaving state (cleanup)
- `handle_input(event)`: Process input events
- `update(dt)`: Update logic (dt = delta time)
- `render(surface)`: Draw state to PyGame surface

---

### GameStateManager

**Purpose:** Manages state transitions and current state

**Key Attributes:**

- `current_state`: Active game state
- `previous_state`: Previous state (for back button)
- `states`: Registry of available states

**Key Methods:**

- `register_state(mode, state)`: Register a state implementation
- `transition_to(mode)`: Switch to new state
- `update(dt)`: Update current state
- `render(surface)`: Render current state
- `handle_input(event)`: Forward input to current state
- `get_current_mode()`: Get current mode enum

---

## Usage Example

### Implementing a State

```python
from game.states.state_machine import GameState, GameMode

class SectorMapState(GameState):
    def __init__(self, state_manager):
        super().__init__(state_manager)
        self.mode = GameMode.SECTOR_MAP

    def enter(self):
        # Setup sector view
        print("Entering sector map")

    def exit(self):
        # Cleanup
        print("Leaving sector map")

    def handle_input(self, event):
        # Process keyboard/mouse
        pass

    def update(self, dt):
        # Update game logic
        pass

    def render(self, surface):
        # Draw to screen
        surface.fill((0, 0, 0))  # Black background
```

### Using State Manager

```python
from game.states.state_machine import GameStateManager, GameMode

# Create manager
manager = GameStateManager()

# Register states
manager.register_state(GameMode.SECTOR_MAP, SectorMapState(manager))
manager.register_state(GameMode.COMBAT, CombatState(manager))

# Transition
manager.transition_to(GameMode.SECTOR_MAP)  # Calls exit on old, enter on new

# In game loop
manager.handle_input(event)
manager.update(dt)
manager.render(screen)
```

---

## State Transition Flow

```
1. Call transition_to(new_mode)
2. Validate transition is legal
3. Call current_state.exit()
4. Set previous_state = current_state
5. Set current_state = states[new_mode]
6. Call current_state.enter()
```

---

## Integration Points

**Dependencies:**

- `pygame` (TYPE_CHECKING only for type hints)

**Used by:**

- `game.controller.GameController` - Manages state transitions

---

## Future Enhancements

- [ ] State transition validation rules
- [ ] State history stack (back button navigation)
- [ ] State serialization (save/load)
- [ ] Transition animations
- [ ] State-specific configuration

---

## Change History

- **10-30-2025** - Documentation created
- **10-29-2025** - State machine pattern implemented
