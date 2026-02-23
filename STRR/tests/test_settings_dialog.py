#!/usr/bin/env python3
"""
Star Trek Retro Remake - Settings Dialog Tests

Tests for settings dialog and all configuration tabs.
"""

import pytest

pytest.importorskip("PySide6")


import sys
from pathlib import Path
from unittest.mock import Mock

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.game.ui.settings_dialog import (
    AudioTab,
    GameplayTab,
    GraphicsTab,
    KeyBindingsTab,
    SettingsDialog,
    load_settings_from_toml,
    save_settings_to_toml,
)

pytestmark = pytest.mark.gui


@pytest.fixture
def sample_settings():
    """Create sample settings dictionary."""
    return {
        "display": {
            "width": 1280,
            "height": 720,
            "fullscreen": False,
            "vsync": True,
            "target_fps": 60,
        },
        "audio": {
            "master_volume": 80,
            "music_volume": 70,
            "effects_volume": 90,
        },
        "gameplay": {
            "difficulty": "Normal",
            "autosave_interval": 5,
            "tutorial_hints": True,
            "show_grid_coordinates": True,
        },
        "key_bindings": {
            "move": "M",
            "fire": "F",
            "end_turn": "Space",
            "open_map": "Tab",
            "settings": "Esc",
        },
    }


@pytest.fixture
def temp_config_file(tmp_path, sample_settings):
    """Create temporary config file for testing."""
    import tomli_w

    config_path = tmp_path / "game_settings.toml"
    with config_path.open("wb") as f:
        tomli_w.dump(sample_settings, f)
    return config_path


class TestSettingsFileOperations:
    """Test TOML settings file operations."""

    def test_load_settings_from_existing_file(self, temp_config_file, sample_settings):
        """Test loading settings from existing TOML file."""
        loaded_settings = load_settings_from_toml(temp_config_file)

        # Verify all sections loaded
        assert "display" in loaded_settings
        assert "audio" in loaded_settings
        assert "gameplay" in loaded_settings
        assert "key_bindings" in loaded_settings

        # Verify specific values
        assert loaded_settings["display"]["width"] == 1280
        assert loaded_settings["audio"]["master_volume"] == 80

    def test_load_settings_from_nonexistent_file(self, tmp_path):
        """Test loading from nonexistent file returns empty dict."""
        nonexistent = tmp_path / "nonexistent.toml"
        settings = load_settings_from_toml(nonexistent)

        assert settings == {}

    def test_save_settings_to_file(self, tmp_path, sample_settings):
        """Test saving settings to TOML file."""
        config_path = tmp_path / "new_settings.toml"

        # Save settings
        save_settings_to_toml(sample_settings, config_path)

        # Verify file was created
        assert config_path.exists()

        # Load and verify
        loaded = load_settings_from_toml(config_path)
        assert loaded["display"]["width"] == sample_settings["display"]["width"]


class TestGraphicsTab:
    """Test GraphicsTab component."""

    def test_graphics_tab_initialization(self, qtbot, sample_settings):
        """Test graphics tab initializes with settings."""
        tab = GraphicsTab(sample_settings)
        qtbot.addWidget(tab)

        # Verify resolution combo box
        assert tab.resolution_combo.currentText() == "1280x720"

        # Verify checkboxes
        assert not tab.fullscreen_check.isChecked()
        assert tab.vsync_check.isChecked()

        # Verify FPS combo
        assert tab.fps_combo.currentText() == "60"

    def test_graphics_tab_get_settings(self, qtbot, sample_settings):
        """Test getting settings from graphics tab."""
        tab = GraphicsTab(sample_settings)
        qtbot.addWidget(tab)

        # Change some settings
        tab.resolution_combo.setCurrentText("1920x1080")
        tab.fullscreen_check.setChecked(True)
        tab.vsync_check.setChecked(False)
        tab.fps_combo.setCurrentText("144")

        # Get settings
        settings = tab.get_settings()

        # Verify changes
        assert settings["display"]["width"] == 1920
        assert settings["display"]["height"] == 1080
        assert settings["display"]["fullscreen"]
        assert not settings["display"]["vsync"]
        assert settings["display"]["target_fps"] == 144

    def test_graphics_tab_unlimited_fps(self, qtbot, sample_settings):
        """Test unlimited FPS option."""
        tab = GraphicsTab(sample_settings)
        qtbot.addWidget(tab)

        # Set to unlimited
        tab.fps_combo.setCurrentText("Unlimited")

        settings = tab.get_settings()
        assert settings["display"]["target_fps"] == 0


