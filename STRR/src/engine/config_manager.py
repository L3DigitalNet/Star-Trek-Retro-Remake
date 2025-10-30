#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Star Trek Retro Remake - Configuration Manager

Description:
    Utility module for loading and saving TOML configuration files.
    Provides a clean interface for configuration management throughout
    the game with type-safe operations and caching support.

Author: Star Trek Retro Remake Development Team
Email: team@startrekretroremake.dev
GitHub: https://github.com/L3DigitalNet/Star-Trek-Retro-Remake
Date Created: 10-29-2025
Date Changed: 10-30-2025
License: Open Source

Features:
    - TOML configuration loading with Python 3.14+ stdlib
    - Type-safe configuration access with type hints
    - Configuration validation and error handling
    - Configuration caching for performance
    - Dot notation for nested value access

Requirements:
    - Python 3.14+ for tomllib in standard library
    - tomli_w for TOML writing functionality

Classes:
    - ConfigManager: Main configuration loading/saving interface

Functions:
    - load_config(): Load configuration from TOML
    - save_config(): Save configuration to TOML format
    - get_config_value(): Get configuration value using dot notation
    - set_config_value(): Set configuration value using dot notation
"""

__version__ = "0.0.11"

import tomllib
from pathlib import Path
from typing import Any, Dict, Union, Optional

# For TOML writing, we'll use tomli_w (lightweight, stdlib-compatible)
try:
    import tomli_w
except ImportError:
    # Fallback for development - will need tomli_w for production
    tomli_w = None

from game.exceptions import ConfigurationError


class ConfigManager:
    """Manages loading and saving of TOML/JSON configuration files."""

    def __init__(self, config_dir: Union[str, Path]):
        """
        Initialize ConfigManager with configuration directory.

        Args:
            config_dir: Path to configuration files directory
        """
        self.config_dir = Path(config_dir)
        self.config_cache: Dict[str, Dict[str, Any]] = {}

    def load_config(self, filename: str, use_cache: bool = True) -> Dict[str, Any]:
        """
        Load configuration from TOML file.

        Args:
            filename: Configuration filename (without extension)
            use_cache: Whether to use cached configuration data

        Returns:
            Dictionary containing configuration data

        Raises:
            ConfigurationError: If configuration cannot be loaded
        """
        if use_cache and filename in self.config_cache:
            return self.config_cache[filename]

        toml_path = self.config_dir / f"{filename}.toml"
        if not toml_path.exists():
            raise ConfigurationError(f"Configuration file not found: {toml_path}")

        try:
            config_data = self._load_toml(toml_path)
            if use_cache:
                self.config_cache[filename] = config_data
            return config_data
        except Exception as e:
            raise ConfigurationError(
                f"Failed to load TOML config '{toml_path}': {e}"
            ) from e

    def save_config(self, filename: str, config_data: Dict[str, Any]) -> None:
        """
        Save configuration to TOML format.

        Args:
            filename: Configuration filename (without extension)
            config_data: Configuration dictionary to save

        Raises:
            ConfigurationError: If configuration cannot be saved
        """
        if tomli_w is None:
            raise ConfigurationError("tomli_w not available - cannot save TOML files")

        toml_path = self.config_dir / f"{filename}.toml"

        try:
            # Ensure directory exists
            toml_path.parent.mkdir(parents=True, exist_ok=True)

            # Write TOML file
            with open(toml_path, "wb") as f:
                tomli_w.dump(config_data, f)

            # Update cache
            self.config_cache[filename] = config_data.copy()

        except Exception as e:
            raise ConfigurationError(
                f"Failed to save TOML config '{toml_path}': {e}"
            ) from e

    def clear_cache(self) -> None:
        """Clear configuration cache."""
        self.config_cache.clear()

    def get_config_value(
        self, filename: str, key_path: str, default: Any = None
    ) -> Any:
        """
        Get specific configuration value using dot notation.

        Args:
            filename: Configuration filename (without extension)
            key_path: Dot-separated path to configuration key (e.g., "display.width")
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        config = self.load_config(filename)

        # Navigate nested dictionary using dot notation
        current = config
        for key in key_path.split("."):
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default

        return current

    def set_config_value(self, filename: str, key_path: str, value: Any) -> None:
        """
        Set specific configuration value using dot notation.

        Args:
            filename: Configuration filename (without extension)
            key_path: Dot-separated path to configuration key
            value: Value to set
        """
        config = self.load_config(filename)

        # Navigate to parent dictionary
        current = config
        keys = key_path.split(".")
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]

        # Set the value
        current[keys[-1]] = value

        # Save updated configuration
        self.save_config(filename, config)

    def _load_toml(self, file_path: Path) -> Dict[str, Any]:
        """Load TOML file using Python 3.14+ stdlib."""
        with open(file_path, "rb") as f:
            return tomllib.load(f)


# Convenience functions for global configuration access
_global_config_manager: Optional[ConfigManager] = None


def initialize_config_manager(config_dir: Union[str, Path]) -> ConfigManager:
    """
    Initialize global configuration manager.

    Args:
        config_dir: Path to configuration directory

    Returns:
        ConfigManager instance
    """
    global _global_config_manager
    _global_config_manager = ConfigManager(config_dir)
    return _global_config_manager


def get_config_manager() -> ConfigManager:
    """
    Get global configuration manager instance.

    Returns:
        ConfigManager instance

    Raises:
        ConfigurationError: If config manager not initialized
    """
    if _global_config_manager is None:
        raise ConfigurationError(
            "Configuration manager not initialized. "
            "Call initialize_config_manager() first."
        )
    return _global_config_manager


def load_config(filename: str, use_cache: bool = True) -> Dict[str, Any]:
    """Convenience function to load configuration."""
    return get_config_manager().load_config(filename, use_cache)


def save_config(filename: str, config_data: Dict[str, Any]) -> None:
    """Convenience function to save configuration."""
    return get_config_manager().save_config(filename, config_data)


def get_config_value(filename: str, key_path: str, default: Any = None) -> Any:
    """Convenience function to get configuration value."""
    return get_config_manager().get_config_value(filename, key_path, default)


def set_config_value(filename: str, key_path: str, value: Any) -> None:
    """Convenience function to set configuration value."""
    return get_config_manager().set_config_value(filename, key_path, value)
