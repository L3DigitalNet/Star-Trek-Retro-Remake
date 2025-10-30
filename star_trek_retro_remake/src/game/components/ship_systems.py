#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Star Trek Retro Remake - Ship Systems Components

Description:
    Ship system components implementing the Component pattern for modular
    starship subsystems.

Author: Star Trek Retro Remake Development Team
Email: development@star-trek-retro-remake.org
GitHub: https://github.com/L3DigitalNet/Star-Trek-Retro-Remake
Date Created: 10-29-2025
Date Changed: 10-29-2025
License: MIT

Features:
    - Component pattern for ship subsystems
    - Weapon, shield, engine, and sensor systems
    - Damage and repair mechanics
    - Power usage and efficiency tracking

Requirements:
    - Linux environment
    - Python 3.14+ for latest language features

Classes:
    - ShipSystem: Base class for all ship subsystems
    - WeaponSystems: Ship weapons and targeting
    - ShieldSystems: Defensive shield management
    - EngineSystems: Propulsion and movement
    - SensorSystems: Detection and scanning
    - LifeSupportSystems: Crew life support

Functions:
    - None
"""

from abc import ABC, abstractmethod
from typing import Final, TYPE_CHECKING

if TYPE_CHECKING:
    from ..entities.base import GridPosition
    from ..entities.starship import Starship

__version__: Final[str] = "0.0.1"


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

    Public methods:
        can_target: Check if target is within firing arc and range
        calculate_damage: Calculate weapon damage against target
        fire_weapon: Execute weapon firing

    Private methods:
        None
    """

    def __init__(self):
        """Initialize weapon systems with default configuration."""
        super().__init__("Weapons", 1.0)
        self.phaser_arrays = 4
        self.torpedo_tubes = 2
        self.torpedo_count = 10
        self.phaser_range = 5  # grid cells
        self.torpedo_range = 8  # grid cells

    def can_target(self, target_pos: 'GridPosition', ship_pos: 'GridPosition',
                   ship_orientation: int) -> bool:
        """
        Check if target is within firing arc and range.

        Args:
            target_pos: Position of the target
            ship_pos: Position of this ship
            ship_orientation: Current ship orientation

        Returns:
            True if target can be engaged, False otherwise
        """
        distance = ship_pos.distance_to(target_pos)

        # Check range
        if distance > self.phaser_range:
            return False

        # Check firing arc (simplified to forward 180 degrees)
        # TODO: Implement proper arc calculations based on orientation
        return True

    def calculate_damage(self, weapon_type: str, target: 'Starship') -> int:
        """
        Calculate weapon damage against target.

        Args:
            weapon_type: Type of weapon (phaser, torpedo)
            target: Target starship

        Returns:
            Calculated damage amount
        """
        base_damage = 10 if weapon_type == "phaser" else 25
        return int(base_damage * self.efficiency)

    def fire_weapon(self, weapon_type: str) -> bool:
        """
        Execute weapon firing.

        Args:
            weapon_type: Type of weapon to fire

        Returns:
            True if weapon fired successfully, False otherwise
        """
        if not self.active:
            return False

        if weapon_type == "torpedo" and self.torpedo_count > 0:
            self.torpedo_count -= 1
            return True
        elif weapon_type == "phaser":
            return True

        return False

    def update(self, dt: float) -> None:
        """Update weapon systems state."""
        if not self.active:
            return
        # Weapon cooling, recharge, etc.


class ShieldSystems(ShipSystem):
    """
    Manages defensive shields.

    Handles shield strength, recharging, and damage absorption
    for starship defensive systems.

    Attributes:
        shield_strength: Current shield strength
        max_shield_strength: Maximum shield capacity
        recharge_rate: Shield recharge rate per second

    Public methods:
        absorb_damage: Absorb incoming damage
        recharge_shields: Manually trigger shield recharge

    Private methods:
        None
    """

    def __init__(self):
        """Initialize shield systems with default configuration."""
        super().__init__("Shields", 1.0)
        self.shield_strength = 100.0
        self.max_shield_strength = 100.0
        self.recharge_rate = 5.0  # per second

    def absorb_damage(self, damage: int, damage_type: str) -> int:
        """
        Absorb damage and return remaining damage.

        Args:
            damage: Incoming damage amount
            damage_type: Type of damage (kinetic, energy, etc.)

        Returns:
            Remaining damage after shield absorption
        """
        if not self.active or self.shield_strength <= 0:
            return damage

        # Shield effectiveness based on damage type
        effectiveness = 0.8 if damage_type == "energy" else 0.6
        absorbed = min(damage * effectiveness, self.shield_strength)

        self.shield_strength -= absorbed
        return int(damage - absorbed)

    def recharge_shields(self, amount: float) -> None:
        """
        Manually trigger shield recharge.

        Args:
            amount: Amount of shield strength to restore
        """
        self.shield_strength = min(self.max_shield_strength,
                                 self.shield_strength + amount)

    def update(self, dt: float) -> None:
        """Recharge shields over time."""
        if self.active and self.shield_strength < self.max_shield_strength:
            recharge = self.recharge_rate * dt * self.efficiency
            self.shield_strength = min(self.max_shield_strength,
                                     self.shield_strength + recharge)


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

    def detect_targets(self, ship_position: 'GridPosition',
                      targets: list) -> list:
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
            if hasattr(target, 'position'):
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