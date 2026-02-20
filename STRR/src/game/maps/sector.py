#!/usr/bin/env python3
"""
Star Trek Retro Remake - Sector Map

Description:
    Sector map implementation for detailed exploration with 3D grid support.

Author: Star Trek Retro Remake Development Team
Email: development@star-trek-retro-remake.org
GitHub: https://github.com/L3DigitalNet/Star-Trek-Retro-Remake
Date Created: 10-29-2025
Date Changed: 02-19-2026
License: MIT

Features:
    - 3D grid-based sector exploration
    - Multiple z-levels for spatial depth
    - Entity placement and obstacle management
    - Environmental effects and hazards

Requirements:
    - Linux environment
    - Python 3.14+ for latest language features

Classes:
    - SectorMap: Detailed sector exploration with 3D grid

Functions:
    - None
"""

import random
from typing import Final

from ..entities.base import GridPosition

__version__: Final[str] = "0.0.31"


class SectorMap:
    """
    Detailed sector exploration with 3D grid support.

    Manages a 3D grid-based sector with multiple z-levels,
    entity placement, obstacles, and environmental effects.

    Attributes:
        coordinates: Galaxy coordinates of this sector
        sector_type: Type of sector (federation, neutral, hostile, etc.)
        grid_size: Size of the sector grid as (width, height, depth)
        entities: Dictionary of entities by position
        obstacles: Set of obstacle positions
        environmental_effects: Dictionary of environmental effects

    Public methods:
        is_in_bounds: Check if position is within sector bounds
        has_obstacle: Check if position contains an obstacle
        place_entity: Place an entity at a position
        remove_entity: Remove an entity from a position
        get_entity_at: Get entity at a specific position
        add_obstacle: Add an obstacle at a position

    Private methods:
        _initialize_sector: Set up sector based on type
    """

    def __init__(
        self,
        coordinates: tuple[int, int],
        sector_type: str = "standard",
        random_seed: int | None = None,
    ):
        """
        Initialize a new sector map.

        Args:
            coordinates: Galaxy coordinates of this sector
            sector_type: Type of sector to create
            random_seed: Optional seed for deterministic random generation (testing)
        """
        # Store sector identification and configuration
        self.coordinates = coordinates
        self.sector_type = sector_type
        self.grid_size = (20, 20, 5)  # width, height, depth (3D grid)
        self.random_seed = random_seed

        # Initialize entity and obstacle tracking structures
        self.entities: dict[GridPosition, object] = {}
        self.obstacles: set[GridPosition] = set()
        self.environmental_effects: dict[GridPosition, str] = {}

        # Generate sector content based on type
        self._initialize_sector()

    def is_in_bounds(self, position: GridPosition) -> bool:
        """
        Check if position is within sector bounds.

        Args:
            position: Position to check

        Returns:
            True if position is within bounds, False otherwise
        """
        # Validate position against 3D grid boundaries
        return (
            0 <= position.x < self.grid_size[0]
            and 0 <= position.y < self.grid_size[1]
            and 0 <= position.z < self.grid_size[2]
        )

    def has_obstacle(self, position: GridPosition) -> bool:
        """
        Check if position contains an obstacle.

        Args:
            position: Position to check

        Returns:
            True if position has an obstacle, False otherwise
        """
        return position in self.obstacles

    def place_entity(self, entity: object, position: GridPosition) -> bool:
        """
        Place an entity at a position.

        Args:
            entity: Entity to place
            position: Position to place entity at

        Returns:
            True if placement was successful, False otherwise
        """
        # Validate position is within sector bounds
        if not self.is_in_bounds(position):
            return False

        # Prevent placement on obstacles
        if self.has_obstacle(position):
            return False

        # Register entity at position
        self.entities[position] = entity
        return True

    def remove_entity(self, position: GridPosition) -> object | None:
        """
        Remove an entity from a position.

        Args:
            position: Position to remove entity from

        Returns:
            Removed entity or None if no entity was present
        """
        return self.entities.pop(position, None)

    def get_entity_at(self, position: GridPosition) -> object | None:
        """
        Get entity at a specific position.

        Args:
            position: Position to check

        Returns:
            Entity at position or None if empty
        """
        return self.entities.get(position)

    def add_obstacle(self, position: GridPosition) -> bool:
        """
        Add an obstacle at a position.

        Args:
            position: Position to place obstacle

        Returns:
            True if obstacle was added, False otherwise
        """
        if not self.is_in_bounds(position):
            return False

        self.obstacles.add(position)
        return True

    def move_entity(self, old_pos: GridPosition, new_pos: GridPosition) -> bool:
        """
        Move an entity from old position to new position.

        Updates the entities dictionary to reflect the new position and
        synchronizes the entity's position attribute if present.

        Args:
            old_pos: Current position of the entity
            new_pos: Target position for the entity

        Returns:
            True if move was successful, False otherwise
        """
        # Validate target position is within sector bounds
        if not self.is_in_bounds(new_pos):
            return False

        # Retrieve entity from current position
        entity = self.entities.pop(old_pos, None)
        if entity is None:
            return False

        # Verify target position is not blocked by obstacle
        if self.has_obstacle(new_pos):
            # Rollback: restore entity at original position
            self.entities[old_pos] = entity
            return False

        # Complete move: register entity at new position
        self.entities[new_pos] = entity

        # Synchronize entity's internal position state to prevent desync
        if hasattr(entity, "position"):
            entity.position = new_pos

        return True

    def get_all_entities(self) -> list[tuple[GridPosition, object]]:
        """
        Get all entities in the sector.

        Returns:
            List of (position, entity) tuples
        """
        return list(self.entities.items())

    def _initialize_sector(self) -> None:
        """Set up sector based on type."""
        # Initialize RNG with optional seed for deterministic generation
        rng = (
            random.Random(self.random_seed) if self.random_seed is not None else random
        )

        # Generate sector content based on sector type
        if self.sector_type == "asteroid_field":
            # Populate sector with randomly distributed asteroids
            for _ in range(10):
                x = rng.randint(0, self.grid_size[0] - 1)
                y = rng.randint(0, self.grid_size[1] - 1)
                z = rng.randint(0, self.grid_size[2] - 1)
                self.add_obstacle(GridPosition(x, y, z))

        elif self.sector_type == "nebula":
            # Create nebula effect zone in central region
            for x in range(5, 15):
                for y in range(5, 15):
                    for z in range(1, 4):
                        pos = GridPosition(x, y, z)
                        self.environmental_effects[pos] = "nebula"
