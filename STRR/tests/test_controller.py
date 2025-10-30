#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Star Trek Retro Remake - Controller Tests

Description:
    Unit tests for the game controller, testing MVC coordination,
    input handling, and game state management.

Author: Star Trek Retro Remake Development Team
Email: development@star-trek-retro-remake.org
GitHub: https://github.com/L3DigitalNet/Star-Trek-Retro-Remake
Date Created: 10-30-2025
Date Changed: 10-30-2025
License: MIT

Test Coverage:
    - GameController initialization
    - MVC component coordination
    - Input event handling
    - Ship movement and combat actions
    - Turn management
    - Save/load game functionality

Requirements:
    - pytest >= 8.0.0
    - Python 3.14+
"""

from typing import Final
from unittest.mock import Mock, patch, MagicMock

import pytest
import pygame

from STRR.src.game.controller import GameController
from STRR.src.game.model import GameModel
from STRR.src.game.entities.base import GridPosition
from STRR.src.game.states.state_machine import GameMode

__version__: Final[str] = "0.0.18"


@pytest.fixture
def mock_model():
    """Create a mock game model."""
    model = Mock(spec=GameModel)
    model.player_ship = Mock()
    model.player_ship.position = GridPosition(5, 5, 0)
    model.current_sector = Mock()
    model.current_sector.is_in_bounds.return_value = True
    model.game_objects = []
    return model


@pytest.fixture
def controller(mock_model):
    """Create a controller with a mock model."""
    return GameController(mock_model)


class TestGameControllerInitialization:
    """Test GameController initialization."""

    def test_controller_initialization_with_model(self, mock_model):
        """Test that controller initializes with model reference."""
        # Act
        controller = GameController(mock_model)

        # Assert
        assert controller.model == mock_model
        assert controller.view is None
        assert controller.running is False

    def test_controller_creates_state_manager(self, mock_model):
        """Test that controller creates a state manager."""
        # Act
        controller = GameController(mock_model)

        # Assert
        assert controller.state_manager is not None

    @patch("STRR.src.game.controller.pygame.time.Clock")
    def test_controller_creates_clock(self, mock_clock, mock_model):
        """Test that controller creates a pygame clock."""
        # Act
        controller = GameController(mock_model)

        # Assert
        mock_clock.assert_called_once()


class TestGameControllerViewManagement:
    """Test view management functionality."""

    def test_set_view_assigns_view_reference(self, controller):
        """Test that set_view assigns the view reference."""
        # Arrange
        mock_view = Mock()

        # Act
        controller.set_view(mock_view)

        # Assert
        assert controller.view == mock_view

    def test_controller_starts_in_stopped_state(self, controller):
        """Test that controller starts with running = False."""
        # Assert
        assert controller.running is False

    def test_start_sets_running_to_true(self, controller):
        """Test that start() sets running state to True."""
        # Act
        controller.start()

        # Assert
        assert controller.running is True

    def test_stop_sets_running_to_false(self, controller):
        """Test that stop() sets running state to False."""
        # Arrange
        controller.running = True

        # Act
        controller.stop()

        # Assert
        assert controller.running is False


class TestGameControllerShipMovement:
    """Test ship movement handling."""

    def test_handle_ship_move_request_with_valid_move(self, controller, mock_model):
        """Test handling valid ship movement request."""
        # Arrange
        mock_model.execute_move.return_value = True
        destination = GridPosition(6, 6, 0)
        mock_view = Mock()
        controller.set_view(mock_view)

        # Act
        controller.handle_ship_move_request(destination)

        # Assert
        mock_model.execute_move.assert_called_once_with(
            mock_model.player_ship, destination
        )
        mock_view.render_sector_map.assert_called_once()

    def test_handle_ship_move_request_with_invalid_move(self, controller, mock_model):
        """Test handling invalid ship movement request."""
        # Arrange
        mock_model.execute_move.return_value = False
        destination = GridPosition(100, 100, 0)
        mock_view = Mock()
        controller.set_view(mock_view)

        # Act
        controller.handle_ship_move_request(destination)

        # Assert
        mock_view.show_message.assert_called_once_with("Invalid move")

    def test_handle_ship_move_request_without_player_ship(self, controller, mock_model):
        """Test handling move request when player ship doesn't exist."""
        # Arrange
        mock_model.player_ship = None
        destination = GridPosition(6, 6, 0)

        # Act
        controller.handle_ship_move_request(destination)

        # Assert
        mock_model.execute_move.assert_not_called()


