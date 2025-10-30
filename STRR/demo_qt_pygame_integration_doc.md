# demo_qt_pygame_integration.py Documentation

## Purpose

Standalone demonstration of PySide6 + pygame-ce integration pattern. Shows how to embed pygame rendering into a Qt window with proper layout, controls, and event handling.

## Architecture

### Key Components

**PygameWidget Class:**

- Custom `QLabel` subclass for displaying pygame surfaces
- Handles conversion from pygame surface to Qt pixmap
- Pre-allocates buffer for efficient image conversion
- Fixed size widget (800x600) for game display

**MainWindow Class:**

- Main Qt window with horizontal layout
- Left panel: Qt controls (buttons, labels, status)
- Right panel: pygame rendering area
- Update timer for ~60 FPS rendering

## Features

### Visual Elements

**Control Panel:**

- Title and info text
- Start, Pause/Resume, Reset buttons
- Status display area
- Frame counter
- Quit button

**Game Display:**

- 800x600 pygame surface
- Grid background (space theme)
- Bouncing circle animation (USS Enterprise)
- Star field effect
- Text labels

### Animation

Simple bouncing ball physics:

- Circle moves across screen
- Bounces off edges
- Velocity: (2, 1.5) pixels per frame
- Represents starship movement

### Controls

- **Start Game**: Update status message
- **Pause/Resume**: Toggle animation timer
- **Reset Animation**: Reset circle to initial position
- **Quit**: Close application and cleanup

## Implementation Details

### Surface Conversion

```python
surface_data = pygame.image.tobytes(self.surface, "RGB")
self._qimage_buffer[:] = surface_data
qimage = QImage(self._qimage_buffer, w, h, w * 3, QImage.Format_RGB888)
pixmap = QPixmap.fromImage(qimage)
self.setPixmap(pixmap)
```

**Why this approach:**

- Reuses buffer to prevent memory allocations each frame
- Uses modern `tobytes()` API (not deprecated `tostring()`)
- Efficient for 60 FPS rendering

### Update Loop

Timer-based update at 60 FPS:

- QTimer with 16ms interval
- pygame clock for frame timing
- Delta time calculation for frame-rate independence
- Immediate mode rendering (clear → draw → display)

### Layout Structure

```
QMainWindow
└── QWidget (central)
    └── QHBoxLayout (main)
        ├── QGroupBox (control panel)
        │   └── QVBoxLayout
        │       ├── QLabel (title)
        │       ├── QLabel (info)
        │       ├── QPushButton (start)
        │       ├── QPushButton (pause)
        │       ├── QPushButton (reset)
        │       ├── QLabel (status)
        │       ├── QLabel (frames)
        │       ├── Stretch
        │       └── QPushButton (quit)
        └── QWidget (game area)
            └── QVBoxLayout
                ├── QLabel (title)
                ├── PygameWidget (game display)
                └── QLabel (instructions)
```

## Usage

### Running the Demo

```bash
cd /home/chris/GitHub/Star-Trek-Retro-Remake
.venv/bin/python STRR/demo_qt_pygame_integration.py
```

### Expected Behavior

1. Window opens with control panel on left, game area on right
2. Animation starts immediately (bouncing circle)
3. Frame counter updates every 60 frames
4. All buttons functional
5. Clean shutdown when window closed

## Learning Points

### For Developers

**Key Patterns:**

1. Qt layout management (HBoxLayout, VBoxLayout)
2. pygame surface rendering without display window
3. Efficient image format conversion
4. Event-driven architecture with Qt signals/slots
5. Resource cleanup on application exit

**Common Mistakes to Avoid:**

1. Don't call `pygame.display.set_mode()` - use `pygame.Surface()`
2. Don't use `pygame.event.get()` - let Qt handle events
3. Don't create new buffers each frame - reuse pre-allocated buffers
4. Don't forget `pygame.quit()` in `closeEvent()`

## Integration with Main Game

This demo shows the pattern used in `STRR/src/game/view.py`:

**Similarities:**

- Same surface conversion approach
- Timer-based update loop
- Custom widget for pygame display
- Qt layout for controls

**Differences:**

- Main game has full MVC architecture
- Complex game state management
- 3D grid rendering with isometric projection
- Mouse and keyboard input forwarding to controller

## Testing

### Manual Tests

1. **Animation**: Circle should bounce smoothly
2. **Pause**: Animation should freeze/resume
3. **Reset**: Circle returns to starting position
4. **Frame Counter**: Updates regularly
5. **Quit**: Clean exit without errors

### Performance

- Target: 60 FPS
- Typical: 60 FPS (measured with `clock.get_fps()`)
- No frame drops under normal conditions

## Version History

- **v0.0.1** (2025-10-30): Initial demo implementation

## References

- Main implementation: `STRR/src/game/view.py`
- Integration docs: `STRR/src/game/PYSIDE6_PYGAME_INTEGRATION.md`
- Architecture: `/docs/ARCHITECTURE.md`
