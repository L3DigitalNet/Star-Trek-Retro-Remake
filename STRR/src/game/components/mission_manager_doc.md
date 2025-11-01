# Mission Manager Documentation

## Overview

The Mission Manager is a comprehensive system for managing mission objectives, lifecycle, and rewards in Star Trek Retro Remake. It provides a flexible framework for creating, tracking, and completing various types of missions throughout the game.

## Architecture

### Components

- **MissionType**: Enum defining mission categories (PATROL, COMBAT, ESCORT, RESCUE, DIPLOMATIC, SURVEY)
- **MissionStatus**: Enum tracking mission lifecycle (AVAILABLE, ACTIVE, COMPLETED, FAILED)
- **MissionObjective**: Individual objectives within missions with progress tracking
- **MissionReward**: Reward structure with reputation, supplies, spare parts, and experience
- **Mission**: Complete mission definition with objectives, rewards, and state
- **MissionManager**: Central manager coordinating all mission operations

### Data Flow

```
Mission Templates (TOML) → MissionManager.generate_mission() → Mission Instance
                                                              ↓
Player accepts mission → Mission.status = ACTIVE → MissionManager.active_missions
                                                              ↓
Objectives completed → Mission.update() → Auto-complete → MissionManager.completed_missions
```

## Mission Types

### 1. Patrol Mission
- **Objective**: Scan designated waypoints and report anomalies
- **Base Rewards**: 10 reputation, 5 supplies, 50 experience
- **Difficulty Scaling**: Increases waypoint count

### 2. Combat Mission
- **Objective**: Engage and defeat enemy vessels
- **Base Rewards**: 20 reputation, 10 spare parts, 100 experience
- **Difficulty Scaling**: Increases enemy count and strength

### 3. Escort Mission
- **Objective**: Protect civilian transport between locations
- **Base Rewards**: 15 reputation, 10 supplies, 5 spare parts, 75 experience
- **Difficulty Scaling**: Increases distance and threat level

### 4. Rescue Mission
- **Objective**: Locate and recover stranded vessels or crew
- **Base Rewards**: 25 reputation, 125 experience
- **Difficulty Scaling**: Increases search area and hazards

### 5. Diplomatic Mission
- **Objective**: Transport diplomats or conduct negotiations
- **Base Rewards**: 30 reputation, 15 supplies, 5 spare parts, 150 experience
- **Difficulty Scaling**: Increases distance and political complexity

### 6. Survey Mission
- **Objective**: Gather scientific data from anomalies or planets
- **Base Rewards**: 12 reputation, 5 supplies, 5 spare parts, 80 experience
- **Difficulty Scaling**: Increases scan targets and data points

## Usage

### Creating Missions

```python
from pathlib import Path
from STRR.src.game.components.mission_manager import (
    MissionManager,
    MissionType
)

# Initialize manager with templates
mission_path = Path("assets/data/mission_templates.toml")
manager = MissionManager(mission_path)

# Generate new mission
mission = manager.generate_mission(
    mission_type=MissionType.PATROL,
    difficulty=2,
    sector_location="A5"
)
```

### Managing Mission Lifecycle

```python
# Accept mission
manager.accept_mission(mission)

# Update objectives during gameplay
mission.objectives[0].update_progress(1)

# Update mission state each turn
manager.update_active_missions()

# Complete mission and grant rewards
if mission.is_completed():
    manager.complete_mission(mission, player_ship)
```

### Querying Missions

```python
# Get active mission count
count = manager.get_active_mission_count()

# Get missions for specific sector
sector_missions = manager.get_available_missions_by_sector("B3")

# Check mission status
if mission.status == MissionStatus.ACTIVE:
    print(f"Turns active: {mission.turns_active}")
```

## Mission Templates (TOML)

### Template Structure

```toml
[missions.mission_type]
name = "Mission Name"
description = "Mission description"
mission_type = "TYPE"

[[missions.mission_type.objectives]]
description = "Objective description"
type = "objective_type"
target_count = 1

[missions.mission_type.rewards]
reputation = 10
supplies = 5
spare_parts = 0
experience = 50
```

### Difficulty Scaling

