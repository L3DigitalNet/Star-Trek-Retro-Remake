#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Star Trek Retro Remake - Game View

Description:
    Game view implementation using PySide6 for UI and pygame-ce for game rendering.
    Implements the View component of the MVC pattern.

Author: Star Trek Retro Remake Development Team
Email: development@star-trek-retro-remake.org
GitHub: https://github.com/L3DigitalNet/Star-Trek-Retro-Remake
Date Created: 10-29-2025
Date Changed: 10-30-2025
License: MIT

Features:
    - PySide6 main window and UI management
    - pygame-ce game surface for rendering
    - UI widgets and dialog management
    - Event handling and user interaction

Requirements:
    - Linux environment
    - Python 3.14+ for latest language features
    - PySide6 for UI framework
    - pygame-ce (Community Edition) for game rendering

Classes:
    - GameView: Main view component implementing UI and rendering

Functions:
    - None
"""

import logging
from typing import Final, TYPE_CHECKING

import pygame
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QImage, QPixmap, QMouseEvent, QKeyEvent

# Import isometric grid renderer
from engine.isometric_grid import GridRenderer, create_sector_grid

if TYPE_CHECKING:
    from game.controller import GameController
    from game.entities.base import GridPosition

__version__: Final[str] = "0.0.3"

logger = logging.getLogger(__name__)


class GameDisplay(QLabel):
    """
    Custom QLabel for game display with mouse and keyboard input.

    Captures mouse and keyboard events and forwards them to the controller.
    """

    def __init__(self, view: 'GameView'):
        """
        Initialize the game display widget.

        Args:
            view: Reference to parent view
        """
        super().__init__()
        self.view = view
        self.setFocusPolicy(Qt.StrongFocus)  # Allow keyboard focus
        self.setMouseTracking(True)  # Track mouse movement

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """
        Handle mouse press events.

        Args:
            event: Qt mouse event
        """
        if event.button() == Qt.LeftButton:
            pos = (event.pos().x(), event.pos().y())
            logger.info(f"Mouse clicked at: {pos}")
            self.view.controller._handle_mouse_click(pos)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """
        Handle keyboard press events.

        Args:
            event: Qt keyboard event
        """
        # Convert Qt keys to pygame keys
        key_map = {
            Qt.Key_Up: pygame.K_UP,
            Qt.Key_Down: pygame.K_DOWN,
            Qt.Key_Left: pygame.K_LEFT,
            Qt.Key_Right: pygame.K_RIGHT,
            Qt.Key_PageUp: pygame.K_PAGEUP,
            Qt.Key_PageDown: pygame.K_PAGEDOWN,
            Qt.Key_Space: pygame.K_SPACE,
            Qt.Key_Escape: pygame.K_ESCAPE,
        }

        qt_key = event.key()
        if qt_key in key_map:
            pygame_key = key_map[qt_key]
            logger.info(f"Key pressed: {event.key()} -> pygame key: {pygame_key}")
            self.view.controller._handle_keypress(pygame_key)
        else:
            logger.debug(f"Unmapped key pressed: {event.key()}")


class GameView:
    """
    Main view component implementing UI and rendering.

    Manages the PySide6 main window, pygame-ce rendering surface,
    and all user interface elements using the View pattern.

    Attributes:
        controller: Reference to the game controller
        main_window: PySide6 main application window
        game_surface: pygame-ce surface for game rendering
        update_timer: Timer for regular UI updates

    Public methods:
        run: Start the view event loop
        close: Close the view and cleanup resources
        render_sector_map: Render the sector map view
        show_combat_dialog: Display combat results
        show_ship_status: Display ship status information

    Private methods:
        _setup_ui: Initialize the user interface
        _setup_pygame_widget: Set up pygame-ce integration
        _update_display: Update the display regularly
    """

    def __init__(self, controller: 'GameController'):
        """
        Initialize the game view.

        Args:
            controller: Reference to the game controller
        """
        self.controller = controller

        # Initialize PySide6 main window
        self.main_window = QMainWindow()
        self.main_window.setWindowTitle("Star Trek Retro Remake")
        self.main_window.setGeometry(100, 100, 1024, 768)

        # Initialize pygame-ce surface
        pygame.init()
        self.game_surface = pygame.Surface((800, 600))

        # Initialize isometric grid renderer
        self.grid_renderer = create_sector_grid()
        self.current_z_level = 0  # Current visible z-level
        self.selected_cell: GridPosition | None = None

        # Set up UI
        self._setup_ui()

        # Clock for managing updates
        self.clock = pygame.time.Clock()

        # Set up update timer
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self._update_display)
        self.update_timer.start(16)  # ~60 FPS

        logger.info("GameView initialized with isometric grid renderer")

    def run(self) -> None:
        """Start the view event loop."""
        self.main_window.show()
        # PySide6 event loop will be managed by the application

    def close(self) -> None:
        """Close the view and cleanup resources."""
        self.update_timer.stop()
        self.main_window.close()
        pygame.quit()

    def render_sector_map(self, sector_map, game_objects: list) -> None:
        """
        Render the sector map view.

        Args:
            sector_map: Sector map to render
            game_objects: List of game objects to display
        """
        # Clear the game surface
        self.game_surface.fill((20, 20, 30))  # Dark space background

        # Render isometric grid
        self.grid_renderer.render_grid(
            self.game_surface,
            visible_z_levels=[self.current_z_level]
        )

        # Highlight selected cell if any
        if self.selected_cell:
            self.grid_renderer.render_cell_highlight(
                self.game_surface,
                self.selected_cell,
                color=(0, 255, 0)  # Green highlight
            )

        # Render game objects
        for obj in game_objects:
            self._render_game_object(obj)

    def show_combat_dialog(self, result) -> None:
        """
        Display combat results dialog.

        Args:
            result: Combat result data to display
        """
        # Placeholder for combat dialog
        logger.info("Combat Result: %s", result.message)

    def show_ship_status(self, ship) -> None:
        """
        Display ship status information.

        Args:
            ship: Starship to display status for
        """
        # Placeholder for ship status display
        logger.info("Ship Status: %s - Hull: %.1f%%", ship.name, ship.hull_integrity)

    def show_message(self, message: str) -> None:
        """
        Display a message to the user.

        Args:
            message: Message to display
        """
        # Placeholder for message display
        logger.info("Message: %s", message)

    def _setup_ui(self) -> None:
        """Initialize the user interface."""
        # Create central widget
        central_widget = QWidget()
        self.main_window.setCentralWidget(central_widget)

        # Create layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Create custom game display widget with input handling
        self.game_label = GameDisplay(self)
        self.game_label.setMinimumSize(800, 600)
        layout.addWidget(self.game_label)

        # Set focus to game display for keyboard input
        self.game_label.setFocus()

        # pygame-ce widget will be integrated here
        self._setup_pygame_widget()

    def _setup_pygame_widget(self) -> None:
        """Set up pygame-ce integration widget."""
        # Placeholder for pygame-ce widget integration
        # This will embed the pygame-ce surface in the PySide6 window
        pass

    def _update_display(self) -> None:
        """Update the display regularly."""
        # Clear pygame event queue (events are handled by Qt now)
        pygame.event.pump()

        # Calculate delta time
        dt = self.clock.tick(60) / 1000.0

        # Update controller
        self.controller._update(dt)

        # Render current state first (clears screen)
        self.controller.state_manager.render(self.game_surface)

        # Render the game content on top
        if hasattr(self.controller.model, 'current_sector') and self.controller.model.current_sector:
            self.render_sector_map(
                self.controller.model.current_sector,
                self.controller.model.game_objects
            )

        # Convert pygame surface to QPixmap and display
        # Get the pygame surface as a string buffer
        surface_string = pygame.image.tostring(self.game_surface, 'RGB')
        w, h = self.game_surface.get_size()

        # Create QImage from the buffer
        qimage = QImage(surface_string, w, h, w * 3, QImage.Format_RGB888)

        # Convert to QPixmap and display
        pixmap = QPixmap.fromImage(qimage)
        self.game_label.setPixmap(pixmap)

    def set_z_level(self, z_level: int) -> None:
        """
        Set the currently visible z-level.

        Args:
            z_level: Z-level to display (0 to max_z_levels-1)
        """
        if 0 <= z_level < self.grid_renderer.max_z_levels:
            self.current_z_level = z_level
            logger.debug("Z-level changed to: %d", z_level)

    def set_selected_cell(self, position: 'GridPosition') -> None:
        """
        Set the currently selected grid cell.

        Args:
            position: Grid position to select
        """
        self.selected_cell = position
        logger.debug("Selected cell: %s", position)

    def clear_selection(self) -> None:
        """Clear the current cell selection."""
        self.selected_cell = None

    def _render_grid(self, sector_map) -> None:
        """
        Render the sector grid.

        Args:
            sector_map: Sector map to render grid for
        """
        # Grid rendering is now handled by render_sector_map
        # This method kept for compatibility
        pass

    def _render_game_object(self, obj) -> None:
        """
        Render a single game object.

        Args:
            obj: Game object to render
        """
        # Get object position and convert to screen coordinates
        if hasattr(obj, 'position'):
            screen_pos = self.grid_renderer.world_to_screen(obj.position)

            # Draw a placeholder circle for the object
            # Color varies based on object type
            color = (255, 255, 0)  # Yellow default

            if hasattr(obj, 'name') and 'Enterprise' in obj.name:
                color = (0, 255, 255)  # Cyan for player ship

            # Draw circle at screen position
            pygame.draw.circle(self.game_surface, color, screen_pos, 8)

            # Draw name label if available
            if hasattr(obj, 'name') and obj.name:
                font = pygame.font.Font(None, 18)
                text = font.render(obj.name, True, (255, 255, 255))
                text_rect = text.get_rect(center=(screen_pos[0], screen_pos[1] - 15))
                self.game_surface.blit(text, text_rect)