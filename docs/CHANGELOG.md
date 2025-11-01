# Changelog

All notable changes to the Star Trek Retro Remake project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.0.29] - 2025-11-01

### Fixed

- **Starship Attribute Access**: Corrected component-based attribute access in `view.py`
  - Changed `ship.shields` to `ship.systems["shields"].total_shield_strength`
  - Changed `ship.energy` to `ship.resources.energy_current`
  - Fixed `AttributeError` that occurred when displaying ship status
  - Properly uses ShieldSystems and ResourceManager components

### Technical Details

- Shields accessed via ShieldSystems component: `total_shield_strength` property
- Energy accessed via ResourceManager component: `energy_current` attribute
- Progress bars now correctly display shield and energy percentages
- Follows component-based architecture pattern consistently

## [0.0.28] - 2025-11-01

### Fixed

- **Config Manager Initialization**: Added `initialize_config_manager()` call in `application.py`
  - Config manager now properly initialized before first use
  - Fixes `ConfigurationError: Configuration manager not initialized` on startup
  - Added imports to top-level: `Path`, `initialize_config_manager`
- **Undefined Variable**: Fixed `sector_name` potentially unbound in `view.py`
  - Added else clause with "Sector: Unknown" fallback
  - Prevents `NameError` when `current_sector` is None
- **Duplicate Code**: Removed duplicate `setText(sector_name)` call in `update_ui_state()`
- **Version Inconsistency**: Updated `application.py` from v0.0.23 to v0.0.28

### Changed

- **Import Organization**: Moved local imports to module top-level
  - Dialog imports (`QDialog`, `QHBoxLayout`, `QLabel`, `QListWidget`, `QPushButton`, `QVBoxLayout`)
  - Mission dialogs (`MissionSelectionDialog`, `MissionBriefingDialog`)
  - Settings dialog (`SettingsDialog`)
  - Improves code clarity and performance (PEP 8 compliance)
- **Version Updates**: Incremented to 0.0.28
  - pyproject.toml
  - application.py
  - view.py

### Technical Details

- Configuration manager initialization successful ✓
- Config file paths corrected (removed duplicate .toml extension) ✓
- All critical startup bugs resolved ✓
- Code quality improved with proper import organization ✓
- 380/381 tests passing (99.7% pass rate) ✓

## [0.0.27] - 2025-11-01

### Changed

- **UI Loading Architecture**: Refactored to use compiled .ui files for better performance
  - Replaced `QUiLoader` runtime loading with compiled `Ui_MainWindow` class
  - Direct access to UI elements via `self.ui.element_name` for type safety
  - Removed `_get_required_ui_element()` method (no longer needed)
  - Updated imports: removed unused `QAction`, `QDockWidget`, `QProgressBar`, `QPushButton`
  - Compiled `main_window_complete.ui` to `main_window_complete_ui.py`
- **Version Consistency**: Updated to 0.0.27
  - pyproject.toml
  - STRR/src/game/view.py

### Technical Benefits

- **Performance**: Eliminated runtime XML parsing overhead
- **Type Safety**: Direct attribute access provides better IDE autocompletion
- **Compile-Time Verification**: UI elements validated during compilation
- **Code Clarity**: Cleaner initialization pattern with `setupUi()`

## [0.0.26] - 2025-10-31

### Fixed

- **Local Import Anti-Pattern**: Moved `MissionType` import to top-level in mission_dialogs.py (line 73)
- **Controller Test Failures**: Updated tests to match confident design pattern (no defensive None checks)
  - test_handle_ship_move_request_without_player_ship: Expects None propagation
  - test_handle_combat_action_without_player_ship: Expects None propagation
- **Settings Dialog Test Failures**: Fixed GameplayTab attribute references
  - Updated tests to use `autosave_check` (checkbox) instead of `autosave_combo`
  - Corrected nested dict structure for settings validation
  - Fixed boolean comparison style (PEP 8 compliance)

### Added

- **Controller Integration Methods**: Mission system coordination
  - `show_mission_briefing(mission)`: Display mission briefing dialog
  - `accept_mission(mission)`: Add mission to active missions
  - `show_mission_selection()`: Show available missions dialog
  - `update_mission_tracker()`: Update mission tracker widget
- **View Integration Methods**: Dialog display handlers
  - `_on_settings()`: Show settings dialog
  - `_show_mission_selection()`: Display mission selection dialog
  - `_show_mission_briefing(mission)`: Display mission briefing
  - `_update_mission_tracker()`: Update tracker with active missions
- **Test Infrastructure**: PySide6 Qt testing support
  - `qtbot` fixture in conftest.py for widget lifecycle management
  - `qapp` session fixture for QApplication singleton
  - `SimpleQtBot` class for widget cleanup
- **Comprehensive Test Suites**: 34 new tests for dialog systems
  - test_mission_dialogs.py: 16 tests (mission UI components)
  - test_settings_dialog.py: 18 tests (settings dialog and tabs)

### Changed

- **Version Consistency**: Updated to 0.0.26
  - pyproject.toml
  - All modified component files
- **Test Coverage**: From 347 → 381 tests (100% pass rate)
  - Mission dialog components fully tested
  - Settings dialog components fully tested
  - Controller integration verified

### Technical

- **Testing Framework**: Enhanced pytest with Qt support
  - QtBot fixture for widget interaction testing
  - Mission manager fixture for dialog tests
  - Temporary config file fixtures for settings tests
- **Code Quality**: Confident design pattern enforcement
  - Controller methods rely on valid model state
  - No defensive None checks in business logic
  - Type hints maintained throughout

