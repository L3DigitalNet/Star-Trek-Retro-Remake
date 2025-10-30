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

**Primary Motivations:**

- **Exploration**: Discover new sectors, anomalies, and uncharted space
- **Tactical Mastery**: Perfect combat strategies and ship management
- **Career Advancement**: Rise through Starfleet ranks from Captain to Admiral
- **Resource Optimization**: Efficiently manage energy, supplies, and crew morale
- **Faction Relations**: Build reputation with Federation allies and navigate diplomatic challenges

**Short-term Goals:**

- Complete assigned missions successfully
- Defeat enemy ships in tactical combat
- Maintain ship systems and crew morale
- Explore and chart new sectors
- Gather resources and supplies at starbases

**Long-term Goals:**

- Achieve promotion to higher Starfleet ranks
- Unlock advanced ship classes and upgrades
- Build maximum reputation with Federation Command
- Master all combat scenarios and difficulty levels
- Complete the full sector exploration campaign

### 2.4 Victory Conditions

Victory conditions will vary based on the game mode and specific missions. Generally, players can achieve victory by:

**Mission-Based Victory:**

- Successfully completing all primary mission objectives
- Achieving optional secondary objectives for bonus rewards
- Maintaining acceptable casualty and resource loss thresholds
- Completing time-sensitive missions before deadline expires

**Combat Victory:**

- Defeating all enemy starships in combat encounter
- Forcing enemy ships to retreat or surrender
- Protecting allied vessels until reinforcements arrive
- Surviving ambush scenarios with minimal damage

**Exploration Victory:**

- Charting 100% of assigned sector territory
- Discovering all anomalies and points of interest
- Establishing first contact with new alien species
- Gathering complete scientific data on sector phenomena

**Campaign Victory:**

- Achieving Admiral rank through sustained performance
- Completing all story missions in the campaign
- Maintaining "Excellent" reputation with Starfleet Command
- Successfully defending Federation space from major threats

**Failure Conditions:**

- Player ship destroyed with no respawn available (Admiral Mode)
- Critical mission failure resulting in court-martial
- Reputation falling to "Disgraced" status
- Abandoning post or desertion during critical missions

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

#### Captain Experience System

**Experience Points (XP):**

- Earned through combat victories, mission completion, and exploration
- Required XP scales exponentially: Level N requires N * 100 XP

**Captain Levels:**

- Level 1-5: Junior Captain (starting experience)
- Level 6-10: Captain (competent command)
- Level 11-15: Senior Captain (veteran status)
- Level 16-20: Commodore (multi-ship authority)
- Level 21+: Admiral (fleet command capability)

**Captain Skills:**

- **Command**: +5% crew efficiency per level
- **Tactical**: +2% weapon accuracy per level
- **Science**: +10% sensor range per level
- **Engineering**: +5% repair speed per level

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

- Higher ranks unlock better missions
- Increased resource allocation from starbases
- Access to advanced ship upgrades
- Priority docking and repair services

**Reputation Gains/Losses:**

- Mission success: +10 to +50 reputation
- Mission failure: -20 to -100 reputation
- Civilian casualties: -50 reputation
- Destroying allied ships: -200 reputation
- Heroic actions: +100 reputation

#### Starship Upgrades

**Upgrade Categories:**

- Weapons Systems (increased damage, reduced cooldown)
- Shield Systems (increased capacity, faster recharge)
- Engine Systems (increased speed, reduced AP cost)
- Sensor Systems (increased range, better accuracy)

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
  - Standard AI behavior patterns

- **Captain Mode**: Challenging tactical gameplay
  - Enhanced enemy stats (+25% hull/shields)
  - Standard resource generation
  - More aggressive AI tactics
  - Reduced action points (4 AP per turn)

- **Admiral Mode**: Expert players only
  - Maximum enemy stats (+50% hull/shields)
  - Resource scarcity (-25% regeneration)
  - Advanced AI with tactical coordination
  - Permadeath for crew members

#### Balance Considerations

**Ship Class Balance:**

- Constitution Class: Balanced all-rounder (baseline)
- Miranda Class: Faster, lighter shields (-20% hull, +30% speed)
- Excelsior Class: Heavy cruiser (+40% hull, -20% maneuverability)

**Weapon Balance:**

- Phasers: 10-15 damage, 0.5s cooldown, 85% accuracy, 1 AP
- Torpedoes: 25-35 damage, 1.0s cooldown, 75% accuracy, 2 AP
- Range vs. Damage: Close range (+20% damage), Long range (-30% damage)

**Resource Economy:**

- Energy regenerates 10 units/turn (passive)
- Shield regenerates 5 points/turn when not in combat
- Supplies consumed 1 unit/turn during travel, 3 units/turn in combat
- Crew morale decreases 2 points/week without shore leave

