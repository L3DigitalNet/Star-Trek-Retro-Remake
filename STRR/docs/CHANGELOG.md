# Changelog

All notable changes to the Star Trek Retro Remake project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Qt Designer integration for UI design workflow
- `.ui` file loading with QUiLoader for runtime UI loading
- UI compilation script (`scripts/compile_ui.py`) for optional Python compilation
- Comprehensive Qt Designer workflow documentation (`docs/QT_DESIGNER_WORKFLOW.md`)
- Base `main_window.ui` file matching current functionality
- UI directory structure (`STRR/src/ui/designer/`, `STRR/src/ui/compiled/`)

### Changed

- Refactored `GameView` to load UI from Qt Designer `.ui` files instead of programmatic creation
- Updated `view_doc.md` with Qt Designer integration details
- Added Qt Designer reference to main README.md documentation

### Added (Planned Features)

- Advanced AI behavior system for enemy ships
- Mission generation and dynamic storytelling system
- Audio and visual effects framework
- Comprehensive save/load functionality
- Entity sprite system for visual ship representation
- Movement animation and pathfinding visualization
- Mouse wheel zoom support
- Minimap for navigation
- Configurable z-level visibility range
- Settings dialog window
- Save/Load game dialogs
- Menu bar integration

### Changed

- TBD

### Fixed

- TBD

### Removed

- TBD

## [0.0.10] - 2025-10-30

### Added

- **Enhanced PySide6 UI Layout**: Complete Qt window integration with control panel
  - Left control panel with game controls and status displays
  - Ship status display showing hull, shields, and energy
  - Z-level indicator with automatic updates
  - Message display area for game feedback
  - Game control buttons (New Game, Save, Load, Settings, Quit)
  - Proper horizontal layout separating UI controls from game display
  - Centered game display area with title and instructions

- **Standalone Integration Demo** (`demo_qt_pygame_integration.py`)
  - Complete working example of PySide6 + pygame-ce integration
  - Control panel with buttons and status displays
  - Animated bouncing circle (USS Enterprise simulation)
  - 60 FPS rendering with proper timing
  - Clean resource management and shutdown handling
  - Fully documented for learning and reference

- **Comprehensive Documentation**
  - `PYSIDE6_PYGAME_INTEGRATION.md`: Technical integration guide
  - `demo_qt_pygame_integration_doc.md`: Demo file documentation
  - `QT_PYGAME_INTEGRATION_README.md`: Quick start guide
  - Detailed architecture diagrams and code examples
  - Best practices and troubleshooting guide

### Changed

- **View Architecture** (`view.py`)
  - Refactored from simple vertical layout to horizontal split layout
  - Game display now 1280x900 (from 1920x1080) to accommodate control panel
  - Main window size adjusted to 1920x1080 for better screen utilization
  - `show_message()` now updates UI message display in real-time
  - `set_z_level()` now updates UI label automatically
  - `show_ship_status()` now updates UI status panel with ship details

- **Image Conversion API** (Performance & Compatibility)
  - Updated from deprecated `pygame.image.tostring()` to `pygame.image.tobytes()`
  - Applied to both `view.py` and `demo_qt_pygame_integration.py`
  - Eliminates deprecation warnings
  - Future-proof API usage for pygame-ce 2.3.0+

### Technical Implementation

- **Layout Structure**:
  - `QHBoxLayout` for main window (control panel | game area)
  - Control panel: `QGroupBox` with `QVBoxLayout` for vertical stacking
  - Game area: `QWidget` with `QVBoxLayout` for title/display/instructions

- **Qt Signal/Slot Pattern**:
  - Button clicks connected to handler methods
  - Clean separation between UI events and game logic
  - Proper method naming convention (`_on_action`)

- **Resource Management**:
  - Pre-allocated buffers for image conversion
  - Cached fonts to prevent per-frame allocation
  - Proper cleanup in `closeEvent()`
  - Timer management for clean shutdown

