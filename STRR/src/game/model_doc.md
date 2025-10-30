# Game Model Documentation

**File:** `STRR/src/game/model.py`
**Version:** 0.0.1
**Last Updated:** 10-30-2025

---

## Purpose

The `model.py` file implements the **Model** component of the MVC (Model-View-Controller) architecture. It is the **core game logic and state container** with these key characteristics:

- **Pure game logic** - No UI dependencies whatsoever
- **Independently testable** - Can be tested without PyGame or PySide6
- **Business rules** - All game mechanics, turn management, combat resolution
- **State management** - Maintains complete game state
- **Data operations** - Save/load game state

This is where the "rules of the game" live. All calculations, validations, and state transitions happen here.

---

## Architecture

### MVC Model Pattern

The Model is **completely independent** from the View and Controller:

```
GameModel (this file)
    ↓ provides state/logic
Controller
    ↓ updates display
View
```

**Key principle:** The Model never imports or depends on View or Controller code.

### State Container Pattern

The Model acts as a centralized state container managing:

- **Game world:** Galaxy, sectors, entities
- **Player state:** Player ship, resources, missions
- **Game mechanics:** Turns, combat, movement
- **Meta-state:** Save data, game progression

### Turn-Based System

```
Player Action → Model validates → Model updates state → Model advances turn → AI processes → Ready for next action
```

---

## Classes

### CombatResult (dataclass)

**Purpose:** Immutable data container for combat action results

**Attributes:**

- `success` (bool): Whether the combat action succeeded
- `message` (str): Human-readable description of what happened
- `damage` (int): Amount of damage dealt (default: 0)

**Usage:**

```python
result = CombatResult(
    success=True,
    message="Direct hit on enemy shields",
    damage=25
)
```

---

### TurnManager

**Purpose:** Manages the turn-based gameplay loop

**Attributes:**

- `turn_number` (int): Current turn counter (starts at 0)
- `current_phase` (str): Current phase of turn (e.g., "player", "ai", "environment")

**Public Methods:**

#### advance_turn() -> None

Increments the turn counter and processes AI/NPC actions.

**Behavior:**

1. Increments `turn_number` by 1
2. Calls `_process_ai_turns()` to handle AI entities
3. Prepares for next player action

**Example:**

```python
turn_manager = TurnManager()
print(turn_manager.turn_number)  # 0
turn_manager.advance_turn()
print(turn_manager.turn_number)  # 1
```

#### get_turn_info() -> dict[str, int | str]

Returns current turn information as a dictionary.

**Returns:**

- Dictionary with keys: `turn_number` (int), `current_phase` (str)

**Example:**

```python
info = turn_manager.get_turn_info()
print(f"Turn {info['turn_number']}, Phase: {info['current_phase']}")
# Output: Turn 5, Phase: player
```

**Private Methods:**

#### _process_ai_turns() -> None

Processes AI entity actions for the current turn. (Stub - to be implemented)

---

### GameModel

**Purpose:** Main game state container and logic coordinator

**Attributes:**

- `galaxy` (GalaxyMap): Complete galaxy map with all sectors
- `current_sector` (Optional[SectorMap]): Currently active sector for detailed play
- `player_ship` (Optional[Starship]): The player's controllable starship
- `turn_manager` (TurnManager): Turn management system
- `game_objects` (list[object]): All active game entities
- `active_missions` (list[object]): Current active missions (to be typed)

**Public Methods:**

#### initialize_new_game() -> None

Sets up a new game with default starting conditions.

**Behavior:**

1. Creates player's Constitution-class ship "Enterprise" at position (5, 5, 1)
2. Loads the starting sector (0, 0)
3. Adds player ship to game objects list
4. Resets turn counter

**Example:**

```python
model = GameModel()
model.initialize_new_game()
print(model.player_ship.name)  # "Enterprise"
print(model.turn_manager.turn_number)  # 0
```

#### execute_move(ship: Starship, destination: GridPosition) -> bool

Attempts to move a starship to a new position.

**Parameters:**

- `ship`: The starship to move
- `destination`: Target 3D grid position

**Returns:**

- `True` if move succeeded
- `False` if move failed (invalid position, insufficient fuel, etc.)

**Behavior:**

1. Validates the move using `_is_valid_move()`
2. Calculates fuel cost based on distance
3. Checks if ship has sufficient fuel
4. Updates ship position
5. Deducts fuel from engines
6. Advances turn

**Example:**

```python
model = GameModel()
model.initialize_new_game()
ship = model.player_ship
new_pos = GridPosition(6, 6, 1)

if model.execute_move(ship, new_pos):
    print("Move successful!")
else:
    print("Move failed - check fuel or obstacles")
```