**Combat Pacing:**

- Average combat: 5-10 turns
- Boss encounters: 15-25 turns
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

### 4.4 Combat Map

**Overview:**
Combat occurs on a separate tactical map generated from the sector environment where the encounter was initiated. The combat map provides a focused arena for turn-based tactical ship combat.

**Map Structure:**

- Grid-based 15x15 cells with 3-5 z-levels (smaller than sector maps)
- Same isometric perspective as sector map for consistency
- Generated procedurally based on sector environment type
- Limited battlefield encourages tactical positioning

**Environmental Features:**

*Open Space Combat:*

- Clear lines of sight
- No movement penalties
- Emphasizes maneuver and positioning
- Standard sensor range

*Nebula Combat:*

- Reduced sensor range (-50%)
- Visual obstruction (partially transparent fog effect)
- Movement penalties (-1 AP per move)
- Energy weapon accuracy reduced (-10%)
- Ideal for ambushes and stealth tactics

*Asteroid Field Combat:*

- Dense obstacles providing cover
- Line of sight frequently blocked
- Movement requires careful navigation
- Collision damage from careless flying
- Cover bonuses (+20% damage reduction when behind asteroids)

*Debris Field Combat:*

- Scattered wreckage from destroyed ships/stations
- Partial cover and obstacles
- Salvage opportunities (repair materials)
- Navigation hazards
- Thematic for battles near stations or previous engagements

**Combat Mechanics:**

- Turn-based initiative system (same as sector map)
- Facing and firing arcs critical for weapons
- Shield facings and directional damage
- Line of sight calculations for weapons and sensors
- Cover and obstruction provide tactical depth

**Time Scale:**

- Each turn represents seconds to minutes
- Fast-paced compared to sector exploration
- Urgency in decision-making

### 4.5 Locations and Environments

This section describes the types of locations and environmental features found throughout the game world across all three map types.

#### Galaxy Map Environments

**Federation Core Sectors:**

- High security, frequent patrols
- Numerous starbases and support facilities
- Safe travel with minimal random encounters
- Mission focus: Patrol, escort, diplomacy

**Border Sectors:**

- Mixed Federation/Neutral control
- Moderate threat level
- Starbases less frequent
- Mission focus: Patrol, reconnaissance, border defense

**Neutral Zone Sectors:**

- Uncharted or disputed space
- High exploration potential
- Random encounters common
- Mission focus: Exploration, first contact, scientific surveys

**Hostile Territory Sectors:**

- Enemy-controlled space (Klingon, Romulan)
- High danger, aggressive encounters
- Limited friendly facilities
- Mission focus: Combat, espionage, rescue operations

**Unexplored Sectors:**

- Unknown composition and threats
- High risk/high reward exploration
- No friendly support available
- Mission focus: Deep space exploration, discovery

#### Sector Map Locations

**Starbases:**

- Major Federation facilities orbiting planets or in deep space
- Services: Repairs, resupply, crew rest, ship upgrades
- Mission briefings and strategic coordination
- Safe haven from hostile forces
- Docking and undocking mechanics

**Star Systems:**

- Central star with orbiting planets and moons
- Planets: Habitable worlds, gas giants, barren rocks
- Moons: Natural satellites with varying compositions
- Asteroid belts: Mining opportunities, navigation hazards
- Scientific interest and survey missions

**Space Stations:**

- Smaller than starbases, varied purposes
- Civilian: Trading posts, research stations
- Military: Defense platforms, sensor arrays
- Neutral: Independent or alien-operated facilities
- May be damaged, abandoned, or hostile

**Anomalies:**

- Black Holes: Extreme gravity wells, sensor interference, navigation hazards
- Wormholes: Potential shortcuts or story elements (future)
- Subspace Rifts: Exotic phenomena affecting sensors and systems
- Temporal Anomalies: Story-driven unusual events
- Scientific value and potential dangers

**Environmental Objects:**

- Nebulae: Gas clouds affecting sensors and movement
- Asteroid Fields: Dense rock formations providing cover
- Debris Fields: Wreckage from battles or destroyed structures
- Comet Trails: Visual features and navigation challenges
- Ion Storms: Temporary sensor and communications disruption

#### Environmental Effects on Gameplay

**Sensor Impact:**

- Nebulae: Reduce detection range, hide enemy ships
- Ion Storms: Intermittent sensor blackouts
- Asteroid Fields: Line of sight obstruction

**Movement Impact:**

- Dense asteroid fields: Increased AP cost per move
- Nebulae: Speed reduction penalties
- Debris fields: Navigation hazard checks

**Combat Impact:**

