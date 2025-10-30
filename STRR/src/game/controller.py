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
Date Changed: 10-30-2025 (v0.0.9 - Bug fixes)
License: MIT

Features:
    - MVC pattern controller coordination
    - Input handling and event processing
    - Game state management and transitions
    - Command processing and validation

Requirements:
    - Linux environment
    - Python 3.14+ for latest language features
    - pygame-ce (Community Edition) for event handling

Classes:
    - GameController: Main controller coordinating model and view

Functions:
    - None
"""

from typing import Final, TYPE_CHECKING
import logging

import pygame

from .states.state_machine import GameStateManager, GameMode
from .states.sector_state import SectorState
from .entities.base import GridPosition

if TYPE_CHECKING:
    from .model import GameModel
    from .view import GameView
    from .entities.starship import Starship

__version__: Final[str] = "0.0.10"

logger = logging.getLogger(__name__)


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
        clock: pygame-ce clock for timing

    Public methods:
        set_view: Set the view reference
        start: Start the controller and game loop
        stop: Stop the controller
        handle_ship_move_request: Process ship movement
        handle_combat_action: Process combat actions
        start_new_game: Initialize a new game

    Private methods:
        _setup_states: Initialize game states
        _handle_events: Process pygame-ce events
        _update: Update game logic
        _render: Render game display
    """

    def __init__(self, model: "GameModel"):
        """
        Initialize the game controller.

        Args:
            model: Game model reference
        """
        self.model = model
        self.view: "GameView" | None = None

        # Initialize game state management
        self.state_manager = GameStateManager()
        self._setup_states()

        # Controller state
        self.running = False
        self.clock = pygame.time.Clock()

    def set_view(self, view: "GameView") -> None:
        """
        Set the view reference.

        Args:
            view: Game view instance
        """
        self.view = view

    def start(self) -> None:
        """Start the controller."""
        self.running = True

        # Initialize with main menu state
        # self.state_manager.transition_to(GameMode.MAIN_MENU)

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
                self.model.current_sector, self.model.game_objects
            )

    def handle_combat_action(self, target: "Starship", weapon_type: str) -> None:
        """
        Handle combat action request.

        Args:
            target: Target starship
            weapon_type: Type of weapon to use
        """
        if not self.model.player_ship:
            return

        # Resolve combat through model
        result = self.model.resolve_combat(self.model.player_ship, target, weapon_type)

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
                self.model.current_sector, self.model.game_objects
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
                self.model.current_sector, self.model.game_objects
            )

        return success

    def _setup_states(self) -> None:
        """Initialize game states."""
        # Register sector exploration state
        sector_state = SectorState(self.state_manager)
        self.state_manager.register_state(GameMode.SECTOR_MAP, sector_state)

    # Note: _game_loop() and _handle_events() removed
    # Events are now handled exclusively through Qt widgets (GameDisplay)
    # Qt events are forwarded to handle_mouse_click() and handle_keypress()

    def handle_mouse_click(self, mouse_pos: tuple[int, int]) -> None:
        """
        Handle mouse click events for grid interaction.

        Args:
            mouse_pos: Mouse position (x, y) in screen coordinates
        """
        if not self.view:
            return

        logger.debug(f"Processing mouse click at screen position: {mouse_pos}")

        # Convert screen coordinates to grid position
        grid_pos = self.view.grid_renderer.screen_to_world(
            mouse_pos, self.view.current_z_level
        )

        logger.debug(f"Converted to grid position: {grid_pos}")

        # Validate grid position is within renderer bounds
        if not self.view.grid_renderer.is_in_bounds(grid_pos):
            logger.warning(f"Grid position {grid_pos} is out of renderer bounds")
            return

        # Additional validation: check if position is within sector map bounds
        if self.model.current_sector and not self.model.current_sector.is_in_bounds(
            grid_pos
        ):
            logger.warning(f"Grid position {grid_pos} is out of sector bounds")
            return

        # Update view selection
        self.view.set_selected_cell(grid_pos)

        # Attempt to move player ship to clicked position
        if self.model.player_ship:
            logger.debug(f"Attempting to move ship to {grid_pos}")
            self.handle_ship_move_request(grid_pos)

    def handle_keypress(self, key: int) -> None:
        """
        Handle keyboard input.

        Args:
            key: pygame key constant
        """
        if not self.view:
            return

        logger.debug(f"Processing key press: {key}")

        # Z-level controls (validation is centralized in set_z_level)
        if key == pygame.K_PAGEUP:
            self.view.set_z_level(self.view.current_z_level + 1)
        elif key == pygame.K_PAGEDOWN:
            self.view.set_z_level(self.view.current_z_level - 1)

        # Zoom controls
        elif key in (pygame.K_PLUS, pygame.K_EQUALS):
            logger.debug("Zooming in")
            self.view.grid_renderer.zoom_in()
        elif key == pygame.K_MINUS:
            logger.debug("Zooming out")
            self.view.grid_renderer.zoom_out()
        elif key == pygame.K_0:
            logger.debug("Resetting zoom")
            self.view.grid_renderer.reset_zoom()

        # Camera panning
        elif key == pygame.K_LEFT:
            logger.debug("Panning camera left")
            self._pan_camera(10, 0)
        elif key == pygame.K_RIGHT:
            logger.debug("Panning camera right")
            self._pan_camera(-10, 0)
        elif key == pygame.K_UP:
            logger.debug("Panning camera up")
            self._pan_camera(0, 10)
        elif key == pygame.K_DOWN:
            logger.debug("Panning camera down")
            self._pan_camera(0, -10)

    def _pan_camera(self, dx: int, dy: int) -> None:
        """
        Pan the camera by the specified offset.

        Args:
            dx: X offset in pixels
            dy: Y offset in pixels
        """
        if not self.view:
            return

        offset = self.view.grid_renderer.camera_offset
        new_offset = (offset[0] + dx, offset[1] + dy)
        self.view.grid_renderer.set_camera_offset(new_offset)

    def _update(self, dt: float) -> None:
        """
        Update game logic.

        Args:
            dt: Time delta since last update in seconds
        """
        # Update current state
        self.state_manager.update(dt)
