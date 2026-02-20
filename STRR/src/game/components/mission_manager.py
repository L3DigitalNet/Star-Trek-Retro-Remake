#!/usr/bin/env python3
"""
Star Trek Retro Remake - Mission Manager

Description:
    Mission system for managing objectives, mission lifecycle, and rewards.
    Supports patrol, combat, escort, rescue, diplomatic, and survey missions.

Author: Star Trek Retro Remake Development Team
Email: development@star-trek-retro-remake.org
GitHub: https://github.com/L3DigitalNet/Star-Trek-Retro-Remake
Date Created: 10-31-2025
Date Changed: 02-19-2026
License: MIT License

Features:
    - Mission data structures with comprehensive type hints
    - Mission template system loaded from TOML files
    - Mission state tracking (available, active, completed, failed)
    - Dynamic mission generation based on sector threat level
    - Reputation rewards and penalties for mission outcomes
    - Mission objective tracking and completion detection
    - Support for multiple active missions
    - Persistent mission history

Requirements:
    - Linux environment
    - Python 3.14+ for latest language features
    - Standard library (dataclasses, enum, typing)

Known Issues:
    - Mission generation algorithm needs balancing
    - Diplomatic mission dialog not yet implemented

Planned Features:
    - Procedural mission generation with story elements
    - Mission chains and campaign arcs
    - Time-sensitive missions with deadlines
    - Multi-stage missions with dynamic objectives

Classes:
    - MissionType: Enum for mission categories
    - MissionStatus: Enum for mission lifecycle states
    - MissionObjective: Single objective within a mission
    - MissionReward: Rewards granted on mission completion
    - Mission: Complete mission definition with objectives and state
    - MissionManager: Central manager for all mission operations

Functions:
    - load_mission_templates(): Load mission definitions from TOML
    - generate_mission(): Create new mission from template
    - check_mission_completion(): Verify if objectives are met
    - apply_mission_rewards(): Grant rewards to player
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path
from typing import TYPE_CHECKING, Final

if TYPE_CHECKING:
    from ..entities.starship import Starship

try:
    import tomllib
except ImportError:
    import tomli as tomllib  # type: ignore[import-not-found,no-redef]

__version__: Final[str] = "0.0.31"


# Mission system configuration
class MissionType(Enum):
    """Available mission categories in the game."""

    PATROL = auto()  # Scan waypoints, report anomalies
    COMBAT = auto()  # Engage and defeat enemy ships
    ESCORT = auto()  # Protect friendly ship between waypoints
    RESCUE = auto()  # Locate and recover stranded vessels
    DIPLOMATIC = auto()  # Transport diplomats, negotiate
    SURVEY = auto()  # Gather scientific data from anomalies


class MissionStatus(Enum):
    """Mission lifecycle states."""

    AVAILABLE = auto()  # Can be accepted at starbase
    ACTIVE = auto()  # Currently in progress
    COMPLETED = auto()  # Successfully finished
    FAILED = auto()  # Mission failed or abandoned


@dataclass
class MissionObjective:
    """Single objective within a mission."""

    description: str  # Human-readable objective text
    objective_type: str  # Type identifier (scan, destroy, escort, etc.)
    target_count: int  # Number of targets to complete
    current_count: int = 0  # Progress toward completion
    completed: bool = False  # Objective completion flag

    def update_progress(self, amount: int = 1) -> None:
        """
        Increment objective progress and check completion.

        Updates current_count and sets completed flag when target reached.
        """
        self.current_count = min(self.current_count + amount, self.target_count)
        if self.current_count >= self.target_count:
            self.completed = True


@dataclass
class MissionReward:
    """Rewards granted on mission completion."""

    reputation: int = 0  # Reputation points gained/lost
    supplies: int = 0  # Medical supplies awarded
    spare_parts: int = 0  # Spare parts awarded
    experience: int = 0  # Experience points for crew


@dataclass
class Mission:
    """Complete mission definition with objectives and state."""

    mission_id: str  # Unique mission identifier
    mission_type: MissionType  # Mission category
    name: str  # Mission name/title
    description: str  # Detailed mission briefing
    objectives: list[MissionObjective]  # List of objectives to complete
    reward: MissionReward  # Rewards on completion
    status: MissionStatus = MissionStatus.AVAILABLE  # Current state
    difficulty: int = 1  # Difficulty rating (1-5)
    sector_location: str = ""  # Sector where mission takes place
    turns_active: int = 0  # Turns since mission accepted

    def is_completed(self) -> bool:
        """Check if all objectives are completed."""
        return all(obj.completed for obj in self.objectives)

    def update(self) -> None:
        """Update mission state based on objective completion."""
        if self.status == MissionStatus.ACTIVE:
            self.turns_active += 1
            if self.is_completed():
                self.status = MissionStatus.COMPLETED


class MissionManager:
    """Central manager for all mission operations."""

    def __init__(self, mission_data_path: Path) -> None:
        """
        Initialize mission manager.

        Args:
            mission_data_path: Path to mission templates TOML file
        """
        self.mission_templates: dict[str, dict] = {}
        self.available_missions: list[Mission] = []
        self.active_missions: list[Mission] = []
        self.completed_missions: list[Mission] = []
        self.mission_counter: int = 0  # For generating unique IDs

        # Load mission templates from TOML
        if mission_data_path.exists():
            self._load_mission_templates(mission_data_path)

    def _load_mission_templates(self, path: Path) -> None:
        """
        Load mission templates from TOML file.

        Args:
            path: Path to mission_templates.toml
        """
        with path.open("rb") as file:
            data = tomllib.load(file)
            self.mission_templates = data.get("missions", {})

    def generate_mission(
        self,
        mission_type: MissionType,
        difficulty: int,
        sector_location: str,
    ) -> Mission:
        """
        Generate new mission from template.

        Args:
            mission_type: Type of mission to generate
            difficulty: Difficulty rating (1-5)
            sector_location: Sector coordinates where mission occurs

        Returns:
            Newly generated mission
        """
        # Get template for mission type
        template_name = mission_type.name.lower()
        template = self.mission_templates.get(template_name, {})

        # Generate unique mission ID
        self.mission_counter += 1
        mission_id = f"{template_name}_{self.mission_counter:04d}"

        # Create objectives based on template and difficulty
        objectives = self._create_objectives(template, difficulty)

        # Calculate rewards based on difficulty
        reward = self._calculate_rewards(template, difficulty)

        # Create mission instance
        mission = Mission(
            mission_id=mission_id,
            mission_type=mission_type,
            name=template.get("name", f"Mission {self.mission_counter}"),
            description=template.get("description", "No description available."),
            objectives=objectives,
            reward=reward,
            status=MissionStatus.AVAILABLE,
            difficulty=difficulty,
            sector_location=sector_location,
        )

        return mission

    def _create_objectives(
        self, template: dict, difficulty: int
    ) -> list[MissionObjective]:
        """
        Create mission objectives from template and difficulty.

        Args:
            template: Mission template data
            difficulty: Difficulty rating affecting target counts

        Returns:
            List of mission objectives
        """
        objectives: list[MissionObjective] = []

        # Get objective templates
        obj_templates = template.get("objectives", [])

        for obj_data in obj_templates:
            # Scale target count with difficulty
            base_count = obj_data.get("target_count", 1)
            target_count = base_count * difficulty

            objective = MissionObjective(
                description=obj_data.get("description", "Complete objective"),
                objective_type=obj_data.get("type", "generic"),
                target_count=target_count,
            )
            objectives.append(objective)

        return objectives

    def _calculate_rewards(self, template: dict, difficulty: int) -> MissionReward:
        """
        Calculate mission rewards based on template and difficulty.

        Args:
            template: Mission template data
            difficulty: Difficulty multiplier for rewards

        Returns:
            Mission reward structure
        """
        base_rewards = template.get("rewards", {})

        return MissionReward(
            reputation=base_rewards.get("reputation", 10) * difficulty,
            supplies=base_rewards.get("supplies", 0) * difficulty,
            spare_parts=base_rewards.get("spare_parts", 0) * difficulty,
            experience=base_rewards.get("experience", 50) * difficulty,
        )

    def accept_mission(self, mission: Mission) -> None:
        """
        Accept an available mission and add to active missions.

        Args:
            mission: Mission to accept
        """
        if mission.status == MissionStatus.AVAILABLE:
            mission.status = MissionStatus.ACTIVE
            self.active_missions.append(mission)
            if mission in self.available_missions:
                self.available_missions.remove(mission)

    def abandon_mission(self, mission: Mission) -> None:
        """
        Abandon an active mission with reputation penalty.

        Args:
            mission: Mission to abandon
        """
        if mission.status == MissionStatus.ACTIVE:
            mission.status = MissionStatus.FAILED
            if mission in self.active_missions:
                self.active_missions.remove(mission)
            self.completed_missions.append(mission)

    def complete_mission(self, mission: Mission, player_ship: Starship) -> None:
        """
        Complete mission and apply rewards to player ship.

        Args:
            mission: Mission to complete
            player_ship: Player's starship to receive rewards
        """
        if mission.status == MissionStatus.ACTIVE and mission.is_completed():
            mission.status = MissionStatus.COMPLETED

            # Apply rewards - use getattr for dynamic access
            resource_manager = getattr(player_ship, "resource_manager", None)
            if resource_manager:
                resource_manager.add_supplies(mission.reward.supplies)
                resource_manager.add_spare_parts(mission.reward.spare_parts)

            # Move to completed missions
            if mission in self.active_missions:
                self.active_missions.remove(mission)
            self.completed_missions.append(mission)

    def update_active_missions(self) -> None:
        """Update all active missions and check for completion."""
        for mission in self.active_missions[:]:  # Copy list to allow modification
            mission.update()
            # Auto-complete if objectives met
            if mission.status == MissionStatus.COMPLETED:
                if mission in self.active_missions:
                    self.active_missions.remove(mission)
                self.completed_missions.append(mission)

    def get_active_mission_count(self) -> int:
        """Get number of currently active missions."""
        return len(self.active_missions)

    def get_available_missions_by_sector(self, sector: str) -> list[Mission]:
        """
        Get available missions for specific sector.

        Args:
            sector: Sector identifier

        Returns:
            List of available missions in that sector
        """
        return [m for m in self.available_missions if m.sector_location == sector]
