#!/usr/bin/env python3
"""
Star Trek Retro Remake - Game Application

Description:
    Main game application class implementing the MVC pattern and coordinating
    all game systems. Manages the game loop, state transitions, and resource
    management.

Author: Star Trek Retro Remake Development Team
Email: development@star-trek-retro-remake.org
GitHub: https://github.com/L3DigitalNet/Star-Trek-Retro-Remake
Date Created: 10-29-2025
Date Changed: 02-19-2026
License: MIT

Features:
    - Game loop with fixed timestep for consistent physics
    - State machine for main menu, galaxy map, sector map, combat, paused states
    - Hybrid State Machine + Game Object + Component architecture for Star Trek game objects
    - Object pooling for efficient memory management
    - Separated game logic from rendering for testability using MVC pattern
    - pygame-ce for game engine, PySide6 for UI/menus
    - Standard library first approach
    - Clean confident design patterns

Requirements:
    - Linux environment
    - Python 3.14+ for latest language features
    - pygame-ce (Community Edition) for game engine functionality
    - PySide6 for UI, menus, and settings

Classes:
    - StarTrekRetroRemake: Main application controller implementing MVC pattern

Functions:
    - None
"""

import sys
from pathlib import Path
from typing import Final, cast

import pygame
from PySide6.QtWidgets import QApplication

from ..engine.config_manager import initialize_config_manager
from .controller import GameController
from .model import GameModel
from .view import GameView

__version__: Final[str] = "0.0.31"


class StarTrekRetroRemake:
    """
    Main game application implementing MVC pattern.

    Coordinates the game model, view, and controller components.
    Manages the application lifecycle and system initialization.

    Attributes:
        model: Game logic and state management
        view: UI rendering and display management
        controller: Input handling and coordination
        running: Application execution state

    Public methods:
        run: Start the application main loop
        shutdown: Clean shutdown of the application

    Private methods:
        _initialize_systems: Initialize pygame-ce, PySide6, and configuration systems
        _cleanup: Clean up resources on shutdown
    """

    def __init__(self) -> None:
        """Initialize the Star Trek Retro Remake application."""
        # Initialize core systems
        self._initialize_systems()

        # Create MVC components
        self.model = GameModel()
        self.controller = GameController(self.model)
        self.view = GameView(self.controller)

        # Set up component relationships
        self.controller.set_view(self.view)

        # Application state
        self.running = True

    def run(self) -> None:
        """
        Start the application main loop.

        Runs the main game loop until the application is closed.
        """
        # Initialize the game (don't start the loop in controller)
        self.controller.start_new_game()

        # Show the view
        self.view.run()

        # Run the PySide6 event loop
        sys.exit(self.qt_app.exec())

    def shutdown(self) -> None:
        """Initiate clean shutdown of the application."""
        self.running = False
        self.controller.stop()
        self.view.close()
        self._cleanup()

    def _initialize_systems(self) -> None:
        """
        Initialize configuration, PyGame, and PySide6 systems.

        Initializes core game systems in the following order:
        1. Configuration manager (TOML config file loading)
        2. PyGame (game rendering engine)
        3. PySide6 (UI framework)

        The configuration manager must be initialized before creating
        the GameView, as the view requires access to display settings
        and other configuration values during initialization.
        """
        # Initialize configuration manager FIRST (required by other systems)
        # Path: STRR/src/game/application.py -> STRR/config/
        config_dir = Path(__file__).parent.parent.parent / "config"
        initialize_config_manager(config_dir)

        # Initialize PyGame for game rendering (without display)
        pygame.init()

        # Initialize PySide6 application
        if not QApplication.instance():
            self.qt_app = QApplication(sys.argv)
        else:
            self.qt_app = cast(QApplication, QApplication.instance())

    def _cleanup(self) -> None:
        """Clean up resources on shutdown."""
        # Cleanup pygame-ce
        pygame.quit()

        # Cleanup PySide6
        if self.qt_app:
            self.qt_app.quit()