- **Coordinate Handling**:
  - Mouse events from Qt widgets
  - Coordinate conversion (Qt → pygame)
  - Bounds validation before forwarding to controller

### Files Added

- `STRR/demo_qt_pygame_integration.py` - Standalone demo
- `STRR/demo_qt_pygame_integration_doc.md` - Demo documentation
- `STRR/src/game/PYSIDE6_PYGAME_INTEGRATION.md` - Technical docs
- `QT_PYGAME_INTEGRATION_README.md` - Quick start guide

### Files Modified

- `STRR/src/game/view.py` - Enhanced UI layout
- `STRR/docs/CHANGELOG.md` - This file
- Date Changed fields updated in modified files

### Integration Benefits

- **Developer Experience**: Clear separation between Qt UI and pygame rendering
- **User Experience**: Professional windowed interface with proper controls
- **Maintainability**: Well-documented pattern for future UI additions
- **Performance**: 60 FPS maintained with efficient rendering pipeline
- **Flexibility**: Easy to add more Qt widgets (dialogs, menus, settings)

## [0.0.9] - 2025-10-30

### Fixed

- **CRITICAL: Race Condition in Sector Loading** (`model.py`)
  - Added validation after `get_sector()` to ensure sector exists before creating player ship
  - Added validation that `place_entity()` succeeds when placing player ship
  - Prevents game initialization with `None` sector or failed entity placement
  - Raises `RuntimeError` with descriptive message if initialization fails

- **CRITICAL: Entity Position Desynchronization** (`model.py`)
  - Ship position now updated BEFORE calling `move_entity()` instead of after
  - Ensures `ship.position` and `sector.entities` dictionary stay synchronized
  - Added rollback mechanism: if sector move fails, ship position reverts to old position
  - Prevents entity duplication or orphaned references in sector map

- **HIGH: Missing Bounds Validation in Mouse Clicks** (`controller.py`)
  - Added dual validation for grid positions from screen-to-world conversion
  - First validates against renderer bounds (visual grid)
  - Then validates against sector map bounds (logical grid)
  - Prevents invalid positions from being selected or moved to
  - Added descriptive logging for both validation failures

- **HIGH: Division by Zero Risk in Zoom** (`isometric_grid.py`)
  - Enforced minimum tile dimensions of 4 pixels in `set_zoom()`
  - Prevents division by zero in coordinate conversion formulas
  - Minimum z-level offset of 2 pixels also enforced
  - Ensures safe math operations at extreme zoom levels (down to 25%)

- **MEDIUM: Grid Size Mismatch** (`isometric_grid.py`)
  - Fixed `create_sector_grid()` to use 20×20 grid matching `SectorMap.grid_size`
  - Previously used 30×30 causing wasted rendering and confusion
  - Updated camera offset calculation for correct grid centering
  - All dimensions now consistent between sector map and renderer

- **MEDIUM: Move Execution Optimization** (`model.py`)
  - Engine system existence check moved before distance calculation
  - Prevents expensive distance calculation when engine is missing
  - More efficient early-exit pattern for invalid moves

### Changed

- Updated `test_isometric_grid.py` to reflect corrected 20×20 sector grid dimensions
- Enhanced error messages with descriptive `RuntimeError` exceptions
- Improved logging detail in controller for coordinate validation
- Updated "Date Changed" fields in affected modules (model.py, controller.py, isometric_grid.py)

### Technical Details

- All 75 unit tests passing after fixes
- No breaking changes to public APIs
- Improved robustness for edge cases and error conditions
- Better separation of concerns between renderer and sector map bounds

## [0.0.8] - 2025-10-30

### Changed

- **Simplified Grid Color Scheme**: Monochrome design for maximum clarity
  - Current z-level: Pure white (255, 255, 255) with full opacity (alpha=255)
  - Adjacent z-levels: Gray (128, 128, 128) with low transparency (alpha=80)
  - Removed color-coding per z-level for cleaner, less distracting display
  - Creates stark contrast between active and context layers
  - Easier to focus on current gameplay plane

