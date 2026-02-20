#!/usr/bin/env python3
"""
Star Trek Retro Remake - Game Model Tests

Description:
    Unit tests for the game model and core game logic.

Author: Star Trek Retro Remake Development Team
Date Created: 10-29-2025
Date Changed: 10-30-2025
License: MIT
"""

from typing import Final
from unittest.mock import patch

import pytest
from src.game.entities.base import GridPosition
from src.game.model import CombatResult, GameModel, TurnManager

pytestmark = pytest.mark.unit

__version__: Final[str] = "0.0.1"


class TestTurnManager:
    """Test cases for TurnManager class."""

    def test_turn_manager_initialization(self):
        """Test that TurnManager initializes correctly."""
        # Arrange & Act
        turn_manager = TurnManager()

        # Assert
        assert turn_manager.turn_number == 0
        assert turn_manager.current_phase == "input"

    def test_advance_turn(self):
        """Test that advance_turn increments turn number."""
        # Arrange
        turn_manager = TurnManager()
        initial_turn = turn_manager.turn_number

        # Act
        turn_manager.advance_turn()

        # Assert
        assert turn_manager.turn_number == initial_turn + 1

    def test_get_turn_info(self):
        """Test that get_turn_info returns correct information."""
        # Arrange
        turn_manager = TurnManager()
        turn_manager.turn_number = 5

        # Act
        info = turn_manager.get_turn_info()

        # Assert
        assert info["turn_number"] == 5
        assert info["current_phase"] == "input"
        assert "active_entity" in info
        assert "entities_remaining" in info


class TestCombatResult:
    """Test cases for CombatResult dataclass."""

    def test_combat_result_creation(self):
        """Test CombatResult creation with all parameters."""
        # Arrange & Act
        result = CombatResult(True, "Hit successful", 25)

        # Assert
        assert result.success is True
        assert result.message == "Hit successful"
        assert result.damage == 25

    def test_combat_result_default_damage(self):
        """Test CombatResult creation with default damage."""
        # Arrange & Act
        result = CombatResult(False, "Missed target")

        # Assert
        assert result.success is False
        assert result.message == "Missed target"
        assert result.damage == 0


class TestGameModel:
    """Test cases for GameModel class."""

    def test_game_model_initialization(self):
        """Test that GameModel initializes with correct default state."""
        # Arrange & Act
        model = GameModel()

        # Assert
        assert model.galaxy is not None
        assert model.turn_manager is not None
        assert model.mission_manager is not None
        assert model.game_objects == []
        # current_sector and player_ship are initialized in initialize_new_game()
        # Mission manager tracks active missions internally

    def test_initialize_new_game(self, game_model):
        """Test that initialize_new_game sets up game correctly."""
        # Arrange & Act
        game_model.initialize_new_game()

        # Assert
        assert game_model.player_ship is not None
        assert game_model.current_sector is not None
        assert game_model.player_ship in game_model.game_objects
        assert game_model.player_ship.name == "Enterprise"
        assert game_model.player_ship.ship_class == "Constitution"

    def test_execute_move_valid(self, initialized_game_model):
        """Test successful ship movement."""
        # Arrange
        ship = initialized_game_model.player_ship
        initial_position = ship.position
        target_position = GridPosition(
            initial_position.x + 1, initial_position.y, initial_position.z
        )

        # Act
        result = initialized_game_model.execute_move(ship, target_position)

        # Assert
        assert result is True
        assert ship.position == target_position

    def test_execute_move_out_of_bounds(self, initialized_game_model):
        """Test movement to out-of-bounds position fails."""
        # Arrange
        ship = initialized_game_model.player_ship
        out_of_bounds_position = GridPosition(999, 999, 999)

        # Act
        result = initialized_game_model.execute_move(ship, out_of_bounds_position)

        # Assert
        assert result is False

    def test_execute_move_insufficient_fuel(self, initialized_game_model):
        """Test movement with insufficient fuel fails."""
        # Arrange
        ship = initialized_game_model.player_ship
        engines = ship.get_system("engines")
        engines.fuel = 0  # No fuel

        target_position = GridPosition(
            ship.position.x + 1, ship.position.y, ship.position.z
        )

        # Act
        result = initialized_game_model.execute_move(ship, target_position)

        # Assert
        assert result is False

    def test_resolve_combat_successful(self, combat_scenario):
        """Test successful combat resolution."""
        # Arrange
        model = combat_scenario["model"]
        player_ship = combat_scenario["player_ship"]
        enemy_ship = combat_scenario["enemy_ship"]

        # Patch random.random through model's module reference so both the hit
        # roll (must be <= hit_chance to register a hit) and the crit roll are
        # deterministic. 0.0 guarantees a hit; crit is allowed to remain random
        # but we pin it to 0.0 as well to avoid any edge-case interaction.
        with patch("src.game.model.random.random", return_value=0.0):
            # Act
            result = model.resolve_combat(player_ship, enemy_ship, "phaser")

        # Assert
        assert result.success is True
        assert result.damage > 0
        assert "damage" in result.message

    def test_resolve_combat_weapons_offline(self, combat_scenario):
        """Test combat with weapons offline fails."""
        # Arrange
        model = combat_scenario["model"]
        player_ship = combat_scenario["player_ship"]
        enemy_ship = combat_scenario["enemy_ship"]

        # Disable weapons
        weapons = player_ship.get_system("weapons")
        weapons.active = False

        # Act
        result = model.resolve_combat(player_ship, enemy_ship, "phaser")

        # Assert
        assert result.success is False
        assert result.message == "Weapons offline"
        assert result.damage == 0

    def test_save_game_placeholder(self, initialized_game_model):
        """Test save game functionality (placeholder)."""
        # Arrange & Act
        result = initialized_game_model.save_game("/tmp/test_save.json")

        # Assert
        # Currently returns True as placeholder
        assert result is True

    def test_load_game_placeholder(self, initialized_game_model):
        """Test load game functionality (placeholder)."""
        # Arrange & Act
        result = initialized_game_model.load_game("/tmp/test_save.json")

        # Assert
        # Currently returns True as placeholder
        assert result is True

    def test_is_valid_move_with_initialized_sector(self, initialized_game_model):
        """Test move validation with initialized game."""
        # Arrange
        ship = initialized_game_model.player_ship
        destination = GridPosition(7, 7, 1)  # Valid position in default 20x20 sector

        # Act
        result = initialized_game_model._is_valid_move(ship, destination)

        # Assert
        assert result is True  # Should be valid within sector bounds

    def test_create_player_ship(self, game_model):
        """Test player ship creation."""
        # Arrange
        position = GridPosition(5, 5, 1)

        # Act
        ship = game_model._create_player_ship(position)

        # Assert
        assert ship.position == position
        assert ship.ship_class == "Constitution"
        assert ship.name == "Enterprise"
