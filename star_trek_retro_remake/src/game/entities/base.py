#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Star Trek Retro Remake - Base Entity Classes

Description:
    Core base classes for all game entities implementing the Game Object pattern
    with component composition.

Author: Star Trek Retro Remake Development Team
Email: development@star-trek-retro-remake.org
GitHub: https://github.com/L3DigitalNet/Star-Trek-Retro-Remake
Date Created: 10-29-2025
Date Changed: 10-29-2025
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
from typing import Final, Optional

__version__: Final[str] = "0.0.1"


@dataclass
class GridPosition:
    """
    3D grid position with z-level support.

    Represents a position in the game's 3D grid system where x and y are
    the horizontal coordinates and z represents the vertical level.

    Attributes:
        x: Horizontal x-coordinate
        y: Horizontal y-coordinate
        z: Vertical z-level (default 0)
    """
    x: int
    y: int
    z: int = 0

    def distance_to(self, other: 'GridPosition') -> float:
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
        return (dx*dx + dy*dy + dz*dz) ** 0.5


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

    Public methods:
        update: Update entity logic each game tick
        destroy: Mark entity for removal from the game

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
        self.faction: Optional[str] = None

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

    @staticmethod
    def _generate_id() -> str:
        """
        Generate unique entity ID.

        Returns:
            Unique string identifier
        """
        return str(uuid.uuid4())