#!/usr/bin/env python3
"""
Tests for Configuration Manager

Description:
    Test suite for config_manager module ensuring proper initialization,
    configuration loading, and error handling.

Author: Star Trek Retro Remake Development Team
Email: development@star-trek-retro-remake.org
GitHub: https://github.com/L3DigitalNet/Star-Trek-Retro-Remake
Date Created: 11-02-2025
Date Changed: 11-02-2025
License: MIT
"""

import tempfile
from pathlib import Path

import pytest
from src.engine.config_manager import (
    ConfigManager,
    get_config_manager,
    get_config_value,
    initialize_config_manager,
)
from src.game.exceptions import ConfigurationError


class TestConfigManager:
    """Test suite for ConfigManager class."""

    @pytest.fixture
    def temp_config_dir(self):
        """Create temporary config directory with test files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_dir = Path(tmpdir)

            # Create test config file
            test_config = config_dir / "test_settings.toml"
            test_config.write_text(
                """
[display]
width = 1280
height = 720
fps_limit = 60

[graphics]
quality = "high"
vsync = true
"""
            )

            # Create nested config file
            nested_config = config_dir / "nested.toml"
            nested_config.write_text(
                """
[game]
difficulty = "normal"

[game.player]
starting_resources = 1000
starting_crew = 100

[audio]
master_volume = 0.8
music_volume = 0.6
"""
            )

            yield config_dir

    @pytest.fixture
    def config_manager(self, temp_config_dir):
        """Create ConfigManager instance with temp directory."""
        return ConfigManager(temp_config_dir)

    def test_initialization(self, temp_config_dir):
        """Test ConfigManager initializes correctly."""
        # Arrange & Act
        manager = ConfigManager(temp_config_dir)

        # Assert
        assert manager.config_dir == temp_config_dir
        assert isinstance(manager.config_cache, dict)
        assert len(manager.config_cache) == 0

    def test_load_config_basic(self, config_manager):
        """Test loading configuration file."""
        # Arrange & Act
        config = config_manager.load_config("test_settings")

        # Assert
        assert config is not None
        assert "display" in config
        assert config["display"]["width"] == 1280
        assert config["display"]["height"] == 720

    def test_load_config_with_extension(self, config_manager):
        """Test loading configuration file with .toml extension."""
        # Arrange & Act
        config = config_manager.load_config("test_settings.toml")

        # Assert
        assert config is not None
        assert "display" in config
        assert config["display"]["width"] == 1280

    def test_load_config_caching(self, config_manager):
        """Test configuration caching works correctly."""
        # Arrange & Act
        config1 = config_manager.load_config("test_settings")
        config2 = config_manager.load_config("test_settings")

        # Assert
        assert config1 is config2  # Same object from cache
        assert "test_settings" in config_manager.config_cache

    def test_load_config_no_cache(self, config_manager):
        """Test loading without cache returns new object."""
        # Arrange & Act
        config1 = config_manager.load_config("test_settings", use_cache=False)
        config2 = config_manager.load_config("test_settings", use_cache=False)

        # Assert
        assert config1 is not config2  # Different objects

    def test_load_config_not_found(self, config_manager):
        """Test error when config file doesn't exist."""
        # Arrange, Act & Assert
        with pytest.raises(ConfigurationError) as exc_info:
            config_manager.load_config("nonexistent")

        assert "Configuration file not found" in str(exc_info.value)

    def test_get_config_value_simple(self, config_manager):
        """Test getting simple config value."""
        # Arrange & Act
        width = config_manager.get_config_value("test_settings", "display.width")

        # Assert
        assert width == 1280

    def test_get_config_value_nested(self, config_manager):
        """Test getting deeply nested config value."""
        # Arrange & Act
        starting_crew = config_manager.get_config_value(
            "nested", "game.player.starting_crew"
        )

        # Assert
        assert starting_crew == 100

    def test_get_config_value_default(self, config_manager):
        """Test default value returned when key not found."""
        # Arrange & Act
        result = config_manager.get_config_value(
            "test_settings", "nonexistent.key", default=42
        )

        # Assert
        assert result == 42

    def test_get_config_value_with_extension(self, config_manager):
        """Test getting config value with .toml extension in filename."""
        # Arrange & Act
        width = config_manager.get_config_value("test_settings.toml", "display.width")

        # Assert
        assert width == 1280

    def test_clear_cache(self, config_manager):
        """Test clearing configuration cache."""
        # Arrange
        config_manager.load_config("test_settings")
        assert len(config_manager.config_cache) > 0

        # Act
        config_manager.clear_cache()

        # Assert
        assert len(config_manager.config_cache) == 0


