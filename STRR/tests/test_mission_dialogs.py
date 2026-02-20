#!/usr/bin/env python3
"""
Star Trek Retro Remake - Mission Dialogs Tests

Tests for mission dialog components including briefing, selection, and tracker.
"""

import sys
from pathlib import Path
from unittest.mock import Mock

import pytest

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.game.components.mission_manager import (
    Mission,
    MissionManager,
    MissionObjective,
    MissionReward,
    MissionStatus,
    MissionType,
)


@pytest.fixture
def sample_mission():
    """Create a sample mission for testing."""
    objectives = [
        MissionObjective(
            description="Patrol waypoint Alpha",
            objective_type="patrol",
            target_count=3,
        ),
        MissionObjective(
            description="Scan anomaly",
            objective_type="scan",
            target_count=1,
        ),
    ]

    reward = MissionReward(
        reputation=100,
        supplies=50,
        spare_parts=25,
        experience=200,
    )

    mission = Mission(
        mission_id="patrol_0001",
        mission_type=MissionType.PATROL,
        name="Sector Patrol Alpha",
        description="Patrol the sector and scan for anomalies.",
        objectives=objectives,
        reward=reward,
        status=MissionStatus.AVAILABLE,
        difficulty=2,
        sector_location="Alpha Quadrant",
    )

    return mission


@pytest.fixture
def mission_manager(tmp_path):
    """Create a mission manager with temporary TOML file."""
    # Create temporary mission templates file
    toml_content = """
[missions.patrol]
name = "Sector Patrol"
description = "Patrol designated waypoints and report findings."
objectives = [
    { type = "patrol", description = "Patrol waypoint", target_count = 3 }
]
rewards = { reputation = 50, supplies = 20, spare_parts = 10, experience = 100 }
"""
    toml_file = tmp_path / "mission_templates.toml"
    toml_file.write_text(toml_content)

    manager = MissionManager(toml_file)
    return manager


class TestMissionDialogHelpers:
    """Test helper functions for mission dialogs."""

    def test_format_difficulty_color(self):
        """Test difficulty color formatting."""
        from src.game.ui.mission_dialogs import format_difficulty_color

        # Test all difficulty levels
        assert format_difficulty_color(1) == "#00FF00"  # Green
        assert format_difficulty_color(2) == "#7FFF00"  # Yellow-Green
        assert format_difficulty_color(3) == "#FFFF00"  # Yellow
        assert format_difficulty_color(4) == "#FF8C00"  # Orange
        assert format_difficulty_color(5) == "#FF0000"  # Red
        assert format_difficulty_color(6) == "#FFFFFF"  # Default white

    def test_format_reward_text(self, sample_mission):
        """Test reward text formatting."""
        from src.game.ui.mission_dialogs import format_reward_text

        text = format_reward_text(sample_mission)

        # Check that all reward components are present
        assert "Reputation" in text
        assert "+100" in text
        assert "Supplies" in text
        assert "+50" in text
        assert "Spare Parts" in text
        assert "+25" in text
        assert "Experience" in text
        assert "+200" in text


class TestObjectiveProgressBar:
    """Test ObjectiveProgressBar widget."""

    def test_progress_bar_initialization(self, qtbot):
        """Test progress bar initialization."""
        from src.game.ui.mission_dialogs import ObjectiveProgressBar

        progress_bar = ObjectiveProgressBar("Test Objective", 2, 5)
        qtbot.addWidget(progress_bar)

        # Verify label text
        assert progress_bar.label.text() == "Test Objective"

        # Verify progress bar values
        assert progress_bar.progress_bar.minimum() == 0
        assert progress_bar.progress_bar.maximum() == 5
        assert progress_bar.progress_bar.value() == 2
        assert "2/5" in progress_bar.progress_bar.format()

    def test_progress_bar_update(self, qtbot):
        """Test progress bar value update."""
        from src.game.ui.mission_dialogs import ObjectiveProgressBar

        progress_bar = ObjectiveProgressBar("Test Objective", 0, 10)
        qtbot.addWidget(progress_bar)

        # Update progress
        progress_bar.update_progress(7)

        # Verify updated values
        assert progress_bar.progress_bar.value() == 7
        assert "7/10" in progress_bar.progress_bar.format()


