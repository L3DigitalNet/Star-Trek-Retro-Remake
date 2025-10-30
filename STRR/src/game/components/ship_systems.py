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
Date Changed: 10-31-2025
License: MIT

Features:
    - Component pattern for ship subsystems
    - Weapon systems with firing arcs, line of sight, and accuracy
    - Shield systems with directional facings (forward/aft/port/starboard)
    - Damage and repair mechanics with critical hits
    - Power usage and efficiency tracking
    - Range-based damage and hit calculations

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

Functions:
    - None
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..entities.base import GameObject, GridPosition
    from ..entities.starship import Starship

__version__ = "0.0.21"


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
        _load_combat_config: Load combat settings from configuration
    """

    _combat_config: dict[str, float] | None = None  # Class-level config cache

    def __init__(self):
        """Initialize weapon systems with default configuration."""
        super().__init__("Weapons", 1.0)

        # Load combat configuration
        config = self._load_combat_config()

        self.phaser_arrays = 4
        self.torpedo_tubes = 2
        self.torpedo_count = 10
        self.phaser_range = 5  # grid cells
        self.torpedo_range = 8  # grid cells
        self.firing_arc = config.get("weapon_firing_arc", 270)
        self.accuracy_base = config.get("weapon_accuracy_base", 0.85)
        self.cooldown_time = 1.0  # seconds between shots
        self.current_cooldown = 0.0

    @classmethod
    def _load_combat_config(cls) -> dict[str, float]:
        """
        Load combat configuration from game settings.

        Returns:
            Dictionary of combat configuration values
        """
        if cls._combat_config is None:
            try:
                from pathlib import Path
                import tomllib

                # Find config file relative to this module
                config_path = (
                    Path(__file__).parent.parent.parent
                    / "config"
                    / "game_settings.toml"
                )

                with open(config_path, "rb") as f:
                    settings = tomllib.load(f)
                    cls._combat_config = settings.get("game", {}).get("combat", {})
            except Exception:
                # Fallback to defaults if config can't be loaded
                cls._combat_config = {
                    "weapon_firing_arc": 270,
                    "weapon_accuracy_base": 0.85,
                    "weapon_range_penalty": 0.4,
                    "critical_hit_chance": 0.1,
                    "critical_hit_multiplier": 1.5,
                    "shield_energy_effectiveness": 0.85,
                    "shield_kinetic_effectiveness": 0.65,
                    "shield_min_absorption": 0.1,
                }

        return cls._combat_config

    def can_target(
        self,
        target_pos: "GridPosition",
        ship_pos: "GridPosition",
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
        ship_pos: "GridPosition",
        target_pos: "GridPosition",
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
        ship_pos: "GridPosition",
        target_pos: "GridPosition",
        obstacles: list["GameObject"],
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
        self, pos1: "GridPosition", pos2: "GridPosition", test_pos: "GridPosition"
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
        config = self._load_combat_config()
        range_penalty = config.get("weapon_range_penalty", 0.4)

        # Base accuracy modified by range
        range_factor = 1.0 - (distance / max_range) * range_penalty

        # Apply system efficiency
        final_accuracy = self.accuracy_base * range_factor * self.efficiency

        return max(0.1, min(1.0, final_accuracy))  # Clamp between 10% and 100%

    def calculate_damage(
        self, weapon_type: str, distance: float, target: "Starship" | None = None
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
        attacker_pos: "GridPosition | None" = None,
        ship_pos: "GridPosition | None" = None,
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
        config = WeaponSystems._load_combat_config()

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
        ship_pos: "GridPosition",
        attacker_pos: "GridPosition",
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
        for facing, strength in distribution.items():
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

    def detect_targets(self, ship_position: "GridPosition", targets: list) -> list:
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
