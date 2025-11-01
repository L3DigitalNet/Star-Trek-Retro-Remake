#!/usr/bin/env python3
"""
Star Trek Retro Remake - PySide6 + pygame-ce Integration Demo

Description:
    Demonstrates how to embed pygame-ce rendering into a PySide6 Qt window.
    Shows proper integration pattern with Qt widgets alongside game display.

Author: Star Trek Retro Remake Development Team
Email: development@star-trek-retro-remake.org
GitHub: https://github.com/L3DigitalNet/Star-Trek-Retro-Remake
Date Created: 10-30-2025
Date Changed: 10-30-2025
License: MIT

Features:
    - PySide6 main window with proper layout
    - pygame-ce surface embedded in Qt widget
    - Control panel with Qt widgets (buttons, labels, etc.)
    - Proper event handling for both Qt and pygame
    - Clean separation between UI controls and game rendering

Requirements:
    - Linux environment
    - Python 3.14+
    - pygame-ce (Community Edition)
    - PySide6

Classes:
    - PygameWidget: Custom QLabel for pygame surface display
    - MainWindow: Main Qt window with layout

Functions:
    - main(): Entry point for demo
"""

import sys
from typing import Final

import pygame
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

__version__: Final[str] = "0.0.1"


class PygameWidget(QLabel):
    """
    Custom QLabel widget that displays a pygame surface.

    This widget converts pygame surface to QPixmap and displays it.
    It also handles mouse events and forwards them to pygame coordinates.

    Attributes:
        surface_size: Size of the pygame surface (width, height)
        surface: pygame surface for rendering
        qimage_buffer: Pre-allocated buffer for image conversion

    Public methods:
        update_from_surface: Update display from pygame surface
    """

    def __init__(self, width: int = 800, height: int = 600):
        """
        Initialize the pygame widget.

        Args:
            width: Width of the pygame surface
            height: Height of the pygame surface
        """
        super().__init__()

        # Set up widget properties
        self.setMinimumSize(width, height)
        self.setMaximumSize(width, height)
        self.setScaledContents(False)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("background-color: black; border: 2px solid #333;")

        # Create pygame surface
        self.surface_size = (width, height)
        self.surface = pygame.Surface(self.surface_size)

        # Pre-allocate buffer for efficient image conversion
        self._qimage_buffer = bytearray(width * height * 3)

        # Enable mouse tracking
        self.setMouseTracking(True)

    def update_from_surface(self) -> None:
        """
        Update the widget display from the pygame surface.

        Converts the pygame surface to QPixmap and displays it.
        Uses pre-allocated buffer to reduce memory allocations.
        """
        w, h = self.surface_size

        # Get surface data and copy into reusable buffer
        surface_data = pygame.image.tobytes(self.surface, "RGB")
        self._qimage_buffer[:] = surface_data

        # Create QImage from buffer
        qimage = QImage(self._qimage_buffer, w, h, w * 3, QImage.Format_RGB888)

        # Convert to QPixmap and display
        pixmap = QPixmap.fromImage(qimage)
        self.setPixmap(pixmap)

    def get_surface(self) -> pygame.Surface:
        """
        Get the pygame surface for rendering.

        Returns:
            pygame surface
        """
        return self.surface