- Cover from asteroids: Damage reduction
- Nebula concealment: Harder to target
- Environmental hazards: Collision damage potential

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

**First Officer**

- **Role**: Executive officer and tactical advisor
- **Combat Benefits**: Provides tactical advice during combat encounters
- **Special Ability**: Can assume command if captain is incapacitated
- **Progression**: Experience level affects AP pool (+1 AP at level 5)
- **Skills**: Command, Tactics, Leadership

**Chief Engineer**

- **Role**: Manages all ship systems and power distribution
- **Combat Benefits**: Provides repair estimates and damage assessments
- **Special Ability**: Emergency repairs during combat (2 AP cost, level 5+)
- **Progression**: Reduces repair time and improves system efficiency
- **Skills**: Engineering, Warp Theory, Systems Management

**Chief of Security / Tactical Officer**

- **Role**: Manages weapons systems and ship security
- **Combat Benefits**: Provides targeting recommendations and threat analysis
- **Special Ability**: Increases weapon accuracy (+5% at level 5)
- **Progression**: Unlocks advanced targeting solutions
- **Skills**: Tactics, Weapons Systems, Security Protocols

**Science Officer**

- **Role**: Analyzes anomalies, alien technology, and enemy ships
- **Combat Benefits**: Provides detailed sensor data and weakness identification
- **Special Ability**: Can identify enemy ship classes and weak points
- **Progression**: Improves sensor range and analysis speed
- **Skills**: Science, Sensors, Xenobiology

**Helm Officer**

- **Role**: Controls ship movement and navigation
- **Combat Benefits**: Provides navigation efficiency and evasive maneuvers
- **Special Ability**: Reduces movement AP costs (-1 AP at level 8)
- **Progression**: Unlocks advanced piloting techniques
- **Skills**: Piloting, Navigation, Stellar Cartography

**Communications Officer**

- **Role**: Manages all ship communications and diplomatic contacts
- **Combat Benefits**: Coordinates with allied ships, can call for reinforcements
- **Special Ability**: Hailing attempts more likely to succeed
- **Progression**: Improves diplomatic outcomes and intelligence gathering
- **Skills**: Communications, Diplomacy, Universal Translator

**Medical Officer**

- **Role**: Maintains crew health and treats casualties
- **Combat Benefits**: Reduces crew casualties and speeds recovery
- **Special Ability**: Emergency medical treatment during combat
- **Progression**: Improves crew morale and reduces casualty severity
- **Skills**: Medicine, Xenobiology, Psychology

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

**Klingon Captain**

- **Personality**: Aggressive, honor-focused, direct confrontation
- **Tactics**: Frontal assault, overwhelming firepower, never retreats
- **Dialogue**: Challenges to honorable combat, disdain for weakness
- **Ship Classes**: D7 Cruiser, Bird-of-Prey

**Romulan Commander**

- **Personality**: Tactical, strategic, uses deception and misdirection
- **Tactics**: Cloaking ambushes, flanking maneuvers, strategic withdrawal
- **Dialogue**: Calculated threats, strategic analysis, veiled warnings
- **Ship Classes**: Bird-of-Prey, Warbird

**Gorn Captain**

- **Personality**: Methodical, powerful, deliberate actions
- **Tactics**: Defensive positioning, heavy weapons, endurance warfare
- **Dialogue**: Territorial warnings, slow deliberate speech
- **Ship Classes**: Heavy Cruiser

**Orion Pirate Captain**

- **Personality**: Opportunistic, mercenary, profit-motivated
- **Tactics**: Targets weak ships, flees when outmatched, uses tricks
- **Dialogue**: Demands tribute, offers deals, threatens when cornered
- **Ship Classes**: Raider, Corsair

**Tholian Commander**

- **Personality**: Alien logic, territorial, energy-based beings
- **Tactics**: Web weapons, precision strikes, exotic energy weapons
- **Dialogue**: Cryptic warnings, mathematical logic, territorial claims
- **Ship Classes**: Tholian Web-Spinner

#### Neutral Characters

**Merchant Captain**

- **Role**: Trading opportunities and rumors
- **Interaction**: Buy/sell resources, information exchange
- **Benefits**: Access to rare supplies and equipment

**Independent Explorer**

- **Role**: Provides sector information and discoveries
- **Interaction**: Share exploration data, collaborative missions
- **Benefits**: Sector maps, anomaly locations

**Civilian Transport Captain**

- **Role**: Escort mission opportunities
- **Interaction
- **Benefits**: Reputation gains, emergency assistance

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

**Action Points (AP)**: Resource spent each turn to perform actions. Most ships have 5 AP per turn. Movement costs 1 AP per grid cell, phasers cost 1 AP, torpedoes cost 2 AP.

