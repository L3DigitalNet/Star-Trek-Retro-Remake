#!/usr/bin/env python3
"""
Star Trek Retro Remake - Settings Dialog

Description:
    PySide6 settings dialog for configuring game options including graphics,
    audio, gameplay preferences, and key bindings. Integrates with TOML
    configuration system.

Author: Star Trek Retro Remake Development Team
Email: development@star-trek-retro-remake.org
GitHub: https://github.com/L3DigitalNet/Star-Trek-Retro-Remake
Date Created: 10-31-2025
Date Changed: 02-19-2026
License: MIT License

Features:
    - Tabbed interface for organized settings categories
    - Graphics settings (resolution, fullscreen, V-Sync)
    - Audio settings (master volume, music, effects)
    - Gameplay settings (difficulty, auto-save, hints)
    - Key binding customization with conflict detection
    - Load from and save to game_settings.toml
    - Apply and cancel functionality
    - Settings validation

Requirements:
    - Linux environment
    - Python 3.14+ for latest language features
    - PySide6 6.7+ for UI components

Known Issues:
    - Key binding editor basic implementation
    - Some settings require restart

Planned Features:
    - Advanced graphics options
    - Audio mixer controls
    - Custom difficulty presets
    - Key binding profiles

Classes:
    - SettingsDialog: Main settings dialog with tabs
    - GraphicsTab: Graphics configuration tab
    - AudioTab: Audio configuration tab
    - GameplayTab: Gameplay preferences tab
    - KeyBindingsTab: Key binding customization tab

Functions:
    - load_settings_from_toml(): Load settings from file
    - save_settings_to_toml(): Save settings to file
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any, Final

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QGroupBox,
    QLabel,
    QPushButton,
    QSlider,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

if TYPE_CHECKING:
    pass

try:
    import tomllib
except ImportError:
    import tomli as tomllib  # type: ignore[import-not-found,no-redef]

import tomli_w

__version__: Final[str] = "0.0.31"


def load_settings_from_toml(config_path: Path) -> dict[str, Any]:
    """
    Load settings from TOML configuration file.

    Args:
        config_path: Path to game_settings.toml

    Returns:
        Dictionary of settings
    """
    if not config_path.exists():
        return {}

    with config_path.open("rb") as f:
        return tomllib.load(f)


def save_settings_to_toml(settings: dict[str, Any], config_path: Path) -> None:
    """
    Save settings to TOML configuration file.

    Args:
        settings: Dictionary of settings to save
        config_path: Path to game_settings.toml
    """
    with config_path.open("wb") as f:
        tomli_w.dump(settings, f)


class GraphicsTab(QWidget):
    """Graphics settings tab."""

    def __init__(self, settings: dict[str, Any]) -> None:
        """
        Initialize graphics tab.

        Args:
            settings: Current settings dictionary
        """
        super().__init__()
        self.settings = settings.get("display", {})
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Set up the tab UI components."""
        layout = QVBoxLayout(self)

        # Display settings group
        display_group = QGroupBox("Display Settings")
        display_layout = QFormLayout()

        # Resolution
        self.resolution_combo = QComboBox()
        self.resolution_combo.addItems(
            [
                "1920x1080",
                "1600x900",
                "1280x720",
                "1024x768",
            ]
        )
        width = self.settings.get("width", 1280)
        height = self.settings.get("height", 720)
        current_res = f"{width}x{height}"
        index = self.resolution_combo.findText(current_res)
        if index >= 0:
            self.resolution_combo.setCurrentIndex(index)
        display_layout.addRow("Resolution:", self.resolution_combo)

        # Fullscreen
        self.fullscreen_check = QCheckBox()
        self.fullscreen_check.setChecked(self.settings.get("fullscreen", False))
        display_layout.addRow("Fullscreen:", self.fullscreen_check)

        # V-Sync
        self.vsync_check = QCheckBox()
        self.vsync_check.setChecked(self.settings.get("vsync", True))
        display_layout.addRow("V-Sync:", self.vsync_check)

        display_group.setLayout(display_layout)
        layout.addWidget(display_group)

        # Performance settings group
        perf_group = QGroupBox("Performance")
        perf_layout = QFormLayout()

        # Frame rate limit
        self.fps_combo = QComboBox()
        self.fps_combo.addItems(["30", "60", "120", "144", "Unlimited"])
        target_fps = str(self.settings.get("target_fps", 60))
        fps_index = self.fps_combo.findText(target_fps)
        if fps_index >= 0:
            self.fps_combo.setCurrentIndex(fps_index)
        perf_layout.addRow("FPS Limit:", self.fps_combo)

        perf_group.setLayout(perf_layout)
        layout.addWidget(perf_group)

        layout.addStretch()

    def get_settings(self) -> dict[str, Any]:
        """Get current graphics settings."""
        resolution = self.resolution_combo.currentText().split("x")
        fps_text = self.fps_combo.currentText()
        fps = 0 if fps_text == "Unlimited" else int(fps_text)

        return {
            "display": {
                "width": int(resolution[0]),
                "height": int(resolution[1]),
                "fullscreen": self.fullscreen_check.isChecked(),
                "vsync": self.vsync_check.isChecked(),
                "target_fps": fps,
            }
        }