#### resolve_combat(attacker: Starship, target: Starship, weapon_type: str) -> CombatResult

Resolves combat between two starships.

**Parameters:**

- `attacker`: The attacking starship
- `target`: The target starship
- `weapon_type`: Type of weapon ("phaser" or "torpedo")

**Returns:**

- `CombatResult` object with success status, message, and damage

**Behavior:**

1. Validates attacker's weapons are online
2. Checks if target is in range and firing arc
3. Calculates damage based on weapon type and efficiency
4. Applies damage to target
5. Returns result

**Example:**

```python
result = model.resolve_combat(
    model.player_ship,
    enemy_ship,
    "phaser"
)

if result.success:
    print(f"{result.message} - {result.damage} damage dealt")
else:
    print(f"Attack failed: {result.message}")
```

#### save_game(filepath: str) -> bool

Saves the current game state to a file.

**Parameters:**

- `filepath`: Path where save file should be created

**Returns:**

- `True` if save succeeded, `False` otherwise

**Status:** Stub implementation - to be completed

#### load_game(filepath: str) -> bool

Loads a saved game state from a file.

**Parameters:**

- `filepath`: Path to the save file to load

**Returns:**

- `True` if load succeeded, `False` otherwise

**Status:** Stub implementation - to be completed

**Private Methods:**

#### _is_valid_move(ship: Starship, destination: GridPosition) -> bool

Validates whether a move request is legal.

**Checks:**

1. Current sector exists
2. Destination is within sector bounds
3. No obstacles at destination
4. (Future: Check for enemy zones, anomalies, etc.)

**Returns:**

- `True` if move is valid, `False` otherwise

#### _create_player_ship(position: GridPosition) -> Starship

Factory method that creates the player's starting ship.

**Parameters:**

- `position`: Starting position for the ship

**Returns:**

- Configured `Starship` instance (Constitution-class "Enterprise")

---

## Usage Examples

### Example 1: Basic Game Setup

```python
from game.model import GameModel
from game.entities.base import GridPosition

# Create and initialize game
model = GameModel()
model.initialize_new_game()

# Access game state
print(f"Playing as: {model.player_ship.name}")
print(f"Ship class: {model.player_ship.ship_class}")
print(f"Position: {model.player_ship.position}")
print(f"Turn: {model.turn_manager.turn_number}")
```

### Example 2: Ship Movement

```python
model = GameModel()
model.initialize_new_game()

ship = model.player_ship
current_pos = ship.position
new_pos = GridPosition(current_pos.x + 1, current_pos.y, current_pos.z)

# Attempt move
if model.execute_move(ship, new_pos):
    print(f"Moved from {current_pos} to {ship.position}")
    print(f"Turn is now: {model.turn_manager.turn_number}")
else:
    print("Move blocked or invalid")
```

### Example 3: Combat Simulation

```python
from game.entities.starship import Starship
from game.entities.base import GridPosition

model = GameModel()
model.initialize_new_game()

# Create enemy ship
enemy = Starship(GridPosition(7, 7, 1), "Bird-of-Prey", "Klingon Cruiser")
model.game_objects.append(enemy)

# Attack with phasers
result = model.resolve_combat(model.player_ship, enemy, "phaser")
print(f"Combat result: {result.message}")
print(f"Damage: {result.damage}")
print(f"Enemy hull: {enemy.hull_integrity}%")

# Attack with torpedoes
result = model.resolve_combat(model.player_ship, enemy, "torpedo")
print(f"Torpedo result: {result.message}")
```

### Example 4: Turn Management

```python
model = GameModel()
model.initialize_new_game()

# Game loop simulation
for turn in range(5):
    print(f"\n--- Turn {model.turn_manager.turn_number} ---")

    # Player action
    new_pos = GridPosition(5 + turn, 5, 1)
    model.execute_move(model.player_ship, new_pos)

    # Turn info
    info = model.turn_manager.get_turn_info()
    print(f"Phase: {info['current_phase']}")
```

---

## Integration Points

### Dependencies

**Project modules:**

- `game.entities.starship.Starship` - Starship entity class
- `game.entities.base.GridPosition` - 3D position dataclass
- `game.maps.galaxy.GalaxyMap` - Galaxy-level map
- `game.maps.sector.SectorMap` - Sector-level map

**Standard library:**

- `typing.Final`, `typing.Optional` - Type annotations
- `dataclasses.dataclass` - For `CombatResult`

**Why these dependencies:**

- Entity classes represent game objects that the model manages
- Map classes provide the game world structure
- No UI dependencies - model is testable in isolation

### Used By

**Direct users:**

- `game.controller.GameController` - Executes model methods based on player input
- Test files (`tests/test_game_model.py`) - Unit tests for game logic

