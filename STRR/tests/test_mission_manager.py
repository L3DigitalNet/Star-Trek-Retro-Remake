#!/usr/bin/env python3
"""
Star Trek Retro Remake - Mission System Tests

Description:
    Comprehensive unit tests for mission system components including
    MissionManager, Mission, MissionObjective, and mission lifecycle.

Author: Star Trek Retro Remake Development Team
Email: development@star-trek-retro-remake.org
GitHub: https://github.com/L3DigitalNet/Star-Trek-Retro-Remake
Date Created: 10-31-2025
Date Changed: 02-19-2026
License: MIT License

Features:
    - Test mission data structures and validation
    - Test mission manager operations
    - Test mission lifecycle (available, active, completed, failed)
    - Test mission objective tracking and completion
    - Test mission reward calculations
    - Test mission generation from templates
    - AAA pattern (Arrange-Act-Assert)

Requirements:
    - Linux environment
    - Python 3.14+ for latest language features
    - pytest 8.0+ for testing framework

Classes:
    - TestMissionObjective: Tests for MissionObjective class
    - TestMission: Tests for Mission class
    - TestMissionManager: Tests for MissionManager class

Functions:
    - None
"""

from pathlib import Path
from tempfile import NamedTemporaryFile

import pytest
from src.game.components.mission_manager import (
    Mission,
    MissionManager,
    MissionObjective,
    MissionReward,
    MissionStatus,
    MissionType,
)

pytestmark = pytest.mark.unit


class TestMissionObjective:
    """Tests for MissionObjective class."""

    def test_objective_creation(self):
        """Test creating a mission objective."""
        # Arrange & Act
        objective = MissionObjective(
            description="Scan 3 waypoints",
            objective_type="scan_waypoint",
            target_count=3,
        )

        # Assert
        assert objective.description == "Scan 3 waypoints"
        assert objective.objective_type == "scan_waypoint"
        assert objective.target_count == 3
        assert objective.current_count == 0
        assert not objective.completed

    def test_objective_progress_update(self):
        """Test updating objective progress."""
        # Arrange
        objective = MissionObjective(
            description="Destroy 2 ships",
            objective_type="destroy_enemy",
            target_count=2,
        )

        # Act
        objective.update_progress(1)

        # Assert
        assert objective.current_count == 1
        assert not objective.completed

    def test_objective_completion(self):
        """Test objective completion when target reached."""
        # Arrange
        objective = MissionObjective(
            description="Scan anomaly",
            objective_type="scan",
            target_count=1,
        )

        # Act
        objective.update_progress(1)

        # Assert
        assert objective.current_count == 1
        assert objective.completed

    def test_objective_progress_capped(self):
        """Test that progress doesn't exceed target."""
        # Arrange
        objective = MissionObjective(
            description="Collect data",
            objective_type="collect",
            target_count=3,
        )

        # Act
        objective.update_progress(5)  # Try to add more than target

        # Assert
        assert objective.current_count == 3  # Should be capped at target
        assert objective.completed