### Removed

- Z-level color differentiation (blue, cyan, purple, amber, red scheme)
- Color-based z-level identification - replaced with opacity/dash patterns

### Technical Implementation

- Modified `GridRenderer.render_z_level()` to use white/gray colors based on current z-level
- Updated transparency values: current=255 (full opacity), adjacent=80 (very transparent)
- Simplified color logic: no more color index calculations or z-level color arrays
- Dashed line patterns still differentiate between current (solid) and adjacent (dashed)

## [0.0.7] - 2025-10-30

### Changed

- **Limited Z-Level Visibility**: Only show current level ± 1 for reduced clutter
  - Renders current z-level + one above + one below only
  - Dramatically reduces visual noise (from 5 layers to maximum 3)
  - Simplified transparency: current=220, below=100, above=140
  - Easier to focus on immediate gameplay area
  - Temporary change for testing purposes; will be configurable later

### Technical Implementation

- Modified `GameView.render_sector_map()` to calculate visible z-range:
  - `min_z = max(0, current_z_level - 1)`
  - `max_z = min(max_z_levels - 1, current_z_level + 1)`
- Loop only iterates through visible range instead of all z-levels
- Simplified alpha values since only 3 levels maximum are ever visible
- Maintains dashed line system for adjacent levels

## [0.0.6] - 2025-10-30

### Added

- **Dashed Grid Lines for Inactive Z-Levels**: Significantly reduces visual clutter
  - Current z-level: Solid lines (no dashing)
  - Distance 1: Light dashing (16px dash, 4px gap)
  - Distance 2: Medium dashing (12px dash, 8px gap)
  - Distance 3+: Heavy dashing (8px dash, 16px gap - very sparse)
  - Progressively sparser dashing makes distant layers less distracting
  - Combined with color differentiation and transparency for optimal depth perception

### Changed

- **Grid Rendering Algorithm**: Enhanced to support variable dash patterns
  - `render_z_level()` now accepts `current_z_level` parameter for dash calculation
  - `_draw_grid_lines()` calculates dash parameters based on distance from active plane
  - New `_draw_dashed_line()` helper function for efficient dash rendering
  - Dashed lines use normalized vector math for precise dash placement

### Technical Implementation

- Added `_draw_dashed_line()` method to `GridRenderer`:
  - Calculates line vector and distance
  - Normalizes direction for consistent dash spacing
  - Iterates through pattern (dash + gap) to draw segments
  - Handles partial dashes at line endpoints

- Updated `render_z_level()` signature to accept optional `current_z_level` parameter
- Updated `_draw_grid_lines()` to calculate and apply dash patterns based on z-level distance
- Modified `GameView.render_sector_map()` to pass current z-level for dash calculation

### Visual Impact

The combination of three visual techniques now creates excellent depth perception:

1. **Distinct hue per z-level** (color coding)
2. **Distance-based transparency** (alpha fading)
3. **Progressive dash density** (NEW - reduces visual noise)

Result: Far z-levels appear as subtle, sparse dashed hints while the current level remains clear and prominent.

## [0.0.5] - 2025-10-30

### Added

- **Zoom Functionality**: Dynamic zoom in/out capability with keyboard controls
  - Zoom range: 25% to 400% (0.25x to 4.0x)
  - Keyboard shortcuts: `+`/`=` to zoom in, `-` to zoom out, `0` to reset
  - Smooth zoom transitions with 20% increment per step
  - Tile dimensions scale proportionally with zoom level
  - Z-level offset scales with zoom for consistent depth perception
  - Zoom level logged for debugging

- **1920x1080 Display Resolution**: Updated window and surface sizes for modern displays
  - Main window: 1920x1080 pixels
  - Game surface: 1920x1080 pixels
  - Widget minimum size: 1920x1080 pixels
  - Provides larger viewport for better grid visualization

