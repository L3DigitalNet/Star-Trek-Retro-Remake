#!/usr/bin/env python3
"""
Star Trek Retro Remake - Game Controller

Description:
    Game controller implementing the Controller component of the MVC pattern.
    Coordinates between model and view, handles input, and manages game flow.

Author: Star Trek Retro Remake Development Team
Email: development@star-trek-retro-remake.org
GitHub: https://github.com/L3DigitalNet/Star-Trek-Retro-Remake
Date Created: 10-29-2025
Date Changed: 10-31-2025 (v0.0.26 - Added mission system coordination methods)
License: MIT

Features:
    - MVC pattern controller coordination
    - Input handling and event processing
    - Game state management and transitions
    - Command processing and validation
    - Combat action coordination with targeting
    - Target selection and weapon firing
    - Mission system coordination and dialog management

Requirements:
    - Linux environment
    - Python 3.14+ for latest language features
    - pygame-ce (Community Edition) for event handling

Classes:
    - GameController: Main controller coordinating model and view

Functions:
    - None
"""

import logging
from typing import TYPE_CHECKING, Final

import pygame

from .entities.base import GridPosition
from .states.sector_state import SectorState
from .states.state_machine import GameMode, GameStateManager

if TYPE_CHECKING:
    from .components.mission_manager import Mission
    from .entities.starship import Starship
    from .model import GameModel
    from .view import GameView

