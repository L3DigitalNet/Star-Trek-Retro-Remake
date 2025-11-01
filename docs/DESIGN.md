# Game Design Document: Star Trek Retro Remake

## Table of Contents

### Milestones

- [In Progress Milestones](#in-progress-milestones)
- [Next Milestones](#next-milestones)
- [Completed Milestones](#completed-milestones)

### Executive Summary

- [1.1 Game Overview](#11-game-overview)
- [1.2 Target Audience](#12-target-audience)
- [1.3 Platform and Technical Requirements](#13-platform-and-technical-requirements)
- [1.4 Competitive Analysis](#14-competitive-analysis)
- [1.5 Key Features](#15-key-features)

### Game Overview

- [2.1 Setting and Theme](#21-setting-and-theme)
- [2.2 Core Player Fantasy](#22-core-player-fantasy)
- [2.3 Player Goals and Motivation](#23-player-goals-and-motivation)
- [2.4 Victory Conditions](#24-victory-conditions)

### Gameplay

- [3.1 Core Gameplay Loop](#31-core-gameplay-loop)
  - [3.1.1 Time Scale](#311-time-scale)
  - [3.1.2 Turn Phases](#312-turn-phases)
- [3.2 Game Modes](#32-game-modes)
- [3.3 Player Progression](#33-player-progression)
- [3.4 Difficulty and Balance](#34-difficulty-and-balance)

### Game World

- [4.1 World Overview](#41-world-overview)
- [4.2 Galaxy Map](#42-galaxy-map)
- [4.3 Sector Map](#43-sector-map)
- [4.4 Locations and Environments](#44-locations-and-environments)
- [4.5 Factions and NPCs](#45-factions-and-npcs)

### Game Mechanics

- [5.1 Starships](#51-starships)
- [5.2 Combat System](#52-combat-system)
- [5.3 Resource Management](#53-resource-management)
- [5.4 Mission System](#54-mission-system)
- [5.5 Economy and Trading](#55-economy-and-trading)
- [5.6 AI and NPCs](#56-ai-and-npcs)

### User Interface and User Experience

- [6.1 UI Design Philosophy](#61-ui-design-philosophy)
- [6.2 Interface Layout](#62-interface-layout)
- [6.3 Input Controls](#63-input-controls)
- [6.4 Accessibility](#64-accessibility)

### Audio and Visual Design

- [7.1 Art Style](#71-art-style)
- [7.2 Audio Design](#72-audio-design)
- [7.3 Visual Effects](#73-visual-effects)

### Narrative and Storytelling

- [8.1 Story Overview](#81-story-overview)
- [8.2 Characters](#82-characters)
- [8.3 Dialogue System](#83-dialogue-system)
- [8.4 Cutscenes and Presentation](#84-cutscenes-and-presentation)

### Technical Requirements

- [9.1 Technical Architecture](#91-technical-architecture)
- [9.2 Platform Requirements](#92-platform-requirements)
- [9.3 Performance Requirements](#93-performance-requirements)
- [9.4 Data Management](#94-data-management)
- [9.5 Localization](#95-localization)

### Production

- [10.1 Development Milestones](#101-development-milestones)
- [10.2 Team Structure](#102-team-structure)
- [10.3 Testing Strategy](#103-testing-strategy)
- [10.4 Risk Assessment](#104-risk-assessment)
- [10.5 Resource Requirements](#105-resource-requirements)

### Marketing and Business

- [11.1 Marketing Strategy](#111-marketing-strategy)
- [11.2 Monetization Model](#112-monetization-model)
- [11.3 Community and Support](#113-community-and-support)
- [11.4 Post-Launch Content](#114-post-launch-content)

### Legal and Compliance

- [12.1 Intellectual Property](#121-intellectual-property)
- [12.2 Privacy and Data Protection](#122-privacy-and-data-protection)
- [12.3 Content Rating Considerations](#123-content-rating-considerations)
- [12.4 Platform Compliance](#124-platform-compliance)

### Future Development

- [13.1 Post-Launch Features (v1.1+)](#131-post-launch-features-v11)
- [13.2 Long-term Vision (v2.0+)](#132-long-term-vision-v20)

### Additional Resources

- [Appendix A: Reference Materials](#appendix-a-reference-materials)
- [Appendix B: Glossary](#appendix-b-glossary)
- [Appendix C: Change Log](#appendix-c-change-log)
- [Appendix D: Credits and Acknowledgments](#appendix-d-credits-and-acknowledgments)

---

## Milestones

### Current Project Status (v0.0.25 - October 31, 2025)

**Project Phase:** Core Systems Implementation (Pre-Alpha)

**Recently Completed:**

- Dialog and Menu Systems - Mission and Settings Dialogs (v0.0.25)
  - Mission briefing, selection, and tracking dialogs
  - Comprehensive settings dialog with TOML integration
- Mission System Foundation (v0.0.24)
  - Complete mission lifecycle management with 6 mission types
  - TOML-based mission templates and rewards system
- Resource Management System (v0.0.22)
  - Energy allocation, supplies tracking, crew morale
- Performance Optimization and Configuration (v0.0.21)
- Basic Combat System with AI (v0.0.20)

**Current Focus:** Completing Dialog and Menu Systems (Priority 2)

**Next Major Goals:**

- Ship Status Panel implementation
- Save/Load Dialog System
- Galaxy Map Mode (Priority 3)

### In Progress Milestones

#### Implement Dialog and Menu Systems (Priority 2)

**Status:** Partial Implementation (v0.0.25 - Mission and Settings Dialogs Complete)

**✅ Completed Components (v0.0.25):**

**Mission Dialogs:**

- ✅ MissionBriefingDialog: Display mission details with accept/decline options
- ✅ MissionSelectionDialog: Browse and select from available missions at starbases
- ✅ MissionTrackerWidget: Real-time display of active missions and objective progress
- ✅ ObjectiveProgressBar: Visual progress indicators for mission objectives
- ✅ Mission reward display (reputation, supplies, spare parts)
- ✅ Mission difficulty indicators and risk assessment
- ✅ Mission objective progress tracking with automatic completion

**Settings Dialog:**

- ✅ SettingsDialog: Tabbed interface with Graphics, Audio, Gameplay, and KeyBindings tabs
- ✅ GraphicsTab: Resolution, fullscreen, VSync, FPS limit configuration
- ✅ AudioTab: Master volume, music volume, effects volume sliders
- ✅ GameplayTab: Difficulty, auto-save interval, tutorial hints, grid display toggles
- ✅ KeyBindingsTab: Customizable key bindings with conflict detection
- ✅ TOML integration: Load from and save to `game_settings.toml`
- ✅ Settings validation and error handling
- ✅ Apply and Cancel button functionality

**🔲 Remaining Components:**

**Ship Status Panel:**

- Detailed system health display (shields, weapons, engines, sensors, life support)
- Crew roster and assignment interface
  - Initial crew: Captain, First Officer, Chief Engineer, Science Officer, Security Chief, Helm Officer
  - Crew health and efficiency display
  - Crew assignment optimization suggestions
- Damage reports with repair priority recommendations
- Resource consumption tracking and alerts
- Real-time status updates during gameplay

**Save/Load Game System:**

- Game state serialization to TOML format
- Load saved games with complete state restoration
- Multiple save slot management (5 manual + 1 auto-save)
- Save game metadata (timestamp, turn count, sector, mission status)
- Save file validation and corruption recovery
- Auto-save functionality with configurable interval

### Next Milestones

#### Implement Galaxy Map Mode (Priority 3)

**Status:** Design Phase

**Galaxy Map Features:**

- Galaxy map grid rendering (10x10 sectors = 100 total sectors)
- Isometric grid visualization adapted from sector map
- Sector navigation and selection with mouse interaction
- Federation, Neutral, and Hostile zone color-coded visualization
- Current sector highlight and path preview

**Sector Information Display:**

- Sector name and coordinates (A1-J10 format)
- Control status (Federation, Neutral, Klingon, Romulan, Gorn, Uncharted)
- Threat level indicator (1-5 scale)
- Known starbase locations marked
- Anomaly and mission icons

**Travel Mechanics:**

- Travel time calculation based on warp speed and distance
- Energy consumption for warp travel (configurable)
- Random encounter system during travel
  - Encounter probability based on threat level
  - Types: hostile ships, distress calls, anomalies, traders
- Transition from Galaxy to Sector map with state preservation

**UI Integration:**

- Galaxy map button in mode switcher toolbar
- Sector information panel in right dock
- Travel route planning with waypoints
- Auto-travel option with interrupt on encounters

#### Implement Sector Map Environmental Objects (Priority 4)

**Status:** Concept Phase

**Space Stations (Starbases):**

- Multiple starbase types (Federation, trading post, repair depot)
- Docking mechanics (simple request action, costs 1 turn)
- Repair and resupply services
  - Free full repairs and resupply at Federation starbases
  - Paid services at neutral trading posts
- Mission briefing and assignment hub
- Crew shore leave and morale boost

**Environmental Hazards:**

- **Asteroids**: Provide cover (+20% defense), collision damage (10 hull)
- **Nebulae**: Sensor interference (-50% range), movement penalty (+1 AP per move)
- **Debris Fields**: Navigation hazards, random damage on entry (5-15 hull)
- **Ion Storms**: Shield disruption, communication jamming
- **Gravity Wells**: Movement cost increase, escape difficulty

**Sensor System Enhancement:**

- Short-range sensors (5 grid cells, standard accuracy)
- Long-range sensors (15 grid cells, reduced accuracy)
- Active scan action (costs 1 AP, reveals detailed info)
- Passive detection (automatic, limited range)
- Sensor interference calculation from environment
- Cloaked ship detection mechanics (future feature)

**Object Interaction:**

- Mining asteroids for resources (future feature)
- Salvaging debris for spare parts
- Scientific analysis of anomalies
- Environmental damage to ship systems

### Completed Milestones

#### Implement Dialog and Menu Systems - Phase 1 (v0.0.25)

**Mission Dialog Components:**

- ✅ MissionBriefingDialog (PySide6 QDialog)
  - Display mission details with formatted objectives
  - Accept/decline buttons with confirmation
  - Mission reward display (reputation, supplies, spare parts)
  - Mission difficulty indicators (1-5 scale with color coding)
  - Estimated completion time and sector location
  - Mission type icons and status indicators
- ✅ MissionSelectionDialog (PySide6 QDialog)
  - Browse available missions at starbases
  - List view with mission name, type, difficulty, rewards
  - Filter missions by type and difficulty
  - Select mission and view detailed briefing
  - Integration with MissionManager for mission availability
- ✅ MissionTrackerWidget (PySide6 QWidget)
  - Real-time display of active missions
  - Collapsible mission cards with objective progress
  - ObjectiveProgressBar for visual progress indication
  - Mission completion status and rewards earned
  - Integration with mission system for automatic updates
- ✅ ObjectiveProgressBar (Custom QProgressBar)
  - Visual progress indicators for mission objectives
  - Color-coded progress (blue = in progress, green = complete)
  - Percentage display with current/target values

**Settings Dialog Components:**

- ✅ SettingsDialog (PySide6 QDialog with QTabWidget)
  - Tabbed interface for organized settings management
  - Apply and Cancel buttons with validation
  - TOML integration for persistent settings
- ✅ GraphicsTab
  - Resolution selection (multiple presets + custom)
  - Fullscreen toggle
  - VSync toggle
  - FPS limit configuration (30/60/144 FPS)
  - Grid display options
- ✅ AudioTab
  - Master volume slider (0-100%)
  - Music volume slider (0-100%)
  - Sound effects volume slider (0-100%)
  - Mute toggles for each audio channel
- ✅ GameplayTab
  - Difficulty selection (Easy/Normal/Hard)
  - Auto-save interval configuration (1-10 turns)
  - Tutorial hints toggle
  - Grid coordinate display toggle
- ✅ KeyBindingsTab
  - Customizable key bindings for all game actions
  - Conflict detection and validation
  - Reset to defaults option
  - Key capture for easy rebinding

**Features Implemented:**

- Complete mission dialog system with PySide6 integration
- Settings management with TOML persistence
- Mission tracking UI with real-time updates
- Visual progress indicators for objectives
- Comprehensive settings validation and error handling
- Qt signal/slot architecture for event handling
- Integration with existing mission_manager and config systems

**Documentation:**

- mission_dialogs_doc.md with API reference and usage examples
- Updated DESIGN.md with completed features
- Code documentation with type hints and docstrings

**Next Steps:**

- Ship Status Panel implementation
- Save/Load Dialog System
- Integration testing for dialog interactions

#### Implement Mission System Foundation (v0.0.24)

- ✅ Mission data structures and TOML schema
  - MissionType enum (PATROL, COMBAT, ESCORT, RESCUE, DIPLOMATIC, SURVEY)
  - MissionStatus enum (AVAILABLE, ACTIVE, COMPLETED, FAILED)
  - MissionObjective with progress tracking and auto-completion
  - MissionReward with reputation, supplies, spare parts, experience
  - Mission class with complete lifecycle management
- ✅ Mission templates system
  - TOML-based mission definitions in `mission_templates.toml`
  - Six mission types with unique objectives and rewards
  - Configurable base rewards and objective targets
  - Dynamic mission generation from templates
- ✅ MissionManager component
  - Mission lifecycle tracking (available, active, completed, failed)
  - Accept, abandon, and complete mission operations
  - Difficulty-based reward scaling (rewards × difficulty)
  - Sector-based mission filtering
  - Active mission count and status tracking
  - Turn-based mission updates with auto-completion
- ✅ GameModel integration
  - Mission system initialized with templates on startup
  - `update_missions()` method for turn-based updates
  - Mission rewards applied to player ship resources
  - Support for multiple active missions
- ✅ Comprehensive testing
  - 18 unit tests with 100% pass rate
  - Tests for mission lifecycle, objectives, rewards, manager operations
  - AAA pattern test structure
  - Fixture-based temporary TOML file testing

Features implemented:

- Complete mission system architecture with type safety
- Mission templates for all six mission types
- Dynamic mission generation with difficulty scaling
- Mission objective progress tracking
- Reward distribution system
- Integration with GameModel turn system
- Comprehensive API documentation
- Full test coverage for mission operations

Next steps for mission system:

- Mission briefing dialog (PySide6) - Priority 2
- Mission selection UI at starbases
- Mission objective tracker in UI status panel
- Reputation system integration

#### Implement Resource Management System (v0.0.22)

- ✅ Energy allocation system
  - Power distribution sliders for shields, weapons, engines, sensors, life support
  - Configurable energy consumption per action (move: 10, fire phaser: 15, fire torpedo: 25, scan: 5, shield regen: 20)
  - Energy regeneration from engines (10/sec base, affected by engine power allocation)
  - Energy capacity (1000) with regeneration affected by system efficiency
- ✅ Supplies tracking
  - Medical supplies (100 starting) for crew health
  - Spare parts (50 starting) for repairs
  - Consumption tracking for maintenance and repairs
  - Resupply at starbases restores to full capacity
- ✅ Crew morale and efficiency systems
  - Morale (0-100) affected by combat outcomes, casualties, time since starbase
  - Efficiency bonuses: high morale (>80) = 1.2x, normal (60-80) = 1.0x, low (<40) = 0.8x
  - Victory bonus (+5), defeat penalty (-10), casualty penalty (-5)
  - Morale degradation over time away from starbase (-0.5 per turn after 10 turns)
  - Starbase visit bonus (+20 morale) with counter resets
- ✅ Ship system condition and maintenance
  - Repair costs based on damage amount (10 spare parts per 0.1 efficiency)
  - Repair effectiveness multiplied by crew efficiency
  - System efficiency tracking with damage accumulation
  - Starbase repairs restore all systems and hull to 100%
- ✅ Space station services
  - Docking mechanics for starbase access
  - Free repairs to full capacity at friendly starbases
  - Refuel and resupply services
  - Crew morale boost on starbase visits

Features implemented:

- ResourceManager component with energy, fuel, and supplies tracking
- CrewManager component with morale and efficiency system
- Power distribution between ship systems
- Configurable resource parameters in game_settings.toml
- Integration with Starship entity for resource-aware operations
- Space station service mechanics for repairs, refuel, and resupply
- 35 comprehensive unit tests with 100% pass rate
- Crew roster with key positions (Captain, First Officer, Chief Engineer, Science Officer, Security Chief, Helm Officer)

#### Performance and Configuration System Optimization (v0.0.21)

- ✅ Configuration System Improvements
  - Moved all combat-related magic numbers to `game_settings.toml`
  - Implemented class-level configuration caching for performance
  - Added configurable combat parameters (firing arc, accuracy, range penalties, critical hits)
  - Added AI behavior configuration (patrol radius, flee threshold, enemy cache duration)
- ✅ Combat System Optimization
  - Added enemy list caching in `ShipAI` to reduce scanning overhead
  - Fixed division by zero guards in weapon calculations
  - Improved AI turn loop scaling based on entity count
  - Enhanced shield effectiveness calculations with minimum absorption
- ✅ Test Suite Maintenance
  - Updated all 292 unit tests to match new systems
  - Maintained 80%+ coverage for critical paths
  - Fixed mock fixtures and test expectations
  - Ensured type consistency across damage calculations
- ✅ Safety and Debugging Improvements
  - Added warning logging for AI turn safety limits
  - Implemented dynamic safety scaling for large battle scenarios
  - Enhanced error handling for edge cases in combat

#### Implement Basic Combat System (v0.0.20)

- ✅ Weapon firing mechanics with firing arcs and line of sight
  - 270° forward firing arc for all weapons
  - Line of sight checking with obstacle detection
  - Range-based accuracy (85% base, reduced by distance)
  - Weapon cooldown system (1.0s torpedoes, 0.5s phasers)
- ✅ Shield and damage calculations with directional facings
  - Four shield facings (forward, aft, port, starboard)
  - 25 shield points per facing (100 total)
  - Automatic facing determination based on attacker position
  - 85% absorption for energy, 65% for kinetic damage
- ✅ Combat resolution with positioning and orientation factors
  - Critical hit system (10% chance, 1.5x damage)
  - Range modifiers for weapon effectiveness
  - Action point costs (1 AP phasers, 2 AP torpedoes)
  - Line of sight and obstruction checking
- ✅ Basic AI for enemy ship behavior
  - Simple state machine (PATROL, ATTACK, FLEE)
  - Target selection with distance and hull scoring
  - Automatic AI processing during end turn
  - Flee behavior at 30% hull integrity
- ✅ Target selection UI with weapon chooser
  - Target list with ship name, class, and range
  - Weapon type selection (Phasers/Torpedoes)
  - Combat feedback messages
  - "No targets in range" handling

Features implemented:

- Advanced WeaponSystems with firing arcs, line of sight, accuracy
- Directional ShieldSystems with four facings
- Combat resolution with critical hits and range modifiers
- Hull and system damage with degradation
- AI state machine for NPC ships (patrol, attack, flee)
- Target selection dialog with weapon chooser
- Complete combat flow from targeting to damage resolution
- AI automatic processing during turn advancement

#### Connect UI to Game Logic (v0.0.19)

- ✅ Wire UI action buttons to controller methods for ship commands
- ✅ Implement real-time UI updates from game state (hull, shields, energy, position)
- ✅ Add status panel updates when game state changes
- ✅ Connect movement actions to ship movement on grid (move mode toggle)
- ✅ Connect zoom controls to isometric grid view (toolbar buttons)
- ✅ Implement mode switching between Galaxy/Sector/Combat states
- Features implemented:
  - Move mode system with toggle button (Move Ship / Cancel Move)
  - Automatic UI state updates after all game actions
  - Combat action button handlers (Fire, Scan, Evasive) with placeholders
  - Utility action button handlers (Dock, Hail) with placeholders
  - Mode switcher buttons fully connected to state machine
  - Real-time status panel updates (ship name, hull, shields, energy, position)
  - Sector name display from coordinates
  - User feedback messages for all actions
  - Zoom controls integrated with proper GridRenderer methods

#### Implement Turn-Based Game Loop (v0.0.18)

- ✅ Fixed timestep game loop with input → update → render phases
- ✅ Turn counter and action point system
- ✅ Initiative system for multiple entities (higher initiative acts first)
- ✅ State persistence between turns
- ✅ Entity registration and turn order management
- ✅ Action point restoration and consumption
- ✅ UI integration with turn display and End Turn button
- ✅ Movement integrated with action point system (1 AP per grid cell)
- Features implemented:
  - GameObject base class with initiative and action point attributes
  - TurnManager with initiative-based sorting and turn advancement
  - Player ship gets 5 action points and initiative 10
  - NPC ships get 3 action points and initiative 6-9
  - Turn phases: input → action → resolution
  - Automatic turn advancement when action points depleted
  - Turn information display in UI (turn number, phase, action points)

#### Basic Map Rendering with Z-Level Support (v0.0.3-v0.0.15)

- Implemented grid-based isometric rendering with multi-layer z-level support
- Features include:
  - Isometric projection with 3D coordinates (x, y, z)
  - Multiple z-level visualization with transparency
  - Grid line rendering with dashed patterns based on z-level distance
  - Camera offset and zoom capabilities (0.25x to 4.0x)
  - Cell highlighting and selection
  - Grid bounds checking and validation
  - Mouse click-to-select and click-to-move functionality
  - Z-level switching via PageUp/PageDown keys
  - Camera panning with arrow keys

#### Basic Starship Entities (v0.0.12)

- Created foundational game objects that can be placed and rendered on the isometric grid
- **Completed Steps:**
  1. ✅ GameObject base class with position and active state
  2. ✅ Starship class with basic attributes (hull, shields, orientation)
  3. ✅ Component pattern for ship systems (WeaponSystems, ShieldSystems, EngineSystems, SensorSystems)
  4. ✅ Visual representation for starships on the isometric grid
  5. ✅ Starship placement at specific grid coordinates and z-levels
  6. ✅ Orientation indicators (facing direction visualization with arrow)
  7. ✅ Multiple starships rendered simultaneously on the map
  8. ✅ Faction-based color coding (Federation blue, Klingon red, Romulan green, etc.)

#### Z-Level Visualization Enhancements (v0.0.13-v0.0.15)

- **Z-Level Reference Lines** (v0.0.13):
  - Vertical dashed lines from ships to their projected position on the active layer
  - Lines use ship's faction color (semi-transparent)
  - Small circle marker at projection point
  - Helps understand spatial relationships between z-levels

- **Z-Level Distance Indicators** (v0.0.15):
  - Numeric display showing distance from active z-level
  - Format: `+N` (above) or `-N` (below)
  - Positioned in upper-right corner of ship entity
  - Yellow text with semi-transparent background
  - Provides quick positional context

#### Integrated PySide6 with pygame-ce (v0.0.10, v0.0.16, v0.0.18)

- ✅ Embed pygame-ce rendering surface within PySide6 main window (v0.0.10)
- ✅ Implement MVC separation (game logic independent of UI)
- ✅ Create comprehensive UI layout with Right-Rail Tactical design (v0.0.16):
  - Central game display area (1280x900) with expanding size policy
  - Right dock panel with three tabs (Status, Actions, Map)
  - Bottom turn bar with End Turn button and game state indicators
  - Top toolbar with mode switcher (Galaxy/Sector/Combat) and zoom controls
  - Menu bar with File and View menus
- ✅ Add status panels showing ship hull, shields, energy, position
- ✅ Add organized action buttons (Movement, Combat, Utilities groups)
- ✅ Implement mini-map placeholder and legend for future navigation
- ✅ Connect UI signals to working handler methods (v0.0.18)
- ✅ Professional windowed interface with proper Qt widgets
- ✅ End Turn button connected to turn management system (v0.0.18)
- ✅ Turn display shows turn number, phase, and action points (v0.0.18)

#### Basic Starship Movement System (v0.0.3-v0.0.18)

- ✅ Enable starships to move across the grid with turn-based mechanics
- ✅ Vector-based movement system with orientation tracking
- ✅ Orientation indicators showing starship facing direction
- ✅ 45-degree orientation system for X, Y, and Z axes
- ✅ Diagonal movement support (up-right, down-left, etc.)
- ✅ Movement cost calculations based on the Pythagorean theorem
- ✅ Distance-based and environment-aware movement costs
- ✅ Movement integrated with action point system (v0.0.18)
- ✅ Click-to-move functionality from UI (v0.0.3)
- ✅ Automatic turn advancement when movement depletes action points (v0.0.18)

## CRITICAL TODO LIST

### High Priority Architecture Issues

- [x] **Hybrid Architecture Specification** - Define State Machine + Game Object + Component pattern implementation
  - Game State Machine for mode transitions (Galaxy/Sector/Combat)
  - Game Object Pattern for entities with natural hierarchies
  - Component Pattern for ship systems (simplified from full ECS)
  - MVC Pattern for UI separation and testability

- [ ] **Game State Machine Definition** - Expand game modes section with detailed state management
  - Define state transitions: Main Menu → Galaxy Map → Sector Map → Combat → Mission Briefing → Settings
  - Specify transition triggers and validation rules
  - Add state persistence and error handling strategies

- [ ] **Object Pooling Strategy** - Detail memory management for turn-based gameplay
  - Define entity pools for starships, projectiles, and effects
  - Specify component pooling for reusable game elements
  - Document resource management and garbage collection strategies

### Medium Priority System Design

- [ ] **Combat System Consolidation** - Merge scattered combat mechanics into cohesive system
  - Define turn structure: Initiative → Action → Resolution → Status phases
  - Specify tactical grid integration (15x15 with 3-5 z-levels)
  - Document environmental factors and victory conditions

- [ ] **Resource Management Enhancement** - Define resource interdependencies and relationships
  - Specify primary resources: Energy, Supplies, Crew Morale, Ship Integrity
  - Document resource consumption and regeneration mechanics
  - Define how resources affect ship systems and combat performance

- [ ] **Testing Strategy Alignment** - Expand testing approach to match project guidelines
  - Define pytest framework usage for core logic testing
  - Specify integration testing for PySide6/pygame-ce interaction
  - Document AI testing and performance benchmarking

### Low Priority Improvements

- [ ] **Version Management Strategy** - Create clear version progression plan
  - Define milestone features for v0.1.0 through v1.0.0
  - Specify feature scope for each release
  - Document error handling timeline (deferred until v1.0.0)

- [ ] **Data Management Specification** - Detail save/load and configuration systems
  - Specify JSON structure for game saves and settings
  - Define asset organization and folder structure
  - Plan for future mod support architecture

- [ ] **Performance Benchmarks** - Set concrete performance targets
  - Define frame rate requirements (60 FPS UI, 30 FPS minimum game view)
  - Specify memory usage limits (512MB maximum for base assets)
  - Set load time targets (2s sector transitions, 1s combat initialization)
  - Implement parallel processing strategies for AI and rendering

### Content Organization

- [ ] **Remove Duplicate Content** - Consolidate overlapping sections 4.4 and 4.5
- [ ] **Expand Faction Descriptions** - Add gameplay characteristics for each faction
- [ ] **Add UI Layout Diagrams** - Include simple ASCII mockups for key interfaces
- [ ] **Create Controls Reference** - Document planned keyboard shortcuts and mouse interactions

---

## 1. Executive Summary

### 1.1 Game Overview

A turn-based and grid-based strategy game set in the Star Trek universe and inspired by classic Star Trek games Star Trek (1971) and Super Star Trek (1973). The player commands a starship, exploring space, completing missions, and engaging in tactical combat with enemy ships.

### 1.2 Target Audience

Star Trek fans, strategy game enthusiasts, and players who enjoy turn-based tactical combat and space exploration games. Especially those who appreciate retro-style games and classic sci-fi settings.

### 1.3 Platform and Technical Requirements

- **Linux Only**: PC (Linux exclusively - no Windows or macOS support planned)
- Developed using Python 3.14+ with pygame-ce (Community Edition) for game engine and PySide6 for UI

### 1.4 Competitive Analysis

Competitors include classic Star Trek games, modern space strategy games, and turn-based tactical games. The game aims to differentiate itself through its faithful representation of the Star Trek universe, grid-based exploration with z-levels, and a focus on tactical combat and resource management.

### 1.5 Key Features

- Turn-based tactical combat
- Grid-based space exploration with 3D z-levels
- Resource management and ship customization
- Classic Star Trek setting (Kirk-era 23rd century)
- Multiple gameplay modes (Galaxy, Sector, Combat)

## 2. Game Overview

### 2.1 Setting and Theme

The game is set in the Kirk-era 23rd century within the Star Trek universe. The player takes on the role of a starship captain, exploring uncharted space, encountering alien species, and upholding the principles of the United Federation of Planets. The theme emphasizes exploration, diplomacy, and tactical combat.

### 2.2 Core Player Fantasy

As a starship captain in the Star Trek universe, the player experiences the thrill of exploration, the challenge of tactical combat, and the responsibility of leadership. The fantasy involves commanding a starship, making strategic decisions, and interacting with diverse alien species.

### 2.3 Player Goals and Motivation

Players are motivated by the desire to explore new worlds, engage in tactical battles, and build their reputation within the Star Trek universe.

**Primary Motivations:**

- **Exploration**: Discover new sectors, anomalies, and uncharted space
- **Tactical Mastery**: Perfect combat strategies and ship management
- **Resource Optimization**: Efficiently manage energy, supplies, and crew morale
- **Faction Relations**: Build reputation with Federation allies and navigate diplomatic challenges

**Short-term Goals:**

- Complete assigned missions successfully
- Defeat enemy ships in tactical combat
- Maintain ship systems and crew morale
- Explore and chart new sectors
- Gather resources and supplies at starbases

**Long-term Goals:**

- Unlock advanced ship classes and upgrades
- Build maximum reputation with Federation Command
- Expand the borders of Federation space through diplomacy or conquest
- Defend against major threats to the Federation (Klingons, Romulans, Gorn, primarily)

### 2.4 Victory Conditions

- Star Trek Retro Remake can largely be considered an open-ended game with no strict win condition, as players can continue exploring and completing missions indefinitely.
- Success conditions can be defined for individual missions or campaigns.
- The game will naturally feel resolved as players achieve significant milestones, such as reaching maximum reputation rank or completing all story missions.
- Post-release planned features will extend playability with additional goals, game mechanics, and unique game modes.

Instead of victory conditions, the game will focus on success metrics for missions and campaigns:

- **Mission Success:** Complete primary objectives, optional secondaries for bonuses, meet casualty/resource thresholds, respect time limits.

- **Combat Success:** Defeat/force retreat of enemy ships, protect allied vessels, survive ambushes with minimal damage.

- **Exploration Success:** Chart 100% sector territory, discover all anomalies, establish first contact, gather complete scientific data.

- **Failure Conditions:** Ship destroyed without respawn, critical mission failure/court-martial, "Disgraced" reputation, desertion during critical missions.

## 3. Gameplay

### 3.1 Core Gameplay Loop

The game operates on a turn-based system where a certain number of actions can be taken each turn based on ship capabilities, resources, and other factors.

#### 3.1.1 Time Scale

Each turn represents a fixed time interval in the game world:

- Minutes in combat
- Hours during sector map exploration
- Days or weeks during galaxy map navigation

#### 3.1.2 Turn Phases

**Combat Mode:**

- Player input phase: The player issues commands to their starship (movement, attacks, resource management)
- NPC phase: Enemy ships and other entities execute their actions based on AI behavior
- Resolution phase: The game processes all actions, updates the game state, and renders the new state

**Sector Map Mode:**

- Player input phase: The player can move their starship, interact with objects, and manage resources
- Event phase: Random events or scripted encounters may occur
- Resolution phase: The game updates the game state based on player actions and events

**Galaxy Map Mode:**

- Player input phase: The player can navigate between sectors, manage resources, and plan missions
- Event phase: Random events or scripted encounters may occur
- Resolution phase: The game updates the game state based on player actions and events

### 3.2 Game Modes

- **Galaxy Map Mode**: Navigate between sectors, manage resources, and plan missions
- **Sector Map Mode**: Explore individual sectors, encounter events, interact with starbases, and engage in tactical combat
- **Combat Mode**: Tactical turn-based combat between starships on a separate combat map

### 3.3 Player Progression

#### Captain Experience System

**Experience Points (XP):**

- Earned through combat victories, mission completion, and exploration
- Required XP scales exponentially: Level N requires N * 100 XP

**Captain Levels:**

- Level 1-5: Junior Captain (starting experience)
- Level 6-10: Captain (competent command)
- Level 11-15: Senior Captain (veteran status)
- Level 16-20: Commodore (multi-ship authority)
- **Level capped** at 20 for initial release
- Planned future expansion: Level 21+: Admiral (fleet command capability)

**Captain Skills:**

- **Command**: +5% crew efficiency per level
  - Improves overall ship performance and crew morale
- **Tactical**: +2% weapon accuracy per level
  - Improves hit and evasion chances in combat
- **Science**: +10% sensor range per level
  - Improves detection of enemy ships and anomalies
- **Engineering**: +5% repair speed per level
  - Reduces time and resource cost for repairs
- **Diplomacy**: +5% reputation gain per level
  - Gives increased success chance on diplomatic missions

Skills may also unlock special abilities or dialog options during missions.

#### Crew Experience System

**Crew Member Levels:**

- Each crew position (First Officer, Chief Engineer, etc.) levels independently
- Crew gains XP from successful actions and survived encounters
- Level 1-10 progression for each crew member

**Crew Benefits:**

- Level 5: Unlock special ability for that station
- Level 8: Reduce action point costs for station actions
- Level 10: Unlock elite bonus (unique per station)

**Crew Specializations:**

- First Officer: +1 AP pool at level 5
- Chief Engineer: Emergency repairs (2 AP) at level 5
- Security Chief: +5% accuracy at level 5
- Science Officer: Enemy ship analysis at level 5
- Helm Officer: -1 AP movement cost at level 8

#### Reputation System

**Starfleet Command Reputation:**

- Rank 1: Probationary (starting status)
- Rank 2: Officer in Good Standing
- Rank 3: Commended Officer
- Rank 4: Distinguished Service
- Rank 5: Exemplary Record

**Reputation Effects:**

- Higher ranks unlock better missions and additional mission options
- Increased resource allocation from starbases
- Access to advanced ship upgrades
- Increased chance of random positive events during diplomatic encounters

**Reputation Gains/Losses:**

- Mission success: +10 to +50 reputation
- Mission failure: -20 to -100 reputation
- Civilian casualties: -50 reputation
- Destroying allied ships: -200 reputation
- Heroic actions: +100 reputation

#### Starship Upgrades

**Upgrade Categories:**

- Weapons Systems (increased damage, reduced cooldown)
  - Phaser Arrays (increased damage, recharge, effective range, and firing arc)
  - Photon Torpedoes (increased damage, range, and hit chance)
- Shield Systems (increased capacity, faster recharge)
- Engine Systems (increased speed, reduced AP cost)
  - Warp drive (increased travel speed on the galaxy map)
  - Impulse engines (increased movement speed on the sector map)
  - Maneuvering thrusters (improved turning and evasion in combat)
- Sensor Systems
  - Short-range sensors (improved detection in sector map and increased hit chance in combat)
  - Long-range sensors (improved detection in sector map and galaxy map)
- Hull Reinforcements (increased hull integrity at the expense of ship mass resulting in decreased fuel efficiency, speed, and maneuverability)
- Crew Quarters (improved crew morale and efficiency)
- Life Support Systems (increased supplies capacity and reduced consumption rates)
- Deflector arrays (resistance to certain environmental hazards, increased speeds through nebulae and asteroid fields)
- Probes (improved exploration capabilities and anomaly detection)

In addition to the listed effects certain upgrades may unlock special abilities or actions during combat or missions.

**Upgrade Tiers:**

- Tier 1: Standard Equipment (starting level)
- Tier 2: Enhanced Systems (+20% effectiveness)
- Tier 3: Advanced Systems (+40% effectiveness)
- Tier 4: Elite Systems (+60% effectiveness)

**Upgrade Acquisition:**

- Purchase at starbases using resources
- Earn through mission rewards
- Salvage from defeated enemy ships
- Unlock through reputation milestones

### 3.4 Difficulty and Balance

#### Difficulty Levels

- **Cadet Mode**: For new players learning the game
  - Reduced enemy ship stats (-25% hull/shields)
  - More generous resource regeneration (+50%)
  - Extended action point pool (+2 AP per turn)
  - Clearer tactical hints and warnings

- **Officer Mode**: Standard balanced gameplay
  - Default enemy and resource values
  - 5 action points per turn for player

- **Captain Mode**: Challenging tactical gameplay
  - Enhanced enemy stats (+25% hull/shields)
  - Standard resource generation
  - Reduced action points (4 AP per turn)

- **Admiral Mode**: Expert players only
  - Maximum enemy stats (+50% hull/shields)
  - Resource scarcity (-25% regeneration)
  - Permadeath for crew members

#### Balance Considerations

**Ship Class Balance:**

Reference 23rd century classes here: [Memory Alpha - Starship Classes](https://memory-alpha.fandom.com/wiki/Starship_classes_of_the_United_Federation_of_Planets)

- Constitution Class: Balanced all-rounder (baseline)
- Constellation Class: Heavy weapons platform (+30% hull, -10% speed)
- Miranda Class: Hybrid Science/Scout (-20% hull, +30% speed)
- Reliant Class: Versatile support ship (+10% hull, +20% speed, improved sensor range)
- Excelsior Class: Heavy cruiser (+40% hull, -20% maneuverability)
- Federation Class: Dreadnought (+50% hull, -30% speed, +20% weapons damage)
- Oberth Class: Science vessel (-30% hull, +40% sensor range, -10% weapons)
- Antares Class: Survey ship (-20% hull, +30% speed, +20% sensor range)
- Soyuz Class: Light cruiser (+10% speed, -10% hull, -10% weapons)

**Weapon Balance:**

- Phasers: 10-15 damage, 0.5s cooldown, 85% accuracy, 1 AP
  - Range based effectiveness:
    - Short range: +15% damage
    - Medium range: no modifier
    - Long range: -20% damage
  - High effectiveness against shields, lower against hull
  - Firing arc depending on phaser array type (narrow, wide, omni) and mount point
- Torpedoes: 25-35 damage, 1.0s cooldown, 75% accuracy, 2 AP
  - Range has no effect on damage but affects hit chance:
    - Short range: +10% accuracy
    - Medium range: no modifier
    - Long range: -15% accuracy
  - High effectiveness against hull, lower against shields
  - Have a speed that affects hit chance based on target max speed, maneuverability, and distance

**Resource Economy:**

- Energy regenerates 10 units/turn (passive)
- Shield regenerates 5 points/turn when not in combat
- Phaser banks have a buffer capacity that can improve with upgrades
- Torpedo launchers have a magazine size (default 10 torpedoes) that can be increased with upgrades
- Supplies consumed 1 unit/turn during travel, 3 units/turn in combat
- Crew morale decreases 2 points/week without shore leave

**Combat Pacing:**

- Average combat: 5-10 turns
- Elite encounters: 15-25 turns
- Initiative range: 6-10 (prevents excessive turn-swapping)

## 4. Game World

### 4.1 World Overview

The game world consists of a galaxy divided into sectors, each containing various star systems, space stations, and other points of interest. The player navigates the galaxy map to select sectors to explore on the sector map. Each sector contains a grid-based map with z-levels to represent 3D space, where the player can encounter NPC starships, anomalies, and other objects.

### 4.2 Galaxy Map

- The galaxy map will be comprised of sectors with different characteristics:
  - Safe zones (federation-controlled space)
  - Neutral zones (uncharted space)
  - Hostile zones (enemy-controlled space)
  - Travel between sectors may involve random encounters or scripted events
  - Time scale will be long (days or weeks per turn)
- A grid-based map with each cell representing a sector
- No z-levels
- Used for navigation between sectors
- Will have faction territories and special locations

### 4.3 Sector Map

- A grid-based map with z-levels to semi-represent 3D space
  - Planning for a maximum of 5 or 7 z-levels
  - Planning for a maximum x-y grid size of 20x20 cells
  - Sizes will vary between sectors
- Will be viewed from a fixed isometric perspective
- All z-levels are visible simultaneously
  - The z-level that the player is currently on is fully visible
  - Other z-levels are partially transparent
- Each cell can contain multiple entities, such as:
  - Empty space
  - A starship (player or NPC)
  - A space station
  - An anomaly (e.g., black hole, nebula, wormhole)
  - Other objects (e.g., asteroids, debris fields)
- The sector map will feature various locations and environments:
  - Star systems (with planets, moons, asteroids)
  - Space stations (for repairs, resupply, trading)
  - Anomalies (black holes, nebulae, wormholes)
  - Nebulae (affecting sensors and movement)
  - Asteroid fields (providing cover and obstacles)
  - Debris fields (remnants of destroyed ships or stations)
- Time scale will be medium (minutes or hours per turn)

### 4.4 Locations and Environments

#### Galaxy Map Sectors

| Sector Type | Security | Facilities | Mission Focus |
|-------------|----------|------------|---------------|
| **Federation Core** | High, frequent patrols | Numerous starbases | Patrol, escort, diplomacy |
| **Border** | Moderate, mixed control | Less frequent starbases | Patrol, reconnaissance, defense |
| **Neutral Zone** | Low, uncharted | Rare | Exploration, first contact, surveys |
| **Hostile Territory** | Enemy-controlled | None (enemy only) | Combat, espionage, rescue |
| **Unexplored** | Unknown | None | Deep space exploration, discovery |

#### Sector Map Locations

**Starbases:** Major Federation facilities providing repairs, resupply, crew rest, ship upgrades, mission briefings. Safe haven with docking mechanics.

**Star Systems:** Central star with orbiting planets (habitable/gas giants/barren), moons, asteroid belts (mining/hazards). Scientific survey opportunities.

**Space Stations:** Smaller facilities - civilian (trading/research), military (defense/sensors), or neutral (independent/alien). May be damaged, abandoned, or hostile.

**Anomalies:** Black holes (gravity wells, sensor interference), wormholes (shortcuts - future), subspace rifts, temporal anomalies. Scientific value with dangers.

#### Environmental Objects

| Environment | Sensor Impact | Movement Impact | Combat Impact |
|-------------|---------------|-----------------|---------------|
| **Open Space** | Standard range | No penalties | Emphasizes maneuver |
| **Nebulae** | -50% detection range | -1 AP per move, speed reduction | -10% accuracy, concealment |
| **Asteroid Fields** | Line of sight blocked | Increased AP cost | +20% damage reduction (cover) |
| **Debris Fields** | Minor obstruction | Navigation hazards | Partial cover, salvage opportunities |
| **Ion Storms** | Intermittent blackouts | Standard | Comms disruption |

#### Combat Map

Combat occurs on a 15x15 grid with 5 or 7 z-levels, procedurally generated from sector environment. Turn-based with initiative system, facing/firing arcs, shield facings, and line of sight calculations. Time scale: seconds to minutes per turn.

### 4.5 Factions and NPCs

- Factions will include:
  - The United Federation of Planets
  - Klingon Empire
  - Romulan Star Empire
  - The Gorn Hegemony
  - The Tholian Assembly
  - The Orion Syndicate
  - Independent traders and explorers

- NPC factions will have varying levels of influence and control over different sectors, affecting mission availability and difficulty.
- Faction relationships will impact gameplay:
  - Allied factions may offer support, resources, and easier missions
  - Hostile factions will present combat challenges and tougher missions
  - Neutral factions may offer trade opportunities and diplomatic missions
- Faction relationships at the beginning of the game will represent canonical Star Trek lore of the 23rd century.
- Faction motivations and behaviors will be reflected in NPC actions and mission types; however, the player can influence these relationships through their actions and skills such as Diplomacy.

- NPC starships will belong to various factions and have different behaviors:
  - Friendly (allied ships, neutral traders)
  - Hostile (enemy ships, pirates)
  - Neutral (independent ships, explorers)

- Will be able to interact with NPCs through:
  - Combat
  - Diplomacy
  - Trading
  - Random encounters
  - Player initiated interactions
  - Missions

## 5. Game Mechanics

### 5.1 Starships

#### Core Starship Representation

**Visual Representation:**

- Starships appear as sprites/icons on the isometric sector map
- Orientation indicated by visual arrow or engine glow
- Faction-specific color coding (Federation blue, Klingon red, Romulan green)
- Sprite size: 32x32 to 64x64 pixels depending on ship class
- Z-level indicators show vertical position relative to active layer

#### Starship Attributes

**Primary Systems:**

- **Hull Integrity**: Total structural damage capacity (varies by ship class)
- **Shield Systems**: Four directional facings (forward, aft, port, starboard) - 25 points each
- **Weapon Systems**:
  - Phaser arrays (270° forward firing arc, 1 AP cost)
  - Photon torpedoes (270° forward arc, 2 AP cost)
- **Engine Systems**:
  - Impulse drive (sector map movement)
  - Warp drive (galaxy map travel)
  - Maneuvering thrusters (turning and evasion)
- **Sensor Systems**:
  - Short-range sensors (tactical scanning)
  - Long-range sensors (strategic detection)

**Secondary Systems:**

- Deflector dish (environmental protection)
- Transporters (crew/cargo transfer)
- Shuttles (away missions)
- Life support (crew capacity)
- Communications array (hailing and diplomacy)

**Crew Attributes:**

- Crew efficiency (affects all system performance)
- Crew morale (influences efficiency and combat effectiveness)
- Individual crew member levels and specializations

#### Movement System

**Movement Mechanics:**

- Vector-based movement allowing all directions on grid
- Movement cost: 1 AP per grid cell
- Distance calculations use Pythagorean theorem for diagonal movement
- Can move between z-levels with increased AP costs
- Ship orientation updates based on movement direction

**Movement Modifiers:**

- Ship capabilities (engine power, thruster efficiency)
- Environmental factors:
  - Nebulae: -1 AP per move, reduced speed
  - Asteroid fields: increased AP cost, navigation hazards
  - Debris fields: minor navigation penalties
  - Open space: standard movement costs
- Engine power allocation affects maximum movement range
- Damaged engines reduce movement capability

**Orientation and Facing:**

- Facing determines firing arcs (270° forward cone)
- Affects shield coverage (automatic facing detection based on attacker position)
- Influences sensor effectiveness (forward sensors more effective)
- Updates automatically at end of turn based on final movement vector

#### Combat Capabilities

- Engage enemy ships within weapon range and firing arc
- Line of sight checking for valid targeting
- Range-based accuracy and damage calculations
- Critical hit system (10% chance, 1.5x damage)
- Action point costs per weapon type

#### Docking and Services

- Dock at starbases and space stations (1 AP action)
- Access repairs, resupply, upgrades, and mission briefings
- Free repairs and full resupply at friendly Federation starbases
- Crew rest and morale restoration during docking

### 5.2 Combat System

#### Combat Initiation

Combat occurs on the sector map when:

- Player ship encounters hostile NPC ships
- Mission objectives require engagement
- Player initiates combat action (hailing, firing)
- Ambush scenarios trigger from random events

Combat uses the existing sector map grid (15x15 with z-levels) rather than transitioning to a separate combat map.

#### Turn Structure and Initiative

**Initiative System:**

- All entities assigned initiative values at combat start
- Player ship: Initiative 10
- NPC ships: Initiative 6-9 (varies by ship class and crew)
- Higher initiative acts first each turn
- Turn order remains fixed throughout combat

**Action Points:**

- Player ship: 5 AP per turn (base, can be modified by upgrades/crew)
- NPC ships: 3 AP per turn
- Action points fully restore at start of each turn
- Unused AP does not carry over to next turn

#### Combat Actions

**Movement Actions:**

- Cost: 1 AP per grid cell
- Can move in any direction including z-level changes
- Movement updates ship orientation automatically
- Environmental modifiers apply (nebulae, asteroids)

**Weapon Actions:**

- Phasers: 1 AP, 10-15 damage, 0.5s cooldown, 85% base accuracy
  - 270° forward firing arc
  - Range modifiers: +15% damage (short), 0% (medium), -20% (long)
  - High effectiveness vs shields, lower vs hull
- Torpedoes: 2 AP, 25-35 damage, 1.0s cooldown, 75% base accuracy
  - 270° forward firing arc
  - Range affects hit chance: +10% (short), 0% (medium), -15% (long)
  - High effectiveness vs hull, lower vs shields

**Tactical Actions:**

- Scan: 1 AP, reveals enemy ship status and weaknesses
- Evasive Maneuvers: 2 AP, +10% dodge chance for remainder of turn
- Shield Redistribution: 1 AP, reallocate shield power between facings
- Emergency Repairs: 2 AP (requires Chief Engineer Level 5+)

**Special Abilities:**

- Varies by crew skills, ship class, and unlocked abilities
- Examples: Sensor jamming, emergency power, tactical analysis
- Costs vary: 2-3 AP depending on ability

#### Combat Resolution

**Attack Resolution:**

1. Check line of sight between attacker and target
2. Verify target within firing arc (270° forward cone)
3. Calculate base accuracy with range modifiers
4. Apply environmental modifiers (nebulae -10%, asteroid cover +20% defense)
5. Roll for hit/miss (critical hit: 10% chance, 1.5x damage)
6. Determine which shield facing is hit based on attacker position
7. Apply damage to shields first, then hull
8. Apply system damage if hull integrity drops below thresholds

**Damage Calculations:**

- Shield absorption: 85% for energy weapons, 65% for kinetic
- Shields reduced first, then hull takes remaining damage
- Critical hits bypass partial shield absorption
- System damage occurs at 75%, 50%, and 25% hull integrity
- Destroyed systems reduce ship effectiveness

**Combat Resolution Factors:**

- Weapon accuracy and damage values
- Shield strength and hull integrity
- Ship positioning and orientation (firing arcs, shield facings)
- Crew efficiency and morale bonuses
- Environmental effects (nebulae sensor interference, asteroid cover)
- System status (damaged weapons, depleted shields, engine malfunctions)

#### AI Behavior

**AI State Machine:**

- **PATROL**: Default state, moves on patrol route, scans for targets
- **ATTACK**: Engages targets, uses weapons, maintains optimal range
- **FLEE**: Retreats when hull drops below 30%, prioritizes survival

**AI Decision Making:**

- Target selection based on threat level and distance
- Weapon choice based on range and shield status
- Automatic AI processing at end of player turn
- Simple tactical decisions (closing distance, using cover)

#### Combat End Conditions

**Victory Conditions:**

- All enemy ships destroyed or fled
- Mission objectives completed (protect target, survive duration)
- Enemy surrender (rare, based on faction and circumstances)

**Failure Conditions:**

- Player ship destroyed (mission failure, respawn at starbase)
- Protected target destroyed
- Unable to complete time-sensitive objectives

**Post-Combat:**

- Experience points awarded based on performance
- Salvage opportunities from destroyed enemy ships
- Reputation adjustments (victory/defeat, casualties, tactics)
- Ship damage persists, requires repairs at starbase
- Crew morale affected by combat outcome

#### Alternative Resolution

**Diplomatic Options:**

- Hail enemy ship before combat (requires Communications officer)
- Negotiate surrender or retreat (Diplomacy skill check)
- Available for certain factions and mission types
- May result in reputation gains or peaceful resolution

**Retreat Option:**

- Player can attempt to flee combat (success chance based on relative speed)
- Costs 2 AP to initiate retreat
- May result in reputation loss or mission failure
- Enemy may pursue or break off

### 5.3 Resource Management

#### Primary Resources

**Energy System:**

- **Total Capacity**: Varies by ship class and reactor upgrades
- **Regeneration**: 10 units per turn (passive from impulse/warp reactors)
- **Allocation**:
  - Shields (continuous power draw per active shield facing)
  - Weapons (energy per shot for phasers, torpedo launch systems)
  - Engines (movement and warp drive power)
  - Sensors (active scanning consumes energy)
- **Management**: Power distribution sliders in UI for dynamic allocation
- **Depletion**: Zero energy disables systems until regeneration occurs

**Supplies:**

- **Types**:
  - Fuel (dilithium for warp drive, deuterium for impulse)
  - Medical supplies (treatment of crew injuries)
  - Spare parts (ship repairs and maintenance)
  - Food and consumables (crew sustainment)
- **Consumption Rates**:
  - 1 unit per turn during normal travel
  - 3 units per turn during combat
  - Additional consumption for repairs and medical treatment
- **Resupply**: Available at friendly starbases (free) or through trading
- **Mission Impact**: Low supplies reduce crew morale and limit repair capability

**Crew Morale:**

- **Range**: 0-100 (100 = maximum morale)
- **Factors Affecting Morale**:
  - Combat success: +5 morale
  - Combat failure: -10 morale
  - Casualties: -15 morale
  - Shore leave at starbase: +20 morale (temporary boost)
  - Time since last starbase visit: -2 morale per week
  - Ship damage and poor conditions: -5 morale
  - Successful mission completion: +10 morale
- **Effects on Gameplay**:
  - High morale (75-100): +10% crew efficiency bonus
  - Normal morale (50-74): Standard performance
  - Low morale (25-49): -10% crew efficiency penalty
  - Critical morale (0-24): -25% efficiency, risk of crew issues
- **Management**: Shore leave, successful missions, maintaining ship systems

**Ship System Condition:**

- **Integrity Tracking**: Each system has condition rating (0-100%)
- **Degradation Causes**:
  - Combat damage (immediate integrity loss)
  - Normal wear over time (1% per 10 turns active use)
  - Environmental damage (nebulae, ion storms)
- **Effects of Damage**:
  - 75-100%: Full functionality
  - 50-74%: -15% effectiveness
  - 25-49%: -35% effectiveness, increased failure chance
  - 0-24%: System critical, 50% chance of failure per use
  - 0%: System offline until repaired
- **Repair Mechanics**:
  - Automatic repairs: 5% per turn at starbase
  - Emergency repairs: Chief Engineer ability (2 AP, +10% immediate)
  - Full repairs: Dock at starbase (free at Federation bases)
  - Repair costs: Time, supplies, and crew efficiency affected

#### Resource Interdependencies

**Energy and Ship Performance:**

- Low energy (<25%) disables non-essential systems
- Cannot fire weapons without sufficient energy reserve
- Reduced movement range when engine power low
- Shields collapse if energy depleted during combat

**Supplies and Operations:**

- Insufficient supplies prevent repairs
- Medical emergencies require medical supplies
- Cannot maintain crew morale without adequate supplies
- Running out of supplies triggers emergency protocols

**Crew Morale and Efficiency:**

- High morale improves all ship system effectiveness
- Low morale reduces repair speed and combat effectiveness
- Critical morale may trigger crew events (sick bay overflow, discipline issues)
- Morale directly affects crew skill application

**System Condition and Combat:**

- Damaged weapons reduce accuracy and damage output
- Compromised shields have reduced capacity and regeneration
- Engine damage limits movement and evasive capabilities
- Sensor damage reduces detection range and targeting accuracy

#### Resource UI Elements

**Status Panel Display:**

- Energy bar (current/maximum)
- Supplies count with type breakdown
- Crew morale percentage with color coding
- System condition indicators for all major systems

**Management Interface:**

- Power allocation sliders for shields/weapons/engines/sensors
- Supply consumption tracking and alerts
- Crew roster with morale status
- System damage report with repair priorities

#### Resource Strategy

**Optimal Resource Management:**

- Balance energy allocation between offense and defense
- Maintain supply reserves for extended missions
- Visit starbases regularly to restore crew morale
- Repair critical systems before non-essential ones
- Plan mission routes based on resource availability

**Emergency Situations:**

- Energy crisis: Disable non-essential systems, retreat to starbase
- Supply shortage: Trade with merchants, salvage from combat
- Morale collapse: Immediate shore leave, abort non-critical missions
- System failures: Emergency repairs, tactical retreat

### 5.4 Mission System

#### Mission Types

**Patrol Missions:**

- Objective: Travel to designated waypoints in sector
- Duration: 3-5 turns
- Rewards: Low XP, standard supplies
- Difficulty: Easy
- Random encounters: 30% chance of hostile contact

**Escort Missions:**

- Objective: Protect civilian or diplomatic vessel to destination
- Duration: 5-8 turns
- Rewards: Medium XP, reputation bonus
- Difficulty: Medium
- Complications: Ambush scenarios, equipment malfunctions

**Reconnaissance Missions:**

- Objective: Scan anomalies or enemy positions without engagement
- Duration: 4-6 turns
- Rewards: Medium XP, scientific data
- Difficulty: Medium
- Requirements: Stealth approach, sensor management

**Combat Missions:**

- Objective: Engage and destroy enemy forces
- Duration: 2-4 turns plus combat time
- Rewards: High XP, salvage, reputation
- Difficulty: Hard
- Variants: Ship destruction, base assault, ambush scenarios

**Rescue Missions:**

- Objective: Respond to distress calls and save crew/civilians
- Duration: 3-5 turns
- Rewards: High reputation, variable XP
- Difficulty: Variable
- Time pressure: Penalty for delayed arrival

**Diplomatic Missions:**

- Objective: Establish or maintain relations with alien species
- Duration: 2-3 turns plus dialogue
- Rewards: Reputation, trade agreements, intelligence
- Difficulty: Variable
- Skills required: Command skill checks

#### Mission Generation

**Procedural Generation:**

- Missions generated based on sector characteristics
- Federation sectors: More patrol and escort missions
- Neutral zones: More exploration and reconnaissance
- Hostile zones: More combat and rescue missions

**Mission Difficulty Scaling:**

- Scales with player level and reputation
- Higher difficulty missions available at higher ranks
- Enemy ship classes match or exceed player capability

**Mission Frequency:**

- 1-2 missions available per sector visit
- Mission board refreshes when sector is revisited
- Priority missions appear based on story progression

#### Mission Structure

**Mission Briefing:**

- Clear objective statement
- Expected duration and difficulty rating
- Reward preview (XP, resources, reputation)
- Optional: Crew recommendations

**Mission Execution:**

- Waypoint navigation on sector map
- Encounter resolution (combat, dialogue, scanning)
- Resource management during mission
- Decision points with branching outcomes

**Mission Completion:**

- Success/failure evaluation
- Reward distribution
- After-action report
- Reputation adjustment

**Mission Failure Consequences:**

- No XP or resource rewards
- Reputation loss (severity dependent)
- Possible court-martial for critical failures
- Mission may become unavailable

#### Chain Missions

**Story Arcs:**

- Multi-part missions that span several sectors
- Each mission builds on previous outcomes
- Final mission provides exceptional rewards
- Example: "Klingon Incursion" (5-part campaign)

**Chain Mission Benefits:**

- Bonus XP for completing full chain
- Unique ship upgrades or equipment
- Major reputation improvements
- Unlock special crew members or abilities

### 5.5 Economy and Trading

- Economy and trading systems will be basic in the initial release
- Players can trade resources at space stations
- Future plans may include a more complex economy with supply and demand dynamics

### 5.6 AI and NPCs

#### NPC Starship AI

**AI State Machine:**

NPC ships operate using a simple state machine with three core states:

**PATROL State:**

- Default behavior when no threats detected
- Follows predefined patrol routes within sector
- Scans for targets periodically (uses sensor range)
- Transitions to ATTACK when hostile ship detected
- Low energy consumption, standard movement speed

**ATTACK State:**

- Actively engages detected hostile targets
- Target selection based on:
  - Threat assessment (distance, ship class, hull integrity)
  - Mission objectives (protect specific targets)
  - Tactical advantage (positioning, shield status)
- Weapon selection:
  - Phasers at short-medium range
  - Torpedoes at medium-long range when shields detected
- Movement tactics:
  - Close to optimal weapon range
  - Maintain firing arc on target
  - Use environmental cover when available (asteroids)
- Transitions to FLEE when hull drops below 30%

**FLEE State:**

- Activated when hull integrity critical (below 30%)
- Movement priorities:
  - Maximize distance from threats
  - Move toward friendly starbases if in sector
  - Use environmental hazards to block pursuit
- Energy conservation (minimal weapon use)
- Returns to PATROL if threats eliminated or escape successful
- Some factions never flee (Klingons - honor-bound)

#### AI Decision Making

**Target Acquisition:**

- Sensor sweep each turn to detect ships
- Priority scoring system:
  - Distance factor (closer = higher priority)
  - Hull integrity (weaker = higher priority)
  - Ship class (player ship = highest priority)
  - Faction relations (hostile factions = higher priority)
- Switches targets if current target destroyed or higher priority appears

**Tactical Decisions:**

- Range management: Attempts to maintain optimal weapon range
- Shield facing: Rotates to protect damaged shield facings
- Action point allocation: Balances movement and weapons each turn
- Environmental awareness: Uses asteroid cover, avoids nebulae when possible
- Evasive actions: 20% chance to use evasive maneuvers when shields below 50%

**Turn Processing:**

- AI processes actions during NPC phase (after player input phase)
- All NPC ships act in initiative order
- Complete action sequence: assess situation → move → attack → end turn
- Automatic AI processing without player input required

#### Faction-Specific Behaviors

| Faction | Aggression | Tactics | Flee Threshold | Special Behavior |
|---------|------------|---------|----------------|------------------|
| **Klingon** | Very High | Direct assault, close range | Never flees | Prioritizes honor, frontal attacks |
| **Romulan** | High | Flanking, ambush tactics | 25% hull | Uses stealth positioning, strategic |
| **Gorn** | Medium | Defensive, heavy weapons | 20% hull | Holds position, focuses on durability |
| **Orion** | Low | Opportunistic, hit-and-run | 50% hull | Targets weak ships, flees early |
| **Tholian** | Medium | Precision strikes, exotic weapons | 30% hull | Alien logic, unpredictable patterns |

#### NPC Interaction Types

**Combat Encounters:**

- Hostile NPCs attack on sight
- Neutral NPCs may defend if provoked
- Friendly NPCs assist in combat

**Diplomatic Interactions:**

- Hailing enemy ships (Communications officer required)
- Negotiation attempts (Diplomacy skill check)
- Surrender offers from AI when overwhelmed
- Distress calls from friendly or neutral ships

**Random Encounters:**

- Patrol ships requesting identification
- Traders offering goods
- Distressed vessels requiring assistance
- Exploration vessels sharing information

**Mission-Specific NPCs:**

- Escort targets following player ship
- Enemy commanders with scripted behaviors
- Civilian vessels with specific routes
- Special encounter ships with unique AI

#### AI Limitations (Current Implementation)

**Current AI Capabilities:**

- Basic state machine (PATROL, ATTACK, FLEE)
- Simple target selection scoring
- Automatic turn processing
- Faction-specific aggression levels
- Environmental awareness (basic obstacle detection)

**Planned Future Enhancements:**

- Advanced tactical planning (flanking maneuvers, formations)
- Group coordination for multiple enemy ships
- Dynamic difficulty adjustment based on player skill
- Personality system for named enemy commanders
- Learning AI that adapts to player tactics
- More complex environmental utilization (nebula hiding, asteroid navigation)

## 6. User Interface and User Experience

### 6.1 UI Design Philosophy

Inspired by UI's windowed desktop games largely around the mid-1990s era. An example would be a MUD/MUSH/MOO desktop client such as zMUD and MUSHclient. A more modern example is Mudlet. However, typing commands will not be an interaction method in this game. The UI will be entirely mouse-driven with keyboard shortcuts for common actions.

[A desktop application aesthetic (MUSHclient)](UI%20./Images/Example%20(MUSHclient).png)

### 6.2 Interface Layout

**Core Layout Principles:**

- The main game will be contained within a PySide6 application window
- Much of the interaction will be through widgets such as menus, dialogs, and buttons
- The main game view (map) will be rendered using pygame-ce embedded within the PySide6 application
- The map will be centered in the application window with UI elements surrounding it
- Pop-up dialogs will be used for mission briefings, ship status, and other information

#### 6.2.1 Implemented Layout: "Right-Rail Tactical"

**Layout Design:**

```text
+--------------------------------------------------------+
|  Menu Bar: File | View                                  |
+--------------------------------------------------------+
|  Toolbar: [Galaxy] [Sector] [Combat] | [Z↑] [Z↓]      |
+--------------------------------------------------------+
|                              |                         |
|       CENTRAL MAP            |    RIGHT DOCK PANEL     |
|    (pygame-ce surface)       |                         |
|     1280x900 pixels          |   [Status Tab]          |
|   Isometric grid view        |   [Actions Tab]         |
|   with z-level display       |   [Map Tab]             |
|                              |                         |
|                              |   Ship: USS Enterprise  |
|                              |   Hull: [====] 100%     |
|                              |   Shields: [====] 100%  |
|                              |   Energy: [====] 100%   |
|                              |   Position: (10,10,2)   |
|                              |                         |
+------------------------------+-------------------------+
|  Turn Bar: Turn: 1 | Phase: Input | AP: 5 | [End Turn] |
+--------------------------------------------------------+
```

**PySide6 Component Structure:**

**Base Window (QMainWindow):**

- Main application window with menu bar, toolbar, and dock widgets
- Central widget contains game display and turn bar
- Dockable panels for flexible layout customization

**Menu Bar:**

- **File Menu**: New Game, Save Game, Load Game, Exit
- **View Menu**: Toggle dock visibility, zoom controls, z-level display options

**Top Toolbar (QToolBar):**

- Mode switcher buttons: [Galaxy Map] [Sector Map] [Combat Mode]
- Separator
- Zoom controls: [Zoom In] [Zoom Out] [Reset Zoom]
- Z-level navigation: [Z↑] [Z↓] (when in Sector/Combat modes)

**Central Widget (QVBoxLayout):**

1. **Game Surface (QWidget)**:
   - Custom widget embedding pygame-ce rendering surface
   - Size: 1280x900 pixels (expandable)
   - Isometric grid display with z-level visualization
   - Mouse interaction for ship selection and movement
   - QSizePolicy: Expanding, Expanding (fills available space)

2. **Turn Bar (QWidget with QHBoxLayout)**:
   - Turn counter: "Turn: [number]"
   - Current phase: "Phase: Input/Resolution"
   - Action points: "AP: [remaining]/[maximum]"
   - [End Turn] button (triggers turn advancement)
   - Real-time updates after each game action

**Right Dock Panel (QDockWidget):**

- Allowed areas: Left|Right (user can reposition)
- Default position: Docked right
- Minimum width: 300 pixels
- Contains QTabWidget with three tabs:

**Tab 1: Status (QFormLayout)**

- **Ship Name**: Label showing current ship (e.g., "USS Enterprise")
- **Hull Integrity**: QProgressBar (0-100%, red when critical)
- **Shield Status**: Four QProgressBar widgets for each facing
  - Forward shields
  - Aft shields
  - Port shields
  - Starboard shields
- **Energy Level**: QProgressBar (0-maximum capacity)
- **Position**: Label showing grid coordinates (x, y, z)
- **Sector**: Label showing current sector name

**Tab 2: Actions (QVBoxLayout)**

Action buttons organized by category:

- **Movement Group**:
  - [Move Ship] button (toggles move mode)
  - [Cancel Move] button (visible when in move mode)
- **Combat Group**:
  - [Fire Weapons] button (opens target selection dialog)
  - [Scan Target] button (placeholder - future implementation)
  - [Evasive Maneuvers] button (placeholder - future implementation)
- **Utilities Group**:
  - [Dock] button (dock at nearby starbase)
  - [Hail] button (placeholder - future communications)

**Tab 3: Map (QVBoxLayout)**

- **Mini-map**: QLabel placeholder (320x240 pixels)
  - Future: Display sector overview
  - Future: Show ship positions and points of interest
- **Legend**: QTextEdit or QLabel with sector information
  - Faction control
  - Environmental features
  - Nearby objects

**Implementation Details:**

**Resizing Behavior:**

- Central game surface expands/contracts with window size
- Minimum window size: 1600x1000 pixels
- Right dock maintains minimum 300px width
- Turn bar remains fixed height at bottom
- Toolbars remain fixed at top

**Visual Styling:**

- Dark blue-gray background theme (#1E2A3A)
- Cyan highlights for active elements (#00FFFF)
- Progress bars with faction-appropriate colors
- Consistent button styling across all actions
- Clear visual feedback for button states (hover, pressed, disabled)

**User Experience:**

- Tab switching for organized action access
- Status always visible in Status tab
- Quick action access in Actions tab
- Future navigation aids in Map tab
- Dock panel can be hidden via View menu for maximum map space
- Persistent layout preferences (future: save window configuration)

**Rationale for This Design:**

- ✅ Simplifies development: Single coherent layout implementation
- ✅ Focuses on essentials: Status, actions, and map clearly separated
- ✅ Efficient screen usage: Maximizes map visibility while keeping controls accessible
- ✅ Scalable: Easy to add new buttons, status indicators, or tabs
- ✅ Familiar pattern: Standard application layout with docks and toolbars
- ✅ Suitable for turn-based gameplay: No need for split-second UI access
- ✅ Future-proof: Can expand to additional docks or panels as needed

### 6.3 Input Controls

#### Primary Input Methods

**Mouse Controls:**

The primary method of interaction with the game.

**Map Interaction:**

- **Left Click on Grid Cell**: Select cell or move ship (when in move mode)
- **Left Click on Ship**: Select ship for status display
- **Right Click on Ship**: Context menu for ship actions (future)
- **Mouse Wheel Scroll**: Zoom in/out on map view
- **Middle Mouse Drag**: Pan camera (future implementation)

**UI Interaction:**

- **Left Click on Buttons**: Execute actions (Move, Fire, Dock, etc.)
- **Left Click on Menu Items**: Access file operations and settings
- **Left Click on Toolbar Buttons**: Switch modes, adjust zoom, change z-levels
- **Left Click in Tabs**: Switch between Status, Actions, and Map tabs

**Keyboard Controls:**

Secondary input method with shortcuts for common actions.

**Map Navigation:**

- **Arrow Keys**: Pan camera view (future implementation)
- **PageUp / PageDown**: Move up/down z-levels
- **Home**: Reset camera to player ship
- **+ / -**: Zoom in/out
- **0**: Reset zoom to default

**Game Actions:**

- **M**: Toggle move mode
- **Escape**: Cancel current action (move mode, targeting, etc.)
- **Space**: End turn
- **F**: Open fire weapons dialog
- **D**: Dock at nearby starbase
- **S**: Scan target (future)
- **E**: Evasive maneuvers (future)

**Mode Switching:**

- **F1**: Galaxy Map mode
- **F2**: Sector Map mode
- **F3**: Combat mode (when in combat)

**Game Management:**

- **Ctrl+S**: Quick save
- **Ctrl+L**: Load game
- **Ctrl+Q**: Quit game
- **F11**: Toggle fullscreen (future)

**Configuration:**

- All keyboard shortcuts configurable via `key_bindings.toml`
- Custom key mappings supported
- Future: In-game keybinding editor in Settings dialog

#### Dialog and Menu Interactions

**File Menu:**

- **New Game**: Start new game session
- **Save Game**: Save current progress
- **Load Game**: Load saved game
- **Exit**: Close application

**View Menu:**

- **Toggle Right Dock**: Show/hide action panel
- **Toggle Turn Bar**: Show/hide turn information
- **Reset Layout**: Restore default window layout

**Dialog Boxes:**

**Target Selection Dialog:**

- **Click on Ship in List**: Select target
- **Double-Click**: Select and confirm target
- **[Cancel] Button**: Close without selecting
- **[Fire] Button**: Confirm weapon and target

**Mission Briefing Dialog (Future):**

- **Click [Accept]**: Accept mission and start
- **Click [Decline]**: Refuse mission
- **Scroll**: Read full mission details

**Settings Dialog (Future):**

- **Tabs**: Graphics, Audio, Controls, Gameplay
- **Sliders**: Adjust volume, graphics quality
- **Checkboxes**: Toggle features
- **Dropdown Menus**: Select options
- **[Apply] Button**: Save changes
- **[Cancel] Button**: Discard changes

#### Input Response and Feedback

**Visual Feedback:**

- Button hover states: Highlight on mouse-over
- Button pressed states: Visual depression effect
- Cursor changes: Pointer, hand, crosshair based on context
- Selected cells: Highlight with cyan border
- Valid movement cells: Green highlight (in move mode)
- Invalid movement cells: Red highlight (in move mode)

**Audio Feedback (Future):**

- Button clicks: Subtle LCARS-style beep
- Action confirmation: Success tone
- Error actions: Warning sound
- Turn end: Distinctive notification

**Haptic Feedback:**

- Not planned (no gamepad support in initial release)

#### Accessibility Features

**Current Implementation:**

- Large clickable buttons (minimum 60x30 pixels)
- High contrast UI elements
- Clear visual state indicators
- Keyboard shortcuts for all major actions

**Future Considerations:**

- Colorblind mode with pattern overlays
- Adjustable UI scaling (1x, 1.5x, 2x)
- Screen reader support for menus and dialogs
- Configurable keybindings for accessibility needs

### 6.4 Accessibility

- No specific accessibility features are planned at this time.

## 7. Audio and Visual Design

### 7.1 Art Style

#### Visual Direction

**Overall Aesthetic:**

- Retro-inspired pixel art style honoring 1970s-1990s computer game aesthetics
- Clean, functional design prioritizing clarity over visual complexity
- Kirk-era Star Trek (TOS) design language and color palette
- Emphasis on readability and tactical information at a glance

#### Color Palette

**Faction Colors:**

- Federation: Primary blue (#0066CC), accent gold (#FFD700)
- Klingon Empire: Deep red (#CC0000), accent bronze (#CD7F32)
- Romulan Star Empire: Forest green (#228B22), accent silver (#C0C0C0)
- Neutral/Pirates: Gray (#808080), accent orange (#FF8C00)

**UI Colors:**

- Primary Interface: Dark blue-gray background (#1E2A3A)
- Active Elements: Bright cyan highlights (#00FFFF)
- Warning States: Amber (#FFBF00)
- Critical Alerts: Red (#FF0000)
- Success Indicators: Green (#00FF00)

**Space Environment:**

- Deep space: Near-black with subtle blue tint (#0A0E14)
- Nebulae: Purple, pink, and blue gradients
- Stars: White (#FFFFFF) with varying brightness
- Grid lines: Semi-transparent white (#FFFFFF, 30% opacity)

#### Ship Design

**Visual Representation:**

- Top-down isometric view (2.5D perspective)
- Ship sprites: 32x32 to 64x64 pixels
- Clear orientation indicators (arrow or engine glow)
- Faction-specific design silhouettes
- Hull damage shown through sprite degradation

**Ship Details:**

- Constitution Class: Iconic saucer and engineering hull
- Klingon D7: Distinctive bird-of-prey profile
- Romulan Bird-of-Prey: Streamlined warbird design
- Each class has unique sprite recognizable at distance

#### UI Design Style

**Interface Aesthetic:**

- LCARS-inspired (Library Computer Access/Retrieval System)
- Rounded corners on panels and buttons
- Segmented progress bars with clean fills
- Status indicators use color-coding extensively
- Minimal textures, emphasis on flat design with depth through color

**Typography:**

- Primary Font: Clean sans-serif (similar to Federation fonts)
- Monospace Font: For technical readouts and coordinates
- Font sizes: 12pt for body, 14pt for headers, 10pt for details

**Layout Philosophy:**

- Information hierarchy: Critical data most prominent
- Tactical information always visible
- Progressive disclosure: Details on demand
- Consistent widget placement across modes

#### Effects and Animations

**Weapon Effects:**

- Phasers: Bright orange beam with glow
- Torpedoes: Animated projectile with trail
- Explosions: Frame-based sprite animation (4-6 frames)
- Impact flashes: Brief screen-space highlights

**Environmental Effects:**

- Nebula clouds: Subtle animated transparency
- Asteroid rotation: Slow sprite rotation
- Warp travel: Streak effect across screen
- Shield impacts: Hexagonal grid flash at hit location

**UI Animations:**

- Button press: Subtle scale and brightness change
- Panel transitions: Smooth slide or fade (0.2s duration)
- Progress bars: Smooth fill animations
- Alert pulses: Gentle opacity oscillation

#### Icon Design

**Status Icons:**

- Hull: Ship silhouette
- Shields: Hexagonal grid pattern
- Energy: Lightning bolt
- Weapons: Crosshair or phaser icon
- Engines: Stylized nacelle
- Crew: Humanoid figure

**Action Icons:**

- Movement: Directional arrows
- Attack: Targeting reticle
- Scan: Radar sweep
- Dock: Station silhouette
- Repair: Wrench or tool icon

#### Accessibility Considerations

**Visual Clarity:**

- High contrast between elements
- Colorblind-friendly palette (uses patterns + colors)
- Scalable UI elements (1x, 1.5x, 2x options)
- Clear text with readable fonts at all sizes
- Important information never conveyed by color alone

### 7.2 Audio Design

*Deferred to future phases*

### 7.3 Visual Effects

*Deferred to future phases*

## 8. Narrative and Storytelling

### 8.1 Story Overview

- There will be very minimal narrative elements in the initial release
- The player will take on the role of a starship captain in the Star Trek universe
- The game will focus on exploration, tactical combat, and resource management
- Story elements will be introduced through mission briefings, encounters with NPCs, and events on the sector map

### 8.2 Characters

#### Player Character

**Captain [Player Name]**

- Commanding officer of the player's starship
- Customizable name and basic background during game start
- Experience level affects ship performance and mission availability
- Reputation with Starfleet Command influences assignments and promotions

**Character Attributes:**

- **Command Skill**: Affects crew morale and efficiency (0-100)
- **Tactical Skill**: Provides combat bonuses to accuracy and damage (0-100)
- **Science Skill**: Enhances sensor range and analysis capabilities (0-100)
- **Engineering Skill**: Improves repair speed and system efficiency (0-100)

**Captain Background (Optional Story Elements):**

- Academy Graduate: Standard Starfleet training
- Field Promoted: Rose through ranks during crisis
- Explorer: Focused on discovery and scientific missions
- Tactical Officer: Combat-focused background

#### Key Crew Members

| Position | Role | Special Ability (Level 5+) | Skills |
|----------|------|---------------------------|---------|
| **First Officer** | Executive officer, tactical advisor | +1 AP pool; can assume command | Command, Tactics, Leadership |
| **Chief Engineer** | Ship systems, power distribution | Emergency repairs (2 AP cost) | Engineering, Warp Theory, Systems |
| **Security Chief** | Weapons systems, ship security | +5% weapon accuracy | Tactics, Weapons, Security |
| **Science Officer** | Anomaly analysis, enemy identification | Identify ship weaknesses | Science, Sensors, Xenobiology |
| **Helm Officer** | Ship movement, navigation | -1 AP movement cost (Level 8) | Piloting, Navigation, Cartography |
| **Communications** | Ship comms, diplomatic contacts | Better hailing success | Communications, Diplomacy, Translation |
| **Medical Officer** | Crew health, casualty treatment | Emergency medical treatment | Medicine, Xenobiology, Psychology |

#### NPC Characters

**Starfleet Command**

**Admiral [Procedurally Generated Name]**

- **Role**: Represents Federation authority and issues mission assignments
- **Interaction**: Mission briefings, promotions, strategic directives
- **Personality Types**: By-the-book, Maverick, Diplomatic, Tactical
- **Relationship**: Affected by player reputation and mission outcomes

**Starbase Commanders**

**Commander [Procedurally Generated Name]**

- **Role**: Manages starbase operations and local sector defense
- **Interaction**: Repair/resupply services, local intelligence, sector missions
- **Services**: Repairs, upgrades, crew rest, mission briefings
- **Relationship**: Reputation affects service priority and pricing

#### Enemy Commanders

| Faction | Personality | Tactics | Ship Classes |
|---------|-------------|---------|--------------|
| **Klingon** | Aggressive, honor-focused | Frontal assault, overwhelming firepower, never retreats | D7 Cruiser, Bird-of-Prey |
| **Romulan** | Tactical, strategic, deceptive | Cloaking ambushes, flanking, strategic withdrawal | Bird-of-Prey, Warbird |
| **Gorn** | Methodical, powerful, deliberate | Defensive positioning, heavy weapons, endurance | Heavy Cruiser |
| **Orion** | Opportunistic, mercenary | Targets weak ships, flees when outmatched, trickery | Raider, Corsair |
| **Tholian** | Alien logic, territorial | Web weapons, precision strikes, exotic energy | Web-Spinner |

#### Neutral Characters

| Character | Role | Benefits |
|-----------|------|----------|
| **Merchant Captain** | Trading opportunities, rumors | Access to rare supplies and equipment |
| **Independent Explorer** | Sector information, discoveries | Sector maps, anomaly locations |
| **Civilian Transport** | Escort mission opportunities | Reputation gains, emergency assistance |

### 8.3 Dialogue System

*To be defined in future phases*

### 8.4 Cutscenes and Presentation

*No cutscenes planned*

## 9. Technical Requirements

### 9.1 Technical Architecture

#### Architecture Pattern: Hybrid State Machine + Game Object + Component + MVC

The game will use a hybrid architecture optimized for turn-based strategy games:

#### Core Architecture Components

##### Game State Machine

- Manages transitions between game modes: Galaxy Map ↔ Sector Map ↔ Combat Mode
- Handles UI state synchronization with PySide6
- Provides clean separation of game phases
- Supports save/load at any state

##### Game Object Pattern with Component Composition

- Starships, stations, and crew as GameObject base classes
- Component composition for ship systems (not full ECS)
- Natural object hierarchies for Star Trek entities
- Simplified system interactions for turn-based gameplay

##### Model-View-Controller (MVC) Separation

- **Model**: Game logic, state, and data (pure Python)
- **View**: PySide6 UI widgets and pygame-ce rendering
- **Controller**: Input handling and state transitions
- Enables independent testing of game logic

#### Detailed Architecture Specification

**Game State Management:**

```python
class GameState(ABC):
    """Base class for all game states."""
    def enter(self) -> None: ...
    def exit(self) -> None: ...
    def handle_input(self, event) -> None: ...
    def update(self, dt: float) -> None: ...
    def render(self, surface) -> None: ...

class GameStateManager:
    """Manages state transitions and current state."""
    def transition_to(self, new_state: GameState) -> None: ...
    def update(self, dt: float) -> None: ...
```

**Game Object Pattern:**

```python
class GameObject:
    """Base class for all game entities."""
    def __init__(self, position: GridPosition):
        self.id = generate_id()
        self.position = position
        self.active = True

class Starship(GameObject):
    """Star Trek starship with component systems."""
    def __init__(self, position: GridPosition, ship_class: str):
        super().__init__(position)
        self.systems = {
            'weapons': WeaponSystems(),
            'shields': ShieldSystems(),
            'engines': EngineSystems(),
            'sensors': SensorSystems()
        }
        self.crew = CrewRoster()
        self.resources = ResourceManager()
```

**Component Pattern (Simplified):**

```python
class ShipSystem:
    """Base class for ship subsystems."""
    def __init__(self, efficiency: float = 1.0):
        self.efficiency = efficiency
        self.damaged = False
        self.power_usage = 0.0

class WeaponSystems(ShipSystem):
    """Manages ship weapons and firing solutions."""
    def __init__(self):
        super().__init__()
        self.phasers = PhaserArray()
        self.torpedoes = TorpedoLauncher()

    def can_fire_at(self, target: GridPosition) -> bool: ...
    def calculate_damage(self, target: Starship) -> int: ...
```

**MVC Implementation:**

```python
class GameModel:
    """Pure game logic and state (no UI dependencies)."""
    def __init__(self):
        self.galaxy = GalaxyMap()
        self.current_sector = None
        self.player_ship = None
        self.turn_manager = TurnManager()

    def execute_move(self, ship: Starship, destination: GridPosition) -> bool: ...
    def resolve_combat(self, attacker: Starship, target: Starship) -> CombatResult: ...

class GameView:
    """PySide6 UI and pygame-ce rendering (no game logic)."""
    def __init__(self, controller):
        self.controller = controller
        self.main_window = MainWindow()
        self.game_surface = pygame.Surface((800, 600))

    def render_sector_map(self, sector: SectorMap) -> None: ...
    def show_combat_dialog(self, result: CombatResult) -> None: ...

class GameController:
    """Handles input and coordinates Model/View."""
    def __init__(self):
        self.model = GameModel()
        self.view = GameView(self)
        self.state_manager = GameStateManager()

    def handle_ship_move(self, destination: GridPosition) -> None: ...
    def handle_combat_action(self, action: CombatAction) -> None: ...
```

#### Memory Management and Object Pooling

**Entity Pooling:**

```python
class EntityPool:
    """Manages reusable game objects for performance."""
    def __init__(self, entity_type: type, initial_size: int = 50):
        self.pool = [entity_type() for _ in range(initial_size)]
        self.active_entities = set()

    def acquire(self) -> GameObject: ...
    def release(self, entity: GameObject) -> None: ...

class ResourceManager:
    """Centralized resource and memory management."""
    def __init__(self):
        self.starship_pool = EntityPool(Starship, 20)
        self.projectile_pool = EntityPool(Projectile, 100)
        self.effect_pool = EntityPool(VisualEffect, 50)
```

#### State-Specific Implementations

**Galaxy Map State:**

- Large-scale navigation between sectors
- Resource management and fleet status
- Mission briefings and strategic planning
- Time scale: days/weeks per turn

**Sector Map State:**

- Grid-based movement with z-levels
- Real-time encounter resolution
- Environmental interactions
- Time scale: hours/minutes per turn

**Combat State:**

- Tactical turn-based combat
- Detailed ship system management
- Action point allocation
- Time scale: seconds/minutes per turn

#### Data Flow and Dependencies

```text
PySide6 Main Window
    ├── Menu System (PySide6 widgets)
    ├── Game View (pygame-ce embedded surface)
    ├── Dialog System (PySide6 dialogs)
    └── Status Panels (PySide6 widgets)

Game Controller
    ├── Input Handler
    ├── State Manager
    └── Event Dispatcher

Game Model (Pure Logic)
    ├── Galaxy Map
    ├── Sector Maps
    ├── Game Objects
    └── Rule Engine
```

#### Testing Strategy

**Unit Tests (pytest):**

- Game logic isolated from UI
- Ship system interactions
- Combat calculations
- State transitions

**Integration Tests:**

- Controller → Model interactions
- State persistence
- Multi-state workflows

**UI Tests:**

- PySide6 widget behavior
- pygame-ce rendering validation
- User interaction flows

This hybrid architecture provides:

- ✅ Clean separation for testing
- ✅ Appropriate complexity for turn-based gameplay
- ✅ Natural Star Trek entity relationships
- ✅ Performance suitable for target platforms
- ✅ Clear state management
- ✅ Modular design for future expansion

### 9.2 Platform Requirements

#### Target Platform

**Linux Exclusively:**

- All development and testing performed on Linux systems
- Code uses Linux-specific paths, system calls, and conventions
- No Windows or macOS support planned or maintained
- Assumes POSIX-compliant environment

#### System Requirements

**Minimum Requirements:**

- **OS**: Ubuntu 22.04 LTS or equivalent modern Linux distribution
- **Python**: 3.14 or higher (required for latest language features)
- **RAM**: 4 GB minimum
- **Storage**: 500 MB for game and assets
- **Display**: 1600x1000 resolution minimum
- **Graphics**: OpenGL 2.0+ capable GPU

**Recommended Requirements:**

- **OS**: Ubuntu 24.04 LTS or latest stable Linux distribution
- **Python**: Latest Python 3.14+ release
- **RAM**: 8 GB or more
- **Storage**: 1 GB for game, saves, and future content
- **Display**: 1920x1080 or higher resolution
- **Graphics**: Modern GPU with OpenGL 3.0+ support

#### Dependencies

**Core Libraries:**

- **pygame-ce**: Community Edition for Python 3.14+ compatibility
  - Handles game rendering, sprite management, surface operations
  - Required version: Latest stable release
  - Alternative to standard pygame (lacks Python 3.14+ support)
- **PySide6**: Qt for Python bindings
  - UI framework for windows, menus, dialogs, widgets
  - Required version: 6.5.0 or higher
  - Provides native-looking Linux UI elements

**Python Standard Library:**

- Primary dependency strategy: Use stdlib whenever possible
- `tomllib`: Configuration file reading (Python 3.11+)
- `tomli_w`: TOML file writing (external, minimal dependency)
- `dataclasses`: Entity and component definitions
- `typing`: Type hints and annotations
- `abc`: Abstract base classes for patterns

**Development Tools:**

- **pytest**: Testing framework (8.0+)
- **pytest-cov**: Code coverage reporting
- **pytest-mock**: Mocking and fixtures
- **Git**: Version control
- **VS Code**: Recommended IDE with Python extensions

#### Linux-Specific Considerations

**File System:**

- Forward slashes for all path operations (`/`)
- Case-sensitive file names
- Home directory: `~/` or `$HOME`
- Configuration location: `~/.config/star_trek_retro_remake/`
- Save data location: `~/.local/share/star_trek_retro_remake/`

**Display and Window Management:**

- X11 window system support required
- Wayland support via XWayland compatibility layer
- Window decorations provided by system window manager
- Native Linux desktop integration (icons, app launchers)

**Package Management:**

- Distribution via PyPI (future)
- Installation via pip or uv package manager
- System package dependencies: `python3-dev`, `libsdl2-dev`, `libqt6-dev`

**Audio System (Future):**

- PulseAudio or PipeWire support
- ALSA fallback for older systems
- No proprietary audio drivers required

#### Performance Optimization for Linux

**Graphics:**

- OpenGL rendering pipeline (pygame-ce + Qt)
- Hardware acceleration when available
- Software fallback for older systems
- VSync support for smooth rendering

**Multi-threading:**

- Separate threads for game logic, rendering, UI
- Efficient resource loading using thread pools
- GIL-aware design for Python threading

**Memory Management:**

- Object pooling for frequently created/destroyed entities
- Efficient sprite and texture management
- Garbage collection tuning for smooth gameplay
- Memory-mapped file loading for large assets (future)

#### Distribution Format

**Current (Development):**

- Git repository clone
- Virtual environment setup with uv or pip
- Manual dependency installation
- Direct Python execution

**Planned (v1.0):**

- Python wheel package (.whl)
- PyPI distribution
- AppImage for universal Linux compatibility
- Flatpak for sandboxed distribution (future)
- Native .deb package for Debian/Ubuntu (future)

#### No Cross-Platform Support

**Explicit Non-Support:**

- Windows: Possible future Windows compatibility
- macOS: No plans for macOS compatibility
- BSD: May work but unsupported and untested
- Mobile: No Android/iOS versions planned

**Rationale:**

- Simplified development and testing (single platform)
- Linux-native tools and conventions throughout
- No abstraction layers for cross-platform compatibility
- Developer familiarity and preference for Linux ecosystem
- Smaller scope appropriate for solo development

### 9.3 Performance Requirements

#### Frame Rate Targets

**UI and Menus:**

- Target: 60 FPS for PySide6 UI elements
- Minimum acceptable: 30 FPS for complex dialogs
- Smooth animations for button interactions and panel transitions
- Immediate response to mouse clicks (<16ms)

**Game View (pygame-ce):**

- Target: 60 FPS for map rendering and sprite display
- Minimum acceptable: 30 FPS during complex scenes
- Turn-based nature allows lower FPS without gameplay impact
- Priority: Consistency over peak performance

**Combat Animations (Future):**

- Weapon effects: 30-60 FPS
- Explosion animations: 30 FPS minimum
- Particle effects: 24-30 FPS acceptable

#### Load Time Targets

**Application Startup:**

- Initial launch: <3 seconds from execution to main menu
- Configuration loading: <500ms
- Asset preloading: <2 seconds for essential sprites

**Mode Transitions:**

- Sector map loading: <2 seconds
- Combat initialization: <1 second
- Galaxy map rendering: <1 second
- State save/load: <2 seconds

**Asset Loading:**

- Sprite loading on demand: <100ms per sprite sheet
- Configuration file parsing: <50ms per file
- Sector data loading: <200ms per sector

#### Memory Usage Limits

**Base Application:**

- Minimum footprint: 50 MB (Python interpreter + core modules)
- With base assets loaded: <512 MB maximum
- Entity pool allocation: 10 MB reserved
- Sprite cache: 100 MB maximum

**During Gameplay:**

- Sector map active: 256 MB typical
- Combat scenario: 384 MB typical
- Galaxy map navigation: 128 MB typical
- Memory growth: <1 MB per hour of gameplay (no memory leaks)

**Object Pooling:**

- Starship pool: 20 pre-allocated entities
- Projectile pool: 100 pre-allocated entities
- Visual effect pool: 50 pre-allocated entities
- Pool expansion: 25% growth when exhausted

#### CPU Utilization

**Turn Processing:**

- Player turn: <50ms for input validation and state update
- AI turn processing: <200ms per NPC ship
- Multiple NPCs: <1 second for 10 simultaneous AI ships
- Turn advancement: <100ms for state transitions

**Rendering Pipeline:**

- Grid rendering: <10ms per frame
- Entity rendering: <5ms for 20 ships
- UI update: <5ms per frame
- Total frame time budget: 16.7ms (60 FPS) or 33.3ms (30 FPS)

**Background Operations:**

- Asset loading: Low priority, 5-10% CPU usage
- Save game operations: <1 second, non-blocking
- Configuration updates: Asynchronous, <50ms

#### Multi-threading Strategy

**Thread Architecture:**

1. **Main Thread (UI Thread)**:
   - PySide6 event loop and UI updates
   - User input handling
   - Dialog and widget management
   - Render command dispatch

2. **Game Logic Thread**:
   - Turn processing and state updates
   - AI decision making
   - Combat calculations
   - Physics and movement
   - Thread-safe communication with main thread

3. **Rendering Thread**:
   - pygame-ce surface rendering
   - Sprite drawing and transformations
   - Grid and z-level visualization
   - Effect animations (future)

4. **Resource Loading Thread**:
   - Asynchronous asset loading
   - Configuration file parsing
   - Save/load operations
   - Background preparation of next sector

**Thread Synchronization:**

- Queue-based communication between threads
- Lock-free design where possible for game state access
- Copy-on-write for shared data structures
- Event-driven updates from game logic to UI

**Thread Safety:**

- Game model mutations only in game logic thread
- UI updates only in main thread
- Rendering reads from stable game state snapshot
- Atomic operations for critical shared state

#### Optimization Techniques

**Rendering Optimizations:**

- **Dirty Rectangle Tracking**: Only redraw changed portions of screen
- **Sprite Batching**: Group similar sprites for efficient rendering
- **Z-level Culling**: Don't render entities far from active z-level
- **View Frustum Culling**: Skip off-screen entity rendering
- **Sprite Caching**: Pre-render commonly used sprite combinations

**Data Structure Optimizations:**

- **Spatial Partitioning**: Grid-based spatial indexing for entity lookups
- **Object Pooling**: Reuse allocated entities instead of creation/destruction
- **Flyweight Pattern**: Share immutable ship data across instances
- **Lazy Loading**: Load sector data only when entering sector

**Algorithm Optimizations:**

- **Line of Sight**: Bresenham's algorithm for efficient ray casting
- **Pathfinding**: A* with early termination for movement validation
- **AI Decision Making**: Decision trees with early exit conditions
- **Combat Calculations**: Lookup tables for common computations

#### Performance Monitoring

**Built-in Profiling (Development):**

- FPS counter display (toggle with F12)
- Frame time graph (min/max/average)
- Memory usage display
- Thread activity monitor
- Event processing time tracking

**Logging and Diagnostics:**

- Performance warnings for slow operations (>100ms)
- Memory leak detection during development
- AI processing time per ship
- Render time breakdown by component

**Benchmarking Suite:**

- Automated performance tests via pytest-benchmark
- Combat scenario simulations (1v1, 5v5, 10v10)
- Sector loading benchmarks
- AI decision-making speed tests
- Memory usage profiling under load

#### Performance Degradation Handling

**Adaptive Quality:**

- Reduce sprite resolution on low-end systems (future)
- Disable non-essential animations if FPS drops below 30
- Simplify particle effects during performance stress
- Scale back AI complexity if processing too slow

**Graceful Degradation:**

- Never block on rendering (skip frames if necessary)
- Limit AI processing time with hard cutoffs
- Warn user if system struggles with performance
- Provide low-graphics mode option (future)

#### Target Hardware Validation

**Test Configurations:**

- **Minimum Spec**: 4 GB RAM, integrated graphics, dual-core CPU
- **Recommended Spec**: 8 GB RAM, discrete GPU, quad-core CPU
- **Development Spec**: 16 GB RAM, modern GPU, multi-core CPU

**Performance Acceptance Criteria:**

- ✅ 60 FPS on recommended spec during typical gameplay
- ✅ 30 FPS minimum on minimum spec in combat
- ✅ <2 second sector transitions on all test systems
- ✅ <512 MB memory usage with 10+ ships in sector
- ✅ Smooth UI interaction at all times (no lag on clicks)

### 9.4 Data Management

#### Configuration System

The game uses **TOML** format for all configuration files, providing:

- **Human-Readable Format**: Clean syntax with extensive comment support
- **Type Safety**: Better type inference and validation than JSON
- **Nested Structures**: Clear hierarchical organization for complex settings
- **Standard Library Support**: Python 3.14+ `tomllib` for reading, `tomli_w` for writing

#### Configuration Files Structure

```text
star_trek_retro_remake/config/
├── game_settings.toml    # Display, audio, controls, graphics options
├── game_data.toml        # Ship classes, factions, mission definitions
└── key_bindings.toml     # Keyboard, mouse, gamepad mappings

star_trek_retro_remake/assets/data/
├── sectors/
│   └── sol_system.toml   # Sector definitions with object arrays
└── missions/
    └── [mission_files.toml]
```

#### TOML Configuration Examples

**Game Settings:**

```toml
[display]
window_width = 1024
fullscreen = false
[game.grid_size]
galaxy = [10, 10]
sector = [20, 20, 5]
```

**Ship Data:**

```toml
[ship_classes.constitution]
name = "Constitution Class"
hull_integrity = 100
[ship_classes.constitution.systems.weapons]
phaser_arrays = 4
torpedo_capacity = 12
```

**Sector Data:**

```toml
[[objects]]
type = "starbase"
name = "Earth Spacedock"
position = [10, 10, 2]
services = ["repair", "resupply"]
```

#### Configuration Management

```python
from star_trek_retro_remake.src.engine.config_manager import (
    initialize_config_manager, load_config, get_config_value
)

# Initialize system
config_manager = initialize_config_manager("config/")

# Load complete files
settings = load_config("game_settings")
ship_data = load_config("game_data")

# Access specific values with dot notation
window_width = get_config_value("game_settings", "display.window_width", 1024)
phaser_count = get_config_value("game_data", "ship_classes.constitution.systems.weapons.phaser_arrays")
```

#### Save Data Management

- Game data (player progress, settings) will be stored in local TOML files
- Save and load functionality will be implemented for game progress
- Configuration changes persist automatically
- JSON fallback support during development transition

### 9.5 Localization

- The game will be developed in English
- No future plans for localization at this time

## 10. Production

### 10.1 Development Milestones

1. **Pre-Production**
   - Finalize game design document
   - Set up development environment
2. **Develop Core Systems**
   - Map rendering with z-levels
   - Turn-based mechanics
   - Basic starship movement
3. **Simple Entities**
   - Implement basic entities (starships, space stations)
4. **Basic Combat System**
   - Implement combat mechanics
   - Basic AI for enemy ships
5. **Resource Management**
   - Implement resource management systems
6. **To be determined**

### 10.2 Team Structure

- Indie developer (solo project)

### 10.3 Testing Strategy

#### Automated Testing (pytest)

**Unit Testing:**

- Target: 80%+ code coverage for core game logic
- Focus: Game mechanics, combat calculations, state transitions
- Framework: pytest with fixtures and parametrized tests
- Pattern: AAA (Arrange-Act-Assert) for all test cases

**Test Categories:**

- **Game Logic**: Movement, combat, resources, turn management
- **State Machine**: State transitions, mode switching, validation
- **Ship Systems**: Weapons, shields, engines, sensors functionality
- **AI Behavior**: Decision-making, targeting, tactical states
- **Data Management**: Configuration loading, save/load operations

**Integration Testing:**

- Controller-Model interactions
- State persistence across game modes
- Multi-entity scenarios (combat with multiple ships)
- Resource management across turns and missions

**Performance Testing:**

- Frame rate benchmarking (target: 60 FPS UI, 30 FPS minimum)
- Memory usage profiling (target: <512MB base assets)
- Load time measurements (2s sector transitions, 1s combat init)
- Object pooling efficiency validation

#### Manual Testing

**User Interface Testing:**

- PySide6 widget behavior and layout
- pygame-ce rendering validation
- User interaction flows and feedback
- Dialog and menu functionality
- Keyboard shortcuts and mouse controls

**Gameplay Testing:**

- Balance testing across difficulty levels
- Mission variety and progression pacing
- Combat scenarios and tactical depth
- Resource economy balance
- Player progression curves

**User Experience Testing:**

- Tutorial effectiveness
- Clarity of game mechanics
- UI responsiveness and feedback
- Error handling and recovery
- Accessibility features

#### Testing Tools

**Primary Tools:**

- pytest: Core testing framework
- pytest-cov: Code coverage reporting
- pytest-mock: Mocking and fixtures
- pytest-benchmark: Performance benchmarking

**Secondary Tools:**

- cProfile: Python profiling for performance bottlenecks
- memory_profiler: Memory usage analysis
- Git hooks: Pre-commit test execution
- CI/CD: Automated test runs on commits

#### Testing Schedule

**Development Phase:**

- Run unit tests after each code change
- Daily integration test suite execution
- Weekly full test suite with coverage report
- Monthly performance benchmarking

**Pre-Release:**

- Complete test suite execution
- Manual gameplay testing sessions (2-4 hours)
- Balance verification across all difficulty levels
- User acceptance testing with beta testers (future)

#### Test Data Management

**Test Fixtures:**

- Standard ship configurations
- Pre-built sector maps for testing
- Mock game states for various scenarios
- Reference combat outcomes for validation

**Test Coverage Goals:**

- Core game logic: 90%+ coverage
- State machine: 85%+ coverage
- Ship systems: 80%+ coverage
- UI controllers: 70%+ coverage
- Overall project: 80%+ coverage

### 10.4 Risk Assessment

- Intentionally left blank.

### 10.5 Resource Requirements

- Development will primarily require time and effort from the solo developer.

## 11. Marketing and Business

### 11.1 Marketing Strategy

- Open source and free project for my personal enjoyment
- No plans to market

### 11.2 Monetization Model

- N/A

### 11.3 Community and Support

*To be determined*

### 11.4 Post-Launch Content

*To be determined*

## 12. Legal and Compliance

### 12.1 Intellectual Property

- The game is a fan-made project set in the Star Trek universe.
- All intellectual property rights related to Star Trek are owned by their respective holders.
- The game will not be sold or monetized in any way.
- The game will include appropriate disclaimers stating that it is a fan-made project and not affiliated with or endorsed by the official Star Trek franchise.
- Any use of Star Trek intellectual property will be done in accordance with fair use principles and fan work guidelines.
- The game will avoid using copyrighted material such as music, images, or text from the Star Trek franchise without permission.
- The game will focus on original content inspired by the Star Trek universe rather than directly copying existing material.
- The developer will monitor for any potential intellectual property issues and take appropriate action if necessary.

### 12.2 Privacy and Data Protection

- The game will not collect any personal data from players.
- Any data stored (e.g., game progress) will be kept local to the player's device and not shared with third parties.

### 12.3 Content Rating Considerations

- The game will be designed for a general audience.
- Content will be appropriate for all ages, with no explicit material.

### 12.4 Platform Compliance

- The game will comply with all relevant platform guidelines and requirements for distribution.

## 13. Future Development

### 13.1 Post-Launch Features (v1.1+)

#### Advanced Crew Management

- Assign crew to different stations (e.g., weapons, engineering, science)
- Crew skills and experience affecting ship performance

#### Advanced Diplomacy

- Engage in diplomatic negotiations with other factions
- Form alliances or declare war
- Influence other factions through espionage or propaganda

### 13.2 Long-term Vision (v2.0+)

#### Simulation Mode

A real-time management mode overlay for existing turn-based gameplay:

**Real-Time System Management:**

- Ship systems operate continuously instead of turn-by-turn
- Power distribution adjusts in real-time via sliders
- Crew performs actions with time-based completion
- Environmental effects apply continuously (nebula interference, radiation)
- Toggle between turn-based and real-time modes per mission type

**Interconnected Ship Systems:**

- Fuel consumption directly affects engine output and available power
- High power usage generates heat requiring increased cooling
- Coolant systems draw power from main reactor
- Power distribution affects shields, weapons, sensors, and life support
- System failures cascade to related subsystems
- Engineering crew can reroute power in emergencies

**Complexity vs Turn-Based Balance:**

- Simulation mode optional for advanced players
- Turn-based remains primary gameplay mode
- Simulation mode offers higher rewards and challenges
- Real-time decisions require faster tactical thinking
- Pause capability for strategic planning in simulation mode

#### Starship Design and Customization

**Ship Customization System:**

- Visit starbases and shipyards for ship modifications
- Modular component replacement:
  - Weapon systems (phaser types, torpedo launchers)
  - Shield generators (capacity, regeneration rate, coverage)
  - Engine modules (impulse, warp, maneuvering)
  - Sensor arrays (range, resolution, types)
  - Hull reinforcement (armor plating, structural integrity)
- Component slots limit total upgrades
- Trade-offs: Power vs mass vs cost vs crew requirements

**Custom Ship Classes:**

- Design unique ship configurations from base hulls
- Name custom ship classes
- Save and share ship designs (future: community designs)
- Balance stats: Weapons, defense, speed, crew capacity
- Prototype testing missions required before full deployment
- Some components require minimum reputation or captain level

**Visual Customization:**

- Faction-specific paint schemes
- Hull markings and registry numbers
- Ship lighting and engine glow colors
- Custom ship icons for sector map

#### Fleet Management

**Admiral Promotion System:**

- Promotion to Admiral rank at Captain Level 20 and Reputation Rank 5
- Unlocks fleet command capabilities
- Maintain personal ship as flagship
- Command up to 5 additional ships in fleet (scales with experience)

**Fleet Operations:**

- Assign ships to fleet from available Starfleet vessels
- Each ship has crew, captain NPC, and status
- Fleet formations: Line, wedge, defensive screen, patrol spread
- Issue fleet-wide orders or individual ship commands
- Coordinate multi-ship tactics in large-scale battles

**Fleet Mission Types:**

- **Patrol Operations**: Multiple sectors simultaneously covered
- **Task Force Missions**: Combined fleet actions against major threats
- **Blockade Operations**: Control space lanes and borders
- **Convoy Escort**: Protect multiple civilian vessels
- **Fleet Exercises**: Training missions to improve fleet cohesion

**Fleet Management Challenges:**

- Resource allocation across multiple ships
- Personnel management (assign captains and key crew)
- Maintenance schedules and staggered repairs
- Coordinating fleet movements across galaxy map
- Balancing fleet composition for mission types

**Fleet Benefits:**

- Tackle missions impossible for single ship
- Control larger territories
- Increased reputation gains from fleet successes
- Unlock unique fleet-based missions and storylines
- Command multiple ship classes with different roles

## Appendices

### Appendix A: Reference Materials

#### Original Inspiration

**Classic Star Trek Games:**

- Star Trek (1971) - Original mainframe text game by Mike Mayfield
- Super Star Trek (1973) - BASIC version by David Ahl
- Star Trek: 25th Anniversary (1992) - Adventure/strategy hybrid
- Star Trek: Starfleet Command series - Tactical ship combat

#### Star Trek Universe References

**Television Series:**

- Star Trek: The Original Series (1966-1969) - Primary era inspiration
- Key episodes: "Balance of Terror", "Space Seed", "The Doomsday Machine"

**Technical Manuals:**

- Star Trek: The Original Series Sketchbook
- Star Trek Starship Recognition Manual
- Star Fleet Technical Manual by Franz Joseph
- Mr. Scott's Guide to the Enterprise

**Online Resources:**

- Memory Alpha (Star Trek wiki): <https://memory-alpha.fandom.com>
- Ex Astris Scientia (ship analysis): <http://www.ex-astris-scientia.org>
- Star Trek Technical Database: <http://www.shipschematics.net>

#### Game Design References

**Turn-Based Strategy Games:**

- XCOM series - Turn-based tactical combat mechanics
- FTL: Faster Than Light - Ship system management and events
- Into the Breach - Grid-based tactical gameplay
- Civilization series - Turn-based empire management

**Space Strategy Games:**

- Master of Orion series - 4X space strategy
- Star Traders: Frontiers - Space RPG/strategy hybrid
- Starflight - Classic space exploration
- Space Rangers 2 - Open-world space game

#### Technical Documentation

**Python and Libraries:**

- Python 3.14+ Documentation: <https://docs.python.org/3.14/>
- pygame-ce Documentation: <https://pyga.me/docs/>
- PySide6 Documentation: <https://doc.qt.io/qtforpython-6/>
- pytest Documentation: <https://docs.pytest.org/>

**Design Patterns:**

- Game Programming Patterns by Robert Nystrom
- Design Patterns: Elements of Reusable Object-Oriented Software (Gang of Four)
- Architecture Patterns for Game Engines

**Game Development:**

- Game Engine Architecture by Jason Gregory
- The Art of Game Design by Jesse Schell
- Rules of Play by Katie Salen and Eric Zimmerman

#### Development Tools

**Linux Development:**

- Ubuntu/Debian package management
- Git version control
- VS Code IDE
- Qt Designer for UI layout

**Asset Creation:**

- GIMP - Sprite and texture creation
- Inkscape - Vector graphics for UI elements
- Audacity - Audio editing (future)
- Tiled Map Editor - Grid-based map design (potential)

#### Community Resources

**Forums and Communities:**

- Python Game Development subreddit: r/pygame
- Star Trek subreddit: r/startrek
- Game Dev subreddit: r/gamedev
- Linux Gaming: r/linux_gaming

**Open Source Projects:**

- Similar turn-based strategy games on GitHub
- pygame-ce example projects
- PySide6 application examples

### Appendix B: Glossary

#### Game Terms

**Action Points (AP)**: Resource spent per turn for actions. Ships have 5 AP/turn. Movement: 1 AP/cell, phasers: 1 AP, torpedoes: 2 AP.

**Combat Mode**: Tactical turn-based ship combat on grid-based map with z-levels.

**Component**: Modular ship subsystem (weapons, shields, engines, sensors) that can be damaged, upgraded, or replaced.

**Facing**: Ship orientation in degrees (0-315° in 45° increments). Affects firing arcs, shields, and movement.

**Firing Arc**: 270° forward cone where weapons can target. Ships cannot fire behind.

**Galaxy Map**: 10x10 grid showing all sectors for strategic navigation.

**Initiative**: Determines turn order. Higher acts first. Player: 10, NPCs: 6-9.

**Line of Sight (LoS)**: Unobstructed path between grid positions. Required for targeting and detection.

**Object Pool**: Optimization reusing game objects instead of creating/destroying them.

**Sector Map**: 15x15x5 grid representing single sector with 3D z-level support.

**Shield Facing**: Four directional shield zones (forward, aft, port, starboard) absorbing damage independently.

**State Machine**: Pattern managing transitions between game modes (Main Menu, Galaxy Map, Sector Map, Combat).

**Turn**: Complete cycle where entities execute actions in initiative order.

**Z-Level**: Vertical layer (0-4) representing altitude/depth in space. Ships can move between levels.

#### Star Trek Terms

**Constitution Class**: Main Federation starship in Kirk era (USS Enterprise NCC-1701). Balanced cruiser.

**Deflector Shields**: Energy barrier protecting ships from weapons and hazards. Four directional facings.

**Dilithium**: Rare element regulating matter/antimatter reactions in warp cores for FTL travel.

**Federation**: United Federation of Planets, democratic alliance of Earth and member worlds.

**Gorn Hegemony**: Reptilian species. Strong, territorial, slow but powerful ships.

**Impulse Drive**: Sublight propulsion using fusion reactors for in-system travel and combat.

**Klingon Empire**: Warrior empire, often hostile to Federation. Values honor and combat.

**LCARS**: Library Computer Access/Retrieval System. Federation UI style (design inspiration).

**Nacelle**: Warp engine component with warp coils. Vulnerable, critical for FTL.

**Orion Syndicate**: Criminal organization. Known for piracy and smuggling.

**Phaser**: Phased Array by Stimulated Emission of Radiation. Primary Federation energy weapon.

**Photon Torpedo**: Antimatter warhead. High damage, limited ammunition.

**Romulan Star Empire**: Secretive empire from Vulcan exiles. Masters of cloaking and tactics.

**Starbase**: Large orbital/deep space station. Repairs, supplies, mission briefings, command.

**Starfleet**: Military, exploration, and diplomatic service of the Federation.

**Tholian Assembly**: Crystalline beings with exotic energy tech. Territorial, use web weapons.

**Warp Drive**: FTL propulsion via subspace field. Warp factors 1-9.

**Warp Speed**: FTL velocity in warp factors. Warp 1 = light speed, Warp 6 = cruising speed.

#### Technical Terms

**AAA Pattern**: Testing pattern: Arrange setup, Act by calling code, Assert results.

**Component Pattern**: Complex objects composed of smaller, reusable components rather than inheritance.

**ECS (Entity Component System)**: Entities as containers for components, systems process components. Simplified to Component Pattern in this game.

**GameObject**: Base class for interactive entities (ships, stations, projectiles) with position and state.

**Isometric View**: 2.5D projection showing 3D space at an angle with width, depth, and height.

**MVC (Model-View-Controller)**: Architecture separating game logic (Model), rendering (View), and input (Controller).

**Object Pooling**: Memory pattern reusing inactive objects instead of allocating/deallocating repeatedly.

**State Machine**: Model managing discrete states and transitions based on events/conditions.

**TOML (Tom's Obvious Minimal Language)**: Configuration file format. Human-readable, type-safe.

**Turn-Based**: Time advances in discrete turns rather than real-time, allowing strategic planning.

#### Abbreviations

**AI**: Artificial Intelligence (NPC behavior)
**AP**: Action Points (turn resource)
**FPS**: Frames Per Second (performance metric) or First Person Shooter (game genre)
**FTL**: Faster Than Light (warp drive)
**HP**: Hull Points (ship durability)
**LoS**: Line of Sight (visibility)
**NPC**: Non-Player Character (AI-controlled entities)
**TOS**: The Original Series (Star Trek 1966-1969)
**UI**: User Interface (menus, HUD, dialogs)
**UX**: User Experience (interaction design)
**XP**: Experience Points (progression currency)

### Appendix C: Change Log

See `/docs/CHANGELOG.md` for complete version history and detailed change information.

**Quick Reference:**

- Current version: v0.0.20 (October 30, 2025)
- Latest milestone: Basic Combat System implemented
- Next milestone: Resource Management System

**Recent Major Changes:**

- v0.0.20: Combat system with weapons, shields, AI, and target selection
- v0.0.19: UI to game logic connections
- v0.0.18: Turn-based game loop with initiative and action points
- v0.0.16: Complete PySide6 + pygame-ce integration
- v0.0.15: Z-level distance indicators
- v0.0.13: Z-level reference lines
- v0.0.12: Basic starship entities
- v0.0.10: Initial PySide6 integration
- v0.0.3: Isometric grid with z-levels

### Appendix D: Credits and Acknowledgments

- Special thanks to the Star Trek community for their inspiration and support.
- Acknowledgment of any external libraries, tools, or resources used in the development of the game.
