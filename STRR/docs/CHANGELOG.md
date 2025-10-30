# Changelog

All notable changes to the Star Trek Retro Remake project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added (Planned Features)

- PySide6 UI integration with embedded PyGame rendering
- Advanced AI behavior system for enemy ships
- Mission generation and dynamic storytelling system
- Audio and visual effects framework
- Comprehensive save/load functionality

### Changed

- TBD

### Fixed

- TBD

### Removed

- TBD

## [0.0.2] - 2025-10-30

### Added

- TOML configuration system for improved readability and maintainability
- Configuration manager utility with JSON fallback support during migration
- JSON to TOML migration script for future configuration file conversions
- Comprehensive TOML examples with comments and proper organization

### Changed

- **BREAKING**: Migrated all configuration files from JSON to TOML format
  - `game_settings.json` → `game_settings.toml` with improved structure and comments
  - `game_data.json` → `game_data.toml` with cleaner ship class definitions
  - `key_bindings.json` → `key_bindings.toml` with better organization
  - `sol_system.json` → `sol_system.toml` using array of tables for objects
- Updated documentation to reflect TOML usage (ARCHITECTURE.md, DESIGN.md, PROJECT-DOC.md)
- Enhanced configuration system with dot notation access and type safety
- Updated version numbers across project files (pyproject.toml, main.py)
- Corrected documentation path references from `/GDD/DESIGN.md` to `/docs/DESIGN.md`
- Updated all file header "Date Changed" fields to reflect documentation updates

### Fixed

- Documentation path inconsistencies between README.md and copilot instructions
- Version number mismatch between CHANGELOG.md (0.0.2) and project files (0.0.1)

## [0.0.1] - 2024-12-15

### Added

- Initial project structure and development framework
- Core MVC architecture implementation with hybrid State Machine + Game Object + Component pattern
- Game entity system with GameObject base class and Starship implementation
- Component system for ship subsystems (weapons, shields, engines, sensors, life support)
- State machine for game mode transitions (Galaxy Map ↔ Sector Map ↔ Combat Mode)
- Grid-based positioning system with 3D coordinate support (GridPosition with x, y, z levels)
- Turn-based game model with TurnManager and combat resolution system
- Resource management system for ship energy, fuel, crew morale, and supplies
- Comprehensive configuration system with JSON files for game settings, key bindings, and ship classes (later migrated to TOML in v0.0.2)
- Asset management structure with organized directories for graphics, audio, and data
- Comprehensive pytest testing framework with fixtures and AAA pattern testing
- Object pooling foundation for efficient memory management
- Complete project documentation including README.md, PROJECT-DOC.md, and architecture guides
- Development guidelines with Python 3.14+ standards and type hints
- Git workflow and version management system

### Technical Implementation

- **Architecture**: Hybrid State Machine + Game Object + Component + MVC pattern
- **Game Loop**: Fixed timestep implementation ready for PyGame integration
- **Entity System**: GameObject base with Starship and SpaceStation implementations
- **Component Pattern**: Modular ship systems with damage/repair mechanics
- **State Management**: GameStateManager with mode transition validation
- **Configuration**: JSON-based settings for display, audio, gameplay, and controls
- **Testing**: pytest framework with comprehensive test coverage for core logic
- **Documentation**: Complete technical documentation and development guidelines

### Project Structure

- `/main.py`: Game entry point and application launcher
- `/src/game/`: Core MVC architecture (application.py, model.py, view.py, controller.py)
- `/src/entities/`: Game objects (base.py, starship.py with component composition)
- `/src/components/`: Ship systems (ship_systems.py with modular subsystems)
- `/src/states/`: State machine implementation (state_machine.py with GameState management)
- `/src/maps/`: Galaxy, sector, and combat map systems (galaxy.py, sector.py)
- `/config/`: JSON configuration files for all game settings and data
- `/assets/`: Organized asset directories for graphics, audio, and data files
- `/tests/`: Comprehensive pytest test suite with fixtures and mock objects
- `/docs/`: Project documentation including architecture and development guides

### Configuration Files

- `game_settings.json`: Display, audio, and gameplay configuration
- `key_bindings.json`: Keyboard shortcuts and control mappings
- `ship_classes.json`: Starship specifications and capabilities
- `factions.json`: Faction relationships and characteristics
- `missions.json`: Mission templates and objectives

### Testing Coverage

- Unit tests for all entity classes and game logic
- Integration tests for state transitions and system interactions
- Fixtures for common test objects (ships, positions, game states)
- Mock objects for UI and external dependencies
- AAA pattern testing for clear test structure and maintainability

### Development Standards

- Python 3.14+ with modern syntax (union types, match statements, Path.copy())
- Comprehensive type hints for all functions, variables, and data structures
- PEP 8 compliance with f-string formatting exclusively
- Detailed docstrings with function parameters and return values
- Clean architecture with separation of concerns and testable design
- Standard library first approach with justified external dependencies

### Known Limitations

- UI integration pending (PySide6/PyGame coordination not yet implemented)
- Combat AI behavior requires implementation
- Save/load functionality needs development
- Asset loading and caching system pending
- Audio system not yet implemented

### Next Development Phase (v0.1.0)

- PySide6 main window implementation with embedded PyGame widget
- Basic ship movement and exploration mechanics
- Simple combat system with AI opponents
- Resource management UI and feedback systems
- Galaxy and sector map generation algorithms
