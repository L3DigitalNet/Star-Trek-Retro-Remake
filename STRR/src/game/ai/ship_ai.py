#!/usr/bin/env python3
"""
Star Trek Retro Remake - Ship AI

Description:
    AI behavior system for NPC starships using simple state machine.
    Implements patrol, attack, and flee behaviors.

Author: Star Trek Retro Remake Development Team
Email: development@star-trek-retro-remake.org
GitHub: https://github.com/L3DigitalNet/Star-Trek-Retro-Remake
Date Created: 10-30-2025
Date Changed: 02-19-2026 (v0.0.31 - Use public is_valid_move, remove stale _assess_threat docstring)
License: MIT

Features:
    - Simple state machine for AI decision-making
    - Patrol behavior with random movement
    - Attack behavior with target selection
    - Flee behavior when damaged
    - Threat assessment and target prioritization

Requirements:
    - Linux environment
    - Python 3.14+ for latest language features

Classes:
    - AIState: Enumeration of AI states
    - ShipAI: AI controller for NPC ships

Functions:
    - None
"""

from __future__ import annotations

from enum import Enum, auto
from typing import Final, TYPE_CHECKING, cast
import random

if TYPE_CHECKING:
    from ..entities.starship import Starship
    from ..entities.base import GridPosition
    from ..model import GameModel

from ...engine.config_loader import get_combat_config

__version__: Final[str] = "0.0.31"


class AIState(Enum):
    """
    AI state enumeration.

    States:
        PATROL: Wandering/patrolling behavior
        ATTACK: Engaging hostile targets
        FLEE: Retreating from combat
    """

    PATROL = auto()
    ATTACK = auto()
    FLEE = auto()


