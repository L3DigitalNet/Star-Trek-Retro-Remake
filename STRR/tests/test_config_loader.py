#!/usr/bin/env python3
"""
Tests for engine configuration loader.

Description:
    Tests for the config_loader.py module that provides generic
    configuration loading with caching.

Author: Star Trek Retro Remake Development Team
Email: development@star-trek-retro-remake.org
Date Created: 11-01-2025
Date Changed: 11-01-2025
License: MIT
"""

import pytest
from unittest.mock import Mock, patch


class TestConfigLoader:
    """Test ConfigLoader class."""

    def test_config_loader_initialization(self):
        """Test that ConfigLoader can be initialized."""
        # Arrange & Act
        from src.engine.config_loader import ConfigLoader

        loader = ConfigLoader("game_settings", "game.combat")

        # Assert
        assert loader.config_file == "game_settings"
        assert loader.section == "game.combat"
        assert loader._cache is None

    def test_config_loader_data_property_lazy_loading(self):
        """Test that data property implements lazy loading."""
        # Arrange
        from src.engine.config_loader import ConfigLoader

        mock_manager = Mock()
        mock_manager.get_config_value.return_value = {"key": "value"}

        loader = ConfigLoader("game_settings", "game.combat")

        # Act - First access
        with patch("src.engine.config_loader.get_config_manager", return_value=mock_manager):
            data1 = loader.data

        # Assert - Data loaded and cached
        assert loader._cache is not None
        assert data1 == {"key": "value"}
        mock_manager.get_config_value.assert_called_once_with(
            "game_settings", "game.combat", {}
        )

        # Act - Second access
        data2 = loader.data

        # Assert - Same cached data, no additional calls
        assert data2 is data1
        assert mock_manager.get_config_value.call_count == 1

    def test_config_loader_data_no_section(self):
        """Test data property when no section is specified."""
        # Arrange
        from src.engine.config_loader import ConfigLoader

        mock_manager = Mock()
        mock_manager.load_config.return_value = {"section": {"key": "value"}}

        loader = ConfigLoader("game_settings", "")

        # Act
        with patch("src.engine.config_loader.get_config_manager", return_value=mock_manager):
            data = loader.data

        # Assert
        assert data == {"section": {"key": "value"}}
        mock_manager.load_config.assert_called_once_with("game_settings")

    def test_config_loader_get_with_default(self):
        """Test get method returns value or default."""
        # Arrange
        from src.engine.config_loader import ConfigLoader

        mock_manager = Mock()
        mock_manager.get_config_value.return_value = {
            "weapon_range": 5,
            "accuracy": 0.85,
        }

        loader = ConfigLoader("game_settings", "game.combat")

        with patch("src.engine.config_loader.get_config_manager", return_value=mock_manager):
            # Act & Assert - Existing key
            assert loader.get("weapon_range", 10) == 5
            assert loader.get("accuracy", 0.5) == 0.85

            # Act & Assert - Missing key with default
            assert loader.get("missing_key", "default") == "default"
            assert loader.get("another_missing", 100) == 100

    def test_config_loader_get_missing_no_default(self):
        """Test get method returns None for missing key without default."""
        # Arrange
        from src.engine.config_loader import ConfigLoader

        mock_manager = Mock()
        mock_manager.get_config_value.return_value = {"key": "value"}

        loader = ConfigLoader("game_settings", "game.combat")

        with patch("src.engine.config_loader.get_config_manager", return_value=mock_manager):
            # Act
            result = loader.get("missing_key")

            # Assert
            assert result is None

    def test_config_loader_refresh(self):
        """Test refresh method clears cache."""
        # Arrange
        from src.engine.config_loader import ConfigLoader

        mock_manager = Mock()
        mock_manager.get_config_value.return_value = {"key": "value"}

        loader = ConfigLoader("game_settings", "game.combat")

        with patch("src.engine.config_loader.get_config_manager", return_value=mock_manager):
            # Act - Load data
            _ = loader.data
            assert loader._cache is not None

            # Act - Refresh
            loader.refresh()

            # Assert - Cache cleared
            assert loader._cache is None


class TestHelperFunctions:
    """Test module-level helper functions."""

    def test_get_combat_config_returns_config_loader(self):
        """Test that get_combat_config returns ConfigLoader instance."""
        # Arrange & Act
        from src.engine.config_loader import get_combat_config, ConfigLoader

        config = get_combat_config()

        # Assert
        assert isinstance(config, ConfigLoader)
        assert config.config_file == "game_settings"
        assert config.section == "game.combat"

    def test_get_display_config_returns_config_loader(self):
        """Test that get_display_config returns ConfigLoader instance."""
        # Arrange & Act
        from src.engine.config_loader import get_display_config, ConfigLoader

        config = get_display_config()

        # Assert
        assert isinstance(config, ConfigLoader)
        assert config.config_file == "game_settings"
        assert config.section == "display"

    def test_get_audio_config_returns_config_loader(self):
        """Test that get_audio_config returns ConfigLoader instance."""
        # Arrange & Act
        from src.engine.config_loader import get_audio_config, ConfigLoader

        config = get_audio_config()

        # Assert
        assert isinstance(config, ConfigLoader)
        assert config.config_file == "game_settings"
        assert config.section == "audio"

    def test_helper_functions_return_cached_instances(self):
        """Test that helper functions return same instance (lru_cache)."""
        # Arrange & Act
        from src.engine.config_loader import (
            get_combat_config,
            get_display_config,
            get_audio_config,
        )

        # Get instances multiple times
        combat1 = get_combat_config()
        combat2 = get_combat_config()
        display1 = get_display_config()
        display2 = get_display_config()
        audio1 = get_audio_config()
        audio2 = get_audio_config()

        # Assert - Same instances returned (lru_cache)
        assert combat1 is combat2
        assert display1 is display2
        assert audio1 is audio2

        # Assert - Different instances for different configs
        assert combat1 is not display1
        assert combat1 is not audio1
        assert display1 is not audio1


class TestModuleMetadata:
    """Test module metadata."""

    def test_module_has_version(self):
        """Test that config_loader module has version attribute."""
        # Arrange & Act
        from src.engine import config_loader

        # Assert
        assert hasattr(config_loader, "__version__")
        assert isinstance(config_loader.__version__, str)


class TestTypeSafety:
    """Test type safety and generic type parameter."""

    def test_config_loader_with_dict_type(self):
        """Test ConfigLoader with dict type parameter."""
        # Arrange & Act
        from src.engine.config_loader import ConfigLoader

        loader: ConfigLoader[dict] = ConfigLoader("game_settings", "game.combat")

        # Assert - Type hints work (tested by mypy/type checker)
        assert loader.config_file == "game_settings"

    def test_get_method_type_hints(self):
        """Test get method with type hints."""
        # Arrange
        from src.engine.config_loader import ConfigLoader

        mock_manager = Mock()
        mock_manager.get_config_value.return_value = {"key": 42}

        loader = ConfigLoader[dict]("game_settings", "test")

        with patch("src.engine.config_loader.get_config_manager", return_value=mock_manager):
            # Act - Type hints should work for mypy
            value: int | None = loader.get("key", 0)

            # Assert
            assert value == 42