### Changed

- **Enhanced Z-Level Color Differentiation**: Improved visual distinction between layers
  - New color scheme with distinct hues per z-level:
    - Z=0: Dark blue (60, 60, 140) - Deep space
    - Z=1: Cyan-green (80, 140, 120) - Low orbit
    - Z=2: Purple (140, 100, 140) - Mid orbit
    - Z=3: Amber (140, 120, 60) - High orbit
    - Z=4: Reddish (140, 80, 80) - Upper atmosphere
  - Improved transparency algorithm:
    - Current level: 220 alpha (mostly opaque)
    - Levels below: Fade darker (180 - distance*70, min 30)
    - Levels above: Fade lighter (200 - distance*50, min 50)
  - Creates better depth perception with asymmetric fading

### Technical Implementation

- `GridRenderer` class:
  - Added `zoom_level`, `min_zoom`, `max_zoom` attributes
  - Added `base_tile_width`, `base_tile_height` for zoom calculations
  - Implemented `set_zoom()`, `zoom_in()`, `zoom_out()`, `reset_zoom()` methods
  - Tile dimensions now mutable to support dynamic scaling
  - Z-level offset scales proportionally with zoom

- `GameView` class:
  - Updated window geometry to 1920x1080
  - Updated game surface to 1920x1080
  - Enhanced z-level rendering with asymmetric transparency
  - Added keyboard mappings for zoom controls

- `GameController` class:
  - Added zoom key handlers (K_PLUS, K_EQUALS, K_MINUS, K_0)
  - Integrated zoom calls to GridRenderer methods
  - Logging for zoom operations

## [0.0.4] - 2025-10-30

### Fixed

- **Z-Level Rendering**: All z-levels now render simultaneously with transparency-based depth visualization
  - Current z-level renders fully opaque (alpha=255)
  - Other z-levels fade based on distance from current level (alpha=255 - distance*60, minimum 40)
  - Creates true 3D visualization showing multiple layers of the grid simultaneously
  - Bottom-to-top rendering order ensures proper depth layering
  - Each z-level renders to a separate surface with SRCALPHA for transparency support

- **Mouse Click Coordinate Conversion**: Fixed mouse input mapping from Qt widget to pygame surface
  - Accounts for QLabel widget offset within the window
  - Properly converts widget-relative coordinates to pygame surface coordinates
  - Calculates pixmap display offset (centered in widget)
  - Clamps coordinates to valid pygame surface bounds
  - Added detailed logging for debugging coordinate transformations

### Technical Details

- Modified `GameView.render_sector_map()` to iterate through all z-levels instead of just current level
- Each z-level renders to temporary surface with alpha transparency before compositing to main surface
- Updated `GameDisplay.mousePressEvent()` to calculate widget-to-surface coordinate transformation
- Mouse coordinates now accurately map to grid cells under cursor
- Z-level switching (PageUp/PageDown) maintains proper transparency for all visible layers

## [0.0.3] - 2025-10-30

### Integration

- **Isometric Grid System Fully Integrated into MVC Architecture**
  - GridRenderer now embedded in GameView for rendering
  - GameController handles mouse and keyboard input for grid interaction
  - Unified GridPosition class (no more duplication)
  - Complete click-to-select and click-to-move functionality
  - Z-level switching via Page Up/Down keys
  - Camera panning via arrow keys
  - Visual feedback for selected cells (green highlight)
  - Entity rendering at correct grid positions with name labels

### Added

- **Isometric Grid Rendering System** (`isometric_grid.py`)
  - GridRenderer class with full 3D coordinate support (x, y, z)
  - Isometric projection mathematics (world ↔ screen coordinate conversion)
  - Z-level support for vertical space positioning (up to configurable max levels)
  - Grid line rendering with configurable tile sizes and colors
  - Cell highlighting and selection functionality
  - Camera offset and viewport management
  - Grid bounds checking and validation
  - Factory functions for common grid configurations (default, combat, sector)