## [0.0.25] - 2025-10-31

### Added

- **Dialog and Menu Systems (Priority 2 Milestone - Partial)**: UI components for mission and settings management
  - MissionBriefingDialog with detailed mission information display
  - MissionSelectionDialog for browsing and selecting missions at starbases
  - MissionTrackerWidget for displaying active missions in main UI
  - ObjectiveProgressBar for visualizing objective progress
  - SettingsDialog with tabbed interface (Graphics, Audio, Gameplay, Key Bindings)
  - TOML integration for loading and saving settings
  - Difficulty color-coding and visual indicators
  - Signal-based mission acceptance/decline workflow
  - Auto-generation of missions if none available in sector

### Features

- **Mission UI Components**:
  - Mission briefing with objectives, rewards, and difficulty display
  - Mission preview panel in selection dialog
  - Active mission tracker with progress bars
  - Accept/Decline buttons with signal emission
  - Formatted reward text with HTML styling

- **Settings Management**:
  - Graphics settings (resolution, fullscreen, V-Sync, FPS limit)
  - Audio settings (master, music, effects volume sliders)
  - Gameplay settings (difficulty, auto-save, hints, animations)
  - Key bindings tab with reset to defaults
  - Apply/OK/Cancel button workflow

### Technical

- **Version Consistency**: Updated to version 0.0.25
  - mission_dialogs.py, settings_dialog.py
  - Updated Date Changed to 10-31-2025 for all modified files
- **File Structure**: New UI component files
  - STRR/src/game/ui/mission_dialogs.py (507 lines)
  - STRR/src/game/ui/mission_dialogs_doc.md (comprehensive documentation)
  - STRR/src/game/ui/settings_dialog.py (470 lines)

## [0.0.24] - 2025-10-31

### Added

- **Mission System Foundation (Priority 1 Milestone)**: Complete mission management system
  - Mission data structures with comprehensive type hints (MissionType, MissionStatus, MissionObjective, MissionReward, Mission)
  - MissionManager component for tracking mission lifecycle
  - Six mission types: PATROL, COMBAT, ESCORT, RESCUE, DIPLOMATIC, SURVEY
  - TOML-based mission templates with configurable objectives and rewards
  - Dynamic mission generation with difficulty scaling
  - Mission state tracking (available, active, completed, failed)
  - Mission objective progress tracking and auto-completion
  - Reward system with reputation, supplies, spare parts, and experience
  - Sector-based mission filtering
  - Integration with GameModel for turn-based mission updates
  - 18 comprehensive unit tests with 100% pass rate
  - Complete API documentation in mission_manager_doc.md

### Changed

- **GameModel Integration**: Added MissionManager to GameModel initialization
  - Mission system initialized with path to mission_templates.toml
  - New `update_missions()` method for turn-based mission lifecycle updates
  - Updated version to 0.0.24 across modified modules

### Technical

- **Version Consistency**: Updated all modified modules to version 0.0.24
  - model.py, mission_manager.py
  - Updated Date Changed to 10-31-2025 for all modified files
- **File Structure**: New mission system files
  - STRR/src/game/components/mission_manager.py (369 lines)
  - STRR/src/game/components/mission_manager_doc.md (comprehensive documentation)
  - STRR/assets/data/mission_templates.toml (mission definitions)
  - STRR/tests/test_mission_manager.py (18 tests)

## [0.0.23] - 2025-10-31

### Changed

- **Confident Design Patterns**: Replaced defensive None checks with architectural guarantees across core modules, except where null checks are required for safety (see v0.0.22 bug fixes)
- **Type Annotations**: Updated `current_sector` from `SectorMap | None` to `SectorMap` in GameModel to reflect actual program constraints
- **UI Element Access**: Removed `hasattr` checks for UI elements in GameView, replaced with confident access patterns since elements are guaranteed from Qt Designer files
- **Configuration Management**: Moved magic numbers to TOML configuration (display dimensions, frame rates, UI colors)
- **Import Optimization**: Simplified TYPE_CHECKING imports where circular dependencies don't exist (moved GridPosition out of TYPE_CHECKING in view.py)
- **Initialization Patterns**: Implemented confident object creation with proper error handling only during setup phase, not during gameplay
- **Code Quality Improvements**: Comprehensive codebase cleanup and standardization
  - Confirmed pygame-ce (Community Edition) package provides drop-in pygame module for Python 3.14+ compatibility
  - Removed unnecessary UTF-8 encoding declarations (`# -*- coding: utf-8 -*-`) from all files per Python 3 standards
  - Cleaned up unused imports (MagicMock, pytest, time) from test files
  - Updated repository guidelines to remove UTF-8 encoding declaration requirements

### Fixed

- **Architectural Integrity**: Eliminated scattered defensive checks that indicated architectural problems
- **Error Handling**: Moved error handling to initialization phase where it belongs, ensuring clean gameplay logic
- **Type Safety**: Resolved type errors in ship_systems.py
  - Fixed return type mismatch in `_load_combat_config()` method (added assertion to ensure non-None return)
  - Fixed unused loop variable warning by prefixing with underscore (`_facing`)

### Documentation

- **Repository Standards**: Updated documentation to reflect Python 3 defaults
  - Modified `.github/copilot-instructions.md` to remove encoding declaration requirement
  - Updated `docs/DOCUMENTATION_STANDARDS.md` to clarify Python 3 UTF-8 default
  - All documentation now correctly states "no encoding declaration needed"

### Technical

