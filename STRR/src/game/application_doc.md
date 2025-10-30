# Application Module Documentation

**File:** `STRR/src/game/application.py`
**Version:** 0.0.1
**Last Updated:** 10-30-2025

---

## Purpose

The `application.py` module serves as the **main application coordinator** for the Star Trek Retro Remake game. It implements the **MVC (Model-View-Controller)** pattern and is responsible for:

- Creating and connecting the Model, View, and Controller components
- Initializing both PyGame (for game rendering) and PySide6 (for UI/menus)
- Managing the application lifecycle (startup, main loop, shutdown)
- Coordinating between the game engine and UI framework

This is the **central hub** that brings all major game systems together.

---

## Architecture

### Design Pattern: MVC (Model-View-Controller)

The application uses the classic MVC pattern with clear separation:

```
StarTrekRetroRemake (Application)
    ├── GameModel (Pure game logic)
    ├── GameView (Rendering & UI)
    └── GameController (Input & coordination)
```

### Framework Separation

- **PyGame:** Used for game rendering, the game loop, and event handling
- **PySide6:** Used for menus, dialogs, settings UI, and window management

Both frameworks are initialized here and coordinated throughout the application lifecycle.

### Lifecycle Flow

```
1. __init__() - Initialize systems and create MVC components
2. run() - Start controller and view event loops
3. shutdown() - Clean shutdown of all systems
4. _cleanup() - Resource cleanup
```

---

## Classes

### StarTrekRetroRemake

**Purpose:** Main application class that coordinates all game systems

**Attributes:**

- `model` (GameModel): Game logic and state management component
- `view` (GameView): UI rendering and display management component
- `controller` (GameController): Input handling and coordination component
- `running` (bool): Application execution state flag
- `qt_app` (QApplication): PySide6 application instance

**Public Methods:**

#### `run() -> None`

Starts the application main loop.

**Behavior:**

1. Starts the game controller
2. Runs the PySide6 event loop (blocking call)
3. Performs clean shutdown when loop exits

**Usage:**

```python
game = StarTrekRetroRemake()
game.run()  # Starts the game and blocks until quit
```

#### `shutdown() -> None`

Initiates a clean shutdown of the application.

**Behavior:**

1. Sets `running` flag to False
2. Stops the game controller
3. Closes the view
4. Triggers cleanup procedures

**Usage:**

```python
# Called when user quits the game
game.shutdown()
```

**Private Methods:**

#### `_initialize_systems() -> None`

Initializes PyGame and PySide6 frameworks.

**Behavior:**

1. Calls `pygame.init()` to initialize all PyGame subsystems
2. Creates or retrieves PySide6 QApplication instance

**⚠️ Important:** This is where you should add PyGame window initialization:

```python
# Add in _initialize_systems():
pygame.display.set_mode((1024, 768))
pygame.display.set_caption("Star Trek Retro Remake")
```

#### `_cleanup() -> None`

Cleans up resources on shutdown.

**Behavior:**

1. Calls `pygame.quit()` to cleanup PyGame
2. Quits the Qt application

---

## Usage Examples

### Example 1: Basic Application Startup

```python
from game.application import StarTrekRetroRemake

def main():
    # Create the application
    app = StarTrekRetroRemake()

    # Start the game (blocks until quit)
    app.run()

if __name__ == "__main__":
    main()
```

### Example 2: Accessing MVC Components

```python
app = StarTrekRetroRemake()

# Access the game model
print(f"Turn number: {app.model.turn_manager.turn_number}")

# Access the view
app.view.show_message("Welcome to Star Trek!")

# Access the controller
app.controller.start_new_game()
```

### Example 3: Graceful Shutdown

```python
app = StarTrekRetroRemake()

try:
    app.run()
except KeyboardInterrupt:
    print("Interrupted by user")
    app.shutdown()
```

---

## Integration Points

### Dependencies

**Direct imports:**

- `game.model.GameModel` - Game logic and state
- `game.view.GameView` - Rendering and UI
- `game.controller.GameController` - Input and coordination

**External libraries:**

- `pygame` - Required for game rendering engine
- `PySide6.QtWidgets.QApplication` - Required for Qt UI framework

**Why these dependencies:**

- `pygame`: Provides the game rendering surface and event loop
- `PySide6`: Provides professional UI components for menus and dialogs
- MVC components: Core architecture requires all three to function

### Used By

**Direct users:**

- `main.py` - Entry point that creates and runs this application

**Indirect users:**

