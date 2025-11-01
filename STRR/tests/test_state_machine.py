#!/usr/bin/env python3
"""
Star Trek Retro Remake - State Machine Tests

Description:
    Unit tests for game state machine, state management, transitions,
    and state-specific behavior.

Author: Star Trek Retro Remake Development Team
Date Created: 10-30-2025
Date Changed: 10-30-2025
License: MIT
"""

from typing import Final
from unittest.mock import Mock

import pygame
from src.game.states.state_machine import (
    GameMode,
    GameState,
    GameStateManager,
)

__version__: Final[str] = "0.0.11"


# Concrete test state implementations
class MockGameState(GameState):
    """Concrete mock state for testing."""

    def __init__(self, state_manager):
        super().__init__(state_manager)
        self.entered = False
        self.exited = False
        self.updated = False
        self.rendered = False
        self.input_handled = False

    def enter(self) -> None:
        self.entered = True

    def exit(self) -> None:
        self.exited = True

    def handle_input(self, event: pygame.event.Event) -> None:
        self.input_handled = True

    def update(self, dt: float) -> None:
        self.updated = True

    def render(self, surface: pygame.Surface) -> None:
        self.rendered = True


class TestGameMode:
    """Test cases for GameMode enumeration."""

    def test_all_game_modes_exist(self):
        """Test that all expected game modes are defined."""
        # Arrange & Act & Assert
        assert GameMode.MAIN_MENU
        assert GameMode.GALAXY_MAP
        assert GameMode.SECTOR_MAP
        assert GameMode.COMBAT
        assert GameMode.SETTINGS
        assert GameMode.PAUSED

    def test_game_mode_values(self):
        """Test that game modes have correct string values."""
        # Arrange & Act & Assert
        assert GameMode.MAIN_MENU.value == "main_menu"
        assert GameMode.GALAXY_MAP.value == "galaxy_map"
        assert GameMode.SECTOR_MAP.value == "sector_map"
        assert GameMode.COMBAT.value == "combat"
        assert GameMode.SETTINGS.value == "settings"
        assert GameMode.PAUSED.value == "paused"

    def test_game_mode_uniqueness(self):
        """Test that all game modes are unique."""
        # Arrange
        modes = [
            GameMode.MAIN_MENU,
            GameMode.GALAXY_MAP,
            GameMode.SECTOR_MAP,
            GameMode.COMBAT,
            GameMode.SETTINGS,
            GameMode.PAUSED,
        ]

        # Act
        unique_modes = set(modes)

        # Assert
        assert len(unique_modes) == len(modes)


class TestGameState:
    """Test cases for GameState base class."""

    def test_state_initialization(self):
        """Test that game state initializes correctly."""
        # Arrange
        manager = Mock()

        # Act
        state = MockGameState(manager)

        # Assert
        assert state.state_manager == manager
        assert state.mode is None

    def test_state_enter(self):
        """Test state enter method."""
        # Arrange
        manager = Mock()
        state = MockGameState(manager)

        # Act
        state.enter()

        # Assert
        assert state.entered is True

    def test_state_exit(self):
        """Test state exit method."""
        # Arrange
        manager = Mock()
        state = MockGameState(manager)

        # Act
        state.exit()

        # Assert
        assert state.exited is True

    def test_state_update(self):
        """Test state update method."""
        # Arrange
        manager = Mock()
        state = MockGameState(manager)

        # Act
        state.update(0.016)

        # Assert
        assert state.updated is True

    def test_state_render(self):
        """Test state render method."""
        # Arrange
        pygame.init()
        manager = Mock()
        state = MockGameState(manager)
        surface = pygame.Surface((800, 600))

        # Act
        state.render(surface)

        # Assert
        assert state.rendered is True

    def test_state_handle_input(self):
        """Test state input handling."""
        # Arrange
        pygame.init()
        manager = Mock()
        state = MockGameState(manager)
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)

        # Act
        state.handle_input(event)

        # Assert
        assert state.input_handled is True


