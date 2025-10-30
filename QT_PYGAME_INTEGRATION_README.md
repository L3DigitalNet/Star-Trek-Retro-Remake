# PySide6 + pygame-ce Integration

## Quick Start

### Run the Demo

```bash
cd /home/chris/GitHub/Star-Trek-Retro-Remake
.venv/bin/python STRR/demo_qt_pygame_integration.py
```

### Run the Main Game

```bash
cd /home/chris/GitHub/Star-Trek-Retro-Remake
.venv/bin/python STRR/main.py
```

## What's New

The game now features a proper Qt window with:

- **Control Panel** (left side):
  - Ship status display
  - Z-level indicator
  - Game control buttons (New, Save, Load, Settings)
  - Message display area

- **Game Display** (right side):
  - pygame-ce rendering surface (1280x900)
  - Isometric grid view
  - Interactive game objects
  - Mouse and keyboard controls

## Key Files

- `STRR/demo_qt_pygame_integration.py` - Simple standalone demo
- `STRR/src/game/view.py` - Production game view with full UI
- `STRR/src/game/PYSIDE6_PYGAME_INTEGRATION.md` - Technical documentation

## Architecture

```
Main Window (PySide6)
├── Control Panel (Qt Widgets)
│   ├── Status displays
│   ├── Buttons
│   └── Message area
└── Game Display (pygame-ce)
    ├── Isometric grid
    ├── Game objects
    └── Effects
```

## Features

### Mouse Controls

- **Left Click**: Select grid cell / Move ship

### Keyboard Controls

- **PageUp/PageDown**: Change Z-level
- **+/-**: Zoom in/out
- **0**: Reset zoom
- **Arrow Keys**: Pan camera

### UI Controls

- **New Game**: Start fresh game
- **Save/Load**: Game state persistence (coming soon)
- **Settings**: Configure game (coming soon)
- **Quit**: Exit application

## Implementation Highlights

### Efficient Rendering

- Pre-allocated buffers for image conversion
- 60 FPS update rate via QTimer
- Reusable resources (fonts, surfaces)

### Event Handling

- Qt handles all events (no pygame event loop)
- Mouse coordinate conversion (Qt → pygame)
- Keyboard mapping (Qt keys → pygame keys)

### Clean Separation

- MVC architecture maintained
- Game logic independent of UI
- pygame rendering separate from Qt widgets

## Development Notes

### Do's ✅

- Use `pygame.init()` (no display mode)
- Handle all events through Qt
- Pre-allocate buffers for performance
- Use `pygame.image.tobytes()` (not `tostring()`)

### Don'ts ❌

- Don't use `pygame.display.set_mode()`
- Don't use `pygame.event.get()` or `pygame.event.pump()`
- Don't create new buffers each frame
- Don't forget `pygame.quit()` in cleanup

## Next Steps

Planned enhancements:

- Dialog windows (settings, save/load)
- Menu bar integration
- Status indicators and animations
- Tooltips and help system
- Sound controls panel

## Documentation

See detailed documentation:

- Technical: `STRR/src/game/PYSIDE6_PYGAME_INTEGRATION.md`
- Demo: `STRR/demo_qt_pygame_integration_doc.md`
- Architecture: `/docs/ARCHITECTURE.md`
