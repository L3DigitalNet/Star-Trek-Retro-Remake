# Events Documentation

**File:** `STRR/src/game/events.py`
**Version:** 0.0.1
**Last Updated:** 10-30-2025

---

## Purpose

Implements an **Event Bus** system for loose coupling between game components. Enables **publish/subscribe** pattern for component communication without direct dependencies.

---

## Architecture

### Publish/Subscribe Pattern

```
Component A → publish(event) → EventBus → notify → Component B (subscribed)
                                        → notify → Component C (subscribed)
```

Components communicate through events, not direct references.

---

## Classes

### EventPriority (Enum)

Priority levels for event handling:

- `LOW`: Non-critical events
- `NORMAL`: Standard events
- `HIGH`: Important events
- `CRITICAL`: Must-process-first events

---

### GameEvent (dataclass)

**Purpose:** Container for event data

**Attributes:**

- `event_type` (str): Event identifier (e.g., "ship_destroyed")
- `data` (dict): Event-specific data
- `priority` (EventPriority): Handling priority
- `timestamp` (float): When event occurred
- `handled` (bool): Whether processed

**Methods:**

- `mark_handled()`: Mark as processed
- `is_handled()`: Check if processed

---

### EventBus

**Purpose:** Central event dispatcher

**Key Methods:**

- `subscribe(event_type, callback, priority, filter)`: Register listener
- `unsubscribe(event_type, callback)`: Remove listener
- `publish(event)`: Dispatch event to listeners
- `clear(event_type)`: Remove all listeners
- `enable()` / `disable()`: Control event bus

**Priority Handling:** Higher priority listeners execute first

---

## Usage Examples

### Example 1: Basic Pub/Sub

```python
from game.events import get_event_bus, GameEvent, EventPriority

# Get global event bus
bus = get_event_bus()

# Subscribe to event
def on_ship_destroyed(event):
    print(f"Ship destroyed: {event.data['ship_name']}")

bus.subscribe("ship_destroyed", on_ship_destroyed)

# Publish event
event = GameEvent(
    "ship_destroyed",
    data={"ship_name": "Enterprise", "killer": "Klingon"},
    priority=EventPriority.HIGH
)
bus.publish(event)
```

### Example 2: Filtered Subscription

```python
# Only receive events for player's ship
def is_player_ship(event):
    return event.data.get("player_owned", False)

bus.subscribe(
    "ship_damaged",
    on_player_damage,
    event_filter=is_player_ship
)
```

### Example 3: Convenience Functions

```python
from game.events import publish_event, subscribe_event, GameEvent

# Subscribe
subscribe_event("combat_start", handle_combat)

# Publish
publish_event(GameEvent("combat_start", {"attacker": ship_id}))
```

---

## Common Event Types

Suggested event types for the game:

- `"ship_moved"`: Ship changed position
- `"ship_destroyed"`: Ship eliminated
- `"ship_damaged"`: Ship took damage
- `"combat_start"` / `"combat_end"`: Combat state changes
- `"turn_advanced"`: Turn incremented
- `"mission_started"` / `"mission_completed"`: Mission lifecycle
- `"sector_entered"`: Changed sectors

---

## Integration Points

**Dependencies:** None (standard library only)

**Used by:** Any component needing loosely-coupled communication

---

## Benefits

1. **Loose Coupling:** Components don't need references to each other
2. **Extensibility:** Add new listeners without modifying publishers
3. **Debugging:** Can log all events for debugging
4. **Testing:** Can mock event bus for isolated testing

---

## Change History

- **10-30-2025** - Documentation created
- **10-29-2025** - Event bus system implemented
