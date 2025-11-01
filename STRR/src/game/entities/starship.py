#!/usr/bin/env python3
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
    - Directional shields with facing system
    - Advanced damage system with hull and system damage
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

from typing import TYPE_CHECKING, Final

from ..components.ship_systems import (
    CrewManager,
    EngineSystems,
    LifeSupportSystems,
    ResourceManager,
    SensorSystems,
    ShieldSystems,
    ShipSystem,
    WeaponSystems,
)
from .base import GameObject, GridPosition

if TYPE_CHECKING:
    from ..ai.ship_ai import ShipAI

__version__: Final[str] = "0.0.22"


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
        ai_controller: AI controller for NPC ships (None for player ship)
        is_player: Whether this is the player's ship

    Public methods:
        get_system: Retrieve a specific ship system
        take_damage: Apply damage to ship systems and hull
        repair_system: Repair a damaged ship system
        get_orientation_radians: Get orientation in radians for rendering
        set_ai_controller: Attach AI controller to this ship

    Private methods:
        _get_faction_color: Determine color based on faction
        _apply_system_damage: Apply damage to systems when hull critical
    """

    def __init__(
        self,
        position: GridPosition,
        ship_class: str,
        name: str = "",
        faction: str = "Federation",
        is_player: bool = False,
    ):
        """
        Initialize a new starship.

        Args:
            position: Initial 3D grid position
            ship_class: Ship class designation
            name: Ship name
            faction: Faction affiliation (Federation, Klingon, Romulan, etc.)
            is_player: Whether this is the player's ship
        """
        super().__init__(position, name)
        self.ship_class = ship_class
        self.faction = faction
        self.is_player = is_player

        # Initialize ship systems using component composition
        self.systems: dict[str, ShipSystem] = {
            "weapons": WeaponSystems(),
            "shields": ShieldSystems(),
            "engines": EngineSystems(),
            "sensors": SensorSystems(),
            "life_support": LifeSupportSystems(),
            "resources": ResourceManager(),
            "crew": CrewManager(),
        }

        # Ship resources and crew (quick access properties)
        self.resources: ResourceManager = self.systems["resources"]  # type: ignore
        self.crew: CrewManager = self.systems["crew"]  # type: ignore

        # Ship state
        self.hull_integrity: float = 100.0
        self.orientation: int = 0  # 0-359 degrees

        # Visual representation attributes
        self.color = self._get_faction_color(faction)
        self.size = 16  # Base size in pixels for rendering

        # AI controller (None for player ship)
        self.ai_controller: ShipAI | None = None

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

    def take_damage(
        self,
        amount: int,
        damage_type: str = "energy",
        attacker_pos: GridPosition | None = None,
    ) -> dict[str, int | str]:
        """
        Apply damage to ship systems and hull.

        Args:
            amount: Amount of damage to apply
            damage_type: Type of damage (kinetic, energy, etc.)
            attacker_pos: Position of attacker for shield facing calculation

        Returns:
            Dictionary with damage results (shields_absorbed, hull_damage, facing_hit)
        """
        result: dict[str, int | str] = {
            "shields_absorbed": 0,
            "hull_damage": 0,
            "facing_hit": "unknown",
        }

        # Shield absorption first
        shields = self.get_system("shields")
        if shields and shields.active:
            remaining = shields.absorb_damage(
                amount,
                damage_type,
                ship_orientation=self.orientation,
                attacker_pos=attacker_pos,
                ship_pos=self.position,
            )
            result["shields_absorbed"] = amount - remaining
            amount = remaining

            # Determine which facing was hit for reporting
            if attacker_pos:
                result["facing_hit"] = shields._determine_hit_facing(
                    self.position, attacker_pos, self.orientation
                )

        # Apply remaining damage to hull
        if amount > 0:
            self.hull_integrity = max(0, self.hull_integrity - amount)
            result["hull_damage"] = amount

            # Check for critical damage to systems
            if self.hull_integrity < 50:
                self._apply_system_damage(amount)

            # Destroy ship if hull fails
            if self.hull_integrity <= 0:
                self.destroy()

        return result

    def _apply_system_damage(self, hull_damage: int) -> None:
        """
        Apply damage to ship systems when hull is critically damaged.

        Args:
            hull_damage: Amount of hull damage taken
        """
        import random

        # Chance of system damage increases as hull weakens
        damage_chance = 0.3 + (1.0 - self.hull_integrity / 100.0) * 0.4

        if random.random() < damage_chance:
            # Select random system to damage
            system_names = list(self.systems.keys())
            if system_names:
                damaged_system = random.choice(system_names)
                system = self.systems[damaged_system]
                system.damage(hull_damage * 0.1)  # System takes 10% of hull damage

    def repair_system(
        self, system_name: str, repair_amount: float, use_supplies: bool = True
    ) -> bool:
        """
        Repair a damaged ship system.

        Args:
            system_name: Name of the system to repair
            repair_amount: Amount of repair to apply
            use_supplies: Whether to consume spare parts for repair

        Returns:
            True if repair was successful, False otherwise
        """
        system = self.get_system(system_name)
        if not system:
            return False

        # Calculate repair cost based on damage and crew efficiency
        damage_amount = system.max_efficiency - system.efficiency
        spare_parts_needed = int(damage_amount * 10)  # 10 parts per 0.1 efficiency

        # Check if we have supplies for repair (if required)
        if use_supplies and spare_parts_needed > 0:
            if not self.resources.use_supplies("spare_parts", spare_parts_needed):
                return False  # Not enough spare parts

        # Apply repair with crew efficiency modifier
        crew_efficiency = self.crew.get_efficiency_multiplier()
        effective_repair = repair_amount * crew_efficiency

        system.repair(effective_repair)
        return True

    def get_orientation_radians(self) -> float:
        """
        Get ship orientation in radians for rendering.

        Returns:
            Orientation angle in radians (0 to 2π)
        """
        import math

        return math.radians(self.orientation)

    def allocate_power(self, system: str, percentage: float) -> bool:
        """
        Set power distribution percentage for a system.

        Args:
            system: System name (shields, weapons, engines, sensors, life_support)
            percentage: Power allocation percentage (0-100)

        Returns:
            True if allocation successful, False if invalid
        """
        return self.resources.allocate_power(system, percentage)

    def consume_energy_for_action(self, action: str) -> bool:
        """
        Consume energy for an action.

        Args:
            action: Action name (move, fire_phaser, fire_torpedo, scan, shield_regen)

        Returns:
            True if energy was consumed, False if insufficient
        """
        return self.resources.consume_energy(action)

    def has_sufficient_energy(self, action: str) -> bool:
        """
        Check if ship has enough energy for an action.

        Args:
            action: Action name

        Returns:
            True if energy is available
        """
        cost = self.resources.energy_costs.get(action, 0.0)
        return self.resources.has_energy(cost)

    def refuel_at_starbase(self) -> None:
        """Refuel ship to maximum capacity at starbase."""
        self.resources.refuel(
            self.resources.fuel_capacity - self.resources.fuel_current
        )

    def resupply_at_starbase(self) -> None:
        """Resupply ship to maximum capacity at starbase."""
        self.resources.resupply(
            "medical", 100 - self.resources.supplies.get("medical", 0)
        )
        self.resources.resupply(
            "spare_parts", 50 - self.resources.supplies.get("spare_parts", 0)
        )
        # Boost crew morale on starbase visit
        self.crew.visit_starbase()

    def get_crew_efficiency(self) -> float:
        """
        Get current crew efficiency multiplier.

        Returns:
            Efficiency multiplier (0.5 - 1.5)
        """
        return self.crew.get_efficiency_multiplier()

    def record_combat_result(self, victory: bool) -> None:
        """
        Record combat outcome and update crew morale.

        Args:
            victory: True if combat won, False if lost
        """
        self.crew.record_combat_outcome(victory)

    def set_ai_controller(self, ai: ShipAI) -> None:
        """
        Attach AI controller to this ship.

        Args:
            ai: AI controller instance
        """
        self.ai_controller = ai


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
            service_type: Type of service to provide (repair, refuel, resupply)

        Returns:
            True if service was provided, False otherwise
        """
        # Check if ship is docked
        if ship not in self.docked_ships:
            return False

        # Provide service based on type
        if service_type == "refuel":
            ship.refuel_at_starbase()
            return True
        elif service_type == "resupply":
            ship.resupply_at_starbase()
            return True
        elif service_type == "repair":
            # Repair all systems to full efficiency
            for system in ship.systems.values():
                system.repair(system.max_efficiency)
            # Repair hull to 100%
            ship.hull_integrity = 100.0
            return True

        return False
