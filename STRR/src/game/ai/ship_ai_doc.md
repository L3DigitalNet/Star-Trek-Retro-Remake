# Ship AI Module Documentation

**Module:** `STRR/src/game/ai/ship_ai.py`
**Version:** 0.0.21
**Last Updated:** 10-31-2025

## Overview

The Ship AI module implements an autonomous decision-making system for NPC starships using a simple state machine architecture. It provides three distinct behavioral states (PATROL, ATTACK, FLEE) with intelligent transitions based on combat conditions, hull integrity, and threat assessment.

## Purpose

This module enables:

- Autonomous NPC ship behavior without player intervention
- Dynamic state transitions based on combat situation
- Target selection and prioritization for combat AI
- Realistic patrol and flee behaviors
- Integration with the turn-based combat system

## Architecture

### Design Pattern

- **State Machine Pattern**: AI behavior organized into discrete states with clear transition rules
- **Component Integration**: Works with GameModel, Starship entities, and ship components
- **Turn-Based Integration**: AI processes during entity turns via GameModel

### Key Components

1. **AIState Enum**: Defines three behavioral states (PATROL, ATTACK, FLEE)
2. **ShipAI Class**: Main AI controller managing state and decision-making
3. **Configuration System**: Loads AI parameters from game_settings.toml

## Classes

### AIState (Enum)

Enumeration of AI behavioral states.

**States:**

- `PATROL`: Random movement within patrol radius, searching for threats
- `ATTACK`: Aggressive combat behavior targeting nearest/weakest enemies
- `FLEE`: Retreat behavior when hull integrity is critical

### ShipAI

AI controller for NPC starships.

**Attributes:**

- `ship`: The starship being controlled
- `state`: Current AI state (AIState enum)
- `target`: Current target entity (if any)
- `patrol_center`: Original position for patrol behavior
- `_model_ref`: Reference to GameModel for world queries
- `_enemy_cache`: Cached list of detected enemies (refreshes every 3 turns)
- `_cache_age`: Age of enemy cache in turns

**Configuration (from game_settings.toml):**

- `patrol_radius`: Maximum distance for patrol movement (default: 5 cells)
- `flee_threshold`: Hull percentage to trigger flee state (default: 30%)
- `enemy_cache_duration`: Turns before refreshing enemy list (default: 3)

**Public Methods:**

#### `__init__(ship: Starship, model: GameModel)`

Initialize AI controller for a starship.

**Parameters:**

- `ship`: The starship to control
- `model`: GameModel reference for world queries

**Returns:** None

#### `process_turn() -> None`

Process AI decision-making for current turn. Main entry point called by GameModel during AI turns.

**Behavior:**

- Updates state based on current conditions
- Executes state-specific behavior (patrol/attack/flee)
- Consumes action points for performed actions

**Returns:** None

#### `set_state(new_state: AIState) -> None`

Change AI state with logging for debugging.

**Parameters:**

- `new_state`: The state to transition to

**Returns:** None

**Private Methods:**

#### `_update_state() -> None`

Evaluate conditions and transition states as needed.

**State Transition Rules:**

- PATROL → ATTACK: Enemies detected within sensor range
- ATTACK → FLEE: Hull below flee threshold (30% default)
- FLEE → PATROL: Hull recovered above flee threshold
- ATTACK → PATROL: No enemies in range

#### `_patrol_behavior() -> None`

Execute patrol behavior: random movement within patrol radius.

**Actions:**

- Select random position within patrol_radius of patrol_center
- Move toward selected position if possible
- Consumes action points for movement

#### `_attack_behavior() -> None`

Execute attack behavior: engage nearest/weakest enemy.

**Actions:**

1. Select target using `_select_target()`
2. Move toward target if out of weapon range
3. Fire weapons if in range and action points available
4. Consumes action points for movement and combat

#### `_flee_behavior() -> None`

Execute flee behavior: retreat from combat.

**Actions:**

- Calculate escape direction (away from nearest threat)
- Move in escape direction if possible
- Transition to PATROL once hull recovers
- Consumes action points for movement

#### `_select_target() -> Starship | None`

Select best target based on distance and hull integrity.

**Scoring Algorithm:**

- Distance score: Closer targets prioritized
- Hull score: Weaker targets prioritized (below 50% hull)
- Combined score used to rank targets

**Returns:** Selected target Starship or None if no valid targets

#### `_get_enemies() -> list[GameObject]`

Get list of enemy entities using cached results for performance.

**Caching:**

- Enemy list cached for `enemy_cache_duration` turns (default: 3)
- Automatically refreshes when cache expires
- Reduces scanning overhead for multiple AI ships

**Returns:** List of enemy GameObject entities

#### `_is_enemy(entity: GameObject) -> bool`

Determine if entity is hostile.

**Logic:**

- Currently treats all non-self ships as enemies
- Future: Will use faction relationships from game_data.toml

