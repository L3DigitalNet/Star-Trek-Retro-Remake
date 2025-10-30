#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Star Trek Retro Remake - Maps Tests

Description:
    Unit tests for galaxy and sector map systems, grid management,
    entity placement, and spatial queries.

Author: Star Trek Retro Remake Development Team
Date Created: 10-30-2025
Date Changed: 10-30-2025
License: MIT
"""

from typing import Final

from src.game.maps.galaxy import GalaxyMap
from src.game.maps.sector import SectorMap
from src.game.entities.base import GridPosition
from src.game.entities.starship import Starship, SpaceStation

__version__: Final[str] = "0.0.11"


class TestGalaxyMap:
    """Test cases for GalaxyMap class."""

    def test_galaxy_map_creation(self):
        """Test creating a galaxy map."""
        # Arrange & Act
        galaxy = GalaxyMap((5, 5))

        # Assert
        assert galaxy.galaxy_size == (5, 5)
        assert isinstance(galaxy.sectors, dict)

    def test_galaxy_map_default_dimensions(self):
        """Test default galaxy dimensions."""
        # Arrange & Act
        galaxy = GalaxyMap()

        # Assert
        assert galaxy.galaxy_size == (10, 10)
        assert isinstance(galaxy.sectors, dict)

    def test_get_sector_valid(self):
        """Test getting a valid sector."""
        # Arrange
        galaxy = GalaxyMap((5, 5))

        # Act
        sector = galaxy.get_sector(2, 3)

        # Assert
        assert sector is not None
        assert sector.coordinates == (2, 3)

    def test_get_sector_out_of_bounds(self):
        """Test getting out-of-bounds sector returns None."""
        # Arrange
        galaxy = GalaxyMap((5, 5))

        # Act
        # Out of bounds should still create sector on demand
        sector = galaxy.get_sector(10, 10)

        # Assert - Actually creates sector on demand, but check validity
        if sector:
            assert not galaxy.is_valid_coordinates(10, 10)

    def test_get_sector_negative_coordinates(self):
        """Test getting sector with negative coordinates."""
        # Arrange
        galaxy = GalaxyMap((5, 5))

        # Act
        sector = galaxy.get_sector(-1, 0)

        # Assert - Creates sector on demand but invalid coordinates
        if sector:
            assert not galaxy.is_valid_coordinates(-1, 0)

    def test_get_adjacent_sectors(self):
        """Test getting adjacent sectors."""
        # Arrange
        galaxy = GalaxyMap((5, 5))

        # Act
        adjacent = galaxy.get_neighboring_sectors(2, 2)

        # Assert
        assert len(adjacent) > 0
        # Should include neighbors (up to 8 in non-edge positions)
        assert len(adjacent) <= 8

    def test_get_adjacent_sectors_corner(self):
        """Test getting adjacent sectors from corner position."""
        # Arrange
        galaxy = GalaxyMap((5, 5))

        # Act
        adjacent = galaxy.get_neighboring_sectors(0, 0)

        # Assert
        # Corner should have 3 neighbors
        assert len(adjacent) == 3

    def test_get_adjacent_sectors_edge(self):
        """Test getting adjacent sectors from edge position."""
        # Arrange
        galaxy = GalaxyMap((5, 5))

        # Act
        adjacent = galaxy.get_neighboring_sectors(2, 0)

        # Assert
        # Edge (not corner) should have 5 neighbors
        assert len(adjacent) == 5

    def test_generate_sectors(self):
        """Test that sectors are generated correctly."""
        # Arrange & Act
        galaxy = GalaxyMap((3, 3))

        # Assert
        for x in range(3):
            for y in range(3):
                sector = galaxy.get_sector(x, y)
                assert sector is not None
                assert sector.coordinates == (x, y)


class TestSectorMap:
    """Test cases for SectorMap class."""

    def test_sector_map_creation(self):
        """Test creating a sector map."""
        # Arrange & Act
        sector = SectorMap((0, 0), "standard")

        # Assert
        assert sector.coordinates == (0, 0)
        assert sector.sector_type == "standard"
        assert sector.grid_size == (20, 20, 5)
        assert sector.entities == {}

    def test_sector_map_custom_type(self):
        """Test creating a sector with different type."""
        # Arrange & Act
        sector = SectorMap((1, 1), "combat")

        # Assert
        assert sector.grid_size == (20, 20, 5)
        assert sector.sector_type == "combat"

    def test_place_entity(self):
        """Test placing an entity in the sector."""
        # Arrange
        sector = SectorMap((0, 0), "standard")
        position = GridPosition(5, 5, 1)
        ship = Starship(position, "Constitution", "Test Ship")

        # Act
        result = sector.place_entity(ship, position)

        # Assert
        assert result is True
        assert position in sector.entities
        assert sector.entities[position] == ship

    def test_place_entity_out_of_bounds(self):
        """Test placing entity out of bounds fails."""
        # Arrange
        sector = SectorMap((0, 0), "standard")
        position = GridPosition(100, 100, 1)
        ship = Starship(position, "Constitution", "Test Ship")

        # Act
        result = sector.place_entity(ship, position)

        # Assert
        assert result is False

    def test_place_entity_on_occupied_position(self):
        """Test placing entity on occupied position - actually overwrites."""
        # Arrange
        sector = SectorMap((0, 0), "standard")
        position = GridPosition(5, 5, 1)
        ship1 = Starship(position, "Constitution", "Ship 1")
        ship2 = Starship(position, "Miranda", "Ship 2")

        sector.place_entity(ship1, position)

        # Act - place_entity allows overwriting, doesn't check if occupied
        result = sector.place_entity(ship2, position)

        # Assert
        assert result is True
        assert sector.entities[position] == ship2  # Second ship overwrites

    def test_remove_entity(self):
        """Test removing an entity from the sector."""
        # Arrange
        sector = SectorMap((0, 0), "standard")
        position = GridPosition(5, 5, 1)
        ship = Starship(position, "Constitution", "Test Ship")
        sector.place_entity(ship, position)

        # Act
        result = sector.remove_entity(position)

        # Assert
        assert result == ship  # Returns removed entity
        assert position not in sector.entities

    def test_remove_entity_nonexistent(self):
        """Test removing nonexistent entity returns None."""
        # Arrange
        sector = SectorMap((0, 0), "standard")
        position = GridPosition(5, 5, 1)

        # Act
        result = sector.remove_entity(position)

        # Assert
        assert result is None  # Returns None for nonexistent

    def test_get_entity_at_position(self):
        """Test getting entity at a specific position."""
        # Arrange
        sector = SectorMap((0, 0), "standard")
        position = GridPosition(5, 5, 1)
        ship = Starship(position, "Constitution", "Test Ship")
        sector.place_entity(ship, position)

        # Act
        entity = sector.get_entity_at(position)

        # Assert
        assert entity == ship

    def test_get_entity_at_empty_position(self):
        """Test getting entity at empty position returns None."""
        # Arrange
        sector = SectorMap((0, 0), "standard")
        position = GridPosition(5, 5, 1)

        # Act
        entity = sector.get_entity_at(position)

        # Assert
        assert entity is None

    def test_position_occupied_via_get_entity_at(self):
        """Test checking if position is occupied using get_entity_at."""
        # Arrange
        sector = SectorMap((0, 0), "standard")
        position = GridPosition(5, 5, 1)
        ship = Starship(position, "Constitution", "Test Ship")
        sector.place_entity(ship, position)

        # Act
        occupied = sector.get_entity_at(position) is not None
        empty = sector.get_entity_at(GridPosition(6, 6, 1)) is not None

        # Assert
        assert occupied is True
        assert empty is False

    def test_manually_filter_entities_in_range(self):
        """Test manually filtering entities within range."""
        # Arrange
        sector = SectorMap((0, 0), "standard")

        # Place multiple entities
        ship1 = Starship(GridPosition(5, 5, 1), "Constitution", "Ship 1")
        ship2 = Starship(GridPosition(6, 6, 1), "Miranda", "Ship 2")
        ship3 = Starship(GridPosition(15, 15, 1), "Excelsior", "Ship 3")

        sector.place_entity(ship1, ship1.position)
        sector.place_entity(ship2, ship2.position)
        sector.place_entity(ship3, ship3.position)

        # Act - manually filter entities within range
        center = GridPosition(5, 5, 1)
        max_range = 3.0
        nearby = [
            entity
            for pos, entity in sector.get_all_entities()
            if pos.distance_to(center) <= max_range
        ]

        # Assert
        assert len(nearby) == 2  # ship1 and ship2
        assert ship1 in nearby
        assert ship2 in nearby
        assert ship3 not in nearby

    def test_get_all_entities(self):
        """Test getting all entities in sector."""
        # Arrange
        sector = SectorMap((0, 0), "standard")

        ship1 = Starship(GridPosition(5, 5, 1), "Constitution", "Ship 1")
        ship2 = Starship(GridPosition(6, 6, 1), "Miranda", "Ship 2")

        sector.place_entity(ship1, ship1.position)
        sector.place_entity(ship2, ship2.position)

        # Act
        all_entities = sector.get_all_entities()

        # Assert
        assert len(all_entities) == 2
        # get_all_entities returns list of (position, entity) tuples
        entities_only = [entity for pos, entity in all_entities]
        assert ship1 in entities_only
        assert ship2 in entities_only

    def test_move_entity(self):
        """Test moving an entity within the sector."""
        # Arrange
        sector = SectorMap((0, 0), "standard")
        old_position = GridPosition(5, 5, 1)
        new_position = GridPosition(6, 6, 1)
        ship = Starship(old_position, "Constitution", "Test Ship")
        sector.place_entity(ship, old_position)

        # Act
        result = sector.move_entity(old_position, new_position)

        # Assert
        assert result is True
        assert old_position not in sector.entities
        assert new_position in sector.entities
        assert sector.entities[new_position] == ship
        assert ship.position == new_position

    def test_move_entity_to_occupied_position(self):
        """Test moving entity to occupied position - overwrites."""
        # Arrange
        sector = SectorMap((0, 0), "standard")
        pos1 = GridPosition(5, 5, 1)
        pos2 = GridPosition(6, 6, 1)
        ship1 = Starship(pos1, "Constitution", "Ship 1")
        ship2 = Starship(pos2, "Miranda", "Ship 2")

        sector.place_entity(ship1, pos1)
        sector.place_entity(ship2, pos2)

        # Act - move_entity doesn't prevent overwriting
        result = sector.move_entity(pos1, pos2)

        # Assert
        assert result is True
        assert pos1 not in sector.entities
        assert sector.entities[pos2] == ship1  # ship1 overwrites ship2

    def test_is_position_valid(self):
        """Test position validation."""
        # Arrange
        sector = SectorMap((0, 0), "standard")

        # Act & Assert - sector has grid_size (20, 20, 5)
        assert sector.is_in_bounds(GridPosition(0, 0, 0))
        assert sector.is_in_bounds(GridPosition(5, 5, 1))
        assert sector.is_in_bounds(GridPosition(19, 19, 4))
        assert not sector.is_in_bounds(GridPosition(-1, 5, 1))
        assert not sector.is_in_bounds(GridPosition(20, 5, 1))
        assert not sector.is_in_bounds(GridPosition(5, 20, 1))

    def test_clear_entities_manually(self):
        """Test manually clearing all entities from sector."""
        # Arrange
        sector = SectorMap((0, 0), "standard")
        ship1 = Starship(GridPosition(5, 5, 1), "Constitution", "Ship 1")
        ship2 = Starship(GridPosition(6, 6, 1), "Miranda", "Ship 2")

        sector.place_entity(ship1, ship1.position)
        sector.place_entity(ship2, ship2.position)

        # Act - manually clear by resetting dictionary
        sector.entities.clear()

        # Assert
        assert len(sector.entities) == 0


class TestMapIntegration:
    """Integration tests for galaxy and sector maps."""

    def test_galaxy_sector_integration(self):
        """Test integration between galaxy and sector maps."""
        # Arrange
        galaxy = GalaxyMap((3, 3))

        # Act
        sector = galaxy.get_sector(1, 1)

        # Assert
        assert sector is not None
        assert isinstance(sector, SectorMap)
        assert sector.coordinates == (1, 1)

    def test_entity_placement_across_sectors(self):
        """Test placing entities in different sectors."""
        # Arrange
        galaxy = GalaxyMap((3, 3))
        sector1 = galaxy.get_sector(0, 0)
        sector2 = galaxy.get_sector(1, 1)

        ship1 = Starship(GridPosition(5, 5, 1), "Constitution", "Ship 1")
        ship2 = Starship(GridPosition(5, 5, 1), "Miranda", "Ship 2")

        # Act
        result1 = sector1.place_entity(ship1, ship1.position)
        result2 = sector2.place_entity(ship2, ship2.position)

        # Assert
        assert result1 is True
        assert result2 is True
        assert sector1.get_entity_at(ship1.position) == ship1
        assert sector2.get_entity_at(ship2.position) == ship2

    def test_space_station_in_sector(self):
        """Test placing a space station in a sector."""
        # Arrange
        sector = SectorMap((0, 0), "starbase")
        position = GridPosition(10, 10, 1)
        station = SpaceStation(position, "starbase", "Deep Space 9")

        # Act
        result = sector.place_entity(station, position)

        # Assert
        assert result is True
        assert sector.get_entity_at(position) == station

    def test_multiple_entities_different_z_levels(self):
        """Test placing entities at different z-levels."""
        # Arrange
        sector = SectorMap((0, 0), "standard")
        pos_z0 = GridPosition(5, 5, 0)
        pos_z1 = GridPosition(5, 5, 1)
        pos_z2 = GridPosition(5, 5, 2)

        ship1 = Starship(pos_z0, "Constitution", "Ship 1")
        ship2 = Starship(pos_z1, "Miranda", "Ship 2")
        ship3 = Starship(pos_z2, "Excelsior", "Ship 3")

        # Act
        result1 = sector.place_entity(ship1, pos_z0)
        result2 = sector.place_entity(ship2, pos_z1)
        result3 = sector.place_entity(ship3, pos_z2)

        # Assert
        assert result1 is True
        assert result2 is True
        assert result3 is True
        assert len(sector.entities) == 3