class TestAudioTab:
    """Test AudioTab component."""

    def test_audio_tab_initialization(self, qtbot, sample_settings):
        """Test audio tab initializes with settings."""
        tab = AudioTab(sample_settings)
        qtbot.addWidget(tab)

        # Verify slider values
        assert tab.master_slider.value() == 80
        assert tab.music_slider.value() == 70
        assert tab.effects_slider.value() == 90

    def test_audio_tab_get_settings(self, qtbot, sample_settings):
        """Test getting settings from audio tab."""
        tab = AudioTab(sample_settings)
        qtbot.addWidget(tab)

        # Change slider values
        tab.master_slider.setValue(50)
        tab.music_slider.setValue(60)
        tab.effects_slider.setValue(40)

        # Get settings
        settings = tab.get_settings()

        # Verify changes
        assert settings["audio"]["master_volume"] == 50
        assert settings["audio"]["music_volume"] == 60
        assert settings["audio"]["effects_volume"] == 40

    def test_audio_tab_slider_labels_update(self, qtbot, sample_settings):
        """Test slider labels update with value."""
        tab = AudioTab(sample_settings)
        qtbot.addWidget(tab)

        # Change value
        tab.master_slider.setValue(75)

        # Verify label updated
        assert "75%" in tab.master_label.text()


class TestGameplayTab:
    """Test GameplayTab component."""

    def test_gameplay_tab_initialization(self, qtbot, sample_settings):
        """Test gameplay tab initializes with settings."""
        tab = GameplayTab(sample_settings)
        qtbot.addWidget(tab)

        # Verify combo box
        assert tab.difficulty_combo.currentText() == "Normal"

        # Verify checkboxes
        assert tab.hints_check.isChecked()
        assert tab.autosave_check.isChecked()
        assert tab.animations_check.isChecked()

    def test_gameplay_tab_get_settings(self, qtbot, sample_settings):
        """Test gameplay tab returns current settings."""
        tab = GameplayTab(sample_settings)
        qtbot.addWidget(tab)

        # Modify settings
        tab.difficulty_combo.setCurrentText("Hard")
        tab.autosave_check.setChecked(False)
        tab.hints_check.setChecked(False)
        tab.animations_check.setChecked(False)

        settings = tab.get_settings()

        # Verify returned settings (GameplayTab returns nested dict)
        assert settings["gameplay"]["difficulty"] == "Hard"
        assert not settings["gameplay"]["auto_save"]
        assert not settings["gameplay"]["tutorial_hints"]
        assert not settings["gameplay"]["combat_animations"]


class TestKeyBindingsTab:
    """Test KeyBindingsTab component."""

    def test_keybindings_tab_initialization(self, qtbot, sample_settings):
        """Test key bindings tab initializes with settings."""
        tab = KeyBindingsTab(sample_settings)
        qtbot.addWidget(tab)

        # Verify buttons exist and have correct text
        assert "move" in tab.key_buttons
        assert tab.key_buttons["move"].text() == "M"
        assert tab.key_buttons["fire"].text() == "F"

    def test_keybindings_tab_get_settings(self, qtbot, sample_settings):
        """Test getting settings from key bindings tab."""
        tab = KeyBindingsTab(sample_settings)
        qtbot.addWidget(tab)

        # Change a key binding
        tab.key_buttons["move"].setText("W")

        # Get settings
        settings = tab.get_settings()

        # Verify change
        assert settings["key_bindings"]["move"] == "W"

    def test_keybindings_tab_reset_defaults(self, qtbot, sample_settings):
        """Test resetting key bindings to defaults."""
        tab = KeyBindingsTab(sample_settings)
        qtbot.addWidget(tab)

        # Change some bindings
        tab.key_buttons["move"].setText("X")
        tab.key_buttons["fire"].setText("Y")

        # Reset to defaults
        tab._reset_defaults()

        # Verify defaults restored
        assert tab.key_buttons["move"].text() == "M"
        assert tab.key_buttons["fire"].text() == "F"
        assert tab.key_buttons["end_turn"].text() == "Space"


