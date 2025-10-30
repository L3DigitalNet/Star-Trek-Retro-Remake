# Base Entities Documentation

**File:** `STRR/src/game/entities/base.py`
**Version:** 0.0.1
**Last Updated:** 10-30-2025

---

## Purpose

Defines base classes for all game entities using the **Game Object Pattern**. Provides:

- 3D grid positioning system
- Unique entity identification
- Core entity lifecycle
- Base entity interface

---

## Classes

### GridPosition (dataclass)

**Purpose:** Represents 3D coordinates in space

**Attributes:**

- `x` (int): Horizontal X coordinate
- `y` (int): Horizontal Y coordinate
- `z` (int): Vertical Z-level (default: 0)

**Methods:**

- `distance_to(other: GridPosition) -> float`: Calculate 3D Euclidean distance

**Example:**

```python
pos1 = GridPosition(5, 5, 1)
pos2 = GridPosition(7, 7, 1)
distance = pos1.distance_to(pos2)  # Returns ~2.83
```

---

### GameObject

**Purpose:** Base class for all game entities

**Attributes:**

- `id` (str): Unique UUID identifier
- `position` (GridPosition): Current 3D position
- `name` (str): Display name
- `active` (bool): Whether entity is active (default: True)
- `faction` (Optional[str]): Faction affiliation

**Methods:**

- `update(dt: float)`: Update entity logic (override in subclasses)
- `destroy()`: Mark entity for removal (sets active=False)

**Example:**

```python
from game.entities.base import GameObject, GridPosition

class Asteroid(GameObject):
    def __init__(self, position: GridPosition):
        super().__init__(position, "Asteroid")
        self.faction = "neutral"

    def update(self, dt: float):
        # Asteroid logic here
        pass
```

---

## Integration Points

**Dependencies:**

- `uuid` - For unique ID generation

**Used by:**

- `game.entities.starship.Starship` - Extends GameObject
- All entity types

---

## Change History

- **10-30-2025** - Documentation created
- **10-29-2025** - Base entity classes implemented
