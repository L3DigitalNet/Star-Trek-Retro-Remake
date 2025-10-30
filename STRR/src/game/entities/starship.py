#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Star Trek Retro Remake - Starship Entity

Description:
    Starship entity implementing the Game Object pattern with component
    composition for modular ship systems.

Author: Star Trek Retro Remake Development Team
Email: development@star-trek-retro-remake.org
GitHub: https://github.com/L3DigitalNet/Star-Trek-Retro-Remake
Date Created: 10-29-2025
Date Changed: 10-30-2025
License: MIT

Features:
    - Component composition for ship systems
    - Modular weapon, shield, engine, and sensor systems
    - Crew and resource management
    - Damage and repair mechanics

Requirements:
    - Linux environment
    - Python 3.14+ for latest language features

Classes:
    - Starship: Star Trek starship with modular systems
    - SpaceStation: Space station with docking and services

Functions:
    - None
"""

from typing import Final

from .base import GameObject, GridPosition
from ..components.ship_systems import (
    ShipSystem,
    WeaponSystems,
    ShieldSystems,
    EngineSystems,
    SensorSystems,
    LifeSupportSystems,
)

__version__: Final[str] = "0.0.12"


class Starship(GameObject):
    """
    Star Trek starship with modular systems.

    Implements a starship entity with component-based ship systems,
    crew management, and resource tracking.

    Attributes:
        ship_class: Class designation of the starship
        faction: Faction affiliation
        systems: Dictionary of ship subsystems
        crew: Crew roster management
        resources: Resource management system
        hull_integrity: Current hull integrity percentage
        orientation: Current facing direction (0-359 degrees)
        color: RGB color tuple for rendering
        size: Base size in pixels for rendering

    Public methods:
        get_system: Retrieve a specific ship system
        take_damage: Apply damage to ship systems and hull
        repair_system: Repair a damaged ship system
        get_orientation_radians: Get orientation in radians for rendering

    Private methods:
        _get_faction_color: Determine color based on faction
    """

    def __init__(
        self,
        position: GridPosition,
        ship_class: str,
        name: str = "",
        faction: str = "Federation",
    ):
        """
        Initialize a new starship.

        Args:
            position: Initial 3D grid position
            ship_class: Ship class designation
            name: Ship name
            faction: Faction affiliation (Federation, Klingon, Romulan, etc.)
        """
        super().__init__(position, name)
        self.ship_class = ship_class
        self.faction = faction

        # Initialize ship systems using component composition
        self.systems: dict[str, ShipSystem] = {
            "weapons": WeaponSystems(),
            "shields": ShieldSystems(),
            "engines": EngineSystems(),
            "sensors": SensorSystems(),
            "life_support": LifeSupportSystems(),
        }

        # Ship resources and crew (simplified for initial implementation)
        self.crew: object | None = None  # Will be implemented later
        self.resources: object | None = None  # Will be implemented later

        # Ship state
        self.hull_integrity: float = 100.0
        self.orientation: int = 0  # 0-359 degrees

        # Visual representation attributes
        self.color = self._get_faction_color(faction)
        self.size = 16  # Base size in pixels for rendering

    def _get_faction_color(self, faction: str) -> tuple[int, int, int]:
        """
        Get the display color for a ship based on faction.

        Args:
            faction: Faction name

        Returns:
            RGB color tuple for rendering
        """
        # Faction color mapping
        faction_colors: dict[str, tuple[int, int, int]] = {
            "Federation": (60, 120, 200),  # Blue
            "Klingon": (180, 40, 40),  # Red
            "Romulan": (60, 180, 80),  # Green
            "Gorn": (200, 160, 40),  # Yellow
            "Tholian": (180, 100, 200),  # Purple
            "Orion": (40, 200, 160),  # Cyan
            "Neutral": (140, 140, 140),  # Gray
        }
        return faction_colors.get(faction, (200, 200, 200))  # White default

    def get_system(self, system_name: str) -> ShipSystem | None:
        """
        Get a specific ship system.

        Args:
            system_name: Name of the system to retrieve

        Returns:
            The requested ship system or None if not found
        """
        return self.systems.get(system_name)

    def take_damage(self, amount: int, damage_type: str = "kinetic") -> None:
        """
        Apply damage to ship systems and hull.

        Args:
            amount: Amount of damage to apply
            damage_type: Type of damage (kinetic, energy, etc.)
        """
        # Shield absorption first
        shields = self.get_system("shields")
        if shields and shields.active:
            amount = shields.absorb_damage(amount, damage_type)

        # Apply remaining damage to hull
        if amount > 0:
            self.hull_integrity = max(0, self.hull_integrity - amount)
            if self.hull_integrity <= 0:
                self.destroy()

    def repair_system(self, system_name: str, repair_amount: float) -> bool:
        """
        Repair a damaged ship system.

        Args:
            system_name: Name of the system to repair
            repair_amount: Amount of repair to apply

        Returns:
            True if repair was successful, False otherwise
        """
        system = self.get_system(system_name)
        if system:
            system.repair(repair_amount)
            return True
        return False

    def get_orientation_radians(self) -> float:
        """
        Get ship orientation in radians for rendering.

        Returns:
            Orientation angle in radians (0 to 2π)
        """
        import math

        return math.radians(self.orientation)


class SpaceStation(GameObject):
    """
    Space station with docking and services.

    Represents a space station that can provide services to starships
    such as repairs, resupply, and trading.

    Attributes:
        station_type: Type of space station
        services: List of available services
        docked_ships: List of currently docked ships

    Public methods:
        dock_ship: Dock a ship at the station
        undock_ship: Remove a ship from the station
        provide_service: Provide a service to a docked ship

    Private methods:
        _initialize_services: Set up available services
    """

    def __init__(self, position: GridPosition, station_type: str, name: str = ""):
        """
        Initialize a new space station.

        Args:
            position: Station position in 3D grid
            station_type: Type of station (starbase, outpost, etc.)
            name: Station name
        """
        super().__init__(position, name)
        self.station_type = station_type
        self.services: list[str] = []  # Will be expanded later
        self.docked_ships: list[Starship] = []

    def dock_ship(self, ship: Starship) -> bool:
        """
        Dock a ship at the station.

        Args:
            ship: Starship to dock

        Returns:
            True if docking was successful, False otherwise
        """
        # Check if ship is at station position
        if ship.position.distance_to(self.position) <= 1.0:
            self.docked_ships.append(ship)
            return True
        return False

    def undock_ship(self, ship: Starship) -> bool:
        """
        Remove a ship from the station.

        Args:
            ship: Starship to undock

        Returns:
            True if undocking was successful, False otherwise
        """
        if ship in self.docked_ships:
            self.docked_ships.remove(ship)
            return True
        return False

    def provide_service(self, ship: Starship, service_type: str) -> bool:
        """
        Provide a service to a docked ship.

        Args:
            ship: Ship receiving the service
            service_type: Type of service to provide

        Returns:
            True if service was provided, False otherwise
        """
        # Service implementation will be added later
        return ship in self.docked_ships and service_type in self.services