__version__: Final[str] = "0.0.26"

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

    def __init__(self, model: GameModel):
        """
        Initialize the game controller.

        Args:
            model: Game model reference
        """
        self.model = model
        self.view: GameView | None = None

        # Initialize game state management
        self.state_manager = GameStateManager()
        self._setup_states()

        # Controller state
        self.running = False
        self.clock = pygame.time.Clock()

    def set_view(self, view: GameView) -> None:
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
        # Execute movement through model - player_ship guaranteed to exist during gameplay
        success = self.model.execute_move(self.model.player_ship, destination)

        if not success and self.view:
            self.view.show_message("Invalid move")
        elif self.view:
            # Update view with new state
            self.view.render_sector_map(
                self.model.current_sector, self.model.game_objects
            )
            # Update UI elements (ship status, position, etc.)
            self.view.update_ui_state()
            # Update turn display
            self._update_turn_display()

    def handle_combat_action(self, target: Starship, weapon_type: str) -> None:
        """
        Handle combat action from player.

        Args:
            target: Target starship
            weapon_type: Type of weapon to use (phaser or torpedo)
        """
        # Resolve combat through model - player_ship guaranteed to exist during gameplay
        result = self.model.resolve_combat(self.model.player_ship, target, weapon_type)

        # Display result through view
        if self.view:
            if result.success:
                self.view.show_message(result.message)
                # Update view after combat
                self.view.render_sector_map(
                    self.model.current_sector, self.model.game_objects
                )
                self.view.update_ui_state()
                self._update_turn_display()
            else:
                self.view.show_message(f"Attack failed: {result.message}")

    def get_available_targets(self, weapon_type: str = "phaser") -> list[Starship]:
        """
        Get list of valid targets for the player ship.

        Args:
            weapon_type: Type of weapon to consider for range

        Returns:
            List of targetable enemy ships
        """
        # player_ship guaranteed to exist during gameplay
        return self.model.get_potential_targets(self.model.player_ship, weapon_type)

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
            # Update all UI elements
            self.view.update_ui_state()
            # Update turn information display
            self._update_turn_display()

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
            # Update all UI elements
            self.view.update_ui_state()
            # Update turn information display
            self._update_turn_display()

        return success

    def end_turn(self) -> None:
        """
        End the current entity's turn and advance to next.

        Processes AI turns for NPCs and updates the view.
        """

        self.model.end_current_turn()

        # Process AI turns until it's player's turn again
        self._process_ai_turns()

        # Update view with new turn information
        if self.view:
            self.view.render_sector_map(
                self.model.current_sector, self.model.game_objects
            )
            # Update all UI elements
            self.view.update_ui_state()
            # Update turn information display
            self._update_turn_display()

    def _process_ai_turns(self) -> None:
        """
        Process AI turns until it's the player's turn.

        Runs AI logic for all NPC ships in turn order.
        """
        # Get current entity from turn manager
        current_entity = self.model.turn_manager.get_current_entity()

        # Keep processing AI turns until player's turn
        # Safety limit scales with total entity count
        total_entities = len(self.model.turn_manager.entities)
        max_ai_turns = max(20, total_entities * 2)  # At least 20, or 2x entity count
        turns_processed = 0

        while current_entity and isinstance(current_entity, Starship):
            # Stop if it's the player's turn
            if current_entity.is_player:
                break

            # Stop if safety limit reached (prevents infinite loops)
            if turns_processed >= max_ai_turns:
                logger.warning(f"AI turn limit reached ({max_ai_turns}), breaking loop")
                break

            # Process AI turn if ship has AI controller
            if current_entity.ai_controller:
                self.model.process_ai_turn(current_entity)

            # Advance to next entity
            self.model.turn_manager.next_entity()
            current_entity = self.model.turn_manager.get_current_entity()
            turns_processed += 1

    def switch_to_galaxy_mode(self) -> None:
        """
        Switch to Galaxy Map mode.

        Transitions the game state to galaxy-level strategic view.
        """
        logger.info("Switching to Galaxy Map mode")
        # TODO: Implement galaxy map state and rendering (future milestone)
        if self.view:
            self.view.show_message("Galaxy Map not yet implemented")

    def switch_to_sector_mode(self) -> None:
        """
        Switch to Sector Map mode.

        Transitions the game state to sector-level tactical view.
        """
        logger.info("Switching to Sector Map mode")
        self.state_manager.transition_to(GameMode.SECTOR_MAP)
        if self.view:
            self.view.render_sector_map(
                self.model.current_sector, self.model.game_objects
            )

    def switch_to_combat_mode(self) -> None:
        """
        Switch to Combat mode.

        Transitions the game state to combat-focused view.
        """
        logger.info("Switching to Combat mode")
        # TODO: Implement combat mode state and rendering (next milestone)
        if self.view:
            self.view.show_message("Combat Mode not yet implemented")

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

        # If move mode is active, attempt to move player ship
        if self.view.move_mode and self.model.player_ship:
            logger.debug(f"Move mode: Attempting to move ship to {grid_pos}")
            self.handle_ship_move_request(grid_pos)
            # Deactivate move mode after successful click
            self.view.move_mode = False
            self.view.move_btn.setText("Move Ship")
            self.view.show_message(f"Moving to position {grid_pos}")

    def handle_keypress(self, key: int) -> None:
        """
        Handle keyboard input.

        Args:
            key: pygame key constant
        """
        if not self.view:
            return

        logger.debug(f"Processing key press: {key}")

        # Settings dialog
        if key == pygame.K_ESCAPE:
            logger.debug("Opening settings dialog")
            self.view.show_settings_dialog()

        # Z-level controls (validation is centralized in set_z_level)
        elif key == pygame.K_PAGEUP:
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

    def _update_turn_display(self) -> None:
        """Update the view's turn information display."""
        if not self.view:
            return

        # Get current turn status from model
        turn_info = self.model.get_turn_status()

        # Update turn bar in view
        self.view.update_turn_info(
            turn_number=turn_info["turn_number"],
            action_points=turn_info["action_points"],
            phase=turn_info["current_phase"],
        )

    def show_mission_selection(self, sector: str) -> None:
        """
        Show mission selection dialog at starbase.

        Args:
            sector: Sector identifier for mission filtering
        """
        if not self.view:
            return

        self.view.show_mission_selection_dialog(sector)

    def accept_mission(self, mission: Mission) -> None:
        """
        Accept a mission and add to active missions.

        Args:
            mission: Mission to accept
        """
        self.model.mission_manager.accept_mission(mission)

        if self.view:
            self.view.show_message(f"Mission accepted: {mission.name}")
            self.view.update_mission_tracker()

    def show_mission_briefing(self, mission: Mission) -> None:
        """
        Show detailed mission briefing dialog.

        Args:
            mission: Mission to display
        """
        if not self.view:
            return

        self.view.show_mission_briefing_dialog(mission)

    def update_mission_tracker(self) -> None:
        """Update the mission tracker widget with current mission status."""
        if not self.view:
            return

        self.view.update_mission_tracker()