class TestMissionBriefingDialog:
    """Test MissionBriefingDialog."""

    def test_briefing_dialog_initialization(self, qtbot, sample_mission):
        """Test briefing dialog displays mission correctly."""
        from src.game.ui.mission_dialogs import MissionBriefingDialog

        dialog = MissionBriefingDialog(sample_mission)
        qtbot.addWidget(dialog)

        # Verify mission is stored
        assert dialog.mission == sample_mission

        # Verify window title
        assert "Mission Briefing" in dialog.windowTitle()

        # Verify minimum size
        assert dialog.minimumWidth() >= 500
        assert dialog.minimumHeight() >= 400

    def test_briefing_dialog_accept_signal(self, qtbot, sample_mission):
        """Test mission acceptance signal."""
        from src.game.ui.mission_dialogs import MissionBriefingDialog

        dialog = MissionBriefingDialog(sample_mission)
        qtbot.addWidget(dialog)

        # Connect signal to mock
        mock_handler = Mock()
        dialog.mission_accepted.connect(mock_handler)

        # Simulate accept button click
        dialog._on_accept()

        # Verify signal was emitted with mission
        mock_handler.assert_called_once_with(sample_mission)

    def test_briefing_dialog_decline_signal(self, qtbot, sample_mission):
        """Test mission decline signal."""
        from src.game.ui.mission_dialogs import MissionBriefingDialog

        dialog = MissionBriefingDialog(sample_mission)
        qtbot.addWidget(dialog)

        # Connect signal to mock
        mock_handler = Mock()
        dialog.mission_declined.connect(mock_handler)

        # Simulate decline button click
        dialog._on_decline()

        # Verify signal was emitted with mission
        mock_handler.assert_called_once_with(sample_mission)


class TestMissionSelectionDialog:
    """Test MissionSelectionDialog."""

    def test_selection_dialog_initialization(self, qtbot, mission_manager):
        """Test selection dialog initialization."""
        from src.game.ui.mission_dialogs import MissionSelectionDialog

        dialog = MissionSelectionDialog(mission_manager, "Alpha Quadrant")
        qtbot.addWidget(dialog)

        # Verify manager and sector are stored
        assert dialog.mission_manager == mission_manager
        assert dialog.sector == "Alpha Quadrant"

        # Verify window properties
        assert "Available Missions" in dialog.windowTitle()
        assert "Alpha Quadrant" in dialog.windowTitle()
        assert dialog.minimumWidth() >= 600

    def test_selection_dialog_loads_missions(self, qtbot, mission_manager):
        """Test mission loading in selection dialog."""
        from src.game.ui.mission_dialogs import MissionSelectionDialog

        # Generate some missions
        mission1 = mission_manager.generate_mission(
            MissionType.PATROL, 1, "Alpha Quadrant"
        )
        mission2 = mission_manager.generate_mission(
            MissionType.COMBAT, 2, "Alpha Quadrant"
        )
        mission_manager.available_missions.extend([mission1, mission2])

        dialog = MissionSelectionDialog(mission_manager, "Alpha Quadrant")
        qtbot.addWidget(dialog)

        # Verify missions are loaded in list
        assert dialog.mission_list.count() == 2

    def test_selection_dialog_mission_selection(self, qtbot, mission_manager):
        """Test mission selection from list."""
        from src.game.ui.mission_dialogs import MissionSelectionDialog

        # Generate mission
        mission = mission_manager.generate_mission(
            MissionType.PATROL, 1, "Alpha Quadrant"
        )
        mission_manager.available_missions.append(mission)

        dialog = MissionSelectionDialog(mission_manager, "Alpha Quadrant")
        qtbot.addWidget(dialog)

        # Select first mission
        dialog.mission_list.setCurrentRow(0)
        item = dialog.mission_list.item(0)
        dialog._on_mission_clicked(item)

        # Verify mission is selected
        assert dialog.selected_mission == mission
        assert dialog.view_details_btn.isEnabled()


