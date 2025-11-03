---
mode: "agent"
description: "Perform comprehensive testing using Pytest, focusing on unit tests, coverage analysis, and type validation"
---

# Testing Management and Coverage

Handle comprehensive testing of project following repository guidelines and clean architecture principles using Pytest.

## Core Testing Requirements

### Test File Organization - MANDATORY
- **MUST** store ALL test files in each project's `/tests/` directory
- **NEVER** place test files in base project directory
- **INCLUDE** pytest tests, unit tests, example scripts, test configs in `/tests/`
- **MIRROR** source code structure in test directory organization
- **MAINTAIN** clear separation between different test types

### PyTest Standards - REQUIRED
- **MUST** write unit tests for ALL business logic
- **MUST** follow AAA pattern: Arrange, Act, Assert
- **TARGET** 80%+ test coverage for critical paths
- **MUST** use descriptive test names that explain expected behavior
- **MUST** keep tests fast, isolated, and deterministic
- **MUST** ensure tests are discoverable by pytest

## Test Generation Principles

### Unit Test Structure
```python
def test_function_name_should_behavior_when_condition():
    """Test that function_name produces expected behavior under specific condition."""
    # Arrange
    input_data = create_test_data()
    expected_result = define_expected_outcome()

    # Act
    actual_result = function_to_test(input_data)

    # Assert
    assert actual_result == expected_result
```

### Test Categories and Focus
- **Unit Tests**: Test individual functions and methods in isolation
- **Integration Tests**: Test interactions between modules and components
- **Functional Tests**: Test complete workflows and user scenarios
- **Performance Tests**: Test timing and resource usage for critical operations

### Version-Aware Testing Strategy

#### Pre-v1.0.0 Focus (Current Phase)
- **FOCUS** on core functionality testing and business logic validation
- **MINIMIZE** error handling and edge case testing (defer until v1.0.0)
- **PRIORITIZE** happy path testing and expected behavior patterns
- **TEST** clean architecture and confident design patterns
- **VALIDATE** proper initialization sequences and program flow

#### Test Architecture Alignment
- **REFLECT** confident design patterns in test structure
- **AVOID** excessive defensive testing for scenarios that shouldn't occur
- **FOCUS** on testing actual program behavior and constraints
- **VALIDATE** type hints and documented interfaces
- **TEST** clear, linear program flow expectations

## Type Safety and Validation Testing

### Type Hint Verification
- **VERIFY** runtime behavior matches type annotations
- **TEST** that functions accept and return expected types
- **VALIDATE** collection types and their contents
- **CHECK** protocol implementations and interface compliance
- **ENSURE** generic types work correctly with various type parameters

### Contract Testing
- **TEST** public interfaces behave as documented
- **VERIFY** function preconditions and postconditions
- **VALIDATE** class invariants and state consistency
- **CHECK** module boundaries and interaction points

## Game-Specific Testing Patterns

### Turn-Based Mechanics Testing
```python
def test_ship_fires_weapon(starship, enemy_ship):
    """Test weapon firing consumes turn and damages target."""
    # Arrange
    initial_shields = enemy_ship.shields
    initial_turn = game_state.turn_number
    weapon = starship.get_component(WeaponSystem)

    # Act
    weapon.fire(enemy_ship, distance=5)

    # Assert
    assert enemy_ship.shields < initial_shields  # Damage applied
    assert game_state.turn_number == initial_turn + 1  # Turn consumed
```

### 3D Grid System Testing
```python
def test_3d_distance_calculation(grid):
    """Test 3D distance between two positions."""
    # Arrange
    pos1 = (0, 0, 0)  # Origin
    pos2 = (3, 4, 0)  # Same z-level

    # Act
    distance = grid.calculate_distance_3d(pos1, pos2)

    # Assert
    assert distance == 5.0  # Pythagorean theorem: 3² + 4² = 5²
```

