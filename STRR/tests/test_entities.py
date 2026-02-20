#!/usr/bin/env python3
"""
Star Trek Retro Remake - Entity Tests

Description:
    Unit tests for game entities including starships and base objects.

Author: Star Trek Retro Remake Development Team
Date Created: 10-29-2025
Date Changed: 01-27-2025
License: MIT
"""

from typing import Final

import pytest
from src.game.entities.base import GameObject, GridPosition
from src.game.entities.starship import SpaceStation, Starship

pytestmark = pytest.mark.unit

__version__: Final[str] = "0.0.1"


class TestGridPosition:
    """Test cases for GridPosition class."""

    def test_grid_position_creation(self):
        """Test that GridPosition creates correctly with default z-level."""
        # Arrange & Act
        position = GridPosition(5, 10)

        # Assert
        assert position.x == 5
        assert position.y == 10
        assert position.z == 0

    def test_grid_position_creation_with_z(self):
        """Test that GridPosition creates correctly with specified z-level."""
        # Arrange & Act
        position = GridPosition(3, 7, 2)

        # Assert
        assert position.x == 3
        assert position.y == 7
        assert position.z == 2

    def test_distance_calculation_2d(self):
        """Test distance calculation between two 2D positions."""
        # Arrange
        pos1 = GridPosition(0, 0)
        pos2 = GridPosition(3, 4)

        # Act
        distance = pos1.distance_to(pos2)

        # Assert
        assert distance == 5.0  # 3-4-5 triangle

    def test_distance_calculation_3d(self):
        """Test distance calculation between two 3D positions."""
        # Arrange
        pos1 = GridPosition(0, 0, 0)
        pos2 = GridPosition(1, 1, 1)

        # Act
        distance = pos1.distance_to(pos2)

        # Assert
        expected = (1**2 + 1**2 + 1**2) ** 0.5
        assert abs(distance - expected) < 0.001


class TestGameObject:
    """Test cases for GameObject base class."""

    def test_game_object_creation(self, grid_position):
        """Test that GameObject creates with required attributes."""
        # Arrange & Act
        obj = GameObject(grid_position, "Test Object")

        # Assert
        assert obj.position == grid_position
        assert obj.name == "Test Object"
        assert obj.active is True
        assert obj.faction is None
        assert obj.id is not None
        assert len(obj.id) > 0

    def test_game_object_unique_ids(self, grid_position):
        """Test that each GameObject gets a unique ID."""
        # Arrange & Act
        obj1 = GameObject(grid_position, "Object 1")
        obj2 = GameObject(grid_position, "Object 2")

        # Assert
        assert obj1.id != obj2.id

    def test_game_object_destroy(self, grid_position):
        """Test that destroy() marks object as inactive."""
        # Arrange
        obj = GameObject(grid_position, "Test Object")
        assert obj.active is True

        # Act
        obj.destroy()

        # Assert
        assert obj.active is False


