#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Star Trek Retro Remake - Galaxy Map

Description:
    Galaxy map implementation for large-scale navigation between sectors.

Author: Star Trek Retro Remake Development Team
Email: development@star-trek-retro-remake.org
GitHub: https://github.com/L3DigitalNet/Star-Trek-Retro-Remake
Date Created: 10-29-2025
Date Changed: 10-30-2025
License: MIT

Features:
    - Galaxy-scale navigation system
    - Sector management and organization
    - Faction territory mapping
    - Strategic navigation interface

Requirements:
    - Linux environment
    - Python 3.14+ for latest language features

Classes:
    - GalaxyMap: Galaxy-wide navigation and sector management

Functions:
    - None
"""

from typing import Final, Optional, Dict, Tuple

from .sector import SectorMap

__version__: Final[str] = "0.0.1"


class GalaxyMap:
    """
    Galaxy-wide navigation and sector management.

    Manages the collection of sector maps and provides
    navigation capabilities between different regions of space.

    Attributes:
        sectors: Dictionary of sector maps by coordinates
        galaxy_size: Size of the galaxy grid
        current_coordinates: Current galaxy position

    Public methods:
        get_sector: Retrieve a sector map by coordinates
        create_sector: Create a new sector at coordinates
        get_neighboring_sectors: Get adjacent sectors
        is_valid_coordinates: Check if coordinates are within bounds

    Private methods:
        _initialize_default_sectors: Create starting sectors
    """

    def __init__(self, galaxy_size: Tuple[int, int] = (10, 10)):
        """
        Initialize the galaxy map.

        Args:
            galaxy_size: Size of the galaxy grid as (width, height)
        """
        self.galaxy_size = galaxy_size
        self.sectors: Dict[Tuple[int, int], SectorMap] = {}
        self.current_coordinates: Tuple[int, int] = (0, 0)

        # Initialize starting sectors
        self._initialize_default_sectors()

    def get_sector(self, x: int, y: int) -> Optional[SectorMap]:
        """
        Retrieve a sector map by coordinates.

        Args:
            x: Galaxy x-coordinate
            y: Galaxy y-coordinate

        Returns:
            SectorMap at coordinates or None if not found
        """
        coordinates = (x, y)
        if coordinates not in self.sectors:
            # Create sector on demand
            self.sectors[coordinates] = SectorMap(coordinates)

        return self.sectors.get(coordinates)

    def create_sector(self, x: int, y: int, sector_type: str = "standard") -> SectorMap:
        """
        Create a new sector at coordinates.

        Args:
            x: Galaxy x-coordinate
            y: Galaxy y-coordinate
            sector_type: Type of sector to create

        Returns:
            Newly created sector map
        """
        coordinates = (x, y)
        sector = SectorMap(coordinates, sector_type)
        self.sectors[coordinates] = sector
        return sector

    def get_neighboring_sectors(self, x: int, y: int) -> list[SectorMap]:
        """
        Get adjacent sectors to the specified coordinates.

        Args:
            x: Galaxy x-coordinate
            y: Galaxy y-coordinate

        Returns:
            List of neighboring sector maps
        """
        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue

                neighbor_x, neighbor_y = x + dx, y + dy
                if self.is_valid_coordinates(neighbor_x, neighbor_y):
                    sector = self.get_sector(neighbor_x, neighbor_y)
                    if sector:
                        neighbors.append(sector)

        return neighbors

    def is_valid_coordinates(self, x: int, y: int) -> bool:
        """
        Check if coordinates are within galaxy bounds.

        Args:
            x: Galaxy x-coordinate
            y: Galaxy y-coordinate

        Returns:
            True if coordinates are valid, False otherwise
        """
        return (0 <= x < self.galaxy_size[0] and
                0 <= y < self.galaxy_size[1])

    def _initialize_default_sectors(self) -> None:
        """Create starting sectors for the game."""
        # Create a few initial sectors
        self.create_sector(0, 0, "federation")
        self.create_sector(1, 0, "neutral")
        self.create_sector(0, 1, "neutral")