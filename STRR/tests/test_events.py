#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Star Trek Retro Remake - Event System Tests

Description:
    Unit tests for event bus system, event handling, and event-driven
    communication between game components.

Author: Star Trek Retro Remake Development Team
Date Created: 10-30-2025
Date Changed: 10-30-2025
License: MIT
"""

from typing import Final
import time

from src.game.events import (
    GameEvent,
    EventPriority,
    EventListener,
    EventBus,
)

__version__: Final[str] = "0.0.11"


class TestGameEvent:
    """Test cases for GameEvent class."""

    def test_event_creation(self):
        """Test creating a game event."""
        # Arrange & Act
        event = GameEvent("test_event")

        # Assert
        assert event.event_type == "test_event"
        assert event.data == {}
        assert event.priority == EventPriority.NORMAL
        assert event.handled is False

    def test_event_with_data(self):
        """Test creating an event with data."""
        # Arrange
        data = {"player": "Enterprise", "action": "move"}

        # Act
        event = GameEvent("player_move", data=data)

        # Assert
        assert event.event_type == "player_move"
        assert event.data["player"] == "Enterprise"
        assert event.data["action"] == "move"

    def test_event_with_priority(self):
        """Test creating an event with specific priority."""
        # Arrange & Act
        event = GameEvent("critical_event", priority=EventPriority.CRITICAL)

        # Assert
        assert event.priority == EventPriority.CRITICAL

    def test_mark_event_handled(self):
        """Test marking an event as handled."""
        # Arrange
        event = GameEvent("test_event")
        assert event.handled is False

        # Act
        event.mark_handled()

        # Assert
        assert event.handled is True
        assert event.is_handled() is True


class TestEventPriority:
    """Test cases for EventPriority enum."""

    def test_priority_levels_exist(self):
        """Test that all priority levels are defined."""
        # Arrange & Act & Assert
        assert EventPriority.LOW
        assert EventPriority.NORMAL
        assert EventPriority.HIGH
        assert EventPriority.CRITICAL

    def test_priority_order(self):
        """Test that priority levels have correct ordering."""
        # Arrange
        priorities = [
            EventPriority.LOW,
            EventPriority.NORMAL,
            EventPriority.HIGH,
            EventPriority.CRITICAL,
        ]

        # Act - Get auto-generated values
        values = [p.value for p in priorities]

        # Assert - Values should be in ascending order
        assert values == sorted(values)


class TestEventListener:
    """Test cases for EventListener wrapper."""

    def test_listener_creation(self):
        """Test creating an event listener."""

        # Arrange
        def test_callback(event):
            pass

        # Act
        listener = EventListener(callback=test_callback, priority=EventPriority.HIGH)

        # Assert
        assert listener.callback == test_callback
        assert listener.priority == EventPriority.HIGH
        assert listener.event_filter is None

    def test_listener_with_filter(self):
        """Test creating a listener with event filter."""

        # Arrange
        def test_callback(event):
            pass

        def test_filter(event):
            return event.priority == EventPriority.CRITICAL

        # Act
        listener = EventListener(
            callback=test_callback,
            priority=EventPriority.NORMAL,
            event_filter=test_filter,
        )

        # Assert
        assert listener.event_filter is not None
        # Test the filter
        critical_event = GameEvent("test", priority=EventPriority.CRITICAL)
        normal_event = GameEvent("test", priority=EventPriority.NORMAL)
        assert listener.event_filter(critical_event) is True
        assert listener.event_filter(normal_event) is False


class TestEventBus:
    """Test cases for EventBus dispatcher."""

    def test_event_bus_initialization(self):
        """Test that EventBus initializes correctly."""
        # Arrange & Act
        bus = EventBus()

        # Assert
        assert bus.listeners == {}
        assert bus.enabled is True

    def test_subscribe_to_event(self):
        """Test subscribing to an event type."""
        # Arrange
        bus = EventBus()
        callback_executed = False

        def test_callback(event):
            nonlocal callback_executed
            callback_executed = True

        # Act
        bus.subscribe("test_event", test_callback)

        # Assert
        assert "test_event" in bus.listeners
        assert len(bus.listeners["test_event"]) == 1

    def test_subscribe_multiple_listeners(self):
        """Test subscribing multiple listeners to same event."""
        # Arrange
        bus = EventBus()

        def callback1(event):
            pass

        def callback2(event):
            pass

        # Act
        bus.subscribe("test_event", callback1)
        bus.subscribe("test_event", callback2)

        # Assert
        assert len(bus.listeners["test_event"]) == 2

    def test_unsubscribe_from_event(self):
        """Test unsubscribing from an event."""
        # Arrange
        bus = EventBus()

        def test_callback(event):
            pass

        bus.subscribe("test_event", test_callback)

        # Act
        result = bus.unsubscribe("test_event", test_callback)

        # Assert
        assert result is True
        assert len(bus.listeners.get("test_event", [])) == 0

    def test_publish_event(self):
        """Test publishing an event."""
        # Arrange
        bus = EventBus()
        received_event = None

        def test_callback(event):
            nonlocal received_event
            received_event = event

        bus.subscribe("test_event", test_callback)

        # Act
        event = GameEvent("test_event", data={"value": 42})
        bus.publish(event)

        # Assert
        assert received_event is not None
        assert received_event.event_type == "test_event"
        assert received_event.data["value"] == 42

    def test_publish_with_no_listeners(self):
        """Test publishing an event with no listeners doesn't crash."""
        # Arrange
        bus = EventBus()

        # Act
        event = GameEvent("unsubscribed_event")
        bus.publish(event)  # Should not raise exception

        # Assert - If we get here, test passes

    def test_priority_order_execution(self):
        """Test that listeners execute in priority order."""
        # Arrange
        bus = EventBus()
        execution_order = []

        def low_priority_callback(event):
            execution_order.append("low")

        def high_priority_callback(event):
            execution_order.append("high")

        def critical_priority_callback(event):
            execution_order.append("critical")

        # Act
        bus.subscribe("test_event", low_priority_callback, priority=EventPriority.LOW)
        bus.subscribe("test_event", high_priority_callback, priority=EventPriority.HIGH)
        bus.subscribe(
            "test_event", critical_priority_callback, priority=EventPriority.CRITICAL
        )

        event = GameEvent("test_event")
        bus.publish(event)

        # Assert
        assert execution_order == ["critical", "high", "low"]

    def test_event_filter_blocks_listener(self):
        """Test that event filter can block listener execution."""
        # Arrange
        bus = EventBus()
        callback_executed = False

        def test_callback(event):
            nonlocal callback_executed
            callback_executed = True

        def filter_critical_only(event):
            return event.priority == EventPriority.CRITICAL

        # Act
        bus.subscribe("test_event", test_callback, event_filter=filter_critical_only)

        # Publish normal priority event (should be filtered)
        normal_event = GameEvent("test_event", priority=EventPriority.NORMAL)
        bus.publish(normal_event)

        # Assert
        assert callback_executed is False

        # Publish critical priority event (should pass filter)
        critical_event = GameEvent("test_event", priority=EventPriority.CRITICAL)
        bus.publish(critical_event)

        assert callback_executed is True

    def test_handled_event_stops_propagation(self):
        """Test that marking event as handled stops propagation."""
        # Arrange
        bus = EventBus()
        first_executed = False
        second_executed = False

        def first_callback(event):
            nonlocal first_executed
            first_executed = True
            event.mark_handled()  # Stop propagation

        def second_callback(event):
            nonlocal second_executed
            second_executed = True

        # Act
        bus.subscribe("test_event", first_callback, priority=EventPriority.HIGH)
        bus.subscribe("test_event", second_callback, priority=EventPriority.LOW)

        event = GameEvent("test_event")
        bus.publish(event)

        # Assert
        assert first_executed is True
        assert second_executed is False  # Should not execute

    def test_clear_specific_event(self):
        """Test clearing listeners for specific event type."""
        # Arrange
        bus = EventBus()

        def callback1(event):
            pass

        def callback2(event):
            pass

        bus.subscribe("test_event", callback1)
        bus.subscribe("other_event", callback2)

        # Act
        bus.clear("test_event")

        # Assert
        assert (
            "test_event" not in bus.listeners
            or len(bus.listeners.get("test_event", [])) == 0
        )
        assert "other_event" in bus.listeners

    def test_clear_all_events(self):
        """Test clearing all event listeners."""
        # Arrange
        bus = EventBus()

        def callback1(event):
            pass

        def callback2(event):
            pass

        bus.subscribe("test_event", callback1)
        bus.subscribe("other_event", callback2)

        # Act
        bus.clear()

        # Assert
        assert len(bus.listeners) == 0

    def test_enable_disable_event_bus(self):
        """Test enabling and disabling the event bus."""
        # Arrange
        bus = EventBus()
        callback_executed = False

        def test_callback(event):
            nonlocal callback_executed
            callback_executed = True

        bus.subscribe("test_event", test_callback)

        # Act - Disable bus
        bus.disable()
        bus.publish(GameEvent("test_event"))

        # Assert - Callback should not execute
        assert callback_executed is False

        # Act - Re-enable bus
        bus.enable()
        bus.publish(GameEvent("test_event"))

        # Assert - Callback should execute
        assert callback_executed is True

    def test_event_data_mutation(self):
        """Test that event data can be mutated by listeners."""
        # Arrange
        bus = EventBus()

        def mutate_callback(event):
            event.data["modified"] = True

        bus.subscribe("test_event", mutate_callback)

        # Act
        event = GameEvent("test_event", data={"initial": "value"})
        bus.publish(event)

        # Assert
        assert event.data["modified"] is True
        assert event.data["initial"] == "value"


