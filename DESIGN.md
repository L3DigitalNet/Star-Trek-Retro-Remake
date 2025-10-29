# Planning and Design Document for Star Trek Retro Remake

## Basic Overview

A turn-based and grid-based strategy game set in the Star Trek universe and inspired by classic Star Trek games Star Trek (1971) and Super Star Trek (1973). The player commands a starship, exploring space, completing missions, and engaging in tactical combat with enemy ships.

## Setting and Theme

The game is set in the Kirk-era 23rd century within the Star Trek universe. The player takes on the role of a starship captain, exploring uncharted space, encountering alien species, and upholding the principles of the United Federation of Planets. The theme emphasizes exploration, diplomacy, and tactical combat.

## Game Mechanics

### Game Loop

- The game will operate on a turn-based system.
- A certain number of actions can be taken each turn based on ship capabilities, resources, and mode.

#### Game Play Modes

- Galaxy Map Mode: Navigate between sectors, manage resources, and plan missions.
- Sector Map Mode: Explore individual sectors, encounter events, interact with starbases, and engage in tactical combat.
- Combat Mode: Tactical turn-based combat between starships on the sector map.

#### Turn Structure

- Each turn represents a fixed time interval in the game world
  - Seconds or minutes in combat
  - Hours or days during sector map exploration
  - Days or weeks during galaxy map navigation

- While in combat mode each turn consists of:
  - Player input phase: The player issues commands to their starship (movement, attacks, resource management).
  - NPC phase: Enemy ships and other entities execute their actions based on AI behavior.
  - Resolution phase: The game processes all actions, updates the game state, and renders the new state.

- While in sector map mode each turn consists of:
  - Player input phase: The player can move their starship, interact with objects, and manage resources.
  - Event phase: Random events or scripted encounters may occur.
  - Resolution phase: The game updates the game state based on player actions and events.

- While in galaxy map mode each turn consists of:
  - Player input phase: The player can navigate between sectors, manage resources, and plan missions.
  - Event phase: Random events or scripted encounters may occur.
  - Resolution phase: The game updates the game state based on player actions and events.

#### Input Handling

- The game will support both keyboard and mouse input.
- Interactions will be primarily be handled through mouse clicks, keyboard shortcuts, menu selections, sliders, dialog boxes, etc.
- Mouse input will be used for interacting with the game world (e.g., clicking on objects directly within the map, selecting objects in the map, etc.).

### User Interface

- The main game will be contained within a PyQt6 application window.
- Much of the interaction will be through widgets such as menus, dialogs, and buttons.
- The main game view (map) will be rendered using PyGame embedded within the PyQt6 application.
- The map will be centered in the application window with UI elements surrounding it.
- Pop-up dialogs will be used for mission briefings, ship status, and other information.

### Map

There are multiple sector maps that are accessed via a galaxy map.

#### Sector Map

- A grid-based map with z-levels to semi-represent 3D space
  - Planning for a maximum of 5 or 7 z-levels.
  - Planning for a maximum x-y grid size of 20x20 cells.
  - Sizes will vary between sectors.
- Will be viewed from a fixed isometric perspective.
- All z-levels are visible simultaneously.
  - The z-level that the player is currently on is fully visible.
  - Other z-levels are partially transparent.
- Each cell can contain:
  - Empty space
  - A starship (player or NPC)
  - A space station
  - An anomaly (e.g., black hole, nebula, wormhole)
  - Other objects (e.g., asteroids, debris fields)

#### Galaxy Map

- A grid-based map with each cell representing a sector.
- No z-levels.
- Used for navigation between sectors.
- Will have faction territories and special locations.

### Starships

- Player is the captain of a starship.
- The starship is represented on the sector map by a sprite/icon.
- Starships have attributes:
  - Hull integrity
  - Shield strength
  - Weapon systems
  - Engine power
  - Crew morale
- Starships can move between cells on the sector map.
  - Starships have a vector-based movement system allowing movement in all directions.
  - At the end of a turn the starship's orientation will determine its facing for the next turn.
  - Starship orientation will affect weapon firing arcs, shield coverage, and sensor range.
- Starships can engage in combat with enemy ships.
- Starships can dock at space stations for repairs and resupply.

### Resource Management

- Players must manage ship resources:
  - Energy allocation (shields, weapons, engines)
  - Sensor modes (long-range, short-range, passive)
  - Supplies (fuel, food, medical supplies)

## Features to be Developed Post-v1.0.0

### Advanced crew management

- Assign crew to different stations (e.g., weapons, engineering, science).
- Crew skills and experience affecting ship performance.

### Advanced Diplomacy

- Engage in diplomatic negotiations with other factions.
- Form alliances or declare war.
- Influence other factions through espionage or propaganda.

### Simulation Mode

- A real-time management mode where the player has to manage ship systems and crew in real-time.
- Complex ship systems that are strongly interconnected.
  - Fuel consumption affecting engine power and weapon systems.
  - High power usage increases coolant requirements.
  - Increased cooling needs can lead to less resource allocation for other systems.
  - Power distribution affecting shields, weapons, and sensors.

### Starship Design and Customization

- Players can customize their starship's capabilities (weapons, shields, engines, etc.) at starbases and shipyards.
- Modular ship components (e.g., engines, weapons, shields) can be upgraded or replaced.
- Players can design their own starship classes with unique attributes and abilities.

### Fleet Management

- Players can earn a promotion to Admiral and command a fleet of starships.
- Players can manage multiple starships within their fleet.
- Fleets can be assigned to different missions or tasks.
- Players can issue orders to individual starships or the entire fleet.