- **Comprehensive Documentation** (`isometric_grid_doc.md`)
  - Complete API reference with all classes, methods, and attributes
  - Mathematical details of isometric projection formulas
  - Usage examples for common scenarios
  - Integration guides for MVC architecture
  - Performance considerations and optimization notes

- **Full Test Suite** (`test_isometric_grid.py`)
  - 41 unit tests covering all functionality
  - Tests for GridPosition operations (distance, addition, subtraction)
  - Tests for coordinate conversion (world ↔ screen, round-trip validation)
  - Tests for bounds checking and edge cases
  - Tests for camera operations and z-level calculations
  - Tests for rendering operations and factory functions
  - All tests passing with 100% success rate

- **Interactive Demo** (`demo_isometric_grid.py`)
  - Full-featured interactive demonstration application
  - Mouse click cell selection with visual feedback
  - Keyboard controls for z-level switching and camera panning
  - Multiple grid preset modes (default, combat, sector)
  - Real-time information panel showing grid state
  - Help overlay with complete control reference
  - Clean, documented code suitable as example implementation

### Technical Implementation

- **GridPosition dataclass**: Immutable 3D coordinate representation with mathematical operations
- **GridRenderer class**: Core rendering engine with isometric projection
- **Projection formulas**:
  - World to screen: `screen_x = (x - y) * (tile_width/2) + camera_x`
  - World to screen: `screen_y = (x + y) * (tile_height/2) - (z * z_offset) + camera_y`
- **Z-level visualization**: Vertical offset per level with configurable pixel spacing
- **Color scheme**: Different colors for each z-level to enhance depth perception
- **Factory pattern**: Convenience functions for common grid configurations

### Integration Points

- Compatible with existing MVC architecture in `model.py`, `view.py`, `controller.py`
- Uses GridPosition dataclass compatible with game entity system
- Designed for integration with pygame-ce rendering in GameView
- Ready for controller integration for mouse-to-world coordinate conversion

### Testing Coverage

- **GridPosition**: 10 tests covering creation, distance, operators, immutability
- **Initialization**: 3 tests for renderer setup and configuration
- **Coordinate Conversion**: 8 tests for projection math and round-trip accuracy
- **Bounds Checking**: 6 tests for validation logic
- **Camera Operations**: 2 tests for viewport management
- **Rendering**: 7 tests for grid drawing and highlighting
- **Factory Functions**: 3 tests for preset configurations
- **Edge Cases**: 3 tests for extreme values and special scenarios

### Performance Characteristics

- Efficient isometric projection using integer math where possible
- Minimal memory allocation (no caching, pure functional rendering)
- Suitable for grids up to 30x30 with 5 z-levels at 60 FPS
- Object pooling pattern compatible for future optimization

## [0.0.2] - 2025-10-30

### Added

- TOML configuration system for improved readability and maintainability
- Configuration manager utility with JSON fallback support during migration
- JSON to TOML migration script for future configuration file conversions
- Comprehensive TOML examples with comments and proper organization

### Changed

- **BREAKING**: Migrated all configuration files from JSON to TOML format
  - `game_settings.json` → `game_settings.toml` with improved structure and comments
  - `game_data.json` → `game_data.toml` with cleaner ship class definitions
  - `key_bindings.json` → `key_bindings.toml` with better organization
  - `sol_system.json` → `sol_system.toml` using array of tables for objects
- Updated documentation to reflect TOML usage (ARCHITECTURE.md, DESIGN.md, PROJECT-DOC.md)
- Enhanced configuration system with dot notation access and type safety
- Updated version numbers across project files (pyproject.toml, main.py)
- Corrected documentation path references from `/GDD/DESIGN.md` to `/docs/DESIGN.md`
- Updated all file header "Date Changed" fields to reflect documentation updates

### Fixed