class TestGameStateManager:
    """Test cases for GameStateManager."""

    def test_state_manager_initialization(self):
        """Test that state manager initializes correctly."""
        # Arrange & Act
        manager = GameStateManager()

        # Assert
        assert manager.current_state is None
        assert manager.previous_state is None
        assert manager.states == {}

    def test_register_state(self):
        """Test registering a state."""
        # Arrange
        manager = GameStateManager()
        state = MockGameState(manager)

        # Act
        manager.register_state(GameMode.MAIN_MENU, state)

        # Assert
        assert GameMode.MAIN_MENU in manager.states
        assert manager.states[GameMode.MAIN_MENU] == state
        assert state.mode == GameMode.MAIN_MENU

    def test_register_multiple_states(self):
        """Test registering multiple states."""
        # Arrange
        manager = GameStateManager()
        menu_state = MockGameState(manager)
        game_state = MockGameState(manager)

        # Act
        manager.register_state(GameMode.MAIN_MENU, menu_state)
        manager.register_state(GameMode.GALAXY_MAP, game_state)

        # Assert
        assert len(manager.states) == 2
        assert manager.states[GameMode.MAIN_MENU] == menu_state
        assert manager.states[GameMode.GALAXY_MAP] == game_state

    def test_transition_to_state(self):
        """Test transitioning to a new state."""
        # Arrange
        manager = GameStateManager()
        state = MockGameState(manager)
        manager.register_state(GameMode.MAIN_MENU, state)

        # Act
        manager.transition_to(GameMode.MAIN_MENU)

        # Assert
        assert manager.current_state == state
        assert state.entered is True

    def test_transition_calls_exit_on_previous_state(self):
        """Test that transitioning exits the previous state."""
        # Arrange
        manager = GameStateManager()
        menu_state = MockGameState(manager)
        game_state = MockGameState(manager)
        manager.register_state(GameMode.MAIN_MENU, menu_state)
        manager.register_state(GameMode.GALAXY_MAP, game_state)

        manager.transition_to(GameMode.MAIN_MENU)

        # Act
        manager.transition_to(GameMode.GALAXY_MAP)

        # Assert
        assert menu_state.exited is True
        assert game_state.entered is True
        assert manager.previous_state == menu_state
        assert manager.current_state == game_state

    def test_transition_to_unregistered_state_raises_error(self):
        """Test that transitioning to unregistered state raises ValueError."""
        # Arrange
        manager = GameStateManager()

        # Act & Assert
        try:
            manager.transition_to(GameMode.MAIN_MENU)
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "Unknown game mode" in str(e)

    def test_update_current_state(self):
        """Test updating the current state."""
        # Arrange
        manager = GameStateManager()
        state = MockGameState(manager)
        manager.register_state(GameMode.MAIN_MENU, state)
        manager.transition_to(GameMode.MAIN_MENU)

        # Act
        manager.update(0.016)

        # Assert
        assert state.updated is True

    def test_update_with_no_current_state(self):
        """Test updating with no current state doesn't crash."""
        # Arrange
        manager = GameStateManager()

        # Act
        manager.update(0.016)  # Should not raise exception

        # Assert - If we get here, test passes

    def test_render_current_state(self):
        """Test rendering the current state."""
        # Arrange
        pygame.init()
        manager = GameStateManager()
        state = MockGameState(manager)
        manager.register_state(GameMode.MAIN_MENU, state)
        manager.transition_to(GameMode.MAIN_MENU)
        surface = pygame.Surface((800, 600))

        # Act
        manager.render(surface)

        # Assert
        assert state.rendered is True

    def test_render_with_no_current_state(self):
        """Test rendering with no current state doesn't crash."""
        # Arrange
        pygame.init()
        manager = GameStateManager()
        surface = pygame.Surface((800, 600))

        # Act
        manager.render(surface)  # Should not raise exception

        # Assert - If we get here, test passes

    def test_handle_input_current_state(self):
        """Test handling input for current state."""
        # Arrange
        pygame.init()
        manager = GameStateManager()
        state = MockGameState(manager)
        manager.register_state(GameMode.MAIN_MENU, state)
        manager.transition_to(GameMode.MAIN_MENU)
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)

        # Act
        manager.handle_input(event)

        # Assert
        assert state.input_handled is True

    def test_handle_input_with_no_current_state(self):
        """Test handling input with no current state doesn't crash."""
        # Arrange
        pygame.init()
        manager = GameStateManager()
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)

        # Act
        manager.handle_input(event)  # Should not raise exception

        # Assert - If we get here, test passes

    def test_get_current_mode(self):
        """Test getting current game mode."""
        # Arrange
        manager = GameStateManager()
        state = MockGameState(manager)
        manager.register_state(GameMode.MAIN_MENU, state)
        manager.transition_to(GameMode.MAIN_MENU)

        # Act
        current_mode = manager.get_current_mode()

        # Assert
        assert current_mode == GameMode.MAIN_MENU

    def test_get_current_mode_with_no_state(self):
        """Test getting current mode with no active state."""
        # Arrange
        manager = GameStateManager()

        # Act
        current_mode = manager.get_current_mode()

        # Assert
        assert current_mode is None

    def test_validate_transition(self):
        """Test transition validation."""
        # Arrange
        manager = GameStateManager()
        state = MockGameState(manager)
        manager.register_state(GameMode.MAIN_MENU, state)

        # Act
        result = manager._validate_transition(GameMode.MAIN_MENU)

        # Assert
        assert result is True  # All transitions allowed by default

    def test_multiple_transitions(self):
        """Test multiple state transitions."""
        # Arrange
        manager = GameStateManager()
        menu_state = MockGameState(manager)
        galaxy_state = MockGameState(manager)
        sector_state = MockGameState(manager)

        manager.register_state(GameMode.MAIN_MENU, menu_state)
        manager.register_state(GameMode.GALAXY_MAP, galaxy_state)
        manager.register_state(GameMode.SECTOR_MAP, sector_state)

        # Act
        manager.transition_to(GameMode.MAIN_MENU)
        manager.transition_to(GameMode.GALAXY_MAP)
        manager.transition_to(GameMode.SECTOR_MAP)

        # Assert
        assert manager.current_state == sector_state
        assert manager.previous_state == galaxy_state
        assert menu_state.exited is True
        assert galaxy_state.exited is True
        assert sector_state.entered is True


