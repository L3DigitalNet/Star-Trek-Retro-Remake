# Isometric Grid Renderer Documentation

## Overview

The `isometric_grid.py` module provides a comprehensive system for rendering isometric grids with 3D z-level support for the Star Trek Retro Remake game. This module handles the mathematical conversion between 3D world coordinates and 2D screen coordinates, enabling visualization of space positioning with vertical depth.

## Purpose

This module serves as the core rendering engine for the game's spatial representation:

- **Isometric Projection**: Converts 3D grid coordinates (x, y, z) to 2D screen space
- **Z-Level Support**: Visualizes vertical positioning in space (e.g., different orbital altitudes)
- **Grid Visualization**: Renders grid lines for spatial reference
- **Interactive Selection**: Supports cell highlighting and mouse-to-world coordinate conversion
- **View Modes**: Provides preset configurations for different game views (combat, sector map)

## Architecture

### Design Pattern

The module follows the **Renderer Pattern** with:

- **GridRenderer**: Main rendering class handling all grid operations
- **GridPosition**: Immutable data class representing 3D coordinates
- **Factory Functions**: Convenience functions for creating common grid configurations

### Integration with MVC

- **Model**: GridPosition represents spatial data
- **View**: GridRenderer provides rendering capabilities
- **Controller**: Receives user input via screen_to_world conversion

## Classes

### GridPosition

Immutable dataclass representing a 3D grid coordinate.

#### Attributes

- `x: int` - Grid X coordinate
- `y: int` - Grid Y coordinate  
- `z: int` - Grid Z coordinate (default 0, represents elevation/depth)

#### Methods

```python
def distance_to(self, other: GridPosition) -> float
```
Calculate 3D Euclidean distance to another position.

**Parameters:**
- `other` - Target position

**Returns:** Distance as float

**Example:**
```python
pos1 = GridPosition(0, 0, 0)
pos2 = GridPosition(3, 4, 0)
distance = pos1.distance_to(pos2)  # Returns 5.0
```

#### Operators

- `__add__`: Add two positions component-wise
- `__sub__`: Subtract two positions component-wise

**Example:**
```python
pos1 = GridPosition(5, 10, 2)
pos2 = GridPosition(2, 3, 1)
result = pos1 + pos2  # GridPosition(7, 13, 3)
```

### GridRenderer

Main class for isometric grid rendering with z-level support.

#### Initialization

```python
def __init__(
    self,
    tile_width: int = 64,
    tile_height: int = 32,
    grid_width: int = 20,
    grid_height: int = 20,
    max_z_levels: int = 4,
    camera_offset: tuple[int, int] = (400, 100)
)
```

**Parameters:**
- `tile_width` - Width of each isometric tile in pixels (default 64)
- `tile_height` - Height of each isometric tile in pixels (default 32)
- `grid_width` - Number of tiles in X direction (default 20)
- `grid_height` - Number of tiles in Y direction (default 20)
- `max_z_levels` - Maximum number of vertical layers (default 4)
- `camera_offset` - Initial camera position in screen space (default (400, 100))

#### Attributes

**Visual Properties:**
- `grid_color` - Color for grid lines (RGB tuple)
- `highlight_color` - Color for highlighted cells (RGB tuple)
- `z_level_offset` - Vertical pixel offset per z-level (default 24)
- `z_level_colors` - Tuple of colors for different z-levels

**Grid Dimensions:**
- `tile_width` - Tile width in pixels (immutable)
- `tile_height` - Tile height in pixels (immutable)
- `grid_width` - Grid width in tiles (immutable)
- `grid_height` - Grid height in tiles (immutable)
- `max_z_levels` - Maximum z-levels (immutable)

**Camera:**
- `camera_offset` - Current camera position [x, y]

#### Public Methods

##### world_to_screen

```python
def world_to_screen(self, position: GridPosition) -> tuple[int, int]
```

Convert 3D world coordinates to 2D screen coordinates using isometric projection.

**Projection Formula:**
```
screen_x = (world_x - world_y) * (tile_width / 2) + camera_x
screen_y = (world_x + world_y) * (tile_height / 2) - (world_z * z_offset) + camera_y
```

**Parameters:**
- `position` - Grid position in world coordinates

**Returns:** Tuple of (screen_x, screen_y) in pixels

