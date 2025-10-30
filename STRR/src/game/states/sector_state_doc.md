# Sector State Module Documentation

**Module:** `STRR/src/game/states/sector_state.py`
**Version:** 0.0.1
**Last Updated:** 10-30-2025

## Overview

The Sector State module implements the sector exploration gameplay state within the game's state machine. It handles sector-level navigation, entity interactions, and grid-based movement in the isometric 3D space.

## Purpose

This module enables:

- Sector-level exploration and navigation
- Isometric grid-based gameplay view
- Entity interaction within sectors
- State-specific input handling
- Integration with the game state machine

## Architecture

### Design Pattern

- **State Pattern**: Implements GameState interface for state machine integration
- **MVC Integration**: Works with GameModel, GameView, and GameController
- **Event-Driven**: Processes pygame-ce events for user interaction

### Key Components

1. **SectorState Class**: Main state implementation for sector exploration
2. **GameState Interface**: Parent class defining state contract
3. **GameStateManager Integration**: Managed by state machine for transitions

## Classes

### SectorState

Sector exploration game state implementation.

**Inheritance:** Extends `GameState` abstract base class

**Attributes:**

- `mode`: GameMode.SECTOR_MAP (identifies this state)
- `state_manager`: Reference to GameStateManager for state transitions

**Public Methods:**

#### `__init__(state_manager: GameStateManager)`

Initialize the sector state.

**Parameters:**

- `state_manager`: The game state manager instance

**Returns:** None

#### `enter() -> None`

Called when entering sector state. Sets up sector-specific initialization.

**Actions:**

- Logs state entry
- Initializes sector-specific UI elements (future)
- Prepares sector map for rendering

**Returns:** None

#### `exit() -> None`

Called when leaving sector state. Performs cleanup.

**Actions:**

- Logs state exit
- Cleans up sector-specific resources (future)
- Saves sector state if needed

**Returns:** None

#### `handle_input(event: pygame.event.Event) -> None`

Process pygame-ce events for sector exploration.

**Parameters:**

- `event`: pygame event object

**Currently Handled Events:**

- Mouse clicks for entity selection
- Keyboard input for ship commands
- UI interaction events

**Returns:** None

#### `update(dt: float) -> None`

Update sector state logic.

**Parameters:**

- `dt`: Delta time in seconds since last update

**Actions:**

- Updates entity positions (animations)
- Processes turn-based timers
- Updates sector state (future AI, events)

**Returns:** None

#### `render() -> None`

Render sector map and entities.

**Actions:**

- Delegates to GameView for rendering
- Ensures correct view state for sector display
- Renders grid, entities, UI overlays

**Returns:** None

## Integration Points

### GameStateManager Integration

The state machine manages sector state lifecycle:

```python
# In GameStateManager:
sector_state = SectorState(self)
self.states[GameMode.SECTOR_MAP] = sector_state

# Transition to sector:
self.change_state(GameMode.SECTOR_MAP)
# Calls: sector_state.enter()
```

### Controller Integration

GameController delegates to active state:

```python
# In GameController._handle_events():
for event in pygame.event.get():
    current_state = self.state_manager.get_current_state()
    current_state.handle_input(event)
```

### Model Integration

Sector state queries/modifies GameModel:

```python
# In SectorState methods:
sector_map = self.state_manager.model.get_sector(x, y)
player_ship = self.state_manager.model.player_ship
```

### View Integration

Sector state triggers view updates:

```python
# In SectorState.render():
self.state_manager.view.render_sector_map(
    sector_map,
    current_z_level
)
```

## Usage Examples

### Basic State Transition

```python
from STRR.src.game.states.sector_state import SectorState
from STRR.src.game.states.state_machine import GameMode

# Transition to sector exploration:
game_controller.state_manager.change_state(GameMode.SECTOR_MAP)
# Automatically calls enter(), starts sector gameplay
```

### Custom State Initialization

```python
# In SectorState.enter():
def enter(self) -> None:
    super().enter()

    # Custom initialization
    self._setup_sector_camera()
    self._load_sector_entities()
    self._initialize_sector_ui()
```

### Event Handling

```python
# In SectorState.handle_input():
def handle_input(self, event: pygame.event.Event) -> None:
    if event.type == pygame.MOUSEBUTTONDOWN:
        # Convert screen coords to grid position
        grid_pos = self._screen_to_grid(event.pos)
        self._handle_cell_click(grid_pos)

    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_m:
            # Switch to galaxy map
            self.state_manager.change_state(GameMode.GALAXY_MAP)
```

## State Machine Diagram

```
┌──────────────┐
│  MAIN_MENU   │
└──────┬───────┘
       │
       ▼
┌──────────────┐         ┌──────────────┐
│  GALAXY_MAP  │◄───────►│  SECTOR_MAP  │◄─┐
└──────────────┘         └──────┬───────┘  │
                                │           │
                                ▼           │
                         ┌──────────────┐  │
                         │    COMBAT    │──┘
                         └──────────────┘
                                │
                                ▼
                         ┌──────────────┐
                         │   PAUSED     │
                         └──────────────┘
```

## Future Enhancements

### Planned Features

- **Sector Events**: Random encounters, distress calls, anomalies
- **Dialog System**: Hailing ships, station interactions
- **Minimap**: Small overview of sector in UI
- **Waypoints**: Set destination markers on grid
- **Autopilot**: Automatic navigation to waypoints

### State-Specific UI

- Sector name display with coordinates
- Entity list panel showing all ships/stations
- Distance/range indicators
- Sensor sweep visualization
- Current sector objectives display

### Performance Optimizations

- Entity culling for off-screen objects
- Level-of-detail rendering for distant z-levels
- Lazy loading of sector data
- Entity pooling for temporary objects

## Testing

### Unit Tests

Test coverage in `STRR/tests/test_sector_state.py`:

- State initialization and cleanup
- State transitions (enter/exit)
- Event handling and input processing
- Model/view integration
- State persistence

### Integration Tests

- Full state machine transitions
- Sector exploration workflows
- Combat state transitions from sector
- Save/load during sector exploration

## Related Documentation

- **State Machine**: `STRR/src/game/states/state_machine_doc.md`
- **GameController**: `STRR/src/game/controller_doc.md`
- **GameModel**: `STRR/src/game/model_doc.md`
- **GameView**: `STRR/src/game/view_doc.md`
- **Isometric Grid**: `STRR/src/engine/isometric_grid_doc.md`

## Linux Compatibility

All sector state code is fully compatible with Linux systems:

- Pure Python implementation
- Uses pygame-ce for cross-platform input handling
- Path handling uses pathlib for Linux compatibility
- No OS-specific dependencies

**Python Requirements:** 3.14+ for latest language features