- **Version Consistency**: Updated all modified core modules to version 0.0.23
  - application.py, controller.py, view.py, isometric_grid.py
  - sector_state.py, ship_systems.py
  - Updated Date Changed to 10-31-2025 for all modified files

## [0.0.22] - 2025-10-31

### Added

- **Resource Management System**: Complete energy, fuel, and supplies tracking
  - ResourceManager component with energy capacity (1000), regeneration (10/sec), and consumption tracking
  - Power distribution system for shields, weapons, engines, sensors, life support
  - Configurable energy costs per action (move: 10, fire phaser: 15, fire torpedo: 25, scan: 5, shield regen: 20)
  - Fuel system with capacity (500) and consumption tracking
  - Supply tracking for medical supplies (100) and spare parts (50)
  - Energy regeneration affected by engine power allocation and system efficiency
  - Resupply and refuel mechanics for starbase services

- **Crew Management System**: Morale and efficiency tracking
  - CrewManager component with crew roster (Captain, First Officer, Chief Engineer, Science Officer, Security Chief, Helm Officer)
  - Morale system (0-100) affecting ship system efficiency
  - Morale modifiers: victory (+5), defeat (-10), casualty (-5), turns away from starbase (-0.5 per turn after 10)
  - Efficiency multipliers based on morale: high morale (>80) = 1.2x, normal (60-80) = 1.0x, low (<40) = 0.8x
  - Starbase visit bonus (+20 morale) and counter resets
  - Combat outcome tracking (victories/defeats) with morale impact

- **Enhanced Starship Resource Integration**:
  - Integrated ResourceManager and CrewManager into Starship entity
  - Power allocation methods for system-level power distribution
  - Energy consumption checks before actions
  - Crew efficiency modifiers for repairs and operations
  - Repair system now consumes spare parts based on damage amount
  - Repair effectiveness affected by crew efficiency multiplier

- **Space Station Services**:
  - Refuel service restores fuel to maximum capacity
  - Resupply service restores medical supplies and spare parts
  - Repair service fixes all systems and hull to 100% efficiency
  - Starbase visit boosts crew morale and resets mission counters

- **Configuration System**:
  - Added [game.resources] section to game_settings.toml with all energy, fuel, and supply parameters
  - Added [game.crew] section with morale modifiers and efficiency multipliers
  - All resource values configurable via TOML with fallback defaults

### Fixed

- **Critical Null Reference Bugs**: Added null checks for `player_ship` in `GameController.handle_ship_move_request()` and `handle_combat_action()` methods to prevent crashes when player ship is not initialized
- **Model Validation Bug**: Added null check for `current_sector` in `GameModel._is_valid_move()` to prevent AttributeError when sector is not loaded
- **Import Order Violation**: Fixed PEP 8 violation by moving module import to proper location in `main.py`
- **Encoding Declaration**: Removed unnecessary UTF-8 encoding declaration in `main.py` as it's redundant in Python 3.14+
- **Test Failures**: Fixed 3 failing tests related to null reference bugs:
  - `test_handle_ship_move_request_without_player_ship`
  - `test_handle_combat_action_without_player_ship`
  - `test_is_valid_move_no_sector`

### Changed

- **Version Management**: Updated version to 0.0.22 across all core modules and pyproject.toml
- **Error Handling**: Improved defensive programming with proper null checks and early returns
- **Starship Repair Mechanics**: Updated repair_system() to consume supplies and apply crew efficiency
  - Repair costs calculated based on damage amount (10 spare parts per 0.1 efficiency)
  - Repair effectiveness multiplied by crew efficiency (0.8x to 1.2x)
  - Optional supply consumption for field repairs vs starbase repairs

### Testing

- **Comprehensive Test Coverage**: Added 35 new unit tests for resource management
  - TestResourceManager: 14 tests covering energy, fuel, supplies, and power distribution
  - TestCrewManager: 10 tests covering morale, efficiency, combat outcomes, and crew management
  - TestStarshipResourceIntegration: 11 tests covering integration with Starship entity
  - All tests passing with edge case coverage (zero energy, insufficient supplies, morale extremes)

## [0.0.21] - 2025-01-27

### Fixed

- **Division by Zero Guard**: Added safety check in `WeaponSystems.get_hit_chance()` to prevent division by zero when weapon has no range
- **AI Turn Loop Scaling**: Fixed `_process_ai_turns()` to dynamically scale safety limit based on total entity count (minimum 20, or 2x entity count)
- **Shield Effectiveness**: Ensured shields always absorb minimum damage (10% of incoming damage or available shield strength) when active, preventing complete bypass
- **Type Consistency**: Verified `take_damage()` always returns consistent dict structure with all expected keys
- **Command Signature**: Fixed `FireWeaponCommand.execute()` to pass distance parameter matching updated `calculate_damage()` signature
- **Test Suite**: Updated all unit tests to match new shield facing system, weapon damage calculations, and controller mock requirements
  - Fixed `test_ship_systems.py` weapon tests to use new 3-parameter signature with distance
  - Updated shield tests to use `total_shield_strength` property and `shield_facings` dictionary
  - Fixed `test_controller.py` mock to include `get_turn_status()` and `turn_manager` attributes
  - Updated `test_entities.py` to use `total_shield_strength` instead of deprecated `shield_strength`

### Changed

