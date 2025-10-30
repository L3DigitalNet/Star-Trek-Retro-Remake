# Python File Reference Guide

**Version:** 0.0.2
**Last Updated:** 10-30-2025

This document provides a clear reference for the purpose of each Python file in the Star Trek Retro Remake project and indicates where to add specific types of code.

> **📖 Note:** For detailed documentation on individual files, see the corresponding `_doc.md` files located alongside each `.py` file. This guide provides a high-level overview, while `_doc.md` files contain comprehensive module-specific documentation. See [DOCUMENTATION_STANDARDS.md](DOCUMENTATION_STANDARDS.md) for more information.

---

## Entry Point

### `/star_trek_retro_remake/main.py`

**Purpose:** Application entry point and bootstrapping

**Contains:**

- `main()` function - program entry
- Version constant
- Python path setup for imports

**Add code here for:**

- Command-line argument parsing
- Initial application setup
- Global initialization
- Top-level error handling

---

## Core Application Layer

### `/star_trek_retro_remake/src/game/application.py`

**Purpose:** Main application coordinator implementing MVC pattern

**Contains:**

- `StarTrekRetroRemake` class - main application controller
- System initialization (pygame-ce + PySide6)
- Application lifecycle management
- MVC component coordination

**Add code here for:**

- **pygame-ce window initialization** ⭐ (in `_initialize_systems()`)
- PySide6 Qt application setup
- Linking Model-View-Controller components
- Application-wide resource management
- Main loop coordination
- Shutdown procedures

**Key Method for pygame-ce Setup:**

```python
def _initialize_systems(self) -> None:
    # Add pygame.display.set_mode() here
    # Add pygame.init() configurations here
```

---

## MVC Components

### `/star_trek_retro_remake/src/game/model.py`

**Purpose:** Pure game logic and state (no UI dependencies)

**Contains:**

- `GameModel` class - game state container
- `TurnManager` class - turn-based mechanics
- `CombatResult` dataclass - combat outcomes

**Add code here for:**

- Game rules and logic
- State management
- Turn processing
- Combat resolution
- Save/load game state
- Mission management
- Resource calculations

**DO NOT add here:**

- Any UI code
- pygame-ce rendering
- PySide6 widgets
- Direct user input handling

---

### `/star_trek_retro_remake/src/game/view.py`

**Purpose:** UI rendering and display (View in MVC)

**Contains:**

- `GameView` class - manages all visual output
- PySide6 main window
- pygame-ce surface integration

**Add code here for:**

- **pygame-ce rendering logic** ⭐
- **pygame-ce surface drawing**
- PySide6 widget creation
- UI layout management
- Dialog boxes
- HUD elements
- Visual effects
- Display updates

**Key Areas:**

- `_setup_pygame_widget()` - embed pygame-ce in Qt
- `_render_grid()` - sector grid rendering
- `_render_game_object()` - entity rendering
- `render_sector_map()` - main game view

---

### `/star_trek_retro_remake/src/game/controller.py`

**Purpose:** Coordinates Model and View, handles input

**Contains:**

- `GameController` class - MVC coordinator
- Input event processing
- Game loop management
- State transition coordination

**Add code here for:**

- **pygame-ce event handling** ⭐
- Input processing (keyboard, mouse)
- Command execution
- Model-View synchronization
- Game state transitions
- Game loop implementation

**Key Method for Game Loop:**

```python
def _game_loop(self) -> None:
    # Main game loop with pygame-ce clock
    # Event handling → Update → Render cycle
```

---

## Supporting Systems

### `/star_trek_retro_remake/src/game/commands.py`

**Purpose:** Command pattern for undoable actions

**Contains:**

- `Command` base class
- `MoveShipCommand` - ship movement
- `FireWeaponCommand` - combat actions
- `CommandHistory` - undo/redo management

**Add code here for:**

- New command types (scan, dock, repair, etc.)
- Undo/redo logic
- Command validation
- Action recording

---

### `/star_trek_retro_remake/src/game/events.py`

**Purpose:** Event bus for component communication

**Contains:**

- `GameEvent` class - event data
- `EventBus` class - publish/subscribe system
- `EventPriority` enum - event ordering
- Global event bus functions

**Add code here for:**

- New event types
- Event listeners
- Cross-component notifications
- Event filtering logic

**Usage pattern:**

```python
from game.events import publish_event, subscribe_event, GameEvent

# Publish
publish_event(GameEvent("ship_destroyed", {"ship_id": id}))

# Subscribe
subscribe_event("ship_destroyed", my_handler)
```

---

### `/star_trek_retro_remake/src/game/exceptions.py`

**Purpose:** Custom exception definitions

**Contains:**

- `GameError` - base exception
- `InvalidMoveError` - movement errors
- `InsufficientResourcesError` - resource errors
- `SystemOfflineError` - ship system errors
- `CombatError` - combat errors
- `ConfigurationError` - config errors
- `SaveLoadError` - save/load errors
- `StateTransitionError` - state machine errors
- `EntityNotFoundError` - entity errors

**Add code here for:**

- New exception types
- Error context data
- Error hierarchy

---

### `/star_trek_retro_remake/src/game/states/state_machine.py`

**Purpose:** Game state machine implementation

**Contains:**

