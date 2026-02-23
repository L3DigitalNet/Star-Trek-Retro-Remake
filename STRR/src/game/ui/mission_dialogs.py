#!/usr/bin/env python3
"""
Star Trek Retro Remake - Mission Dialogs

Description:
    PySide6 dialog components for mission system including mission briefing,
    mission selection, and mission tracker interfaces.

Author: Star Trek Retro Remake Development Team
Email: development@star-trek-retro-remake.org
GitHub: https://github.com/L3DigitalNet/Star-Trek-Retro-Remake
Date Created: 10-31-2025
Date Changed: 10-31-2025
License: MIT License

Features:
    - Mission briefing dialog with detailed mission information
    - Mission selection interface at starbases
    - Mission tracker widget for active missions
    - Accept/decline mission functionality
    - Difficulty indicators and reward display
    - Objective progress tracking
    - Integration with MissionManager

Requirements:
    - Linux environment
    - Python 3.14+ for latest language features
    - PySide6 6.7+ for UI components

Known Issues:
    - Mission icons not yet implemented
    - Reward animations pending

Planned Features:
    - Mission history view
    - Mission recommendations based on player level
    - Dynamic mission notifications

Classes:
    - MissionBriefingDialog: Main dialog for mission details
    - MissionSelectionDialog: Dialog for choosing missions at starbase
    - MissionTrackerWidget: Widget showing active missions
    - ObjectiveProgressBar: Custom progress bar for objectives

Functions:
    - format_difficulty_color(): Get color based on difficulty
    - format_reward_text(): Format reward information
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Final

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QProgressBar,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

if TYPE_CHECKING:
    from ..components.mission_manager import (
        Mission,
        MissionManager,
    )

__version__: Final[str] = "0.0.31"


def format_difficulty_color(difficulty: int) -> str:
    """
    Get color code based on mission difficulty.

    Args:
        difficulty: Difficulty rating (1-5)

    Returns:
        HTML color code string
    """
    colors = {
        1: "#00FF00",  # Green - Easy
        2: "#7FFF00",  # Yellow-Green - Moderate
        3: "#FFFF00",  # Yellow - Challenging
        4: "#FF8C00",  # Orange - Hard
        5: "#FF0000",  # Red - Very Hard
    }
    return colors.get(difficulty, "#FFFFFF")


def format_reward_text(mission: Mission) -> str:
    """
    Format mission reward information as HTML.

    Args:
        mission: Mission instance with reward data

    Returns:
        HTML formatted reward text
    """
    reward = mission.reward
    parts = []

    if reward.reputation > 0:
        parts.append(f"<b>Reputation:</b> +{reward.reputation}")
    if reward.supplies > 0:
        parts.append(f"<b>Supplies:</b> +{reward.supplies}")
    if reward.spare_parts > 0:
        parts.append(f"<b>Spare Parts:</b> +{reward.spare_parts}")
    if reward.experience > 0:
        parts.append(f"<b>Experience:</b> +{reward.experience}")

    return "<br>".join(parts)


class ObjectiveProgressBar(QWidget):
    """Custom widget for displaying objective progress."""

    def __init__(self, objective_text: str, current: int, target: int) -> None:
        """
        Initialize objective progress bar.

        Args:
            objective_text: Description of objective
            current: Current progress
            target: Target value for completion
        """
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Objective description
        self.label = QLabel(objective_text)
        layout.addWidget(self.label)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(target)
        self.progress_bar.setValue(current)
        self.progress_bar.setFormat(f"{current}/{target}")
        layout.addWidget(self.progress_bar)

    def update_progress(self, current: int) -> None:
        """Update progress bar value."""
        self.progress_bar.setValue(current)
        target = self.progress_bar.maximum()
        self.progress_bar.setFormat(f"{current}/{target}")


class MissionBriefingDialog(QDialog):
    """Dialog for displaying mission briefing and accepting missions."""

    mission_accepted = Signal(object)  # Emits Mission object
    mission_declined = Signal(object)  # Emits Mission object

    def __init__(self, mission: Mission, parent: QWidget | None = None) -> None:
        """
        Initialize mission briefing dialog.

        Args:
            mission: Mission to display
            parent: Parent widget
        """
        super().__init__(parent)
        self.mission = mission
        self.setWindowTitle("Mission Briefing")
        self.setMinimumWidth(500)
        self.setMinimumHeight(400)

        self._setup_ui()

    def _setup_ui(self) -> None:
        """Set up the dialog UI components."""
        layout = QVBoxLayout(self)

        # Mission title and difficulty
        title_layout = QHBoxLayout()
        title_label = QLabel(f"<h2>{self.mission.name}</h2>")
        title_layout.addWidget(title_label)
        title_layout.addStretch()

        # Difficulty indicator
        diff_color = format_difficulty_color(self.mission.difficulty)
        diff_text = "★" * self.mission.difficulty
        diff_label = QLabel(
            f'<span style="color: {diff_color}; font-size: 20px;">{diff_text}</span>'
        )
        title_layout.addWidget(diff_label)

        layout.addLayout(title_layout)

        # Separator
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line)

        # Mission details
        details_group = QGroupBox("Mission Details")
        details_layout = QFormLayout()

        # Mission type
        details_layout.addRow(
            "Mission Type:", QLabel(self.mission.mission_type.name.title())
        )

        # Sector location
        details_layout.addRow(
            "Location:", QLabel(self.mission.sector_location or "Unknown")
        )

        # Difficulty level
        details_layout.addRow("Difficulty:", QLabel(str(self.mission.difficulty)))

        details_group.setLayout(details_layout)
        layout.addWidget(details_group)

        # Mission description
        desc_group = QGroupBox("Briefing")
        desc_layout = QVBoxLayout()
        self.description_text = QTextEdit()
        self.description_text.setReadOnly(True)
        self.description_text.setMaximumHeight(100)
        self.description_text.setPlainText(self.mission.description)
        desc_layout.addWidget(self.description_text)
        desc_group.setLayout(desc_layout)
        layout.addWidget(desc_group)

        # Objectives
        obj_group = QGroupBox("Objectives")
        obj_layout = QVBoxLayout()
        for obj in self.mission.objectives:
            obj_label = QLabel(f"• {obj.description} (Target: {obj.target_count})")
            obj_layout.addWidget(obj_label)
        obj_group.setLayout(obj_layout)
        layout.addWidget(obj_group)

        # Rewards
        reward_group = QGroupBox("Rewards")
        reward_layout = QVBoxLayout()
        reward_label = QLabel(format_reward_text(self.mission))
        reward_label.setTextFormat(Qt.TextFormat.RichText)
        reward_layout.addWidget(reward_label)
        reward_group.setLayout(reward_layout)
        layout.addWidget(reward_group)

        layout.addStretch()

        # Dialog buttons
        button_box = QDialogButtonBox()
        accept_btn = button_box.addButton(
            "Accept Mission", QDialogButtonBox.ButtonRole.AcceptRole
        )
        decline_btn = button_box.addButton(
            "Decline", QDialogButtonBox.ButtonRole.RejectRole
        )

        accept_btn.clicked.connect(self._on_accept)
        decline_btn.clicked.connect(self._on_decline)

        layout.addWidget(button_box)

    def _on_accept(self) -> None:
        """Handle mission acceptance."""
        self.mission_accepted.emit(self.mission)
        self.accept()

    def _on_decline(self) -> None:
        """Handle mission decline."""
        self.mission_declined.emit(self.mission)
        self.reject()


class MissionSelectionDialog(QDialog):
    """Dialog for selecting missions at a starbase."""

    mission_selected = Signal(object)  # Emits selected Mission

    def __init__(
        self,
        mission_manager: MissionManager,
        sector: str,
        parent: QWidget | None = None,
    ) -> None:
        """
        Initialize mission selection dialog.

        Args:
            mission_manager: MissionManager instance
            sector: Current sector identifier
            parent: Parent widget
        """
        super().__init__(parent)
        self.mission_manager = mission_manager
        self.sector = sector
        self.selected_mission: Mission | None = None

        self.setWindowTitle(f"Available Missions - Sector {sector}")
        self.setMinimumWidth(600)
        self.setMinimumHeight(500)

        self._setup_ui()
        self._load_missions()

    def _setup_ui(self) -> None:
        """Set up the dialog UI components."""
        layout = QVBoxLayout(self)

        # Header
        header = QLabel("<h2>Mission Selection</h2>")
        layout.addWidget(header)

        # Instructions
        instructions = QLabel(
            "Select a mission from the list below to view details and accept."
        )
        instructions.setWordWrap(True)
        layout.addWidget(instructions)

        # Mission list
        list_layout = QHBoxLayout()

        # Mission list widget
        self.mission_list = QListWidget()
        self.mission_list.itemClicked.connect(self._on_mission_clicked)
        list_layout.addWidget(self.mission_list, stretch=1)

        # Mission preview panel
        self.preview_group = QGroupBox("Mission Preview")
        preview_content = QVBoxLayout()

        self.preview_name = QLabel("<i>Select a mission to preview</i>")
        self.preview_name.setWordWrap(True)
        preview_content.addWidget(self.preview_name)

        self.preview_type = QLabel()
        preview_content.addWidget(self.preview_type)

        self.preview_difficulty = QLabel()
        preview_content.addWidget(self.preview_difficulty)

        self.preview_description = QTextEdit()
        self.preview_description.setReadOnly(True)
        self.preview_description.setMaximumHeight(150)
        preview_content.addWidget(self.preview_description)

        preview_content.addStretch()
        self.preview_group.setLayout(preview_content)
        list_layout.addWidget(self.preview_group, stretch=1)

        layout.addLayout(list_layout)

        # Dialog buttons
        button_layout = QHBoxLayout()
        self.view_details_btn = QPushButton("View Full Briefing")
        self.view_details_btn.setEnabled(False)
        self.view_details_btn.clicked.connect(self._on_view_details)
        button_layout.addWidget(self.view_details_btn)

        button_layout.addStretch()

        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.reject)
        button_layout.addWidget(close_btn)

        layout.addLayout(button_layout)

    def _load_missions(self) -> None:
        """Load available missions for the current sector."""
        from ..components.mission_manager import MissionType

        missions = self.mission_manager.get_available_missions_by_sector(self.sector)

        if not missions:
            # Generate some missions if none available
            mission_types = list(MissionType)
            for i, mission_type in enumerate(mission_types[:3], 1):
                mission = self.mission_manager.generate_mission(
                    mission_type=mission_type,
                    difficulty=i,
                    sector_location=self.sector,
                )
                self.mission_manager.available_missions.append(mission)
                missions.append(mission)

        # Populate list
        for mission in missions:
            item = QListWidgetItem(f"{mission.name} (Difficulty: {mission.difficulty})")
            item.setData(Qt.ItemDataRole.UserRole, mission)
            self.mission_list.addItem(item)

    def _on_mission_clicked(self, item: QListWidgetItem) -> None:
        """Handle mission list item click."""
        mission = item.data(Qt.ItemDataRole.UserRole)
        self.selected_mission = mission

        # Update preview
        self.preview_name.setText(f"<h3>{mission.name}</h3>")
        self.preview_type.setText(f"<b>Type:</b> {mission.mission_type.name.title()}")

        diff_color = format_difficulty_color(mission.difficulty)
        diff_stars = "★" * mission.difficulty
        self.preview_difficulty.setText(
            f'<b>Difficulty:</b> <span style="color: {diff_color};">{diff_stars}</span>'
        )

        self.preview_description.setPlainText(mission.description)
        self.view_details_btn.setEnabled(True)

    def _on_view_details(self) -> None:
        """Show full mission briefing dialog."""
        if self.selected_mission:
            briefing = MissionBriefingDialog(self.selected_mission, self)
            briefing.mission_accepted.connect(self._on_mission_accepted)
            briefing.exec()

    def _on_mission_accepted(self, mission: Mission) -> None:
        """Handle mission acceptance."""
        self.mission_selected.emit(mission)
        self.accept()


class MissionTrackerWidget(QWidget):
    """Widget displaying active missions and their progress."""

    def __init__(
        self, mission_manager: MissionManager, parent: QWidget | None = None
    ) -> None:
        """
        Initialize mission tracker widget.

        Args:
            mission_manager: MissionManager instance
            parent: Parent widget
        """
        super().__init__(parent)
        self.mission_manager = mission_manager

        self._setup_ui()

    def _setup_ui(self) -> None:
        """Set up the widget UI components."""
        layout = QVBoxLayout(self)

        # Header
        header = QLabel("<h3>Active Missions</h3>")
        layout.addWidget(header)

        # Mission list container
        self.mission_container = QVBoxLayout()
        layout.addLayout(self.mission_container)

        layout.addStretch()

    def update_missions(self) -> None:
        """Update the display of active missions."""
        # Clear existing mission widgets
        while self.mission_container.count():
            child = self.mission_container.takeAt(0)
            widget = child.widget() if child is not None else None
            if widget:
                widget.deleteLater()

        # Add active missions
        active_missions = self.mission_manager.active_missions

        if not active_missions:
            no_missions_label = QLabel("<i>No active missions</i>")
            self.mission_container.addWidget(no_missions_label)
            return

        for mission in active_missions:
            mission_widget = self._create_mission_widget(mission)
            self.mission_container.addWidget(mission_widget)

    def _create_mission_widget(self, mission: Mission) -> QWidget:
        """Create widget for single mission display."""
        widget = QGroupBox(mission.name)
        layout = QVBoxLayout()

        # Mission info
        info_label = QLabel(
            f"<b>Type:</b> {mission.mission_type.name.title()} | "
            f"<b>Location:</b> {mission.sector_location}"
        )
        layout.addWidget(info_label)

        # Objectives
        for obj in mission.objectives:
            obj_progress = ObjectiveProgressBar(
                obj.description, obj.current_count, obj.target_count
            )
            layout.addWidget(obj_progress)

        widget.setLayout(layout)
        return widget
