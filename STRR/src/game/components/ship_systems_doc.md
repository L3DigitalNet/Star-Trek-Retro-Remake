# Ship Systems Documentation

**File:** `STRR/src/game/components/ship_systems.py`
**Version:** 0.0.1
**Last Updated:** 10-30-2025

---

## Purpose

Implements ship subsystems using the **Component Pattern**. Each system is a self-contained component with specific functionality.

---

## Classes

### ShipSystem (Abstract Base)

**Purpose:** Base class for all ship systems

**Attributes:**

- `name` (str): System identifier
- `efficiency` (float): Current efficiency (0.0 to max_efficiency)
- `max_efficiency` (float): Maximum efficiency rating
- `damaged` (bool): Whether system is damaged
- `active` (bool): Whether system is online
- `power_usage` (float): Current power consumption

**Methods:**

- `update(dt: float)`: Update system state
- `repair(amount: float)`: Repair damage
- `damage(amount: float)`: Apply damage

---

### WeaponSystems

**Purpose:** Ship weapons and targeting

**Attributes:**

- `phaser_arrays` (int): Number of phasers (default: 4)
- `torpedo_tubes` (int): Number of torpedo launchers (default: 2)
- `torpedo_count` (int): Available torpedoes (default: 10)
- `phaser_range` / `torpedo_range` (int): Maximum ranges

**Methods:**

- `can_target(target_pos, ship_pos, orientation) -> bool`: Check if target is in range/arc
- `calculate_damage(weapon_type, target) -> int`: Calculate damage
- `fire_weapon(weapon_type) -> bool`: Execute weapon firing

---

### ShieldSystems

**Purpose:** Defensive shields

**Attributes:**

- `shield_strength` (float): Current shield level (0-100)
- `max_shield_strength` (float): Maximum capacity
- `recharge_rate` (float): Recharge per second

**Methods:**

- `absorb_damage(damage, damage_type) -> int`: Absorb damage, return overflow
- `recharge_shields(amount)`: Manual recharge

---

### EngineSystems

**Purpose:** Propulsion and movement

**Attributes:**

- `impulse_power` (float): Current power level (0.0-1.0)
- `warp_capable` (bool): Can go to warp
- `fuel` / `max_fuel` (float): Fuel levels

**Methods:**

- `calculate_movement_cost(distance) -> float`: Calculate fuel cost
- `set_impulse_power(level)`: Adjust power

---

### SensorSystems

**Purpose:** Detection and scanning

**Attributes:**

- `short_range` (int): Short range distance (default: 3)
- `long_range` (int): Long range distance (default: 10)
- `passive_mode` (bool): Passive vs active scanning

**Methods:**

- `scan_range() -> int`: Get effective range
- `set_passive_mode(passive)`: Toggle mode
- `detect_targets(position, targets) -> list`: Scan for targets in range

---

### LifeSupportSystems

**Purpose:** Crew life support

**Attributes:**

- `atmosphere_quality` (float): Air quality (0-100)
- `temperature` (float): Temperature in Celsius
- `gravity` (float): Artificial gravity level

**Methods:**

- `maintain_environment()`: Update environmental conditions
- `emergency_mode()`: Switch to emergency life support

---

## Usage Example

```python
from game.components.ship_systems import WeaponSystems, ShieldSystems

# Weapons
weapons = WeaponSystems()
if weapons.can_target(target_pos, ship_pos, orientation):
    damage = weapons.calculate_damage("phaser", target)
    weapons.fire_weapon("phaser")

# Shields
shields = ShieldSystems()
remaining_damage = shields.absorb_damage(50, "energy")
print(f"Shield strength: {shields.shield_strength}")
```

---

## Integration Points

**Dependencies:** None (self-contained components)

**Used by:**

- `game.entities.starship.Starship` - Composition pattern

---

## Change History

- **10-30-2025** - Documentation created
- **10-29-2025** - Ship system components implemented
