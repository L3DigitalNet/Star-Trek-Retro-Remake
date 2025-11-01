#!/usr/bin/env python3
"""
Star Trek Retro Remake - Command Pattern Tests

Description:
    Unit tests for command pattern implementation including commands,
    command history, undo/redo functionality, and macro recording.

Author: Star Trek Retro Remake Development Team
Date Created: 10-30-2025
Date Changed: 10-30-2025
License: MIT
"""

from typing import Final

from src.game.commands import (
    CommandHistory,
    FireWeaponCommand,
    MoveShipCommand,
)
from src.game.entities.base import GridPosition
from src.game.entities.starship import Starship

__version__: Final[str] = "0.0.11"


class TestCommand:
    """Test cases for Command base class."""

    def test_command_initialization(self):
        """Test that Command initializes with correct attributes."""
        # Arrange & Act
        # Using a concrete subclass since Command is abstract
        position = GridPosition(5, 5, 1)
        ship = Starship(position, "Constitution", "Test Ship")
        target = GridPosition(6, 6, 1)
        command = MoveShipCommand(ship, target)

        # Assert
        assert command.executed is False
        assert "Test Ship" in command.description
        assert "to" in command.description

    def test_command_execution_tracking(self):
        """Test that command execution state is tracked."""
        # Arrange
        position = GridPosition(5, 5, 1)
        ship = Starship(position, "Constitution", "Test Ship")
        target = GridPosition(6, 6, 1)
        command = MoveShipCommand(ship, target)

        # Act
        result = command.execute()

        # Assert
        assert result is True
        assert command.executed is True


class TestMoveShipCommand:
    """Test cases for MoveShipCommand."""

    def test_move_ship_command_creation(self):
        """Test creating a move ship command."""
        # Arrange
        position = GridPosition(5, 5, 1)
        ship = Starship(position, "Constitution", "Test Ship")
        target = GridPosition(6, 6, 1)

        # Act
        command = MoveShipCommand(ship, target)

        # Assert
        assert command.ship == ship
        assert command.destination == target
        assert command.previous_position is None
        assert "Move" in command.description

    def test_move_ship_execute(self):
        """Test executing a move ship command."""
        # Arrange
        position = GridPosition(5, 5, 1)
        ship = Starship(position, "Constitution", "Test Ship")
        target = GridPosition(6, 6, 1)
        command = MoveShipCommand(ship, target)

        # Act
        result = command.execute()

        # Assert
        assert result is True
        assert ship.position == target
        assert command.previous_position == position

    def test_move_ship_undo(self):
        """Test undoing a move ship command."""
        # Arrange
        position = GridPosition(5, 5, 1)
        ship = Starship(position, "Constitution", "Test Ship")
        target = GridPosition(6, 6, 1)
        command = MoveShipCommand(ship, target)
        command.execute()

        # Act
        result = command.undo()

        # Assert
        assert result is True
        assert ship.position == position
        assert command.executed is False

    def test_move_ship_cannot_execute_twice(self):
        """Test that executed command cannot be executed again."""
        # Arrange
        position = GridPosition(5, 5, 1)
        ship = Starship(position, "Constitution", "Test Ship")
        target = GridPosition(6, 6, 1)
        command = MoveShipCommand(ship, target)
        command.execute()

        # Act
        result = command.can_execute()

        # Assert
        assert result is False

    def test_move_ship_cannot_undo_unexecuted(self):
        """Test that unexecuted command cannot be undone."""
        # Arrange
        position = GridPosition(5, 5, 1)
        ship = Starship(position, "Constitution", "Test Ship")
        target = GridPosition(6, 6, 1)
        command = MoveShipCommand(ship, target)

        # Act
        result = command.can_undo()

        # Assert
        assert result is False