class TestStarship:
    """Test cases for Starship class."""

    def test_starship_creation(self, grid_position):
        """Test that Starship creates with proper systems."""
        # Arrange & Act
        ship = Starship(grid_position, "Constitution", "Enterprise", "Federation")

        # Assert
        assert ship.ship_class == "Constitution"
        assert ship.name == "Enterprise"
        assert ship.faction == "Federation"
        assert ship.hull_integrity == 100.0
        assert ship.orientation == 0
        assert (
            len(ship.systems) == 7
        )  # All ship systems (weapons, shields, engines, sensors, life_support, resources, crew)
        assert ship.color == (60, 120, 200)  # Federation blue
        assert ship.size == 16

    def test_starship_get_system(self, test_starship):
        """Test that get_system returns correct systems."""
        # Arrange & Act
        weapons = test_starship.get_system("weapons")
        shields = test_starship.get_system("shields")
        nonexistent = test_starship.get_system("nonexistent")

        # Assert
        assert weapons is not None
        assert shields is not None
        assert nonexistent is None

    def test_starship_take_damage_with_shields(self, test_starship):
        """Test damage application with shields active."""
        # Arrange
        initial_hull = test_starship.hull_integrity
        shields = test_starship.get_system("shields")
        initial_shield_strength = shields.total_shield_strength

        # Act
        test_starship.take_damage(20, "energy")

        # Assert
        # Shields should absorb most energy damage
        assert shields.total_shield_strength < initial_shield_strength
        assert (
            test_starship.hull_integrity == initial_hull
            or test_starship.hull_integrity > initial_hull - 20
        )

    def test_starship_take_damage_no_shields(self, test_starship):
        """Test damage application with shields down."""
        # Arrange
        initial_hull = test_starship.hull_integrity
        shields = test_starship.get_system("shields")
        shields.active = False

        # Act
        test_starship.take_damage(25)

        # Assert
        assert test_starship.hull_integrity == initial_hull - 25

    def test_starship_destruction(self, test_starship):
        """Test that ship is destroyed when hull reaches zero."""
        # Arrange
        test_starship.hull_integrity = 10
        # Disable shields so all damage goes to hull
        shields = test_starship.get_system("shields")
        shields.active = False

        # Act
        test_starship.take_damage(15)

        # Assert
        assert test_starship.hull_integrity == 0
        assert test_starship.active is False

    def test_starship_repair_system(self, test_starship):
        """Test system repair functionality."""
        # Arrange
        weapons = test_starship.get_system("weapons")
        weapons.damage(0.5)  # Damage weapons
        initial_efficiency = weapons.efficiency

        # Act
        result = test_starship.repair_system("weapons", 0.3)

        # Assert
        assert result is True
        assert weapons.efficiency > initial_efficiency

    def test_starship_repair_nonexistent_system(self, test_starship):
        """Test repair of nonexistent system returns False."""
        # Arrange & Act
        result = test_starship.repair_system("nonexistent", 0.5)

        # Assert
        assert result is False

    def test_starship_orientation_radians(self, test_starship):
        """Test orientation conversion to radians."""
        # Arrange
        import math

        test_starship.orientation = 90  # East

        # Act
        radians = test_starship.get_orientation_radians()

        # Assert
        assert abs(radians - math.pi / 2) < 0.001  # Should be π/2 radians

    def test_starship_faction_colors(self, grid_position):
        """Test that different factions have different colors."""
        # Arrange & Act
        fed_ship = Starship(grid_position, "Constitution", "Enterprise", "Federation")
        klingon_ship = Starship(grid_position, "Bird-of-Prey", "IKS Korinar", "Klingon")
        romulan_ship = Starship(grid_position, "Warbird", "IRW Valdore", "Romulan")

        # Assert
        assert fed_ship.color == (60, 120, 200)  # Blue
        assert klingon_ship.color == (180, 40, 40)  # Red
        assert romulan_ship.color == (60, 180, 80)  # Green
        assert fed_ship.color != klingon_ship.color != romulan_ship.color


class TestSpaceStation:
    """Test cases for SpaceStation class."""

    def test_space_station_creation(self, grid_position):
        """Test that SpaceStation creates correctly."""
        # Arrange & Act
        station = SpaceStation(grid_position, "starbase", "Deep Space 9")

        # Assert
        assert station.station_type == "starbase"
        assert station.name == "Deep Space 9"
        assert station.services == []
        assert station.docked_ships == []

    def test_space_station_docking(self, grid_position):
        """Test ship docking at station."""
        # Arrange
        station = SpaceStation(grid_position, "starbase", "Test Station")
        ship = Starship(grid_position, "Constitution", "Test Ship")

        # Act
        result = station.dock_ship(ship)

        # Assert
        assert result is True
        assert ship in station.docked_ships

    def test_space_station_docking_too_far(self, grid_position):
        """Test that ships too far away cannot dock."""
        # Arrange
        station = SpaceStation(grid_position, "starbase", "Test Station")
        far_position = GridPosition(grid_position.x + 5, grid_position.y + 5)
        ship = Starship(far_position, "Constitution", "Test Ship")

        # Act
        result = station.dock_ship(ship)

        # Assert
        assert result is False
        assert ship not in station.docked_ships

    def test_space_station_undocking(self, grid_position):
        """Test ship undocking from station."""
        # Arrange
        station = SpaceStation(grid_position, "starbase", "Test Station")
        ship = Starship(grid_position, "Constitution", "Test Ship")
        station.dock_ship(ship)

        # Act
        result = station.undock_ship(ship)

        # Assert
        assert result is True
        assert ship not in station.docked_ships
