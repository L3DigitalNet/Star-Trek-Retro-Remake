#!/usr/bin/env python3
"""
Star Trek Retro Remake - Resource Management Tests

Description:
    Unit tests for ResourceManager and CrewManager components.

Author: Star Trek Retro Remake Development Team
Email: development@star-trek-retro-remake.org
GitHub: https://github.com/L3DigitalNet/Star-Trek-Retro-Remake
Date Created: 10-31-2025
Date Changed: 10-31-2025
License: MIT

Features:
    - Test energy allocation and consumption
    - Test fuel management
    - Test supplies tracking
    - Test crew morale and efficiency
    - Test starbase services
    - Edge case testing (zero energy, full supplies, etc.)

Requirements:
    - Linux environment
    - Python 3.14+ for latest language features
    - pytest 8.0+ for testing framework
"""

import pytest
from src.game.components.ship_systems import CrewManager, ResourceManager
from src.game.entities.base import GridPosition
from src.game.entities.starship import Starship

pytestmark = pytest.mark.unit

__version__ = "0.0.22"


class TestResourceManager:
    """Test suite for ResourceManager component."""

    def test_resource_manager_initialization(self):
        """Test ResourceManager initializes with correct defaults."""
        resources = ResourceManager()

        assert resources.energy_current == resources.energy_capacity
        assert resources.fuel_current == resources.fuel_capacity
        assert resources.energy_capacity > 0
        assert resources.fuel_capacity > 0
        assert "medical" in resources.supplies
        assert "spare_parts" in resources.supplies

    def test_energy_consumption(self):
        """Test energy consumption for actions."""
        resources = ResourceManager()
        initial_energy = resources.energy_current

        # Consume energy for move action
        success = resources.consume_energy("move")
        assert success is True
        assert resources.energy_current < initial_energy

    def test_insufficient_energy(self):
        """Test action fails when insufficient energy."""
        resources = ResourceManager()
        resources.energy_current = 5.0  # Very low energy

        # Try expensive action
        success = resources.consume_energy("fire_torpedo")
        assert success is False
        assert resources.energy_current == 5.0  # Energy unchanged

    def test_energy_regeneration(self):
        """Test energy regenerates over time."""
        resources = ResourceManager()
        resources.energy_current = 500.0  # Half capacity

        # Regenerate energy
        resources.regenerate_energy(1.0)  # 1 second
        assert resources.energy_current > 500.0
        assert resources.energy_current <= resources.energy_capacity

    def test_power_distribution(self):
        """Test power allocation to ship systems."""
        resources = ResourceManager()

        # Allocate power to shields
        success = resources.allocate_power("shields", 50.0)
        assert success is True
        assert resources.get_system_power("shields") == 50.0

    def test_invalid_power_allocation(self):
        """Test invalid power allocation fails."""
        resources = ResourceManager()

        # Try invalid system
        success = resources.allocate_power("invalid_system", 50.0)
        assert success is False

        # Try invalid percentage
        success = resources.allocate_power("shields", 150.0)
        assert success is False

    def test_fuel_consumption(self):
        """Test fuel consumption."""
        resources = ResourceManager()
        initial_fuel = resources.fuel_current

        # Consume fuel
        success = resources.consume_fuel()
        assert success is True
        assert resources.fuel_current < initial_fuel

    def test_insufficient_fuel(self):
        """Test action fails when insufficient fuel."""
        resources = ResourceManager()
        resources.fuel_current = 1.0  # Very low fuel

        # Try to consume more than available
        success = resources.consume_fuel(10.0)
        assert success is False
        assert resources.fuel_current == 1.0  # Fuel unchanged

    def test_refuel(self):
        """Test refueling ship."""
        resources = ResourceManager()
        resources.fuel_current = 100.0  # Low fuel

        # Refuel
        resources.refuel(200.0)
        assert resources.fuel_current == 300.0
        assert resources.fuel_current <= resources.fuel_capacity

    def test_supplies_usage(self):
        """Test using supplies."""
        resources = ResourceManager()
        initial_parts = resources.supplies["spare_parts"]

        # Use spare parts
        success = resources.use_supplies("spare_parts", 10)
        assert success is True
        assert resources.supplies["spare_parts"] == initial_parts - 10

    def test_insufficient_supplies(self):
        """Test action fails when insufficient supplies."""
        resources = ResourceManager()
        resources.supplies["medical"] = 5

        # Try to use more than available
        success = resources.use_supplies("medical", 10)
        assert success is False
        assert resources.supplies["medical"] == 5  # Supplies unchanged

    def test_resupply(self):
        """Test resupplying."""
        resources = ResourceManager()
        resources.supplies["medical"] = 50

        # Resupply
        resources.resupply("medical", 25)
        assert resources.supplies["medical"] == 75

    def test_has_energy(self):
        """Test checking available energy."""
        resources = ResourceManager()
        resources.energy_current = 100.0

        assert resources.has_energy(50.0) is True
        assert resources.has_energy(150.0) is False

    def test_energy_regeneration_with_power_allocation(self):
        """Test energy regen affected by engine power allocation."""
        resources = ResourceManager()
        resources.energy_current = 500.0

        # Set engine power to 50%
        resources.allocate_power("engines", 50.0)
        resources.regenerate_energy(1.0)
        energy_50 = resources.energy_current

        # Reset and test with 100% engine power
        resources.energy_current = 500.0
        resources.allocate_power("engines", 100.0)
        resources.regenerate_energy(1.0)
        energy_100 = resources.energy_current

        # Higher engine power should regenerate more energy
        assert energy_100 > energy_50