- **Configuration System**: Moved all combat-related magic numbers to `game_settings.toml` under `[game.combat]` section
  - Weapon firing arc (270°)
  - Base accuracy (85%)
  - Range penalty factor (40%)
  - Critical hit chance (10%) and multiplier (1.5x)
  - Shield effectiveness vs energy (85%) and kinetic (65%)
  - Shield minimum absorption rate (10%)
  - AI patrol radius (5 cells)
  - AI flee threshold (30% hull)
  - AI enemy cache duration (3 turns)
- **Configuration Loading**: Added class-level config cache in `WeaponSystems` and `ShipAI` to load settings from TOML with fallback defaults
- **Combat Calculations**: Updated all combat calculations to use configuration values instead of hardcoded constants

### Optimized

- **AI Performance**: Added enemy list caching in `ShipAI` to reduce scanning overhead (refreshes every 3 turns by default)
- **Warning Logging**: Added warning log when AI turn safety limit is reached for debugging

### Testing

- **Coverage**: Maintained 80%+ coverage for critical paths (ship_systems: 81.45%, commands: 84.83%, starship: 96.15%)
- **Test Count**: All 292 unit tests passing with updated mock fixtures and test expectations

## [0.0.20] - 2025-10-30

### Added

- **Advanced Weapon Systems**: Complete weapon mechanics implementation
  - Firing arc calculations (270° forward arc by default)
  - Line of sight checking with obstacle detection
  - Range-based accuracy calculations (85% base, reduced by range)
  - Weapon cooldown system (1.0s torpedoes, 0.5s phasers)
  - Hit chance calculation with range penalties
  - Phasers: 15 damage base, 5 cell range, loses 30% damage at max range
  - Torpedoes: 30 damage base, 8 cell range, maintains full damage
  - Fire weapon action costs: 1 AP for phasers, 2 AP for torpedoes

- **Directional Shield System**: Shield facings with positional damage
  - Four shield facings: forward, aft, port, starboard
  - 25 shield points per facing (100 total)
  - Automatic facing determination based on attacker position
  - Damage absorption: 85% for energy, 65% for kinetic
  - Per-facing recharge at 2.0 points per second
  - Shield redistribution system for tactical management
  - Hull damage when shields penetrated

- **Combat Resolution System**: Complete combat mechanics
  - Critical hit system (10% chance, 1.5x damage multiplier)
  - Range modifiers affecting weapon effectiveness
  - Damage reporting with shields absorbed/hull damage breakdown
  - Action point consumption for combat actions
  - Weapon type selection (phasers vs torpedoes)
  - Target validation with range and arc checks
  - Line of sight obstacle checking

- **Advanced Damage System**: Hull and system damage mechanics
  - Shield-first damage absorption with facing system
  - Hull integrity tracking (0-100%)
  - System damage when hull drops below 50%
  - Random system damage on critical hull hits (30% base chance + hull damage factor)
  - System efficiency degradation from damage
  - Ship destruction at 0% hull integrity
  - Damage result reporting with detailed breakdown

- **AI System for NPC Ships**: Simple state machine AI
  - Three AI states: PATROL, ATTACK, FLEE
  - State transitions based on hull damage and enemy presence
  - PATROL: Random movement within patrol radius
  - ATTACK: Move toward and fire at nearest/weakest enemy
  - FLEE: Retreat when hull below 30%, return to patrol when recovered
  - Target selection with distance and hull integrity scoring
  - Sensor range-based enemy detection
  - AI processes automatically during end turn

- **Combat UI Integration**: Target selection and weapon firing
  - Target selection dialog with distance display
  - Weapon type chooser (Phasers 1 AP / Torpedoes 2 AP)
  - Target list showing ship name, class, and range
  - Combat result messages with detailed feedback
  - Fire button opens target selection when enemies in range
  - "No targets in range" message when appropriate
  - Automatic UI updates after combat actions

### Changed

- **WeaponSystems Component** (v0.0.20): Enhanced with advanced combat features
  - Added firing arc, line of sight, and accuracy calculations
  - Implemented cooldown and hit chance systems
  - Range-based damage calculations
  - Obstacle detection for line of sight

- **ShieldSystems Component** (v0.0.20): Directional shield implementation
  - Changed from single shield pool to four directional facings
  - Automatic hit facing determination from attacker position
  - Per-facing recharge and damage absorption
  - Shield redistribution capability

- **Starship Entity** (v0.0.20): Enhanced damage and AI support
  - Updated `take_damage()` with detailed damage result reporting
  - Added `_apply_system_damage()` for critical hull damage
  - Added `ai_controller` attribute for NPC ships
  - Added `is_player` flag to distinguish player ship
  - Added `set_ai_controller()` method

- **GameModel** (v0.0.20): Combat and AI integration
  - Enhanced `resolve_combat()` with complete combat mechanics
  - Added `get_potential_targets()` for weapon range queries
  - Added `_initialize_ai()` to create AI controllers for NPCs
  - Added `process_ai_turn()` for AI decision processing
  - Player ship marked with `is_player=True` flag
  - NPC ships automatically get AI controllers

- **GameController** (v0.0.20): Combat action coordination
  - Enhanced `handle_combat_action()` with full combat flow
  - Added `get_available_targets()` for UI target lists
  - Added `_process_ai_turns()` to handle AI during end turn
  - AI turns process automatically until player's turn
  - Combat UI updates with damage feedback

- **GameView** (v0.0.20): Combat UI implementation
  - Replaced fire button placeholder with full target selection
  - Added weapon type selection dialog
  - Added target list with ship info and range
  - Fixed isometric_grid import path (../engine/)
  - Consolidated Qt imports to eliminate duplicates

### Technical Details

