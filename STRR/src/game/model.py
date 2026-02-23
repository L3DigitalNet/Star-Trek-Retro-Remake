#!/usr/bin/env python3
"""
Star Trek Retro Remake - Game Model

Description:
    Pure game logic and state management implementing the Model component of the
    MVC pattern. Contains no UI dependencies and can be tested independently.

Author: Star Trek Retro Remake Development Team
Email: development@star-trek-retro-remake.org
GitHub: https://github.com/L3DigitalNet/Star-Trek-Retro-Remake
Date Created: 10-29-2025
Date Changed: 02-19-2026 (v0.0.32 - Call CrewManager.on_turn_advanced() from end_current_turn())
License: MIT

Features:
    - Pure game logic with no UI dependencies
    - Galaxy and sector map management
    - Turn-based game mechanics with action points
    - Advanced combat system with weapons and shields
    - Line of sight and firing arc calculations
    - Directional shield system with facings
    - Critical hit system and range modifiers
    - Starship and entity management
    - Mission and event systems
    - Save/load game state functionality

Requirements:
    - Linux environment
    - Python 3.14+ for latest language features

Classes:
    - GameModel: Core game state and logic management
    - TurnManager: Turn-based gameplay coordination
    - CombatResult: Combat action result data

Functions:
    - None
"""

import random
from dataclasses import dataclass
from pathlib import Path
from typing import Final, TypedDict, cast

from ..engine.config_loader import get_combat_config
from .components.mission_manager import MissionManager
from .entities.base import GameObject, GridPosition
from .entities.starship import Starship
from .maps.galaxy import GalaxyMap
from .maps.sector import SectorMap

__version__: Final[str] = "0.0.32"


class TurnStatus(TypedDict):
    """Typed return value for GameModel.get_turn_status().

    Keys returned by get_turn_info() plus action_points fields added
    by get_turn_status(). Controller unpacks these into update_turn_info().
    """

    turn_number: int
    current_phase: str
    active_entity: str
    entities_remaining: int
    action_points: int
    max_action_points: int


@dataclass
class CombatResult:
    """
    Results of a combat action.

    Attributes:
        success: Whether the combat action succeeded
        message: Descriptive message about the result
        damage: Amount of damage dealt (if applicable)
    """

    success: bool
    message: str
    damage: int = 0


