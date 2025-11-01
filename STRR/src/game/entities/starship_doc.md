# Starship Entity Documentation

**File:** `STRR/src/game/entities/starship.py`
**Version:** 0.0.22
**Last Updated:** 10-31-2025

---

## Purpose

Defines starship and space station entities. Implements **Game Object Pattern** with **Component Composition** for ship systems.

---

## Classes

### Starship

**Purpose:** Player and NPC starships with modular systems

**Key Attributes:**

- `ship_class` (str): Ship type ("Constitution", "Bird-of-Prey", etc.)
- `systems` (dict[str, ShipSystem]): Ship subsystems (weapons, shields, engines, sensors, life_support, resources, crew)
- `resources` (ResourceManager): Quick access to resource management system
- `crew` (CrewManager): Quick access to crew management system
- `hull_integrity` (float): Hull strength (0-100%)
- `orientation` (int): Facing direction (0-359 degrees)

**Key Methods:**

- `get_system(name: str)`: Retrieve a specific ship system
- `take_damage(amount: int, damage_type: str)`: Apply damage (shields absorb first)
- `repair_system(name: str, amount: float, use_supplies: bool)`: Repair with supplies and crew efficiency
- `allocate_power(system: str, percentage: float)`: Set power distribution
- `consume_energy_for_action(action: str)`: Use energy for action
- `has_sufficient_energy(action: str)`: Check if energy available
- `refuel_at_starbase()`: Restore fuel to maximum
- `resupply_at_starbase()`: Restore supplies and boost morale
- `get_crew_efficiency()`: Get current efficiency multiplier (0.8 - 1.2)
- `record_combat_result(victory: bool)`: Update crew morale from combat

**Example:**

```python
from game.entities.starship import Starship
from game.entities.base import GridPosition

# Create ship
ship = Starship(GridPosition(5, 5, 1), "Constitution", "Enterprise")

# Access systems
weapons = ship.get_system('weapons')
shields = ship.get_system('shields')

# Resource management
ship.allocate_power('shields', 40.0)  # Allocate 40% power to shields
if ship.has_sufficient_energy('fire_phaser'):
    ship.consume_energy_for_action('fire_phaser')

# Combat and morale
ship.take_damage(50, "kinetic")
ship.record_combat_result(victory=True)  # Boost crew morale
print(f"Hull: {ship.hull_integrity}%")
print(f"Morale: {ship.crew.morale}%")
print(f"Efficiency: {ship.get_crew_efficiency()}x")

# Repairs with supplies and crew efficiency
if ship.resources.supplies['spare_parts'] >= 30:
    ship.repair_system('shields', 0.3, use_supplies=True)

# Energy and fuel
print(f"Energy: {ship.resources.energy_current}/{ship.resources.energy_capacity}")
print(f"Fuel: {ship.resources.fuel_current}/{ship.resources.fuel_capacity}")
```

---

### SpaceStation

**Purpose:** Space stations providing services

**Key Attributes:**

- `station_type` (str): Station type
- `services` (list[str]): Available services
- `docked_ships` (list[Starship]): Currently docked ships

**Key Methods:**

- `dock_ship(ship: Starship) -> bool`: Dock a ship at station
- `undock_ship(ship: Starship) -> bool`: Undock a ship from station
- `provide_service(ship: Starship, service_type: str) -> bool`: Provide service to docked ship

**Available Services:**

- `"refuel"`: Restore fuel to maximum capacity
- `"resupply"`: Restore medical supplies and spare parts to full
- `"repair"`: Restore all systems and hull to 100%, boost crew morale

**Example:**

```python
from game.entities.starship import Starship, SpaceStation
from game.entities.base import GridPosition

# Create station and ship
station = SpaceStation(GridPosition(10, 10, 0), "Starbase", "Starbase 11")
ship = Starship(GridPosition(10, 10, 0), "Constitution", "Enterprise")

# Dock at station
if station.dock_ship(ship):
    # Get repairs and resupply
    station.provide_service(ship, "repair")      # Hull and systems to 100%
    station.provide_service(ship, "refuel")      # Fuel to maximum
    station.provide_service(ship, "resupply")    # Supplies to full, morale boost

    # Undock
    station.undock_ship(ship)
```

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
