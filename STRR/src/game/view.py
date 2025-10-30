#!/usr/bin/env python3
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
    - Target selection dialog for combat
    - Weapon firing with phaser and torpedo options

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
from pathlib import Path
from typing import TYPE_CHECKING, Final

import pygame
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QAction, QImage, QKeyEvent, QMouseEvent, QPixmap
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QDockWidget, QLabel, QProgressBar, QPushButton

from ..engine.isometric_grid import create_sector_grid

if TYPE_CHECKING:
    from .controller import GameController
    from .entities.base import GridPosition

__version__: Final[str] = "0.0.21"

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
        logger.debug(
            f"Mouse click: widget=({widget_x}, {widget_y}) -> "
            f"pygame=({pixmap_x}, {pixmap_y}) offset=({x_offset}, {y_offset})"
        )

        self.view.controller.handle_mouse_click(pos)

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
            logger.debug(f"Key pressed: {event.key()} -> pygame key: {pygame_key}")
            self.view.controller.handle_keypress(pygame_key)
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

        # Load UI from Qt Designer file
        self._load_ui()

        # Override close event to ensure proper cleanup
        self.main_window.closeEvent = self._handle_close_event

        # Initialize pygame-ce surface
        pygame.init()
        self.game_surface = pygame.Surface((1280, 900))

        # Initialize isometric grid renderer
        self.grid_renderer = create_sector_grid()
        self.current_z_level = 0  # Current visible z-level
        self.selected_cell: GridPosition | None = None
        self.move_mode: bool = False  # Whether move mode is active

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

        # Connect UI signals to slots
        self._connect_signals()

        # Replace the gameDisplay QLabel with our custom GameDisplay widget
        self._setup_game_display()

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

        # Update ship name
        if hasattr(self, "ship_name_label") and self.ship_name_label:
            self.ship_name_label.setText(ship.name)

        # Update hull progress bar
        if hasattr(self, "hull_progress") and self.hull_progress:
            self.hull_progress.setValue(int(ship.hull_integrity))

        # Update shields if ship has them
        if hasattr(ship, "shields") and hasattr(self, "shields_progress"):
            if self.shields_progress:
                self.shields_progress.setValue(int(ship.shields))

        # Update energy if ship has it
        if hasattr(ship, "energy") and hasattr(self, "energy_progress"):
            if self.energy_progress:
                self.energy_progress.setValue(int(ship.energy))

        # Update position if available
        if hasattr(ship, "position") and hasattr(self, "coordinates_label"):
            if self.coordinates_label:
                pos = ship.position
                self.coordinates_label.setText(f"X: {pos.x}, Y: {pos.y}, Z: {pos.z}")

    def show_message(self, message: str) -> None:
        """
        Display a message to the user.

        Args:
            message: Message to display
        """
        logger.info("Message: %s", message)
        # Message display removed in new layout - use status bar or dialogs

    def _load_ui(self) -> None:
        """Load UI from Qt Designer .ui file."""
        # Get the path to the UI file
        ui_dir = Path(__file__).parent.parent / "ui" / "designer"
        ui_file = ui_dir / "main_window.ui"

        if not ui_file.exists():
            logger.error(f"UI file not found: {ui_file}")
            raise FileNotFoundError(f"UI file not found: {ui_file}")

        # Load the UI file - QUiLoader.load() expects a file path string or QIODevice
        loader = QUiLoader()
        self.main_window = loader.load(str(ui_file))

        # Store references to status UI elements in right dock
        self.ship_name_label = self.main_window.findChild(QLabel, "shipNameLabel")
        self.hull_progress = self.main_window.findChild(QProgressBar, "hullProgressBar")
        self.shields_progress = self.main_window.findChild(
            QProgressBar, "shieldsProgressBar"
        )
        self.energy_progress = self.main_window.findChild(
            QProgressBar, "energyProgressBar"
        )
        self.coordinates_label = self.main_window.findChild(QLabel, "coordinatesLabel")
        self.sector_label = self.main_window.findChild(QLabel, "sectorLabel")

        # Store references to turn bar elements
        self.end_turn_btn = self.main_window.findChild(QPushButton, "endTurnButton")
        self.action_points_label = self.main_window.findChild(
            QLabel, "actionPointsLabel"
        )
        self.phase_label = self.main_window.findChild(QLabel, "phaseLabel")
        self.turn_number_label = self.main_window.findChild(QLabel, "turnNumberLabel")

        # Store references to action buttons
        self.move_btn = self.main_window.findChild(QPushButton, "moveButton")
        self.rotate_btn = self.main_window.findChild(QPushButton, "rotateButton")
        self.fire_btn = self.main_window.findChild(QPushButton, "fireButton")
        self.scan_btn = self.main_window.findChild(QPushButton, "scanButton")
        self.evasive_btn = self.main_window.findChild(QPushButton, "evasiveButton")
        self.dock_btn = self.main_window.findChild(QPushButton, "dockButton")
        self.hail_btn = self.main_window.findChild(QPushButton, "hailButton")

        # Store references to toolbar actions
        self.action_galaxy = self.main_window.findChild(QAction, "actionGalaxyMode")
        self.action_sector = self.main_window.findChild(QAction, "actionSectorMode")
        self.action_combat = self.main_window.findChild(QAction, "actionCombatMode")
        self.action_zoom_in = self.main_window.findChild(QAction, "actionZoomIn")
        self.action_zoom_out = self.main_window.findChild(QAction, "actionZoomOut")
        self.action_zoom_reset = self.main_window.findChild(QAction, "actionZoomReset")

        # Store references to menu actions
        self.action_new_game = self.main_window.findChild(QAction, "actionNewGame")
        self.action_save_game = self.main_window.findChild(QAction, "actionSaveGame")
        self.action_load_game = self.main_window.findChild(QAction, "actionLoadGame")
        self.action_quit = self.main_window.findChild(QAction, "actionQuit")

        # Store reference to right dock
        self.right_dock = self.main_window.findChild(QDockWidget, "rightDock")

        logger.info(f"UI loaded from: {ui_file}")

    def _connect_signals(self) -> None:
        """Connect UI signals to slots."""
        # Menu actions
        self.action_new_game.triggered.connect(self._on_new_game)
        self.action_save_game.triggered.connect(self._on_save_game)
        self.action_load_game.triggered.connect(self._on_load_game)
        self.action_quit.triggered.connect(self._on_quit)

        # Toolbar mode actions
        self.action_galaxy.triggered.connect(self._on_galaxy_mode)
        self.action_sector.triggered.connect(self._on_sector_mode)
        self.action_combat.triggered.connect(self._on_combat_mode)

        # Toolbar zoom actions
        self.action_zoom_in.triggered.connect(self._on_zoom_in)
        self.action_zoom_out.triggered.connect(self._on_zoom_out)
        self.action_zoom_reset.triggered.connect(self._on_zoom_reset)

        # Turn bar
        self.end_turn_btn.clicked.connect(self._on_end_turn)

        # Action buttons
        self.move_btn.clicked.connect(self._on_move)
        self.rotate_btn.clicked.connect(self._on_rotate)
        self.fire_btn.clicked.connect(self._on_fire)
        self.scan_btn.clicked.connect(self._on_scan)
        self.evasive_btn.clicked.connect(self._on_evasive)
        self.dock_btn.clicked.connect(self._on_dock)
        self.hail_btn.clicked.connect(self._on_hail)

    def _setup_game_display(self) -> None:
        """Replace the placeholder game display with custom GameDisplay widget."""
        # Find the game display label in the loaded UI
        old_label = self.main_window.findChild(QLabel, "gameDisplay")
        if not old_label:
            logger.error("gameDisplay label not found in UI file")
            return

        # Get parent layout
        parent_layout = old_label.parent().layout()
        if not parent_layout:
            logger.error("Could not find parent layout for gameDisplay")
            return

        # Find the position of the old label in the layout
        index = -1
        for i in range(parent_layout.count()):
            if parent_layout.itemAt(i).widget() == old_label:
                index = i
                break

        if index == -1:
            logger.error("Could not find gameDisplay in parent layout")
            return

        # Create custom game display widget
        self.game_label = GameDisplay(self)
        self.game_label.setMinimumSize(1280, 900)
        self.game_label.setMaximumSize(1280, 900)

        # Replace the old label with the new widget
        parent_layout.removeWidget(old_label)
        old_label.deleteLater()
        parent_layout.insertWidget(index, self.game_label)

        # Set focus to game display for keyboard input
        self.game_label.setFocus()

        logger.info("Custom game display widget installed")

    def _on_new_game(self) -> None:
        """Handle New Game action."""
        if self.controller:
            self.controller.start_new_game()
        logger.info("New game started")

    def _on_save_game(self) -> None:
        """Handle Save Game action."""
        logger.info("Save game functionality coming soon...")

    def _on_load_game(self) -> None:
        """Handle Load Game action."""
        logger.info("Load game functionality coming soon...")

    def _on_quit(self) -> None:
        """Handle Quit action."""
        self.main_window.close()

    def _on_galaxy_mode(self) -> None:
        """Handle Galaxy Mode toolbar action."""
        logger.info("Switching to Galaxy Map mode")
        self.controller.switch_to_galaxy_mode()
        self.show_message("Switched to Galaxy Map")

    def _on_sector_mode(self) -> None:
        """Handle Sector Mode toolbar action."""
        logger.info("Switching to Sector Map mode")
        self.controller.switch_to_sector_mode()
        self.show_message("Switched to Sector Map")

    def _on_combat_mode(self) -> None:
        """Handle Combat Mode toolbar action."""
        logger.info("Switching to Combat mode")
        self.controller.switch_to_combat_mode()
        self.show_message("Switched to Combat Mode")

    def _on_zoom_in(self) -> None:
        """Handle Zoom In toolbar action."""
        self.grid_renderer.zoom_in()
        logger.info(f"Zoom in: {self.grid_renderer.zoom_level:.2f}x")
        self.show_message(f"Zoom: {self.grid_renderer.zoom_level:.2f}x")

    def _on_zoom_out(self) -> None:
        """Handle Zoom Out toolbar action."""
        self.grid_renderer.zoom_out()
        logger.info(f"Zoom out: {self.grid_renderer.zoom_level:.2f}x")
        self.show_message(f"Zoom: {self.grid_renderer.zoom_level:.2f}x")

    def _on_zoom_reset(self) -> None:
        """Handle Zoom Reset toolbar action."""
        self.grid_renderer.reset_zoom()
        logger.info("Zoom reset: 1.0x")
        self.show_message("Zoom reset to 1.0x")

    def _on_end_turn(self) -> None:
        """Handle End Turn button click."""
        logger.info("End turn requested")
        self.controller.end_turn()

    def _on_move(self) -> None:
        """
        Handle Move button click.

        Toggles move mode - when active, clicking on the grid will
        move the player ship to that location.
        """
        self.move_mode = not self.move_mode
        if self.move_mode:
            logger.info("Move mode activated - click on grid to move ship")
            self.show_message("Move Mode: Click on grid to move ship")
            self.move_btn.setText("Cancel Move")
        else:
            logger.info("Move mode deactivated")
            self.show_message("Move mode cancelled")
            self.move_btn.setText("Move Ship")

    def _on_rotate(self) -> None:
        """
        Handle Rotate button click.

        Opens a dialog to select new orientation for the player ship.
        """
        logger.info("Rotate action selected")
        # TODO: Implement rotation dialog (future milestone)
        self.show_message("Rotation not yet implemented")

    def _on_fire(self) -> None:
        """
        Handle Fire Weapons button click.

        Opens target selection dialog and fires weapons at selected target.
        """
        logger.info("Fire weapons action selected")

        # Get available targets from controller
        targets = self.controller.get_available_targets("phaser")

        if not targets:
            self.show_message("No targets in range")
            return

        # Show target selection dialog
        from PySide6.QtWidgets import (
            QDialog,
            QHBoxLayout,
            QLabel,
            QListWidget,
            QPushButton,
            QVBoxLayout,
        )

        dialog = QDialog(self.main_window)
        dialog.setWindowTitle("Select Target")
        dialog.setMinimumWidth(300)

        layout = QVBoxLayout()

        # Add instructions
        label = QLabel("Select target to fire phasers:")
        layout.addWidget(label)

        # Create target list
        target_list = QListWidget()
        for target in targets:
            distance = self.controller.model.player_ship.position.distance_to(
                target.position
            )
            target_list.addItem(
                f"{target.name} ({target.ship_class}) - {distance:.1f} units"
            )
        layout.addWidget(target_list)

        # Add weapon type selection
        weapon_label = QLabel("Weapon type:")
        layout.addWidget(weapon_label)

        weapon_layout = QHBoxLayout()
        phaser_btn = QPushButton("Phasers (1 AP)")
        torpedo_btn = QPushButton("Torpedoes (2 AP)")
        weapon_layout.addWidget(phaser_btn)
        weapon_layout.addWidget(torpedo_btn)
        layout.addLayout(weapon_layout)

        # Add action buttons
        button_layout = QHBoxLayout()
        cancel_btn = QPushButton("Cancel")
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)

        dialog.setLayout(layout)

        # Track selected weapon type
        selected_weapon = ["phaser"]  # Default

        # Connect buttons
        def fire_phaser():
            selected_weapon[0] = "phaser"
            selected_index = target_list.currentRow()
            if selected_index >= 0:
                target = targets[selected_index]
                dialog.accept()
                self.controller.handle_combat_action(target, "phaser")

        def fire_torpedo():
            selected_weapon[0] = "torpedo"
            selected_index = target_list.currentRow()
            if selected_index >= 0:
                target = targets[selected_index]
                dialog.accept()
                self.controller.handle_combat_action(target, "torpedo")

        phaser_btn.clicked.connect(fire_phaser)
        torpedo_btn.clicked.connect(fire_torpedo)
        cancel_btn.clicked.connect(dialog.reject)

        # Show dialog
        dialog.exec()

    def _on_scan(self) -> None:
        """
        Handle Scan Target button click.

        Scans selected target for detailed information (placeholder).
        """
        logger.info("Scan target action selected")
        # TODO: Implement target scanning system (next milestone)
        self.show_message("Target scanning not yet implemented")

    def _on_evasive(self) -> None:
        """
        Handle Evasive Maneuvers button click.

        Activates defensive maneuvering (placeholder).
        """
        logger.info("Evasive maneuvers selected")
        # TODO: Implement evasive maneuvers system (next milestone)
        self.show_message("Evasive maneuvers not yet implemented")

    def _on_dock(self) -> None:
        """
        Handle Dock at Station button click.

        Initiates docking procedure at nearby station (placeholder).
        """
        logger.info("Dock at station action selected")
        # TODO: Implement docking system (future milestone)
        self.show_message("Docking not yet implemented")

    def _on_hail(self) -> None:
        """
        Handle Hail Ship button click.

        Opens communication with selected ship (placeholder).
        """
        logger.info("Hail ship action selected")
        # TODO: Implement communication system (future milestone)
        self.show_message("Communications not yet implemented")

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
            # Z-level display removed in new layout - could add to status bar

    def update_turn_info(
        self, turn_number: int, phase: str, action_points: int
    ) -> None:
        """
        Update turn information display.

        Args:
            turn_number: Current turn number
            phase: Current phase name
            action_points: Remaining action points
        """
        if hasattr(self, "turn_number_label") and self.turn_number_label:
            self.turn_number_label.setText(f"Turn: {turn_number}")

        if hasattr(self, "phase_label") and self.phase_label:
            self.phase_label.setText(f"Phase: {phase}")

        if hasattr(self, "action_points_label") and self.action_points_label:
            self.action_points_label.setText(f"AP: {action_points}")

    def update_ui_state(self) -> None:
        """
        Update all UI elements to reflect current game state.

        Refreshes ship status, position, turn information, and sector name.
        Called after any game state change that affects the UI.
        """
        # Update ship status if player ship exists
        if self.controller.model.player_ship:
            self.show_ship_status(self.controller.model.player_ship)

        # Update sector name if available
        if (
            self.controller.model.current_sector
            and hasattr(self, "sector_label")
            and self.sector_label
        ):
            coords = self.controller.model.current_sector.coordinates
            sector_name = f"Sector {coords[0]}-{coords[1]}"
            self.sector_label.setText(sector_name)

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
        Uses GridRenderer.render_entity for starships with orientation indicators.

        Args:
            obj: Game object to render
        """
        # Get object position
        if not hasattr(obj, "position"):
            return

        # Only render objects on adjacent z-levels to prevent visual clutter
        min_z = max(0, self.current_z_level - 1)
        max_z = min(self.grid_renderer.max_z_levels - 1, self.current_z_level + 1)

        if not (min_z <= obj.position.z <= max_z):
            return  # Skip rendering objects on invisible z-levels

        # Check if this is a starship with rendering attributes
        if hasattr(obj, "color") and hasattr(obj, "size"):
            # This is a starship - use full entity rendering
            orientation = (
                obj.get_orientation_radians()
                if hasattr(obj, "get_orientation_radians")
                else 0.0
            )
            name = obj.name if hasattr(obj, "name") else ""

            self.grid_renderer.render_entity(
                self.game_surface,
                obj.position,
                obj.color,
                obj.size,
                orientation,
                name,
                self.current_z_level,  # Pass current z-level for reference lines
            )
        else:
            # Fallback rendering for other objects (stations, etc.)
            screen_pos = self.grid_renderer.world_to_screen(obj.position)

            # Draw a placeholder shape
            color = (255, 255, 0)  # Yellow default

            # Draw circle at screen position
            pygame.draw.circle(self.game_surface, color, screen_pos, 8)

            # Draw name label if available
            if hasattr(obj, "name") and obj.name:
                font = self._fonts[18]
                text = font.render(obj.name, True, (255, 255, 255))
                text_rect = text.get_rect(center=(screen_pos[0], screen_pos[1] - 15))
                self.game_surface.blit(text, text_rect)
