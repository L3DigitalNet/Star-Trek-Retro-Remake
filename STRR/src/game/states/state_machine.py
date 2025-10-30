#!/usr/bin/env python3
"""
Star Trek Retro Remake - State Machine

Description:
    Core game state machine implementing state management and transitions
    between different game modes.

Author: Star Trek Retro Remake Development Team
Email: development@star-trek-retro-remake.org
GitHub: https://github.com/L3DigitalNet/Star-Trek-Retro-Remake
Date Created: 10-29-2025
Date Changed: 10-30-2025
License: MIT

Features:
    - State machine for game mode transitions
    - Clean state boundaries and responsibilities
    - State persistence and validation
    - Event-driven state changes

Requirements:
    - Linux environment
    - Python 3.14+ for latest language features

Classes:
    - GameMode: Enumeration of available game modes
    - GameState: Base class for all game states
    - GameStateManager: State transition management

Functions:
    - None
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import TYPE_CHECKING, Dict, Final, Optional

if TYPE_CHECKING:
    import pygame

__version__: Final[str] = "0.0.1"


class GameMode(Enum):
    """
    Enumeration of available game modes.

    Defines all possible states the game can be in and provides
    a clear interface for state transitions.
    """

    MAIN_MENU = "main_menu"
    GALAXY_MAP = "galaxy_map"
    SECTOR_MAP = "sector_map"
    COMBAT = "combat"
    SETTINGS = "settings"
    PAUSED = "paused"


class GameState(ABC):
    """
    Base class for all game states.

    Implements the State pattern interface providing consistent
    behavior across all game modes.

    Attributes:
        state_manager: Reference to the state manager
        mode: Game mode identifier for this state

    Public methods:
        enter: Called when entering this state
        exit: Called when leaving this state
        handle_input: Process input events
        update: Update game logic with delta time
        render: Render state-specific content

    Private methods:
        None
    """

    def __init__(self, state_manager: "GameStateManager"):
        """
        Initialize the game state.

        Args:
            state_manager: Reference to the state manager
        """
        self.state_manager = state_manager
        self.mode: Optional[GameMode] = None  # Set by subclasses

    @abstractmethod
    def enter(self) -> None:
        """Called when entering this state."""
        pass

    @abstractmethod
    def exit(self) -> None:
        """Called when leaving this state."""
        pass

    @abstractmethod
    def handle_input(self, event: "pygame.event.Event") -> None:
        """
        Process input events.

        Args:
            event: PyGame event to process
        """
        pass

    @abstractmethod
    def update(self, dt: float) -> None:
        """
        Update game logic with delta time.

        Args:
            dt: Time elapsed since last update in seconds
        """
        pass

    @abstractmethod
    def render(self, surface: "pygame.Surface") -> None:
        """
        Render state-specific content.

        Args:
            surface: PyGame surface to render to
        """
        pass


class GameStateManager:
    """
    Manages state transitions and current state.

    Coordinates state changes, validation, and maintains
    the current game state throughout the application lifecycle.

    Attributes:
        current_state: Currently active game state
        previous_state: Previously active state for rollback
        states: Registry of available states by mode

    Public methods:
        register_state: Register a state for a specific mode
        transition_to: Transition to a new state
        update: Update current state
        render: Render current state
        get_current_mode: Get current game mode

    Private methods:
        _validate_transition: Validate state transition is legal
    """

    def __init__(self):
        """Initialize the game state manager."""
        self.current_state: Optional[GameState] = None
        self.previous_state: Optional[GameState] = None
        self.states: Dict[GameMode, GameState] = {}

    def register_state(self, mode: GameMode, state: GameState) -> None:
        """
        Register a state for a specific mode.

        Args:
            mode: Game mode identifier
            state: State instance to register
        """
        self.states[mode] = state
        state.mode = mode

    def transition_to(self, mode: GameMode) -> None:
        """
        Transition to a new state.

        Args:
            mode: Target game mode to transition to

        Raises:
            ValueError: If the target mode is not registered
        """
        if mode not in self.states:
            raise ValueError(f"Unknown game mode: {mode}")

        # Validate transition is legal
        if not self._validate_transition(mode):
            return

        # Exit current state
        if self.current_state:
            self.current_state.exit()
            self.previous_state = self.current_state

        # Enter new state
        self.current_state = self.states[mode]
        self.current_state.enter()

    def update(self, dt: float) -> None:
        """
        Update current state.

        Args:
            dt: Time elapsed since last update in seconds
        """
        if self.current_state:
            self.current_state.update(dt)

    def render(self, surface: "pygame.Surface") -> None:
        """
        Render current state.

        Args:
            surface: PyGame surface to render to
        """
        if self.current_state:
            self.current_state.render(surface)

    def handle_input(self, event: "pygame.event.Event") -> None:
        """
        Process input events for current state.

        Args:
            event: PyGame event to process
        """
        if self.current_state:
            self.current_state.handle_input(event)

    def get_current_mode(self) -> Optional[GameMode]:
        """
        Get current game mode.

        Returns:
            Current game mode or None if no state is active
        """
        return self.current_state.mode if self.current_state else None

    def _validate_transition(self, target_mode: GameMode) -> bool:
        """
        Validate state transition is legal.

        Args:
            target_mode: Target mode to transition to

        Returns:
            True if transition is allowed, False otherwise
        """
        # For now, all transitions are allowed
        # This can be expanded with transition rules later
        return True