class TestEventBusIntegration:
    """Integration tests for EventBus with multiple components."""

    def test_multiple_event_types(self):
        """Test handling multiple different event types."""
        # Arrange
        bus = EventBus()
        combat_events = []
        movement_events = []

        def combat_callback(event):
            combat_events.append(event)

        def movement_callback(event):
            movement_events.append(event)

        bus.subscribe("combat", combat_callback)
        bus.subscribe("movement", movement_callback)

        # Act
        bus.publish(GameEvent("combat", data={"damage": 10}))
        bus.publish(GameEvent("movement", data={"position": (5, 5)}))
        bus.publish(GameEvent("combat", data={"damage": 20}))

        # Assert
        assert len(combat_events) == 2
        assert len(movement_events) == 1

    def test_event_chain_reaction(self):
        """Test that events can trigger other events."""
        # Arrange
        bus = EventBus()
        events_fired = []

        def first_callback(event):
            events_fired.append("first")
            # Trigger secondary event
            bus.publish(GameEvent("secondary"))

        def second_callback(event):
            events_fired.append("second")

        bus.subscribe("primary", first_callback)
        bus.subscribe("secondary", second_callback)

        # Act
        bus.publish(GameEvent("primary"))

        # Assert
        assert events_fired == ["first", "second"]