**Example:**
```python
renderer = GridRenderer()
world_pos = GridPosition(5, 5, 1)
screen_pos = renderer.world_to_screen(world_pos)
# Returns screen coordinates where this cell should be drawn
```

##### screen_to_world

```python
def screen_to_world(
    self,
    screen_pos: tuple[int, int],
    z_level: int = 0
) -> GridPosition
```

Convert 2D screen coordinates to 3D world coordinates (inverse projection).

**Parameters:**
- `screen_pos` - Screen position (x, y) in pixels
- `z_level` - Z-level to calculate for (default 0)

**Returns:** GridPosition in world coordinates

**Example:**
```python
renderer = GridRenderer()
mouse_pos = (500, 300)
grid_pos = renderer.screen_to_world(mouse_pos, z_level=1)
# Returns which grid cell was clicked at z-level 1
```

##### render_grid

```python
def render_grid(
    self,
    surface: pygame.Surface,
    visible_z_levels: list[int] | None = None
) -> None
```

Render the complete isometric grid with all or specified z-levels.

**Parameters:**
- `surface` - pygame Surface to render on
- `visible_z_levels` - List of z-levels to render (None = all levels)

**Example:**
```python
renderer = GridRenderer()
screen = pygame.display.set_mode((800, 600))
renderer.render_grid(screen)  # Draw all z-levels
renderer.render_grid(screen, [0, 1, 2])  # Draw only first 3 levels
```

##### render_z_level

```python
def render_z_level(self, surface: pygame.Surface, z_level: int) -> None
```

Render a specific z-level of the grid.

**Parameters:**
- `surface` - pygame Surface to render on
- `z_level` - Z-level to render (0 to max_z_levels-1)

**Example:**
```python
renderer = GridRenderer(max_z_levels=5)
screen = pygame.display.set_mode((800, 600))
renderer.render_z_level(screen, 2)  # Draw only z-level 2
```

##### render_cell_highlight

```python
def render_cell_highlight(
    self,
    surface: pygame.Surface,
    position: GridPosition,
    color: tuple[int, int, int] | None = None
) -> None
```

Highlight a specific grid cell with a filled diamond shape.

**Parameters:**
- `surface` - pygame Surface to render on
- `position` - Grid position to highlight
- `color` - Highlight color (None = use default yellow)

**Example:**
```python
renderer = GridRenderer()
screen = pygame.display.set_mode((800, 600))
selected_cell = GridPosition(10, 5, 1)
renderer.render_cell_highlight(screen, selected_cell)
# Or with custom color
renderer.render_cell_highlight(screen, selected_cell, (255, 0, 0))
```

##### is_in_bounds

```python
def is_in_bounds(self, position: GridPosition) -> bool
```

Check if a position is within grid bounds.

**Parameters:**
- `position` - Grid position to check

**Returns:** True if valid, False otherwise

**Example:**
```python
renderer = GridRenderer(grid_width=20, grid_height=20, max_z_levels=4)
pos1 = GridPosition(5, 10, 2)
pos2 = GridPosition(25, 10, 2)
renderer.is_in_bounds(pos1)  # True
renderer.is_in_bounds(pos2)  # False (x out of bounds)
```

##### set_camera_offset

```python
def set_camera_offset(self, offset: tuple[int, int]) -> None
```

Update the camera position offset for panning/scrolling.

**Parameters:**
- `offset` - New camera offset (x, y) in pixels

**Example:**
```python
renderer = GridRenderer()
renderer.set_camera_offset((500, 200))  # Pan camera to new position
```

#### Private Methods

##### _draw_grid_lines

Internal method to draw grid lines for a specific z-level.

##### _calculate_cell_corners

Internal method to calculate the four corner positions of an isometric cell.

## Factory Functions

### create_default_grid

```python
def create_default_grid() -> GridRenderer
```

Create a grid renderer with default settings suitable for general use.

**Returns:** GridRenderer with standard parameters

**Example:**
```python
renderer = create_default_grid()
```

### create_combat_grid

```python
def create_combat_grid() -> GridRenderer
```

Create a grid renderer optimized for combat view (smaller, more focused).

**Configuration:**
- 48x24 pixel tiles
- 15x15 grid
- 3 z-levels
- Camera at (400, 200)