class TestGameControllerCombat:
    """Test combat action handling."""

    def test_handle_combat_action_with_player_ship(self, controller, mock_model):
        """Test handling combat action with valid player ship."""
        # Arrange
        target = Mock()
        mock_result = Mock()
        mock_model.resolve_combat.return_value = mock_result
        mock_view = Mock()
        controller.set_view(mock_view)

        # Act
        controller.handle_combat_action(target, "phaser")

        # Assert
        mock_model.resolve_combat.assert_called_once_with(
            mock_model.player_ship, target, "phaser"
        )
        mock_view.show_combat_dialog.assert_called_once_with(mock_result)

    def test_handle_combat_action_without_player_ship(self, controller, mock_model):
        """Test handling combat action when player ship doesn't exist."""
        # Arrange
        mock_model.player_ship = None
        target = Mock()

        # Act
        controller.handle_combat_action(target, "phaser")

        # Assert
        mock_model.resolve_combat.assert_not_called()


class TestGameControllerGameManagement:
    """Test game initialization and management."""

    def test_start_new_game_initializes_model(self, controller, mock_model):
        """Test that start_new_game initializes the game model."""
        # Act
        controller.start_new_game()

        # Assert
        mock_model.initialize_new_game.assert_called_once()

    def test_start_new_game_transitions_to_sector_map(self, controller):
        """Test that start_new_game transitions to sector map state."""
        # Act
        controller.start_new_game()

        # Assert
        assert controller.state_manager.get_current_mode() == GameMode.SECTOR_MAP

    def test_start_new_game_renders_view(self, controller, mock_model):
        """Test that start_new_game updates the view."""
        # Arrange
        mock_view = Mock()
        mock_model.get_turn_status.return_value = {
            "turn_number": 1,
            "action_points": 10,
            "current_phase": "movement",
        }
        controller.set_view(mock_view)

        # Act
        controller.start_new_game()

        # Assert
        mock_view.render_sector_map.assert_called_once()

    def test_save_game_calls_model_save(self, controller, mock_model):
        """Test that save_game delegates to model."""
        # Arrange
        mock_model.save_game.return_value = True
        filepath = "/tmp/savegame.json"

        # Act
        result = controller.save_game(filepath)

        # Assert
        mock_model.save_game.assert_called_once_with(filepath)
        assert result is True

    def test_load_game_calls_model_load(self, controller, mock_model):
        """Test that load_game delegates to model."""
        # Arrange
        mock_model.load_game.return_value = True
        filepath = "/tmp/savegame.json"

        # Act
        result = controller.load_game(filepath)

        # Assert
        mock_model.load_game.assert_called_once_with(filepath)
        assert result is True

    def test_load_game_updates_view_on_success(self, controller, mock_model):
        """Test that load_game updates view when successful."""
        # Arrange
        mock_model.load_game.return_value = True
        mock_model.get_turn_status.return_value = {
            "turn_number": 1,
            "action_points": 10,
            "current_phase": "movement",
        }
        mock_view = Mock()
        controller.set_view(mock_view)
        filepath = "/tmp/savegame.json"

        # Act
        controller.load_game(filepath)

        # Assert
        mock_view.render_sector_map.assert_called_once()


class TestGameControllerTurnManagement:
    """Test turn management functionality."""

    def test_end_turn_advances_model_turn(self, controller, mock_model):
        """Test that end_turn advances the turn in the model."""
        # Act
        controller.end_turn()

        # Assert
        mock_model.end_current_turn.assert_called_once()

    def test_end_turn_updates_view(self, controller, mock_model):
        """Test that end_turn updates the view."""
        # Arrange
        mock_model.get_turn_status.return_value = {
            "turn_number": 1,
            "action_points": 10,
            "current_phase": "movement",
        }
        mock_view = Mock()
        controller.set_view(mock_view)

        # Act
        controller.end_turn()

        # Assert
        mock_view.render_sector_map.assert_called_once()