**Returns:** True if entity is hostile, False otherwise

## Integration Points

### GameModel Integration

The GameModel class manages AI processing:

```python
# In GameModel.__init__():
self._initialize_ai()  # Create AI controllers for NPC ships

# In GameModel.end_current_turn():
if not current_entity.is_player:
    current_entity.ai_controller.process_turn()  # AI makes decisions
```

### Starship Integration

NPC starships have an `ai_controller` attribute:

```python
# Create AI controller
ship.ai_controller = ShipAI(ship, game_model)

# AI processes turn
ship.ai_controller.process_turn()
```

### Configuration Integration

AI parameters loaded from `game_settings.toml`:

```toml
[game.combat]
ai_patrol_radius = 5        # Patrol movement radius
ai_flee_threshold = 30      # Hull % to trigger flee
ai_enemy_cache_duration = 3 # Turns to cache enemy list
```

## Usage Examples

### Basic AI Setup

```python
from STRR.src.game.ai.ship_ai import ShipAI, AIState
from STRR.src.game.entities.starship import Starship

# Create NPC ship
npc_ship = Starship(
    name="IKS Korinar",
    ship_class="D7 Cruiser",
    position=GridPosition(10, 10, 1),
    faction="Klingon"
)

# Attach AI controller
npc_ship.ai_controller = ShipAI(npc_ship, game_model)

# AI will process during turn
npc_ship.ai_controller.process_turn()
```

### Manual State Changes

```python
# Override AI state (for scripted events)
npc_ship.ai_controller.set_state(AIState.ATTACK)

# Check current state
if npc_ship.ai_controller.state == AIState.FLEE:
    print(f"{npc_ship.name} is retreating!")
```

### Custom AI Behavior

```python
# Modify AI parameters
npc_ship.ai_controller.patrol_radius = 10  # Larger patrol area
npc_ship.ai_controller.flee_threshold = 20  # More aggressive

# Process turn with custom parameters
npc_ship.ai_controller.process_turn()
```

## State Machine Diagram

```
    ┌─────────┐
    │ PATROL  │◄─────┐
    └────┬────┘      │
         │           │
    Enemy│           │No enemies /
  detected│           │Hull recovered
         │           │
         ▼           │
    ┌─────────┐     │
    │ ATTACK  │─────┤
    └────┬────┘     │
         │          │
    Hull │          │
     low │          │
         ▼          │
    ┌─────────┐    │
    │  FLEE   │────┘
    └─────────┘
```

## Performance Considerations

### Enemy List Caching

- Enemy detection expensive (scans all entities in sector)
- Cache refreshes every 3 turns (configurable)
- Reduces overhead when multiple AI ships active
- Trade-off: AI may target destroyed ships for 1-2 turns

### Action Point Management

- AI actions consume action points like player
- Movement costs 1 AP per cell
- Weapon firing costs 1-2 AP depending on weapon type
- AI turn ends when action points exhausted

### Turn Processing

- GameModel processes all AI turns automatically during `end_current_turn()`
- Safety limit prevents infinite loops (2x entity count, minimum 20)
- Warning logged if safety limit reached

## Future Enhancements

### Planned Features

- **Faction-Based Targeting**: Use faction relationships instead of "all non-self"
- **Coordinated Tactics**: Multiple AI ships coordinate attacks
- **Formation Flying**: AI ships maintain tactical formations
- **Defensive Maneuvers**: Evasive actions, shield redistribution
- **Communication**: AI ships hail/respond to player
- **Mission Objectives**: AI follows scripted mission goals

### Configuration Expansion

- Per-faction AI parameters (Klingons aggressive, Romulans cautious)
- AI difficulty levels (Easy/Normal/Hard)
- Ship class-specific behaviors (scouts vs battleships)

## Testing

### Unit Tests

Comprehensive test coverage in `STRR/tests/test_ship_ai.py`:

- State initialization and transitions
- Target selection algorithms
- Patrol/attack/flee behavior validation
- Enemy caching and detection
- Integration with turn system

### Manual Testing

Use demo files to test AI behavior:

- Run game and observe NPC ship behavior
- Adjust hull damage to trigger flee state
- Monitor AI decision-making in logs (DEBUG level)

## Related Documentation

- **Starship Entity**: `STRR/src/game/entities/starship_doc.md`
- **GameModel**: `STRR/src/game/model_doc.md`
- **Ship Systems**: `STRR/src/game/components/ship_systems_doc.md`
- **Combat System**: See CHANGELOG.md v0.0.20 for combat mechanics
- **Configuration**: `STRR/config/game_settings.toml`

## Linux Compatibility

All AI code is fully compatible with Linux systems:

- Pure Python implementation (no OS-specific calls)
- Path handling uses pathlib for Linux compatibility
- Configuration loading uses standard library (tomli-w)
- No Windows-specific dependencies

**Python Requirements:** 3.14+ for latest language features
