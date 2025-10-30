# Star Trek Retro Remake - Architecture Implementation Guide

<!--
Description:
    Detailed architecture specification and implementation guidelines for the
    Star Trek Retro Remake game. This document provides practical guidance
    for implementing the hybrid State Machine + Game Object + Component + MVC
    architecture defined in the Game Design Document.

Author: Star Trek Retro Remake Development Team
Date Created: 10-29-2025
Date Changed: 10-29-2025
License: Open Source

Features:
    - Hybrid architecture optimized for turn-based strategy games
    - Game State Machine for clean mode transitions
    - Game Object Pattern with Component composition
    - MVC separation for testable game logic
    - Object pooling for memory efficiency
    - PyGame/PySide6 integration patterns

Requirements:
    - Python 3.14+ for latest language features
    - PyGame for game engine functionality
    - PySide6 for UI, menus, and settings
    - Linux environment (primary target)

Architecture Overview:
    This architecture specification replaces the original ECS design with a
    hybrid approach better suited for turn-based strategy games. The design
    emphasizes clean separation of concerns, testability, and maintainability
    while avoiding unnecessary complexity.
-->

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Core Components](#core-components)
3. [Implementation Guidelines](#implementation-guidelines)
4. [Testing Strategy](#testing-strategy)
5. [Performance Guidelines](#performance-guidelines)
6. [Integration Guide](#integration-guide)

## Architecture Overview

### Design Philosophy

The Star Trek Retro Remake uses a **Hybrid State Machine + Game Object + Component + MVC** architecture optimized for turn-based strategy games. This design provides:

- **Clean Separation**: Game logic isolated from UI and rendering
- **Testability**: Pure Python business logic can be tested independently
- **Maintainability**: Clear component boundaries and responsibilities
- **Performance**: Object pooling and efficient resource management
- **Flexibility**: Modular design supports future expansion

### Why Not Pure ECS?

ECS (Entity-Component-System) is optimized for:

- Real-time games with thousands of entities
- Performance-critical scenarios
- Data-oriented design with cache optimization

Our game characteristics:

- Turn-based gameplay (performance less critical)
- Smaller entity counts (dozens, not thousands)
- Clear object hierarchies (starships contain systems)
- Heavy UI interaction (PySide6 widgets)

### Architecture Layers

```text
┌─────────────────────────────────────────┐
│            PySide6 UI Layer             │
│        (Menus, Dialogs, Windows)        │
├─────────────────────────────────────────┤
│             Controller Layer            │
│        (Input, State Management)        │
├─────────────────────────────────────────┤
│              Model Layer                │
│         (Game Logic, Data)              │
├─────────────────────────────────────────┤
│             View Layer                  │
│        (PyGame Rendering)               │
└─────────────────────────────────────────┘
```

## Core Components

### 1. Game State Machine

Manages transitions between major game modes:

```python
from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional

class GameMode(Enum):
    MAIN_MENU = "main_menu"
    GALAXY_MAP = "galaxy_map"
    SECTOR_MAP = "sector_map"
    COMBAT = "combat"
    SETTINGS = "settings"
    PAUSED = "paused"

class GameState(ABC):
    """Base class for all game states."""

    def __init__(self, state_manager: 'GameStateManager'):
        self.state_manager = state_manager
        self.mode = None  # Set by subclasses

    @abstractmethod
    def enter(self) -> None:
        """Called when entering this state."""
        pass

    @abstractmethod
    def exit(self) -> None:
        """Called when leaving this state."""
        pass

    @abstractmethod
    def handle_input(self, event) -> None:
        """Process input events."""
        pass

    @abstractmethod
    def update(self, dt: float) -> None:
        """Update game logic with delta time."""
        pass

    @abstractmethod
    def render(self, surface) -> None:
        """Render state-specific content."""
        pass

class GameStateManager:
    """Manages state transitions and current state."""

    def __init__(self):
        self.current_state: Optional[GameState] = None
        self.previous_state: Optional[GameState] = None
        self.states: dict[GameMode, GameState] = {}

    def register_state(self, mode: GameMode, state: GameState) -> None:
        """Register a state for a specific mode."""
        self.states[mode] = state

    def transition_to(self, mode: GameMode) -> None:
        """Transition to a new state."""
        if mode not in self.states:
            raise ValueError(f"Unknown game mode: {mode}")

        if self.current_state:
            self.current_state.exit()
            self.previous_state = self.current_state

        self.current_state = self.states[mode]
        self.current_state.enter()

    def update(self, dt: float) -> None:
        """Update current state."""
        if self.current_state:
            self.current_state.update(dt)

    def render(self, surface) -> None:
        """Render current state."""
        if self.current_state:
            self.current_state.render(surface)
```

### 2. Game Object Pattern

Base classes for all game entities:

```python
from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

@dataclass
class GridPosition:
    """3D grid position with z-level support."""
    x: int
    y: int
    z: int = 0

    def distance_to(self, other: 'GridPosition') -> float:
        """Calculate 3D distance to another position."""
        dx = self.x - other.x
        dy = self.y - other.y
        dz = self.z - other.z
        return (dx*dx + dy*dy + dz*dz) ** 0.5

class GameObject:
    """Base class for all game entities."""

    def __init__(self, position: GridPosition, name: str = ""):
        self.id = self._generate_id()
        self.position = position
        self.name = name
        self.active = True
        self.faction = None

    @staticmethod
    def _generate_id() -> str:
        """Generate unique entity ID."""
        import uuid
        return str(uuid.uuid4())

    def update(self, dt: float) -> None:
        """Update entity logic."""
        pass

    def destroy(self) -> None:
        """Mark entity for removal."""
        self.active = False

class Starship(GameObject):
    """Star Trek starship with modular systems."""

    def __init__(self, position: GridPosition, ship_class: str, name: str = ""):
        super().__init__(position, name)
        self.ship_class = ship_class

        # Ship systems (component composition)
        self.systems: Dict[str, 'ShipSystem'] = {
            'weapons': WeaponSystems(),
            'shields': ShieldSystems(),
            'engines': EngineSystems(),
            'sensors': SensorSystems(),
            'life_support': LifeSupportSystems()
        }

        # Ship resources
        self.crew = CrewRoster()
        self.resources = ResourceManager()

        # Ship state
        self.hull_integrity = 100.0
        self.orientation = 0  # 0-359 degrees

    def get_system(self, system_name: str) -> Optional['ShipSystem']:
        """Get a specific ship system."""
        return self.systems.get(system_name)

    def take_damage(self, amount: int, damage_type: str = "kinetic") -> None:
        """Apply damage to ship systems."""
        # Shield absorption first
        shields = self.get_system('shields')
        if shields and shields.active:
            amount = shields.absorb_damage(amount, damage_type)

        # Remaining damage to hull
        if amount > 0:
            self.hull_integrity = max(0, self.hull_integrity - amount)
            if self.hull_integrity <= 0:
                self.destroy()

class SpaceStation(GameObject):
    """Space station with docking and services."""

    def __init__(self, position: GridPosition, station_type: str, name: str = ""):
        super().__init__(position, name)
        self.station_type = station_type
        self.services = []  # repair, resupply, trading, etc.
        self.docked_ships = []
```

### 3. Component System (Simplified)

Ship systems as composable components:

```python
from abc import ABC, abstractmethod
from typing import Dict, Any

class ShipSystem(ABC):
    """Base class for all ship subsystems."""

    def __init__(self, name: str, max_efficiency: float = 1.0):
        self.name = name
        self.efficiency = max_efficiency
        self.max_efficiency = max_efficiency
        self.damaged = False
        self.active = True
        self.power_usage = 0.0

    @abstractmethod
    def update(self, dt: float) -> None:
        """Update system state."""
        pass

    def repair(self, amount: float) -> None:
        """Repair system damage."""
        self.efficiency = min(self.max_efficiency, self.efficiency + amount)
        if self.efficiency >= self.max_efficiency * 0.5:
            self.damaged = False

    def damage(self, amount: float) -> None:
        """Apply damage to system."""
        self.efficiency = max(0, self.efficiency - amount)
        if self.efficiency < self.max_efficiency * 0.5:
            self.damaged = True
        if self.efficiency <= 0:
            self.active = False

class WeaponSystems(ShipSystem):
    """Manages ship weapons and targeting."""

    def __init__(self):
        super().__init__("Weapons", 1.0)
        self.phaser_arrays = 4
        self.torpedo_tubes = 2
        self.torpedo_count = 10
        self.phaser_range = 5  # grid cells
        self.torpedo_range = 8  # grid cells

    def can_target(self, target_pos: GridPosition, ship_pos: GridPosition,
                   ship_orientation: int) -> bool:
        """Check if target is within firing arc."""
        distance = ship_pos.distance_to(target_pos)

        # Check range
        if distance > self.phaser_range:
            return False

        # Check firing arc (simplified to forward 180 degrees)
        # TODO: Implement proper arc calculations
        return True

    def calculate_damage(self, weapon_type: str, target: Starship) -> int:
        """Calculate weapon damage against target."""
        base_damage = 10 if weapon_type == "phaser" else 25
        return int(base_damage * self.efficiency)

    def update(self, dt: float) -> None:
        """Update weapon systems."""
        if not self.active:
            return
        # Weapon cooling, recharge, etc.

class ShieldSystems(ShipSystem):
    """Manages defensive shields."""

    def __init__(self):
        super().__init__("Shields", 1.0)
        self.shield_strength = 100.0
        self.max_shield_strength = 100.0
        self.recharge_rate = 5.0  # per second

    def absorb_damage(self, damage: int, damage_type: str) -> int:
        """Absorb damage and return remaining damage."""
        if not self.active or self.shield_strength <= 0:
            return damage

        # Shield effectiveness based on damage type
        effectiveness = 0.8 if damage_type == "energy" else 0.6
        absorbed = min(damage * effectiveness, self.shield_strength)

        self.shield_strength -= absorbed
        return int(damage - absorbed)

    def update(self, dt: float) -> None:
        """Recharge shields over time."""
        """Recharge shields over time."""
        if self.active and self.shield_strength < self.max_shield_strength:
            recharge = self.recharge_rate * dt * self.efficiency
            self.shield_strength = min(self.max_shield_strength,
                                     self.shield_strength + recharge)

class EngineSystems(ShipSystem):
    """Manages propulsion and movement."""

    def __init__(self):
        super().__init__("Engines", 1.0)
        self.impulse_power = 1.0
        self.warp_capable = True
        self.fuel = 100.0
        self.max_fuel = 100.0

    def calculate_movement_cost(self, distance: int) -> float:
        """Calculate fuel cost for movement."""
        return distance * 0.5 / self.efficiency

    def update(self, dt: float) -> None:
        """Update engine systems."""
        if not self.active:
            return
        # Engine maintenance, fuel consumption, etc.

class SensorSystems(ShipSystem):
    """Manages sensors and detection."""

    def __init__(self):
        super().__init__("Sensors", 1.0)
        self.short_range = 3  # grid cells
        self.long_range = 10  # grid cells
        self.passive_mode = True

    def scan_range(self) -> int:
        """Get current effective sensor range."""
        base_range = self.long_range if not self.passive_mode else self.short_range
        return int(base_range * self.efficiency)

    def update(self, dt: float) -> None:
        """Update sensor systems."""
        if not self.active:
            return
        # Sensor sweeps, data processing, etc.
```

### 4. Model-View-Controller (MVC)

Clean separation of concerns:

```python
from typing import List, Optional, Dict
import pygame
from PySide6.QtWidgets import QMainWindow, QWidget

class GameModel:
    """Pure game logic and state (no UI dependencies)."""

    def __init__(self):
        self.galaxy = GalaxyMap()
        self.current_sector: Optional[SectorMap] = None
        self.player_ship: Optional[Starship] = None
        self.turn_manager = TurnManager()
        self.game_objects: List[GameObject] = []
        self.active_missions: List[Mission] = []

    def initialize_new_game(self) -> None:
        """Set up a new game."""
        # Create player ship
        start_position = GridPosition(5, 5, 1)
        self.player_ship = Starship(start_position, "Constitution", "Enterprise")

        # Load starting sector
        self.current_sector = self.galaxy.get_sector(0, 0)
        self.game_objects.append(self.player_ship)

    def execute_move(self, ship: Starship, destination: GridPosition) -> bool:
        """Execute ship movement if valid."""
        if not self._is_valid_move(ship, destination):
            return False

        # Calculate movement cost
        distance = int(ship.position.distance_to(destination))
        engines = ship.get_system('engines')
        fuel_cost = engines.calculate_movement_cost(distance)

        if engines.fuel < fuel_cost:
            return False  # Insufficient fuel

        # Execute move
        ship.position = destination
        engines.fuel -= fuel_cost
        self.turn_manager.advance_turn()
        return True

    def resolve_combat(self, attacker: Starship, target: Starship,
                      weapon_type: str) -> 'CombatResult':
        """Resolve combat between two ships."""
        weapons = attacker.get_system('weapons')
        if not weapons or not weapons.active:
            return CombatResult(False, "Weapons offline")

        # Check targeting
        if not weapons.can_target(target.position, attacker.position,
                                attacker.orientation):
            return CombatResult(False, "Target out of range")

        # Calculate damage
        damage = weapons.calculate_damage(weapon_type, target)
        target.take_damage(damage)

        return CombatResult(True, f"Hit for {damage} damage", damage)

    def _is_valid_move(self, ship: Starship, destination: GridPosition) -> bool:
        """Check if move is valid."""
        if not self.current_sector:
            return False

        # Check bounds
        if not self.current_sector.is_in_bounds(destination):
            return False

        # Check for obstacles
        if self.current_sector.has_obstacle(destination):
            return False

        return True

class GameView:
    """Handles all rendering and UI display (no game logic)."""

    def __init__(self, controller: 'GameController'):
        self.controller = controller

        # PySide6 main window
        self.main_window = QMainWindow()
        self.setup_ui()

        # PyGame surface for game rendering
        self.game_surface = pygame.Surface((800, 600))
        pygame.init()

    def setup_ui(self) -> None:
        """Initialize PySide6 interface."""
        # Menu bar, status panels, dialogs, etc.
        pass

    def render_sector_map(self, sector: 'SectorMap',
                         game_objects: List[GameObject]) -> None:
        """Render the sector map and objects."""
        # Clear surface
        self.game_surface.fill((0, 0, 0))

        # Render grid
        self._render_grid(sector)

        # Render objects
        for obj in game_objects:
            self._render_game_object(obj)

        # Update display
        # Convert pygame surface to QPixmap and display in QLabel

    def show_combat_dialog(self, result: 'CombatResult') -> None:
        """Display combat results dialog."""
        # PySide6 dialog with combat information
        pass

    def show_ship_status(self, ship: Starship) -> None:
        """Display ship status panel."""
        # PySide6 widget with ship systems information
        pass

    def _render_grid(self, sector: 'SectorMap') -> None:
        """Render sector grid."""
        # Draw grid lines for each z-level
        pass

    def _render_game_object(self, obj: GameObject) -> None:
        """Render a single game object."""
        # Draw object sprite at grid position
        pass

class GameController:
    """Coordinates Model and View, handles input."""

    def __init__(self):
        self.model = GameModel()
        self.view = GameView(self)
        self.state_manager = GameStateManager()

        # Initialize states
        self._setup_states()

    def _setup_states(self) -> None:
        """Initialize all game states."""
        self.state_manager.register_state(
            GameMode.GALAXY_MAP,
            GalaxyMapState(self.state_manager, self)
        )
        self.state_manager.register_state(
            GameMode.SECTOR_MAP,
            SectorMapState(self.state_manager, self)
        )
        self.state_manager.register_state(
            GameMode.COMBAT,
            CombatState(self.state_manager, self)
        )

    def handle_ship_move_request(self, destination: GridPosition) -> None:
        """Handle player ship movement request."""
        if not self.model.player_ship:
            return

        success = self.model.execute_move(self.model.player_ship, destination)
        if not success:
            self.view.show_message("Invalid move")
        else:
            self.view.render_sector_map(
                self.model.current_sector,
                self.model.game_objects
            )

    def handle_combat_action(self, target: Starship, weapon_type: str) -> None:
        """Handle combat action request."""
        if not self.model.player_ship:
            return

        result = self.model.resolve_combat(
            self.model.player_ship, target, weapon_type
        )
        self.view.show_combat_dialog(result)

    def start_new_game(self) -> None:
        """Initialize and start a new game."""
        self.model.initialize_new_game()
        self.state_manager.transition_to(GameMode.SECTOR_MAP)

        # Update view
        self.view.render_sector_map(
            self.model.current_sector,
            self.model.game_objects
        )

# Supporting classes
class CombatResult:
    """Results of a combat action."""

    def __init__(self, success: bool, message: str, damage: int = 0):
        self.success = success
        self.message = message
        self.damage = damage

class TurnManager:
    """Manages turn-based gameplay."""

    def __init__(self):
        self.turn_number = 0
        self.current_phase = "player"

    def advance_turn(self) -> None:
        """Advance to next turn."""
        self.turn_number += 1
        # Handle NPC actions, events, etc.

# Additional supporting classes would be defined here:
# - GalaxyMap, SectorMap
# - Mission system
# - Resource management
# - CrewRoster
# - etc.
```

## Implementation Guidelines

### State Management

1. **Clear State Boundaries**: Each state should have distinct responsibilities
2. **State Persistence**: Save/load should work from any state
3. **Transition Validation**: Validate state transitions are legal
4. **Error Handling**: Graceful degradation if state transition fails

### Object Lifecycle

1. **Object Pooling**: Reuse objects for performance
2. **Clean Destruction**: Properly clean up resources
3. **Reference Management**: Avoid circular references
4. **Memory Monitoring**: Track object creation/destruction

### Component Interaction

1. **Loose Coupling**: Components should not directly reference each other
2. **Event System**: Use events for component communication
3. **Dependency Injection**: Pass dependencies explicitly
4. **Interface Contracts**: Use protocols/ABC for contracts

### Testing Strategy

1. **Unit Tests**: Test each component in isolation
2. **Integration Tests**: Test component interactions
3. **State Tests**: Test state transitions and persistence
4. **UI Tests**: Test UI behavior separately from logic

This architecture provides a solid foundation for the Star Trek Retro Remake while maintaining flexibility for future expansion.

## Performance Guidelines

### Memory Management

1. **Object Pooling**: Implement object pools for frequently created/destroyed objects
   - Ship projectiles (phasers, torpedoes)
   - UI elements (combat dialogs, status windows)
   - Temporary calculation objects

2. **Resource Cleanup**: Ensure proper cleanup of PyGame and PySide6 resources
   - Surface management
   - Font caching
   - Image loading/unloading

3. **State Persistence**: Minimize memory usage during state transitions
   - Clear unnecessary caches when switching states
   - Lazy load resources when entering new states

### Rendering Optimization

1. **Dirty Rectangle Updates**: Only redraw changed portions of the screen
2. **Layer Management**: Separate static background from dynamic objects
3. **Sprite Batching**: Group similar rendering operations
4. **Z-Level Optimization**: Minimize overdraw in 3D grid rendering

### Turn-Based Performance

1. **AI Processing**: Limit AI calculation time per turn
2. **Batch Operations**: Group similar operations (all ship updates together)
3. **Event Queuing**: Queue events to prevent frame rate spikes
4. **Background Processing**: Use threading for non-critical calculations

### PySide6 Integration

1. **Widget Reuse**: Cache and reuse dialog windows
2. **Model Updates**: Batch model updates to prevent excessive redraws
3. **Thread Safety**: Ensure UI updates happen on main thread
4. **Resource Loading**: Load UI resources asynchronously when possible

## Integration Guide

### PyGame + PySide6 Setup

1. **Window Management**: PySide6 main window contains PyGame widget
2. **Event Handling**: Route PyGame events through PySide6 event system
3. **Resource Sharing**: Share fonts, colors, and styling between frameworks
4. **Testing**: Test each framework independently before integration

### State Machine Integration

1. **UI States**: Map game states to PySide6 window configurations
2. **Rendering States**: Each state defines its PyGame rendering requirements
3. **Input Routing**: Route input events to appropriate state handlers
4. **Persistence**: Save/load state information across sessions
