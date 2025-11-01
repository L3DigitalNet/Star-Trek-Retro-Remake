# Ship Systems Documentation

**File:** `STRR/src/game/components/ship_systems.py`
**Version:** 0.0.22
**Last Updated:** 10-31-2025

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

### ResourceManager

**Purpose:** Energy, fuel, and supplies management

**Attributes:**

- `energy_capacity` / `energy_current` (float): Energy reserves
- `energy_regen_rate` (float): Regeneration per second
- `fuel_capacity` / `fuel_current` (float): Fuel reserves
- `fuel_consumption` (float): Fuel consumption rate
- `supplies` (dict[str, int]): Medical supplies and spare parts
- `power_distribution` (dict[str, float]): Power allocation percentages
- `energy_costs` (dict[str, float]): Energy cost per action

**Methods:**

- `allocate_power(system, percentage)`: Set power distribution
- `consume_energy(action)`: Use energy for action
- `regenerate_energy(dt)`: Add energy from engines
- `consume_fuel(amount)`: Use fuel
- `refuel(amount)`: Add fuel to reserves
- `resupply(supply_type, amount)`: Restock supplies
- `use_supplies(supply_type, amount)`: Consume supplies
- `has_energy(amount)`: Check available energy
- `get_system_power(system)`: Get power allocation

**Configuration:** Loads from `game_settings.toml` [game.resources] section

---

### CrewManager

**Purpose:** Crew roster, morale, and efficiency

**Attributes:**

- `crew_roster` (dict[str, str]): Crew positions and names
- `morale` (float): Current morale (0-100)
- `base_efficiency` (float): Base efficiency multiplier
- `turns_since_starbase` (int): Turns since last starbase visit
- `casualties` (int): Casualties since starbase
- `combat_victories` / `combat_defeats` (int): Combat record
- `morale_modifiers` (dict[str, float]): Configurable morale changes

**Methods:**

- `get_efficiency_multiplier()`: Calculate efficiency from morale (0.8 - 1.2)
- `update_morale(change)`: Directly modify morale
- `record_combat_outcome(victory)`: Update morale from combat result
- `record_casualty()`: Decrease morale for crew loss
- `visit_starbase()`: Reset counters and boost morale
- `assign_crew(position, name)`: Change crew assignment

**Configuration:** Loads from `game_settings.toml` [game.crew] section

**Efficiency Tiers:**

- High morale (>80): 1.2x efficiency bonus
- Normal morale (60-80): 1.0x efficiency
- Low morale (40-60): 0.9x efficiency
- Very low morale (<40): 0.8x efficiency penalty

---

## Usage Example

```python
from game.components.ship_systems import WeaponSystems, ShieldSystems, ResourceManager, CrewManager

# Weapons
weapons = WeaponSystems()
if weapons.can_target(target_pos, ship_pos, orientation):
    damage = weapons.calculate_damage("phaser", distance, target)
    weapons.fire_weapon("phaser")

# Shields
shields = ShieldSystems()
remaining_damage = shields.absorb_damage(50, "energy", ship_orientation, attacker_pos, ship_pos)
print(f"Shield strength: {shields.total_shield_strength}")

# Resources
resources = ResourceManager()
if resources.has_energy(15.0):
    resources.consume_energy("fire_phaser")
resources.allocate_power("shields", 40.0)
resources.regenerate_energy(1.0)

# Crew
crew = CrewManager()
crew.record_combat_outcome(victory=True)  # +5 morale
efficiency = crew.get_efficiency_multiplier()  # 0.8 - 1.2
crew.visit_starbase()  # +20 morale, reset counters
```

---

## Integration Points

**Dependencies:**

- `pathlib.Path` - For config file location
- `tomllib` - For loading TOML configuration

**Configuration Files:**

- `STRR/config/game_settings.toml` - [game.resources] and [game.crew] sections

**Used by:**

- `game.entities.starship.Starship` - Composition pattern for all ship systems

---

## Change History

- **10-31-2025** - Added ResourceManager and CrewManager components (v0.0.22)
- **10-30-2025** - Documentation created
- **10-29-2025** - Ship system components implemented