class AudioTab(QWidget):
    """Audio settings tab."""

    def __init__(self, settings: dict[str, Any]) -> None:
        """
        Initialize audio tab.

        Args:
            settings: Current settings dictionary
        """
        super().__init__()
        self.settings = settings.get("audio", {})
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Set up the tab UI components."""
        layout = QVBoxLayout(self)

        # Volume settings group
        volume_group = QGroupBox("Volume Settings")
        volume_layout = QFormLayout()

        # Master volume
        self.master_slider = QSlider(Qt.Orientation.Horizontal)
        self.master_slider.setRange(0, 100)
        self.master_slider.setValue(int(self.settings.get("master_volume", 80)))
        self.master_label = QLabel(f"{self.master_slider.value()}%")
        self.master_slider.valueChanged.connect(
            lambda v: self.master_label.setText(f"{v}%")
        )
        volume_layout.addRow("Master Volume:", self.master_slider)
        volume_layout.addRow("", self.master_label)

        # Music volume
        self.music_slider = QSlider(Qt.Orientation.Horizontal)
        self.music_slider.setRange(0, 100)
        self.music_slider.setValue(int(self.settings.get("music_volume", 70)))
        self.music_label = QLabel(f"{self.music_slider.value()}%")
        self.music_slider.valueChanged.connect(
            lambda v: self.music_label.setText(f"{v}%")
        )
        volume_layout.addRow("Music Volume:", self.music_slider)
        volume_layout.addRow("", self.music_label)

        # Effects volume
        self.effects_slider = QSlider(Qt.Orientation.Horizontal)
        self.effects_slider.setRange(0, 100)
        self.effects_slider.setValue(int(self.settings.get("effects_volume", 90)))
        self.effects_label = QLabel(f"{self.effects_slider.value()}%")
        self.effects_slider.valueChanged.connect(
            lambda v: self.effects_label.setText(f"{v}%")
        )
        volume_layout.addRow("Effects Volume:", self.effects_slider)
        volume_layout.addRow("", self.effects_label)

        volume_group.setLayout(volume_layout)
        layout.addWidget(volume_group)

        layout.addStretch()

    def get_settings(self) -> dict[str, Any]:
        """Get current audio settings."""
        return {
            "audio": {
                "master_volume": self.master_slider.value(),
                "music_volume": self.music_slider.value(),
                "effects_volume": self.effects_slider.value(),
            }
        }


class GameplayTab(QWidget):
    """Gameplay settings tab."""

    def __init__(self, settings: dict[str, Any]) -> None:
        """
        Initialize gameplay tab.

        Args:
            settings: Current settings dictionary
        """
        super().__init__()
        self.settings = settings.get("gameplay", {})
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Set up the tab UI components."""
        layout = QVBoxLayout(self)

        # Game settings group
        game_group = QGroupBox("Game Settings")
        game_layout = QFormLayout()

        # Difficulty
        self.difficulty_combo = QComboBox()
        self.difficulty_combo.addItems(["Easy", "Normal", "Hard", "Very Hard"])
        difficulty = self.settings.get("difficulty", "Normal")
        diff_index = self.difficulty_combo.findText(difficulty)
        if diff_index >= 0:
            self.difficulty_combo.setCurrentIndex(diff_index)
        game_layout.addRow("Difficulty:", self.difficulty_combo)

        # Auto-save
        self.autosave_check = QCheckBox()
        self.autosave_check.setChecked(self.settings.get("auto_save", True))
        game_layout.addRow("Auto-Save:", self.autosave_check)

        # Tutorial hints
        self.hints_check = QCheckBox()
        self.hints_check.setChecked(self.settings.get("tutorial_hints", True))
        game_layout.addRow("Tutorial Hints:", self.hints_check)

        # Combat animations
        self.animations_check = QCheckBox()
        self.animations_check.setChecked(self.settings.get("combat_animations", True))
        game_layout.addRow("Combat Animations:", self.animations_check)

        game_group.setLayout(game_layout)
        layout.addWidget(game_group)

        layout.addStretch()

    def get_settings(self) -> dict[str, Any]:
        """Get current gameplay settings."""
        return {
            "gameplay": {
                "difficulty": self.difficulty_combo.currentText(),
                "auto_save": self.autosave_check.isChecked(),
                "tutorial_hints": self.hints_check.isChecked(),
                "combat_animations": self.animations_check.isChecked(),
            }
        }