class TestMissionTrackerWidget:
    """Test MissionTrackerWidget."""

    def test_tracker_initialization(self, qtbot, mission_manager):
        """Test tracker widget initialization."""
        from src.game.ui.mission_dialogs import MissionTrackerWidget

        tracker = MissionTrackerWidget(mission_manager)
        qtbot.addWidget(tracker)

        # Verify manager is stored
        assert tracker.mission_manager == mission_manager

    def test_tracker_displays_no_missions(self, qtbot, mission_manager):
        """Test tracker displays message when no active missions."""
        from src.game.ui.mission_dialogs import MissionTrackerWidget

        tracker = MissionTrackerWidget(mission_manager)
        qtbot.addWidget(tracker)

        # Update with no active missions
        tracker.update_missions()

        # Should display "No active missions" message
        assert tracker.mission_container.count() > 0

    def test_tracker_displays_active_missions(self, qtbot, mission_manager):
        """Test tracker displays active missions."""
        from src.game.ui.mission_dialogs import MissionTrackerWidget

        # Create and activate mission
        mission = mission_manager.generate_mission(
            MissionType.PATROL, 1, "Alpha Quadrant"
        )
        mission_manager.accept_mission(mission)

        tracker = MissionTrackerWidget(mission_manager)
        qtbot.addWidget(tracker)

        # Update missions
        tracker.update_missions()

        # Should display mission widget
        assert tracker.mission_container.count() > 0

    def test_tracker_updates_on_mission_changes(self, qtbot, mission_manager):
        """Test tracker updates when missions change."""
        from src.game.ui.mission_dialogs import MissionTrackerWidget

        tracker = MissionTrackerWidget(mission_manager)
        qtbot.addWidget(tracker)

        # Initially no missions - should show "No active missions" label
        tracker.update_missions()
        initial_count = tracker.mission_container.count()
        assert initial_count == 1  # One label saying "No active missions"

        # Add active mission
        mission = mission_manager.generate_mission(
            MissionType.PATROL, 1, "Alpha Quadrant"
        )
        mission_manager.accept_mission(mission)

        # Update tracker - should show mission widget
        tracker.update_missions()
        updated_count = tracker.mission_container.count()

        # Should still be 1 widget (the mission group box replaced the label)
        assert updated_count == 1


class TestMissionDialogIntegration:
    """Test integration between dialog components."""

    def test_briefing_to_selection_flow(self, qtbot, mission_manager):
        """Test flow from selection to briefing dialog."""
        from src.game.ui.mission_dialogs import MissionSelectionDialog

        # Create mission
        mission = mission_manager.generate_mission(
            MissionType.PATROL, 1, "Alpha Quadrant"
        )
        mission_manager.available_missions.append(mission)

        # Create selection dialog
        selection_dialog = MissionSelectionDialog(mission_manager, "Alpha Quadrant")
        qtbot.addWidget(selection_dialog)

        # Select mission
        selection_dialog.mission_list.setCurrentRow(0)
        item = selection_dialog.mission_list.item(0)
        selection_dialog._on_mission_clicked(item)

        # Verify mission is selected
        assert selection_dialog.selected_mission == mission

    def test_mission_accepted_updates_manager(self, qtbot, mission_manager):
        """Test accepting mission updates mission manager."""
        from src.game.ui.mission_dialogs import MissionBriefingDialog

        # Create available mission
        mission = mission_manager.generate_mission(
            MissionType.PATROL, 1, "Alpha Quadrant"
        )
        mission.status = MissionStatus.AVAILABLE

        # Create briefing dialog
        dialog = MissionBriefingDialog(mission)
        qtbot.addWidget(dialog)

        # Accept mission through manager
        mission_manager.accept_mission(mission)

        # Verify mission status changed
        assert mission.status == MissionStatus.ACTIVE
        assert mission in mission_manager.active_missions
