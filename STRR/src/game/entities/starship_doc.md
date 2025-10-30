# Starship Entity Documentation

**File:** `STRR/src/game/entities/starship.py`
**Version:** 0.0.1
**Last Updated:** 10-30-2025

---

## Purpose

Defines starship and space station entities. Implements **Game Object Pattern** with **Component Composition** for ship systems.

---

## Classes

### Starship

**Purpose:** Player and NPC starships with modular systems

**Key Attributes:**

- `ship_class` (str): Ship type ("Constitution", "Bird-of-Prey", etc.)
- `systems` (dict[str, ShipSystem]): Ship subsystems (weapons, shields, engines, sensors, life_support)
- `hull_integrity` (float): Hull strength (0-100%)
- `orientation` (int): Facing direction (0-359 degrees)

**Key Methods:**

- `get_system(name: str)`: Retrieve a specific ship system
- `take_damage(amount: int, damage_type: str)`: Apply damage (shields absorb first)
- `repair_system(name: str, amount: float)`: Repair a damaged system

**Example:**

```python
from game.entities.starship import Starship
from game.entities.base import GridPosition

# Create ship
ship = Starship(GridPosition(5, 5, 1), "Constitution", "Enterprise")

# Access systems
weapons = ship.get_system('weapons')
shields = ship.get_system('shields')

# Combat
ship.take_damage(50, "kinetic")
print(f"Hull: {ship.hull_integrity}%")

# Repairs
ship.repair_system('shields', 20.0)
```

---

### SpaceStation

**Purpose:** Space stations providing services

**Key Attributes:**

- `station_type` (str): Station type
- `services` (list[str]): Available services
- `docked_ships` (list[Starship]): Currently docked ships

**Key Methods:**

- `dock_ship(ship: Starship) -> bool`: Dock a ship
- `undock_ship(ship: Starship) -> bool`: Undock a ship
- `provide_service(ship: Starship, service_type: str) -> bool`: Provide service

---

## Integration Points

**Dependencies:**

- `game.entities.base.GameObject` - Base class
- `game.components.ship_systems` - Ship subsystems

**Used by:**

- `game.model.GameModel` - Manages starships
- Combat and movement systems

---

## Change History

- **10-30-2025** - Documentation created
- **10-29-2025** - Starship entities implemented