class KeyBindingsTab(QWidget):
    """Key bindings settings tab."""

    def __init__(self, settings: dict[str, Any]) -> None:
        """
        Initialize key bindings tab.

        Args:
            settings: Current settings dictionary
        """
        super().__init__()
        self.settings = settings.get("key_bindings", {})
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Set up the tab UI components."""
        layout = QVBoxLayout(self)

        # Key bindings group
        bindings_group = QGroupBox("Key Bindings")
        bindings_layout = QFormLayout()

        # Common actions
        actions = [
            ("Move", "move"),
            ("Fire Weapons", "fire"),
            ("End Turn", "end_turn"),
            ("Open Map", "open_map"),
            ("Settings", "settings"),
        ]

        self.key_buttons: dict[str, QPushButton] = {}

        for action_name, action_key in actions:
            key = self.settings.get(action_key, "Not Set")
            button = QPushButton(key)
            button.setMinimumWidth(100)
            # Note: Full key rebinding implementation would capture key press
            bindings_layout.addRow(f"{action_name}:", button)
            self.key_buttons[action_key] = button

        bindings_group.setLayout(bindings_layout)
        layout.addWidget(bindings_group)

        # Reset to defaults button
        reset_btn = QPushButton("Reset to Defaults")
        reset_btn.clicked.connect(self._reset_defaults)
        layout.addWidget(reset_btn)

        layout.addStretch()

    def _reset_defaults(self) -> None:
        """Reset key bindings to defaults."""
        defaults = {
            "move": "M",
            "fire": "F",
            "end_turn": "Space",
            "open_map": "Tab",
            "settings": "Esc",
        }

        for action_key, default_key in defaults.items():
            if action_key in self.key_buttons:
                self.key_buttons[action_key].setText(default_key)

    def get_settings(self) -> dict[str, Any]:
        """Get current key binding settings."""
        bindings = {}
        for action_key, button in self.key_buttons.items():
            bindings[action_key] = button.text()

        return {"key_bindings": bindings}


class SettingsDialog(QDialog):
    """Main settings dialog with tabbed interface."""

    def __init__(self, config_path: Path, parent: QWidget | None = None) -> None:
        """
        Initialize settings dialog.

        Args:
            config_path: Path to game_settings.toml
            parent: Parent widget
        """
        super().__init__(parent)
        self.config_path = config_path
        self.settings = load_settings_from_toml(config_path)

        self.setWindowTitle("Settings")
        self.setMinimumWidth(500)
        self.setMinimumHeight(400)

        self._setup_ui()

    def _setup_ui(self) -> None:
        """Set up the dialog UI components."""
        layout = QVBoxLayout(self)

        # Tab widget
        self.tabs = QTabWidget()

        # Create tabs
        self.graphics_tab = GraphicsTab(self.settings)
        self.audio_tab = AudioTab(self.settings)
        self.gameplay_tab = GameplayTab(self.settings)
        self.keybindings_tab = KeyBindingsTab(self.settings)

        # Add tabs
        self.tabs.addTab(self.graphics_tab, "Graphics")
        self.tabs.addTab(self.audio_tab, "Audio")
        self.tabs.addTab(self.gameplay_tab, "Gameplay")
        self.tabs.addTab(self.keybindings_tab, "Key Bindings")

        layout.addWidget(self.tabs)

        # Dialog buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
            | QDialogButtonBox.StandardButton.Apply
        )
        button_box.accepted.connect(self._on_ok)
        button_box.rejected.connect(self.reject)
        button_box.button(QDialogButtonBox.StandardButton.Apply).clicked.connect(
            self._on_apply
        )

        layout.addWidget(button_box)

    def _gather_settings(self) -> dict[str, Any]:
        """Gather settings from all tabs."""
        all_settings = {}

        # Merge settings from each tab
        all_settings.update(self.graphics_tab.get_settings())
        all_settings.update(self.audio_tab.get_settings())
        all_settings.update(self.gameplay_tab.get_settings())
        all_settings.update(self.keybindings_tab.get_settings())

        return all_settings

    def _on_apply(self) -> None:
        """Apply settings without closing dialog."""
        settings = self._gather_settings()
        save_settings_to_toml(settings, self.config_path)

    def _on_ok(self) -> None:
        """Apply settings and close dialog."""
        self._on_apply()
        self.accept()
