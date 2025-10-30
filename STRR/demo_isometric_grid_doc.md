# Isometric Grid Demo Documentation

**Module:** `STRR/demo_isometric_grid.py`
**Version:** 0.0.1
**Last Updated:** 10-30-2025

## Overview

The Isometric Grid Demo is an interactive demonstration application showcasing the isometric grid rendering system. It provides hands-on examples of grid visualization, cell selection, z-level switching, camera panning, and zoom functionality.

## Purpose

This demo enables:

- Visual testing of isometric grid rendering
- Interactive exploration of grid features
- Understanding of coordinate systems (screen ↔ world)
- Testing of z-level visualization
- Camera control experimentation
- Reference implementation for grid integration

## Features

### Interactive Controls

- **Mouse Click**: Select grid cells with visual feedback
- **Arrow Keys / WASD**: Pan camera in four directions
- **Page Up/Down**: Switch between z-levels
- **+/- Keys**: Zoom in and out
- **0 Key**: Reset zoom to default
- **1/2/3 Keys**: Switch between grid presets
- **H Key**: Toggle help display
- **ESC / Q Keys**: Quit application

### Visual Feedback

- **Selected Cell**: Green highlight overlay
- **Z-Level Colors**: Different colors per z-level for depth perception
- **Help Overlay**: On-screen control reference
- **Status Display**: Current position, z-level, zoom level

### Grid Presets

1. **Default Grid** (Key 1): 20×20 grid, 5 z-levels
2. **Combat Grid** (Key 2): 15×15 grid, 3 z-levels
3. **Sector Grid** (Key 3): 30×30 grid, 5 z-levels

## Usage

### Running the Demo

```bash
# From project root
cd STRR
python demo_isometric_grid.py

# Or with full path
python STRR/demo_isometric_grid.py
```

### Basic Interaction

1. **Select Cells**: Click on any grid cell to select it (green highlight)
2. **Explore Z-Levels**: Use Page Up/Down to see different layers
3. **Pan Camera**: Arrow keys or WASD to move viewport
4. **Zoom**: +/- to zoom, 0 to reset
5. **Switch Presets**: 1/2/3 for different grid configurations
6. **View Help**: Press H to see controls overlay

### Testing Scenarios

#### Coordinate Conversion

1. Click on various cells
2. Observe console output showing screen → world → screen conversion
3. Verify coordinates are consistent

#### Z-Level Visualization

1. Select a cell on z-level 0
2. Press Page Up to move to higher levels
3. Observe how the grid rendering changes
4. Note transparency and color changes

#### Camera Panning

1. Use arrow keys to move camera
2. Click cells at different viewport positions
3. Verify selection works correctly at all positions

#### Zoom Testing

1. Press + to zoom in
2. Click cells and verify selection
3. Press - to zoom out
4. Press 0 to reset zoom
5. Test camera panning at different zoom levels

## Architecture

### Class Structure

#### IsometricGridDemo

Main application class managing the demo.

**Attributes:**

- `screen`: pygame display surface (1920×1080)
- `clock`: pygame clock for frame rate control
- `grid`: GridRenderer instance for drawing
- `running`: Whether demo is active
- `selected_pos`: Currently selected GridPosition (or None)
- `current_z_level`: Active z-level being viewed
- `show_help`: Whether to display help overlay
- `font_small`: Font for UI text (24pt)
- `font_large`: Font for help text (32pt)

**Methods:**

##### `__init__()`

Initialize demo with default grid configuration.

**Actions:**

- Initialize pygame
- Create display surface (1920×1080)
- Create default GridRenderer (20×20 grid, 5 z-levels)
- Set up fonts
- Initialize state variables

##### `run()`

Main demo loop processing events, updating, and rendering.

**Loop:**

1. Process pygame events
2. Draw grid and selected cell
3. Display help overlay (if enabled)
4. Update display
5. Maintain 60 FPS

##### `_handle_events()`

Process pygame events for input handling.

**Handled Events:**

- `QUIT`: Exit application
- `MOUSEBUTTONDOWN`: Select grid cell at mouse position
- `KEYDOWN`: Process keyboard commands

##### `_draw()`

Render the current frame.

**Rendering Order:**

1. Clear screen (black background)
2. Render all z-levels with transparency
3. Highlight selected cell (if any)
4. Display help overlay (if enabled)
5. Display position/zoom info

##### `_draw_help()`

Render help overlay showing controls.

**Display:**

- Semi-transparent background
- Control list with key bindings
- Positioned in center of screen

##### `_handle_click(mouse_pos: tuple[int, int])`

Convert mouse click to grid position and select cell.

**Process:**

1. Convert screen coordinates to world coordinates
2. Validate position is within grid bounds
3. Update selected_pos and current_z_level
4. Log coordinates for debugging

