#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Star Trek Retro Remake - Ship Systems Tests

Description:
    Unit tests for ship component systems including weapons, shields,
    engines, sensors, and life support.

Author: Star Trek Retro Remake Development Team
Email: development@star-trek-retro-remake.org
GitHub: https://github.com/L3DigitalNet/Star-Trek-Retro-Remake
Date Created: 10-30-2025
Date Changed: 10-30-2025
License: MIT

Test Coverage:
    - ShipSystem base class functionality
    - WeaponSystems: targeting, damage, firing
    - ShieldSystems: damage absorption, recharge
    - EngineSystems: movement cost, fuel management
    - SensorSystems: detection, scanning
    - LifeSupportSystems: environmental management

Requirements:
    - pytest >= 8.0.0
    - Python 3.14+
"""

from typing import Final
from unittest.mock import Mock

import pytest

from STRR.src.game.components.ship_systems import (
    ShipSystem,
    WeaponSystems,
    ShieldSystems,
    EngineSystems,
    SensorSystems,
    LifeSupportSystems,
)
from STRR.src.game.entities.base import GridPosition

__version__: Final[str] = "0.0.18"


class TestShipSystemBase:
    """Test base ShipSystem class."""

    def test_ship_system_initialization(self):
        """Test basic system initialization."""

        # Arrange & Act
        class TestSystem(ShipSystem):
            def update(self, dt: float) -> None:
                pass

        system = TestSystem("Test System", 1.0)

        # Assert
        assert system.name == "Test System"
        assert system.efficiency == 1.0
        assert system.max_efficiency == 1.0
        assert system.damaged is False
        assert system.active is True
        assert system.power_usage == 0.0

    def test_ship_system_repair_increases_efficiency(self):
        """Test that repair increases system efficiency."""

        # Arrange
        class TestSystem(ShipSystem):
            def update(self, dt: float) -> None:
                pass

        system = TestSystem("Test System", 1.0)
        system.efficiency = 0.5

        # Act
        system.repair(0.3)

        # Assert
        assert system.efficiency == 0.8

    def test_ship_system_repair_caps_at_max_efficiency(self):
        """Test that repair doesn't exceed max efficiency."""

        # Arrange
        class TestSystem(ShipSystem):
            def update(self, dt: float) -> None:
                pass

        system = TestSystem("Test System", 1.0)
        system.efficiency = 0.9

        # Act
        system.repair(0.5)

        # Assert
        assert system.efficiency == 1.0

    def test_ship_system_repair_clears_damaged_flag(self):
        """Test that repairing above 50% clears damaged flag."""

        # Arrange
        class TestSystem(ShipSystem):
            def update(self, dt: float) -> None:
                pass

        system = TestSystem("Test System", 1.0)
        system.efficiency = 0.4
        system.damaged = True

        # Act
        system.repair(0.2)

        # Assert
        assert pytest.approx(system.efficiency, 0.01) == 0.6
        assert system.damaged is False

    def test_ship_system_damage_decreases_efficiency(self):
        """Test that damage decreases system efficiency."""

        # Arrange
        class TestSystem(ShipSystem):
            def update(self, dt: float) -> None:
                pass

        system = TestSystem("Test System", 1.0)

        # Act
        system.damage(0.3)

        # Assert
        assert system.efficiency == 0.7

    def test_ship_system_damage_sets_damaged_flag(self):
        """Test that damage below 50% sets damaged flag."""

        # Arrange
        class TestSystem(ShipSystem):
            def update(self, dt: float) -> None:
                pass

        system = TestSystem("Test System", 1.0)

        # Act
        system.damage(0.6)

        # Assert
        assert system.efficiency == 0.4
        assert system.damaged is True

    def test_ship_system_severe_damage_deactivates_system(self):
        """Test that damage to 0% deactivates the system."""

        # Arrange
        class TestSystem(ShipSystem):
            def update(self, dt: float) -> None:
                pass

        system = TestSystem("Test System", 1.0)

        # Act
        system.damage(1.0)

        # Assert
        assert system.efficiency == 0.0
        assert system.active is False