- **File Updates**:
  - `ship_systems.py` (v0.0.20): Advanced weapon and shield systems
  - `starship.py` (v0.0.20): Damage system and AI integration
  - `model.py` (v0.0.20): Combat resolution and AI processing
  - `controller.py` (v0.0.20): Combat coordination and AI turns
  - `view.py` (v0.0.20): Target selection and combat UI
  - `ship_ai.py` (v0.0.20): New AI module for NPC behavior
  - `main.py` (v0.0.20): Version bump
  - `pyproject.toml`: Version bump to 0.0.20

- **New Modules**:
  - `STRR/src/game/ai/`: New AI package
  - `STRR/src/game/ai/ship_ai.py`: ShipAI class with state machine

- **Architecture Pattern**: Maintains clean MVC with added AI layer
  - Model contains pure combat logic and AI processing
  - Controller coordinates combat actions and AI turns
  - View provides combat UI without game logic
  - AI operates on model data without direct view access

- **Combat Mechanics Balance**:
  - Phasers: Fast, cheap, shorter range, better for multiple targets
  - Torpedoes: Slow, expensive, longer range, more damage
  - Shields provide significant protection until depleted
  - Critical hits add tactical excitement
  - Range penalties encourage positioning

### Milestone Progress

**Completed: "Implement Basic Combat System"**

- ✅ Weapon firing mechanics with firing arcs and line of sight
- ✅ Shield and damage calculations with directional facings
- ✅ Combat resolution with positioning and range factors
- ✅ Basic AI for enemy ship behavior (patrol/attack/flee)
- ✅ Target selection UI with weapon type chooser
- ✅ Critical hit system and range modifiers
- ✅ Line of sight and obstruction checking

**Next Milestone: "Implement Resource Management System"**

- Energy allocation system for ship subsystems
- Supplies tracking (fuel, medical, spare parts)
- Crew morale and efficiency systems
- Ship system condition and maintenance

## [0.0.19] - 2025-10-30

### Added

- **Move Mode System**: Interactive ship movement with UI feedback
  - "Move Ship" button toggles move mode on/off
  - Visual feedback: button text changes to "Cancel Move" when active
  - Status messages guide user through move process
  - Mouse click on grid moves ship when mode is active
  - Automatic mode deactivation after movement

- **Combat Action Button Handlers**: Placeholder implementations for future combat features
  - Fire Weapons button with feedback message
  - Scan Target button with feedback message
  - Evasive Maneuvers button with feedback message
  - All buttons provide appropriate "not yet implemented" messages

- **Utility Action Button Handlers**: Placeholder implementations for future features
  - Dock at Station button with feedback message
  - Hail Ship button with feedback message
  - Ready for future milestone implementation

- **Mode Switcher Integration**: Toolbar buttons connected to state machine
  - Galaxy Map mode button (shows "not yet implemented" message)
  - Sector Map mode button (fully functional, transitions to sector state)
  - Combat Mode button (shows "not yet implemented" message)
  - Proper state validation and UI updates on mode changes

- **Real-Time UI Status Updates**: Automatic UI refresh after game state changes
  - New `update_ui_state()` method in GameView
  - Updates ship status (hull, shields, energy) after every action
  - Updates ship position display after movement
  - Updates sector name display from sector coordinates
  - Integrated into all state-changing controller methods

### Changed

- **Zoom Control Integration**: Improved zoom button functionality
  - Toolbar zoom buttons now call proper GridRenderer methods
  - `_on_zoom_in()` uses `grid_renderer.zoom_in()`
  - `_on_zoom_out()` uses `grid_renderer.zoom_out()`
  - `_on_zoom_reset()` uses `grid_renderer.reset_zoom()`
  - Status messages show current zoom level

- **Mouse Click Behavior**: Move mode integration with click handler
  - Controller `handle_mouse_click()` now checks `view.move_mode`
  - Ship only moves on click when move mode is active
  - Automatic feedback and mode reset after successful move
  - Prevents accidental movement from exploration clicks

- **Controller State Management**: Enhanced UI synchronization
  - `handle_ship_move_request()` now calls `update_ui_state()`
  - `start_new_game()` initializes all UI elements
  - `load_game()` refreshes UI after load
  - `end_turn()` updates UI for new turn state

- **Rotation Button**: Clarified placeholder status
  - Shows "Rotation not yet implemented" message
  - Prepared for future orientation system

### Fixed

- **Sector Name Display**: Fixed AttributeError in UI updates
  - SectorMap doesn't have `name` attribute
  - Now generates name from coordinates: "Sector X-Y"
  - Prevents crashes when updating sector label

### Technical Details

- **File Updates**:
  - `view.py` (v0.0.19): Added move mode, updated all button handlers, added `update_ui_state()`
  - `controller.py` (v0.0.19): Added mode switching methods, integrated UI updates
  - `main.py` (v0.0.19): Version bump
  - `pyproject.toml`: Version bump to 0.0.19

- **Architecture Pattern**: Maintains MVC separation
  - View handles UI events and user feedback
  - Controller coordinates between model and view
  - Model contains pure game logic without UI dependencies

- **User Experience**: Improved interaction flow
  - Clear visual feedback for all actions
  - Toggle-based move mode prevents accidental actions
  - Status messages guide user through game features
  - Disabled features clearly communicate future availability

### Milestone Progress

**Completed: "Connect UI to Game Logic"**

- ✅ Wire UI action buttons to controller methods
- ✅ Implement real-time UI updates from game state
- ✅ Add status panel updates when state changes
- ✅ Connect movement actions to ship movement on grid
- ✅ Connect zoom controls to isometric grid view
- ✅ Implement mode switching between states

