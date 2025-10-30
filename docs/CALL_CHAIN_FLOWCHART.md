# Star Trek Retro Remake - Call Chain Flow Chart

## Overview

This document provides visual flow charts showing how the game's components interact, where to implement specific features, and the execution flow from startup to gameplay.

## Table of Contents

- [Application Startup Flow](#application-startup-flow)
- [Main Game Loop](#main-game-loop)
- [State Machine Architecture](#state-machine-architecture)
- [MVC Component Interaction](#mvc-component-interaction)
- [Event Processing Flow](#event-processing-flow)
- [Rendering Pipeline](#rendering-pipeline)
- [Where to Code Specific Features](#where-to-code-specific-features)

---

## Application Startup Flow

```text
┌─────────────────────────────────────────────────────────────┐
│                         GAME STARTUP                         │
└─────────────────────────────────────────────────────────────┘

main.py (Entry Point)
    │
    ├─> if __name__ == "__main__"
    │
    ├─> StarTrekRetroRemake() instantiated
    │       │
    │       ├─> __init__()
    │       │       │
    │       │       ├─> ConfigManager.initialize()
    │       │       │       └─> Load game_settings.toml
    │       │       │           Load game_data.toml
    │       │       │           Load key_bindings.toml
    │       │       │
    │       │       ├─> GameModel() created
    │       │       │       └─> Initialize game state
    │       │       │           Create empty entities
    │       │       │
    │       │       ├─> GameView() created
    │       │       │       └─> pygame.init()
    │       │       │           Create display surface
    │       │       │           Load assets
    │       │       │
    │       │       └─> GameController(model, view) created
    │       │               └─> StateManager() created
    │       │                   clock = pygame.time.Clock()
    │       │                   running = False
    │       │
    │       └─> run() called
    │               │
    │               ├─> controller.start()
    │               │       │
    │               │       ├─> running = True
    │               │       ├─> start_new_game()
    │               │       │       │
    │               │       │       └─> state_manager.transition_to(SECTOR_MAP)
    │               │       │               └─> SectorMapState initialized
    │               │       │
    │               │       └─> _game_loop() ◄────┐
    │               │               │              │
    │               │               └─> [BLOCKING] │
    │               │                              │
    │               └─> view.run()                 │
    │                       │                      │
    │                       └─> [NON-BLOCKING]     │
    │                                              │
    └──────────────────────────────────────────────┘
                    GAME NOW RUNNING
```

---

## Main Game Loop

```text
┌─────────────────────────────────────────────────────────────┐
│              MAIN GAME LOOP (60 FPS Fixed)                   │
│              Location: controller.py::_game_loop()          │
└─────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────┐
    │   while self.running == True     │
    └────────────┬─────────────────────┘
                 │
                 ▼
    ┌────────────────────────────────────┐
    │  dt = clock.tick(60) / 1000.0      │ ◄─── Frame Rate Control
    │  (Delta time in seconds)           │      (16.67ms per frame)
    └────────────┬───────────────────────┘
                 │
                 ▼
    ┌────────────────────────────────────┐
    │  _handle_events()                  │
    │  ├─> pygame.event.get() [pygame-ce]            │
    │  ├─> Process QUIT, KEYDOWN, etc    │
    │  └─> state_manager.handle_event()  │
    │          └─> current_state.        │
    │              handle_event(event)   │
    └────────────┬───────────────────────┘
                 │
                 ▼
    ┌────────────────────────────────────┐
    │  _update(dt)                       │
    │  └─> state_manager.update(dt)      │
    │          └─> current_state.        │
    │              update(dt)            │
    │              └─> Update game logic │
    │                  Move entities     │
    │                  Check collisions  │
    │                  Process AI        │
    └────────────┬───────────────────────┘
                 │
                 ▼
    ┌────────────────────────────────────┐
    │  _render()                         │
    │  ├─> screen.fill(BLACK)            │
    │  ├─> state_manager.render(screen)  │
    │  │       └─> current_state.        │
    │  │           render(screen)        │
    │  │           └─> Draw grid         │
    │  │               Draw entities     │
    │  │               Draw UI elements  │
    │  └─> pygame.display.flip() [pygame-ce]         │
    └────────────┬───────────────────────┘
                 │
                 └─> Loop back to top
```

---

## State Machine Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│                    STATE MACHINE FLOW                        │
│            Location: states/ directory + controller.py      │
└─────────────────────────────────────────────────────────────┘

    ┌─────────────────┐
    │   MAIN_MENU     │ (Future)
    │   [Planned]     │
    └────────┬────────┘
             │ Start New Game
             ▼
    ┌─────────────────┐
    │   GALAXY_MAP    │ (Future)
    │   [Planned]     │
    │                 │
    │  - Navigate     │
    │    sectors      │
    │  - Manage       │
    │    resources    │
    └────────┬────────┘
             │ Enter Sector
             ▼
    ┌─────────────────┐
    │   SECTOR_MAP    │ ◄──────────┐ (Currently Active)
    │   [Active]      │            │
    │                 │            │
    │  - Explore grid │            │
    │  - Move ship    │            │
    │  - Encounter    │            │
    │    events       │            │
    └────────┬────────┘            │
             │ Combat Initiated    │
             ▼                     │
    ┌─────────────────┐            │
    │   COMBAT_MAP    │            │
    │   [Planned]     │            │
    │                 │            │
    │  - Tactical     │            │
    │    combat       │            │
    │  - Turn-based   │            │
    │  - Initiative   │            │
    └────────┬────────┘            │
             │ Combat Ends         │
             └─────────────────────┘

    ┌─────────────────┐
    │    SETTINGS     │ (Accessible from any state)
    │   [Planned]     │
    └─────────────────┘

    ┌─────────────────┐
    │     PAUSED      │ (Accessible from any state)
    │   [Planned]     │
    └─────────────────┘


State Transition Code Pattern:
─────────────────────────────────
# In controller.py or any state
self.state_manager.transition_to(GameMode.COMBAT)
    │
    ├─> Calls current_state.exit()
    ├─> Creates new state instance
    └─> Calls new_state.enter()
```

---

## MVC Component Interaction

```text
┌─────────────────────────────────────────────────────────────┐
│                  MVC ARCHITECTURE PATTERN                    │
└─────────────────────────────────────────────────────────────┘

┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│              │         │              │         │              │
│     VIEW     │◄────────│  CONTROLLER  │────────►│    MODEL     │
│  (view.py)   │         │(controller.py)│         │  (model.py)  │
│              │         │              │         │              │
└──────┬───────┘         └──────┬───────┘         └──────┬───────┘
       │                        │                        │
       │                        │                        │
       ▼                        ▼                        ▼
┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│  pygame-ce   │         │  Event       │         │  Game State  │
│  Rendering   │         │  Handling    │         │  & Logic     │
│              │         │              │         │              │
│  - Display   │         │  - Keyboard  │         │  - Entities  │
│  - Graphics  │         │  - Mouse     │         │  - Positions │
│  - UI Draw   │         │  - Commands  │         │  - Stats     │
└──────────────┘         └──────────────┘         │  - Rules     │
                                                   └──────────────┘

DATA FLOW:
──────────

User Input → Controller → Model (Update State)
                 ↓
            View (Render State)


IMPLEMENTATION RULES:
────────────────────

1. VIEW (view.py):
   - ONLY rendering code
   - NO game logic
   - NO direct model manipulation
   - Receives data to display

2. CONTROLLER (controller.py):
   - Handles all input events
   - Coordinates Model and View
   - Manages state transitions
   - NO rendering code

3. MODEL (model.py):
   - Pure game logic
   - NO pygame/pygame-ce imports
   - NO rendering dependencies
   - Fully testable in isolation
```

---

## Event Processing Flow

```text
┌─────────────────────────────────────────────────────────────┐
│                    EVENT PROCESSING FLOW                     │
└─────────────────────────────────────────────────────────────┘

User Action (Keyboard/Mouse)
        │
        ▼
┌────────────────────────┐
│  pygame.event.get() [pygame-ce]    │
│  (in controller.py)    │
└───────────┬────────────┘
            │
            ▼
┌────────────────────────────────────────┐
│  Controller::_handle_events()          │
│                                        │
│  for event in pygame.event.get(): [pygame-ce]      │
└───────────┬────────────────────────────┘
            │
            ├─> event.type == QUIT?
            │       └─> self.running = False
            │
            ├─> event.type == KEYDOWN?
            │       │
            │       ├─> ESC key? → Pause/Menu
            │       ├─> Arrow keys? → Movement
            │       └─> Other keys? → Commands
            │
            └─> Pass to State Manager
                    │
                    ▼
            ┌──────────────────────────┐
            │  state_manager.          │
            │  handle_event(event)     │
            └───────────┬──────────────┘
                        │
                        ▼
            ┌──────────────────────────┐
            │  current_state.          │
            │  handle_event(event)     │
            │                          │
            │  Example: SectorMapState │
            └───────────┬──────────────┘
                        │
                        ├─> KEYDOWN → movement_command
                        ├─> MOUSEBUTTONDOWN → select_entity
                        └─> Update model based on input
                                │
                                ▼
                        ┌──────────────────┐
                        │  model.update()  │
                        │  - Move ship     │
                        │  - Update state  │
                        └──────────────────┘
```

---

## Rendering Pipeline

```text
┌─────────────────────────────────────────────────────────────┐
│                     RENDERING PIPELINE                       │
└─────────────────────────────────────────────────────────────┘

_render() called (60 times per second)
    │
    ▼
┌────────────────────────────────────┐
│  Clear screen                      │
│  screen.fill(BLACK)                │
└────────────┬───────────────────────┘
             │
             ▼
┌────────────────────────────────────┐
│  state_manager.render(screen)      │
└────────────┬───────────────────────┘
             │
             ▼
┌────────────────────────────────────┐
│  current_state.render(screen)      │
│                                    │
│  Example: SectorMapState           │
└────────────┬───────────────────────┘
             │
             ├─> Draw Grid Layer
             │       │
             │       ├─> For each z-level:
             │       │   ├─> Draw grid lines
             │       │   └─> Apply transparency
             │       │       (current z: opaque)
             │       │       (other z: semi-transparent)
             │       │
             │       └─> Isometric projection
             │
             ├─> Draw Entity Layer
             │       │
             │       ├─> For each entity in model:
             │       │   ├─> Get position (x, y, z)
             │       │   ├─> Convert to screen coords
             │       │   ├─> Draw sprite/icon
             │       │   └─> Draw orientation indicator
             │       │
             │       └─> Apply z-sorting
             │
             ├─> Draw UI Layer
             │       │
             │       ├─> Ship status panel
             │       ├─> Resource indicators
             │       ├─> Turn counter
             │       └─> Action buttons
             │
             └─> Draw Debug Layer (if enabled)
                     │
                     ├─> FPS counter
                     ├─> Entity positions
                     └─> Collision boxes

    ▼
┌────────────────────────────────────┐
│  pygame.display.flip() [pygame-ce]             │
│  (Swap buffers, show frame)        │
└────────────────────────────────────┘
```

---

## Where to Code Specific Features

```text
┌─────────────────────────────────────────────────────────────┐
│              FEATURE IMPLEMENTATION LOCATIONS                │
└─────────────────────────────────────────────────────────────┘

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  GAME LOGIC & STATE (Pure Python, No UI)                   ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

📁 STRR/src/game/model.py
   ├─ Core game state management
   ├─ Entity position tracking
   ├─ Game rules and validation
   └─ Turn management

   WHERE TO ADD:
   • Ship movement rules
   • Combat calculations (formulas)
   • Resource management logic
   • Victory/defeat conditions
   • Save/load game state

📁 STRR/src/game/entities/
   ├─ base.py → Base GameObject class
   ├─ starship.py → Starship logic and stats
   └─ [future: station.py, planet.py, etc.]

   WHERE TO ADD:
   • New entity types (stations, planets)
   • Entity-specific behaviors
   • Stat calculations
   • Entity interactions

📁 STRR/src/game/components/
   └─ ship_systems.py → Ship subsystems

   WHERE TO ADD:
   • Weapon systems logic
   • Shield calculations
   • Engine power management
   • Sensor mechanics
   • Life support systems

📁 STRR/src/game/maps/
   ├─ galaxy.py → Galaxy map data/logic
   ├─ sector.py → Sector map data/logic
   └─ combat.py → Combat map generation

   WHERE TO ADD:
   • Map generation algorithms
   • Grid coordinate systems
   • Z-level management
   • Pathfinding logic
   • Environmental effects

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  STATE MANAGEMENT (Game Mode Logic)                        ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

📁 STRR/src/game/states/
   ├─ [future: main_menu.py]
   ├─ [future: galaxy_map.py]
   ├─ sector_map.py → Sector exploration mode
   ├─ [future: combat.py]
   ├─ [future: settings.py]
   └─ [future: paused.py]

   WHERE TO ADD:
   • New game modes/states
   • Mode-specific input handling
   • State transition logic
   • Mode-specific UI coordination

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  INPUT & COORDINATION (Event Processing)                   ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

📁 STRR/src/game/controller.py
   ├─ Main game loop
   ├─ State manager integration
   ├─ High-level event routing
   └─ Model-View coordination

   WHERE TO ADD:
   • Global hotkeys (ESC, F-keys)
   • State transition triggers
   • Pause/unpause logic
   • Game initialization

📁 STRR/src/game/commands.py
   └─ Command pattern for actions

   WHERE TO ADD:
   • New player commands
   • Undo/redo functionality
   • Command validation
   • Action queuing

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  RENDERING & UI (pygame-ce Display)                           ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

📁 STRR/src/game/view.py
   ├─ pygame-ce initialization
   ├─ Display surface management
   └─ Asset loading

   WHERE TO ADD:
   • Screen resolution handling
   • Fullscreen toggle
   • Asset caching
   • Sprite loading

📁 STRR/src/game/states/ (render methods)
   └─ Each state's render() method

   WHERE TO ADD:
   • Grid rendering (isometric)
   • Entity sprite drawing
   • Z-level visualization
   • HUD elements
   • Visual effects
   • Animation logic

📁 STRR/src/ui/ (Future - PySide6)
   ├─ dialogs/ → Modal dialogs
   └─ widgets/ → UI widgets

   WHERE TO ADD:
   • Mission briefing dialogs
   • Ship status windows
   • Settings menus
   • Inventory screens

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  CONFIGURATION & DATA (TOML Files)                         ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

📁 STRR/config/
   ├─ game_settings.toml → Display, controls, etc.
   ├─ game_data.toml → Ship classes, factions
   └─ key_bindings.toml → Input mappings

   WHERE TO ADD:
   • New game settings
   • Ship stats and classes
   • Faction definitions
   • Key binding customization

📁 STRR/assets/data/
   ├─ sectors/sol_system.toml
   └─ missions/ → Mission definitions

   WHERE TO ADD:
   • Sector definitions
   • Mission scripts
   • Star system data
   • Planet/station info

📁 STRR/src/engine/config_manager.py
   └─ Configuration loading/saving

   WHERE TO ADD:
   • New config file types
   • Validation logic
   • Default value handling

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  TESTING (pytest)                                          ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

📁 STRR/tests/
   ├─ test_game_model.py → Model logic tests
   ├─ test_entities.py → Entity behavior tests
   └─ conftest.py → Test fixtures

   WHERE TO ADD:
   • Unit tests for game logic
   • Integration tests for systems
   • Fixture data for testing
```

---

## Quick Reference: "I want to add..."

```text
┌─────────────────────────────────────────────────────────────┐
│                  QUICK FEATURE LOOKUP                        │
└─────────────────────────────────────────────────────────────┘

"I want to add a new weapon type"
    → LOGIC: components/ship_systems.py (WeaponSystems class)
    → DATA: config/game_data.toml (weapon stats)
    → RENDERING: states/combat.py (render method)
    → TESTING: tests/test_ship_systems.py

"I want to add ship movement"
    → LOGIC: model.py (movement rules) + entities/starship.py
    → INPUT: states/sector_map.py (handle_event method)
    → RENDERING: states/sector_map.py (render method)
    → TESTING: tests/test_entities.py

"I want to add a new game mode"
    → STATE: states/new_mode.py (create new GameState subclass)
    → CONTROLLER: controller.py (add transition method)
    → MODEL: model.py (add mode-specific state if needed)

"I want to add a new UI dialog"
    → FUTURE: ui/dialogs/new_dialog.py (PySide6)
    → FOR NOW: states/[current_state].py (pygame-ce draw code)

"I want to add a new entity type"
    → CLASS: entities/new_entity.py (GameObject subclass)
    → MODEL: model.py (track in appropriate list)
    → DATA: config/game_data.toml (entity stats)
    → RENDERING: states/[state].py (draw in render method)

"I want to change key bindings"
    → DATA: config/key_bindings.toml
    → INPUT: states/[state].py (handle_event method)

"I want to add combat mechanics"
    → LOGIC: model.py + components/ship_systems.py
    → STATE: states/combat.py (when created)
    → FORMULAS: components/ship_systems.py (damage calc, etc.)

"I want to add resource management"
    → LOGIC: model.py (resource tracking)
    → ENTITIES: entities/starship.py (resource consumption)
    → UI: states/[state].py (display resources in HUD)
    → DATA: config/game_data.toml (resource limits)

"I want to add AI behavior"
    → LOGIC: [future] ai/ directory
    → UPDATE: states/[state].py (update method, NPC turn)
    → MODEL: model.py (NPC decision making)

"I want to change the grid rendering"
    → RENDERING: states/sector_map.py (render method)
    → ISOMETRIC: [calculate screen coordinates from grid]
    → Z-LEVELS: [transparency based on current z]
```

---

## Architecture Principles Summary

```text
┌─────────────────────────────────────────────────────────────┐
│                 DESIGN PATTERN REMINDERS                     │
└─────────────────────────────────────────────────────────────┘

✅ DO:
   • Keep game logic in model.py and entities/
   • Keep rendering in view.py and state render() methods
   • Keep input handling in controller.py and state handle_event()
   • Use state pattern for different game modes
   • Use component composition for ship systems
   • Test game logic independently from UI
   • Use TOML files for configuration data
   • Follow type hints everywhere
   • Keep functions under 20 lines

❌ DON'T:
   • Put game logic in rendering code
   • Import pygame/pygame-ce in model.py or entities/
   • Hardcode values (use config files)
   • Create full ECS (use GameObject + Components)
   • Mix PySide6 UI with pygame-ce rendering
   • Add error handling before v1.0.0 (clean design first)
```

---

## Version History

- **v1.0** (2025-10-30): Initial flow chart documentation