class TurnManager:
    """
    Manages turn-based gameplay mechanics.

    Implements initiative-based turn ordering where entities with higher
    initiative act first. Handles action point restoration and turn phases.

    Attributes:
        turn_number: Current turn number
        current_phase: Current phase of the turn (input, action, resolution)
        active_entities: List of entities participating in combat/turns
        turn_order: Initiative-sorted list of entities
        current_entity_index: Index of entity currently acting
        action_history: Record of actions taken this turn

    Public methods:
        advance_turn: Advance to the next turn
        get_turn_info: Get current turn information
        register_entity: Add entity to turn tracking
        unregister_entity: Remove entity from turn tracking
        get_current_entity: Get entity whose turn it is
        next_entity: Advance to next entity in turn order
        start_turn_phase: Begin a new turn phase
        end_turn_phase: Complete current turn phase

    Private methods:
        _process_ai_turns: Process AI entity turns
        _sort_by_initiative: Sort entities by initiative
        _restore_action_points: Restore all entities' action points
    """

    def __init__(self) -> None:
        """Initialize the turn manager."""
        self.turn_number: int = 0
        self.current_phase: str = "input"  # input, action, resolution

        # Entity tracking for turn-based combat
        self.active_entities: list[GameObject] = []
        self.turn_order: list[GameObject] = []
        self.current_entity_index: int = 0

        # Action tracking
        self.action_history: list[dict[str, str | int]] = []

    def advance_turn(self) -> None:
        """Advance to the next turn and reset entity states."""
        self.turn_number += 1
        self.current_entity_index = 0
        self.action_history.clear()

        # Restore action points for all entities
        self._restore_action_points()

        # Recalculate turn order based on initiative
        self._sort_by_initiative()

        # Start with input phase
        self.current_phase = "input"

        # Process AI entity turns
        self._process_ai_turns()

    def get_turn_info(self) -> dict[str, int | str]:
        """
        Get current turn information.

        Returns:
            Dictionary with turn number, phase, and active entity
        """
        current_entity = self.get_current_entity()
        return {
            "turn_number": self.turn_number,
            "current_phase": self.current_phase,
            "active_entity": current_entity.name if current_entity else "None",
            "entities_remaining": len(self.turn_order) - self.current_entity_index,
        }

    def register_entity(self, entity: GameObject) -> None:
        """
        Add entity to turn tracking.

        Args:
            entity: Game object to track for turns
        """
        if entity not in self.active_entities and entity.active:
            self.active_entities.append(entity)
            self._sort_by_initiative()

    def unregister_entity(self, entity: GameObject) -> None:
        """
        Remove entity from turn tracking.

        Args:
            entity: Game object to remove from tracking
        """
        if entity in self.active_entities:
            self.active_entities.remove(entity)
            self._sort_by_initiative()

    def get_current_entity(self) -> GameObject | None:
        """
        Get entity whose turn it is.

        Returns:
            Currently active entity or None if no entities
        """
        if 0 <= self.current_entity_index < len(self.turn_order):
            return self.turn_order[self.current_entity_index]
        return None

    def next_entity(self) -> GameObject | None:
        """
        Advance to next entity in turn order.

        Returns:
            Next entity in turn order or None if turn complete
        """
        self.current_entity_index += 1
        if self.current_entity_index >= len(self.turn_order):
            # All entities have acted, advance turn
            self.advance_turn()
            return None
        return self.get_current_entity()

    def start_turn_phase(self, phase: str) -> None:
        """
        Begin a new turn phase.

        Args:
            phase: Phase name (input, action, resolution)
        """
        self.current_phase = phase

    def end_turn_phase(self) -> None:
        """Complete current turn phase and advance to next."""
        phase_order = ["input", "action", "resolution"]
        current_index = phase_order.index(self.current_phase)

        if current_index < len(phase_order) - 1:
            self.current_phase = phase_order[current_index + 1]
        else:
            # Completed all phases, advance to next entity or turn
            self.next_entity()

    def _process_ai_turns(self) -> None:
        """Process AI entity turns and actions."""
        from .entities.starship import Starship

        # Get current entity
        current_entity = (
            self.turn_order[self.current_entity_index] if self.turn_order else None
        )

        if current_entity and isinstance(current_entity, Starship):
            # Check if entity has AI controller
            if current_entity.ai_controller and not current_entity.is_player:
                # Let AI make decisions and act
                # AI will use action points and may end turn early
                pass  # AI updates are called from GameModel now

    def _sort_by_initiative(self) -> None:
        """Sort active entities by initiative (highest first)."""
        self.turn_order = sorted(
            [e for e in self.active_entities if e.active],
            key=lambda entity: entity.initiative,
            reverse=True,  # Higher initiative acts first
        )

    def _restore_action_points(self) -> None:
        """Restore action points for all active entities."""
        for entity in self.active_entities:
            if entity.active:
                entity.reset_action_points()