class TestGlobalConfigManager:
    """Test suite for global config manager functions."""

    @pytest.fixture(autouse=True)
    def reset_global_manager(self):
        """Reset global config manager before each test."""
        import src.engine.config_manager as cm

        cm._global_config_manager = None
        yield
        cm._global_config_manager = None

    @pytest.fixture
    def temp_config_dir(self):
        """Create temporary config directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_dir = Path(tmpdir)

            # Create test config
            test_config = config_dir / "game_settings.toml"
            test_config.write_text(
                """
[display]
game_surface_width = 1280
game_surface_height = 900
fps_limit = 60
"""
            )

            yield config_dir

    def test_initialize_config_manager(self, temp_config_dir):
        """Test initializing global config manager."""
        # Arrange & Act
        manager = initialize_config_manager(temp_config_dir)

        # Assert
        assert manager is not None
        assert isinstance(manager, ConfigManager)
        assert manager.config_dir == temp_config_dir

    def test_get_config_manager_not_initialized(self):
        """Test error when accessing uninitialized config manager."""
        # Arrange, Act & Assert
        with pytest.raises(ConfigurationError) as exc_info:
            get_config_manager()

        assert "not initialized" in str(exc_info.value)

    def test_get_config_manager_after_init(self, temp_config_dir):
        """Test getting config manager after initialization."""
        # Arrange
        initialize_config_manager(temp_config_dir)

        # Act
        manager = get_config_manager()

        # Assert
        assert manager is not None
        assert isinstance(manager, ConfigManager)

    def test_get_config_value_convenience_function(self, temp_config_dir):
        """Test convenience function for getting config values."""
        # Arrange
        initialize_config_manager(temp_config_dir)

        # Act
        width = get_config_value("game_settings", "display.game_surface_width")

        # Assert
        assert width == 1280

    def test_get_config_value_with_default(self, temp_config_dir):
        """Test convenience function with default value."""
        # Arrange
        initialize_config_manager(temp_config_dir)

        # Act
        value = get_config_value("game_settings", "nonexistent.key", default=9999)

        # Assert
        assert value == 9999


class TestApplicationIntegration:
    """Test config manager integration with application startup."""

    @pytest.fixture
    def game_config_dir(self):
        """Use actual game config directory."""
        return Path(__file__).parent.parent / "config"

    @pytest.fixture(autouse=True)
    def reset_global_manager(self):
        """Reset global config manager before each test."""
        import src.engine.config_manager as cm

        cm._global_config_manager = None
        yield
        cm._global_config_manager = None

    def test_application_config_initialization(self, game_config_dir):
        """Test that application can initialize config manager correctly."""
        # Arrange & Act
        manager = initialize_config_manager(game_config_dir)

        # Assert
        assert manager is not None
        assert game_config_dir.exists()
        assert (game_config_dir / "game_settings.toml").exists()

    def test_view_can_access_config_after_init(self, game_config_dir):
        """Test that view can access config values after initialization."""
        # Arrange
        initialize_config_manager(game_config_dir)

        # Act
        game_width = get_config_value(
            "game_settings.toml", "display.game_surface_width", 1280
        )
        game_height = get_config_value(
            "game_settings.toml", "display.game_surface_height", 900
        )

        # Assert
        assert isinstance(game_width, int)
        assert isinstance(game_height, int)
        assert game_width > 0
        assert game_height > 0

    def test_config_files_exist(self, game_config_dir):
        """Test that required config files exist."""
        # Arrange & Act
        game_settings = game_config_dir / "game_settings.toml"
        game_data = game_config_dir / "game_data.toml"
        key_bindings = game_config_dir / "key_bindings.toml"

        # Assert
        assert game_settings.exists(), "game_settings.toml missing"
        assert game_data.exists(), "game_data.toml missing"
        assert key_bindings.exists(), "key_bindings.toml missing"