- `GameMode` enum - available game modes
- `GameState` abstract base class
- `GameStateManager` - state transitions

**Add code here for:**

- New game state implementations
- State-specific logic classes
- State transition rules
- State validation

**State Types to Implement:**

- `MainMenuState`
- `GalaxyMapState`
- `SectorMapState`
- `CombatState`
- `SettingsState`
- `PausedState`

---

## Entities

### `/star_trek_retro_remake/src/game/entities/base.py`

**Purpose:** Base classes for all game entities

**Contains:**

- `GridPosition` dataclass - 3D positioning
- `GameObject` class - base entity class

**Add code here for:**

- Core entity properties
- Position calculations
- Entity lifecycle management
- Common entity behaviors

---

### `/star_trek_retro_remake/src/game/entities/starship.py`

**Purpose:** Starship and space station entities

**Contains:**

- `Starship` class - player and NPC ships
- `SpaceStation` class - stations and bases

**Add code here for:**

- Ship-specific logic
- Crew management
- Resource tracking
- Station services
- Docking mechanics

---

## Components

### `/star_trek_retro_remake/src/game/components/ship_systems.py`

**Purpose:** Modular ship subsystems (Component pattern)

**Contains:**

- `ShipSystem` abstract base class
- `WeaponSystems` - weapons and targeting
- `ShieldSystems` - defensive shields
- `EngineSystems` - propulsion
- `SensorSystems` - detection and scanning
- `LifeSupportSystems` - crew support

**Add code here for:**

- New ship systems (communications, transporters, etc.)
- System-specific mechanics
- Power management
- Damage modeling
- System interactions

---

## Maps

### `/star_trek_retro_remake/src/game/maps/galaxy.py`

**Purpose:** Galaxy-scale map and navigation

**Contains:**

- `GalaxyMap` class - sector collection management

**Add code here for:**

- Galaxy generation
- Sector organization
- Faction territories
- Large-scale navigation
- Strategic map features

---

### `/star_trek_retro_remake/src/game/maps/sector.py`

**Purpose:** Detailed sector maps with 3D grid

**Contains:**

- `SectorMap` class - 3D grid sector management

**Add code here for:**

- Sector generation
- 3D grid logic
- Entity placement
- Obstacle management
- Environmental effects
- Hazard zones

---

## Engine/Utilities

### `/star_trek_retro_remake/src/engine/config_manager.py`

**Purpose:** Configuration file loading and management

**Contains:**

- `ConfigManager` class - TOML/JSON config handling
- Global config manager functions

**Add code here for:**

- Config validation
- File migration logic
- Config schema definitions
- Settings management

---

## Quick Reference by Task

### **PyGame Window Initialization**

→ `/star_trek_retro_remake/src/game/application.py`

- Method: `_initialize_systems()`
- Initialize `pygame.display.set_mode()`
- Set window title, icon, etc.

### **pygame-ce Rendering**

→ `/star_trek_retro_remake/src/game/view.py`

- Methods: `_render_grid()`, `_render_game_object()`, `render_sector_map()`
- All drawing code goes here

### **pygame-ce Event Handling**

→ `/star_trek_retro_remake/src/game/controller.py`

- Method: `_handle_events()`
- Process keyboard, mouse, quit events

### **Game Logic/Rules**

→ `/star_trek_retro_remake/src/game/model.py`

- Pure logic, no UI
- State changes, calculations

### **Ship Systems**

→ `/star_trek_retro_remake/src/game/components/ship_systems.py`

- Add new systems as classes inheriting from `ShipSystem`

### **New Entity Types**

→ `/star_trek_retro_remake/src/game/entities/`

- Inherit from `GameObject` in `base.py`
- Create new files for new entity categories

### **State Machine States**

→ `/star_trek_retro_remake/src/game/states/`

- Create new state classes inheriting from `GameState`
- Register in `GameStateManager`

### **UI Dialogs/Widgets**

→ `/star_trek_retro_remake/src/ui/`

- PySide6 dialogs in `dialogs/`
- PySide6 widgets in `widgets/`

---

## Architecture Summary

```text
main.py
  └─> application.py (StarTrekRetroRemake)
       ├─> model.py (GameModel) ← Pure game logic
       ├─> view.py (GameView) ← pygame-ce + PySide6 rendering
       └─> controller.py (GameController) ← Coordination + Input
            ├─> states/state_machine.py (GameStateManager)
            ├─> commands.py (CommandHistory)
            ├─> events.py (EventBus)
            ├─> entities/ (GameObject hierarchy)
            │    ├─> base.py
            │    └─> starship.py
            ├─> components/ (Ship systems)
            │    └─> ship_systems.py
            └─> maps/ (Game world)
                 ├─> galaxy.py
                 └─> sector.py
```

---

## Notes

- **Separation of Concerns:** Keep game logic in `model.py`, rendering in `view.py`, coordination in `controller.py`
- **pygame-ce vs PySide6:** pygame-ce for game rendering, PySide6 for menus/dialogs/settings
- **3D Grid:** All positions use `GridPosition(x, y, z)` - remember the z-level!
- **Turn-Based:** All actions should advance turn counter
- **Component Pattern:** Ship systems are components, not full ECS
- **Testing:** All game logic in model.py can be tested without UI

---

## Version History

- **0.0.2** (10-30-2025) - Initial reference document created