class GameModel:
    """
    Pure game logic and state management.

    Contains all game state and business logic without any UI dependencies.
    Can be tested independently of the UI components.

    Attributes:
        galaxy: Galaxy map containing all sectors
        current_sector: Currently active sector map
        player_ship: Player's starship entity
        turn_manager: Turn-based gameplay manager
        game_objects: List of all active game objects
        active_missions: List of current active missions

    Public methods:
        initialize_new_game: Set up a new game
        execute_move: Execute starship movement
        resolve_combat: Resolve combat between entities
        save_game: Save current game state
        load_game: Load saved game state

    Private methods:
        _is_valid_move: Validate movement request
        _create_player_ship: Create the player's starting ship
    """

    def __init__(self) -> None:
        """Initialize the game model with default state."""
        # Map system
        self.galaxy = GalaxyMap()
        # Will be initialized in initialize_new_game() - guaranteed to exist during gameplay
        self.current_sector: SectorMap

        # Player and entities - initialized in initialize_new_game()
        self.player_ship: Starship
        self.game_objects: list[GameObject] = []

        # Game systems
        self.turn_manager = TurnManager()

        # Mission system - initialize with mission templates path
        mission_path = (
            Path(__file__).parent.parent.parent
            / "assets"
            / "data"
            / "mission_templates.toml"
        )
        self.mission_manager = MissionManager(mission_path)

    def initialize_new_game(self) -> None:
        """Set up a new game with default starting conditions."""
        # Load starting sector - confident initialization ensures it exists
        sector = self.galaxy.get_sector(0, 0)
        if sector is None:
            raise RuntimeError(
                "Critical error: Starting sector (0, 0) does not exist in galaxy"
            )
        self.current_sector = sector

        # Create player ship at starting position
        start_position = GridPosition(5, 5, 1)
        self.player_ship = self._create_player_ship(start_position)

        # Set player ship initiative and action points
        self.player_ship.initiative = 10  # Player acts first
        self.player_ship.max_action_points = 5  # Player gets more actions
        self.player_ship.reset_action_points()

        # Add player ship to game objects
        self.game_objects.append(self.player_ship)

        # Register ship in sector entities dictionary
        if not self.current_sector.place_entity(self.player_ship, start_position):
            raise RuntimeError(f"Failed to place player ship at {start_position}")

        # Register player ship with turn manager
        self.turn_manager.register_entity(self.player_ship)

        # Add test ships for milestone demonstration
        self._add_test_ships()

        # Initialize AI for NPC ships
        self._initialize_ai()

        # Start first turn
        self.turn_manager.advance_turn()

    def execute_move(self, ship: Starship, destination: GridPosition) -> bool:
        """
        Execute ship movement if valid.

        Args:
            ship: The starship to move
            destination: Target position for movement

        Returns:
            True if movement was successful, False otherwise
        """
        # Calculate movement cost in action points (1 AP per grid cell)
        distance = int(ship.position.distance_to(destination))
        action_cost = max(1, distance)  # Minimum 1 AP per move

        # Check if ship has enough action points
        if not ship.has_action_points(action_cost):
            return False

        # Validate movement
        if not self._is_valid_move(ship, destination):
            return False

        # Get engine system and validate it exists
        from .components.ship_systems import (
            EngineSystems,
        )  # local runtime import for isinstance narrowing

        engines = ship.get_system("engines")
        if not engines or not isinstance(engines, EngineSystems):
            return False

        # Calculate fuel cost
        fuel_cost = engines.calculate_movement_cost(distance)

        # Check fuel availability
        if engines.fuel < fuel_cost:
            return False

        # Store old position for rollback if needed
        old_position = ship.position

        # Update ship position BEFORE moving in sector map
        # This ensures ship.position and sector.entities stay synchronized
        ship.position = destination

        # Move entity in sector map (updates entities dictionary)
        if not self.current_sector.move_entity(old_position, destination):
            # Rollback ship position if sector move failed
            ship.position = old_position
            return False

        # Deduct resources
        engines.fuel -= fuel_cost
        ship.spend_action_points(action_cost)

        # Check if ship has actions remaining, otherwise end turn
        if ship.action_points <= 0:
            self.turn_manager.next_entity()

        # Cleanup inactive objects after action
        self._cleanup_inactive_objects()

        return True

    def resolve_combat(
        self, attacker: Starship, target: Starship, weapon_type: str
    ) -> CombatResult:
        """
        Resolve combat between two starships.

        Args:
            attacker: The attacking starship
            target: The target starship
            weapon_type: Type of weapon being used (phaser or torpedo)

        Returns:
            CombatResult containing the outcome
        """
        # Get attacker's weapon system
        from .components.ship_systems import (
            WeaponSystems,
        )  # local runtime import for isinstance narrowing

        weapons = attacker.get_system("weapons")
        if not weapons or not weapons.active or not isinstance(weapons, WeaponSystems):
            return CombatResult(False, "Weapons offline", 0)

        # Check action points
        action_cost = 2 if weapon_type == "torpedo" else 1
        if not attacker.has_action_points(action_cost):
            return CombatResult(False, "Insufficient action points", 0)

        # Check targeting capability (range and arc)
        if not weapons.can_target(
            target.position, attacker.position, attacker.orientation, weapon_type
        ):
            return CombatResult(False, "Target out of range or arc", 0)

        # Check line of sight
        obstacles = [
            obj
            for obj in self.game_objects
            if obj != attacker and obj != target and obj.active
        ]
        if not weapons.check_line_of_sight(
            attacker.position, target.position, obstacles
        ):
            return CombatResult(False, "Line of sight blocked", 0)

        # Fire weapon
        if not weapons.fire_weapon(weapon_type):
            return CombatResult(False, f"Unable to fire {weapon_type}", 0)

        # Calculate hit chance
        distance = attacker.position.distance_to(target.position)
        hit_chance = weapons.get_hit_chance(distance, weapon_type)

        # Roll for hit
        roll = random.random()
        if roll > hit_chance:
            # Miss
            attacker.spend_action_points(action_cost)
            return CombatResult(False, f"{weapon_type.capitalize()} missed target", 0)

        # Calculate damage
        damage = weapons.calculate_damage(weapon_type, distance, target)

        # Load combat config for critical hits
        config = get_combat_config()
        crit_chance = cast(float, config.get("critical_hit_chance") or 0.1)
        crit_multiplier = cast(float, config.get("critical_hit_multiplier") or 1.5)

        # Check for critical hit (from config)
        is_critical = random.random() < crit_chance
        if is_critical:
            damage = int(damage * crit_multiplier)

        # Apply damage to target
        damage_type = "energy" if weapon_type == "phaser" else "kinetic"
        damage_result = target.take_damage(damage, damage_type, attacker.position)

        # Deduct action points
        attacker.spend_action_points(action_cost)

        # Check if attacker's turn is over
        if attacker.action_points <= 0:
            self.turn_manager.next_entity()

        # Build result message
        crit_text = " (CRITICAL HIT)" if is_critical else ""
        shield_text = (
            f" (shields absorbed {damage_result['shields_absorbed']})"
            if int(damage_result["shields_absorbed"]) > 0
            else ""
        )
        hull_text = (
            f" hull damage: {damage_result['hull_damage']}"
            if int(damage_result["hull_damage"]) > 0
            else ""
        )
        facing_text = (
            f" {damage_result['facing_hit']} shields"
            if damage_result["facing_hit"] != "unknown"
            else ""
        )

        message = f"{weapon_type.capitalize()} hit{crit_text}!{facing_text}{shield_text}{hull_text}"

        return CombatResult(True, message, damage)

    def get_potential_targets(
        self, attacker: Starship, weapon_type: str = "phaser"
    ) -> list[Starship]:
        """
        Get list of valid targets for a ship.

        Args:
            attacker: Ship looking for targets
            weapon_type: Type of weapon to consider for range

        Returns:
            List of targetable enemy ships
        """
        from .components.ship_systems import (
            WeaponSystems,
        )  # local runtime import for isinstance narrowing

        weapons = attacker.get_system("weapons")
        if not weapons or not weapons.active or not isinstance(weapons, WeaponSystems):
            return []

        targets: list[Starship] = []

        # Find all enemy ships in range
        for obj in self.game_objects:
            if isinstance(obj, Starship) and obj.active and obj != attacker:
                # Check if different faction (enemy)
                if obj.faction != attacker.faction:
                    # Check if in range and arc
                    if weapons.can_target(
                        obj.position,
                        attacker.position,
                        attacker.orientation,
                        weapon_type,
                    ):
                        targets.append(obj)

        return targets

    def save_game(self, filepath: str) -> bool:
        """
        Save current game state to file.

        Args:
            filepath: Path to save the game file

        Returns:
            True if save was successful, False otherwise
        """
        # Save functionality will be implemented here
        return True

    def load_game(self, filepath: str) -> bool:
        """
        Load saved game state from file.

        Args:
            filepath: Path to the saved game file

        Returns:
            True if load was successful, False otherwise
        """
        # Load functionality will be implemented here
        return True

    def _is_valid_move(self, ship: Starship, destination: GridPosition) -> bool:
        """
        Check if the requested move is valid.

        Args:
            ship: The starship requesting movement
            destination: Target destination

        Returns:
            True if move is valid, False otherwise
        """
        # Check sector bounds
        if not self.current_sector.is_in_bounds(destination):
            return False

        # Check for obstacles
        if self.current_sector.has_obstacle(destination):
            return False

        return True

    def is_valid_move(self, ship: Starship, destination: GridPosition) -> bool:
        """Check if a move is valid for the given entity.

        Public API for AI controllers. Delegates to internal validation logic.
        Exposed here to avoid coupling AI code to private GameModel internals.
        """
        return self._is_valid_move(ship, destination)

    def _create_player_ship(self, position: GridPosition) -> Starship:
        """
        Create the player's starting starship.

        Args:
            position: Starting position for the ship

        Returns:
            Configured player starship
        """
        return Starship(
            position, "Constitution", "Enterprise", "Federation", is_player=True
        )

    def _add_test_ships(self) -> None:
        """
        Add test starships for milestone demonstration.

        Creates multiple ships at different positions, z-levels, and orientations
        to demonstrate entity rendering with visual differentiation.
        """
        # Test ship configurations: (position, ship_class, name, faction, orientation, initiative)
        test_ships = [
            (
                GridPosition(8, 8, 1),
                "Bird-of-Prey",
                "IKS Korinar",
                "Klingon",
                45,
                8,
            ),
            (GridPosition(12, 6, 2), "Warbird", "IRW Valdore", "Romulan", 135, 7),
            (GridPosition(10, 10, 0), "D7 Cruiser", "IKS Amar", "Klingon", 270, 6),
            (GridPosition(7, 12, 1), "Scout", "USS Reliant", "Federation", 180, 9),
        ]

        # Create and place each test ship
        for position, ship_class, name, faction, orientation, initiative in test_ships:
            ship = Starship(position, ship_class, name, faction)
            ship.orientation = orientation  # Set facing direction
            ship.initiative = initiative  # Set turn order priority
            ship.max_action_points = 3  # NPC ships get 3 actions per turn
            ship.reset_action_points()

            self.game_objects.append(ship)
            self.current_sector.place_entity(ship, position)

            # Register ship with turn manager for combat
            self.turn_manager.register_entity(ship)

    def _initialize_ai(self) -> None:
        """
        Initialize AI controllers for NPC ships.

        Creates and attaches AI controllers to all non-player ships.
        """
        from .ai.ship_ai import ShipAI
        from .entities.starship import Starship

        for obj in self.game_objects:
            if isinstance(obj, Starship) and not obj.is_player:
                # Create and attach AI controller
                ai = ShipAI(obj)
                obj.set_ai_controller(ai)

    def process_ai_turn(self, ship: Starship) -> None:
        """
        Process one turn for an AI-controlled ship.

        Args:
            ship: AI-controlled starship
        """
        if ship.ai_controller:
            ship.ai_controller.update(self)

    def end_current_turn(self) -> None:
        """
        Manually end the current entity's turn.

        Advances to the next entity in turn order or starts a new turn
        if all entities have acted. Also fires per-turn callbacks on the
        player ship's crew system so morale/starbase tracking increments
        exactly once per turn, not once per frame.
        """
        self.turn_manager.next_entity()

        # Fire per-turn crew tick on the player ship. Local runtime import
        # required — TYPE_CHECKING-only imports are erased at runtime and
        # isinstance() against them raises NameError (see project CLAUDE.md).
        assert hasattr(self, "player_ship"), (
            "end_current_turn() called before initialize_new_game()"
        )
        from .components.ship_systems import CrewManager  # local runtime import

        crew = self.player_ship.get_system("crew")
        if isinstance(crew, CrewManager):
            crew.on_turn_advanced()

    def get_turn_status(self) -> TurnStatus:
        """
        Get current turn status information.

        Returns:
            TurnStatus with turn number, phase, active entity, and action points
        """
        # Build explicit TurnStatus instead of mutating get_turn_info() dict so
        # mypy can verify the return type matches the TypedDict exactly.
        tm = self.turn_manager
        current_entity = tm.get_current_entity()
        action_points: int = current_entity.action_points if current_entity else 0
        max_action_points: int = (
            current_entity.max_action_points if current_entity else 0
        )
        active_entity_name: str = current_entity.name if current_entity else "None"
        return TurnStatus(
            turn_number=tm.turn_number,
            current_phase=tm.current_phase,
            active_entity=active_entity_name,
            entities_remaining=len(tm.turn_order) - tm.current_entity_index,
            action_points=action_points,
            max_action_points=max_action_points,
        )

    def update_missions(self) -> None:
        """Update all active missions and check for completion."""
        self.mission_manager.update_active_missions()

    def _cleanup_inactive_objects(self) -> None:
        """
        Remove destroyed objects from game to prevent memory leaks.

        Filters out all game objects where active=False. All objects in
        game_objects list are guaranteed to be GameObject instances.
        """
        self.game_objects = [obj for obj in self.game_objects if obj.active]