class TestWeaponSystems:
    """Test WeaponSystems component."""

    def test_weapon_systems_initialization(self):
        """Test weapon systems default configuration."""
        # Act
        weapons = WeaponSystems()

        # Assert
        assert weapons.name == "Weapons"
        assert weapons.phaser_arrays == 4
        assert weapons.torpedo_tubes == 2
        assert weapons.torpedo_count == 10
        assert weapons.phaser_range == 5
        assert weapons.torpedo_range == 8

    def test_can_target_within_range(self):
        """Test targeting validation for target within range."""
        # Arrange
        weapons = WeaponSystems()
        ship_pos = GridPosition(5, 5, 0)
        target_pos = GridPosition(7, 7, 0)

        # Act
        result = weapons.can_target(target_pos, ship_pos, 0)

        # Assert
        assert result is True

    def test_can_target_outside_range(self):
        """Test targeting validation for target outside range."""
        # Arrange
        weapons = WeaponSystems()
        ship_pos = GridPosition(5, 5, 0)
        target_pos = GridPosition(15, 15, 0)

        # Act
        result = weapons.can_target(target_pos, ship_pos, 0)

        # Assert
        assert result is False

    def test_calculate_damage_phaser(self):
        """Test phaser damage calculation."""
        # Arrange
        weapons = WeaponSystems()
        target = Mock()

        # Act
        damage = weapons.calculate_damage("phaser", target)

        # Assert
        assert damage == 10

    def test_calculate_damage_torpedo(self):
        """Test torpedo damage calculation."""
        # Arrange
        weapons = WeaponSystems()
        target = Mock()

        # Act
        damage = weapons.calculate_damage("torpedo", target)

        # Assert
        assert damage == 25

    def test_calculate_damage_with_reduced_efficiency(self):
        """Test damage calculation with damaged weapons."""
        # Arrange
        weapons = WeaponSystems()
        weapons.efficiency = 0.5
        target = Mock()

        # Act
        damage = weapons.calculate_damage("phaser", target)

        # Assert
        assert damage == 5

    def test_fire_weapon_phaser_success(self):
        """Test successful phaser firing."""
        # Arrange
        weapons = WeaponSystems()

        # Act
        result = weapons.fire_weapon("phaser")

        # Assert
        assert result is True

    def test_fire_weapon_torpedo_success(self):
        """Test successful torpedo firing."""
        # Arrange
        weapons = WeaponSystems()
        initial_count = weapons.torpedo_count

        # Act
        result = weapons.fire_weapon("torpedo")

        # Assert
        assert result is True
        assert weapons.torpedo_count == initial_count - 1

    def test_fire_weapon_torpedo_depleted(self):
        """Test firing torpedo when depleted."""
        # Arrange
        weapons = WeaponSystems()
        weapons.torpedo_count = 0

        # Act
        result = weapons.fire_weapon("torpedo")

        # Assert
        assert result is False

    def test_fire_weapon_inactive_system(self):
        """Test firing weapon with inactive system."""
        # Arrange
        weapons = WeaponSystems()
        weapons.active = False

        # Act
        result = weapons.fire_weapon("phaser")

        # Assert
        assert result is False

    def test_weapon_update(self):
        """Test weapon systems update."""
        # Arrange
        weapons = WeaponSystems()

        # Act & Assert - should not raise
        weapons.update(0.016)


class TestShieldSystems:
    """Test ShieldSystems component."""

    def test_shield_systems_initialization(self):
        """Test shield systems default configuration."""
        # Act
        shields = ShieldSystems()

        # Assert
        assert shields.name == "Shields"
        assert shields.shield_strength == 100.0
        assert shields.max_shield_strength == 100.0
        assert shields.recharge_rate == 5.0

    def test_absorb_damage_energy_type(self):
        """Test shield absorption of energy damage."""
        # Arrange
        shields = ShieldSystems()
        incoming_damage = 50

        # Act
        remaining_damage = shields.absorb_damage(incoming_damage, "energy")

        # Assert
        assert remaining_damage == 10  # 50 - (50 * 0.8)
        assert shields.shield_strength == 60.0  # 100 - 40

    def test_absorb_damage_kinetic_type(self):
        """Test shield absorption of kinetic damage."""
        # Arrange
        shields = ShieldSystems()
        incoming_damage = 50

        # Act
        remaining_damage = shields.absorb_damage(incoming_damage, "kinetic")

        # Assert
        assert remaining_damage == 20  # 50 - (50 * 0.6)
        assert shields.shield_strength == 70.0  # 100 - 30

    def test_absorb_damage_when_shields_depleted(self):
        """Test damage absorption with depleted shields."""
        # Arrange
        shields = ShieldSystems()
        shields.shield_strength = 0.0
        incoming_damage = 50

        # Act
        remaining_damage = shields.absorb_damage(incoming_damage, "energy")

        # Assert
        assert remaining_damage == 50
        assert shields.shield_strength == 0.0

    def test_absorb_damage_when_shields_inactive(self):
        """Test damage absorption with inactive shields."""
        # Arrange
        shields = ShieldSystems()
        shields.active = False
        incoming_damage = 50

        # Act
        remaining_damage = shields.absorb_damage(incoming_damage, "energy")

        # Assert
        assert remaining_damage == 50

    def test_recharge_shields_normal(self):
        """Test manual shield recharge."""
        # Arrange
        shields = ShieldSystems()
        shields.shield_strength = 50.0

        # Act
        shields.recharge_shields(25.0)

        # Assert
        assert shields.shield_strength == 75.0

    def test_recharge_shields_caps_at_max(self):
        """Test shield recharge doesn't exceed maximum."""
        # Arrange
        shields = ShieldSystems()
        shields.shield_strength = 90.0

        # Act
        shields.recharge_shields(50.0)

        # Assert
        assert shields.shield_strength == 100.0

    def test_shield_update_recharges_over_time(self):
        """Test shield automatic recharge during update."""
        # Arrange
        shields = ShieldSystems()
        shields.shield_strength = 50.0
        dt = 1.0  # 1 second

        # Act
        shields.update(dt)

        # Assert
        assert shields.shield_strength == 55.0  # 50 + (5.0 * 1.0)

    def test_shield_update_with_reduced_efficiency(self):
        """Test shield recharge with damaged system."""
        # Arrange
        shields = ShieldSystems()
        shields.shield_strength = 50.0
        shields.efficiency = 0.5
        dt = 1.0

        # Act
        shields.update(dt)

        # Assert
        assert shields.shield_strength == 52.5  # 50 + (5.0 * 1.0 * 0.5)


