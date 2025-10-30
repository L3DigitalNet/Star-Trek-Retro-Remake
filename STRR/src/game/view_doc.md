# Game View Documentation

**File:** `STRR/src/game/view.py`
**Version:** 0.0.10
**Last Updated:** 10-30-2025

---

## Purpose

The `view.py` file implements the **View** component of the MVC architecture. It is responsible for **all visual output** including:

- PySide6 UI windows, menus, and dialogs (loaded from Qt Designer .ui files)
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

### Qt Designer Integration

The UI is designed in **Qt Designer** and loaded from `.ui` files:

- UI files located in: `STRR/src/ui/designer/`
- Main window: `main_window.ui`
- Runtime loading via `QUiLoader`
- Custom widgets replace placeholders at runtime

**See:** `/docs/QT_DESIGNER_WORKFLOW.md` for complete Qt Designer workflow documentation

### Dual-Framework Integration

- **PySide6:** Main window, menus, dialogs, settings UI (designed in Qt Designer)
- **pygame-ce:** Game rendering surface embedded in PySide6 window

---

## Classes

### GameDisplay

**Purpose:** Custom QLabel widget for game display with mouse and keyboard input

**Inherits:** `QLabel`

**Key Features:**

- Captures mouse clicks and converts widget coordinates to pygame surface coordinates
- Handles keyboard input and forwards to controller
- Replaces placeholder `gameDisplay` label from UI file at runtime

**Key Methods:**

- `mousePressEvent(event)`: Handle mouse clicks with coordinate conversion
- `keyPressEvent(event)`: Handle keyboard input (arrows, PageUp/Down, zoom, etc.)

### GameView

**Purpose:** Main view coordinator managing all visual output

**Key Attributes:**

- `controller` (GameController): Reference to controller for coordinated actions
- `main_window` (QMainWindow): PySide6 main application window (loaded from .ui file)
- `game_surface` (pygame.Surface): pygame-ce rendering surface (1280x900)
- `game_label` (GameDisplay): Custom widget for game display
- `grid_renderer` (GridRenderer): Isometric grid renderer
- `update_timer` (QTimer): 60 FPS update timer
- `ship_status_label` (QLabel): Ship status display (from UI file)
- `z_level_label` (QLabel): Z-level indicator (from UI file)
- `message_display` (QLabel): Message area (from UI file)

**Key Methods:**

**Lifecycle:**

- `run()`: Show window and start event loop
- `close()`: Cleanup and close

**Rendering:**

- `render_sector_map(sector_map, game_objects)`: Render game view with isometric grid
- `set_z_level(z_level)`: Change visible z-level
- `set_selected_cell(position)`: Highlight selected grid cell
- `clear_selection()`: Clear grid cell selection

**UI Updates:**

- `show_combat_dialog(result)`: Display combat results
- `show_ship_status(ship)`: Display ship information
- `show_message(message)`: Display message to user

**Private Methods:**

- `_load_ui()`: Load UI from Qt Designer .ui file
- `_connect_signals()`: Connect button signals to handler methods
- `_setup_game_display()`: Replace placeholder with custom GameDisplay widget
- `_update_display()`: Main render loop (60 FPS)
- `_render_game_object(obj)`: Render individual game objects
- `_on_new_game()`, `_on_save_game()`, etc.: UI button handlers

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

## Qt Designer Workflow

The UI is designed in Qt Designer and loaded at runtime:

**UI File Location:**
`STRR/src/ui/designer/main_window.ui`

**Loading Process:**

1. `_load_ui()`: Load .ui file with `QUiLoader`
2. Find and cache widget references by object name
3. `_connect_signals()`: Connect button signals to handlers
4. `_setup_game_display()`: Replace placeholder with custom `GameDisplay`

**Modifying UI:**

1. Open `main_window.ui` in Qt Designer
2. Make changes and save
3. Run application - changes load automatically

**See:** `/docs/QT_DESIGNER_WORKFLOW.md` for complete workflow documentation

---

## Implementation Status

**Current:** Fully functional with Qt Designer integration, isometric grid rendering
**TODO:** Combat dialogs, additional UI panels, settings dialog

---

## Change History

- **10-30-2025** - Qt Designer integration, updated documentation
- **10-29-2025** - Initial stub implementation