class TestMission:
    """Tests for Mission class."""

    def test_mission_creation(self):
        """Test creating a mission."""
        # Arrange
        objectives = [
            MissionObjective("Scan waypoint", "scan", 1),
            MissionObjective("Report data", "report", 1),
        ]
        reward = MissionReward(reputation=10, supplies=5)

        # Act
        mission = Mission(
            mission_id="patrol_0001",
            mission_type=MissionType.PATROL,
            name="Sector Patrol",
            description="Patrol the sector",
            objectives=objectives,
            reward=reward,
            difficulty=2,
            sector_location="A1",
        )

        # Assert
        assert mission.mission_id == "patrol_0001"
        assert mission.mission_type == MissionType.PATROL
        assert mission.name == "Sector Patrol"
        assert mission.status == MissionStatus.AVAILABLE
        assert mission.difficulty == 2
        assert len(mission.objectives) == 2

    def test_mission_completion_check(self):
        """Test checking if mission is completed."""
        # Arrange
        objectives = [
            MissionObjective("Task 1", "type1", 1),
            MissionObjective("Task 2", "type2", 1),
        ]
        mission = Mission(
            mission_id="test_001",
            mission_type=MissionType.COMBAT,
            name="Test Mission",
            description="Test",
            objectives=objectives,
            reward=MissionReward(),
        )

        # Act - complete first objective only
        objectives[0].update_progress(1)

        # Assert
        assert not mission.is_completed()

        # Act - complete second objective
        objectives[1].update_progress(1)

        # Assert
        assert mission.is_completed()

    def test_mission_update_increments_turns(self):
        """Test that mission update increments turn counter."""
        # Arrange
        objective = MissionObjective(
            "Task", "type", 10
        )  # High target to avoid auto-completion
        mission = Mission(
            mission_id="test_001",
            mission_type=MissionType.PATROL,
            name="Test",
            description="Test",
            objectives=[objective],
            reward=MissionReward(),
            status=MissionStatus.ACTIVE,
        )

        # Act
        mission.update()
        mission.update()

        # Assert
        assert mission.turns_active == 2
        assert mission.status == MissionStatus.ACTIVE  # Should still be active

    def test_mission_auto_completion(self):
        """Test mission auto-completes when objectives met."""
        # Arrange
        objective = MissionObjective("Task", "type", 1)
        mission = Mission(
            mission_id="test_001",
            mission_type=MissionType.RESCUE,
            name="Test",
            description="Test",
            objectives=[objective],
            reward=MissionReward(),
            status=MissionStatus.ACTIVE,
        )

        # Act
        objective.update_progress(1)
        mission.update()

        # Assert
        assert mission.status == MissionStatus.COMPLETED