### State Machine Testing
```python
def test_state_transition_galaxy_to_sector(state_machine):
    """Test valid state transition."""
    # Arrange
    state_machine.current_state = GameState.GALAXY_MAP

    # Act
    state_machine.transition_to(GameState.SECTOR_MAP)

    # Assert
    assert state_machine.current_state == GameState.SECTOR_MAP
    assert state_machine.previous_state == GameState.GALAXY_MAP
```

### Component System Testing
```python
def test_ship_component_composition(starship):
    """Test ship has all required systems."""
    # Arrange/Act
    weapons = starship.get_component(WeaponSystem)
    shields = starship.get_component(ShieldSystem)
    engines = starship.get_component(EngineSystem)

    # Assert
    assert weapons is not None
    assert shields is not None
    assert engines is not None
    assert weapons.power_level == 100  # Full power on initialization
```

### MVC Separation Testing
```python
def test_model_no_rendering_dependencies():
    """Test game model has no pygame/UI dependencies."""
    # Arrange
    import STRR.src.game.model as model_module

    # Act
    imports = get_module_imports(model_module)

    # Assert
    assert 'pygame' not in imports
    assert 'PySide6' not in imports  # Except for type hints
```

## Coverage Analysis and Reporting

### Coverage Targets and Priorities
- **TARGET** 85%+ coverage for game logic (models, controllers, state machine)
- **TARGET** 80%+ coverage for entity/component systems
- **PRIORITIZE** turn-based mechanics, combat calculations, state transitions
- **FOCUS** on testing actual game behavior patterns
- **MEASURE** coverage of critical gameplay scenarios
- **IDENTIFY** gaps in game logic testing (ship systems, combat, movement)

### Coverage Tools and Configuration
```python
# pytest configuration in pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "--cov=src --cov-report=html --cov-report=term-missing"
```

## Testing Best Practices

### Test Data and Fixtures
- **CREATE** reusable test data and setup functions
- **USE** pytest fixtures for common test resources
- **MAINTAIN** clear test data organization
- **AVOID** hardcoded test values that obscure test intent
- **SEPARATE** test data from test logic

### Mocking and Isolation
- **USE** proper mocking of external dependencies
- **ISOLATE** units under test from complex dependencies
- **MOCK** file system operations, network calls, and external services
- **MAINTAIN** clear boundaries between real and mocked components
- **VALIDATE** mock usage doesn't obscure actual behavior

### Test Performance and Reliability
- **ENSURE** tests run quickly (target < 1 second per test)
- **MAKE** tests deterministic and repeatable
- **AVOID** tests that depend on external resources or timing
- **ELIMINATE** flaky tests that pass/fail inconsistently
- **OPTIMIZE** test execution time without sacrificing coverage

## Repository Integration

### Shared Testing Utilities
- **USE** `projects/common_lib/` for shared test utilities and fixtures
- **CREATE** reusable testing patterns and helpers
- **MAINTAIN** consistency across project test suites
- **ELIMINATE** duplicate testing code through shared utilities

### Python Standard Library Focus
- **PREFER** built-in testing capabilities and assert statements
- **USE** unittest.mock for mocking needs
- **LEVERAGE** built-in modules for test data generation
- **MINIMIZE** external testing dependencies beyond pytest

### Linux Environment Compliance
- **IMPORTANT** All tests designed for Linux environments only
- **TEST** Linux-specific paths, commands, and system calls
- **NOT COMPATIBLE** with Windows environments
- **VALIDATE** proper behavior on target Linux systems

## Testing Decision Framework

### When writing tests, prioritize:
1. **Core Business Logic**: Does this function perform critical business operations?
2. **Public Interfaces**: Is this function part of the public API?
3. **Integration Points**: Does this component interact with other modules?
4. **Type Safety**: Are the type annotations and behavior consistent?
5. **Happy Path Coverage**: Are the expected use cases thoroughly tested?