class TestSettingsDialog:
    """Test main SettingsDialog."""

    def test_settings_dialog_initialization(self, qtbot, temp_config_file):
        """Test settings dialog initializes correctly."""
        dialog = SettingsDialog(temp_config_file)
        qtbot.addWidget(dialog)

        # Verify window properties
        assert "Settings" in dialog.windowTitle()
        assert dialog.minimumWidth() >= 500
        assert dialog.minimumHeight() >= 400

        # Verify tabs exist
        assert dialog.tabs.count() == 4
        assert dialog.graphics_tab is not None
        assert dialog.audio_tab is not None
        assert dialog.gameplay_tab is not None
        assert dialog.keybindings_tab is not None

    def test_settings_dialog_gather_settings(self, qtbot, temp_config_file):
        """Test gathering settings from all tabs."""
        dialog = SettingsDialog(temp_config_file)
        qtbot.addWidget(dialog)

        # Modify some settings in each tab
        dialog.graphics_tab.fullscreen_check.setChecked(True)
        dialog.audio_tab.master_slider.setValue(50)
        dialog.gameplay_tab.difficulty_combo.setCurrentText("Hard")
        dialog.keybindings_tab.key_buttons["move"].setText("W")

        # Gather settings
        all_settings = dialog._gather_settings()

        # Verify all sections present
        assert "display" in all_settings
        assert "audio" in all_settings
        assert "gameplay" in all_settings
        assert "key_bindings" in all_settings

        # Verify specific changes
        assert all_settings["display"]["fullscreen"]
        assert all_settings["audio"]["master_volume"] == 50
        assert all_settings["gameplay"]["difficulty"] == "Hard"
        assert all_settings["key_bindings"]["move"] == "W"

    def test_settings_dialog_apply_saves_file(self, qtbot, temp_config_file):
        """Test apply button saves settings to file."""
        dialog = SettingsDialog(temp_config_file)
        qtbot.addWidget(dialog)

        # Change a setting
        dialog.graphics_tab.fullscreen_check.setChecked(True)

        # Apply settings
        dialog._on_apply()

        # Verify file was updated
        loaded = load_settings_from_toml(temp_config_file)
        assert loaded["display"]["fullscreen"]

    def test_settings_dialog_ok_saves_and_closes(self, qtbot, temp_config_file):
        """Test OK button saves and closes dialog."""
        dialog = SettingsDialog(temp_config_file)
        qtbot.addWidget(dialog)

        # Change a setting
        dialog.audio_tab.master_slider.setValue(33)

        # Mock accept method to prevent actual closing in test
        dialog.accept = Mock()

        # Click OK
        dialog._on_ok()

        # Verify file was saved
        loaded = load_settings_from_toml(temp_config_file)
        assert loaded["audio"]["master_volume"] == 33

        # Verify dialog was accepted
        dialog.accept.assert_called_once()


class TestSettingsDialogIntegration:
    """Test integration scenarios for settings dialog."""

    def test_load_save_roundtrip(self, qtbot, tmp_path, sample_settings):
        """Test loading, modifying, and saving settings."""
        config_path = tmp_path / "roundtrip_settings.toml"

        # Save initial settings
        save_settings_to_toml(sample_settings, config_path)

        # Load in dialog
        dialog = SettingsDialog(config_path)
        qtbot.addWidget(dialog)

        # Modify multiple settings
        dialog.graphics_tab.resolution_combo.setCurrentText("1920x1080")
        dialog.audio_tab.music_slider.setValue(45)
        dialog.gameplay_tab.autosave_check.setChecked(False)

        # Save
        dialog._on_apply()

        # Load fresh and verify
        loaded = load_settings_from_toml(config_path)
        assert loaded["display"]["width"] == 1920
        assert loaded["display"]["height"] == 1080
        assert loaded["audio"]["music_volume"] == 45
        assert not loaded["gameplay"]["auto_save"]

    def test_settings_persist_across_dialogs(self, qtbot, temp_config_file):
        """Test settings persist when reopening dialog."""
        # First dialog - change settings
        dialog1 = SettingsDialog(temp_config_file)
        qtbot.addWidget(dialog1)
        dialog1.graphics_tab.vsync_check.setChecked(False)
        dialog1._on_apply()

        # Second dialog - verify changes persisted
        dialog2 = SettingsDialog(temp_config_file)
        qtbot.addWidget(dialog2)
        assert not dialog2.graphics_tab.vsync_check.isChecked()
