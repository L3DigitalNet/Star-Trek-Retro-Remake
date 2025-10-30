# PySide6 + pygame-ce Integration Documentation

## Overview

This document describes the integration pattern used to embed pygame-ce rendering into PySide6 Qt windows in the Star Trek Retro Remake project.

## Architecture Pattern

The integration follows a clean separation between:

- **PySide6 (Qt6)**: UI framework for menus, dialogs, controls, and window management
- **pygame-ce**: Game rendering engine for the actual game display

## Key Components

### 1. Main Window Layout

The main window uses a horizontal layout (`QHBoxLayout`) with two sections:

```
┌──────────────────────────────────────────────────────┐
│                   Main Window                        │
├────────────────┬─────────────────────────────────────┤
│                │                                     │
│  Control Panel │     Game Display Area               │
│   (Qt Widgets) │    (pygame Surface)                 │
│                │                                     │
│  - Status      │    - Grid Rendering                 │
│  - Buttons     │    - Game Objects                   │
│  - Messages    │    - Effects                        │
│                │                                     │
└────────────────┴─────────────────────────────────────┘
```

### 2. GameDisplay Widget

Custom `QLabel` subclass that:

- Displays pygame surface as `QPixmap`
- Captures mouse and keyboard events
- Forwards events to game controller
- Handles coordinate conversion

**Key Methods:**

- `mousePressEvent()`: Convert Qt mouse clicks to pygame coordinates
- `keyPressEvent()`: Convert Qt key events to pygame key constants

### 3. Surface to Pixmap Conversion

Efficient conversion using pre-allocated buffer:

```python
# In __init__:
self._qimage_buffer = bytearray(width * height * 3)

# In update loop:
surface_data = pygame.image.tobytes(self.surface, "RGB")
self._qimage_buffer[:] = surface_data
qimage = QImage(self._qimage_buffer, w, h, w * 3, QImage.Format_RGB888)
pixmap = QPixmap.fromImage(qimage)
label.setPixmap(pixmap)
```

This approach:

- Reuses buffer to reduce garbage collection
- Uses modern `tobytes()` API (not deprecated `tostring()`)
- Maintains 60 FPS performance

### 4. Update Loop

Uses Qt `QTimer` for regular updates (~60 FPS):

```python
self.update_timer = QTimer()
self.update_timer.timeout.connect(self._update_display)
self.update_timer.start(16)  # ~60 FPS
```

**Update Cycle:**

1. Calculate delta time
2. Update game logic
3. Render to pygame surface
4. Convert surface to QPixmap
5. Update QLabel display

### 5. Event Handling

**Mouse Events:**

- Captured by `GameDisplay.mousePressEvent()`
- Converted from widget coordinates to pygame surface coordinates
- Account for centering and widget resize
- Forwarded to controller

**Keyboard Events:**

- Captured by `GameDisplay.keyPressEvent()`
- Mapped from Qt key constants to pygame key constants
- Forwarded to controller

**Important:** Do NOT use `pygame.event.get()` or `pygame.event.pump()` - all events handled through Qt!

## Implementation Files

### Demo Example

- **File:** `STRR/demo_qt_pygame_integration.py`
- **Purpose:** Standalone demo showing basic integration pattern
- **Features:**
  - Control panel with buttons
  - pygame rendering with animation
  - Mouse and keyboard input
  - Clean shutdown handling

### Production Implementation

- **File:** `STRR/src/game/view.py`
- **Class:** `GameView`
- **Features:**
  - Full game UI with control panel
  - Ship status display
  - Message area
  - Z-level indicator
  - Game controls (New, Save, Load, Settings)

## Best Practices

### 1. Resource Management

```python
def closeEvent(self, event):
    """Handle window close - cleanup pygame."""
    self.update_timer.stop()
    pygame.quit()
    event.accept()
```

### 2. Coordinate Conversion

```python
def mousePressEvent(self, event):
    # Get click position
    widget_pos = event.pos()

    # Calculate offset (for centering)
    x_offset = (widget_width - pixmap_width) // 2
    y_offset = (widget_height - pixmap_height) // 2

    # Convert to pygame coordinates
    pixmap_x = widget_x - x_offset
    pixmap_y = widget_y - y_offset

    # Validate bounds before forwarding
    if 0 <= pixmap_x < pixmap_width and 0 <= pixmap_y < pixmap_height:
        self.view.controller._handle_mouse_click((pixmap_x, pixmap_y))
```

### 3. Performance Optimization

- Pre-allocate buffers for image conversion
- Use cached fonts (don't create every frame)
- Only render visible z-levels
- Use object pooling for temporary objects

### 4. Qt and pygame Interaction

- **Initialize pygame without display:** `pygame.init()` (not `pygame.display.set_mode()`)
- **No pygame event loop:** All events through Qt
- **Single timer:** Use Qt timer, not pygame clock for main loop
- **Clean separation:** Game logic separate from rendering

## Common Patterns

### Creating a Control Button

```python
button = QPushButton("Action")
button.clicked.connect(self._on_action)
layout.addWidget(button)
```

### Updating Status Display

```python
self.status_label.setText(f"Status: {status}")
```

### Showing Messages

```python
def show_message(self, message: str) -> None:
    logger.info("Message: %s", message)
    if hasattr(self, "message_display"):
        self.message_display.setText(message)
```

## Troubleshooting

### Issue: Mouse clicks not working

- Check coordinate conversion (widget → pygame)
- Verify click is within pygame surface bounds
- Check if widget has focus

### Issue: Keyboard not responding

- Call `self.game_label.setFocus()` in `_setup_ui()`
- Set focus policy: `setFocusPolicy(Qt.StrongFocus)`
- Verify key mapping (Qt keys → pygame keys)

### Issue: Poor performance

- Check update timer frequency (16ms = 60 FPS)
- Verify buffer reuse (not creating new buffers each frame)
- Profile with `pygame.time.Clock().get_fps()`

### Issue: Deprecation warnings

- Use `pygame.image.tobytes()` not `tostring()`
- Check pygame-ce version compatibility

## Version History

- **v0.0.9** (2025-10-30): Enhanced UI with control panel, proper layout
- **v0.0.8** (2025-10-30): Fixed coordinate conversion bugs
- **v0.0.7** (2025-10-30): Initial integration implementation

## References

- PySide6 Documentation: <https://doc.qt.io/qtforpython-6/>
- pygame-ce Documentation: <https://pyga.me/docs/>
- Qt Layouts: <https://doc.qt.io/qtforpython-6/PySide6/QtWidgets/QLayout.html>
- QTimer: <https://doc.qt.io/qtforpython-6/PySide6/QtCore/QTimer.html>
