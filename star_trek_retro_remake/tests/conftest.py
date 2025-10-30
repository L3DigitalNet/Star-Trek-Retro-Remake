#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Star Trek Retro Remake - Test Configuration

Description:
    pytest configuration and fixtures for testing the Star Trek Retro Remake game.
    Provides shared test setup and utilities.

Author: Star Trek Retro Remake Development Team
Email: development@star-trek-retro-remake.org
GitHub: https://github.com/L3DigitalNet/Star-Trek-Retro-Remake
Date Created: 10-29-2025
Date Changed: 10-29-2025
License: MIT

Features:
    - pytest fixtures for game components
    - Test utilities and helpers
    - Mock objects for testing
    - Test data generation

Requirements:
    - Linux environment
    - Python 3.14+ for latest language features
    - pytest framework for testing

Functions:
    - Various pytest fixtures for testing
"""

import sys
import pytest
from typing import Final
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from src.game.model import GameModel
from src.game.entities.base import GridPosition
from src.game.entities.starship import Starship
from src.game.maps.galaxy import GalaxyMap
from src.game.maps.sector import SectorMap

__version__: Final[str] = "0.0.1"


@pytest.fixture
def grid_position():
    """Provide a test grid position."""
    return GridPosition(5, 5, 1)


@pytest.fixture
def test_starship(grid_position):
    """Provide a test starship for testing."""
    return Starship(grid_position, "Constitution", "Test Ship")


@pytest.fixture
def game_model():
    """Provide a fresh game model instance for testing."""
    return GameModel()


@pytest.fixture
def initialized_game_model(game_model):
    """Provide an initialized game model with a new game."""
    game_model.initialize_new_game()
    return game_model


@pytest.fixture
def galaxy_map():
    """Provide a test galaxy map."""
    return GalaxyMap((5, 5))


@pytest.fixture
def sector_map():
    """Provide a test sector map."""
    return SectorMap((0, 0), "standard")


@pytest.fixture
def combat_scenario(initialized_game_model):
    """Set up a combat scenario for testing."""
    # Create an enemy ship
    enemy_position = GridPosition(7, 7, 1)
    enemy_ship = Starship(enemy_position, "Miranda", "Enemy Ship")
    enemy_ship.faction = "hostile"

    # Add enemy to game
    initialized_game_model.game_objects.append(enemy_ship)
    initialized_game_model.current_sector.place_entity(enemy_ship, enemy_position)

    return {
        "model": initialized_game_model,
        "player_ship": initialized_game_model.player_ship,
        "enemy_ship": enemy_ship
    }