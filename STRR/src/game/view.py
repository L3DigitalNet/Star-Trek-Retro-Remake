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
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QGroupBox,
)
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QImage, QPixmap, QMouseEvent, QKeyEvent

# Import isometric grid renderer
from engine.isometric_grid import GridRenderer, create_sector_grid

if TYPE_CHECKING:
    from game.controller import GameController
    from game.entities.base import GridPosition

__version__: Final[str] = "0.0.10"

logger = logging.getLogger(__name__)


class GameDisplay(QLabel):
    """
    Custom QLabel for game display with mouse and keyboard input.

    Captures mouse and keyboard events and forwards them to the controller.
    """

    def __init__(self, view: "GameView"):
        """
        Initialize the game display widget.

        Args:
            view: Reference to parent view
        """
        super().__init__()
        self.view = view
        self.setFocusPolicy(Qt.StrongFocus)  # Allow keyboard focus
        self.setMouseTracking(True)  # Track mouse movement
        self.setScaledContents(False)  # Don't scale pixmap, keep original size
        self.setAlignment(Qt.AlignCenter)  # Ensure pixmap is centered

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """
        Handle mouse press events.

        Converts widget coordinates to pygame surface coordinates accounting
        for centering, scaling, and window resize.

        Args:
            event: Qt mouse event
        """
        if event.button() != Qt.LeftButton:
            return

        # Get the pixmap to determine actual display area
        pixmap = self.pixmap()
        if not pixmap or pixmap.isNull():
            logger.warning("No pixmap available for mouse click")
            return

        # Get click position relative to widget
        widget_pos = event.pos()
        widget_x = widget_pos.x()
        widget_y = widget_pos.y()

        # Get widget and pixmap dimensions
        widget_size = self.size()
        pixmap_size = pixmap.size()

        widget_width = widget_size.width()
        widget_height = widget_size.height()
        pixmap_width = pixmap_size.width()
        pixmap_height = pixmap_size.height()

        # Calculate pixmap position in widget (centered)
        x_offset = (widget_width - pixmap_width) // 2
        y_offset = (widget_height - pixmap_height) // 2

        # Convert to pixmap (pygame surface) coordinates
        pixmap_x = widget_x - x_offset
        pixmap_y = widget_y - y_offset

        # Validate click is within pixmap bounds
        if not (0 <= pixmap_x < pixmap_width and 0 <= pixmap_y < pixmap_height):
            logger.debug(
                f"Click outside pixmap bounds: widget=({widget_x}, {widget_y}), "
                f"pixmap=({pixmap_x}, {pixmap_y}), bounds=(0-{pixmap_width}, 0-{pixmap_height})"
            )
            return

        pos = (pixmap_x, pixmap_y)
        logger.info(
            f"Mouse click: widget=({widget_x}, {widget_y}) -> "
            f"pygame=({pixmap_x}, {pixmap_y}) offset=({x_offset}, {y_offset})"
        )

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
            Qt.Key_Plus: pygame.K_PLUS,
            Qt.Key_Equal: pygame.K_EQUALS,  # For + without shift
            Qt.Key_Minus: pygame.K_MINUS,
            Qt.Key_0: pygame.K_0,  # For reset zoom
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

    def __init__(self, controller: "GameController"):
        """
        Initialize the game view.

        Args:
            controller: Reference to the game controller
        """
        self.controller = controller

        # Initialize PySide6 main window
        self.main_window = QMainWindow()
        self.main_window.setWindowTitle("Star Trek Retro Remake")
        self.main_window.setGeometry(100, 100, 1920, 1080)

        # Override close event to ensure proper cleanup
        self.main_window.closeEvent = self._handle_close_event

        # Initialize pygame-ce surface
        pygame.init()
        self.game_surface = pygame.Surface((1280, 900))

        # Initialize isometric grid renderer
        self.grid_renderer = create_sector_grid()
        self.current_z_level = 0  # Current visible z-level
        self.selected_cell: GridPosition | None = None

        # Font caching to prevent creating fonts every frame
        self._fonts: dict[int, pygame.font.Font] = {
            18: pygame.font.Font(None, 18),
            24: pygame.font.Font(None, 24),
            32: pygame.font.Font(None, 32),
        }

        # Pre-allocate QImage buffer to reduce GC pressure
        # Buffer size: width * height * 3 bytes (RGB)
        w, h = self.game_surface.get_size()
        self._qimage_buffer = bytearray(w * h * 3)

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

    def _handle_close_event(self, event) -> None:
        """
        Handle window close event.

        Ensures proper cleanup when user clicks the X button.

        Args:
            event: Qt close event
        """
        logger.info("Window close event triggered - cleaning up resources")
        self.update_timer.stop()
        pygame.quit()
        event.accept()

    def render_sector_map(self, sector_map, game_objects: list) -> None:
        """
        Render the sector map view.

        Args:
            sector_map: Sector map to render
            game_objects: List of game objects to display
        """
        # Clear the game surface
        self.game_surface.fill((20, 20, 30))  # Dark space background

        # Render only current z-level and adjacent levels (above and below)
        # This reduces visual clutter for testing purposes
        min_z = max(0, self.current_z_level - 1)
        max_z = min(self.grid_renderer.max_z_levels - 1, self.current_z_level + 1)

        # Render from bottom to top with transparency for depth perception
        for z in range(min_z, max_z + 1):
            # Create a temporary surface for this z-level
            z_surface = pygame.Surface(self.game_surface.get_size(), pygame.SRCALPHA)

            # Simple transparency: white for current, transparent gray for others
            if z == self.current_z_level:
                # Current level: fully opaque white
                alpha = 255
            else:
                # Adjacent levels: semi-transparent gray
                alpha = 80

            # Render this z-level to temporary surface with dashing based on distance
            self.grid_renderer.render_z_level(z_surface, z, self.current_z_level)

            # Apply transparency and blit to main surface
            z_surface.set_alpha(alpha)
            self.game_surface.blit(z_surface, (0, 0))

        # Highlight selected cell if any
        if self.selected_cell:
            self.grid_renderer.render_cell_highlight(
                self.game_surface,
                self.selected_cell,
                color=(0, 255, 0),  # Green highlight
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
        logger.info("Ship Status: %s - Hull: %.1f%%", ship.name, ship.hull_integrity)

        # Update ship status label in UI
        if hasattr(self, "ship_status_label"):
            status_text = (
                f"<b>{ship.name}</b><br>"
                f"Status: Active<br>"
                f"Hull: {ship.hull_integrity:.1f}%<br>"
            )

            # Add shields if ship has them
            if hasattr(ship, "shields"):
                status_text += f"Shields: {ship.shields:.1f}%<br>"

            # Add energy if ship has it
            if hasattr(ship, "energy"):
                status_text += f"Energy: {ship.energy:.0f}"

            self.ship_status_label.setText(status_text)

    def show_message(self, message: str) -> None:
        """
        Display a message to the user.

        Args:
            message: Message to display
        """
        logger.info("Message: %s", message)
        if hasattr(self, "message_display"):
            self.message_display.setText(message)

    def _setup_ui(self) -> None:
        """Initialize the user interface."""
        # Create central widget
        central_widget = QWidget()
        self.main_window.setCentralWidget(central_widget)

        # Create main horizontal layout
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        # Create control panel (left side)
        control_panel = self._create_control_panel()
        main_layout.addWidget(control_panel)

        # Create game display area (right side)
        game_container = QWidget()
        game_layout = QVBoxLayout()
        game_container.setLayout(game_layout)

        # Add title for game area
        game_title = QLabel("<h3>Sector Map View</h3>")
        game_title.setAlignment(Qt.AlignCenter)
        game_layout.addWidget(game_title)

        # Create custom game display widget with input handling
        self.game_label = GameDisplay(self)
        self.game_label.setMinimumSize(1280, 900)
        self.game_label.setMaximumSize(1280, 900)
        game_layout.addWidget(self.game_label)

        # Add instructions
        instructions = QLabel(
            "Controls: PageUp/PageDown (Z-levels) | +/- (Zoom) | "
            "Arrow Keys (Pan) | Left Click (Select/Move)"
        )
        instructions.setAlignment(Qt.AlignCenter)
        instructions.setStyleSheet(
            "padding: 5px; background-color: #2a2a2a; color: #ccc;"
        )
        game_layout.addWidget(instructions)

        main_layout.addWidget(game_container)

        # Set focus to game display for keyboard input
        self.game_label.setFocus()

        # pygame-ce widget will be integrated here
        self._setup_pygame_widget()

    def _create_control_panel(self) -> QWidget:
        """
        Create the control panel with game controls and status.

        Returns:
            QWidget containing control panel
        """
        # Create group box for controls
        group_box = QGroupBox("Game Controls")
        group_box.setMaximumWidth(350)
        group_box.setMinimumWidth(300)

        layout = QVBoxLayout()

        # Title
        title = QLabel("<h2>Star Trek<br>Retro Remake</h2>")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #00aaff; padding: 10px;")
        layout.addWidget(title)

        # Ship status label
        self.ship_status_label = QLabel(
            "<b>USS Enterprise</b><br>"
            "Status: Active<br>"
            "Hull: 100%<br>"
            "Shields: 100%<br>"
            "Energy: 5000"
        )
        self.ship_status_label.setStyleSheet(
            "padding: 10px; background-color: #1a1a1a; "
            "border: 1px solid #333; border-radius: 5px; color: #ccc;"
        )
        self.ship_status_label.setWordWrap(True)
        layout.addWidget(self.ship_status_label)

        # Z-level label
        self.z_level_label = QLabel("Z-Level: 0")
        self.z_level_label.setStyleSheet(
            "padding: 8px; background-color: #2a2a2a; "
            "border: 1px solid #444; border-radius: 3px; font-weight: bold;"
        )
        layout.addWidget(self.z_level_label)

        # Control buttons
        new_game_btn = QPushButton("New Game")
        new_game_btn.clicked.connect(self._on_new_game)
        layout.addWidget(new_game_btn)

        save_game_btn = QPushButton("Save Game")
        save_game_btn.clicked.connect(self._on_save_game)
        layout.addWidget(save_game_btn)

        load_game_btn = QPushButton("Load Game")
        load_game_btn.clicked.connect(self._on_load_game)
        layout.addWidget(load_game_btn)

        settings_btn = QPushButton("Settings")
        settings_btn.clicked.connect(self._on_settings)
        layout.addWidget(settings_btn)

        # Message display area
        message_label = QLabel("<b>Messages:</b>")
        layout.addWidget(message_label)

        self.message_display = QLabel("Ready to explore...")
        self.message_display.setStyleSheet(
            "padding: 10px; background-color: #0a0a0a; "
            "border: 1px solid #333; border-radius: 5px; "
            "color: #00ff00; font-family: monospace;"
        )
        self.message_display.setWordWrap(True)
        self.message_display.setMinimumHeight(100)
        layout.addWidget(self.message_display)

        # Add stretch to push quit button to bottom
        layout.addStretch()

        # Quit button
        quit_btn = QPushButton("Quit")
        quit_btn.clicked.connect(self._on_quit)
        quit_btn.setStyleSheet("background-color: #aa0000;")
        layout.addWidget(quit_btn)

        group_box.setLayout(layout)
        return group_box

    def _on_new_game(self) -> None:
        """Handle New Game button click."""
        if self.controller:
            self.controller.start_new_game()
            self.show_message("New game started!")

    def _on_save_game(self) -> None:
        """Handle Save Game button click."""
        self.show_message("Save game functionality coming soon...")

    def _on_load_game(self) -> None:
        """Handle Load Game button click."""
        self.show_message("Load game functionality coming soon...")

    def _on_settings(self) -> None:
        """Handle Settings button click."""
        self.show_message("Settings dialog coming soon...")

    def _on_quit(self) -> None:
        """Handle Quit button click."""
        self.main_window.close()

    def _setup_pygame_widget(self) -> None:
        """Set up pygame-ce integration widget."""
        # Placeholder for pygame-ce widget integration
        # This will embed the pygame-ce surface in the PySide6 window
        pass

    def _update_display(self) -> None:
        """Update the display regularly."""
        # Events are handled by Qt, not pygame
        # pygame.event.pump() removed to prevent event queue conflicts

        # Calculate delta time
        dt = self.clock.tick(60) / 1000.0

        # Update controller
        self.controller._update(dt)

        # Clear the surface
        self.game_surface.fill((20, 20, 30))

        # Render sector map directly (state machine integration deferred)
        if (
            hasattr(self.controller.model, "current_sector")
            and self.controller.model.current_sector
        ):
            self.render_sector_map(
                self.controller.model.current_sector, self.controller.model.game_objects
            )

        # Convert pygame surface to QPixmap using pre-allocated buffer
        w, h = self.game_surface.get_size()

        # Get surface data and copy into reusable buffer
        surface_data = pygame.image.tobytes(self.game_surface, "RGB")
        self._qimage_buffer[:] = surface_data  # Reuse buffer to reduce GC pressure

        # Create QImage from the buffer (buffer remains valid while QImage exists)
        qimage = QImage(self._qimage_buffer, w, h, w * 3, QImage.Format_RGB888)

        # Convert to QPixmap and display
        pixmap = QPixmap.fromImage(qimage)
        self.game_label.setPixmap(pixmap)

    def set_z_level(self, z_level: int) -> None:
        """
        Set the currently visible z-level.

        Args:
            z_level: Z-level to display (0 to max_z_levels-1)
        """
        # Clamp to valid range (centralized validation)
        z_level = max(0, min(z_level, self.grid_renderer.max_z_levels - 1))

        if z_level != self.current_z_level:
            self.current_z_level = z_level
            logger.info("Z-level changed to: %d", z_level)
            # Update UI label
            if hasattr(self, "z_level_label"):
                self.z_level_label.setText(f"Z-Level: {z_level}")

    def set_selected_cell(self, position: "GridPosition") -> None:
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

        Only renders objects on visible z-levels (current ±1).

        Args:
            obj: Game object to render
        """
        # Get object position and convert to screen coordinates
        if hasattr(obj, "position"):
            # Only render objects on adjacent z-levels to prevent visual clutter
            min_z = max(0, self.current_z_level - 1)
            max_z = min(self.grid_renderer.max_z_levels - 1, self.current_z_level + 1)

            if not (min_z <= obj.position.z <= max_z):
                return  # Skip rendering objects on invisible z-levels

            screen_pos = self.grid_renderer.world_to_screen(obj.position)

            # Draw a placeholder circle for the object
            # Color varies based on object type
            color = (255, 255, 0)  # Yellow default

            if hasattr(obj, "name") and "Enterprise" in obj.name:
                color = (0, 255, 255)  # Cyan for player ship

            # Draw circle at screen position
            pygame.draw.circle(self.game_surface, color, screen_pos, 8)

            # Draw name label if available
            if hasattr(obj, "name") and obj.name:
                # Use cached font to prevent creating fonts every frame
                font = self._fonts[18]
                text = font.render(obj.name, True, (255, 255, 255))
                text_rect = text.get_rect(center=(screen_pos[0], screen_pos[1] - 15))
                self.game_surface.blit(text, text_rect)