- Any code that needs to access the application context or MVC components

---

## Configuration

### Requirements

**System:**

- Linux environment (primary target)
- Python 3.14+

**Libraries:**

- PyGame (game engine)
- PySide6 (UI framework)

### Initialization Order

**Critical:** Systems must be initialized in this order:

1. PyGame initialization (`pygame.init()`)
2. Qt application creation
3. Model creation (pure logic, no dependencies)
4. Controller creation (depends on model)
5. View creation (depends on controller)
6. Controller-View linkage (`controller.set_view()`)

**Rationale:** This order ensures each component has its dependencies available when created.

---

## Common Patterns

### Pattern 1: Adding Window Configuration

To configure the PyGame window during startup, modify `_initialize_systems()`:

```python
def _initialize_systems(self) -> None:
    """Initialize PyGame and PySide6 systems."""
    # Initialize PyGame for game rendering
    pygame.init()

    # Configure display
    self.screen = pygame.display.set_mode((1024, 768))
    pygame.display.set_caption("Star Trek Retro Remake")

    # Set icon (optional)
    # icon = pygame.image.load("assets/icon.png")
    # pygame.display.set_icon(icon)

    # Initialize PySide6 application
    if not QApplication.instance():
        self.qt_app = QApplication(sys.argv)
    else:
        self.qt_app = QApplication.instance()
```

### Pattern 2: Adding Splash Screen

To show a splash screen during initialization:

```python
def __init__(self):
    """Initialize the Star Trek Retro Remake application."""
    # Initialize core systems
    self._initialize_systems()

    # Show splash screen (PySide6)
    self._show_splash_screen()

    # Create MVC components (takes time)
    self.model = GameModel()
    self.controller = GameController(self.model)
    self.view = GameView(self.controller)

    # Hide splash screen
    self._hide_splash_screen()

    # Continue with setup...
```

### Pattern 3: Handling Multiple Game Instances

The application is designed as a singleton. For multiple games:

```python
# Don't do this:
game1 = StarTrekRetroRemake()
game2 = StarTrekRetroRemake()  # Will cause Qt application conflicts!

# Instead, shutdown the first before creating another:
game1 = StarTrekRetroRemake()
game1.run()
game1.shutdown()

game2 = StarTrekRetroRemake()
game2.run()
```

---

## Troubleshooting

### Issue: Qt Application Already Exists Warning

**Symptom:** Warning about QApplication already being instantiated

**Cause:** Creating multiple StarTrekRetroRemake instances without cleanup

**Solution:**

```python
# Always shutdown before creating a new instance
if app:
    app.shutdown()
app = StarTrekRetroRemake()
```

### Issue: PyGame Window Not Appearing

**Symptom:** Game starts but no window is visible

**Cause:** `pygame.display.set_mode()` not called in `_initialize_systems()`

**Solution:** Add display initialization:

```python
def _initialize_systems(self) -> None:
    pygame.init()
    pygame.display.set_mode((1024, 768))  # Add this line
    # ... rest of initialization
```

### Issue: Import Errors for MVC Components

**Symptom:** `ImportError` or `ModuleNotFoundError` for model/view/controller

**Cause:** Python path not set up correctly

**Solution:** Ensure `main.py` adds the correct path:

```python
sys.path.insert(0, str(Path(__file__).parent / "src"))
```

### Issue: Game Freezes on Startup

**Symptom:** Application hangs during initialization

**Cause:** Circular import or blocking operation in component initialization

**Solution:**

1. Check for circular imports in model/view/controller
2. Ensure no blocking I/O during `__init__`
3. Move heavy initialization to `run()` method

---

## Notes

### PyGame vs PySide6 Event Loops

The application runs **two event loops**:

1. **PyGame event loop:** Managed by GameController for game events
2. **Qt event loop:** Managed by `QApplication.exec()` for UI events

These are coordinated through the View, which bridges both systems.

### Memory Management

- The application creates MVC components during `__init__`
- Components are not explicitly deleted but cleaned up during `_cleanup()`
- Python's garbage collector handles memory after shutdown

### Future Enhancements

Planned features for this module:

- [ ] Splash screen during loading
- [ ] Configuration file loading before MVC creation
- [ ] Performance profiling hooks
- [ ] Multiple game instance support with proper isolation
- [ ] Auto-save on shutdown
- [ ] Crash recovery system

---

## Change History

- **10-30-2025** - Initial documentation created
- **10-29-2025** - Module created with MVC pattern implementation
