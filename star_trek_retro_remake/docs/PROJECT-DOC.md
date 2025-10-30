# -*- coding: utf-8 -*-

"""
Star Trek Retro Remake - Project Documentation

Description:
    Comprehensive project documentation covering architecture, implementation,
    development guidelines, and technical specifications for the Star Trek
    Retro Remake game project.

Author: Star Trek Retro Remake Development Team
Email: <development@star-trek-retro-remake.dev>
GitHub: <https://github.com/YourUsername/Star-Trek-Retro-Remake>
Date Created: 12-15-2024
Date Changed: 12-15-2024
License: MIT License

Features:
    - Hybrid State Machine + Game Object + Component + MVC architecture
    - Turn-based tactical combat with detailed ship systems
    - 3D grid-based exploration with multiple z-levels
    - PyGame game engine with PySide6 UI framework
    - Comprehensive testing framework with pytest
    - Object pooling and memory management for performance
    - Clean separation of game logic from UI for testability
    - Modular design supporting future expansion

Requirements:
    - Linux environment (primary target platform)
    - Python 3.14+ for latest language features and syntax
    - PyGame 2.5+ for game engine functionality
    - PySide6 6.7+ for UI, menus, and dialogs
    - pytest 8.0+ for comprehensive testing framework

Project Structure:
    - /main.py: Game entry point and application launcher
    - /src/game/: Core MVC architecture and game loop
    - /src/entities/: Game objects (starships, stations, crew)
    - /src/components/: Ship systems and modular components
    - /src/states/: State machine implementation
    - /src/maps/: Galaxy, sector, and combat map systems
    - /config/: TOML configuration files (settings, bindings, data)
    - /assets/: Graphics, audio, and data files
    - /tests/: Comprehensive pytest test suite
    - /docs/: Project documentation and guides

Known Issues:
    - PySide6/PyGame integration pending implementation
    - Combat system requires AI behavior implementation
    - Asset loading system needs optimization
    - Save/load functionality not yet implemented

Planned Features:
    - Complete PySide6 UI implementation with embedded PyGame
    - Advanced AI for enemy ships and factions
    - Mission generation and dynamic storytelling
    - Comprehensive audio and visual effects
    - Multiplayer support (future expansion)
    - Mod support and community content tools

Classes:
    - GameApplication: Main application controller and coordinator
    - GameModel: Pure game logic and state management
    - GameView: PySide6 UI and PyGame rendering
    - GameController: Input handling and state transitions
    - GameStateManager: State machine coordination
    - GameObject: Base class for all game entities
    - Starship: Star Trek starship with component systems
    - ShipSystem: Base class for ship subsystems

Functions:
    - main(): Application entry point and initialization
    - initialize_game(): Set up new game state and resources
    - run_game_loop(): Core game loop execution
    - handle_events(): Process input and system events
    - update_game_state(): Update game logic and objects
    - render_game(): Draw current game state to screen
"""

# Star Trek Retro Remake - Project Documentation

## Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture Documentation](#architecture-documentation)
3. [Development Guidelines](#development-guidelines)
4. [Implementation Details](#implementation-details)
5. [Testing Strategy](#testing-strategy)
6. [Performance Optimization](#performance-optimization)
7. [Configuration System](#configuration-system)
8. [Asset Management](#asset-management)
9. [Development Workflow](#development-workflow)
10. [Troubleshooting Guide](#troubleshooting-guide)

## Project Overview

### Vision Statement

Star Trek Retro Remake is a turn-based, grid-based strategy game that captures the essence of classic Star Trek gaming experiences while leveraging modern development practices and architecture patterns. The project aims to provide an authentic Star Trek command experience through tactical combat, exploration, and resource management.

### Core Design Principles

1. **Clean Architecture**: Hybrid State Machine + Game Object + Component + MVC pattern
2. **Testable Design**: Pure game logic separated from UI dependencies
3. **Modern Python**: Python 3.14+ features with comprehensive type hints
4. **Performance Focus**: Object pooling and efficient memory management
5. **Maintainable Code**: Clear separation of concerns and modular design
6. **Standard Library First**: Minimize external dependencies where possible

### Project Scope

#### Included in v1.0.0

- Turn-based tactical combat system
- 3D grid-based exploration (Galaxy/Sector/Combat maps)
- Resource management and ship customization
- Basic AI for enemy ships and NPCs
- Save/load functionality
- Mission system and objectives
- PySide6 UI with embedded PyGame rendering

#### Future Expansions (v1.1+)

- Advanced diplomacy system
- Fleet management capabilities
- Multiplayer support
- Mod support and community tools
- Advanced AI behaviors
- Real-time simulation mode

## Architecture Documentation

### Hybrid Architecture Pattern

The project uses a carefully designed hybrid approach combining:

#### State Machine Pattern

```python
class GameStateManager:
    """Manages transitions between major game modes."""

    def __init__(self):
        self.current_state: Optional[GameState] = None
        self.states: dict[GameMode, GameState] = {}

    def transition_to(self, mode: GameMode) -> None:
        """Transition to new game mode with validation."""
        if self.current_state:
            self.current_state.exit()
        self.current_state = self.states[mode]
        self.current_state.enter()
```

#### Game Object Pattern with Component Composition

```python
class Starship(GameObject):
    """Star Trek starship with modular systems."""

    def __init__(self, position: GridPosition, ship_class: str):
        super().__init__(position)
        self.systems: dict[str, ShipSystem] = {
            'weapons': WeaponSystems(),
            'shields': ShieldSystems(),
            'engines': EngineSystems(),
            'sensors': SensorSystems(),
            'life_support': LifeSupportSystems()
        }
```

#### Model-View-Controller Separation

```python
class GameModel:
    """Pure game logic (no UI dependencies)."""
    def execute_move(self, ship: Starship, destination: GridPosition) -> bool:
        # Pure business logic for ship movement

class GameView:
    """PySide6 UI and PyGame rendering (no game logic)."""
    def render_sector_map(self, sector: SectorMap) -> None:
        # UI rendering without game state modification

class GameController:
    """Coordinates Model and View."""
    def handle_ship_move_request(self, destination: GridPosition) -> None:
        success = self.model.execute_move(self.model.player_ship, destination)
        if success:
            self.view.render_sector_map(self.model.current_sector)
```

### State Management

#### Game Modes

1. **Main Menu**: Game startup, settings, load/save
2. **Galaxy Map**: Strategic navigation between sectors
3. **Sector Map**: Tactical exploration and encounters
4. **Combat Mode**: Turn-based tactical combat
5. **Mission Briefing**: Objective presentation and planning
6. **Settings**: Configuration and preferences

#### State Transitions

```
Main Menu ↔ Galaxy Map ↔ Sector Map ↔ Combat Mode
    ↑           ↑            ↑           ↑
    └───────────┴────────────┴───────────┴─→ Settings
```

#### State Persistence

- Game state can be saved/loaded from any state
- Configuration persists across sessions
- Window state and preferences maintained

### Component System

#### Ship Systems Architecture

```python
class ShipSystem(ABC):
    """Base class for all ship subsystems."""

    @abstractmethod
    def update(self, dt: float) -> None:
        """Update system state each turn."""

    def repair(self, amount: float) -> None:
        """Repair system damage."""

    def damage(self, amount: float) -> None:
        """Apply damage to system."""
```

#### System Interactions

- **Power Management**: Systems compete for available power
- **Damage Cascading**: Critical system failures affect other systems
- **Crew Efficiency**: Crew skills impact system performance
- **Resource Dependencies**: Systems require specific resources

### Memory Management

#### Object Pooling Strategy

```python
class EntityPool:
    """Manages reusable game objects for performance."""

    def __init__(self, entity_type: type, initial_size: int = 50):
        self.pool = [entity_type() for _ in range(initial_size)]
        self.active_entities = set()

    def acquire(self) -> GameObject:
        """Get entity from pool or create new one."""

    def release(self, entity: GameObject) -> None:
        """Return entity to pool for reuse."""
```

#### Resource Management

- **Lazy Loading**: Load assets only when needed
- **Cache Management**: Intelligent caching with memory limits
- **Reference Tracking**: Avoid circular references and memory leaks
- **Garbage Collection**: Explicit cleanup for large objects

## Development Guidelines

### Python Standards

#### Code Style

- **PEP 8 Compliance**: Strict adherence to Python style guidelines
- **Type Hints**: Comprehensive typing for all functions and variables
- **Modern Syntax**: Python 3.14+ features (Path.copy(), match statements, etc.)
- **F-strings Only**: No .format() or % string formatting

#### Function Design

```python
def calculate_weapon_damage(
    attacker: Starship,
    target: Starship,
    weapon_type: str,
    environmental_factors: dict[str, float]
) -> CombatResult:
    """
    Calculate weapon damage with comprehensive factors.

    Args:
        attacker: Ship firing the weapon
        target: Ship receiving damage
        weapon_type: Type of weapon ('phaser', 'torpedo', etc.)
        environmental_factors: Environmental modifiers

    Returns:
        CombatResult with damage amount and success status
    """
    # Implementation with max 3 nesting levels
```

#### Documentation Standards

- **Module Headers**: Comprehensive file documentation
- **Class Documentation**: Purpose, attributes, methods
- **Function Documentation**: Parameters, returns, examples
- **Inline Comments**: Explain complex logic and design decisions

### File Organization

#### Module Structure

```python
# -*- coding: utf-8 -*-
"""
Star Trek Retro Remake - [Module Name]

Description:
    Detailed description of module purpose and functionality.

[Standard header with author, dates, features, requirements, etc.]
"""

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # Forward references for type hints only

# Standard library imports
import json
from pathlib import Path
from dataclasses import dataclass

# Third-party imports
import pygame
from PySide6.QtWidgets import QWidget

# Local imports
from ..common import GameError
from .base import GameObject
```

#### Directory Standards

```
src/
├── game/           # Core MVC architecture
├── entities/       # Game objects and entities
├── components/     # Ship systems and components
├── states/         # State machine implementation
├── maps/           # Map systems and generation
├── ai/             # AI behavior and decision making
├── utils/          # Utility functions and helpers
└── common/         # Shared types and constants
```

### Version Management

#### Version Format

- **MAJOR.MINOR.PATCH** (e.g., 1.2.3)
- **Pre-release**: 0.x.x for development versions
- **Release**: 1.0.0 for first public release

#### Change Documentation

```markdown
## [1.0.0] - 2024-12-15

### Added
- Complete combat system with tactical grid
- Resource management for ship systems
- Save/load functionality

### Changed
- Improved AI decision making algorithms
- Enhanced UI responsiveness

### Fixed
- Memory leak in object pooling system
- State transition validation issues

### Removed
- Deprecated legacy combat mechanics
```

## Implementation Details

### PyGame Integration

#### Game Loop Structure

```python
class GameApplication:
    """Main application with PyGame/PySide6 integration."""

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.running = True

    def run(self) -> None:
        """Main game loop with fixed timestep."""
        while self.running:
            dt = self.clock.tick(60) / 1000.0  # 60 FPS, convert to seconds

            self.handle_events()
            self.update(dt)
            self.render()
```

#### Rendering Pipeline

1. **Clear Surface**: Reset drawing surface
2. **Render Background**: Draw static elements
3. **Render Objects**: Draw dynamic game objects
4. **Render UI**: Draw interface elements
5. **Update Display**: Present final frame

### PySide6 Integration

#### Main Window Structure

```python
class MainWindow(QMainWindow):
    """Main application window with embedded PyGame."""

    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setup_pygame_widget()

    def setup_pygame_widget(self):
        """Embed PyGame surface in QWidget."""
        self.game_widget = PyGameWidget()
        self.setCentralWidget(self.game_widget)
```

#### Dialog System

- **Modal Dialogs**: Mission briefings, ship status
- **Non-Modal Panels**: Resource monitoring, minimap
- **Context Menus**: Right-click object information
- **Settings Windows**: Configuration and preferences

### Configuration System

#### TOML Configuration Structure

The project uses **TOML** format for all configuration files, providing improved readability and maintainability:

**Game Settings (`config/game_settings.toml`):**

```toml
[display]
window_width = 1024     # Default window width in pixels
window_height = 768     # Default window height in pixels
fullscreen = false      # Start in windowed mode
vsync = true           # Enable vertical sync to prevent screen tearing

[audio]
master_volume = 0.8     # Master audio volume (0.0 - 1.0)
music_volume = 0.6      # Background music volume
sfx_volume = 0.7        # Sound effects volume

[game]
difficulty = "normal"           # Game difficulty: easy, normal, hard, expert
auto_save = true               # Automatically save game progress
turn_timer = 30                # Turn time limit in seconds (0 = unlimited)

[game.grid_size]
galaxy = [10, 10]              # Galaxy map dimensions [width, height]
sector = [20, 20, 5]           # Sector map dimensions [width, height, z-levels]
```

**Key Bindings (`config/key_bindings.toml`):**

```toml
[keyboard.movement]
move_up = "w"              # Move ship/cursor up
move_down = "s"            # Move ship/cursor down
move_left = "a"            # Move ship/cursor left
move_right = "d"           # Move ship/cursor right
move_up_z = "q"            # Move up in z-level (space layer)
move_down_z = "e"          # Move down in z-level (space layer)

[keyboard.combat]
fire_phasers = "space"     # Fire phaser arrays
fire_torpedoes = "t"       # Launch photon torpedoes
shields_toggle = "shift"   # Raise/lower shields
```

**Ship Classes (`config/game_data.toml`):**

```toml
[ship_classes.constitution]
name = "Constitution Class"
hull_integrity = 100
crew_capacity = 430

[ship_classes.constitution.systems.weapons]
phaser_arrays = 4
torpedo_tubes = 2
torpedo_capacity = 12

[ship_classes.constitution.systems.shields]
max_strength = 100
recharge_rate = 5.0
```

#### Configuration Management

```python
from star_trek_retro_remake.src.engine.config_manager import (
    initialize_config_manager, load_config, get_config_value
)

# Initialize configuration system
config_manager = initialize_config_manager("config/")

# Load complete configuration files
settings = load_config("game_settings")
ship_data = load_config("game_data")

# Access specific values with dot notation
window_width = get_config_value("game_settings", "display.window_width", 1024)
phaser_count = get_config_value("game_data", "ship_classes.constitution.systems.weapons.phaser_arrays")

# Save configuration changes
set_config_value("game_settings", "display.fullscreen", True)
```

## Testing Strategy

### Test Architecture

#### Unit Testing with pytest

```python
class TestStarship:
    """Comprehensive starship testing."""

    def test_starship_creation(self, sample_position):
        """Test starship instantiation and initialization."""
        ship = Starship(sample_position, "Constitution", "Enterprise")

        assert ship.position == sample_position
        assert ship.ship_class == "Constitution"
        assert ship.name == "Enterprise"
        assert ship.hull_integrity == 100.0

    def test_weapon_targeting(self, player_ship, enemy_ship):
        """Test weapon targeting and range calculations."""
        weapons = player_ship.get_system('weapons')

        # Test within range
        assert weapons.can_target(enemy_ship.position, player_ship.position, 0)

        # Test out of range
        enemy_ship.position = GridPosition(100, 100, 0)
        assert not weapons.can_target(enemy_ship.position, player_ship.position, 0)
```

#### Integration Testing

```python
def test_combat_integration():
    """Test complete combat sequence."""
    # Arrange
    game_model = GameModel()
    game_model.initialize_new_game()

    attacker = game_model.player_ship
    target = create_enemy_ship()

    # Act
    result = game_model.resolve_combat(attacker, target, "phaser")

    # Assert
    assert result.success
    assert result.damage > 0
    assert target.hull_integrity < 100.0
```

#### Test Fixtures

```python
@pytest.fixture
def sample_position():
    """Standard test position."""
    return GridPosition(5, 5, 1)

@pytest.fixture
def player_ship(sample_position):
    """Configured player starship for testing."""
    ship = Starship(sample_position, "Constitution", "Enterprise")
    # Configure systems for predictable testing
    return ship

@pytest.fixture
def game_model():
    """Initialized game model for testing."""
    model = GameModel()
    model.initialize_new_game()
    return model
```

### Test Coverage Requirements

#### Coverage Targets

- **Core Logic**: 90%+ coverage for game mechanics
- **Entity System**: 85%+ coverage for all entities
- **Component System**: 85%+ coverage for ship systems
- **State Management**: 95%+ coverage for state transitions

#### Coverage Monitoring

```bash
# Generate coverage report
python -m pytest tests/ --cov=src --cov-report=html

# View detailed coverage
open htmlcov/index.html

# Coverage with missing lines
python -m pytest tests/ --cov=src --cov-report=term-missing
```

## Performance Optimization

### Memory Management

#### Object Pooling Implementation

```python
class StarshipPool:
    """Specialized pool for starship objects."""

    def __init__(self, initial_size: int = 20):
        self.available = [Starship(GridPosition(0, 0, 0), "Unknown")
                         for _ in range(initial_size)]
        self.active = set()

    def acquire(self, position: GridPosition, ship_class: str) -> Starship:
        """Get configured starship from pool."""
        if self.available:
            ship = self.available.pop()
            ship.reset(position, ship_class)
        else:
            ship = Starship(position, ship_class)

        self.active.add(ship)
        return ship

    def release(self, ship: Starship) -> None:
        """Return starship to pool."""
        self.active.remove(ship)
        self.available.append(ship)
```

#### Memory Monitoring

```python
class PerformanceMonitor:
    """Track memory usage and performance metrics."""

    def __init__(self):
        self.frame_times = []
        self.memory_usage = []

    def update(self, frame_time: float) -> None:
        """Record performance metrics."""
        self.frame_times.append(frame_time)
        self.memory_usage.append(self.get_memory_usage())

        # Keep only recent samples
        if len(self.frame_times) > 1000:
            self.frame_times.pop(0)
            self.memory_usage.pop(0)
```

### Rendering Optimization

#### Dirty Rectangle Updates

```python
class RenderManager:
    """Efficient rendering with dirty rectangle tracking."""

    def __init__(self, surface: pygame.Surface):
        self.surface = surface
        self.dirty_rects = []

    def mark_dirty(self, rect: pygame.Rect) -> None:
        """Mark screen region for redraw."""
        self.dirty_rects.append(rect)

    def render_frame(self) -> None:
        """Render only dirty regions."""
        if self.dirty_rects:
            pygame.display.update(self.dirty_rects)
            self.dirty_rects.clear()
```

#### Sprite Batching

```python
class SpriteBatch:
    """Batch similar rendering operations."""

    def __init__(self):
        self.batches: dict[str, list] = {}

    def add_sprite(self, sprite_type: str, position: tuple, image: pygame.Surface):
        """Add sprite to appropriate batch."""
        if sprite_type not in self.batches:
            self.batches[sprite_type] = []
        self.batches[sprite_type].append((position, image))

    def render_all(self, surface: pygame.Surface) -> None:
        """Render all batched sprites."""
        for sprite_type, sprites in self.batches.items():
            for position, image in sprites:
                surface.blit(image, position)
        self.batches.clear()
```

## Configuration System

### Configuration Files

#### Game Settings (config/game_settings.json)

```json
{
    "display": {
        "resolution": [1024, 768],
        "fullscreen": false,
        "vsync": true,
        "fps_limit": 60,
        "ui_scale": 1.0
    },
    "audio": {
        "master_volume": 0.8,
        "effects_volume": 0.7,
        "music_volume": 0.6,
        "voice_volume": 0.8
    },
    "gameplay": {
        "difficulty": "normal",
        "turn_timer": 30,
        "auto_save": true,
        "show_damage_numbers": true,
        "combat_speed": "normal"
    },
    "controls": {
        "mouse_sensitivity": 1.0,
        "scroll_speed": 1.0,
        "double_click_time": 500
    }
}
```

#### Key Bindings (config/key_bindings.json)

```json
{
    "movement": {
        "move_north": "w",
        "move_south": "s",
        "move_east": "d",
        "move_west": "a",
        "move_up": "q",
        "move_down": "e"
    },
    "combat": {
        "fire_phasers": "space",
        "fire_torpedoes": "t",
        "raise_shields": "r",
        "evasive_maneuvers": "v",
        "target_enemy": "tab"
    },
    "interface": {
        "toggle_minimap": "m",
        "ship_status": "s",
        "galaxy_map": "g",
        "pause_game": "p",
        "quick_save": "f5",
        "quick_load": "f9"
    }
}
```

#### Ship Classes (config/ship_classes.json)

```json
{
    "Constitution": {
        "hull_points": 100,
        "shield_strength": 80,
        "phaser_arrays": 4,
        "torpedo_tubes": 2,
        "torpedo_capacity": 10,
        "crew_complement": 430,
        "fuel_capacity": 100,
        "sensor_range": 10,
        "movement_range": 6
    },
    "Miranda": {
        "hull_points": 75,
        "shield_strength": 60,
        "phaser_arrays": 3,
        "torpedo_tubes": 2,
        "torpedo_capacity": 8,
        "crew_complement": 220,
        "fuel_capacity": 80,
        "sensor_range": 8,
        "movement_range": 7
    }
}
```

### Configuration Loading and Validation

```python
class ConfigLoader:
    """Load and validate configuration files."""

    def __init__(self, config_dir: Path):
        self.config_dir = config_dir
        self.loaded_configs = {}

    def load_config(self, filename: str) -> dict:
        """Load configuration file with validation."""
        config_path = self.config_dir / filename

        try:
            with open(config_path, 'r', encoding='utf-8') as file:
                config = json.load(file)

            self.validate_config(config, filename)
            self.loaded_configs[filename] = config
            return config

        except FileNotFoundError:
            raise ConfigError(f"Configuration file not found: {filename}")
        except json.JSONDecodeError as e:
            raise ConfigError(f"Invalid JSON in {filename}: {e}")
```

## Asset Management

### Asset Organization

#### Directory Structure

```
assets/
├── graphics/
│   ├── ships/
│   │   ├── federation/
│   │   ├── klingon/
│   │   └── romulan/
│   ├── ui/
│   │   ├── buttons/
│   │   ├── panels/
│   │   └── icons/
│   └── effects/
│       ├── weapons/
│       ├── explosions/
│       └── shields/
├── audio/
│   ├── effects/
│   ├── music/
│   └── voice/
└── data/
    ├── missions/
    ├── factions/
    └── sectors/
```

#### Asset Loading System

```python
class AssetManager:
    """Centralized asset loading and caching."""

    def __init__(self, asset_root: Path):
        self.asset_root = asset_root
        self.image_cache: dict[str, pygame.Surface] = {}
        self.sound_cache: dict[str, pygame.mixer.Sound] = {}

    def load_image(self, path: str) -> pygame.Surface:
        """Load image with caching."""
        if path in self.image_cache:
            return self.image_cache[path]

        full_path = self.asset_root / "graphics" / path
        try:
            image = pygame.image.load(str(full_path)).convert_alpha()
            self.image_cache[path] = image
            return image
        except pygame.error as e:
            raise AssetError(f"Failed to load image {path}: {e}")

    def preload_assets(self, asset_list: list[str]) -> None:
        """Preload critical assets."""
        for asset_path in asset_list:
            if asset_path.endswith(('.png', '.jpg', '.bmp')):
                self.load_image(asset_path)
            elif asset_path.endswith(('.wav', '.ogg', '.mp3')):
                self.load_sound(asset_path)
```

## Development Workflow

### Version Control

#### Git Workflow

```bash
# Feature development
git checkout -b feature/combat-system
git add src/game/combat.py tests/test_combat.py
git commit -m "feat: implement basic combat mechanics

- Add turn-based combat resolution
- Implement weapon damage calculations
- Add shield absorption mechanics
- Include comprehensive combat tests"

# Code review and merge
git checkout main
git merge feature/combat-system
git tag v0.1.0
```

#### Commit Message Format

```
type(scope): brief description

Detailed description of changes made and reasoning.

- Specific change 1
- Specific change 2
- Breaking changes noted

Closes #123
```

### Code Quality

#### Pre-commit Checks

```bash
# Type checking
mypy src/ --strict

# Style checking
flake8 src/ tests/

# Test execution
pytest tests/ --cov=src --cov-fail-under=80

# Documentation checks
pydocstyle src/
```

#### Continuous Integration

```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.14'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      - name: Run tests
        run: pytest tests/ --cov=src --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

## Troubleshooting Guide

### Common Issues

#### PySide6/PyGame Integration

**Problem**: Flickering or rendering issues with embedded PyGame

```python
# Solution: Proper surface management
class PyGameWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_OpaquePaintEvent)
        self.setUpdatesEnabled(False)  # Manual update control

    def paintEvent(self, event):
        # Convert PyGame surface to QPixmap
        raw_data = pygame.image.tostring(self.game_surface, 'RGB')
        qimg = QImage(raw_data, width, height, QImage.Format_RGB888)
        painter = QPainter(self)
        painter.drawImage(0, 0, qimg)
```

#### Memory Leaks

**Problem**: Growing memory usage during gameplay

```python
# Solution: Explicit cleanup and monitoring
class GameCleaner:
    def cleanup_turn(self):
        """Clean up resources after each turn."""
        # Release pooled objects
        self.projectile_pool.release_all_inactive()

        # Clear temporary collections
        self.temporary_objects.clear()

        # Force garbage collection periodically
        if self.turn_count % 100 == 0:
            import gc
            gc.collect()
```

#### Performance Issues

**Problem**: Frame rate drops during complex scenes

```python
# Solution: Level-of-detail and culling
class RenderOptimizer:
    def cull_objects(self, camera_bounds: pygame.Rect) -> list[GameObject]:
        """Return only objects visible to camera."""
        visible = []
        for obj in self.all_objects:
            if camera_bounds.colliderect(obj.get_bounds()):
                visible.append(obj)
        return visible

    def apply_lod(self, obj: GameObject, distance: float) -> GameObject:
        """Apply level-of-detail based on distance."""
        if distance > 100:
            return obj.get_low_detail_version()
        elif distance > 50:
            return obj.get_medium_detail_version()
        return obj
```

### Debugging Tools

#### Performance Profiler

```python
import cProfile
import pstats

def profile_game_loop():
    """Profile game loop performance."""
    profiler = cProfile.Profile()
    profiler.enable()

    # Run game loop
    game.run_single_frame()

    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative').print_stats(20)
```

#### Memory Monitor

```python
import tracemalloc

def monitor_memory():
    """Track memory allocation patterns."""
    tracemalloc.start()

    # Run problematic code
    game.run_for_turns(100)

    current, peak = tracemalloc.get_traced_memory()
    print(f"Current memory usage: {current / 1024 / 1024:.1f} MB")
    print(f"Peak memory usage: {peak / 1024 / 1024:.1f} MB")

    tracemalloc.stop()
```

### Development Tips

#### Efficient Testing

```bash
# Run only failing tests
pytest tests/ --lf

# Run tests matching pattern
pytest tests/ -k "combat"

# Parallel test execution
pytest tests/ -n auto

# Watch mode for continuous testing
ptw tests/ src/
```

#### Debug Logging

```python
import logging

# Configure debug logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('game_debug.log'),
        logging.StreamHandler()
    ]
)

# Use throughout codebase
logger = logging.getLogger(__name__)
logger.debug(f"Ship {ship.name} moving from {old_pos} to {new_pos}")
```

This documentation provides comprehensive guidance for developing and maintaining the Star Trek Retro Remake project. Refer to specific sections as needed during development, and update documentation as the project evolves.