class TestCrewManager:
    """Test suite for CrewManager component."""

    def test_crew_manager_initialization(self):
        """Test CrewManager initializes with correct defaults."""
        crew = CrewManager()

        assert crew.morale > 0
        assert crew.morale <= 100
        assert len(crew.crew_roster) > 0
        assert crew.turns_since_starbase == 0
        assert crew.casualties == 0

    def test_morale_update(self):
        """Test direct morale updates."""
        crew = CrewManager()
        initial_morale = crew.morale

        # Increase morale
        crew.update_morale(10.0)
        assert crew.morale == initial_morale + 10.0

        # Decrease morale
        crew.update_morale(-5.0)
        assert crew.morale == initial_morale + 5.0

    def test_morale_bounds(self):
        """Test morale stays within 0-100 bounds."""
        crew = CrewManager()

        # Try to exceed maximum
        crew.morale = 95.0
        crew.update_morale(10.0)
        assert crew.morale == 100.0

        # Try to go below minimum
        crew.morale = 5.0
        crew.update_morale(-10.0)
        assert crew.morale == 0.0

    def test_combat_victory(self):
        """Test morale increases after combat victory."""
        crew = CrewManager()
        initial_morale = crew.morale

        crew.record_combat_outcome(victory=True)
        assert crew.morale > initial_morale
        assert crew.combat_victories == 1

    def test_combat_defeat(self):
        """Test morale decreases after combat defeat."""
        crew = CrewManager()
        initial_morale = crew.morale

        crew.record_combat_outcome(victory=False)
        assert crew.morale < initial_morale
        assert crew.combat_defeats == 1

    def test_casualty_impact(self):
        """Test casualties decrease morale."""
        crew = CrewManager()
        initial_morale = crew.morale

        crew.record_casualty()
        assert crew.morale < initial_morale
        assert crew.casualties == 1

    def test_efficiency_multiplier(self):
        """Test efficiency multiplier based on morale."""
        crew = CrewManager()

        # High morale (>80) should give bonus
        crew.morale = 85.0
        efficiency = crew.get_efficiency_multiplier()
        assert efficiency > 1.0

        # Low morale (<40) should give penalty
        crew.morale = 35.0
        efficiency = crew.get_efficiency_multiplier()
        assert efficiency < 1.0

        # Normal morale (60-80) should be neutral
        crew.morale = 70.0
        efficiency = crew.get_efficiency_multiplier()
        assert efficiency == 1.0

    def test_starbase_visit(self):
        """Test starbase visit resets morale and counters."""
        crew = CrewManager()
        crew.morale = 50.0
        crew.turns_since_starbase = 20
        crew.casualties = 5
        crew.combat_victories = 3
        crew.combat_defeats = 2

        initial_morale = crew.morale
        crew.visit_starbase()

        assert crew.morale > initial_morale
        assert crew.turns_since_starbase == 0
        assert crew.casualties == 0
        assert crew.combat_victories == 0
        assert crew.combat_defeats == 0

    def test_crew_assignment(self):
        """Test assigning crew to positions."""
        crew = CrewManager()

        # Assign new crew member
        success = crew.assign_crew("captain", "Jean-Luc Picard")
        assert success is True
        assert crew.crew_roster["captain"] == "Jean-Luc Picard"

        # Try invalid position
        success = crew.assign_crew("invalid_position", "John Doe")
        assert success is False

    def test_morale_degradation_over_time(self):
        """Test morale slowly decreases with turns away from starbase."""
        crew = CrewManager()
        initial_morale = crew.morale

        # Simulate many turns
        for _ in range(15):
            crew.turns_since_starbase += 1
            crew._calculate_morale_modifiers()

        # Morale should have decreased after >10 turns
        assert crew.morale < initial_morale