**Returns:** GridRenderer configured for combat

**Example:**
```python
combat_renderer = create_combat_grid()
```

### create_sector_grid

```python
def create_sector_grid() -> GridRenderer
```

Create a grid renderer optimized for sector map view (larger, strategic).

**Configuration:**
- 32x16 pixel tiles
- 30x30 grid
- 5 z-levels
- Camera at (400, 100)

**Returns:** GridRenderer configured for sector map

**Example:**
```python
sector_renderer = create_sector_grid()
```

## Usage Examples

### Basic Grid Rendering

```python
import pygame
from star_trek_retro_remake.src.engine.isometric_grid import GridRenderer, GridPosition

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Create grid renderer
grid = GridRenderer(tile_width=64, tile_height=32, grid_width=10, grid_height=10)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Clear screen
    screen.fill((0, 0, 0))
    
    # Render grid
    grid.render_grid(screen)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
```

### Interactive Cell Selection

```python
import pygame
from star_trek_retro_remake.src.engine.isometric_grid import GridRenderer, GridPosition

pygame.init()
screen = pygame.display.set_mode((800, 600))
grid = GridRenderer()

selected_cell = None
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Convert mouse click to grid position
            mouse_pos = pygame.mouse.get_pos()
            selected_cell = grid.screen_to_world(mouse_pos, z_level=0)
            
            # Validate selection
            if not grid.is_in_bounds(selected_cell):
                selected_cell = None
    
    screen.fill((0, 0, 0))
    grid.render_grid(screen)
    
    # Highlight selected cell
    if selected_cell:
        grid.render_cell_highlight(screen, selected_cell)
    
    pygame.display.flip()

pygame.quit()
```

### Multi-Level Rendering

```python
import pygame
from star_trek_retro_remake.src.engine.isometric_grid import GridRenderer, GridPosition

pygame.init()
screen = pygame.display.set_mode((800, 600))
grid = GridRenderer(max_z_levels=4)

# Define objects at different z-levels
ship_positions = [
    GridPosition(5, 5, 0),   # Ship at z=0
    GridPosition(8, 8, 1),   # Ship at z=1
    GridPosition(3, 7, 2),   # Ship at z=2
]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill((0, 0, 0))
    
    # Render only specific z-levels
    grid.render_grid(screen, visible_z_levels=[0, 1, 2])
    
    # Highlight ship positions
    for pos in ship_positions:
        grid.render_cell_highlight(screen, pos, (0, 255, 0))
    
    pygame.display.flip()

pygame.quit()
```

### Camera Panning

```python
import pygame
from star_trek_retro_remake.src.engine.isometric_grid import GridRenderer, GridPosition

pygame.init()
screen = pygame.display.set_mode((800, 600))
grid = GridRenderer()

camera_x, camera_y = 400, 100
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Handle arrow keys for camera movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        camera_x -= 5
    if keys[pygame.K_RIGHT]:
        camera_x += 5
    if keys[pygame.K_UP]:
        camera_y -= 5
    if keys[pygame.K_DOWN]:
        camera_y += 5
    
    # Update camera position
    grid.set_camera_offset((camera_x, camera_y))
    
    screen.fill((0, 0, 0))
    grid.render_grid(screen)
    pygame.display.flip()

pygame.quit()
```

## Mathematical Details

### Isometric Projection

The isometric projection uses a 2:1 ratio (width:height) to create the illusion of 3D:

**Forward Transformation (World → Screen):**
```
screen_x = (world_x - world_y) × (tile_width ÷ 2) + camera_x
screen_y = (world_x + world_y) × (tile_height ÷ 2) - (world_z × z_offset) + camera_y
```

**Inverse Transformation (Screen → World):**
```
adjusted_y = screen_y + (world_z × z_offset) - camera_y
adjusted_x = screen_x - camera_x

world_x = (adjusted_x ÷ (tile_width ÷ 2) + adjusted_y ÷ (tile_height ÷ 2)) ÷ 2
world_y = (adjusted_y ÷ (tile_height ÷ 2) - adjusted_x ÷ (tile_width ÷ 2)) ÷ 2
```

### Z-Level Visualization

