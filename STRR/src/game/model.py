#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Star Trek Retro Remake - Game Model

Description:
    Pure game logic and state management implementing the Model component of the
    MVC pattern. Contains no UI dependencies and can be tested independently.

Author: Star Trek Retro Remake Development Team
Email: development@star-trek-retro-remake.org
GitHub: https://github.com/L3DigitalNet/Star-Trek-Retro-Remake
Date Created: 10-29-2025
Date Changed: 10-30-2025 (v0.0.9 - Bug fixes)
License: MIT

Features:
    - Pure game logic with no UI dependencies
    - Galaxy and sector map management
    - Turn-based game mechanics
    - Starship and entity management
    - Mission and event systems
    - Save/load game state functionality

Requirements:
    - Linux environment
    - Python 3.14+ for latest language features

Classes:
    - GameModel: Core game state and logic management
    - TurnManager: Turn-based gameplay coordination
    - CombatResult: Combat action result data

Functions:
    - None
"""

from typing import Final
from dataclasses import dataclass

from .entities.starship import Starship
from .entities.base import GridPosition, GameObject
from .maps.galaxy import GalaxyMap
from .maps.sector import SectorMap

__version__: Final[str] = "0.0.10"


@dataclass
class CombatResult:
    """
    Results of a combat action.

    Attributes:
        success: Whether the combat action succeeded
        message: Descriptive message about the result
        damage: Amount of damage dealt (if applicable)
    """

    success: bool
    message: str
    damage: int = 0


class TurnManager:
    """
    Manages turn-based gameplay mechanics.

    Attributes:
        turn_number: Current turn number
        current_phase: Current phase of the turn

    Public methods:
        advance_turn: Advance to the next turn
        get_turn_info: Get current turn information

    Private methods:
        _process_ai_turns: Process AI entity turns
    """

    def __init__(self):
        """Initialize the turn manager."""
        self.turn_number: int = 0
        self.current_phase: str = "player"

    def advance_turn(self) -> None:
        """Advance to the next turn and process AI actions."""
        self.turn_number += 1
        self._process_ai_turns()

    def get_turn_info(self) -> dict[str, int | str]:
        """Get current turn information."""
        return {"turn_number": self.turn_number, "current_phase": self.current_phase}

    def _process_ai_turns(self) -> None:
        """Process AI entity turns and actions."""
        # AI processing logic will be implemented here
        pass


class GameModel:
    """
    Pure game logic and state management.

    Contains all game state and business logic without any UI dependencies.
    Can be tested independently of the UI components.

    Attributes:
        galaxy: Galaxy map containing all sectors
        current_sector: Currently active sector map
        player_ship: Player's starship entity
        turn_manager: Turn-based gameplay manager
        game_objects: List of all active game objects
        active_missions: List of current active missions

    Public methods:
        initialize_new_game: Set up a new game
        execute_move: Execute starship movement
        resolve_combat: Resolve combat between entities
        save_game: Save current game state
        load_game: Load saved game state

    Private methods:
        _is_valid_move: Validate movement request
        _create_player_ship: Create the player's starting ship
    """

    def __init__(self):
        """Initialize the game model with default state."""
        # Map system
        self.galaxy = GalaxyMap()
        self.current_sector: SectorMap | None = None

        # Player and entities
        self.player_ship: Starship | None = None
        self.game_objects: list[GameObject] = []

        # Game systems
        self.turn_manager = TurnManager()
        self.active_missions: list[object] = []  # Will be properly typed later

    def initialize_new_game(self) -> None:
        """Set up a new game with default starting conditions."""
        # Load starting sector FIRST
        self.current_sector = self.galaxy.get_sector(0, 0)

        # Validate sector was loaded successfully
        if not self.current_sector:
            raise RuntimeError("Failed to load starting sector (0, 0)")

        # Create player ship at starting position
        start_position = GridPosition(5, 5, 1)
        self.player_ship = self._create_player_ship(start_position)

        # Add player ship to game objects
        self.game_objects.append(self.player_ship)

        # Register ship in sector entities dictionary
        if not self.current_sector.place_entity(self.player_ship, start_position):
            raise RuntimeError(f"Failed to place player ship at {start_position}")

    def execute_move(self, ship: Starship, destination: GridPosition) -> bool:
        """
        Execute ship movement if valid.

        Args:
            ship: The starship to move
            destination: Target position for movement

        Returns:
            True if movement was successful, False otherwise
        """
        # Check for active sector
        if not self.current_sector:
            return False

        # Validate movement
        if not self._is_valid_move(ship, destination):
            return False

        # Get engine system and validate it exists
        engines = ship.get_system("engines")
        if not engines:
            return False

        # Calculate movement cost
        distance = int(ship.position.distance_to(destination))
        fuel_cost = engines.calculate_movement_cost(distance)

        # Check fuel availability
        if engines.fuel < fuel_cost:
            return False

        # Store old position for rollback if needed
        old_position = ship.position

        # Update ship position BEFORE moving in sector map
        # This ensures ship.position and sector.entities stay synchronized
        ship.position = destination

        # Move entity in sector map (updates entities dictionary)
        if not self.current_sector.move_entity(old_position, destination):
            # Rollback ship position if sector move failed
            ship.position = old_position
            return False

        # Deduct fuel and advance turn
        engines.fuel -= fuel_cost
        self.turn_manager.advance_turn()

        # Cleanup inactive objects after turn
        self._cleanup_inactive_objects()

        return True

    def resolve_combat(
        self, attacker: Starship, target: Starship, weapon_type: str
    ) -> CombatResult:
        """
        Resolve combat between two starships.

        Args:
            attacker: The attacking starship
            target: The target starship
            weapon_type: Type of weapon being used

        Returns:
            CombatResult containing the outcome
        """
        # Get attacker's weapon system
        weapons = attacker.get_system("weapons")
        if not weapons or not weapons.active:
            return CombatResult(False, "Weapons offline")

        # Check targeting capability
        if not weapons.can_target(
            target.position, attacker.position, attacker.orientation
        ):
            return CombatResult(False, "Target out of range")

        # Calculate and apply damage
        damage = weapons.calculate_damage(weapon_type, target)
        target.take_damage(damage)

        return CombatResult(True, f"Hit for {damage} damage", damage)

    def save_game(self, filepath: str) -> bool:
        """
        Save current game state to file.

        Args:
            filepath: Path to save the game file

        Returns:
            True if save was successful, False otherwise
        """
        # Save functionality will be implemented here
        return True

    def load_game(self, filepath: str) -> bool:
        """
        Load saved game state from file.

        Args:
            filepath: Path to the saved game file

        Returns:
            True if load was successful, False otherwise
        """
        # Load functionality will be implemented here
        return True

    def _is_valid_move(self, ship: Starship, destination: GridPosition) -> bool:
        """
        Check if the requested move is valid.

        Args:
            ship: The starship requesting movement
            destination: Target destination

        Returns:
            True if move is valid, False otherwise
        """
        # Explicit check for current sector (defensive programming for early version)
        if not self.current_sector:
            return False

        # Check sector bounds
        if not self.current_sector.is_in_bounds(destination):
            return False

        # Check for obstacles
        if self.current_sector.has_obstacle(destination):
            return False

        return True

    def _create_player_ship(self, position: GridPosition) -> Starship:
        """
        Create the player's starting starship.

        Args:
            position: Starting position for the ship

        Returns:
            Configured player starship
        """
        return Starship(position, "Constitution", "Enterprise")

    def _cleanup_inactive_objects(self) -> None:
        """
        Remove destroyed objects from game to prevent memory leaks.

        Filters out all game objects where active=False. Uses isinstance
        check to ensure type safety.
        """
        initial_count = len(self.game_objects)
        self.game_objects = [
            obj
            for obj in self.game_objects
            if isinstance(obj, GameObject) and obj.active
        ]
        removed_count = initial_count - len(self.game_objects)

        if removed_count > 0:
            pass  # Cleanup logging deferred until v1.0.0