class ShipAI:
    """
    AI controller for NPC starships.

    Implements simple state machine with patrol, attack, and flee behaviors.

    Attributes:
        ship: The starship this AI controls
        state: Current AI state
        target: Current attack target (if any)
        patrol_center: Center point for patrol behavior
        patrol_radius: Radius for patrol movement
        flee_threshold: Hull percentage to trigger flee state

    Public methods:
        update: Update AI state and execute behavior
        set_state: Manually set AI state
        select_target: Choose best target from available enemies

    Private methods:
        _update_patrol: Execute patrol behavior
        _update_attack: Execute attack behavior
        _update_flee: Execute flee behavior
        _transition_state: Handle state transitions
        _find_patrol_point: Find random point for patrol
    """

    def __init__(self, ship: Starship):
        """
        Initialize AI controller for a ship.

        Args:
            ship: Starship to control
        """
        # Load AI configuration using centralized config loader
        config = get_combat_config()

        self.ship = ship
        self.state = AIState.PATROL
        self.target: Starship | None = None

        # Patrol parameters (from config)
        self.patrol_center = ship.position
        self.patrol_radius = cast(int, config.get("ai_patrol_radius") or 5)

        # Behavior thresholds (from config)
        self.flee_threshold = cast(float, config.get("ai_flee_threshold") or 30.0)

        # Performance cache (from config)
        self._cached_enemies: list[Starship] = []
        self._cache_age = 0
        self._cache_max_age = cast(int, config.get("ai_enemy_cache_turns") or 3)

    def update(self, model: "GameModel") -> None:
        """
        Update AI state and execute behavior.

        Args:
            model: Game model for accessing game state
        """
        # Check for state transitions
        self._transition_state(model)

        # Execute behavior based on current state
        if self.state == AIState.PATROL:
            self._update_patrol(model)
        elif self.state == AIState.ATTACK:
            self._update_attack(model)
        elif self.state == AIState.FLEE:
            self._update_flee(model)

    def _transition_state(self, model: "GameModel") -> None:
        """
        Handle AI state transitions.

        Args:
            model: Game model for accessing game state
        """
        # Check hull damage - flee if critically damaged
        if self.ship.hull_integrity < self.flee_threshold:
            if self.state != AIState.FLEE:
                self.state = AIState.FLEE
                self.target = None
                return

        # If healthy enough and fleeing, return to patrol
        if (
            self.state == AIState.FLEE
            and self.ship.hull_integrity > self.flee_threshold * 1.5
        ):
            self.state = AIState.PATROL
            return

        # Look for enemies if not fleeing (with caching)
        if self.state != AIState.FLEE:
            enemies = self._get_enemies_cached(model)
            if enemies:
                # Transition to attack if enemies in range
                if self.state != AIState.ATTACK:
                    self.state = AIState.ATTACK
                    self.target = self.select_target(enemies)
            else:
                # Return to patrol if no enemies
                if self.state == AIState.ATTACK:
                    self.state = AIState.PATROL
                    self.target = None

    def _update_patrol(self, model: "GameModel") -> None:
        """
        Execute patrol behavior - random movement within patrol area.

        Args:
            model: Game model for movement
        """
        # Move randomly within patrol radius if have action points
        if self.ship.has_action_points(1):
            destination = self._find_patrol_point(model)
            if destination:
                model.execute_move(self.ship, destination)

    def _update_attack(self, model: "GameModel") -> None:
        """
        Execute attack behavior - move toward and fire at target.

        Args:
            model: Game model for combat
        """
        if not self.target or not self.target.active:
            self.target = None
            return

        # Get weapon system
        from ..components.ship_systems import WeaponSystems  # local runtime import for isinstance narrowing
        weapons = self.ship.get_system("weapons")
        if not weapons or not weapons.active or not isinstance(weapons, WeaponSystems):
            return

        # If in weapon range, fire
        if weapons.can_target(
            self.target.position, self.ship.position, self.ship.orientation, "phaser"
        ):
            # Fire weapons if have action points
            if self.ship.has_action_points(1):
                model.resolve_combat(self.ship, self.target, "phaser")
        else:
            # Move closer to target
            if self.ship.has_action_points(1):
                destination = self._move_toward_target(model, self.target.position)
                if destination:
                    model.execute_move(self.ship, destination)

    def _update_flee(self, model: "GameModel") -> None:
        """
        Execute flee behavior - move away from enemies.

        Args:
            model: Game model for movement
        """
        # Find nearest enemy
        enemies = self._find_enemies(model)
        if not enemies:
            return

        nearest_enemy = min(
            enemies, key=lambda e: self.ship.position.distance_to(e.position)
        )

        # Move away from nearest enemy
        if self.ship.has_action_points(1):
            destination = self._move_away_from(model, nearest_enemy.position)
            if destination:
                model.execute_move(self.ship, destination)

    def _get_enemies_cached(self, model: "GameModel") -> list["Starship"]:
        """
        Get enemy ships with caching to reduce scanning overhead.

        Args:
            model: Game model for accessing game objects

        Returns:
            List of enemy ships in sensor range
        """
        # Refresh cache if too old or empty
        if self._cache_age >= self._cache_max_age or not self._cached_enemies:
            self._cached_enemies = self._find_enemies(model)
            self._cache_age = 0
        else:
            self._cache_age += 1

        return self._cached_enemies

    def _find_enemies(self, model: "GameModel") -> list["Starship"]:
        """
        Find all enemy ships within sensor range.

        Args:
            model: Game model for accessing game objects

        Returns:
            List of enemy ships in sensor range
        """
        from ..entities.starship import Starship

        enemies: list["Starship"] = []

        # Get sensor system for range
        from ..components.ship_systems import SensorSystems  # local runtime import for isinstance narrowing
        sensors = self.ship.get_system("sensors")
        sensor_range = sensors.scan_range() if sensors and sensors.active and isinstance(sensors, SensorSystems) else 10

        # Find all enemy ships in range
        for obj in model.game_objects:
            if isinstance(obj, Starship) and obj.active and obj != self.ship:
                if obj.faction != self.ship.faction:
                    distance = self.ship.position.distance_to(obj.position)
                    if distance <= sensor_range:
                        enemies.append(obj)

        return enemies

    def select_target(self, enemies: list["Starship"]) -> "Starship | None":
        """
        Select best target from available enemies.

        Prioritizes closest enemies with lowest hull integrity.

        Args:
            enemies: List of potential targets

        Returns:
            Selected target or None
        """
        if not enemies:
            return None

        # Score targets (lower is better)
        def score_target(enemy: "Starship") -> float:
            distance = self.ship.position.distance_to(enemy.position)
            hull_factor = enemy.hull_integrity / 100.0
            return distance * hull_factor

        return min(enemies, key=score_target)

    def _find_patrol_point(self, model: "GameModel") -> "GridPosition | None":
        """
        Find random point within patrol radius.

        Args:
            model: Game model for validation

        Returns:
            Valid patrol destination or None
        """
        from ..entities.base import GridPosition

        # Try several random points
        for _ in range(10):
            dx = random.randint(-self.patrol_radius, self.patrol_radius)
            dy = random.randint(-self.patrol_radius, self.patrol_radius)

            destination = GridPosition(
                self.patrol_center.x + dx,
                self.patrol_center.y + dy,
                self.ship.position.z,
            )

            if model.is_valid_move(self.ship, destination):
                return destination

        return None

    def _move_toward_target(
        self, model: "GameModel", target_pos: "GridPosition"
    ) -> "GridPosition | None":
        """
        Find best move toward target position.

        Args:
            model: Game model for validation
            target_pos: Target position to move toward

        Returns:
            Valid destination or None
        """
        from ..entities.base import GridPosition

        # Calculate direction to target
        dx = target_pos.x - self.ship.position.x
        dy = target_pos.y - self.ship.position.y

        # Normalize to one grid cell
        if abs(dx) > abs(dy):
            dx = 1 if dx > 0 else -1
            dy = 0
        else:
            dx = 0
            dy = 1 if dy > 0 else -1

        destination = GridPosition(
            self.ship.position.x + dx, self.ship.position.y + dy, self.ship.position.z
        )

        if model.is_valid_move(self.ship, destination):
            return destination

        return None

    def _move_away_from(
        self, model: "GameModel", threat_pos: "GridPosition"
    ) -> "GridPosition | None":
        """
        Find best move away from threat position.

        Args:
            model: Game model for validation
            threat_pos: Position to move away from

        Returns:
            Valid destination or None
        """
        from ..entities.base import GridPosition

        # Calculate direction away from threat
        dx = self.ship.position.x - threat_pos.x
        dy = self.ship.position.y - threat_pos.y

        # Normalize to one grid cell
        if abs(dx) > abs(dy):
            dx = 1 if dx > 0 else -1
            dy = 0
        else:
            dx = 0
            dy = 1 if dy > 0 else -1

        destination = GridPosition(
            self.ship.position.x + dx, self.ship.position.y + dy, self.ship.position.z
        )

        if model.is_valid_move(self.ship, destination):
            return destination

        return None

    def set_state(self, state: AIState) -> None:
        """
        Manually set AI state.

        Args:
            state: New AI state
        """
        self.state = state
