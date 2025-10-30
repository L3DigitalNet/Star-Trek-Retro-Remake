# Sector Map Documentation

**File:** `STRR/src/game/maps/sector.py`
**Version:** 0.0.1
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

- `is_in_bounds(position: GridPosition) -> bool`: Check if position is valid
- `has_obstacle(position: GridPosition) -> bool`: Check for obstacles
- `place_entity(entity, position) -> bool`: Place entity at position
- `remove_entity(position) -> Optional[object]`: Remove entity
- `get_entity_at(position) -> Optional[object]`: Get entity at position
- `add_obstacle(position) -> bool`: Add obstacle
- `get_all_entities() -> list`: Get all entities with positions

**Example:**

```python
from game.maps.sector import SectorMap
from game.entities.base import GridPosition

# Create sector
sector = SectorMap((0, 0), "asteroid_field")

# Check position
pos = GridPosition(5, 5, 1)
if sector.is_in_bounds(pos) and not sector.has_obstacle(pos):
    sector.place_entity(ship, pos)

# Query entities
all_entities = sector.get_all_entities()
for position, entity in all_entities:
    print(f"Entity at {position}: {entity.name}")
```

---

## Integration Points

**Dependencies:**

- `game.entities.base.GridPosition` - 3D positioning

**Used by:**

- `game.model.GameModel` - Current tactical view
- `game.maps.galaxy.GalaxyMap` - Creates sectors

---

## Change History

- **10-30-2025** - Documentation created
- **10-29-2025** - Sector map with 3D grid implemented
