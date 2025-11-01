#!/usr/bin/env python3
"""
Star Trek Retro Remake - Ship Systems Components

Description:
    Ship system components implementing the Component pattern for modular
    starship subsystems.

Author: Star Trek Retro Remake Development Team
Email: development@star-trek-retro-remake.org
GitHub: https://github.com/L3DigitalNet/Star-Trek-Retro-Remake
Date Created: 10-29-2025
Date Changed: 11-01-2025 (v0.0.29 - Refactored to use centralized config loader)
License: MIT

Features:
    - Component pattern for ship subsystems
    - Weapon systems with firing arcs, line of sight, and accuracy
    - Shield systems with directional facings (forward/aft/port/starboard)
    - Damage and repair mechanics with critical hits
    - Power usage and efficiency tracking
    - Range-based damage and hit calculations
    - Resource management (energy, fuel, supplies)
    - Crew morale and efficiency system
    - Power distribution between ship systems

Requirements:
    - Linux environment
    - Python 3.14+ for latest language features

Classes:
    - ShipSystem: Base class for all ship subsystems
    - WeaponSystems: Ship weapons with targeting and firing arcs
    - ShieldSystems: Defensive shield management with facings
    - EngineSystems: Propulsion and movement
    - SensorSystems: Detection and scanning
    - LifeSupportSystems: Crew life support
    - ResourceManager: Energy, fuel, and supplies management
    - CrewManager: Crew roster, morale, and efficiency

Functions:
    - None
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..entities.base import GameObject, GridPosition
    from ..entities.starship import Starship

from ...engine.config_loader import get_combat_config

__version__ = "0.0.29"


class ShipSystem(ABC):
    """
    Base class for all ship subsystems.

    Implements the core Component pattern interface for ship systems
    with damage tracking, efficiency management, and power usage.

    Attributes:
        name: System name identifier
        efficiency: Current system efficiency (0.0 to max_efficiency)
        max_efficiency: Maximum system efficiency
        damaged: Whether the system is damaged
        active: Whether the system is currently active
        power_usage: Current power consumption

    Public methods:
        update: Update system state each game tick
        repair: Repair system damage
        damage: Apply damage to the system

    Private methods:
        None
    """

    def __init__(self, name: str, max_efficiency: float = 1.0):
        """
        Initialize a ship system.

        Args:
            name: System name identifier
            max_efficiency: Maximum efficiency rating
        """
        self.name = name
        self.efficiency = max_efficiency
        self.max_efficiency = max_efficiency
        self.damaged = False
        self.active = True
        self.power_usage = 0.0

    @abstractmethod
    def update(self, dt: float) -> None:
        """
        Update system state.

        Args:
            dt: Time delta since last update in seconds
        """
        pass

    def repair(self, amount: float) -> None:
        """
        Repair system damage.

        Args:
            amount: Amount of repair to apply
        """
        self.efficiency = min(self.max_efficiency, self.efficiency + amount)
        if self.efficiency >= self.max_efficiency * 0.5:
            self.damaged = False

    def damage(self, amount: float) -> None:
        """
        Apply damage to system.

        Args:
            amount: Amount of damage to apply
        """
        self.efficiency = max(0, self.efficiency - amount)
        if self.efficiency < self.max_efficiency * 0.5:
            self.damaged = True
        if self.efficiency <= 0:
            self.active = False


class WeaponSystems(ShipSystem):
    """
    Manages ship weapons and targeting.

    Handles phaser arrays, torpedo launchers, targeting calculations,
    and damage output for starship combat systems.

    Attributes:
        phaser_arrays: Number of phaser arrays
        torpedo_tubes: Number of torpedo launchers
        torpedo_count: Available torpedo count
        phaser_range: Maximum phaser range in grid cells
        torpedo_range: Maximum torpedo range in grid cells
        firing_arc: Firing arc in degrees (centered on forward)
        accuracy_base: Base accuracy percentage
        cooldown_time: Time between shots in seconds
        current_cooldown: Remaining cooldown time

    Public methods:
        can_target: Check if target is within firing arc and range
        calculate_damage: Calculate weapon damage against target
        fire_weapon: Execute weapon firing
        get_hit_chance: Calculate hit probability
        check_line_of_sight: Verify clear line of sight to target

    Private methods:
        _calculate_firing_angle: Get angle to target from ship orientation
        _is_in_firing_arc: Check if angle is within weapon arc
    """

    def __init__(self):
        """Initialize weapon systems with default configuration."""
        super().__init__("Weapons", 1.0)

        # Load combat configuration using centralized config loader
        config = get_combat_config()

        self.phaser_arrays = 4
        self.torpedo_tubes = 2
        self.torpedo_count = 10
        self.phaser_range = 5  # grid cells
        self.torpedo_range = 8  # grid cells
        self.firing_arc = config.get("weapon_firing_arc", 270)
        self.accuracy_base = config.get("weapon_accuracy_base", 0.85)
        self.cooldown_time = 1.0  # seconds between shots
        self.current_cooldown = 0.0

    def can_target(
        self,
        target_pos: GridPosition,
        ship_pos: GridPosition,
        ship_orientation: int,
        weapon_type: str = "phaser",
    ) -> bool:
        """
        Check if target is within firing arc and range.

        Args:
            target_pos: Position of the target
            ship_pos: Position of this ship
            ship_orientation: Current ship orientation in degrees
            weapon_type: Type of weapon to use

        Returns:
            True if target can be engaged, False otherwise
        """
        if not self.active or self.current_cooldown > 0:
            return False

        # Check weapon-specific range
        max_range = self.phaser_range if weapon_type == "phaser" else self.torpedo_range
        distance = ship_pos.distance_to(target_pos)

        if distance > max_range or distance < 0.1:  # Too close or too far
            return False

        # Check firing arc
        angle_to_target = self._calculate_firing_angle(
            ship_pos, target_pos, ship_orientation
        )
        return self._is_in_firing_arc(angle_to_target)

    def _calculate_firing_angle(
        self,
        ship_pos: GridPosition,
        target_pos: GridPosition,
        ship_orientation: int,
    ) -> float:
        """
        Calculate angle from ship orientation to target.

        Args:
            ship_pos: Ship's position
            target_pos: Target's position
            ship_orientation: Ship's facing direction in degrees

        Returns:
            Relative angle to target in degrees (-180 to 180)
        """
        import math

        # Calculate absolute angle to target
        dx = target_pos.x - ship_pos.x
        dy = target_pos.y - ship_pos.y
        angle_to_target = math.degrees(math.atan2(dy, dx))

        # Normalize to 0-360
        angle_to_target = angle_to_target % 360

        # Calculate relative angle from ship orientation
        relative_angle = angle_to_target - ship_orientation

        # Normalize to -180 to 180
        if relative_angle > 180:
            relative_angle -= 360
        elif relative_angle < -180:
            relative_angle += 360

        return relative_angle

    def _is_in_firing_arc(self, relative_angle: float) -> bool:
        """
        Check if angle is within firing arc.

        Args:
            relative_angle: Angle relative to ship orientation (-180 to 180)

        Returns:
            True if within firing arc
        """
        half_arc = self.firing_arc / 2.0
        return abs(relative_angle) <= half_arc

    def check_line_of_sight(
        self,
        ship_pos: GridPosition,
        target_pos: GridPosition,
        obstacles: list[GameObject],
    ) -> bool:
        """
        Check if there's a clear line of sight to target.

        Args:
            ship_pos: Position of firing ship
            target_pos: Position of target
            obstacles: List of potential obstructions

        Returns:
            True if line of sight is clear
        """
        # Simple line of sight check - verify no obstacles between ship and target
        for obstacle in obstacles:
            if hasattr(obstacle, "position") and hasattr(obstacle, "blocks_los"):
                if getattr(obstacle, "blocks_los", False):
                    # Check if obstacle is between ship and target
                    if self._is_between(ship_pos, target_pos, obstacle.position):
                        return False
        return True

    def _is_between(
        self, pos1: GridPosition, pos2: GridPosition, test_pos: GridPosition
    ) -> bool:
        """
        Check if test position is between two positions.

        Args:
            pos1: First position
            pos2: Second position
            test_pos: Position to test

        Returns:
            True if test_pos is approximately on the line between pos1 and pos2
        """
        # Calculate distance threshold
        threshold = 0.5

        # Calculate distances
        total_distance = pos1.distance_to(pos2)
        distance_1 = pos1.distance_to(test_pos)
        distance_2 = test_pos.distance_to(pos2)

        # Check if test_pos is roughly on the line
        return abs(distance_1 + distance_2 - total_distance) < threshold

    def get_hit_chance(self, distance: float, weapon_type: str) -> float:
        """
        Calculate hit probability based on range and conditions.

        Args:
            distance: Distance to target in grid cells
            weapon_type: Type of weapon being used

        Returns:
            Hit chance as a percentage (0.0 to 1.0)
        """
        max_range = self.phaser_range if weapon_type == "phaser" else self.torpedo_range

        # Guard against division by zero
        if max_range <= 0:
            return 0.1  # Minimum hit chance if weapon has no range

        # Get range penalty from config
        config = get_combat_config()
        range_penalty = config.get("weapon_range_penalty", 0.4)

        # Base accuracy modified by range
        range_factor = 1.0 - (distance / max_range) * range_penalty

        # Apply system efficiency
        final_accuracy = self.accuracy_base * range_factor * self.efficiency

        return max(0.1, min(1.0, final_accuracy))  # Clamp between 10% and 100%

    def calculate_damage(
        self, weapon_type: str, distance: float, target: Starship | None = None
    ) -> int:
        """
        Calculate weapon damage against target.

        Args:
            weapon_type: Type of weapon (phaser, torpedo)
            distance: Distance to target in grid cells
            target: Target starship (optional, for future enhancements)

        Returns:
            Calculated damage amount
        """
        # Base damage by weapon type
        if weapon_type == "phaser":
            base_damage = 15
            # Phasers lose effectiveness at range
            range_modifier = 1.0 - (distance / self.phaser_range) * 0.3
        else:  # torpedo
            base_damage = 30
            # Torpedoes maintain damage at range
            range_modifier = 1.0

        # Apply system efficiency
        final_damage = base_damage * self.efficiency * range_modifier

        return int(max(1, final_damage))  # Minimum 1 damage

    def fire_weapon(self, weapon_type: str) -> bool:
        """
        Execute weapon firing.

        Args:
            weapon_type: Type of weapon to fire

        Returns:
            True if weapon fired successfully, False otherwise
        """
        if not self.active or self.current_cooldown > 0:
            return False

        if weapon_type == "torpedo":
            if self.torpedo_count > 0:
                self.torpedo_count -= 1
                self.current_cooldown = self.cooldown_time
                return True
            return False
        elif weapon_type == "phaser":
            self.current_cooldown = self.cooldown_time * 0.5  # Phasers cool faster
            return True

        return False

    def update(self, dt: float) -> None:
        """Update weapon systems state."""
        if not self.active:
            return

        # Update cooldown timer
        if self.current_cooldown > 0:
            self.current_cooldown = max(0, self.current_cooldown - dt)


class ShieldSystems(ShipSystem):
    """
    Manages defensive shields with facing system.

    Handles shield strength, recharging, and damage absorption
    for starship defensive systems with directional shield facings.

    Attributes:
        shield_facings: Dictionary of shield strength by facing
        max_shield_per_facing: Maximum shield strength per facing
        total_shield_strength: Total current shield strength
        max_shield_strength: Total maximum shield capacity
        recharge_rate: Shield recharge rate per second
        facing_names: Valid shield facing names

    Public methods:
        absorb_damage: Absorb incoming damage on specific facing
        recharge_shields: Manually trigger shield recharge
        get_facing_strength: Get shield strength for specific facing
        distribute_shields: Redistribute shields across facings
        get_total_shields: Get total shield strength across all facings

    Private methods:
        _determine_hit_facing: Calculate which facing was hit
        _calculate_angle_to_attacker: Get angle from target to attacker
    """

    def __init__(self):
        """Initialize shield systems with default configuration."""
        super().__init__("Shields", 1.0)

        # Shield facing system - directional shields
        self.facing_names = ["forward", "aft", "port", "starboard"]
        self.max_shield_per_facing = 25.0
        self.shield_facings: dict[str, float] = {
            "forward": 25.0,
            "aft": 25.0,
            "port": 25.0,
            "starboard": 25.0,
        }

        self.max_shield_strength = 100.0  # Total capacity
        self.recharge_rate = 2.0  # per second per facing

    @property
    def total_shield_strength(self) -> float:
        """Get total shield strength across all facings."""
        return sum(self.shield_facings.values())

    def absorb_damage(
        self,
        damage: int,
        damage_type: str,
        ship_orientation: int = 0,
        attacker_pos: GridPosition | None = None,
        ship_pos: GridPosition | None = None,
    ) -> int:
        """
        Absorb damage and return remaining damage.

        Args:
            damage: Incoming damage amount
            damage_type: Type of damage (kinetic, energy, etc.)
            ship_orientation: Target ship's orientation in degrees
            attacker_pos: Position of attacker
            ship_pos: Position of target ship

        Returns:
            Remaining damage after shield absorption
        """
        if not self.active or self.total_shield_strength <= 0:
            return damage

        # Determine which facing was hit
        if attacker_pos and ship_pos:
            facing = self._determine_hit_facing(
                ship_pos, attacker_pos, ship_orientation
            )
        else:
            # Default to forward if positions not provided
            facing = "forward"

        # Load combat configuration
        config = get_combat_config()

        # Shield effectiveness based on damage type (from config)
        if damage_type == "energy":
            effectiveness = config.get("shield_energy_effectiveness", 0.85)
        else:
            effectiveness = config.get("shield_kinetic_effectiveness", 0.65)

        # Calculate maximum possible absorption for this facing
        facing_strength = self.shield_facings[facing]
        max_absorption = damage * effectiveness

        # Shields absorb at least some damage when active (from config)
        min_absorption_rate = config.get("shield_min_absorption", 0.1)
        min_absorption = min(damage * min_absorption_rate, facing_strength)
        absorbed = max(min_absorption, min(max_absorption, facing_strength))

        # Apply damage to this facing
        self.shield_facings[facing] = max(0, facing_strength - absorbed)

        # Calculate remaining damage
        remaining_damage = int(damage - absorbed)

        return remaining_damage

    def _determine_hit_facing(
        self,
        ship_pos: GridPosition,
        attacker_pos: GridPosition,
        ship_orientation: int,
    ) -> str:
        """
        Determine which shield facing was hit.

        Args:
            ship_pos: Position of ship being hit
            attacker_pos: Position of attacker
            ship_orientation: Ship's orientation in degrees

        Returns:
            Name of shield facing that was hit
        """
        import math

        # Calculate angle from ship to attacker
        dx = attacker_pos.x - ship_pos.x
        dy = attacker_pos.y - ship_pos.y
        angle_to_attacker = math.degrees(math.atan2(dy, dx))

        # Normalize to 0-360
        angle_to_attacker = angle_to_attacker % 360

        # Calculate relative angle
        relative_angle = (angle_to_attacker - ship_orientation) % 360

        # Determine facing based on relative angle
        # Forward: 315-45 degrees, Right: 45-135, Aft: 135-225, Left: 225-315
        if relative_angle < 45 or relative_angle >= 315:
            return "forward"
        elif relative_angle < 135:
            return "starboard"
        elif relative_angle < 225:
            return "aft"
        else:
            return "port"

    def get_facing_strength(self, facing: str) -> float:
        """
        Get shield strength for specific facing.

        Args:
            facing: Name of facing (forward, aft, port, starboard)

        Returns:
            Shield strength for that facing
        """
        return self.shield_facings.get(facing, 0.0)

    def distribute_shields(self, distribution: dict[str, float]) -> bool:
        """
        Redistribute shields across facings.

        Args:
            distribution: Dictionary of facing names to strength values

        Returns:
            True if redistribution was successful
        """
        # Validate total doesn't exceed maximum
        total = sum(distribution.values())
        if total > self.max_shield_strength:
            return False

        # Validate each facing doesn't exceed per-facing maximum
        for _facing, strength in distribution.items():
            if strength > self.max_shield_per_facing:
                return False

        # Apply distribution
        self.shield_facings.update(distribution)
        return True

    def recharge_shields(self, amount: float, facing: str | None = None) -> None:
        """
        Manually trigger shield recharge.

        Args:
            amount: Amount of shield strength to restore
            facing: Specific facing to recharge (None for all facings)
        """
        if facing:
            # Recharge specific facing
            current = self.shield_facings.get(facing, 0.0)
            self.shield_facings[facing] = min(
                self.max_shield_per_facing, current + amount
            )
        else:
            # Recharge all facings proportionally
            current_total = self.total_shield_strength
            if current_total < self.max_shield_strength:
                amount_per_facing = amount / len(self.facing_names)
                for facing in self.facing_names:
                    current = self.shield_facings[facing]
                    self.shield_facings[facing] = min(
                        self.max_shield_per_facing, current + amount_per_facing
                    )

    def update(self, dt: float) -> None:
        """Recharge shields over time."""
        if not self.active:
            return

        # Recharge all facings gradually
        for facing in self.facing_names:
            current = self.shield_facings[facing]
            if current < self.max_shield_per_facing:
                recharge = self.recharge_rate * dt * self.efficiency
                self.shield_facings[facing] = min(
                    self.max_shield_per_facing, current + recharge
                )


class EngineSystems(ShipSystem):
    """
    Manages propulsion and movement.

    Handles impulse and warp drive systems, fuel consumption,
    and movement calculations for starship propulsion.

    Attributes:
        impulse_power: Current impulse drive power
        warp_capable: Whether ship has warp capability
        fuel: Current fuel level
        max_fuel: Maximum fuel capacity

    Public methods:
        calculate_movement_cost: Calculate fuel cost for movement
        set_impulse_power: Adjust impulse drive power

    Private methods:
        None
    """

    def __init__(self):
        """Initialize engine systems with default configuration."""
        super().__init__("Engines", 1.0)
        self.impulse_power = 1.0
        self.warp_capable = True
        self.fuel = 100.0
        self.max_fuel = 100.0

    def calculate_movement_cost(self, distance: int) -> float:
        """
        Calculate fuel cost for movement.

        Args:
            distance: Distance to travel in grid cells

        Returns:
            Fuel cost for the movement
        """
        return distance * 0.5 / self.efficiency

    def set_impulse_power(self, power_level: float) -> None:
        """
        Adjust impulse drive power.

        Args:
            power_level: New power level (0.0 to 1.0)
        """
        self.impulse_power = max(0.0, min(1.0, power_level))

    def update(self, dt: float) -> None:
        """Update engine systems state."""
        if not self.active:
            return
        # Engine maintenance, fuel consumption, etc.


class SensorSystems(ShipSystem):
    """
    Manages sensors and detection.

    Handles short and long range sensors, passive and active scanning,
    and target detection for starship sensor arrays.

    Attributes:
        short_range: Short range sensor distance
        long_range: Long range sensor distance
        passive_mode: Whether sensors are in passive mode

    Public methods:
        scan_range: Get current effective sensor range
        set_passive_mode: Toggle passive/active sensor mode
        detect_targets: Scan for targets in range

    Private methods:
        None
    """

    def __init__(self):
        """Initialize sensor systems with default configuration."""
        super().__init__("Sensors", 1.0)
        self.short_range = 3  # grid cells
        self.long_range = 10  # grid cells
        self.passive_mode = True

    def scan_range(self) -> int:
        """
        Get current effective sensor range.

        Returns:
            Current sensor range in grid cells
        """
        base_range = self.long_range if not self.passive_mode else self.short_range
        return int(base_range * self.efficiency)

    def set_passive_mode(self, passive: bool) -> None:
        """
        Toggle passive/active sensor mode.

        Args:
            passive: True for passive mode, False for active
        """
        self.passive_mode = passive

    def detect_targets(self, ship_position: GridPosition, targets: list) -> list:
        """
        Scan for targets in range.

        Args:
            ship_position: Position of the scanning ship
            targets: List of potential targets to scan

        Returns:
            List of detected targets within range
        """
        detected = []
        scan_range = self.scan_range()

        for target in targets:
            if hasattr(target, "position"):
                distance = ship_position.distance_to(target.position)
                if distance <= scan_range:
                    detected.append(target)

        return detected

    def update(self, dt: float) -> None:
        """Update sensor systems state."""
        if not self.active:
            return
        # Sensor sweeps, data processing, etc.


class LifeSupportSystems(ShipSystem):
    """
    Manages crew life support systems.

    Handles environmental controls, atmosphere management,
    and crew health for starship life support.

    Attributes:
        atmosphere_quality: Current atmosphere quality
        temperature: Current temperature level
        gravity: Current artificial gravity level

    Public methods:
        maintain_environment: Update environmental conditions
        emergency_mode: Switch to emergency life support

    Private methods:
        None
    """

    def __init__(self):
        """Initialize life support systems with default configuration."""
        super().__init__("Life Support", 1.0)
        self.atmosphere_quality = 100.0
        self.temperature = 20.0  # Celsius
        self.gravity = 1.0  # Earth gravity

    def maintain_environment(self) -> None:
        """Update environmental conditions based on system efficiency."""
        if self.active:
            self.atmosphere_quality = min(100.0, self.efficiency * 100.0)
        else:
            self.atmosphere_quality = max(0.0, self.atmosphere_quality - 1.0)

    def emergency_mode(self) -> None:
        """Switch to emergency life support mode."""
        if self.efficiency > 0.25:
            self.atmosphere_quality = 50.0
            self.temperature = 15.0
            self.gravity = 0.8

    def update(self, dt: float) -> None:
        """Update life support systems state."""
        if not self.active:
            return
        self.maintain_environment()


class ResourceManager(ShipSystem):
    """
    Manages ship energy, fuel, and supplies.

    Handles power distribution between systems, energy consumption/regeneration,
    fuel tracking, and supply management for starship operations.

    Attributes:
        energy_current: Current energy reserves (0-energy_capacity)
        energy_capacity: Maximum energy capacity
        energy_regen_rate: Energy regeneration per second from engines
        fuel_current: Current fuel reserves (0-fuel_capacity)
        fuel_capacity: Maximum fuel capacity
        fuel_consumption: Fuel consumption rate per turn
        supplies: Dictionary of supply types and quantities
        power_distribution: Power allocation percentages by system

    Public methods:
        allocate_power: Set power distribution percentages
        consume_energy: Use energy for actions
        regenerate_energy: Add energy from engines
        consume_fuel: Use fuel for movement/operations
        refuel: Add fuel to reserves
        resupply: Restock supplies at starbase
        get_system_power: Get power allocation for a system
        has_energy: Check if enough energy available

    Private methods:
        _load_config: Load resource settings from TOML
        _validate_power_distribution: Ensure power allocations sum to 100%
    """

    # Class-level configuration cache
    _resource_config: dict[str, float | int] | None = None

    def __init__(self):
        """Initialize resource manager with default configuration."""
        super().__init__("Resources", 1.0)

        # Load configuration
        config = self._load_config()

        # Energy system
        self.energy_capacity: float = config.get("energy_capacity", 1000.0)
        self.energy_current: float = self.energy_capacity
        self.energy_regen_rate: float = config.get("energy_regen_rate", 10.0)

        # Fuel system
        self.fuel_capacity: float = config.get("fuel_capacity", 500.0)
        self.fuel_current: float = self.fuel_capacity
        self.fuel_consumption: float = config.get("fuel_consumption", 5.0)

        # Supplies tracking
        self.supplies: dict[str, int] = {
            "medical": int(config.get("medical_supplies", 100)),
            "spare_parts": int(config.get("spare_parts", 50)),
        }

        # Power distribution (percentages for each system)
        self.power_distribution: dict[str, float] = {
            "shields": 25.0,
            "weapons": 25.0,
            "engines": 30.0,
            "sensors": 10.0,
            "life_support": 10.0,
        }

        # Energy consumption rates per action (from config)
        self.energy_costs: dict[str, float] = {
            "move": config.get("energy_cost_move", 10.0),
            "fire_phaser": config.get("energy_cost_fire_phaser", 15.0),
            "fire_torpedo": config.get("energy_cost_fire_torpedo", 25.0),
            "scan": config.get("energy_cost_scan", 5.0),
            "shield_regen": config.get("energy_cost_shield_regen", 20.0),
        }

    @classmethod
    def _load_config(cls) -> dict[str, float | int]:
        """
        Load resource configuration from TOML file.

        Returns:
            Dictionary of resource configuration values
        """
        # Return cached config if available
        if cls._resource_config is not None:
            return cls._resource_config

        # Default configuration
        defaults: dict[str, float | int] = {
            "energy_capacity": 1000.0,
            "energy_regen_rate": 10.0,
            "fuel_capacity": 500.0,
            "fuel_consumption": 5.0,
            "medical_supplies": 100,
            "spare_parts": 50,
            "energy_cost_move": 10.0,
            "energy_cost_fire_phaser": 15.0,
            "energy_cost_fire_torpedo": 25.0,
            "energy_cost_scan": 5.0,
            "energy_cost_shield_regen": 20.0,
        }

        # Try to load from TOML configuration
        try:
            config_path = Path(__file__).parents[2] / "config" / "game_settings.toml"
            if config_path.exists():
                with open(config_path, "rb") as f:
                    config_data = tomllib.load(f)
                    resources = config_data.get("game", {}).get("resources", {})
                    defaults.update(resources)
        except Exception:
            pass  # Use defaults if config loading fails

        cls._resource_config = defaults
        return defaults

    def allocate_power(self, system: str, percentage: float) -> bool:
        """
        Set power distribution percentage for a system.

        Args:
            system: System name (shields, weapons, engines, sensors, life_support)
            percentage: Power allocation percentage (0-100)

        Returns:
            True if allocation successful, False if invalid
        """
        if system not in self.power_distribution:
            return False

        if percentage < 0 or percentage > 100:
            return False

        self.power_distribution[system] = percentage
        return True

    def _validate_power_distribution(self) -> bool:
        """
        Validate power distribution sums to ~100%.

        Returns:
            True if distribution is valid
        """
        total = sum(self.power_distribution.values())
        return 95.0 <= total <= 105.0  # Allow small tolerance

    def get_system_power(self, system: str) -> float:
        """
        Get power allocation for a system.

        Args:
            system: System name

        Returns:
            Power allocation percentage (0-100)
        """
        return self.power_distribution.get(system, 0.0)

    def has_energy(self, amount: float) -> bool:
        """
        Check if enough energy is available.

        Args:
            amount: Energy amount to check

        Returns:
            True if energy is available
        """
        return self.energy_current >= amount

    def consume_energy(self, action: str) -> bool:
        """
        Consume energy for an action.

        Args:
            action: Action name (move, fire_phaser, fire_torpedo, scan, shield_regen)

        Returns:
            True if energy was consumed, False if insufficient
        """
        cost = self.energy_costs.get(action, 0.0)
        if self.energy_current >= cost:
            self.energy_current = max(0.0, self.energy_current - cost)
            return True
        return False

    def regenerate_energy(self, dt: float) -> None:
        """
        Regenerate energy based on engine power allocation.

        Args:
            dt: Time delta in seconds
        """
        if not self.active:
            return

        # Regeneration affected by engine power allocation and efficiency
        engine_power_factor = self.power_distribution.get("engines", 30.0) / 100.0
        regen = self.energy_regen_rate * engine_power_factor * self.efficiency * dt
        self.energy_current = min(self.energy_capacity, self.energy_current + regen)

    def consume_fuel(self, amount: float | None = None) -> bool:
        """
        Consume fuel for operations.

        Args:
            amount: Fuel amount to consume (uses default if None)

        Returns:
            True if fuel was consumed, False if insufficient
        """
        consumption = amount if amount is not None else self.fuel_consumption
        if self.fuel_current >= consumption:
            self.fuel_current = max(0.0, self.fuel_current - consumption)
            return True
        return False

    def refuel(self, amount: float) -> None:
        """
        Add fuel to reserves.

        Args:
            amount: Fuel amount to add
        """
        self.fuel_current = min(self.fuel_capacity, self.fuel_current + amount)

    def resupply(self, supply_type: str, amount: int) -> None:
        """
        Restock supplies.

        Args:
            supply_type: Type of supply (medical, spare_parts)
            amount: Amount to add
        """
        if supply_type in self.supplies:
            self.supplies[supply_type] = self.supplies[supply_type] + amount

    def use_supplies(self, supply_type: str, amount: int) -> bool:
        """
        Use supplies for operations.

        Args:
            supply_type: Type of supply (medical, spare_parts)
            amount: Amount to use

        Returns:
            True if supplies were used, False if insufficient
        """
        if supply_type in self.supplies and self.supplies[supply_type] >= amount:
            self.supplies[supply_type] -= amount
            return True
        return False

    def update(self, dt: float) -> None:
        """
        Update resource systems state.

        Args:
            dt: Time delta in seconds
        """
        if not self.active:
            return

        # Regenerate energy from engines
        self.regenerate_energy(dt)


class CrewManager(ShipSystem):
    """
    Manages crew roster, morale, and efficiency.

    Handles crew assignments, morale tracking based on mission outcomes,
    and efficiency bonuses/penalties affecting ship system performance.

    Attributes:
        crew_roster: Dictionary of crew positions and names
        morale: Current crew morale (0-100)
        base_efficiency: Base efficiency multiplier (0-2.0)
        turns_since_starbase: Turns since last starbase visit
        casualties: Number of casualties since last starbase
        combat_victories: Recent combat victories
        combat_defeats: Recent combat defeats

    Public methods:
        get_efficiency_multiplier: Calculate efficiency based on morale
        update_morale: Update morale based on events
        record_combat_outcome: Record combat victory/defeat
        record_casualty: Record crew casualty
        visit_starbase: Reset morale and casualty counters
        assign_crew: Assign crew member to position

    Private methods:
        _load_config: Load crew settings from TOML
        _calculate_morale_modifiers: Calculate morale from various factors
    """

    # Class-level configuration cache
    _crew_config: dict[str, float | int] | None = None

    def __init__(self):
        """Initialize crew manager with default configuration."""
        super().__init__("Crew", 1.0)

        # Load configuration
        config = self._load_config()

        # Crew roster (simplified for initial implementation)
        self.crew_roster: dict[str, str] = {
            "captain": "James T. Kirk",
            "first_officer": "Spock",
            "chief_engineer": "Montgomery Scott",
            "science_officer": "Spock",
            "security_chief": "Pavel Chekov",
            "helm_officer": "Hikaru Sulu",
        }

        # Morale and efficiency tracking
        self.morale: float = config.get("base_morale", 75.0)
        self.base_efficiency: float = 1.0

        # Mission tracking
        self.turns_since_starbase: int = 0
        self.casualties: int = 0
        self.combat_victories: int = 0
        self.combat_defeats: int = 0

        # Morale modifiers from config
        self.morale_modifiers: dict[str, float] = {
            "victory_bonus": config.get("morale_victory_bonus", 5.0),
            "defeat_penalty": config.get("morale_defeat_penalty", -10.0),
            "casualty_penalty": config.get("morale_casualty_penalty", -5.0),
            "turns_penalty": config.get("morale_turns_penalty", -0.5),
            "starbase_bonus": config.get("morale_starbase_bonus", 20.0),
        }

    @classmethod
    def _load_config(cls) -> dict[str, float | int]:
        """
        Load crew configuration from TOML file.

        Returns:
            Dictionary of crew configuration values
        """
        # Return cached config if available
        if cls._crew_config is not None:
            return cls._crew_config

        # Default configuration
        defaults: dict[str, float | int] = {
            "base_morale": 75.0,
            "morale_victory_bonus": 5.0,
            "morale_defeat_penalty": -10.0,
            "morale_casualty_penalty": -5.0,
            "morale_turns_penalty": -0.5,
            "morale_starbase_bonus": 20.0,
            "efficiency_high_morale": 1.2,
            "efficiency_low_morale": 0.8,
        }

        # Try to load from TOML configuration
        try:
            config_path = Path(__file__).parents[2] / "config" / "game_settings.toml"
            if config_path.exists():
                with open(config_path, "rb") as f:
                    config_data = tomllib.load(f)
                    crew = config_data.get("game", {}).get("crew", {})
                    defaults.update(crew)
        except Exception:
            pass  # Use defaults if config loading fails

        cls._crew_config = defaults
        return defaults

    def get_efficiency_multiplier(self) -> float:
        """
        Calculate efficiency multiplier based on morale.

        Returns:
            Efficiency multiplier (0.5 - 1.5)
        """
        # High morale (>80) provides bonus, low morale (<50) provides penalty
        if self.morale >= 80:
            return 1.2  # 20% efficiency bonus
        elif self.morale >= 60:
            return 1.0  # Normal efficiency
        elif self.morale >= 40:
            return 0.9  # 10% efficiency penalty
        else:
            return 0.8  # 20% efficiency penalty

    def update_morale(self, change: float) -> None:
        """
        Update crew morale directly.

        Args:
            change: Morale change amount (positive or negative)
        """
        self.morale = max(0.0, min(100.0, self.morale + change))

    def record_combat_outcome(self, victory: bool) -> None:
        """
        Record combat victory or defeat and update morale.

        Args:
            victory: True if combat won, False if lost
        """
        if victory:
            self.combat_victories += 1
            self.update_morale(self.morale_modifiers["victory_bonus"])
        else:
            self.combat_defeats += 1
            self.update_morale(self.morale_modifiers["defeat_penalty"])

    def record_casualty(self) -> None:
        """Record crew casualty and update morale."""
        self.casualties += 1
        self.update_morale(self.morale_modifiers["casualty_penalty"])

    def visit_starbase(self) -> None:
        """Reset morale and counters after starbase visit."""
        self.update_morale(self.morale_modifiers["starbase_bonus"])
        self.turns_since_starbase = 0
        self.casualties = 0
        self.combat_victories = 0
        self.combat_defeats = 0

    def assign_crew(self, position: str, name: str) -> bool:
        """
        Assign crew member to position.

        Args:
            position: Crew position
            name: Crew member name

        Returns:
            True if assignment successful
        """
        if position in self.crew_roster:
            self.crew_roster[position] = name
            return True
        return False

    def _calculate_morale_modifiers(self) -> None:
        """Calculate and apply morale modifiers from various factors."""
        # Morale slowly decreases based on turns since starbase visit
        if self.turns_since_starbase > 10:
            turns_penalty = (self.turns_since_starbase - 10) * self.morale_modifiers[
                "turns_penalty"
            ]
            self.update_morale(turns_penalty)

    def update(self, dt: float) -> None:
        """
        Update crew systems state.

        Args:
            dt: Time delta in seconds
        """
        if not self.active:
            return

        # Increment turn counter
        self.turns_since_starbase += 1

        # Calculate and apply morale modifiers
        self._calculate_morale_modifiers()
