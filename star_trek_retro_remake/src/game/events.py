#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Star Trek Retro Remake - Event System

Description:
    Event bus system for loose coupling between game components.
    Allows components to communicate without direct dependencies.

Author: Star Trek Retro Remake Development Team
Email: development@star-trek-retro-remake.org
GitHub: https://github.com/L3DigitalNet/Star-Trek-Retro-Remake
Date Created: 10-29-2025
Date Changed: 10-29-2025
License: MIT

Features:
    - Event bus for publish/subscribe pattern
    - Type-safe event definitions
    - Priority-based event handling
    - Event filtering and validation

Requirements:
    - Linux environment
    - Python 3.14+ for latest language features

Classes:
    - GameEvent: Base event class
    - EventBus: Central event dispatcher
    - EventPriority: Event priority levels

Functions:
    - None
"""

import logging
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Final, Callable, Any, Optional

__version__: Final[str] = "0.0.1"

logger = logging.getLogger(__name__)


class EventPriority(Enum):
    """Priority levels for event handling."""
    LOW = auto()
    NORMAL = auto()
    HIGH = auto()
    CRITICAL = auto()


@dataclass
class GameEvent:
    """
    Base class for all game events.

    Events are used to notify components about game state changes
    and actions without creating direct dependencies.

    Attributes:
        event_type: Type identifier for this event
        data: Event-specific data dictionary
        priority: Event handling priority
        timestamp: Event creation timestamp
        handled: Whether event has been handled

    Public methods:
        mark_handled: Mark event as handled
        is_handled: Check if event has been handled
    """
    event_type: str
    data: dict[str, Any] = field(default_factory=dict)
    priority: EventPriority = EventPriority.NORMAL
    timestamp: float = field(default=0.0)
    handled: bool = field(default=False)

    def mark_handled(self) -> None:
        """Mark this event as handled."""
        self.handled = True

    def is_handled(self) -> bool:
        """
        Check if event has been handled.

        Returns:
            True if event has been handled, False otherwise
        """
        return self.handled


@dataclass
class EventListener:
    """
    Event listener wrapper with priority and filtering.

    Attributes:
        callback: Function to call when event occurs
        priority: Listener priority for execution order
        event_filter: Optional filter function for events
    """
    callback: Callable[[GameEvent], None]
    priority: EventPriority = EventPriority.NORMAL
    event_filter: Optional[Callable[[GameEvent], bool]] = None


class EventBus:
    """
    Central event dispatcher for game-wide communication.

    Implements publish/subscribe pattern for loose coupling between
    game components.

    Attributes:
        listeners: Dictionary of event listeners by event type
        enabled: Whether event bus is active

    Public methods:
        subscribe: Register event listener
        unsubscribe: Remove event listener
        publish: Dispatch event to all listeners
        clear: Remove all listeners
        enable: Enable event bus
        disable: Disable event bus

    Private methods:
        _get_sorted_listeners: Get listeners sorted by priority
        _should_handle_event: Check if listener should handle event
    """

    def __init__(self):
        """Initialize the event bus."""
        self.listeners: dict[str, list[EventListener]] = {}
        self.enabled = True
        logger.debug("Event bus initialized")

    def subscribe(
        self,
        event_type: str,
        callback: Callable[[GameEvent], None],
        priority: EventPriority = EventPriority.NORMAL,
        event_filter: Optional[Callable[[GameEvent], bool]] = None
    ) -> None:
        """
        Register an event listener.

        Args:
            event_type: Type of event to listen for
            callback: Function to call when event occurs
            priority: Listener priority for execution order
            event_filter: Optional filter function for events
        """
        if event_type not in self.listeners:
            self.listeners[event_type] = []

        listener = EventListener(callback, priority, event_filter)
        self.listeners[event_type].append(listener)

        logger.debug(
            "Subscribed listener for event '%s' with priority %s",
            event_type, priority.name
        )

    def unsubscribe(
        self,
        event_type: str,
        callback: Callable[[GameEvent], None]
    ) -> bool:
        """
        Remove an event listener.

        Args:
            event_type: Type of event to stop listening for
            callback: Previously registered callback function

        Returns:
            True if listener was removed, False if not found
        """
        if event_type not in self.listeners:
            return False

        initial_count = len(self.listeners[event_type])
        self.listeners[event_type] = [
            listener for listener in self.listeners[event_type]
            if listener.callback != callback
        ]

        removed = len(self.listeners[event_type]) < initial_count

        if removed:
            logger.debug("Unsubscribed listener for event '%s'", event_type)

        return removed

    def publish(self, event: GameEvent) -> None:
        """
        Dispatch event to all registered listeners.

        Args:
            event: Event to publish
        """
        if not self.enabled:
            logger.debug("Event bus disabled, ignoring event '%s'", event.event_type)
            return

        if event.event_type not in self.listeners:
            logger.debug("No listeners for event '%s'", event.event_type)
            return

        # Get listeners sorted by priority
        sorted_listeners = self._get_sorted_listeners(event.event_type)

        logger.debug(
            "Publishing event '%s' to %d listeners",
            event.event_type, len(sorted_listeners)
        )

        # Dispatch to each listener
        for listener in sorted_listeners:
            if event.is_handled():
                break

            if self._should_handle_event(listener, event):
                try:
                    listener.callback(event)
                except Exception as e:
                    logger.error(
                        "Error in event listener for '%s': %s",
                        event.event_type, e, exc_info=True
                    )

    def clear(self, event_type: Optional[str] = None) -> None:
        """
        Remove all listeners.

        Args:
            event_type: Optional specific event type to clear,
                       or None to clear all
        """
        if event_type is None:
            self.listeners.clear()
            logger.debug("Cleared all event listeners")
        elif event_type in self.listeners:
            del self.listeners[event_type]
            logger.debug("Cleared listeners for event '%s'", event_type)

    def enable(self) -> None:
        """Enable the event bus."""
        self.enabled = True
        logger.debug("Event bus enabled")

    def disable(self) -> None:
        """Disable the event bus."""
        self.enabled = False
        logger.debug("Event bus disabled")

    def _get_sorted_listeners(self, event_type: str) -> list[EventListener]:
        """
        Get listeners sorted by priority.

        Args:
            event_type: Event type to get listeners for

        Returns:
            List of listeners sorted by priority (high to low)
        """
        listeners = self.listeners.get(event_type, [])
        return sorted(listeners, key=lambda l: l.priority.value, reverse=True)

    def _should_handle_event(
        self,
        listener: EventListener,
        event: GameEvent
    ) -> bool:
        """
        Check if listener should handle event based on filter.

        Args:
            listener: Event listener to check
            event: Event to potentially handle

        Returns:
            True if listener should handle event, False otherwise
        """
        if listener.event_filter is None:
            return True

        try:
            return listener.event_filter(event)
        except Exception as e:
            logger.error("Error in event filter: %s", e, exc_info=True)
            return False


# Global event bus instance
_global_event_bus: Optional[EventBus] = None


def get_event_bus() -> EventBus:
    """
    Get the global event bus instance.

    Returns:
        Global EventBus instance
    """
    global _global_event_bus
    if _global_event_bus is None:
        _global_event_bus = EventBus()
    return _global_event_bus


def publish_event(event: GameEvent) -> None:
    """
    Convenience function to publish event to global bus.

    Args:
        event: Event to publish
    """
    get_event_bus().publish(event)


def subscribe_event(
    event_type: str,
    callback: Callable[[GameEvent], None],
    priority: EventPriority = EventPriority.NORMAL,
    event_filter: Optional[Callable[[GameEvent], bool]] = None
) -> None:
    """
    Convenience function to subscribe to global event bus.

    Args:
        event_type: Type of event to listen for
        callback: Function to call when event occurs
        priority: Listener priority for execution order
        event_filter: Optional filter function for events
    """
    get_event_bus().subscribe(event_type, callback, priority, event_filter)


def unsubscribe_event(
    event_type: str,
    callback: Callable[[GameEvent], None]
) -> bool:
    """
    Convenience function to unsubscribe from global event bus.

    Args:
        event_type: Type of event to stop listening for
        callback: Previously registered callback function

    Returns:
        True if listener was removed, False if not found
    """
    return get_event_bus().unsubscribe(event_type, callback)
