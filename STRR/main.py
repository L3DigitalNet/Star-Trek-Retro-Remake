#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Star Trek Retro Remake - Main Entry Point

Description:
    Main entry point for the Star Trek Retro Remake game. Initializes the game
    application and starts the main game loop following the hybrid architecture
    patterns.

Author: Star Trek Retro Remake Development Team
Email: development@star-trek-retro-remake.org
GitHub: https://github.com/L3DigitalNet/Star-Trek-Retro-Remake
Date Created: 10-29-2025
Date Changed: 10-30-2025
License: MIT

Features:
    - Game loop with fixed timestep for consistent physics
    - State machine for main menu, galaxy map, sector map, combat, paused states
    - Hybrid State Machine + Game Object + Component architecture for Star Trek game objects
    - Object pooling for efficient memory management
    - Separated game logic from rendering for testability using MVC pattern
    - pygame-ce (Community Edition) for game engine, PySide6 for UI/menus
    - Standard library first approach
    - Clean confident design patterns

Requirements:
    - Linux environment
    - Python 3.14+ for latest language features
    - pygame-ce (Community Edition) for game engine functionality
    - PySide6 for UI, menus, and settings
    - Custom utilities located at ../common_lib/

Known Issues:
    - Initial implementation - core features in development
    - Error handling deferred until v1.0.0

Planned Features:
    - Complete game state system implementation
    - Full combat and exploration mechanics
    - Save/load functionality

Classes:
    - StarTrekRetroRemake: Main application controller

Functions:
    - main(): Entry point function
"""

import sys
import logging
from pathlib import Path
from typing import Final

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Add src directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.game.application import StarTrekRetroRemake

__version__: Final[str] = "0.0.10"


def main() -> None:
    """
    Main entry point for the Star Trek Retro Remake game.

    Initializes the game application and starts the main game loop.
    """
    # Create and run the game application
    game = StarTrekRetroRemake()
    game.run()


if __name__ == "__main__":
    main()