class TestStateTransitions:
    """Integration tests for state transitions."""

    def test_transition_chain(self):
        """Test a chain of state transitions."""
        # Arrange
        manager = GameStateManager()
        states = {
            GameMode.MAIN_MENU: MockGameState(manager),
            GameMode.GALAXY_MAP: MockGameState(manager),
            GameMode.SECTOR_MAP: MockGameState(manager),
            GameMode.COMBAT: MockGameState(manager),
        }

        for mode, state in states.items():
            manager.register_state(mode, state)

        # Act - Simulate game flow
        manager.transition_to(GameMode.MAIN_MENU)
        manager.transition_to(GameMode.GALAXY_MAP)
        manager.transition_to(GameMode.SECTOR_MAP)
        manager.transition_to(GameMode.COMBAT)

        # Assert
        assert manager.current_state == states[GameMode.COMBAT]
        assert states[GameMode.MAIN_MENU].entered is True
        assert states[GameMode.MAIN_MENU].exited is True
        assert states[GameMode.COMBAT].entered is True

    def test_pause_and_resume(self):
        """Test pausing and resuming game state."""
        # Arrange
        manager = GameStateManager()
        game_state = MockGameState(manager)
        pause_state = MockGameState(manager)

        manager.register_state(GameMode.GALAXY_MAP, game_state)
        manager.register_state(GameMode.PAUSED, pause_state)

        manager.transition_to(GameMode.GALAXY_MAP)

        # Act - Pause
        manager.transition_to(GameMode.PAUSED)

        # Assert
        assert manager.current_state == pause_state
        assert manager.previous_state == game_state
        assert game_state.exited is True
        assert pause_state.entered is True

    def test_settings_from_any_state(self):
        """Test accessing settings from any state."""
        # Arrange
        manager = GameStateManager()
        game_state = MockGameState(manager)
        settings_state = MockGameState(manager)

        manager.register_state(GameMode.GALAXY_MAP, game_state)
        manager.register_state(GameMode.SETTINGS, settings_state)

        manager.transition_to(GameMode.GALAXY_MAP)

        # Act
        manager.transition_to(GameMode.SETTINGS)

        # Assert
        assert manager.current_state == settings_state
        assert manager.previous_state == game_state