Each z-level is offset vertically by `z_level_offset` pixels:
- Higher z values appear higher on screen (closer to top)
- Lower z values appear lower on screen (closer to bottom)
- Default offset is 24 pixels per level

### Grid Cell Diamond Shape

Each isometric cell forms a diamond (rhombus) with corners at:
- **Top**: (center_x, center_y - tile_height/2)
- **Right**: (center_x + tile_width/2, center_y)
- **Bottom**: (center_x, center_y + tile_height/2)
- **Left**: (center_x - tile_width/2, center_y)

## Performance Considerations

### Rendering Optimization

- **Culling**: Only visible cells should be rendered (not yet implemented)
- **Layer Rendering**: Render z-levels from bottom to top for proper depth
- **Dirty Rectangles**: Only redraw changed portions (future enhancement)

### Memory Efficiency

- **Immutable Positions**: GridPosition uses frozen dataclass for hashability
- **Color Constants**: Reusable color tuples defined as class constants
- **No State Caching**: Pure functional rendering methods

## Integration Points

### With Game Model

```python
from star_trek_retro_remake.src.game.model import GameModel
from star_trek_retro_remake.src.engine.isometric_grid import GridRenderer

model = GameModel()
renderer = create_sector_grid()

# Render game objects on grid
for obj in model.game_objects:
    screen_pos = renderer.world_to_screen(obj.position)
    # Draw object sprite at screen_pos
```

### With Game Controller

```python
from star_trek_retro_remake.src.game.controller import GameController
from star_trek_retro_remake.src.engine.isometric_grid import GridRenderer

controller = GameController()
renderer = GridRenderer()

# Handle mouse click
def on_mouse_click(mouse_pos):
    grid_pos = renderer.screen_to_world(mouse_pos, z_level=current_z)
    if renderer.is_in_bounds(grid_pos):
        controller.handle_ship_move_request(grid_pos)
```

### With Game View

```python
from star_trek_retro_remake.src.game.view import GameView
from star_trek_retro_remake.src.engine.isometric_grid import GridRenderer

class GameView:
    def __init__(self, controller):
        self.controller = controller
        self.grid_renderer = create_sector_grid()
        
    def render_sector_map(self, sector, game_objects):
        self.grid_renderer.render_grid(self.game_surface)
        for obj in game_objects:
            self.render_game_object(obj)
```

## Testing Considerations

### Unit Tests

Key test cases for `test_isometric_grid.py`:

1. **Coordinate Conversion**
   - World to screen conversion accuracy
   - Screen to world conversion accuracy
   - Round-trip conversion (world → screen → world)

2. **Bounds Checking**
   - Valid positions within bounds
   - Invalid positions outside bounds
   - Edge cases (boundaries)

3. **Z-Level Calculations**
   - Correct vertical offset per z-level
   - Z-level visibility ordering

4. **Camera Operations**
   - Camera offset application
   - Coordinate transformation with camera

5. **GridPosition Operations**
   - Distance calculations
   - Addition and subtraction

### Integration Tests

1. **Rendering Tests**
   - Grid renders without errors
   - Cell highlighting works correctly
   - Multiple z-levels render properly

2. **Interactive Tests**
   - Mouse clicks convert to correct grid cells
   - Camera panning updates display correctly

## Known Limitations

1. **No Culling**: Currently renders all grid lines (performance impact on large grids)
2. **No Zoom**: Camera offset only, no zoom in/out
3. **Fixed Tile Ratio**: 2:1 width:height ratio is hardcoded
4. **No Rotation**: Grid orientation is fixed

## Future Enhancements

1. **Frustum Culling**: Only render visible portion of grid
2. **Zoom Support**: Scale tiles dynamically
3. **Smooth Camera**: Animated camera transitions
4. **Grid Themes**: Multiple visual styles
5. **Hexagonal Grid**: Alternative to isometric diamonds
6. **Minimap**: Small overview of entire grid

## Version History

- **0.0.1** (10-30-2025): Initial implementation
  - Basic isometric projection
  - Z-level support
  - Cell highlighting
  - Factory functions for common configurations

## See Also

- `/docs/ARCHITECTURE.md` - Overall game architecture
- `/docs/DESIGN.md` - Game design document
- `STRR/src/game/view.py` - Game view integration
- `STRR/src/game/model.py` - Game model with GridPosition usage