- **Objective Targets**: `target_count * difficulty`
- **Rewards**: All reward values multiplied by difficulty
- **Example**: Difficulty 3 mission has 3x targets and 3x rewards

## Integration with GameModel

The Mission Manager is integrated into the GameModel for seamless gameplay:

```python
# In GameModel.__init__()
mission_path = Path(__file__).parent.parent.parent / "assets" / "data" / "mission_templates.toml"
self.mission_manager = MissionManager(mission_path)

# Update missions each turn
def update_missions(self) -> None:
    self.mission_manager.update_active_missions()
```

## Testing

Comprehensive unit tests cover:
- Mission objective creation and progress tracking
- Mission lifecycle state transitions
- Mission manager operations (accept, abandon, complete)
- Mission generation from templates
- Reward calculation and scaling
- Sector-based mission filtering

Run tests:
```bash
pytest STRR/tests/test_mission_manager.py -v
```

## Future Enhancements

### Planned Features
- **Mission Chains**: Sequential missions forming campaign arcs
- **Time-Sensitive Missions**: Deadlines and time pressure
- **Dynamic Mission Generation**: Procedural story elements
- **Multi-Stage Missions**: Objectives that unlock progressively
- **Mission Dialog System**: Interactive briefings and debriefings

### Configuration Options
- Mission generation frequency
- Maximum active mission limit
- Reputation thresholds for mission access
- Failure penalties and consequences

## File Structure

```
STRR/
├── src/game/components/
│   └── mission_manager.py         # Mission system implementation
├── assets/data/
│   └── mission_templates.toml     # Mission definitions
└── tests/
    └── test_mission_manager.py    # Unit tests
```

## Version History

- **v0.0.24** (2025-10-31): Initial mission system implementation
  - Core mission data structures
  - Mission manager with lifecycle tracking
  - TOML-based mission templates
  - 18 comprehensive unit tests with 100% pass rate
  - Integration with GameModel

## API Reference

### MissionManager

#### Methods

- `__init__(mission_data_path: Path)`: Initialize with mission templates
- `generate_mission(mission_type, difficulty, sector_location)`: Create new mission
- `accept_mission(mission)`: Accept available mission
- `abandon_mission(mission)`: Abandon active mission (reputation penalty)
- `complete_mission(mission, player_ship)`: Complete mission and grant rewards
- `update_active_missions()`: Update all active missions
- `get_active_mission_count()`: Get count of active missions
- `get_available_missions_by_sector(sector)`: Filter missions by sector

### Mission

#### Attributes

- `mission_id`: Unique identifier
- `mission_type`: MissionType enum
- `name`: Mission title
- `description`: Mission briefing text
- `objectives`: List of MissionObjective instances
- `reward`: MissionReward instance
- `status`: MissionStatus enum
- `difficulty`: Integer difficulty rating (1-5)
- `sector_location`: Sector coordinates
- `turns_active`: Turn counter

#### Methods

- `is_completed()`: Check if all objectives are completed
- `update()`: Update mission state and increment turn counter

### MissionObjective

#### Attributes

- `description`: Human-readable objective text
- `objective_type`: Type identifier string
- `target_count`: Number required for completion
- `current_count`: Current progress
- `completed`: Completion flag

#### Methods

- `update_progress(amount=1)`: Increment progress and check completion

## Best Practices

1. **Generate missions at starbases**: Create missions when player docks
2. **Limit active missions**: Recommend 3-5 active missions maximum
3. **Update each turn**: Call `update_active_missions()` in turn advance
4. **Scale appropriately**: Match difficulty to player progression
5. **Test mission flow**: Verify complete lifecycle before deployment

## Troubleshooting

### Common Issues

**Issue**: Missions not auto-completing
- **Solution**: Ensure `update_active_missions()` is called each turn

**Issue**: Reward scaling incorrect
- **Solution**: Check TOML template base values and difficulty multiplier

**Issue**: Templates not loading
- **Solution**: Verify TOML file path and syntax validity

## Related Documentation

- [DESIGN.md](../../../docs/DESIGN.md) - Mission system milestones
- [ARCHITECTURE.md](../../../docs/ARCHITECTURE.md) - Component architecture
- [GameModel Documentation](model_doc.md) - Integration details