class TestMissionManager:
    """Tests for MissionManager class."""

    @pytest.fixture
    def mission_templates_file(self):
        """Create temporary mission templates file."""
        content = """
[missions.patrol]
name = "Test Patrol"
description = "Test patrol mission"

[[missions.patrol.objectives]]
description = "Scan waypoints"
type = "scan"
target_count = 2

[missions.patrol.rewards]
reputation = 10
supplies = 5
spare_parts = 0
experience = 50

[missions.combat]
name = "Test Combat"
description = "Test combat mission"

[[missions.combat.objectives]]
description = "Destroy enemies"
type = "destroy"
target_count = 1

[missions.combat.rewards]
reputation = 20
supplies = 0
spare_parts = 10
experience = 100
"""
        with NamedTemporaryFile(mode="w", suffix=".toml", delete=False) as f:
            f.write(content)
            temp_path = Path(f.name)

        yield temp_path

        # Cleanup
        temp_path.unlink()

    def test_mission_manager_initialization(self, mission_templates_file):
        """Test mission manager initialization."""
        # Act
        manager = MissionManager(mission_templates_file)

        # Assert
        assert manager.mission_counter == 0
        assert len(manager.available_missions) == 0
        assert len(manager.active_missions) == 0
        assert "patrol" in manager.mission_templates
        assert "combat" in manager.mission_templates

    def test_generate_mission_from_template(self, mission_templates_file):
        """Test generating mission from template."""
        # Arrange
        manager = MissionManager(mission_templates_file)

        # Act
        mission = manager.generate_mission(
            mission_type=MissionType.PATROL,
            difficulty=2,
            sector_location="B5",
        )

        # Assert
        assert mission.mission_id == "patrol_0001"
        assert mission.mission_type == MissionType.PATROL
        assert mission.difficulty == 2
        assert mission.sector_location == "B5"
        assert len(mission.objectives) > 0
        assert mission.objectives[0].target_count == 4  # 2 * difficulty

    def test_mission_reward_scaling(self, mission_templates_file):
        """Test that mission rewards scale with difficulty."""
        # Arrange
        manager = MissionManager(mission_templates_file)

        # Act
        easy_mission = manager.generate_mission(MissionType.COMBAT, 1, "A1")
        hard_mission = manager.generate_mission(MissionType.COMBAT, 3, "A1")

        # Assert
        assert hard_mission.reward.reputation == easy_mission.reward.reputation * 3
        assert hard_mission.reward.experience == easy_mission.reward.experience * 3

    def test_accept_mission(self, mission_templates_file):
        """Test accepting an available mission."""
        # Arrange
        manager = MissionManager(mission_templates_file)
        mission = manager.generate_mission(MissionType.PATROL, 1, "A1")
        manager.available_missions.append(mission)

        # Act
        manager.accept_mission(mission)

        # Assert
        assert mission.status == MissionStatus.ACTIVE
        assert mission in manager.active_missions
        assert mission not in manager.available_missions

    def test_abandon_mission(self, mission_templates_file):
        """Test abandoning an active mission."""
        # Arrange
        manager = MissionManager(mission_templates_file)
        mission = manager.generate_mission(MissionType.COMBAT, 1, "A1")
        manager.accept_mission(mission)

        # Act
        manager.abandon_mission(mission)

        # Assert
        assert mission.status == MissionStatus.FAILED
        assert mission not in manager.active_missions
        assert mission in manager.completed_missions

    def test_complete_mission(self, mission_templates_file):
        """Test completing a mission."""
        # Arrange
        from unittest.mock import Mock

        manager = MissionManager(mission_templates_file)
        mission = manager.generate_mission(MissionType.RESCUE, 1, "A1")
        manager.accept_mission(mission)

        # Complete all objectives
        for obj in mission.objectives:
            obj.update_progress(obj.target_count)

        # Create mock player ship using the correct component API:
        # get_system("resources") must return a ResourceManager instance for
        # isinstance narrowing to pass in complete_mission().
        from src.game.components.ship_systems import ResourceManager
        mock_ship = Mock()
        mock_resource_manager = Mock(spec=ResourceManager)
        mock_ship.get_system.return_value = mock_resource_manager

        # Act
        manager.complete_mission(mission, mock_ship)

        # Assert
        assert mission.status == MissionStatus.COMPLETED
        assert mission in manager.completed_missions
        assert mission not in manager.active_missions
        mock_ship.get_system.assert_called_once_with("resources")
        mock_resource_manager.resupply.assert_any_call("medical", mission.reward.supplies)
        mock_resource_manager.resupply.assert_any_call("spare_parts", mission.reward.spare_parts)

    def test_update_active_missions(self, mission_templates_file):
        """Test updating all active missions."""
        # Arrange
        manager = MissionManager(mission_templates_file)
        mission1 = manager.generate_mission(MissionType.PATROL, 1, "A1")
        mission2 = manager.generate_mission(MissionType.COMBAT, 1, "B2")

        manager.accept_mission(mission1)
        manager.accept_mission(mission2)

        # Complete mission1 objectives
        for obj in mission1.objectives:
            obj.update_progress(obj.target_count)

        # Act
        manager.update_active_missions()

        # Assert
        assert mission1.status == MissionStatus.COMPLETED
        assert mission1 in manager.completed_missions
        assert mission2.status == MissionStatus.ACTIVE
        assert mission2.turns_active == 1

    def test_get_active_mission_count(self, mission_templates_file):
        """Test getting count of active missions."""
        # Arrange
        manager = MissionManager(mission_templates_file)
        mission1 = manager.generate_mission(MissionType.PATROL, 1, "A1")
        mission2 = manager.generate_mission(MissionType.COMBAT, 1, "B2")

        # Act
        manager.accept_mission(mission1)
        manager.accept_mission(mission2)

        # Assert
        assert manager.get_active_mission_count() == 2

    def test_get_missions_by_sector(self, mission_templates_file):
        """Test filtering missions by sector."""
        # Arrange
        manager = MissionManager(mission_templates_file)
        mission_a1 = manager.generate_mission(MissionType.PATROL, 1, "A1")
        mission_b2 = manager.generate_mission(MissionType.COMBAT, 1, "B2")
        mission_a1_2 = manager.generate_mission(MissionType.RESCUE, 1, "A1")

        manager.available_missions.extend([mission_a1, mission_b2, mission_a1_2])

        # Act
        a1_missions = manager.get_available_missions_by_sector("A1")

        # Assert
        assert len(a1_missions) == 2
        assert mission_a1 in a1_missions
        assert mission_a1_2 in a1_missions
        assert mission_b2 not in a1_missions

    def test_mission_counter_increments(self, mission_templates_file):
        """Test that mission counter increments for unique IDs."""
        # Arrange
        manager = MissionManager(mission_templates_file)

        # Act
        mission1 = manager.generate_mission(MissionType.PATROL, 1, "A1")
        mission2 = manager.generate_mission(MissionType.PATROL, 1, "A1")
        mission3 = manager.generate_mission(MissionType.COMBAT, 1, "B2")

        # Assert
        assert mission1.mission_id == "patrol_0001"
        assert mission2.mission_id == "patrol_0002"
        assert mission3.mission_id == "combat_0003"
        assert manager.mission_counter == 3