- Documentation path inconsistencies between README.md and copilot instructions
- Version number mismatch between CHANGELOG.md (0.0.2) and project files (0.0.1)

## [0.0.1] - 2024-12-15

### Added

- Initial project structure and development framework
- Core MVC architecture implementation with hybrid State Machine + Game Object + Component pattern
- Game entity system with GameObject base class and Starship implementation
- Component system for ship subsystems (weapons, shields, engines, sensors, life support)
- State machine for game mode transitions (Galaxy Map ↔ Sector Map ↔ Combat Mode)
- Grid-based positioning system with 3D coordinate support (GridPosition with x, y, z levels)
- Turn-based game model with TurnManager and combat resolution system
- Resource management system for ship energy, fuel, crew morale, and supplies
- Comprehensive configuration system with JSON files for game settings, key bindings, and ship classes (later migrated to TOML in v0.0.2)
- Asset management structure with organized directories for graphics, audio, and data
- Comprehensive pytest testing framework with fixtures and AAA pattern testing
- Object pooling foundation for efficient memory management
- Complete project documentation including README.md, PROJECT-DOC.md, and architecture guides
- Development guidelines with Python 3.14+ standards and type hints
- Git workflow and version management system

### Technical Implementation

- **Architecture**: Hybrid State Machine + Game Object + Component + MVC pattern
- **Game Loop**: Fixed timestep implementation ready for pygame-ce integration
- **Entity System**: GameObject base with Starship and SpaceStation implementations
- **Component Pattern**: Modular ship systems with damage/repair mechanics
- **State Management**: GameStateManager with mode transition validation
- **Configuration**: JSON-based settings for display, audio, gameplay, and controls
- **Testing**: pytest framework with comprehensive test coverage for core logic
- **Documentation**: Complete technical documentation and development guidelines

### Project Structure

- `/main.py`: Game entry point and application launcher
- `/src/game/`: Core MVC architecture (application.py, model.py, view.py, controller.py)
- `/src/entities/`: Game objects (base.py, starship.py with component composition)
- `/src/components/`: Ship systems (ship_systems.py with modular subsystems)
- `/src/states/`: State machine implementation (state_machine.py with GameState management)
- `/src/maps/`: Galaxy, sector, and combat map systems (galaxy.py, sector.py)
- `/config/`: JSON configuration files for all game settings and data
- `/assets/`: Organized asset directories for graphics, audio, and data files
- `/tests/`: Comprehensive pytest test suite with fixtures and mock objects
- `/docs/`: Project documentation including architecture and development guides

### Configuration Files

- `game_settings.json`: Display, audio, and gameplay configuration
- `key_bindings.json`: Keyboard shortcuts and control mappings
- `ship_classes.json`: Starship specifications and capabilities
- `factions.json`: Faction relationships and characteristics
- `missions.json`: Mission templates and objectives

### Testing Coverage

- Unit tests for all entity classes and game logic
- Integration tests for state transitions and system interactions
- Fixtures for common test objects (ships, positions, game states)
- Mock objects for UI and external dependencies
- AAA pattern testing for clear test structure and maintainability

### Development Standards

- Python 3.14+ with modern syntax (union types, match statements, Path.copy())
- Comprehensive type hints for all functions, variables, and data structures
- PEP 8 compliance with f-string formatting exclusively
- Detailed docstrings with function parameters and return values
- Clean architecture with separation of concerns and testable design
- Standard library first approach with justified external dependencies

### Known Limitations

- UI integration pending (PySide6/pygame-ce coordination not yet implemented)
- Combat AI behavior requires implementation
- Save/load functionality needs development
- Asset loading and caching system pending
- Audio system not yet implemented

### Next Development Phase (v0.1.0)

- PySide6 main window implementation with embedded pygame-ce widget
- Basic ship movement and exploration mechanics
- Simple combat system with AI opponents
- Resource management UI and feedback systems
- Galaxy and sector map generation algorithms
