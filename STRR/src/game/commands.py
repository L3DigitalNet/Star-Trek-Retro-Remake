#!/usr/bin/env python3
"""
Star Trek Retro Remake - Command Pattern

Description:
    Command pattern implementation for undoable game actions.
    Allows for command history, undo/redo functionality, and macro recording.

Author: Star Trek Retro Remake Development Team
Email: development@star-trek-retro-remake.org
GitHub: https://github.com/L3DigitalNet/Star-Trek-Retro-Remake
Date Created: 10-29-2025
Date Changed: 10-30-2025
License: MIT

Features:
    - Command pattern for undoable actions
    - Command history management
    - Undo/redo stack implementation
    - Macro recording and playback

Requirements:
    - Linux environment
    - Python 3.14+ for latest language features

Classes:
    - Command: Abstract base command
    - MoveShipCommand: Ship movement command
    - FireWeaponCommand: Weapon firing command
    - CommandHistory: Command history manager

Functions:
    - None
"""

import logging
from abc import ABC, abstractmethod
from typing import Final, Optional

from .entities.base import GridPosition
from .entities.starship import Starship
from .exceptions import InvalidMoveError

__version__: Final[str] = "0.0.21"

logger = logging.getLogger(__name__)


class Command(ABC):
    """
    Abstract base class for all commands.

    Implements the Command pattern allowing actions to be executed,
    undone, and redone with full state tracking.

    Attributes:
        executed: Whether command has been executed
        description: Human-readable command description

    Public methods:
        execute: Execute the command
        undo: Undo the command
        can_execute: Check if command can be executed
        can_undo: Check if command can be undone

    Private methods:
        _do_execute: Actual execution logic (override in subclasses)
        _do_undo: Actual undo logic (override in subclasses)
    """

    def __init__(self, description: str = ""):
        """
        Initialize command.

        Args:
            description: Human-readable description of the command
        """
        self.executed = False
        self.description = description

    def execute(self) -> bool:
        """
        Execute the command.

        Returns:
            True if execution was successful, False otherwise
        """
        if not self.can_execute():
            logger.warning("Cannot execute command: %s", self.description)
            return False

        try:
            result = self._do_execute()
            if result:
                self.executed = True
                logger.debug("Executed command: %s", self.description)
            return result
        except Exception as e:
            logger.error("Error executing command: %s", e, exc_info=True)
            return False

    def undo(self) -> bool:
        """
        Undo the command.

        Returns:
            True if undo was successful, False otherwise
        """
        if not self.can_undo():
            logger.warning("Cannot undo command: %s", self.description)
            return False

        try:
            result = self._do_undo()
            if result:
                self.executed = False
                logger.debug("Undid command: %s", self.description)
            return result
        except Exception as e:
            logger.error("Error undoing command: %s", e, exc_info=True)
            return False

    def can_execute(self) -> bool:
        """
        Check if command can be executed.

        Returns:
            True if command can be executed, False otherwise
        """
        return not self.executed

    def can_undo(self) -> bool:
        """
        Check if command can be undone.

        Returns:
            True if command can be undone, False otherwise
        """
        return self.executed

    @abstractmethod
    def _do_execute(self) -> bool:
        """
        Actual execution logic (override in subclasses).

        Returns:
            True if execution was successful, False otherwise
        """
        pass

    @abstractmethod
    def _do_undo(self) -> bool:
        """
        Actual undo logic (override in subclasses).

        Returns:
            True if undo was successful, False otherwise
        """
        pass


class MoveShipCommand(Command):
    """
    Command to move a starship.

    Stores previous position to allow undo functionality.

    Attributes:
        ship: Starship to move
        destination: Target position
        previous_position: Original position (for undo)
        previous_fuel: Original fuel level (for undo)

    Public methods:
        Inherited from Command

    Private methods:
        _do_execute: Execute ship movement
        _do_undo: Restore previous position
    """

    def __init__(self, ship: Starship, destination: GridPosition):
        """
        Initialize move ship command.

        Args:
            ship: Starship to move
            destination: Target position
        """
        super().__init__(
            f"Move {ship.name} to ({destination.x}, {destination.y}, {destination.z})"
        )
        self.ship = ship
        self.destination = destination
        self.previous_position: Optional[GridPosition] = None
        self.previous_fuel: float = 0.0

    def _do_execute(self) -> bool:
        """
        Execute ship movement.

        Returns:
            True if movement was successful, False otherwise
        """
        # Store previous state
        self.previous_position = GridPosition(
            self.ship.position.x, self.ship.position.y, self.ship.position.z
        )

        engines = self.ship.get_system("engines")
        if engines:
            self.previous_fuel = engines.fuel

        # Calculate fuel cost
        distance = int(self.ship.position.distance_to(self.destination))
        if engines:
            fuel_cost = engines.calculate_movement_cost(distance)

            # Check if enough fuel
            if engines.fuel < fuel_cost:
                raise InvalidMoveError(
                    "Insufficient fuel",
                    ship=self.ship.name,
                    required=fuel_cost,
                    available=engines.fuel,
                )

            # Execute move
            self.ship.position = self.destination
            engines.fuel -= fuel_cost
            return True

        return False

    def _do_undo(self) -> bool:
        """
        Restore previous position.

        Returns:
            True if undo was successful, False otherwise
        """
        if self.previous_position is None:
            return False

        # Restore position
        self.ship.position = self.previous_position

        # Restore fuel
        engines = self.ship.get_system("engines")
        if engines:
            engines.fuel = self.previous_fuel

        return True