**Next Milestone: "Implement Basic Combat System"**

- Weapon firing mechanics with visual feedback
- Shield and damage calculations
- Combat resolution with positioning factors
- Basic AI for enemy ship behavior

## [0.0.18] - 2025-10-30

### Added

- **Turn-Based Game Loop System**: Complete implementation of fixed timestep game loop with turn management
  - Initiative-based turn ordering system where entities with higher initiative act first
  - Action point system for all game entities (GameObject base class)
  - `TurnManager` class with comprehensive turn tracking and entity registration
  - Turn phases: input → action → resolution
  - Automatic action point restoration at start of each turn
  - Entity registration/unregistration for combat tracking
  - Turn history and action tracking

- **GameObject Turn Attributes**: Extended base GameObject class with turn-based mechanics
  - `initiative`: Initiative value for turn order (higher acts first)
  - `action_points`: Current available action points
  - `max_action_points`: Maximum action points per turn (default 3)
  - `reset_action_points()`: Restore action points to maximum
  - `spend_action_points(cost)`: Consume action points for actions
  - `has_action_points(cost)`: Check if entity can perform action

- **Enhanced TurnManager**: Comprehensive turn management system
  - Initiative-based entity sorting (highest initiative acts first)
  - Current entity tracking with `get_current_entity()`
  - Turn advancement with `next_entity()` and `advance_turn()`
  - Turn phase management (input, action, resolution)
  - Entity registration system for combat/turn participation
  - Action history tracking for turn replay
  - Get turn info with entity count and remaining actions

- **GameModel Turn Integration**: Turn system integrated into core game logic
  - Player ship gets initiative 10 and 5 action points (acts first, more actions)
  - NPC ships get initiative 6-9 and 3 action points per turn
  - Entity registration with turn manager on game initialization
  - Movement actions now consume action points (1 AP per grid cell minimum)
  - Automatic turn advancement when entity runs out of action points
  - `end_current_turn()`: Manually end current entity's turn
  - `get_turn_status()`: Get comprehensive turn status information

- **Controller Turn Management**: Controller methods for turn handling
  - `end_turn()`: End current entity's turn and advance to next
  - `_update_turn_display()`: Update view with current turn information
  - Turn information updates after movement and turn changes
  - Connected "End Turn" button to controller.end_turn()

- **View Turn Display Updates**: UI integration for turn information
  - Connected End Turn button to controller (was placeholder)
  - `update_turn_info()`: Updates turn number, phase, and action points in UI
  - Turn display updates automatically on game start, load, and turn changes
  - Action points display shows "AP: X" format in turn bar

### Changed

- **Movement System**: Movement now integrated with action point system
  - Movement costs action points (1 AP per grid cell, minimum 1)
  - Movement checks action point availability before execution
  - Movement automatically advances to next entity when action points depleted
  - Failed movements still visible through existing validation

- **Game Initialization**: Turn system activated on new game
  - Player ship registered with turn manager
  - All test ships registered with turn manager with varied initiative
  - First turn automatically started after initialization
  - Turn display updated on game start

### Technical Details

- **File Updates**:
  - `base.py` (v0.0.18): Added turn-based attributes and methods to GameObject
  - `model.py` (v0.0.18): Enhanced TurnManager and integrated turn system
  - `controller.py` (v0.0.18): Added turn management methods
  - `view.py` (v0.0.18): Connected End Turn button and turn display
  - `main.py` (v0.0.18): Version bump
  - `pyproject.toml`: Version bump to 0.0.18

- **Architecture Pattern**: Turn-based system follows MVC separation
  - Model: Pure turn logic and state management
  - View: Turn information display and user input
  - Controller: Coordination between model and view

- **Action Point Costs** (Initial Implementation):
  - Movement: 1 AP per grid cell distance (minimum 1 AP)
  - Other actions: To be defined in future milestones

### Milestone Progress

**Completed: "Implement Turn-Based Game Loop"**

- ✅ Fixed timestep game loop with input → update → render phases
- ✅ Turn counter and action point system
- ✅ Initiative system for multiple entities
- ✅ State persistence between turns
- ✅ Entity registration and turn order management
- ✅ Action point restoration and consumption
- ✅ UI integration with turn display and End Turn button

## [0.0.17] - 2025-10-30

### Changed

- **Updated Development Milestones**: Reorganized milestone tracking in DESIGN.md to reflect current progress
  - Moved "Integrate PySide6 with pygame-ce" from Next to Completed milestones
  - Added comprehensive completion details for PySide6 integration (v0.0.10 and v0.0.16 work)
  - Moved "Turn-Based Game Loop" to In Progress milestones (currently being implemented)
  - Added new "Connect UI to Game Logic" milestone to Next milestones
  - Updated completed milestone descriptions with version numbers and specific features
  - Improved milestone organization to better track development progress

### Documentation

- Updated DESIGN.md milestone sections for accuracy
- Added detailed completion notes for UI integration work
- Reorganized milestone priorities based on current development state

## [0.0.16] - 2025-10-30

### Added

- **Right-Rail Tactical UI Layout**: Implemented comprehensive Qt application window based on Layout Option 2 from DESIGN.md
  - Central game display area with expanding size policy
  - Right dock panel with three tabs (Status, Actions, Map)
  - Bottom turn bar with End Turn button, action points display, phase indicator, and turn counter
  - Top toolbar with mode switcher buttons (Galaxy/Sector/Combat) and zoom controls
  - Menu bar with File and View menus

