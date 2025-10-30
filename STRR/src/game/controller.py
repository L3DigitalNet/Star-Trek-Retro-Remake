#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Star Trek Retro Remake - Game Controller

Description:
    Game controller implementing the Controller component of the MVC pattern.
    Coordinates between model and view, handles input, and manages game flow.

Author: Star Trek Retro Remake Development Team
Email: development@star-trek-retro-remake.org
GitHub: https://github.com/L3DigitalNet/Star-Trek-Retro-Remake
Date Created: 10-29-2025
Date Changed: 10-30-2025
License: MIT

Features:
    - MVC pattern controller coordination
    - Input handling and event processing
    - Game state management and transitions
    - Command processing and validation

Requirements:
    - Linux environment
    - Python 3.14+ for latest language features
    - PyGame for event handling

Classes:
    - GameController: Main controller coordinating model and view

Functions:
    - None
"""

from typing import Final, Optional, TYPE_CHECKING

import pygame

from .states.state_machine import GameStateManager, GameMode
from .entities.base import GridPosition

if TYPE_CHECKING:
    from .model import GameModel
    from .view import GameView
    from .entities.starship import Starship

__version__: Final[str] = "0.0.1"


class GameController:
    """
    Main controller coordinating model and view.

    Implements the Controller component of the MVC pattern,
    handling input events, coordinating between model and view,
    and managing overall game flow.

    Attributes:
        model: Game model containing logic and state
        view: Game view handling UI and rendering
        state_manager: Game state machine manager
        running: Whether the controller is active
        clock: PyGame clock for timing

    Public methods:
        set_view: Set the view reference
        start: Start the controller and game loop
        stop: Stop the controller
        handle_ship_move_request: Process ship movement
        handle_combat_action: Process combat actions
        start_new_game: Initialize a new game

    Private methods:
        _setup_states: Initialize game states
        _handle_events: Process PyGame events
        _update: Update game logic
        _render: Render game display
    """

    def __init__(self, model: 'GameModel'):
        """
        Initialize the game controller.

        Args:
            model: Game model reference
        """
        self.model = model
        self.view: Optional['GameView'] = None

        # Initialize game state management
        self.state_manager = GameStateManager()
        self._setup_states()

        # Controller state
        self.running = False
        self.clock = pygame.time.Clock()

    def set_view(self, view: 'GameView') -> None:
        """
        Set the view reference.

        Args:
            view: Game view instance
        """
        self.view = view

    def start(self) -> None:
        """Start the controller and game loop."""
        self.running = True

        # Initialize with main menu state
        # self.state_manager.transition_to(GameMode.MAIN_MENU)

        # For now, start directly with a new game
        self.start_new_game()

        # Start the game loop
        self._game_loop()

    def stop(self) -> None:
        """Stop the controller."""
        self.running = False

    def handle_ship_move_request(self, destination: GridPosition) -> None:
        """
        Handle player ship movement request.

        Args:
            destination: Target position for movement
        """
        if not self.model.player_ship:
            return

        # Execute movement through model
        success = self.model.execute_move(self.model.player_ship, destination)

        if not success and self.view:
            self.view.show_message("Invalid move")
        elif self.view:
            # Update view with new state
            self.view.render_sector_map(
                self.model.current_sector,
                self.model.game_objects
            )

    def handle_combat_action(self, target: 'Starship', weapon_type: str) -> None:
        """
        Handle combat action request.

        Args:
            target: Target starship
            weapon_type: Type of weapon to use
        """
        if not self.model.player_ship:
            return

        # Resolve combat through model
        result = self.model.resolve_combat(
            self.model.player_ship, target, weapon_type
        )

        # Display result through view
        if self.view:
            self.view.show_combat_dialog(result)

    def start_new_game(self) -> None:
        """Initialize and start a new game."""
        # Initialize game model
        self.model.initialize_new_game()

        # Transition to sector map state
        self.state_manager.transition_to(GameMode.SECTOR_MAP)

        # Update view if available
        if self.view:
            self.view.render_sector_map(
                self.model.current_sector,
                self.model.game_objects
            )

    def save_game(self, filepath: str) -> bool:
        """
        Save the current game state.

        Args:
            filepath: Path to save the game to

        Returns:
            True if save was successful, False otherwise
        """
        return self.model.save_game(filepath)

    def load_game(self, filepath: str) -> bool:
        """
        Load a saved game state.

        Args:
            filepath: Path to load the game from

        Returns:
            True if load was successful, False otherwise
        """
        success = self.model.load_game(filepath)

        # Update view if load was successful
        if success and self.view:
            self.view.render_sector_map(
                self.model.current_sector,
                self.model.game_objects
            )

        return success

    def _setup_states(self) -> None:
        """Initialize game states."""
        # States will be registered here when implemented
        # For now, create placeholder registrations
        pass

    def _game_loop(self) -> None:
        """Main game loop."""
        while self.running:
            # Calculate delta time
            dt = self.clock.tick(60) / 1000.0  # Convert to seconds

            # Process events
            self._handle_events()

            # Update game logic
            self._update(dt)

            # Render display
            self._render()

    def _handle_events(self) -> None:
        """Process PyGame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            else:
                # Pass events to current state
                self.state_manager.handle_input(event)

    def _update(self, dt: float) -> None:
        """
        Update game logic.

        Args:
            dt: Time delta since last update in seconds
        """
        # Update current state
        self.state_manager.update(dt)

    def _render(self) -> None:
        """Render game display."""
        if self.view:
            # Render current state
            self.state_manager.render(self.view.game_surface)

            # Update display
            pygame.display.flip()