class FireWeaponCommand(Command):
    """
    Command to fire a weapon.

    Stores weapon state for undo functionality.

    Attributes:
        attacker: Attacking starship
        target: Target starship
        weapon_type: Type of weapon to fire
        damage_dealt: Damage dealt (for reporting)
        previous_target_hull: Target's hull integrity before attack

    Public methods:
        Inherited from Command

    Private methods:
        _do_execute: Fire weapon at target
        _do_undo: Restore target's previous state
    """

    def __init__(self, attacker: Starship, target: Starship, weapon_type: str):
        """
        Initialize fire weapon command.

        Args:
            attacker: Attacking starship
            target: Target starship
            weapon_type: Type of weapon to fire
        """
        super().__init__(f"{attacker.name} fires {weapon_type} at {target.name}")
        self.attacker = attacker
        self.target = target
        self.weapon_type = weapon_type
        self.damage_dealt = 0
        self.previous_target_hull = 0.0

    def _do_execute(self) -> bool:
        """
        Fire weapon at target.

        Returns:
            True if weapon fired successfully, False otherwise
        """
        # Store previous state
        self.previous_target_hull = self.target.hull_integrity

        # Get weapon system
        weapons = self.attacker.get_system("weapons")
        if not weapons or not weapons.active:
            return False

        # Check targeting
        if not weapons.can_target(
            self.target.position, self.attacker.position, self.attacker.orientation
        ):
            return False

        # Calculate distance for damage calculation
        distance = self.attacker.position.distance_to(self.target.position)

        # Calculate and apply damage
        self.damage_dealt = weapons.calculate_damage(
            self.weapon_type, distance, self.target
        )
        self.target.take_damage(self.damage_dealt)

        # Fire weapon (consumes ammo if torpedo)
        weapons.fire_weapon(self.weapon_type)

        return True

    def _do_undo(self) -> bool:
        """
        Restore target's previous state.

        Note: Undo for combat is limited in scope.
        This restores hull but not shield state for simplicity.

        Returns:
            True if undo was successful, False otherwise
        """
        # Restore hull integrity
        self.target.hull_integrity = self.previous_target_hull
        self.target.active = True  # Revive if was destroyed

        # Restore ammo if torpedo was fired
        if self.weapon_type == "torpedo":
            weapons = self.attacker.get_system("weapons")
            if weapons:
                weapons.torpedo_count += 1

        return True


class CommandHistory:
    """
    Manages command history for undo/redo functionality.

    Maintains separate stacks for executed commands and undone commands
    to support full undo/redo capability.

    Attributes:
        command_stack: Stack of executed commands
        redo_stack: Stack of undone commands
        max_history: Maximum history size

    Public methods:
        execute: Execute and record command
        undo: Undo last command
        redo: Redo last undone command
        clear: Clear all history
        can_undo: Check if undo is possible
        can_redo: Check if redo is possible

    Private methods:
        _trim_history: Trim history to max size
    """

    def __init__(self, max_history: int = 100):
        """
        Initialize command history.

        Args:
            max_history: Maximum number of commands to keep in history
        """
        self.command_stack: list[Command] = []
        self.redo_stack: list[Command] = []
        self.max_history = max_history
        logger.debug("Command history initialized with max size %d", max_history)

    def execute(self, command: Command) -> bool:
        """
        Execute and record command.

        Args:
            command: Command to execute

        Returns:
            True if command executed successfully, False otherwise
        """
        # Execute the command
        if not command.execute():
            return False

        # Add to history
        self.command_stack.append(command)
        self.redo_stack.clear()  # Clear redo stack after new command

        # Trim history if needed
        self._trim_history()

        logger.debug("Command executed and added to history: %s", command.description)
        return True

    def undo(self) -> bool:
        """
        Undo last command.

        Returns:
            True if undo was successful, False otherwise
        """
        if not self.can_undo():
            return False

        # Pop command from stack
        command = self.command_stack.pop()

        # Undo the command
        if command.undo():
            self.redo_stack.append(command)
            logger.debug("Command undone: %s", command.description)
            return True

        # If undo failed, put command back
        self.command_stack.append(command)
        return False

    def redo(self) -> bool:
        """
        Redo last undone command.

        Returns:
            True if redo was successful, False otherwise
        """
        if not self.can_redo():
            return False

        # Pop command from redo stack
        command = self.redo_stack.pop()

        # Re-execute the command
        if command.execute():
            self.command_stack.append(command)
            logger.debug("Command redone: %s", command.description)
            return True

        # If redo failed, put command back
        self.redo_stack.append(command)
        return False

    def clear(self) -> None:
        """Clear all history."""
        self.command_stack.clear()
        self.redo_stack.clear()
        logger.debug("Command history cleared")

    def can_undo(self) -> bool:
        """
        Check if undo is possible.

        Returns:
            True if there are commands to undo, False otherwise
        """
        return len(self.command_stack) > 0

    def can_redo(self) -> bool:
        """
        Check if redo is possible.

        Returns:
            True if there are commands to redo, False otherwise
        """
        return len(self.redo_stack) > 0

    def _trim_history(self) -> None:
        """Trim history to max size."""
        while len(self.command_stack) > self.max_history:
            self.command_stack.pop(0)
            logger.debug("Trimmed oldest command from history")
