#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
Date Changed: 10-29-2025
License: MIT

Features:
    - Game loop with fixed timestep for consistent physics
    - State machine for main menu, galaxy map, sector map, combat, paused states
    - Hybrid State Machine + Game Object + Component architecture for Star Trek game objects
    - Object pooling for efficient memory management
    - Separated game logic from rendering for testability using MVC pattern
    - PyGame for game engine, PySide6 for UI/menus
    - Standard library first approach
    - Clean confident design patterns

Requirements:
    - Linux environment
    - Python 3.14+ for latest language features
    - PyGame for game engine functionality
    - PySide6 for UI, menus, and settings

Classes:
    - StarTrekRetroRemake: Main application controller implementing MVC pattern

Functions:
    - None
"""

import sys
from typing import Final

import pygame
from PySide6.QtWidgets import QApplication

from game.controller import GameController
from game.model import GameModel
from game.view import GameView

__version__: Final[str] = "0.0.1"


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
        _initialize_systems: Initialize PyGame and PySide6 systems
        _cleanup: Clean up resources on shutdown
    """

    def __init__(self):
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
        # Start the game controller
        self.controller.start()

        # Run the PySide6 event loop
        self.view.run()

        # Clean shutdown
        self._cleanup()

    def shutdown(self) -> None:
        """Initiate clean shutdown of the application."""
        self.running = False
        self.controller.stop()
        self.view.close()

    def _initialize_systems(self) -> None:
        """Initialize PyGame and PySide6 systems."""
        # Initialize PyGame for game rendering
        pygame.init()

        # Initialize PySide6 application
        if not QApplication.instance():
            self.qt_app = QApplication(sys.argv)
        else:
            self.qt_app = QApplication.instance()

    def _cleanup(self) -> None:
        """Clean up resources on shutdown."""
        # Cleanup PyGame
        pygame.quit()

        # Cleanup PySide6
        if self.qt_app:
            self.qt_app.quit()