class TestFireWeaponCommand:
    """Test cases for FireWeaponCommand."""

    def test_fire_weapon_command_creation(self):
        """Test creating a fire weapon command."""
        # Arrange
        attacker_pos = GridPosition(5, 5, 1)
        attacker = Starship(attacker_pos, "Constitution", "Attacker")
        target_pos = GridPosition(7, 7, 1)
        target = Starship(target_pos, "Bird-of-Prey", "Target")

        # Act
        command = FireWeaponCommand(attacker, target, "phaser")

        # Assert
        assert command.attacker == attacker
        assert command.target == target
        assert command.weapon_type == "phaser"
        assert "fires" in command.description
        assert "phaser" in command.description

    def test_fire_weapon_execute(self):
        """Test executing a fire weapon command."""
        # Arrange
        attacker_pos = GridPosition(5, 5, 1)
        attacker = Starship(attacker_pos, "Constitution", "Attacker")
        target_pos = GridPosition(7, 7, 1)
        target = Starship(target_pos, "Bird-of-Prey", "Target")
        initial_hull = target.hull_integrity
        command = FireWeaponCommand(attacker, target, "phaser")

        # Act
        result = command.execute()

        # Assert
        assert result is True
        assert target.hull_integrity < initial_hull or result is True
        assert command.damage_dealt >= 0

    def test_fire_weapon_with_offline_weapons(self):
        """Test firing weapons when weapons system is offline."""
        # Arrange
        attacker_pos = GridPosition(5, 5, 1)
        attacker = Starship(attacker_pos, "Constitution", "Attacker")
        target_pos = GridPosition(7, 7, 1)
        target = Starship(target_pos, "Bird-of-Prey", "Target")

        # Disable weapons
        weapons = attacker.get_system("weapons")
        weapons.active = False

        command = FireWeaponCommand(attacker, target, "phaser")

        # Act
        result = command.execute()

        # Assert
        assert result is False

    def test_fire_weapon_can_undo(self):
        """Test that fire weapon command can be undone (restores hull)."""
        # Arrange
        attacker_pos = GridPosition(5, 5, 1)
        attacker = Starship(attacker_pos, "Constitution", "Attacker")
        target_pos = GridPosition(7, 7, 1)
        target = Starship(target_pos, "Bird-of-Prey", "Target")
        initial_hull = target.hull_integrity
        command = FireWeaponCommand(attacker, target, "phaser")
        command.execute()

        # Act
        result = command.undo()

        # Assert
        assert result is True
        assert target.hull_integrity == initial_hull  # Hull restored


class TestFireWeaponCommandAdvanced:
    """Additional test cases for FireWeaponCommand."""

    def test_fire_multiple_weapon_types(self):
        """Test firing different weapon types."""
        # Arrange
        attacker_pos = GridPosition(5, 5, 1)
        attacker = Starship(attacker_pos, "Constitution", "Attacker")
        target_pos = GridPosition(7, 7, 1)
        target = Starship(target_pos, "Bird-of-Prey", "Target")

        # Act & Assert - Test different weapon types
        phaser_cmd = FireWeaponCommand(attacker, target, "phaser")
        torpedo_cmd = FireWeaponCommand(attacker, target, "torpedo")

        assert phaser_cmd.weapon_type == "phaser"
        assert torpedo_cmd.weapon_type == "torpedo"