class TestEngineSystems:
    """Test EngineSystems component."""

    def test_engine_systems_initialization(self):
        """Test engine systems default configuration."""
        # Act
        engines = EngineSystems()

        # Assert
        assert engines.name == "Engines"
        assert engines.impulse_power == 1.0
        assert engines.warp_capable is True
        assert engines.fuel == 100.0
        assert engines.max_fuel == 100.0

    def test_calculate_movement_cost(self):
        """Test fuel cost calculation for movement."""
        # Arrange
        engines = EngineSystems()
        distance = 10

        # Act
        cost = engines.calculate_movement_cost(distance)

        # Assert
        assert cost == 5.0  # 10 * 0.5 / 1.0

    def test_calculate_movement_cost_damaged_engines(self):
        """Test fuel cost with damaged engines."""
        # Arrange
        engines = EngineSystems()
        engines.efficiency = 0.5
        distance = 10

        # Act
        cost = engines.calculate_movement_cost(distance)

        # Assert
        assert cost == 10.0  # 10 * 0.5 / 0.5

    def test_set_impulse_power_valid(self):
        """Test setting impulse power to valid level."""
        # Arrange
        engines = EngineSystems()

        # Act
        engines.set_impulse_power(0.75)

        # Assert
        assert engines.impulse_power == 0.75

    def test_set_impulse_power_caps_at_one(self):
        """Test impulse power caps at maximum."""
        # Arrange
        engines = EngineSystems()

        # Act
        engines.set_impulse_power(1.5)

        # Assert
        assert engines.impulse_power == 1.0

    def test_set_impulse_power_floors_at_zero(self):
        """Test impulse power floors at minimum."""
        # Arrange
        engines = EngineSystems()

        # Act
        engines.set_impulse_power(-0.5)

        # Assert
        assert engines.impulse_power == 0.0

    def test_engine_update(self):
        """Test engine systems update."""
        # Arrange
        engines = EngineSystems()

        # Act & Assert - should not raise
        engines.update(0.016)


