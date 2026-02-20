#!/usr/bin/env python3
"""
Tests for engine path management.

Description:
    Tests for the paths.py module that provides centralized path
    management for all project resources.

Author: Star Trek Retro Remake Development Team
Email: development@star-trek-retro-remake.org
Date Created: 11-01-2025
Date Changed: 11-01-2025
License: MIT
"""

from pathlib import Path

import pytest

pytestmark = pytest.mark.unit


class TestPathConstants:
    """Test path constant definitions."""

    def test_project_root_exists(self):
        """Test that PROJECT_ROOT is defined and is a Path."""
        # Arrange & Act
        from src.engine.paths import PROJECT_ROOT

        # Assert
        assert isinstance(PROJECT_ROOT, Path)
        assert PROJECT_ROOT.name == "STRR"

    def test_src_root_relationship(self):
        """Test that SRC_ROOT is correctly related to PROJECT_ROOT."""
        # Arrange
        from src.engine.paths import PROJECT_ROOT, SRC_ROOT

        # Act & Assert
        assert SRC_ROOT == PROJECT_ROOT / "src"
        assert SRC_ROOT.parent == PROJECT_ROOT

    def test_config_root_relationship(self):
        """Test that CONFIG_ROOT is correctly related to PROJECT_ROOT."""
        # Arrange
        from src.engine.paths import CONFIG_ROOT, PROJECT_ROOT

        # Act & Assert
        assert CONFIG_ROOT == PROJECT_ROOT / "config"
        assert CONFIG_ROOT.parent == PROJECT_ROOT

    def test_assets_root_relationship(self):
        """Test that ASSETS_ROOT is correctly related to PROJECT_ROOT."""
        # Arrange
        from src.engine.paths import ASSETS_ROOT, PROJECT_ROOT

        # Act & Assert
        assert ASSETS_ROOT == PROJECT_ROOT / "assets"
        assert ASSETS_ROOT.parent == PROJECT_ROOT

    def test_tests_root_relationship(self):
        """Test that TESTS_ROOT is correctly related to PROJECT_ROOT."""
        # Arrange
        from src.engine.paths import PROJECT_ROOT, TESTS_ROOT

        # Act & Assert
        assert TESTS_ROOT == PROJECT_ROOT / "tests"
        assert TESTS_ROOT.parent == PROJECT_ROOT


class TestAssetDirectories:
    """Test asset directory constants."""

    def test_graphics_dir_relationship(self):
        """Test that GRAPHICS_DIR is correctly related to ASSETS_ROOT."""
        # Arrange
        from src.engine.paths import ASSETS_ROOT, GRAPHICS_DIR

        # Act & Assert
        assert GRAPHICS_DIR == ASSETS_ROOT / "graphics"

    def test_audio_dir_relationship(self):
        """Test that AUDIO_DIR is correctly related to ASSETS_ROOT."""
        # Arrange
        from src.engine.paths import ASSETS_ROOT, AUDIO_DIR

        # Act & Assert
        assert AUDIO_DIR == ASSETS_ROOT / "audio"

    def test_data_dir_relationship(self):
        """Test that DATA_DIR is correctly related to ASSETS_ROOT."""
        # Arrange
        from src.engine.paths import ASSETS_ROOT, DATA_DIR

        # Act & Assert
        assert DATA_DIR == ASSETS_ROOT / "data"

    def test_mission_data_dir_relationship(self):
        """Test that MISSION_DATA_DIR is correctly related to DATA_DIR."""
        # Arrange
        from src.engine.paths import DATA_DIR, MISSION_DATA_DIR

        # Act & Assert
        assert MISSION_DATA_DIR == DATA_DIR / "missions"

    def test_sector_data_dir_relationship(self):
        """Test that SECTOR_DATA_DIR is correctly related to DATA_DIR."""
        # Arrange
        from src.engine.paths import DATA_DIR, SECTOR_DATA_DIR

        # Act & Assert
        assert SECTOR_DATA_DIR == DATA_DIR / "sectors"