##### `_handle_key(key: int)`

Process keyboard input for camera, zoom, and mode changes.

**Key Mappings:**

- `K_ESCAPE, K_q`: Quit
- `K_h`: Toggle help
- `K_PAGEUP, K_PAGEDOWN`: Change z-level
- `K_UP, K_w`: Pan camera up
- `K_DOWN, K_s`: Pan camera down
- `K_LEFT, K_a`: Pan camera left
- `K_RIGHT, K_d`: Pan camera right
- `K_PLUS, K_EQUALS`: Zoom in
- `K_MINUS`: Zoom out
- `K_0`: Reset zoom
- `K_1, K_2, K_3`: Load grid presets

##### `_load_preset(preset: int)`

Load one of three grid configuration presets.

**Presets:**

1. Default: 20×20 grid, 5 z-levels
2. Combat: 15×15 grid, 3 z-levels
3. Sector: 30×30 grid, 5 z-levels

## Integration Examples

### Using Grid in Game Code

```python
from STRR.src.engine.isometric_grid import GridRenderer, GridPosition

# Create grid renderer
grid = GridRenderer(
    width=20,
    height=20,
    max_z_levels=5,
    tile_width=64,
    tile_height=32
)

# Convert screen click to world position
world_pos = grid.screen_to_world(mouse_x, mouse_y, current_z)

# Validate and use position
if grid.is_valid_position(world_pos):
    # Place entity at position
    entity.position = world_pos
```

### Custom Rendering

```python
# In your game loop
for z in range(grid.max_z_levels):
    # Render grid level
    grid.render_z_level(surface, z, current_z)

    # Render entities at this z-level
    for entity in entities_at_z[z]:
        grid.render_entity(surface, entity, current_z)

# Highlight selected cell
if selected_pos:
    grid.highlight_cell(surface, selected_pos)
```

## Console Output

The demo logs coordinate conversions for debugging:

```
Selected: GridPosition(x=10, y=12, z=1)
  Screen coords: (640, 240)
  World coords: (10, 12, 1)
  Round-trip screen: (640, 240)
```

**Interpretation:**

- First line: Selected grid position
- Screen coords: Mouse click location
- World coords: Converted grid position
- Round-trip: Validation that conversion is accurate

## Performance Notes

- **Frame Rate**: Locked at 60 FPS
- **Grid Size**: Performance tested up to 30×30 with 5 z-levels
- **Rendering**: All z-levels rendered every frame (no culling)
- **Memory**: Minimal allocation (no caching, pure functional rendering)

**Performance Characteristics:**

- Default grid (20×20×5): 60 FPS stable
- Combat grid (15×15×3): 60 FPS stable
- Sector grid (30×30×5): 60 FPS stable (may vary on older hardware)

## Troubleshooting

### Common Issues

**Grid not rendering:**

- Verify pygame-ce is installed correctly
- Check display surface initialization
- Ensure camera offset is set properly

**Mouse clicks not selecting cells:**

- Verify coordinate conversion is working
- Check screen position relative to grid
- Ensure grid bounds validation is correct

**Z-levels not switching:**

- Check z-level range (0 to max_z_levels-1)
- Verify Page Up/Down keys are detected
- Ensure z-level is passed to rendering methods

**Camera panning not working:**

- Verify arrow key detection
- Check camera offset delta values
- Ensure offset is applied during rendering

## Development Use

### Testing New Features

Use the demo to test new grid features before integrating into main game:

1. Add feature to GridRenderer
2. Add corresponding control to demo
3. Test interactively with visual feedback
4. Integrate into main game once validated

### Learning Tool

New developers can use this demo to understand:

- Isometric projection mathematics
- Coordinate conversion (screen ↔ world)
- Event handling in pygame
- Grid-based positioning
- Z-level visualization

## Related Documentation

- **GridRenderer**: `STRR/src/engine/isometric_grid_doc.md`
- **GameView**: `STRR/src/game/view_doc.md`
- **Architecture**: `/docs/ARCHITECTURE.md`
- **Design**: `/docs/DESIGN.md`

## Linux Compatibility

The demo is fully compatible with Linux systems:

- Uses pygame-ce for cross-platform rendering
- Path handling uses pathlib
- No OS-specific dependencies
- Tested on Linux environments

**Python Requirements:** 3.14+ for latest language features

## Future Enhancements

### Planned Features

- Entity placement demo (drag-and-drop ships)
- Pathfinding visualization
- Line of sight demonstration
- Fog of war preview
- Animation preview (movement, attacks)
- Performance profiling overlay

### User Experience

- Mouse wheel zoom support
- Right-click context menu
- Grid coordinate display at cursor
- Ruler tool for distance measurement
- Screenshot capability
