# Sector Map Documentation

**File:** `STRR/src/game/maps/sector.py`
**Version:** 0.0.2
**Last Updated:** 10-30-2025

---

## Purpose

Manages detailed sector maps with **3D grid system**. Provides tactical-level gameplay space with entities, obstacles, and environmental effects.

---

## Classes

### SectorMap

**Purpose:** 3D grid-based sector with entities and obstacles

**Attributes:**

- `coordinates` (Tuple[int, int]): Galaxy coordinates
- `sector_type` (str): Sector type ("federation", "neutral", "asteroid_field", "nebula")
- `grid_size` (Tuple[int, int, int]): 3D grid dimensions (default: 20x20x5)
- `entities` (dict): Entities by (x, y, z) position
- `obstacles` (set): Obstacle positions
- `environmental_effects` (dict): Environmental hazards

**Key Methods:**

- `is_in_bounds(position: GridPosition) -> bool`: Check if position is valid within sector bounds
- `has_obstacle(position: GridPosition) -> bool`: Check for obstacles at position
- `place_entity(entity, position) -> bool`: Place entity at position (validates bounds and obstacles)
- `remove_entity(position) -> Optional[object]`: Remove and return entity from position
- `get_entity_at(position) -> Optional[object]`: Get entity at position without removing
- `add_obstacle(position) -> bool`: Add obstacle at position (validates bounds)
- `move_entity(old_pos, new_pos) -> bool`: Move entity from old to new position (handles collision/rollback)
- `get_all_entities() -> list`: Get all entities with positions as list of tuples

**Example:**

```python
from game.maps.sector import SectorMap
from game.entities.base import GridPosition

# Create sector with specific type
sector = SectorMap((0, 0), "asteroid_field")

# Check position and place entity
pos = GridPosition(5, 5, 1)
if sector.is_in_bounds(pos) and not sector.has_obstacle(pos):
    sector.place_entity(ship, pos)

# Move entity to new position
new_pos = GridPosition(6, 5, 1)
if sector.move_entity(pos, new_pos):
    print("Ship moved successfully")

# Query entities
all_entities = sector.get_all_entities()
for position, entity in all_entities:
    print(f"Entity at {position}: {entity.name}")

# Create deterministic sector for testing
test_sector = SectorMap((1, 1), "nebula", random_seed=42)
```

---

## Implementation Details

**3D Grid System:**

- Uses `GridPosition(x, y, z)` for all spatial operations
- Grid size: 20×20×5 (width × height × depth)
- Z-levels provide vertical space positioning

**Entity Management:**

- Entities stored as dictionary with GridPosition keys
- Position validation on all operations
- Obstacle collision detection prevents invalid placement
- `move_entity()` includes rollback on collision

**Sector Types:**

- `"standard"` - Empty sector (default)
- `"asteroid_field"` - 10 random asteroid obstacles
- `"nebula"` - Environmental effects in central region (5-15 x, y and 1-4 z)

**Testing Support:**

- Optional `random_seed` parameter for deterministic sector generation
- Enables reproducible tests for asteroid placement

---

## Integration Points

**Dependencies:**

- `game.entities.base.GridPosition` - 3D positioning

**Used by:**

- `game.model.GameModel` - Current tactical view
- `game.maps.galaxy.GalaxyMap` - Creates sectors

---

## Change History

- **10-30-2025** - Added `move_entity()` method, inline comments, updated documentation
- **10-29-2025** - Sector map with 3D grid implemented