class TestConfigurationFiles:
    """Test configuration file path constants."""

    def test_game_settings_file(self):
        """Test that GAME_SETTINGS_FILE points to correct location."""
        # Arrange
        from src.engine.paths import CONFIG_ROOT, GAME_SETTINGS_FILE

        # Act & Assert
        assert GAME_SETTINGS_FILE == CONFIG_ROOT / "game_settings.toml"
        assert GAME_SETTINGS_FILE.name == "game_settings.toml"

    def test_game_data_file(self):
        """Test that GAME_DATA_FILE points to correct location."""
        # Arrange
        from src.engine.paths import CONFIG_ROOT, GAME_DATA_FILE

        # Act & Assert
        assert GAME_DATA_FILE == CONFIG_ROOT / "game_data.toml"
        assert GAME_DATA_FILE.name == "game_data.toml"

    def test_key_bindings_file(self):
        """Test that KEY_BINDINGS_FILE points to correct location."""
        # Arrange
        from src.engine.paths import CONFIG_ROOT, KEY_BINDINGS_FILE

        # Act & Assert
        assert KEY_BINDINGS_FILE == CONFIG_ROOT / "key_bindings.toml"
        assert KEY_BINDINGS_FILE.name == "key_bindings.toml"


class TestMissionFiles:
    """Test mission file path constants."""

    def test_mission_templates_file(self):
        """Test that MISSION_TEMPLATES_FILE points to correct location."""
        # Arrange
        from src.engine.paths import DATA_DIR, MISSION_TEMPLATES_FILE

        # Act & Assert
        assert MISSION_TEMPLATES_FILE == DATA_DIR / "mission_templates.toml"
        assert MISSION_TEMPLATES_FILE.name == "mission_templates.toml"


class TestGetAssetPath:
    """Test get_asset_path function."""

    def test_get_graphics_asset_path(self):
        """Test getting path for graphics asset."""
        # Arrange
        from src.engine.paths import GRAPHICS_DIR, get_asset_path

        # Act
        result = get_asset_path("graphics", "ship.png")

        # Assert
        assert result == GRAPHICS_DIR / "ship.png"

    def test_get_audio_asset_path(self):
        """Test getting path for audio asset."""
        # Arrange
        from src.engine.paths import AUDIO_DIR, get_asset_path

        # Act
        result = get_asset_path("audio", "phaser.wav")

        # Assert
        assert result == AUDIO_DIR / "phaser.wav"

    def test_get_data_asset_path(self):
        """Test getting path for data asset."""
        # Arrange
        from src.engine.paths import DATA_DIR, get_asset_path

        # Act
        result = get_asset_path("data", "mission.toml")

        # Assert
        assert result == DATA_DIR / "mission.toml"

    def test_get_asset_path_invalid_category(self):
        """Test that invalid category raises ValueError."""
        # Arrange
        from src.engine.paths import get_asset_path

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            get_asset_path("invalid_category", "file.txt")

        assert "Unknown asset category" in str(exc_info.value)
        assert "invalid_category" in str(exc_info.value)


class TestModuleMetadata:
    """Test module metadata."""

    def test_module_has_version(self):
        """Test that paths module has version attribute."""
        # Arrange & Act
        from src.engine import paths

        # Assert
        assert hasattr(paths, "__version__")
        assert isinstance(paths.__version__, str)


class TestPathsExist:
    """Test that critical paths exist in the actual project."""

    def test_project_root_exists_on_filesystem(self):
        """Test that PROJECT_ROOT actually exists."""
        # Arrange
        from src.engine.paths import PROJECT_ROOT

        # Act & Assert
        assert PROJECT_ROOT.exists()
        assert PROJECT_ROOT.is_dir()

    def test_config_root_exists_on_filesystem(self):
        """Test that CONFIG_ROOT actually exists."""
        # Arrange
        from src.engine.paths import CONFIG_ROOT

        # Act & Assert
        assert CONFIG_ROOT.exists()
        assert CONFIG_ROOT.is_dir()

    def test_assets_root_exists_on_filesystem(self):
        """Test that ASSETS_ROOT actually exists."""
        # Arrange
        from src.engine.paths import ASSETS_ROOT

        # Act & Assert
        assert ASSETS_ROOT.exists()
        assert ASSETS_ROOT.is_dir()

    def test_game_settings_file_exists_on_filesystem(self):
        """Test that GAME_SETTINGS_FILE actually exists."""
        # Arrange
        from src.engine.paths import GAME_SETTINGS_FILE

        # Act & Assert
        assert GAME_SETTINGS_FILE.exists()
        assert GAME_SETTINGS_FILE.is_file()
