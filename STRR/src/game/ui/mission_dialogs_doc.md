# Mission Dialogs Documentation

## Overview

The Mission Dialogs module provides PySide6-based UI components for the mission system, including mission briefing dialogs, mission selection interfaces, and active mission tracking widgets.

## Components

### MissionBriefingDialog

**Purpose:** Display detailed mission information and allow players to accept or decline missions.

**Features:**
- Mission title with visual difficulty indicators (★ rating)
- Comprehensive mission details (type, location, difficulty)
- Mission description/briefing text
- List of objectives with target counts
- Reward breakdown (reputation, supplies, spare parts, experience)
- Accept/Decline buttons with signal emission

**Usage:**
```python
from STRR.src.game.ui.mission_dialogs import MissionBriefingDialog

# Show mission briefing
dialog = MissionBriefingDialog(mission, parent_widget)
dialog.mission_accepted.connect(on_mission_accepted)
dialog.mission_declined.connect(on_mission_declined)
dialog.exec()
```

**Signals:**
- `mission_accepted(Mission)`: Emitted when player accepts mission
- `mission_declined(Mission)`: Emitted when player declines mission

### MissionSelectionDialog

**Purpose:** Browse and select missions at starbases.

**Features:**
- List of available missions in current sector
- Mission preview panel showing key details
- Difficulty color-coding (green to red)
- "View Full Briefing" button for detailed view
- Auto-generation of missions if none available
- Integration with MissionManager

**Usage:**
```python
from STRR.src.game.ui.mission_dialogs import MissionSelectionDialog

# Show mission selection at starbase
dialog = MissionSelectionDialog(mission_manager, sector_id, parent_widget)
dialog.mission_selected.connect(on_mission_selected)
result = dialog.exec()
```

**Signals:**
- `mission_selected(Mission)`: Emitted when player accepts a mission

### MissionTrackerWidget

**Purpose:** Display active missions and their progress in the main game UI.

**Features:**
- List of all active missions
- Objective progress bars for each mission
- Real-time progress updates
- Mission type and location display
- Compact layout for sidebar/panel integration

**Usage:**
```python
from STRR.src.game.ui.mission_dialogs import MissionTrackerWidget

# Add to main window
tracker = MissionTrackerWidget(mission_manager, parent_widget)
layout.addWidget(tracker)

# Update when missions change
tracker.update_missions()
```

### ObjectiveProgressBar

**Purpose:** Custom widget for displaying individual objective progress.

**Features:**
- Objective description label
- Progress bar with current/target format
- Update method for progress changes

**Usage:**
```python
from STRR.src.game.ui.mission_dialogs import ObjectiveProgressBar

progress = ObjectiveProgressBar("Scan waypoints", current=2, target=5)
# Later update progress
progress.update_progress(3)
```

## Utility Functions

### format_difficulty_color(difficulty: int) -> str

Returns HTML color code based on difficulty level:
- 1: Green (#00FF00) - Easy
- 2: Yellow-Green (#7FFF00) - Moderate
- 3: Yellow (#FFFF00) - Challenging
- 4: Orange (#FF8C00) - Hard
- 5: Red (#FF0000) - Very Hard

### format_reward_text(mission: Mission) -> str

Formats mission rewards as HTML text with bold labels and values.

## Integration Examples

### Complete Mission Flow at Starbase

```python
# Player docks at starbase
def on_dock_at_starbase():
    # Show mission selection dialog
    dialog = MissionSelectionDialog(
        mission_manager=game_model.mission_manager,
        sector=game_model.current_sector.name,
        parent=main_window
    )

    # Connect signal
    dialog.mission_selected.connect(handle_mission_accepted)

    # Show dialog
    dialog.exec()

def handle_mission_accepted(mission):
    # Accept mission in manager
    game_model.mission_manager.accept_mission(mission)

    # Update tracker
    mission_tracker.update_missions()

    # Show confirmation
    QMessageBox.information(
        main_window,
        "Mission Accepted",
        f"Mission '{mission.name}' has been added to your active missions."
    )
```

### Update Mission Tracker Each Turn

```python
def advance_turn():
    # Update game state
    game_model.turn_manager.advance_turn()
    game_model.update_missions()

    # Update UI
    mission_tracker.update_missions()

    # Check for completed missions
    for mission in game_model.mission_manager.active_missions:
        if mission.status == MissionStatus.COMPLETED:
            show_mission_complete_dialog(mission)
```

### Manual Mission Selection (Dev/Testing)

```python
# Generate and show specific mission
from STRR.src.game.components.mission_manager import MissionType

mission = game_model.mission_manager.generate_mission(
    mission_type=MissionType.COMBAT,
    difficulty=3,
    sector_location="A5"
)

briefing = MissionBriefingDialog(mission, main_window)
briefing.mission_accepted.connect(lambda m: game_model.mission_manager.accept_mission(m))
briefing.exec()
```

## Styling and Theming

All dialogs use standard PySide6 widgets and support Qt stylesheets:

```python
# Apply custom stylesheet
dialog.setStyleSheet("""
    QGroupBox {
        font-weight: bold;
        border: 2px solid gray;
        border-radius: 5px;
        margin-top: 10px;
        padding-top: 10px;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 5px 0 5px;
    }
""")
```

## Best Practices

1. **Mission Generation**: Always check for available missions before showing selection dialog
2. **Signal Connections**: Connect signals before showing dialogs to avoid missing events
3. **Tracker Updates**: Call `update_missions()` after any mission state change
4. **Parent Widget**: Always provide parent widget for proper modal behavior
5. **Error Handling**: Validate mission data before displaying in dialogs

## Testing

UI components can be tested with pytest and pytest-qt:

```python
def test_mission_briefing_dialog(qtbot, sample_mission):
    dialog = MissionBriefingDialog(sample_mission)
    qtbot.addWidget(dialog)

    # Test dialog creation
    assert dialog.mission == sample_mission
    assert dialog.windowTitle() == "Mission Briefing"

    # Test accept button
    with qtbot.waitSignal(dialog.mission_accepted):
        dialog._on_accept()
```

## Future Enhancements

- Mission icons and visual indicators
- Animated reward display
- Mission history viewer
- Mission recommendation system
- Dynamic difficulty warnings
- Mission chain visualization
- Time-sensitive mission timers

## Related Documentation

- [mission_manager_doc.md](../../components/mission_manager_doc.md) - Mission system architecture
- [DESIGN.md](../../../../docs/DESIGN.md) - Dialog and menu systems milestone
- [PySide6 Documentation](https://doc.qt.io/qtforpython-6/) - Qt framework reference

## Version History

- **v0.0.25** (2025-10-31): Initial implementation
  - MissionBriefingDialog with full mission details
  - MissionSelectionDialog for starbase interaction
  - MissionTrackerWidget for active mission display
  - ObjectiveProgressBar for progress visualization
  - Utility functions for formatting and styling
