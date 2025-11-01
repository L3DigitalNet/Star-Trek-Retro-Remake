#!/usr/bin/env python3
"""
Star Trek Retro Remake - Centralized Path Management

Description:
    Centralized path management for all project resources including
    configuration files, assets, data, and test resources. Provides
    a single source of truth for all file path calculations.

Author: Star Trek Retro Remake Development Team
Email: development@star-trek-retro-remake.org
GitHub: https://github.com/L3DigitalNet/Star-Trek-Retro-Remake
Date Created: 11-01-2025
Date Changed: 11-01-2025
License: MIT

Features:
    - Centralized path constants for all project directories
    - Single source of truth for resource locations
    - Type-safe path handling with pathlib
    - Easy to modify project structure
    - Better IDE support and autocomplete

Requirements:
    - Linux environment
    - Python 3.14+ for latest language features

Known Issues:
    - None

Planned Features:
    - Additional helper functions for asset discovery
    - Path validation utilities

Classes:
    - None

Functions:
    - get_asset_path: Get path to asset file by category
"""

from pathlib import Path
from typing import Final

__version__: Final[str] = "0.0.29"

# Root directories (calculated once at import)
# From STRR/src/engine/ -> STRR/ is 2 parents up
PROJECT_ROOT: Final[Path] = Path(__file__).parents[2]  # STRR/
SRC_ROOT: Final[Path] = PROJECT_ROOT / "src"
ASSETS_ROOT: Final[Path] = PROJECT_ROOT / "assets"
CONFIG_ROOT: Final[Path] = PROJECT_ROOT / "config"
TESTS_ROOT: Final[Path] = PROJECT_ROOT / "tests"

# Asset subdirectories
GRAPHICS_DIR: Final[Path] = ASSETS_ROOT / "graphics"
AUDIO_DIR: Final[Path] = ASSETS_ROOT / "audio"
DATA_DIR: Final[Path] = ASSETS_ROOT / "data"
MISSION_DATA_DIR: Final[Path] = DATA_DIR / "missions"
SECTOR_DATA_DIR: Final[Path] = DATA_DIR / "sectors"

# Configuration files
GAME_SETTINGS_FILE: Final[Path] = CONFIG_ROOT / "game_settings.toml"
GAME_DATA_FILE: Final[Path] = CONFIG_ROOT / "game_data.toml"
KEY_BINDINGS_FILE: Final[Path] = CONFIG_ROOT / "key_bindings.toml"

# Mission templates
MISSION_TEMPLATES_FILE: Final[Path] = DATA_DIR / "mission_templates.toml"


def get_asset_path(category: str, filename: str) -> Path:
    """
    Get path to asset file.

    Args:
        category: Asset category (graphics, audio, data)
        filename: Asset filename

    Returns:
        Full path to asset

    Raises:
        ValueError: If category is not recognized
    """
    category_map = {
        "graphics": GRAPHICS_DIR,
        "audio": AUDIO_DIR,
        "data": DATA_DIR,
    }

    if category not in category_map:
        raise ValueError(
            f"Unknown asset category: {category}. "
            f"Valid categories: {', '.join(category_map.keys())}"
        )

    return category_map[category] / filename
