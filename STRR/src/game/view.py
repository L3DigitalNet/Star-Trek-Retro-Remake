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
Date Changed: 11-01-2025 (v0.0.29 - Fixed starship attribute access)
License: MIT

Features:
    - PySide6 main window and UI management
    - pygame-ce game surface for rendering
    - UI widgets and dialog management
    - Event handling and user interaction
    - Target selection dialog for combat
    - Weapon firing with phaser and torpedo options
    - Mission briefing and selection dialogs
    - Settings dialog with TOML integration
    - Mission tracker widget

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
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QImage, QKeyEvent, QMouseEvent, QPixmap
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
)

from ..engine.config_manager import get_config_value
from ..engine.isometric_grid import create_sector_grid
from ..ui.compiled.main_window_complete_ui import Ui_MainWindow
from .entities.base import GridPosition
from .ui.mission_dialogs import MissionBriefingDialog, MissionSelectionDialog
from .ui.settings_dialog import SettingsDialog

if TYPE_CHECKING:
    from .components.mission_manager import Mission
    from .controller import GameController

__version__: Final[str] = "0.0.29"

logger = logging.getLogger(__name__)


class GameDisplay(QLabel):
    """
    Custom QLabel for game display with mouse and keyboard input.

    Captures mouse and keyboard events and forwards them to the controller.
    """

    def __init__(self, view: GameView):
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

    def __init__(self, controller: GameController):
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

        # Initialize pygame-ce surface using configuration
        pygame.init()
        game_width = get_config_value(
            "game_settings", "display.game_surface_width", 1280
        )
        game_height = get_config_value(
            "game_settings", "display.game_surface_height", 900
        )
        self.game_surface = pygame.Surface((game_width, game_height))

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

        # Set up update timer using configuration
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self._update_display)
        update_interval = get_config_value(
            "game_settings", "display.update_timer_ms", 16
        )
        self.update_timer.start(update_interval)

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

            # Simple transparency: white for current, transparent gray for others using config
            if z == self.current_z_level:
                # Current level: fully opaque
                alpha = get_config_value(
                    "game_settings", "graphics.current_layer_alpha", 255
                )
            else:
                # Adjacent levels: semi-transparent
                alpha = get_config_value(
                    "game_settings", "graphics.adjacent_layer_alpha", 80
                )

            # Render this z-level to temporary surface with dashing based on distance
            self.grid_renderer.render_z_level(z_surface, z, self.current_z_level)

            # Apply transparency and blit to main surface
            z_surface.set_alpha(alpha)
            self.game_surface.blit(z_surface, (0, 0))

        # Highlight selected cell if any using configuration
        if self.selected_cell:
            highlight_color = get_config_value(
                "game_settings", "graphics.selection_highlight_color", [0, 255, 0]
            )
            self.grid_renderer.render_cell_highlight(
                self.game_surface,
                self.selected_cell,
                color=tuple(highlight_color),
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

        # Update ship name - UI elements loaded from Designer file are guaranteed to exist
        self.ship_name_label.setText(ship.name)

        # Update hull progress bar
        self.hull_progress.setValue(int(ship.hull_integrity))

        # Update shields and energy using component-based access
        shields_pct = (
            ship.systems["shields"].total_shield_strength
            / ship.systems["shields"].max_shield_strength
        ) * 100
        energy_pct = (
            ship.resources.energy_current / ship.resources.energy_capacity
        ) * 100
        self.shields_progress.setValue(int(shields_pct))
        self.energy_progress.setValue(int(energy_pct))

        # Update position - all ships have position
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
        """Load UI from compiled UI class."""
        # Create main window
        self.main_window = QMainWindow()

        # Create UI instance and set up the main window
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_window)

        # Initialize all UI elements with confident pattern
        self._initialize_ui_elements()

        logger.info("UI loaded from compiled main_window_complete_ui.py")

    def _initialize_ui_elements(self) -> None:
        """Initialize all UI elements with confident access pattern."""
        # Status UI elements in right dock - accessed directly from compiled UI
        self.ship_name_label = self.ui.shipNameLabel
        self.hull_progress = self.ui.hullProgressBar
        self.shields_progress = self.ui.shieldsProgressBar
        self.energy_progress = self.ui.energyProgressBar
        self.coordinates_label = self.ui.coordinatesLabel
        self.sector_label = self.ui.sectorLabel

        # Turn bar elements
        self.end_turn_btn = self.ui.endTurnButton
        self.action_points_label = self.ui.actionPointsLabel
        self.phase_label = self.ui.phaseLabel
        self.turn_number_label = self.ui.turnNumberLabel

        # Action buttons
        self.move_btn = self.ui.moveButton
        self.rotate_btn = self.ui.rotateButton
        self.fire_btn = self.ui.fireButton
        self.scan_btn = self.ui.scanButton
        self.evasive_btn = self.ui.evasiveButton
        self.dock_btn = self.ui.dockButton
        self.hail_btn = self.ui.hailButton

        # Toolbar actions
        self.action_galaxy = self.ui.actionGalaxyMode
        self.action_sector = self.ui.actionSectorMode
        self.action_combat = self.ui.actionCombatMode
        self.action_zoom_in = self.ui.actionZoomIn
        self.action_zoom_out = self.ui.actionZoomOut
        self.action_zoom_reset = self.ui.actionZoomReset

        # Menu actions
        self.action_new_game = self.ui.actionNewGame
        self.action_save_game = self.ui.actionSaveGame
        self.action_load_game = self.ui.actionLoadGame
        self.action_quit = self.ui.actionQuit

        # Right dock
        self.right_dock = self.ui.rightDock

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
        # Access the game display label directly from compiled UI
        old_label = self.ui.gameDisplay

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

        # Create custom game display widget using configuration
        self.game_label = GameDisplay(self)
        game_width = get_config_value(
            "game_settings", "display.game_surface_width", 1280
        )
        game_height = get_config_value(
            "game_settings", "display.game_surface_height", 900
        )
        self.game_label.setMinimumSize(game_width, game_height)
        self.game_label.setMaximumSize(game_width, game_height)

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

    def _on_settings(self) -> None:
        """Handle Settings action."""
        self.show_settings_dialog()

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
        dialog = QDialog(self.main_window)
        dialog.setWindowTitle("Select Target")
        dialog.setMinimumWidth(
            get_config_value("game_settings", "graphics.min_dialog_width", 300)
        )

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

        Initiates docking procedure and shows mission selection dialog.
        """
        logger.info("Dock at station action selected")
        # Show mission selection dialog for current sector
        if self.controller and self.controller.model.current_sector:
            sector_name = "Sol System"  # TODO: Get actual sector name
            self.controller.show_mission_selection(sector_name)
        else:
            self.show_message("No station in range")

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

        # Calculate delta time using configuration
        fps_limit = get_config_value("game_settings", "display.fps_limit", 60)
        dt = self.clock.tick(fps_limit) / 1000.0

        # Update controller
        self.controller._update(dt)

        # Clear the surface
        self.game_surface.fill((20, 20, 30))

        # Render sector map directly (state machine integration deferred)
        # current_sector is guaranteed to exist during gameplay
        if getattr(self.controller.model, "current_sector", None) is not None:
            self.render_sector_map(
                self.controller.model.current_sector, self.controller.model.game_objects
            )

        # Get surface data and copy into reusable buffer
        w, h = self.game_surface.get_size()
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
        # UI elements are guaranteed to exist from confident initialization
        self.turn_number_label.setText(f"Turn: {turn_number}")
        self.phase_label.setText(f"Phase: {phase}")
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

        # Update sector name if current_sector exists (defensive check for early UI update)
        if getattr(self.controller.model, "current_sector", None) is not None:
            coords = self.controller.model.current_sector.coordinates
            sector_name = f"Sector {coords[0]}-{coords[1]}"
            self.sector_label.setText(sector_name)
        else:
            # Fallback when sector is not yet initialized
            self.sector_label.setText("Sector: Unknown")

    def set_selected_cell(self, position: GridPosition) -> None:
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
            # Fallback rendering for other objects (stations, etc.) using configuration
            screen_pos = self.grid_renderer.world_to_screen(obj.position)

            # Draw a placeholder shape
            default_color = get_config_value(
                "game_settings", "graphics.default_entity_color", [255, 255, 0]
            )
            color = tuple(default_color)

            # Draw circle at screen position
            pygame.draw.circle(self.game_surface, color, screen_pos, 8)

            # Draw name label if available using configuration
            if hasattr(obj, "name") and obj.name:
                font = self._fonts[18]
                text_color = get_config_value(
                    "game_settings", "graphics.text_color", [255, 255, 255]
                )
                text = font.render(obj.name, True, tuple(text_color))
                text_rect = text.get_rect(center=(screen_pos[0], screen_pos[1] - 15))
                self.game_surface.blit(text, text_rect)

    def show_mission_selection_dialog(self, sector: str) -> None:
        """
        Show mission selection dialog for current sector.

        Args:
            sector: Sector identifier for mission filtering
        """
        dialog = MissionSelectionDialog(
            self.controller.model.mission_manager, sector, self.main_window
        )
        dialog.mission_selected.connect(self.controller.accept_mission)
        dialog.exec()

    def show_mission_briefing_dialog(self, mission: Mission) -> None:
        """
        Show detailed mission briefing dialog.

        Args:
            mission: Mission to display
        """
        dialog = MissionBriefingDialog(mission, self.main_window)
        dialog.mission_accepted.connect(self.controller.accept_mission)
        dialog.exec()

    def show_settings_dialog(self) -> None:
        """Show settings dialog."""
        config_path = Path("STRR/config/game_settings.toml")
        dialog = SettingsDialog(config_path, self.main_window)
        if dialog.exec():
            # Settings were saved, reload if needed
            logger.info("Settings updated")

    def update_mission_tracker(self) -> None:
        """Update mission tracker widget with current missions."""
        # Placeholder for mission tracker widget update
        # Will be implemented when mission tracker is added to main window
        logger.info("Mission tracker update requested")