class TestSensorSystems:
    """Test SensorSystems component."""

    def test_sensor_systems_initialization(self):
        """Test sensor systems default configuration."""
        # Act
        sensors = SensorSystems()

        # Assert
        assert sensors.name == "Sensors"
        assert sensors.short_range == 3
        assert sensors.long_range == 10
        assert sensors.passive_mode is True

    def test_scan_range_passive_mode(self):
        """Test sensor range in passive mode."""
        # Arrange
        sensors = SensorSystems()

        # Act
        range_value = sensors.scan_range()

        # Assert
        assert range_value == 3

    def test_scan_range_active_mode(self):
        """Test sensor range in active mode."""
        # Arrange
        sensors = SensorSystems()
        sensors.set_passive_mode(False)

        # Act
        range_value = sensors.scan_range()

        # Assert
        assert range_value == 10

    def test_scan_range_with_reduced_efficiency(self):
        """Test sensor range with damaged sensors."""
        # Arrange
        sensors = SensorSystems()
        sensors.efficiency = 0.5

        # Act
        range_value = sensors.scan_range()

        # Assert
        assert range_value == 1  # int(3 * 0.5)

    def test_set_passive_mode_true(self):
        """Test enabling passive sensor mode."""
        # Arrange
        sensors = SensorSystems()
        sensors.passive_mode = False

        # Act
        sensors.set_passive_mode(True)

        # Assert
        assert sensors.passive_mode is True

    def test_set_passive_mode_false(self):
        """Test enabling active sensor mode."""
        # Arrange
        sensors = SensorSystems()

        # Act
        sensors.set_passive_mode(False)

        # Assert
        assert sensors.passive_mode is False

    def test_detect_targets_within_range(self):
        """Test detecting targets within sensor range."""
        # Arrange
        sensors = SensorSystems()
        ship_pos = GridPosition(5, 5, 0)

        target1 = Mock()
        target1.position = GridPosition(6, 6, 0)
        target2 = Mock()
        target2.position = GridPosition(7, 7, 0)

        targets = [target1, target2]

        # Act
        detected = sensors.detect_targets(ship_pos, targets)

        # Assert
        assert len(detected) == 2
        assert target1 in detected
        assert target2 in detected

    def test_detect_targets_outside_range(self):
        """Test that targets outside range are not detected."""
        # Arrange
        sensors = SensorSystems()
        ship_pos = GridPosition(5, 5, 0)

        target = Mock()
        target.position = GridPosition(20, 20, 0)

        # Act
        detected = sensors.detect_targets(ship_pos, [target])

        # Assert
        assert len(detected) == 0

    def test_detect_targets_mixed_range(self):
        """Test detecting mix of in-range and out-of-range targets."""
        # Arrange
        sensors = SensorSystems()
        ship_pos = GridPosition(5, 5, 0)

        near_target = Mock()
        near_target.position = GridPosition(6, 6, 0)
        far_target = Mock()
        far_target.position = GridPosition(20, 20, 0)

        targets = [near_target, far_target]

        # Act
        detected = sensors.detect_targets(ship_pos, targets)

        # Assert
        assert len(detected) == 1
        assert near_target in detected
        assert far_target not in detected

    def test_sensor_update(self):
        """Test sensor systems update."""
        # Arrange
        sensors = SensorSystems()

        # Act & Assert - should not raise
        sensors.update(0.016)


class TestLifeSupportSystems:
    """Test LifeSupportSystems component."""

    def test_life_support_initialization(self):
        """Test life support systems default configuration."""
        # Act
        life_support = LifeSupportSystems()

        # Assert
        assert life_support.name == "Life Support"
        assert life_support.atmosphere_quality == 100.0
        assert life_support.temperature == 20.0
        assert life_support.gravity == 1.0

    def test_maintain_environment_when_active(self):
        """Test environment maintenance with active system."""
        # Arrange
        life_support = LifeSupportSystems()
        life_support.atmosphere_quality = 80.0

        # Act
        life_support.maintain_environment()

        # Assert
        assert life_support.atmosphere_quality == 100.0

    def test_maintain_environment_when_inactive(self):
        """Test environment degradation when system inactive."""
        # Arrange
        life_support = LifeSupportSystems()
        life_support.active = False
        life_support.atmosphere_quality = 100.0

        # Act
        life_support.maintain_environment()

        # Assert
        assert life_support.atmosphere_quality == 99.0

    def test_emergency_mode_activation(self):
        """Test emergency life support mode."""
        # Arrange
        life_support = LifeSupportSystems()

        # Act
        life_support.emergency_mode()

        # Assert
        assert life_support.atmosphere_quality == 50.0
        assert life_support.temperature == 15.0
        assert life_support.gravity == 0.8

    def test_emergency_mode_requires_minimum_efficiency(self):
        """Test emergency mode when efficiency too low."""
        # Arrange
        life_support = LifeSupportSystems()
        life_support.efficiency = 0.2
        original_atmosphere = life_support.atmosphere_quality

        # Act
        life_support.emergency_mode()

        # Assert - emergency mode should not activate
        assert life_support.atmosphere_quality == original_atmosphere

    def test_life_support_update(self):
        """Test life support systems update."""
        # Arrange
        life_support = LifeSupportSystems()
        life_support.atmosphere_quality = 50.0

        # Act
        life_support.update(0.016)

        # Assert - should maintain environment
        assert life_support.atmosphere_quality == 100.0
