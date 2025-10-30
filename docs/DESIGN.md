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
- [4.4 Combat Map](#44-combat-map)
- [4.5 Locations and Environments](#45-locations-and-environments)
- [4.6 Factions and NPCs](#46-factions-and-npcs)

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

### Current Project Status (v0.0.20 - October 30, 2025)

**Project Phase:** Core Systems Implementation (Pre-Alpha)

**Recently Completed:**

- Basic combat system with weapons, shields, and AI (v0.0.20)
- UI to game logic connections (v0.0.19)
- Turn-based game loop with initiative and action points (v0.0.18)
- Complete PySide6 + pygame-ce UI integration (v0.0.10, v0.0.16, v0.0.18)
- Isometric grid rendering with z-levels (v0.0.3-v0.0.15)
- Basic starship entities with visual representation (v0.0.12)
- Starship movement system with turn integration (v0.0.3-v0.0.18)

**Current Focus:** Ready for resource management system implementation

**Next Major Goal:** Add energy allocation, supplies, crew morale, and maintenance

### In Progress Milestones

Currently none - ready to start next milestone!

### Next Milestones

#### Implement Basic Combat System

- Weapon firing mechanics (phasers and torpedoes)
  - Line of sight and firing arc calculations based on orientation
  - Weapon range and accuracy calculations
  - Visual feedback for weapon effects on grid
- Shield and damage calculations
  - Shield facing system (forward, aft, port, starboard)
  - Damage penetration and hull damage
  - Shield recharge mechanics
- Combat resolution with positioning and orientation factors
  - Range modifiers for weapons
  - Cover and obstruction mechanics
  - Critical hit system
- Basic AI for enemy ship behavior (patrol, attack, flee)
  - Simple state machine for AI decision-making
  - Target selection and threat assessment
  - Movement and firing patterns

#### Implement Resource Management System

- Energy allocation system
  - Power distribution sliders for shields, weapons, engines, sensors
  - Energy consumption per action
  - Energy regeneration from impulse/warp engines
- Supplies tracking (fuel, medical supplies, spare parts)
  - Consumption rates based on activity
  - Resupply at starbases
  - Mission impact of low supplies
- Crew morale and efficiency systems
  - Morale affected by combat success/failure, casualties, mission duration
  - Efficiency bonuses/penalties for ship systems
  - Rest and shore leave mechanics at starbases
- Ship system condition and maintenance
  - Damage accumulation and repair mechanics
  - System efficiency degradation
  - Repair costs and time requirements

#### Implement Sector Map Enhancements

- Add space stations (starbases) to sector maps
  - Docking and undocking mechanics
  - Repair and resupply services
  - Mission briefing and assignment
- Add environmental objects
  - Asteroids (providing cover, collision damage)
  - Nebulae (sensor interference, movement penalties)
  - Debris fields (navigation hazards)
- Implement sensor system
  - Short-range and long-range sensor modes
  - Detection of ships and objects
  - Sensor interference from environment

#### Implement Dialog and Menu Systems

- Mission briefing dialogs
  - Display mission objectives and parameters
  - Accept/decline mission options
  - Mission reward information
- Ship status dialogs
  - Detailed system status reports
  - Crew roster and assignment
  - Damage reports and repair priorities
- Settings dialog window
  - Display configuration options
  - Apply and save settings changes
  - Key binding customization
- Save/load game functionality through File menu
  - Game state serialization to TOML
  - Load saved games with state restoration
  - Multiple save slot management

#### Implement Galaxy Map Mode

- Galaxy map grid rendering (10x10 sectors)
- Sector navigation and selection
- Federation, Neutral, and Hostile zone visualization
- Sector information display (name, control, threat level)
- Travel time and random encounter system
- Transition from Galaxy to Sector map states

### Completed Milestones

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

### 2.4 Victory Conditions

Victory conditions will vary based on the game mode and specific missions. Generally, players can achieve victory by:

- Successfully completing mission objectives
- Defeating enemy starships in combat
- Establishing diplomatic relations with alien species
- Exploring and charting new star systems

## 3. Gameplay

### 3.1 Core Gameplay Loop

The game operates on a turn-based system where a certain number of actions can be taken each turn based on ship capabilities, resources, and mode.

#### 3.1.1 Time Scale

Each turn represents a fixed time interval in the game world:

- Seconds or minutes in combat
- Hours or days during sector map exploration
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

- Captain experience
- Crew experience
- Reputation with factions
- Reputation with commanding officers
- Starship upgrades and customization

### 3.4 Difficulty and Balance

*[To be defined]*

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

### 4.4 Combat Map

- The combat map will be separate from the sector map.
- It will be randomly generated based on the sector environment.
- The environment may include:
  - Open space
  - Nebulae (affecting sensors and movement)
  - Asteroid fields (providing cover and obstacles)
  - Debris fields (remnants of destroyed ships or stations)
- Movement mechanics will be similar to the sector map.
- Additional gameplay mechanics will apply (e.g., cover, line of sight).
- Time scale will be shorter (seconds or minutes per turn).

### 4.5 Locations and Environments

- The galaxy map will be comprised of sectors with different characteristics:
  - Safe zones (federation-controlled space)
  - Neutral zones (uncharted space)
  - Hostile zones (enemy-controlled space)
  - Travel between sectors may involve random encounters or scripted events
  - Time scale will be long (days or weeks per turn)

- The sector map will feature various locations and environments:
  - Star systems (with planets, moons, asteroids)
  - Space stations (for repairs, resupply, trading)
  - Anomalies (black holes, nebulae, wormholes)
  - Nebulae (affecting sensors and movement)
  - Asteroid fields (providing cover and obstacles)
  - Debris fields (remnants of destroyed ships or stations)
  - Time scale will be medium (minutes or hours per turn)

- The combat map will be separate from the sector map.
  - It will be randomly generated based on the sector environment.
  - The environment may include:
    - Open space
    - Nebulae (affecting sensors and movement)
    - Asteroid fields (providing cover and obstacles)
    - Debris fields (remnants of destroyed ships or stations)
  - Movement mechanics will be similar to the sector map.
  - Additional gameplay mechanics will apply (e.g., cover, line of sight).
  - Time scale will be shorter (seconds or minutes per turn).

### 4.6 Factions and NPCs

- Factions will include:
  - The United Federation of Planets
  - Klingon Empire
  - Romulan Star Empire
  - The Gorn Hegemony
  - The Tholian Assembly
  - The Orion Syndicate

- NPC starships will belong to various factions and have different behaviors:
  - Friendly (allied ships, neutral traders)
  - Hostile (enemy ships, pirates)
  - Neutral (independent ships, explorers)

- Will be able to interact with NPCs through:
  - Combat
  - Diplomacy
  - Trading

## 5. Game Mechanics

### 5.1 Starships

- Player is the captain of a starship
- The starship is represented on the sector map by a sprite/icon
- The representation will indicate the starship's orientation (facing direction)
- Starships have attributes:
  - Hull integrity
  - Shield strength
  - Weapon systems
    - Phaser arrays
    - Photon torpedoes
  - Engine power
  - Sensor range
  - Sensor modes
  - Deflector dish
  - Crew efficiency
  - Crew morale
  - Transporters
  - Shuttles
- Starships can move between cells on the sector map
  - Movement cost may vary based on:
    - Ship capabilities
    - Distance
    - Engine power
    - Environmental factors (e.g., nebulae, asteroid fields)
  - Starships have a vector-based movement system allowing movement in all directions
  - At the end of a turn the starship's orientation will determine its facing for the next turn
  - Starship orientation will affect weapon firing arcs, shield coverage, and sensor range
- Starships can engage in combat with enemy ships
- Starships can dock at space stations for repairs and resupply

### 5.2 Combat System

- Turn-based combat system
- Combat is initiated on the sector map when the player's starship encounters enemy ships or dynamic combat missions are initiated.
- Each starship has a set number of actions per turn based on ship capabilities, Captain experience, crew efficiency, crew stats, etc.
- Actions include:
  - Movement (thrust in any direction, rotate)
  - Firing weapons (phasers, torpedoes)
  - Activating shields
  - Using special abilities (e.g., evasive maneuvers, sensor jamming)
- Combat resolution will consider factors such as:
  - Weapon accuracy and damage
  - Shield strength and hull integrity
  - Starship positioning and orientation
  - Crew efficiency and morale
  - Environmental factors (e.g., nebulae, asteroid fields)
  - Starship systems status (e.g., damaged weapons, depleted shields)
- Successful combat will reward the player with resources, reputation, and progression
- Options to resolve combat through diplomacy or retreat may be available in certain situations

### 5.3 Resource Management

Players must manage ship resources:

- Energy allocation (shields, weapons, engines)
- Sensor modes (long-range, short-range, passive)
- Supplies (fuel, food, medical supplies)
- Crew morale (affected by mission success, encounters, and ship conditions)
- Condition and upkeep of ship systems (weapons, shields, engines)

### 5.4 Mission System

- Missions will be generated based on the player's location and actions
- Missions may include exploration, combat, diplomacy, and resource gathering
- Completing missions will reward the player with resources, reputation, and progression

### 5.5 Economy and Trading

- Economy and trading systems will be basic in the initial release
- Players can trade resources at space stations
- Future plans may include a more complex economy with supply and demand dynamics

### 5.6 AI and NPCs

- Basic AI for enemy starships
- NPC starships will have simple behaviors (patrolling, attacking, fleeing)
- Future plans may include more advanced AI behaviors and interactions

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

#### 6.2.1 Layout Option 1: "Twin Docks + Splitter" (Power-User)

**Use Case:** Persistent Status on the left and Controls/Log on the right

**Layout Sketch:**

```text
+---------------------------------------------------------------+
| Toolbar                                                       |
+-------------+---------------------------+---------------------+
| Left Dock   |        CENTRAL MAP        | Right Dock          |
| (Status)    |      (QSplitter center)   | (Controls/Log tabs) |
+-------------+---------------------------+---------------------+
| Bottom Dock: Message Log / Event Feed                         |
+---------------------------------------------------------------+
```

**Designer Components:**

- **Left QDockWidget (StatusDock):** QVBoxLayout with:
  - Ship portrait/icon
  - QProgressBars (Hull/Shields/Energy)
  - Resource meters
- **Right QDockWidget (ControlDock):** QTabWidget with:
  - Actions (buttons + grouped QGroupBox)
  - Sensors (range sliders, toggles)
  - Systems (tree or table view)
- **Bottom QDockWidget (LogDock):** QPlainTextEdit (read-only) for combat log/events
- **Center:** QWidget with a vertical QSplitter or stacked center holding the map placeholder
- All three docks closable, floatable, movable; save/restore geometry

**Pros:** Highly flexible, great for complex sessions
**Cons:** Requires tuning for sensible defaults

#### 6.2.2 Layout Option 2: "Right-Rail Tactical" (Simple, Focused)

**Use Case:** Early prototypes; Sector/Combat with a single info/control stack

**Layout Sketch:**

```text
+--------------------------------------------------------+
|  Toolbar / Menubar                                     |
+------------------------------+-------------------------+
|          CENTRAL MAP         |  Status / Actions       |
|      (pygame surface)        |  (tabs: Status,         |
|                              |   Actions, Minimap)     |
+------------------------------+-------------------------+
|  Turn/phase bar (bottom)                               |
+--------------------------------------------------------+
```

**Designer Components:**

- **Base:** QMainWindow
- **Central:** QWidget → QVBoxLayout → placeholder QWidget named GameSurface (later used to host pygame surface) + a bottom QWidget (TurnBar) with QHBoxLayout for "End Turn", AP, phase indicator
- **Right Rail:** QDockWidget (dock right, allowed areas: Left|Right). Inside: QTabWidget with tabs:
  - StatusTab (QFormLayout): hull/shields/energy bars (use QProgressBar)
  - ActionsTab (QVBoxLayout): buttons ("Move", "Fire", "Scan", "Evasive")
  - MapTab (QVBoxLayout): mini-map QLabel (future pixmap) + legend
- **Toolbars:** Top QToolBar with mode buttons (Galaxy/Sector/Combat), separator, zoom in/out
- **Resizing:** Set central layout stretch (map=1) and give right dock a Fixed minimum width (e.g., 300 px). Map placeholder QSizePolicy = Expanding, Expanding

**Pros:** Fast to build, great for smaller screens
**Cons:** Single column can get tall; tabs hide info

#### 6.2.3 Layout Option 3: "Dashboard HUD" (Panel Ring)

**Use Case:** Zero hidden info; everything visible at once on big monitors

**Layout Sketch:**

```text
+---------------------------------------------------------------+
| Toolbar                                                       |
+---------+---------------------------------------+-------------+
| Status  |               CENTRAL MAP             | Actions     |
| (left)  |                                       | (right)     |
+---------+---------------------------------------+-------------+
|                 Bottom: Log + Turn Bar                        |
+---------------------------------------------------------------+
```

**Designer Components:**

- **Left Dock (StatusDock):** Compact QGridLayout HUD (bars + icons)
- **Right Dock (ActionDock):** Grouped controls:
  - Movement (arrows/rotate)
  - Weapons (phasers/torps)
  - Utilities (scan, tractor)
- **Bottom:** QSplitter horizontal with Log (QPlainTextEdit) and TurnBar (QHBoxLayout)
- **Center:** Map placeholder with strong "expanding" policy; side docks min width ~260–300 px

**Pros:** No tab-hunting; ideal for Combat mode
**Cons:** Needs space; can feel busy on laptops

#### 6.2.4 Layout Option 4: "Mode-Stacked Center" (Mode-Aware)

**Use Case:** Switch content per Galaxy/Sector/Combat while keeping the chrome

**Layout Sketch:**

```text
+---------------------------------------------------------------+
| Menus/Toolbar                                                 |
+-----------------------+---------------------------------------+
| Left/Right Docks      |  QStackedWidget (center):             |
| (shared)              |  [GalaxyView | SectorView | CombatView]|
+-----------------------+---------------------------------------+
| Bottom Dock: Log / Turn Bar                                   |
+---------------------------------------------------------------+
```

**Designer Components:**

- **Center:** QStackedWidget named ModeStack with three pages:
  - GalaxyPage: simple QGridLayout (galaxy map + filters)
  - SectorPage: main map placeholder + small QFrame overlay host (optional)
  - CombatPage: map + target panel strip (mini right rail) via inner QHBoxLayout
- Use toolbar's mode buttons to switch ModeStack->setCurrentIndex(...)
- Surrounding docks (Status/Actions/Log) stay mounted across modes

**Pros:** Clean separation by mode; test each page in isolation
**Cons:** Slightly more Designer wiring

#### 6.2.5 Layout Option 5: "Notebook Right-Side" (Tabbed Control Center)

**Use Case:** Single, predictable place for all non-map UI

**Layout Sketch:**

```text
+---------------------------------------------------------------+
| Toolbar                                                       |
+------------------------------+--------------------------------+
|          CENTRAL MAP         |  QTabWidget:                   |
|                              |  [ Status | Actions | Intel ]  |
|                              |  [ Minimap | Systems | Cargo ] |
+------------------------------+--------------------------------+
| Bottom: Turn Bar + Log                                        |
+---------------------------------------------------------------+
```

**Designer Components:**

- **Right:** QDockWidget → QTabWidget with 4–6 tabs. Each tab uses QFormLayout/QGridLayout
- Add QToolButtons in the tab bar's corner (Designer: tabBarCornerWidget) for quick actions (End Turn, Center on Player)
- Central + Bottom as in Option 1

**Pros:** Very predictable; tidy .ui
**Cons:** Tab switching during combat can be a little slower

#### 6.2.6 Layout Decision

**Selected Layout:** Layout Option 2 ("Right-Rail Tactical")

**Rationale:**

- Simplicity and focus on essential information
- Fast to build for initial development
- Great for smaller screens
- Suitable for early prototypes

**Future Consideration:**

- Final layout will be determined based on playtesting and user feedback during development
- May transition to other layouts for specific game modes

### 6.3 Input Controls

- The game will support both keyboard and mouse input
- Interactions will be primarily handled through mouse clicks, keyboard shortcuts, menu selections, sliders, dialog boxes, etc.
- Mouse input will be used for interacting with the game world (e.g., clicking on objects directly within the map, selecting objects in the map, etc.)

### 6.4 Accessibility

- No specific accessibility features are planned at this time.

## 7. Audio and Visual Design

### 7.1 Art Style

*[To be defined]*

### 7.2 Audio Design

- Deferred to future development phases

### 7.3 Visual Effects

- Deferred to future development phases

## 8. Narrative and Storytelling

### 8.1 Story Overview

- There will be very minimal narrative elements in the initial release
- The player will take on the role of a starship captain in the Star Trek universe
- The game will focus on exploration, tactical combat, and resource management
- Story elements will be introduced through mission briefings, encounters with NPCs, and events on the sector map

### 8.2 Characters

*[To be defined]*

### 8.3 Dialogue System

*[To be defined]*

### 8.4 Cutscenes and Presentation

- No cutscenes are planned

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

- **Linux Only**: All development targets Linux exclusively
- No Windows or macOS support planned - code and design are Linux-specific

### 9.3 Performance Requirements

- The game should maintain a stable frame rate of 60 FPS during gameplay
- Load times for game assets should be minimized through efficient resource management
- The game should be optimized for performance on target platforms
- Memory usage should be kept within reasonable limits to ensure smooth gameplay
- Multi-threading is planned with separate threads for:
  - Game logic
  - Rendering
  - User interface
  - Resource loading

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

**Game Settings (`game_settings.toml`):**

```toml
[display]
window_width = 1024     # Default window width in pixels
window_height = 768     # Default window height in pixels
fullscreen = false      # Start in windowed mode
vsync = true           # Enable vertical sync

[game.grid_size]
galaxy = [10, 10]              # Galaxy map dimensions
sector = [20, 20, 5]           # Sector map with z-levels
```

**Ship Data (`game_data.toml`):**

```toml
[ship_classes.constitution]
name = "Constitution Class"
hull_integrity = 100
crew_capacity = 430

[ship_classes.constitution.systems.weapons]
phaser_arrays = 4
torpedo_tubes = 2
torpedo_capacity = 12
```

**Sector Data (`sol_system.toml`):**

```toml
sector_id = "sol_system"
name = "Sol System"
grid_size = [20, 20, 5]

[[objects]]
type = "starbase"
name = "Earth Spacedock"
position = [10, 10, 2]
services = ["repair", "resupply", "training"]

[[objects]]
type = "planet"
name = "Earth"
position = [10, 10, 1]
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

- Fully AI tested initially
- Manual testing for user interface and gameplay mechanics

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

- To be determined

### 11.4 Post-Launch Content

- To be determined

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

- A real-time management mode where the player has to manage ship systems and crew in real-time
- Complex ship systems that are strongly interconnected:
  - Fuel consumption affecting engine power and weapon systems
  - High power usage increases coolant requirements
  - Increased cooling needs can lead to less resource allocation for other systems
  - Power distribution affecting shields, weapons, and sensors

#### Starship Design and Customization

- Players can customize their starship's capabilities (weapons, shields, engines, etc.) at starbases and shipyards
- Modular ship components (e.g., engines, weapons, shields) can be upgraded or replaced
- Players can design their own starship classes with unique attributes and abilities

#### Fleet Management

- Players can earn a promotion to Admiral and command a fleet of starships
- Players can manage multiple starships within their fleet
- Fleets can be assigned to different missions or tasks
- Players can issue orders to individual starships or the entire fleet

## Appendices

### Appendix A: Reference Materials

*[To be defined]*

### Appendix B: Glossary

*[To be defined]*

### Appendix C: Change Log

*[To be defined]*

### Appendix D: Credits and Acknowledgments

- Special thanks to the Star Trek community for their inspiration and support.
- Acknowledgment of any external libraries, tools, or resources used in the development of the game.