class MainWindow(QMainWindow):
    """
    Main application window demonstrating PySide6 + pygame integration.

    Shows a Qt window with:
    - Left side: Control panel with Qt widgets
    - Right side: pygame rendering area

    Attributes:
        pygame_widget: Custom widget for pygame display
        update_timer: Timer for regular display updates
        clock: pygame clock for frame timing
        frame_count: Counter for animation

    Public methods:
        update_game: Update game logic and rendering

    Private methods:
        _setup_ui: Initialize the user interface
        _create_control_panel: Create the control panel widgets
        _create_game_area: Create the game display area
    """

    def __init__(self):
        """Initialize the main window."""
        super().__init__()

        # Window properties
        self.setWindowTitle("Star Trek Retro Remake - Qt + pygame Demo")
        self.setGeometry(100, 100, 1200, 700)

        # Initialize pygame
        pygame.init()

        # Set up the UI
        self._setup_ui()

        # Game state
        self.clock = pygame.time.Clock()
        self.frame_count = 0
        self.circle_x = 100
        self.circle_y = 300
        self.circle_dx = 2
        self.circle_dy = 1.5

        # Set up update timer (~60 FPS)
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_game)
        self.update_timer.start(16)  # ~60 FPS

        # Status message
        self.status_label.setText("Game running at 60 FPS")

    def _setup_ui(self) -> None:
        """Initialize the user interface with layout."""
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        # Create control panel (left side)
        control_panel = self._create_control_panel()
        main_layout.addWidget(control_panel)

        # Create game area (right side)
        game_area = self._create_game_area()
        main_layout.addWidget(game_area)

    def _create_control_panel(self) -> QWidget:
        """
        Create the control panel with Qt widgets.

        Returns:
            QWidget containing control panel
        """
        # Create group box for controls
        group_box = QGroupBox("Game Controls")
        group_box.setMaximumWidth(350)

        layout = QVBoxLayout()

        # Title label
        title = QLabel("<h2>Star Trek Retro Remake</h2>")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Info label
        info = QLabel(
            "<b>Integration Demo</b><br><br>"
            "This demonstrates PySide6 Qt window with pygame-ce embedded.<br><br>"
            "• Left panel: Qt widgets (buttons, labels)<br>"
            "• Right panel: pygame rendering surface"
        )
        info.setWordWrap(True)
        layout.addWidget(info)

        # Buttons
        start_btn = QPushButton("Start Game")
        start_btn.clicked.connect(self.on_start_clicked)
        layout.addWidget(start_btn)

        pause_btn = QPushButton("Pause/Resume")
        pause_btn.clicked.connect(self.on_pause_clicked)
        layout.addWidget(pause_btn)

        reset_btn = QPushButton("Reset Animation")
        reset_btn.clicked.connect(self.on_reset_clicked)
        layout.addWidget(reset_btn)

        # Status label
        self.status_label = QLabel("Status: Ready")
        self.status_label.setStyleSheet(
            "padding: 10px; background-color: #f0f0f0; border-radius: 5px;"
        )
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)

        # Frame counter label
        self.frame_label = QLabel("Frames: 0")
        layout.addWidget(self.frame_label)

        # Add stretch to push everything to the top
        layout.addStretch()

        # Quit button at bottom
        quit_btn = QPushButton("Quit")
        quit_btn.clicked.connect(self.close)
        layout.addWidget(quit_btn)

        group_box.setLayout(layout)
        return group_box

    def _create_game_area(self) -> QWidget:
        """
        Create the game display area with pygame widget.

        Returns:
            QWidget containing game display
        """
        # Create container widget
        container = QWidget()
        layout = QVBoxLayout()

        # Title
        title = QLabel("<h3>pygame-ce Rendering Area</h3>")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Create pygame widget
        self.pygame_widget = PygameWidget(800, 600)
        layout.addWidget(self.pygame_widget)

        # Instructions
        instructions = QLabel(
            "pygame surface rendered here - bouncing circle animation"
        )
        instructions.setAlignment(Qt.AlignCenter)
        layout.addWidget(instructions)

        container.setLayout(layout)
        return container

    def update_game(self) -> None:
        """
        Update game logic and rendering.

        Called every frame by the timer (~60 FPS).
        """
        # Calculate delta time
        dt = self.clock.tick(60) / 1000.0

        # Update frame counter
        self.frame_count += 1
        if self.frame_count % 60 == 0:
            self.frame_label.setText(f"Frames: {self.frame_count}")

        # Get pygame surface
        surface = self.pygame_widget.get_surface()

        # Clear with dark blue background (space)
        surface.fill((10, 10, 40))

        # Draw grid
        grid_color = (30, 30, 60)
        for x in range(0, 800, 50):
            pygame.draw.line(surface, grid_color, (x, 0), (x, 600))
        for y in range(0, 600, 50):
            pygame.draw.line(surface, grid_color, (0, y), (800, y))

        # Update circle position (bouncing animation)
        self.circle_x += self.circle_dx
        self.circle_y += self.circle_dy

        # Bounce off edges
        if self.circle_x <= 20 or self.circle_x >= 780:
            self.circle_dx = -self.circle_dx
        if self.circle_y <= 20 or self.circle_y >= 580:
            self.circle_dy = -self.circle_dy

        # Draw bouncing circle (representing a starship)
        pygame.draw.circle(
            surface, (0, 255, 255), (int(self.circle_x), int(self.circle_y)), 20
        )

        # Draw some stars
        import random

        random.seed(42)  # Fixed seed for consistent stars
        for _ in range(100):
            x = random.randint(0, 800)
            y = random.randint(0, 600)
            size = random.randint(1, 2)
            pygame.draw.circle(surface, (200, 200, 200), (x, y), size)

        # Draw text on pygame surface
        font = pygame.font.Font(None, 36)
        text = font.render("USS Enterprise", True, (255, 255, 0))
        text_rect = text.get_rect(center=(int(self.circle_x), int(self.circle_y) - 35))
        surface.blit(text, text_rect)

        # Update the widget display
        self.pygame_widget.update_from_surface()

    def on_start_clicked(self) -> None:
        """Handle Start button click."""
        self.status_label.setText("Status: Game started!")

    def on_pause_clicked(self) -> None:
        """Handle Pause button click."""
        if self.update_timer.isActive():
            self.update_timer.stop()
            self.status_label.setText("Status: Paused")
        else:
            self.update_timer.start(16)
            self.status_label.setText("Status: Resumed")

    def on_reset_clicked(self) -> None:
        """Handle Reset button click."""
        self.circle_x = 100
        self.circle_y = 300
        self.circle_dx = 2
        self.circle_dy = 1.5
        self.frame_count = 0
        self.status_label.setText("Status: Animation reset")

    def closeEvent(self, event) -> None:
        """
        Handle window close event.

        Ensures proper cleanup of pygame resources.

        Args:
            event: Qt close event
        """
        self.update_timer.stop()
        pygame.quit()
        event.accept()


def main() -> None:
    """
    Main entry point for the demo.

    Creates and runs the Qt application with pygame integration.
    """
    # Create Qt application
    app = QApplication(sys.argv)

    # Create and show main window
    window = MainWindow()
    window.show()

    # Run event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
