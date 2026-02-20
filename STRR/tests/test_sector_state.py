#!/usr/bin/env python3
"""
Star Trek Retro Remake - Sector State Tests

Description:
    Unit tests for the sector exploration game state.

Author: Star Trek Retro Remake Development Team
Email: development@star-trek-retro-remake.org
GitHub: https://github.com/L3DigitalNet/Star-Trek-Retro-Remake
Date Created: 10-30-2025
Date Changed: 10-30-2025
License: MIT

Test Coverage:
    - SectorState initialization
    - State lifecycle (enter/exit)
    - State updates and rendering
    - Input event handling

Requirements:
    - pytest >= 8.0.0
    - Python 3.14+
"""
import pytest
pygame = pytest.importorskip("pygame")


from typing import Final
from unittest.mock import MagicMock, Mock

from src.game.states.sector_state import SectorState
from src.game.states.state_machine import GameMode

pytestmark = pytest.mark.gui

__version__: Final[str] = "0.0.18"


@pytest.fixture
def mock_state_manager():
    """Create a mock state manager."""
    return Mock()


@pytest.fixture
def sector_state(mock_state_manager):
    """Create a sector state with mock manager."""
    return SectorState(mock_state_manager)


class TestSectorStateInitialization:
    """Test SectorState initialization."""

    def test_sector_state_initialization(self, mock_state_manager):
        """Test that sector state initializes with correct mode."""
        # Act
        state = SectorState(mock_state_manager)

        # Assert
        assert state.mode == GameMode.SECTOR_MAP
        assert state.state_manager == mock_state_manager

    def test_sector_state_inherits_from_game_state(self, sector_state):
        """Test that sector state inherits from GameState."""
        # Assert
        assert hasattr(sector_state, "enter")
        assert hasattr(sector_state, "exit")
        assert hasattr(sector_state, "update")
        assert hasattr(sector_state, "render")
        assert hasattr(sector_state, "handle_input")


class TestSectorStateLifecycle:
    """Test state lifecycle methods."""

    def test_enter_state_does_not_raise_exception(self, sector_state):
        """Test that entering the state doesn't raise exceptions."""
        # Act & Assert - should not raise
        sector_state.enter()

    def test_exit_state_does_not_raise_exception(self, sector_state):
        """Test that exiting the state doesn't raise exceptions."""
        # Act & Assert - should not raise
        sector_state.exit()


class TestSectorStateUpdate:
    """Test state update functionality."""

    def test_update_with_positive_delta_time(self, sector_state):
        """Test that update handles positive delta time."""
        # Arrange
        dt = 0.016  # ~60 FPS

        # Act & Assert - should not raise
        sector_state.update(dt)

    def test_update_with_zero_delta_time(self, sector_state):
        """Test that update handles zero delta time."""
        # Arrange
        dt = 0.0

        # Act & Assert - should not raise
        sector_state.update(dt)

    def test_update_with_large_delta_time(self, sector_state):
        """Test that update handles large delta time."""
        # Arrange
        dt = 1.0  # 1 second

        # Act & Assert - should not raise
        sector_state.update(dt)


class TestSectorStateRendering:
    """Test state rendering functionality."""

    def test_render_clears_surface_to_space_color(self, sector_state):
        """Test that render fills surface with space background color."""
        # Arrange
        mock_surface = MagicMock(spec=pygame.Surface)

        # Act
        sector_state.render(mock_surface)

        # Assert
        mock_surface.fill.assert_called_once_with((20, 20, 30))

    def test_render_accepts_different_surface_sizes(self, sector_state):
        """Test that render works with different surface dimensions."""
        # Arrange
        mock_surface = MagicMock(spec=pygame.Surface)

        # Act & Assert - should not raise
        sector_state.render(mock_surface)


class TestSectorStateInputHandling:
    """Test input event handling."""

    def test_handle_input_does_not_raise_exception(self, sector_state):
        """Test that handle_input doesn't raise exceptions."""
        # Arrange
        mock_event = Mock(spec=pygame.event.Event)

        # Act & Assert - should not raise
        sector_state.handle_input(mock_event)

    def test_handle_input_with_keydown_event(self, sector_state):
        """Test handling keyboard press events."""
        # Arrange
        mock_event = Mock(spec=pygame.event.Event)
        mock_event.type = pygame.KEYDOWN
        mock_event.key = pygame.K_SPACE

        # Act & Assert - should not raise
        sector_state.handle_input(mock_event)

    def test_handle_input_with_mouse_event(self, sector_state):
        """Test handling mouse button events."""
        # Arrange
        mock_event = Mock(spec=pygame.event.Event)
        mock_event.type = pygame.MOUSEBUTTONDOWN
        mock_event.pos = (100, 100)
        mock_event.button = 1

        # Act & Assert - should not raise
        sector_state.handle_input(mock_event)


class TestSectorStateMode:
    """Test state mode property."""

    def test_sector_state_has_sector_map_mode(self, sector_state):
        """Test that sector state is set to SECTOR_MAP mode."""
        # Assert
        assert sector_state.mode == GameMode.SECTOR_MAP

    def test_sector_state_mode_is_not_main_menu(self, sector_state):
        """Test that sector state is not MAIN_MENU mode."""
        # Assert
        assert sector_state.mode != GameMode.MAIN_MENU

    def test_sector_state_mode_is_not_combat(self, sector_state):
        """Test that sector state is not COMBAT mode."""
        # Assert
        assert sector_state.mode != GameMode.COMBAT


class TestSectorStateIntegration:
    """Test integration scenarios."""

    def test_full_state_lifecycle(self, sector_state):
        """Test complete state lifecycle: enter, update, render, exit."""
        # Arrange
        mock_surface = MagicMock(spec=pygame.Surface)
        dt = 0.016

        # Act - simulate full state usage
        sector_state.enter()
        sector_state.update(dt)
        sector_state.render(mock_surface)
        sector_state.exit()

        # Assert - should complete without exceptions
        mock_surface.fill.assert_called_once()

    def test_multiple_updates_in_sequence(self, sector_state):
        """Test multiple sequential updates."""
        # Arrange
        dt = 0.016

        # Act - simulate multiple game frames
        for _ in range(10):
            sector_state.update(dt)

        # Assert - should not raise exceptions

    def test_multiple_renders_in_sequence(self, sector_state):
        """Test multiple sequential renders."""
        # Arrange
        mock_surface = MagicMock(spec=pygame.Surface)

        # Act - simulate multiple frames
        for _ in range(10):
            sector_state.render(mock_surface)

        # Assert
        assert mock_surface.fill.call_count == 10