- **Status Tab**: Complete ship status monitoring interface
  - Ship name display with styled formatting
  - Hull, shields, and energy progress bars with color coding
  - Position display showing X, Y, Z coordinates
  - Sector name display

- **Actions Tab**: Organized action buttons by category
  - Movement group: Move Ship, Rotate buttons
  - Combat group: Fire Weapons, Scan Target, Evasive Maneuvers buttons
  - Utilities group: Dock at Station, Hail Ship buttons

- **Map Tab**: Mini-map and legend placeholder
  - Mini-map display area (250x250) for future implementation
  - Color-coded legend showing player ships, enemy ships, stations, and asteroids

- **Turn Management UI**: Bottom bar for turn-based gameplay
  - End Turn button with styled appearance
  - Action points counter with yellow highlight
  - Current phase indicator with green highlight
  - Turn number display

### Changed

- **Main Window Layout**: Completely redesigned from left-sidebar to right-dock layout
  - Changed from QHBoxLayout with fixed left panel to QVBoxLayout with QDockWidget
  - Game display now uses central widget with expanding size policy
  - Removed old control panel groupbox in favor of dockable tabs

- **GameView Class**: Updated to support new UI structure
  - Added references to all new UI elements (progress bars, toolbar actions, tab widgets)
  - Connected signals for mode switcher, zoom controls, and action buttons
  - Implemented placeholder handlers for all new UI actions
  - Updated `show_ship_status()` to use progress bars instead of text labels
  - Added `update_turn_info()` method for turn bar updates
  - Removed message display in favor of future status bar/dialogs

- **UI Signal Handling**: Expanded signal/slot connections
  - Menu actions: New Game, Save Game, Load Game, Quit
  - Toolbar mode actions: Galaxy, Sector, Combat mode switchers
  - Toolbar zoom actions: Zoom in, out, reset with grid renderer integration
  - Turn action: End Turn button
  - Ship actions: Move, Rotate, Fire, Scan, Evasive, Dock, Hail buttons

### Technical Details

- **File Updates**:
  - `main_window.ui` (new design): Complete UI redesign with right dock, tabs, toolbar, turn bar
  - `view.py` (v0.0.16): Integrated new UI components, added signal handlers
  - `pyproject.toml`: Version bump to 0.0.16

- **UI Components**:
  - QDockWidget for right panel (closable, movable, floatable)
  - QTabWidget with three tabs for organized information display
  - QProgressBar widgets for visual status indicators
  - QToolBar with mode and zoom actions
  - QFormLayout for clean label/value pairs in status display

- **Design Pattern**: Maintains MVC separation
  - View handles UI updates and user input
  - Controller methods called for game logic
  - State machine integration deferred for future implementation

## [0.0.15] - 2025-10-30

### Added

- **Z-Level Distance Indicators**: Added numeric z-level distance display next to ships
  - Ships on different z-levels now show a small number indicating their distance from the active z-level
  - Format: `+N` for ships above active level, `-N` for ships below
  - Positioned in the upper-right corner of the ship entity
  - Yellow-ish text color with semi-transparent black background for visibility
  - Bordered box for clear distinction from other UI elements
  - Provides quick positional context without cluttering the view

### Changed

- **GridRenderer.render_entity()**: Updated to draw z-level distance indicator
  - Automatically displays distance when entity is on a different z-level
  - Uses small font (18pt) to minimize visual clutter
  - Works in conjunction with existing z-level reference lines

### Technical Details

- **File Updates**:
  - `isometric_grid.py` (v0.0.15): Enhanced entity rendering with z-distance display
  - `main.py` (v0.0.15): Version bump
  - `pyproject.toml`: Version bump to 0.0.15

## [0.0.14] - 2025-10-30

### Changed

- **Zoom and Map Centering**: Adjusted initial view for testing purposes
  - Default zoom increased to 2.0x for closer view of the sector map
  - Camera offset recalculated to center the 20x20 grid in 1280x900 pygame window
  - Grid now properly centered at (640, 130) for optimal viewing
  - Map calculates center based on grid dimensions and tile size at zoom level

### Technical Details

- **File Updates**:
  - `isometric_grid.py` (v0.0.14): Updated `create_sector_grid()` function
    - Changed camera_offset from (960, 380) to (640, 130) for 1280x900 window
    - Added `grid.set_zoom(2.0)` call for closer initial view
    - Updated docstring to reflect new centering calculations
  - `main.py` (v0.0.14): Version bump
  - `pyproject.toml`: Version bump to 0.0.14

### Notes

These changes are temporary for testing purposes. The zoom level and camera positioning will be adjusted based on gameplay requirements as development progresses.

## [0.0.13] - 2025-10-30

### Added

- **Z-Level Reference Lines**: Visual aids for ships on non-current z-levels
  - Added vertical dashed lines from ships to their projected position on the active layer
  - Lines use the ship's faction color (semi-transparent) for easy identification
  - Small circle marker at the projection point on the active layer
  - Makes it much easier to understand spatial relationships between z-levels
  - Automatically enabled when ship is on a different z-level than the active layer

### Changed

- **GridRenderer.render_entity()**: Added optional `current_z_level` parameter
  - When provided, automatically draws reference line if entity is on different z-level
  - Maintains backward compatibility (parameter is optional, default None = no line)

- **GameView**: Updated to pass current z-level when rendering entities
  - Reference lines now automatically appear for all ships on non-active layers

### Technical Details