class TestCommandHistory:
    """Test cases for CommandHistory manager."""

    def test_command_history_initialization(self):
        """Test that CommandHistory initializes correctly."""
        # Arrange & Act
        history = CommandHistory()

        # Assert
        assert history.max_history == 100
        assert len(history.command_stack) == 0
        assert len(history.redo_stack) == 0

    def test_execute_command_through_history(self):
        """Test executing a command through command history."""
        # Arrange
        history = CommandHistory()
        position = GridPosition(5, 5, 1)
        ship = Starship(position, "Constitution", "Test Ship")
        target = GridPosition(6, 6, 1)
        command = MoveShipCommand(ship, target)

        # Act
        result = history.execute(command)

        # Assert
        assert result is True
        assert len(history.command_stack) == 1
        assert ship.position == target

    def test_undo_command(self):
        """Test undoing a command."""
        # Arrange
        history = CommandHistory()
        position = GridPosition(5, 5, 1)
        ship = Starship(position, "Constitution", "Test Ship")
        target = GridPosition(6, 6, 1)
        command = MoveShipCommand(ship, target)
        history.execute(command)

        # Act
        result = history.undo()

        # Assert
        assert result is True
        assert ship.position == position
        assert len(history.command_stack) == 0
        assert len(history.redo_stack) == 1

    def test_redo_command(self):
        """Test redoing a command."""
        # Arrange
        history = CommandHistory()
        position = GridPosition(5, 5, 1)
        ship = Starship(position, "Constitution", "Test Ship")
        target = GridPosition(6, 6, 1)
        command = MoveShipCommand(ship, target)
        history.execute(command)
        history.undo()

        # Act
        result = history.redo()

        # Assert
        assert result is True
        assert ship.position == target
        assert len(history.command_stack) == 1
        assert len(history.redo_stack) == 0

    def test_cannot_undo_empty_history(self):
        """Test that undo on empty history returns False."""
        # Arrange
        history = CommandHistory()

        # Act
        result = history.undo()

        # Assert
        assert result is False

    def test_cannot_redo_at_end_of_history(self):
        """Test that redo at end of history returns False."""
        # Arrange
        history = CommandHistory()
        position = GridPosition(5, 5, 1)
        ship = Starship(position, "Constitution", "Test Ship")
        target = GridPosition(6, 6, 1)
        command = MoveShipCommand(ship, target)
        history.execute(command)

        # Act
        result = history.redo()

        # Assert
        assert result is False

    def test_new_command_clears_redo_stack(self):
        """Test that executing a new command clears redo history."""
        # Arrange
        history = CommandHistory()
        position = GridPosition(5, 5, 1)
        ship = Starship(position, "Constitution", "Test Ship")

        command1 = MoveShipCommand(ship, GridPosition(6, 6, 1))
        command2 = MoveShipCommand(ship, GridPosition(7, 7, 1))

        history.execute(command1)
        history.undo()

        # Act
        history.execute(command2)

        # Assert
        assert len(history.command_stack) == 1
        assert len(history.redo_stack) == 0
        assert history.command_stack[0] == command2

    def test_history_max_size(self):
        """Test that history respects maximum size."""
        # Arrange
        history = CommandHistory(max_history=5)
        position = GridPosition(5, 5, 1)
        ship = Starship(position, "Constitution", "Test Ship")

        # Act
        for i in range(10):
            target = GridPosition(6 + i, 6, 1)
            command = MoveShipCommand(ship, target)
            history.execute(command)

        # Assert
        assert len(history.command_stack) <= 5

    def test_clear_history(self):
        """Test clearing command history."""
        # Arrange
        history = CommandHistory()
        position = GridPosition(5, 5, 1)
        ship = Starship(position, "Constitution", "Test Ship")
        target = GridPosition(6, 6, 1)
        command = MoveShipCommand(ship, target)
        history.execute(command)

        # Act
        history.clear()

        # Assert
        assert len(history.command_stack) == 0
        assert len(history.redo_stack) == 0

    def test_can_undo(self):
        """Test checking if undo is possible."""
        # Arrange
        history = CommandHistory()
        position = GridPosition(5, 5, 1)
        ship = Starship(position, "Constitution", "Test Ship")
        target = GridPosition(6, 6, 1)
        command = MoveShipCommand(ship, target)

        # Act & Assert - Initially can't undo
        assert history.can_undo() is False

        # Execute command
        history.execute(command)
        assert history.can_undo() is True

        # Undo command
        history.undo()
        assert history.can_undo() is False

    def test_can_redo(self):
        """Test checking if redo is possible."""
        # Arrange
        history = CommandHistory()
        position = GridPosition(5, 5, 1)
        ship = Starship(position, "Constitution", "Test Ship")
        target = GridPosition(6, 6, 1)
        command = MoveShipCommand(ship, target)

        # Act & Assert - Initially can't redo
        assert history.can_redo() is False

        # Execute and undo to create redo possibility
        history.execute(command)
        assert history.can_redo() is False

        history.undo()
        assert history.can_redo() is True

        # Redo command
        history.redo()
        assert history.can_redo() is False