**Indirect users:**

- `game.view.GameView` - Reads model state to render (but never modifies it)

---

## Configuration

### Initial State

When `GameModel()` is instantiated:

- Turn number: 0
- No player ship (until `initialize_new_game()`)
- Empty game objects list
- Galaxy map created with default size
- No active sector

### Default New Game

When `initialize_new_game()` is called:

- Player ship: Constitution-class "Enterprise"
- Starting position: (5, 5, 1)
- Starting sector: (0, 0)
- All ship systems at 100% efficiency

---

## Common Patterns

### Pattern 1: Validating Actions Before Execution

```python
def execute_action(model: GameModel, action_data: dict) -> bool:
    """Safe action execution with validation."""
    # Pre-validate
    if not model.player_ship:
        return False

    # Execute action
    if action_data["type"] == "move":
        destination = action_data["destination"]
        return model.execute_move(model.player_ship, destination)
    elif action_data["type"] == "attack":
        target = action_data["target"]
        result = model.resolve_combat(
            model.player_ship,
            target,
            action_data["weapon"]
        )
        return result.success

    return False
```

### Pattern 2: Querying Game State

```python
def get_game_status(model: GameModel) -> dict:
    """Get comprehensive game state summary."""
    return {
        "turn": model.turn_manager.turn_number,
        "phase": model.turn_manager.current_phase,
        "player_ship": model.player_ship.name if model.player_ship else None,
        "position": model.player_ship.position if model.player_ship else None,
        "hull": model.player_ship.hull_integrity if model.player_ship else 0,
        "entities_count": len(model.game_objects),
        "sector": model.current_sector.coordinates if model.current_sector else None
    }
```

### Pattern 3: Testing Model Logic

```python
def test_movement_validation():
    """Test that invalid moves are rejected."""
    model = GameModel()
    model.initialize_new_game()

    # Test out-of-bounds move
    invalid_pos = GridPosition(-1, -1, -1)
    assert not model.execute_move(model.player_ship, invalid_pos)

    # Test valid move
    valid_pos = GridPosition(6, 6, 1)
    assert model.execute_move(model.player_ship, valid_pos)
```

---

## Troubleshooting

### Issue: Movement always fails

**Symptom:** `execute_move()` always returns `False`

**Possible causes:**

1. Destination out of sector bounds
2. Insufficient fuel
3. Obstacle at destination
4. No current sector loaded

**Solution:**

```python
# Debug movement
destination = GridPosition(6, 6, 1)

# Check sector
if not model.current_sector:
    print("No sector loaded!")

# Check bounds
if model.current_sector and not model.current_sector.is_in_bounds(destination):
    print(f"Destination {destination} out of bounds!")

# Check obstacles
if model.current_sector and model.current_sector.has_obstacle(destination):
    print(f"Obstacle at {destination}!")

# Check fuel
engines = model.player_ship.get_system('engines')
if engines:
    distance = int(model.player_ship.position.distance_to(destination))
    fuel_needed = engines.calculate_movement_cost(distance)
    print(f"Fuel: {engines.fuel}/{fuel_needed} needed")
```

### Issue: Combat never succeeds

**Symptom:** `resolve_combat()` always returns `success=False`

**Possible causes:**

1. Weapons offline
2. Target out of range
3. Wrong weapon type

**Solution:**

```python
# Debug combat
weapons = attacker.get_system('weapons')
if not weapons:
    print("No weapons system!")
elif not weapons.active:
    print("Weapons offline!")

if not weapons.can_target(target.position, attacker.position, attacker.orientation):
    print("Target out of range or firing arc!")
```

### Issue: Turn number not advancing

**Symptom:** Turn counter stuck at 0

**Cause:** Forgetting to call actions that advance turns

**Solution:** Only `execute_move()` currently advances turns. Ensure moves are being executed successfully.

---

## Notes

### Model Independence

**Critical:** The Model must NEVER import View or Controller code. This enables:

- Unit testing without UI
- Headless game simulation
- AI training without graphics
- Save state validation

### Future Enhancements

Planned additions to the Model:

- [ ] Mission system implementation
- [ ] AI decision making in `_process_ai_turns()`
- [ ] Save/load with JSON or pickle
- [ ] Event history tracking
- [ ] Multiplayer state synchronization
- [ ] Replay system
- [ ] Procedural content generation

### Performance Considerations

The Model stores all game objects in a single list. For large numbers of entities, consider:

- Spatial partitioning (quadtree/octree)
- Entity culling based on active sector
- Lazy loading of distant sectors

---

## Change History

- **10-30-2025** - Initial documentation created
- **10-29-2025** - Model implementation created with MVC pattern