class TestStarshipResourceIntegration:
    """Test suite for Starship integration with resource systems."""

    def test_starship_has_resources(self):
        """Test Starship initializes with resource systems."""
        ship = Starship(GridPosition(5, 5, 0), "Constitution", "Enterprise")

        assert ship.resources is not None
        assert ship.crew is not None
        assert isinstance(ship.resources, ResourceManager)
        assert isinstance(ship.crew, CrewManager)

    def test_starship_energy_consumption(self):
        """Test Starship can consume energy for actions."""
        ship = Starship(GridPosition(5, 5, 0), "Constitution", "Enterprise")
        initial_energy = ship.resources.energy_current

        success = ship.consume_energy_for_action("move")
        assert success is True
        assert ship.resources.energy_current < initial_energy

    def test_starship_power_allocation(self):
        """Test Starship can allocate power to systems."""
        ship = Starship(GridPosition(5, 5, 0), "Constitution", "Enterprise")

        success = ship.allocate_power("weapons", 40.0)
        assert success is True
        assert ship.resources.get_system_power("weapons") == 40.0

    def test_starship_has_sufficient_energy(self):
        """Test checking if ship has enough energy for action."""
        ship = Starship(GridPosition(5, 5, 0), "Constitution", "Enterprise")
        ship.resources.energy_current = 100.0

        # Should have enough for move
        assert ship.has_sufficient_energy("move") is True

        # Should not have enough for torpedo
        ship.resources.energy_current = 10.0
        assert ship.has_sufficient_energy("fire_torpedo") is False

    def test_starship_refuel_at_starbase(self):
        """Test ship refueling at starbase."""
        ship = Starship(GridPosition(5, 5, 0), "Constitution", "Enterprise")
        ship.resources.fuel_current = 100.0

        ship.refuel_at_starbase()
        assert ship.resources.fuel_current == ship.resources.fuel_capacity

    def test_starship_resupply_at_starbase(self):
        """Test ship resupplying at starbase."""
        ship = Starship(GridPosition(5, 5, 0), "Constitution", "Enterprise")
        ship.resources.supplies["medical"] = 50
        ship.resources.supplies["spare_parts"] = 25
        ship.crew.morale = 50.0

        ship.resupply_at_starbase()

        assert ship.resources.supplies["medical"] == 100
        assert ship.resources.supplies["spare_parts"] == 50
        assert ship.crew.morale > 50.0  # Morale boost

    def test_starship_crew_efficiency(self):
        """Test getting crew efficiency multiplier."""
        ship = Starship(GridPosition(5, 5, 0), "Constitution", "Enterprise")

        ship.crew.morale = 85.0
        efficiency = ship.get_crew_efficiency()
        assert efficiency > 1.0

    def test_starship_record_combat_result(self):
        """Test recording combat results."""
        ship = Starship(GridPosition(5, 5, 0), "Constitution", "Enterprise")
        initial_morale = ship.crew.morale

        ship.record_combat_result(victory=True)
        assert ship.crew.morale > initial_morale
        assert ship.crew.combat_victories == 1

    def test_repair_with_supplies(self):
        """Test ship repair consumes supplies."""
        ship = Starship(GridPosition(5, 5, 0), "Constitution", "Enterprise")

        # Damage a system
        ship.systems["engines"].efficiency = 0.5
        initial_parts = ship.resources.supplies["spare_parts"]

        # Repair system
        success = ship.repair_system("engines", 0.3, use_supplies=True)
        assert success is True
        assert ship.resources.supplies["spare_parts"] < initial_parts

    def test_repair_without_sufficient_supplies(self):
        """Test repair fails without enough supplies."""
        ship = Starship(GridPosition(5, 5, 0), "Constitution", "Enterprise")

        # Damage a system significantly
        ship.systems["engines"].efficiency = 0.1
        ship.resources.supplies["spare_parts"] = 1  # Very low supplies

        # Try to repair (should fail due to insufficient supplies)
        success = ship.repair_system("engines", 0.5, use_supplies=True)
        assert success is False

    def test_repair_affected_by_crew_efficiency(self):
        """Test repair effectiveness affected by crew efficiency."""
        ship = Starship(GridPosition(5, 5, 0), "Constitution", "Enterprise")

        # High morale for better efficiency
        ship.crew.morale = 90.0
        ship.systems["engines"].efficiency = 0.5

        # Repair with high crew efficiency
        ship.repair_system("engines", 0.2, use_supplies=False)
        high_morale_efficiency = ship.systems["engines"].efficiency

        # Reset and test with low morale
        ship.systems["engines"].efficiency = 0.5
        ship.crew.morale = 30.0

        # Repair with low crew efficiency
        ship.repair_system("engines", 0.2, use_supplies=False)
        low_morale_efficiency = ship.systems["engines"].efficiency

        # High morale should result in better repair
        assert high_morale_efficiency > low_morale_efficiency


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
