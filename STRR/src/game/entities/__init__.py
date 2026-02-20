#!/usr/bin/env python3
"""
Star Trek Retro Remake - Entities Package

Description:
    Game entities package implementing the Game Object pattern with component
    composition for Star Trek game objects.

Author: Star Trek Retro Remake Development Team
Date Created: 10-29-2025
Date Changed: 10-30-2025
License: MIT
"""

from typing import Final

from .base import GameObject, GridPosition
from .starship import SpaceStation, Starship

__version__: Final[str] = "0.0.31"

__all__ = [
    "GridPosition",
    "GameObject",
    "Starship",
    "SpaceStation",
]