**Combat Mode**: Tactical turn-based state for ship-to-ship combat on a grid-based map with z-levels.

**Component**: Modular ship subsystem (weapons, shields, engines, sensors) that can be damaged, upgraded, or replaced.

**Facing**: Direction a starship is oriented, measured in degrees (0-315° in 45° increments). Affects firing arcs, shield coverage, and movement.

**Firing Arc**: 270° forward cone from ship's facing where weapons can target enemies. Ships cannot fire behind themselves.

**Galaxy Map**: Large-scale 10x10 grid showing all sectors in the game world. Used for strategic navigation between sectors.

**Initiative**: Numerical value determining turn order in combat. Higher initiative acts first. Player ships typically have initiative 10, NPCs 6-9.

**Line of Sight (LoS)**: Direct unobstructed path between two grid positions. Required for weapons targeting and sensor detection.

**Object Pool**: Performance optimization technique reusing game objects (projectiles, effects) instead of creating/destroying them.

**Sector Map**: Medium-scale 15x15x5 grid representing a single sector of space with 3D z-level support.

**Shield Facing**: One of four directional shield zones (forward, aft, port, starboard) that absorbs damage independently.

**State Machine**: Design pattern managing transitions between game modes (Main Menu, Galaxy Map, Sector Map, Combat).

**Turn**: Complete cycle where all entities execute actions in initiative order, from highest to lowest.

**Z-Level**: Vertical layer in 3D grid space (0-4), representing altitude or depth in space. Ships can move between z-levels.

#### Star Trek Terms

**Constitution Class**: Main Federation starship class in Kirk era (e.g., USS Enterprise NCC-1701). Balanced cruiser design.

**Deflector Shields**: Energy barrier protecting starships from weapons fire and spatial hazards. Has four directional facings.

**Dilithium**: Rare crystalline element that regulates matter/antimatter reactions in warp cores, enabling faster-than-light travel.

**Federation**: United Federation of Planets, democratic alliance of Earth and hundreds of member worlds.

**Gorn Hegemony**: Reptilian species known for strength and territorial nature. Slow but powerful ships.

**Impulse Drive**: Sublight propulsion system using fusion reactors. Used for in-system travel and combat maneuvering.

**Klingon Empire**: Warrior-based interstellar empire, often hostile to Federation. Values honor and combat prowess.

**LCARS**: Library Computer Access/Retrieval System. Federation computer interface style (inspiration for UI design).

**Nacelle**: Warp engine component containing warp coils. Vulnerable to damage, critical for FTL travel.

**Orion Syndicate**: Criminal organization of green-skinned humanoids. Known for piracy and smuggling operations.

**Phaser**: Phased Array by Stimulated Emission of Radiation. Primary directed energy weapon of Federation starships.

**Photon Torpedo**: Antimatter warhead launched via magnetic accelerator. High damage, limited ammunition.

**Romulan Star Empire**: Secretive empire descended from Vulcan exiles. Masters of cloaking technology and tactical warfare.

**Starbase**: Large orbital or deep space station. Provides repairs, supplies, mission briefings, and command facilities.

**Starfleet**: Military, exploratory, and diplomatic service of the United Federation of Planets.

**Tholian Assembly**: Crystalline beings with exotic energy-based technology. Highly territorial, use web weapons.

**Warp Drive**: Faster-than-light propulsion creating subspace field around ship. Warp factors rated 1-9.

**Warp Speed**: Faster-than-light velocity measured in warp factors. Warp 1 = speed of light, Warp 6 = standard cruising speed.

#### Technical Terms

**AAA Pattern**: Arrange-Act-Assert testing pattern where tests: 1) Arrange setup, 2) Act by calling code, 3) Assert results.

**Component Pattern**: Design pattern where complex objects are composed of smaller, reusable component objects rather than inheritance.

**ECS (Entity Component System)**: Architecture where entities are containers for components, and systems process components. Not fully used in this game (simplified to Component Pattern).

**GameObject**: Base class for all interactive game entities (ships, stations, projectiles) with position and state.

**Isometric View**: 2.5D projection where 3D space is displayed at an angle, showing width, depth, and height simultaneously.

**MVC (Model-View-Controller)**: Architecture pattern separating game logic (Model), rendering (View), and input handling (Controller).

**Object Pooling**: Memory management pattern reusing inactive objects instead of allocating/deallocating repeatedly.

**State Machine**: Computational model managing discrete states and transitions between them based on events or conditions.

**TOML (Tom's Obvious Minimal Language)**: Configuration file format used for game settings and data. Human-readable, type-safe.

**Turn-Based**: Gameplay paradigm where time advances in discrete turns rather than continuous real-time, allowing strategic planning.

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