class TestGameControllerMouseInput:
    """Test mouse input handling."""

    def test_handle_mouse_click_converts_screen_to_grid(self, controller):
        """Test that mouse clicks are converted to grid positions."""
        # Arrange
        mock_view = Mock()
        mock_view.grid_renderer.screen_to_world.return_value = GridPosition(5, 5, 0)
        mock_view.grid_renderer.is_in_bounds.return_value = True
        mock_view.current_z_level = 0
        controller.set_view(mock_view)
        controller.model.current_sector.is_in_bounds.return_value = True
        controller.model.player_ship = Mock()
        controller.model.execute_move = Mock(return_value=True)
        mouse_pos = (100, 100)

        # Act
        controller.handle_mouse_click(mouse_pos)

        # Assert
        mock_view.grid_renderer.screen_to_world.assert_called_once_with(mouse_pos, 0)

    def test_handle_mouse_click_sets_selected_cell(self, controller):
        """Test that mouse clicks update the selected cell in view."""
        # Arrange
        mock_view = Mock()
        grid_pos = GridPosition(5, 5, 0)
        mock_view.grid_renderer.screen_to_world.return_value = grid_pos
        mock_view.grid_renderer.is_in_bounds.return_value = True
        mock_view.current_z_level = 0
        controller.set_view(mock_view)
        controller.model.current_sector.is_in_bounds.return_value = True
        controller.model.player_ship = Mock()
        controller.model.execute_move = Mock(return_value=True)
        mouse_pos = (100, 100)

        # Act
        controller.handle_mouse_click(mouse_pos)

        # Assert
        mock_view.set_selected_cell.assert_called_once_with(grid_pos)

    def test_handle_mouse_click_without_view_does_nothing(self, controller):
        """Test that mouse clicks without a view don't cause errors."""
        # Arrange
        controller.view = None
        mouse_pos = (100, 100)

        # Act - should not raise exception
        controller.handle_mouse_click(mouse_pos)


class TestGameControllerKeyboardInput:
    """Test keyboard input handling."""

    def test_handle_keypress_pageup_increases_z_level(self, controller):
        """Test that PageUp increases z-level."""
        # Arrange
        mock_view = Mock()
        mock_view.current_z_level = 0
        controller.set_view(mock_view)

        # Act
        controller.handle_keypress(pygame.K_PAGEUP)

        # Assert
        mock_view.set_z_level.assert_called_once_with(1)

    def test_handle_keypress_pagedown_decreases_z_level(self, controller):
        """Test that PageDown decreases z-level."""
        # Arrange
        mock_view = Mock()
        mock_view.current_z_level = 1
        controller.set_view(mock_view)

        # Act
        controller.handle_keypress(pygame.K_PAGEDOWN)

        # Assert
        mock_view.set_z_level.assert_called_once_with(0)

    def test_handle_keypress_plus_zooms_in(self, controller):
        """Test that + key zooms in."""
        # Arrange
        mock_view = Mock()
        controller.set_view(mock_view)

        # Act
        controller.handle_keypress(pygame.K_PLUS)

        # Assert
        mock_view.grid_renderer.zoom_in.assert_called_once()

    def test_handle_keypress_minus_zooms_out(self, controller):
        """Test that - key zooms out."""
        # Arrange
        mock_view = Mock()
        controller.set_view(mock_view)

        # Act
        controller.handle_keypress(pygame.K_MINUS)

        # Assert
        mock_view.grid_renderer.zoom_out.assert_called_once()

    def test_handle_keypress_zero_resets_zoom(self, controller):
        """Test that 0 key resets zoom."""
        # Arrange
        mock_view = Mock()
        controller.set_view(mock_view)

        # Act
        controller.handle_keypress(pygame.K_0)

        # Assert
        mock_view.grid_renderer.reset_zoom.assert_called_once()

    def test_handle_keypress_arrow_keys_pan_camera(self, controller):
        """Test that arrow keys pan the camera."""
        # Arrange
        mock_view = Mock()
        mock_view.grid_renderer.camera_offset = (0, 0)
        controller.set_view(mock_view)

        # Act
        controller.handle_keypress(pygame.K_LEFT)

        # Assert
        mock_view.grid_renderer.set_camera_offset.assert_called_once_with((10, 0))

    def test_handle_keypress_without_view_does_nothing(self, controller):
        """Test that keypresses without a view don't cause errors."""
        # Arrange
        controller.view = None

        # Act - should not raise exception
        controller.handle_keypress(pygame.K_SPACE)
