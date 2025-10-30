#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Star Trek Retro Remake - Custom Exceptions

Description:
    Custom exception classes for game-specific error handling.

Author: Star Trek Retro Remake Development Team
Email: development@star-trek-retro-remake.org
GitHub: https://github.com/L3DigitalNet/Star-Trek-Retro-Remake
Date Created: 10-29-2025
Date Changed: 10-30-2025
License: MIT

Features:
    - Hierarchical exception structure
    - Game-specific error types
    - Clear error messaging
    - Facilitates debugging and error handling

Requirements:
    - Linux environment
    - Python 3.14+ for latest language features

Classes:
    - GameError: Base exception for all game errors
    - InvalidMoveError: Raised for invalid movement attempts
    - InsufficientResourcesError: Raised when resources are insufficient
    - SystemOfflineError: Raised when ship system is offline
    - CombatError: Raised for combat-related errors
    - ConfigurationError: Raised for configuration problems
    - SaveLoadError: Raised for save/load failures

Functions:
    - None
"""

from typing import Final, Optional

__version__: Final[str] = "0.0.1"


class GameError(Exception):
    """
    Base exception for all game-related errors.

    All custom game exceptions should inherit from this class
    to allow for consistent error handling throughout the application.
    """

    def __init__(self, message: str, details: Optional[dict] = None):
        """
        Initialize game error.

        Args:
            message: Error message describing the problem
            details: Optional dictionary with additional error details
        """
        super().__init__(message)
        self.message = message
        self.details = details or {}


class InvalidMoveError(GameError):
    """
    Raised when attempting an invalid move.

    This exception is raised when a starship attempts to move to
    an invalid position (out of bounds, blocked, etc.).
    """

    def __init__(self, message: str = "Invalid move attempt", **kwargs):
        """
        Initialize invalid move error.

        Args:
            message: Error message
            **kwargs: Additional details (position, reason, etc.)
        """
        super().__init__(message, kwargs)


class InsufficientResourcesError(GameError):
    """
    Raised when resources are insufficient for an action.

    This exception is raised when attempting an action that requires
    more resources than are currently available (fuel, energy, etc.).
    """

    def __init__(
        self,
        resource_type: str,
        required: float,
        available: float,
        message: Optional[str] = None
    ):
        """
        Initialize insufficient resources error.

        Args:
            resource_type: Type of resource that is insufficient
            required: Amount of resource required
            available: Amount of resource available
            message: Optional custom error message
        """
        if message is None:
            message = (
                f"Insufficient {resource_type}: "
                f"required {required}, available {available}"
            )
        super().__init__(
            message,
            {
                "resource_type": resource_type,
                "required": required,
                "available": available
            }
        )


class SystemOfflineError(GameError):
    """
    Raised when attempting to use an offline ship system.

    This exception is raised when trying to use a ship system
    that is currently offline or destroyed.
    """

    def __init__(self, system_name: str, message: Optional[str] = None):
        """
        Initialize system offline error.

        Args:
            system_name: Name of the offline system
            message: Optional custom error message
        """
        if message is None:
            message = f"System '{system_name}' is offline"
        super().__init__(message, {"system_name": system_name})


class CombatError(GameError):
    """
    Raised for combat-related errors.

    This exception is raised when combat actions fail or encounter
    invalid conditions (out of range, no valid target, etc.).
    """

    def __init__(self, message: str = "Combat error occurred", **kwargs):
        """
        Initialize combat error.

        Args:
            message: Error message
            **kwargs: Additional details (target, weapon, reason, etc.)
        """
        super().__init__(message, kwargs)


class ConfigurationError(GameError):
    """
    Raised for configuration-related problems.

    This exception is raised when configuration files are missing,
    malformed, or contain invalid values.
    """

    def __init__(
        self,
        config_name: str,
        message: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize configuration error.

        Args:
            config_name: Name of the configuration file/section
            message: Optional custom error message
            **kwargs: Additional details
        """
        if message is None:
            message = f"Configuration error in '{config_name}'"
        super().__init__(message, {"config_name": config_name, **kwargs})


class SaveLoadError(GameError):
    """
    Raised for save/load operation failures.

    This exception is raised when save or load operations fail
    due to file access, corruption, or format issues.
    """

    def __init__(
        self,
        operation: str,
        filepath: str,
        message: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize save/load error.

        Args:
            operation: Operation that failed ('save' or 'load')
            filepath: Path to the save file
            message: Optional custom error message
            **kwargs: Additional details
        """
        if message is None:
            message = f"Failed to {operation} game from '{filepath}'"
        super().__init__(
            message,
            {"operation": operation, "filepath": filepath, **kwargs}
        )


class StateTransitionError(GameError):
    """
    Raised when an invalid state transition is attempted.

    This exception is raised when trying to transition between
    game states in an invalid manner.
    """

    def __init__(
        self,
        from_state: str,
        to_state: str,
        message: Optional[str] = None
    ):
        """
        Initialize state transition error.

        Args:
            from_state: Current state
            to_state: Attempted target state
            message: Optional custom error message
        """
        if message is None:
            message = f"Invalid transition from '{from_state}' to '{to_state}'"
        super().__init__(
            message,
            {"from_state": from_state, "to_state": to_state}
        )


class EntityNotFoundError(GameError):
    """
    Raised when an entity cannot be found.

    This exception is raised when attempting to access or manipulate
    an entity that doesn't exist or cannot be located.
    """

    def __init__(self, entity_id: str, message: Optional[str] = None):
        """
        Initialize entity not found error.

        Args:
            entity_id: ID of the entity that was not found
            message: Optional custom error message
        """
        if message is None:
            message = f"Entity with ID '{entity_id}' not found"
        super().__init__(message, {"entity_id": entity_id})
