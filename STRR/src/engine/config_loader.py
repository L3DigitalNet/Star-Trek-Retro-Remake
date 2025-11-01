#!/usr/bin/env python3
"""
Star Trek Retro Remake - Configuration Loader

Description:
    Generic configuration loader with caching for all game systems.
    Provides a clean, reusable pattern for loading configuration values
    with lazy initialization and type-safe access.

Author: Star Trek Retro Remake Development Team
Email: development@star-trek-retro-remake.org
GitHub: https://github.com/L3DigitalNet/Star-Trek-Retro-Remake
Date Created: 11-01-2025
Date Changed: 11-01-2025
License: MIT

Features:
    - Generic configuration loader with lazy initialization
    - Automatic caching for performance
    - Type-safe configuration access
    - Module-level helpers for common configs (combat, display, audio)
    - Consistent error handling
    - Eliminates duplicated config loading code

Requirements:
    - Linux environment
    - Python 3.14+ for latest language features

Known Issues:
    - None

Planned Features:
    - Configuration validation support
    - Hot-reloading of configuration files

Classes:
    - ConfigLoader: Generic configuration loader with caching

Functions:
    - get_combat_config: Get combat configuration
    - get_display_config: Get display configuration
    - get_audio_config: Get audio configuration
"""

from functools import lru_cache
from typing import Any, TypeVar, Generic, Final

from .config_manager import get_config_manager

__version__: Final[str] = "0.0.29"

T = TypeVar("T")


class ConfigLoader(Generic[T]):
    """
    Generic configuration loader with caching.

    This class provides a reusable pattern for loading configuration
    sections with lazy initialization and automatic caching.

    Usage:
        combat_config = ConfigLoader[dict]("game_settings", "game.combat")
        weapon_range = combat_config.get("weapon_range", 5)

    Attributes:
        config_file: Configuration filename (without .toml extension)
        section: Section path within config (dot notation)

    Public methods:
        get: Get configuration value with default
        refresh: Clear cache and reload
    """

    def __init__(self, config_file: str, section: str = ""):
        """
        Initialize configuration loader.

        Args:
            config_file: Configuration filename (without .toml)
            section: Section path (dot notation, e.g., "game.combat")
        """
        self.config_file = config_file
        self.section = section
        self._cache: dict[str, Any] | None = None

    @property
    def data(self) -> dict[str, Any]:
        """
        Lazy-loaded configuration data with caching.

        Returns:
            Configuration dictionary for the specified section
        """
        if self._cache is None:
            manager = get_config_manager()

            if self.section:
                self._cache = manager.get_config_value(
                    self.config_file, self.section, {}
                )
            else:
                self._cache = manager.load_config(self.config_file)

        return self._cache

    def get(self, key: str, default: T | None = None) -> T | None:
        """
        Get configuration value with default.

        Args:
            key: Configuration key
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        return self.data.get(key, default)

    def refresh(self) -> None:
        """Clear cache and reload configuration on next access."""
        self._cache = None


# Module-level helpers for common configurations
@lru_cache(maxsize=None)
def get_combat_config() -> ConfigLoader[dict]:
    """
    Get combat configuration loader.

    Returns:
        ConfigLoader for game.combat section

    Usage:
        config = get_combat_config()
        weapon_range = config.get("weapon_range", 5)
    """
    return ConfigLoader("game_settings", "game.combat")


@lru_cache(maxsize=None)
def get_display_config() -> ConfigLoader[dict]:
    """
    Get display configuration loader.

    Returns:
        ConfigLoader for display section

    Usage:
        config = get_display_config()
        screen_width = config.get("width", 1920)
    """
    return ConfigLoader("game_settings", "display")


@lru_cache(maxsize=None)
def get_audio_config() -> ConfigLoader[dict]:
    """
    Get audio configuration loader.

    Returns:
        ConfigLoader for audio section

    Usage:
        config = get_audio_config()
        music_volume = config.get("music_volume", 0.7)
    """
    return ConfigLoader("game_settings", "audio")
