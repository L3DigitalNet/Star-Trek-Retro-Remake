# Game Controller Documentation

**File:** `STRR/src/game/controller.py`
**Version:** 0.0.1
**Last Updated:** 10-30-2025

---

## Purpose

The `controller.py` file implements the **Controller** component of the MVC architecture. It is the **coordination hub** that:

- Processes user input from View
- Executes actions on Model
- Updates View with new state
- Manages game flow and state transitions
- Runs the game loop

---

## Architecture

### MVC Controller Pattern

```
User Input → View → Controller (this file) → Model
                      ↓
                    View (update)
```

The Controller is the **only component** that modifies the Model.

### Game Loop

```
while running:
    handle_events()  # Process input
    update(dt)       # Update game logic
    render()         # Draw to screen
```

Fixed timestep at 60 FPS using pygame-ce clock.

---

## Classes

### GameController

**Purpose:** Coordinates Model and View, handles input, manages game flow

**Key Attributes:**

- `model` (GameModel): Game state and logic
- `view` (Optional[GameView]): Display and UI
- `state_manager` (GameStateManager): Game state machine
- `running` (bool): Game loop flag
- `clock` (pygame.time.Clock): Frame timing (pygame-ce)

**Public Methods:**

#### set_view(view: GameView) -> None

Links the view to the controller.

#### start() -> None

Starts the game loop. Blocking call.

#### stop() -> None

Stops the game loop and exits.

#### handle_ship_move_request(destination: GridPosition) -> None

Processes ship movement request from player.

**Flow:**

1. Validate move through model
2. Execute if valid
3. Update view with result

#### handle_combat_action(target: Starship, weapon_type: str) -> None

Processes combat action request.

**Flow:**

1. Resolve combat through model
2. Get result
3. Display via view

#### start_new_game() -> None

Initializes a new game session.

#### save_game(filepath: str) -> bool / load_game(filepath: str) -> bool

Delegates save/load to model.

---

## Usage Example

```python
from game.controller import GameController
from game.model import GameModel
from game.entities.base import GridPosition

model = GameModel()
controller = GameController(model)

# Set up view (done by application)
controller.set_view(view)

# Start game
controller.start_new_game()

# Handle input
destination = GridPosition(6, 6, 1)
controller.handle_ship_move_request(destination)

# Start game loop (blocking)
controller.start()
```

---

## Game Loop Details

The `_game_loop()` method runs at 60 FPS:

```python
while self.running:
    dt = self.clock.tick(60) / 1000.0  # Delta time in seconds
    self._handle_events()  # Process input
    self._update(dt)       # Update logic
    self._render()         # Draw frame
```

---

## Integration Points

**Dependencies:**

- `game.model.GameModel` - Game state
- `game.view.GameView` - Display
- `game.states.state_machine.GameStateManager` - State management
- `pygame-ce` - Event loop and timing (Community Edition for Python 3.14+ compatibility)

**Used by:**

- `game.application.StarTrekRetroRemake` - Creates and starts controller

---

## Change History

- **10-30-2025** - Documentation created
- **10-29-2025** - Initial MVC implementation
