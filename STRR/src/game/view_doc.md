# Game View Documentation

**File:** `STRR/src/game/view.py`
**Version:** 0.0.1
**Last Updated:** 10-30-2025

---

## Purpose

The `view.py` file implements the **View** component of the MVC architecture. It is responsible for **all visual output** including:

- PySide6 UI windows, menus, and dialogs
- pygame-ce game surface rendering
- Displaying game state visually
- User interface updates

**Key principle:** The View reads from the Model but never modifies it. All state changes go through the Controller.

---

## Architecture

### MVC View Pattern

```
Model → Controller → View (this file) → Display
```

The View receives updates from the Controller and renders the current game state.

### Dual-Framework Integration

- **PySide6:** Main window, menus, dialogs, settings UI
- **pygame-ce:** Game rendering surface embedded in PySide6 window

---

## Classes

### GameView

**Purpose:** Main view coordinator managing all visual output

**Key Attributes:**

- `controller` (GameController): Reference to controller for coordinated actions
- `main_window` (QMainWindow): PySide6 main application window
- `game_surface` (pygame.Surface): pygame-ce rendering surface (800x600)
- `update_timer` (QTimer): 60 FPS update timer

**Key Methods:**

- `run()`: Show window and start event loop
- `close()`: Cleanup and close
- `render_sector_map(sector_map, game_objects)`: Render game view
- `show_combat_dialog(result)`: Display combat results
- `show_ship_status(ship)`: Display ship information
- `show_message(message)`: Display message to user

---

## Usage Example

```python
from game.view import GameView
from game.controller import GameController
from game.model import GameModel

model = GameModel()
controller = GameController(model)
view = GameView(controller)

controller.set_view(view)
view.run()  # Show window
```

---

## Integration Points

**Dependencies:**

- `game.controller.GameController` - For coordinated actions
- `pygame-ce` - Game rendering (Community Edition for Python 3.14+ compatibility)
- `PySide6.QtWidgets` - UI framework

**Used by:**

- `game.application.StarTrekRetroRemake` - Creates and manages view
- `game.controller.GameController` - Updates view based on model changes

---

## Implementation Status

**Current:** Placeholder implementation with stubs
**TODO:** Full pygame-ce/PySide6 integration, rendering logic

---

## Change History

- **10-30-2025** - Documentation created
- **10-29-2025** - Initial stub implementation
