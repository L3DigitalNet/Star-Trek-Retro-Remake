#!/usr/bin/env python3
"""
Star Trek Retro Remake - Base Entity Classes

Description:
    Core base classes for all game entities implementing the Game Object pattern
    with component composition.

Author: Star Trek Retro Remake Development Team
Email: development@star-trek-retro-remake.org
GitHub: https://github.com/L3DigitalNet/Star-Trek-Retro-Remake
Date Created: 10-29-2025
Date Changed: 10-30-2025 (v0.0.18 - Turn-based system)
License: MIT

Features:
    - Game Object Pattern with Component composition
    - 3D grid position system with z-levels
    - Unique entity identification system
    - Clean inheritance hierarchy for Star Trek entities

Requirements:
    - Linux environment
    - Python 3.14+ for latest language features

Classes:
    - GridPosition: 3D position representation with z-level support
    - GameObject: Base class for all game entities

Functions:
    - None
"""

import uuid
from dataclasses import dataclass
from typing import Final

__version__: Final[str] = "0.0.18"


@dataclass(frozen=True)
class GridPosition:
    """
    3D grid position with z-level support.

    Represents a position in the game's 3D grid system where x and y are
    the horizontal coordinates and z represents the vertical level.

    Immutable (frozen) for use as dictionary keys and in sets.

    Attributes:
        x: Horizontal x-coordinate
        y: Horizontal y-coordinate
        z: Vertical z-level (default 0)
    """

    x: int
    y: int
    z: int = 0

    def distance_to(self, other: "GridPosition") -> float:
        """
        Calculate 3D distance to another position.

        Args:
            other: Target position to calculate distance to

        Returns:
            Euclidean distance between positions
        """
        dx = self.x - other.x
        dy = self.y - other.y
        dz = self.z - other.z
        return (dx * dx + dy * dy + dz * dz) ** 0.5

    def __add__(self, other: "GridPosition") -> "GridPosition":
        """Add two grid positions component-wise."""
        return GridPosition(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: "GridPosition") -> "GridPosition":
        """Subtract two grid positions component-wise."""
        return GridPosition(self.x - other.x, self.y - other.y, self.z - other.z)


class GameObject:
    """
    Base class for all game entities.

    Implements the core Game Object pattern with unique identification,
    position tracking, and lifecycle management.

    Attributes:
        id: Unique identifier for the entity
        position: Current 3D grid position
        name: Display name for the entity
        active: Whether the entity is active in the game
        faction: Faction affiliation (if applicable)
        initiative: Initiative value for turn order (higher acts first)
        action_points: Available action points this turn
        max_action_points: Maximum action points per turn

    Public methods:
        update: Update entity logic each game tick
        destroy: Mark entity for removal from the game
        reset_action_points: Restore action points at turn start
        spend_action_points: Consume action points for action
        has_action_points: Check if entity can perform action

    Private methods:
        _generate_id: Generate unique entity identifier
    """

    def __init__(self, position: GridPosition, name: str = ""):
        """
        Initialize a new game object.

        Args:
            position: Initial 3D grid position
            name: Display name for the entity
        """
        self.id = self._generate_id()
        self.position = position
        self.name = name
        self.active = True
        self.faction: str | None = None

        # Turn-based system attributes
        self.initiative: int = 0  # Base initiative (can be modified by ship class)
        self.action_points: int = 0  # Current available action points
        self.max_action_points: int = 3  # Maximum action points per turn

    def update(self, dt: float) -> None:
        """
        Update entity logic.

        Args:
            dt: Time delta since last update in seconds
        """
        # Base implementation - subclasses override for specific behavior
        pass

    def destroy(self) -> None:
        """Mark entity for removal from the game."""
        self.active = False

    def reset_action_points(self) -> None:
        """Restore action points to maximum at start of turn."""
        self.action_points = self.max_action_points

    def spend_action_points(self, cost: int) -> bool:
        """
        Consume action points for an action.

        Args:
            cost: Number of action points to spend

        Returns:
            True if action points were spent, False if insufficient
        """
        if self.action_points >= cost:
            self.action_points -= cost
            return True
        return False

    def has_action_points(self, cost: int) -> bool:
        """
        Check if entity has enough action points.

        Args:
            cost: Required action points

        Returns:
            True if entity has enough action points
        """
        return self.action_points >= cost

    @staticmethod
    def _generate_id() -> str:
        """
        Generate unique entity ID.

        Returns:
            Unique string identifier
        """
        return str(uuid.uuid4())