- **New Methods**:
  - `GridRenderer._render_z_reference_line()`: Draws dashed line from entity to active layer
  - Uses existing `_draw_dashed_line()` helper for consistent line rendering
  - Creates GridPosition at entity's x,y but current z-level for projection calculation

- **File Updates**:
  - `isometric_grid.py` (v0.0.13): Added reference line rendering
  - `view.py` (v0.0.13): Pass current_z_level to render_entity
  - `main.py` (v0.0.13): Version bump
  - `pyproject.toml`: Version bump to 0.0.13

- **Test Results**: All 77 tests pass (no regressions)

### User Experience Improvement

This feature significantly improves spatial awareness when viewing ships at different z-levels. Previously, it was difficult to tell where a ship on z-level 2 was in relation to the current z-level 1 grid. Now, a clear reference line shows exactly where that ship would project down to the active layer, making tactical decisions much easier.

## [0.0.12] - 2025-10-30

### Added

- **Starship Visual Representation**: Complete entity rendering system on isometric grid
  - Added `color` and `size` attributes to Starship class for visual differentiation
  - Faction-based color coding: Federation (blue), Klingon (red), Romulan (green), etc.
  - Added `get_orientation_radians()` method for rendering calculations
  - Created `_get_faction_color()` helper method with 7 faction color mappings

- **Orientation Visualization**: Directional indicators showing ship facing
  - White arrow overlay showing ship orientation (0-359 degrees)
  - Arrow dynamically rotates based on ship's facing direction
  - Clear visual distinction between body and orientation indicator

- **GridRenderer Entity Rendering**: New `render_entity()` method
  - Renders entities (starships, stations) at 3D grid positions
  - Draws colored circle body with white outline for visibility
  - Adds orientation arrow (triangle) pointing in facing direction
  - Displays entity name label above with semi-transparent background
  - Proper isometric projection and z-level positioning

- **GameView Entity Integration**: Updated rendering pipeline
  - `_render_game_object()` now uses GridRenderer.render_entity for starships
  - Detects starships by `color` and `size` attributes
  - Fallback rendering for other entity types (stations, etc.)
  - Only renders entities on visible z-levels (current ±1)

- **Test Starships**: Demonstration scenario with multiple ships
  - Added `_add_test_ships()` method to GameModel
  - Creates 4 test ships at different positions and z-levels:
    - IKS Korinar (Klingon) at (8,8,1) facing 45°
    - IRW Valdore (Romulan) at (12,6,2) facing 135°
    - IKS Amar (Klingon) at (10,10,0) facing 270°
    - USS Reliant (Federation) at (7,12,1) facing 180°
  - Demonstrates visual differentiation and orientation indicators

### Changed

- **Starship Constructor**: Added optional `faction` parameter
  - Default faction: "Federation"
  - Updated `_create_player_ship()` to specify Federation faction
  - All ship instantiations now include faction for proper coloring

### Fixed

- Updated all test fixtures to include faction parameter
- Added tests for new functionality:
  - `test_starship_orientation_radians()` - Orientation conversion
  - `test_starship_faction_colors()` - Faction color differentiation

### Technical Details

- **File Updates**:
  - `starship.py` (v0.0.12): Added visual attributes and faction colors
  - `isometric_grid.py` (v0.0.12): Added render_entity() method
  - `view.py` (v0.0.12): Integrated entity rendering
  - `model.py` (v0.0.12): Added test ships and updated player ship creation
  - `main.py` (v0.0.12): Version bump
  - `pyproject.toml`: Version bump to 0.0.12

- **Test Results**: 77 tests pass (2 new tests added)

### Milestone Progress

**Completed: "Implement Basic Starship Entities"**

- ✅ Create foundational game objects that can be placed and rendered on the isometric grid
- ✅ Create visual representation for starships on the isometric grid
- ✅ Implement starship placement at specific grid coordinates and z-levels
- ✅ Add orientation indicators (facing direction visualization)
- ✅ Test rendering multiple starships on the map simultaneously

## [0.0.11] - 2025-10-30

### Changed

- **TOML-Only Configuration**: Removed JSON fallback support from `config_manager.py`
  - Simplified configuration loading to use TOML exclusively
  - All configuration files now use `.toml` format
  - JSON files moved to `backup/json_config_files/` directory
- Updated documentation to reflect TOML-only approach
  - Modified `STRR/assets/data/README.md` to reference TOML format
  - Updated `config_manager_doc.md` to remove JSON fallback information
- Removed `migrate_json_to_toml()` method and `_load_json()` helper from ConfigManager
- Removed `json` import from config_manager.py (no longer needed)

### Fixed

- **Import Path Fixes**: Corrected module import paths for proper package structure
  - Fixed `isometric_grid.py` to use `from src.game.entities.base` instead of `from game.entities.base`
  - Fixed `config_manager.py` to use `from src.game.exceptions` instead of `from game.exceptions`
  - All demo files now import correctly without ModuleNotFoundError
- **Type Hint Improvements**: Added proper type annotations to exception classes
  - Added `-> None` return type hints to `__init__` methods in exceptions.py
  - Added type hints for `**kwargs` parameters: `**kwargs: str | int | float`
  - Improved type safety in InvalidMoveError, CombatError, ConfigurationError, and SaveLoadError
- Configuration system now cleaner and more maintainable without dual format support
- All 75 unit tests pass successfully with 33.28% code coverage
- Verified all TOML configuration files load correctly

## [Unreleased - Previous]

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
- `/docs/CHANGELOG.md` - This file
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
