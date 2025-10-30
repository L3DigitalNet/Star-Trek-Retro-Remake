# Star Trek Retro Remake

[![Python 3.14+](https://img.shields.io/badge/python-3.14+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PyGame](https://img.shields.io/badge/PyGame-2.5+-green.svg)](https://pygame.org/)
[![PySide6](https://img.shields.io/badge/PySide6-6.7+-purple.svg)](https://wiki.qt.io/Qt_for_Python)

A turn-based, grid-based Star Trek strategy game inspired by the classic retro games **Star Trek (1971)** and **Super Star Trek (1973)**. Command a Federation starship, explore the galaxy, engage in tactical combat, and complete missions in the Kirk-era 23rd century.

## 🚀 Features

- **Turn-based tactical combat** with detailed ship systems
- **3D grid-based exploration** with multiple z-levels
- **Hybrid State Machine + Game Object + Component architecture**
- **Classic Star Trek setting** (Kirk-era 23rd century)
- **Multiple gameplay modes** (Galaxy Map, Sector Map, Combat)
- **Resource management** and ship customization
- **PyGame game engine** with **PySide6 UI framework**

## 🎮 Game Modes

### Galaxy Map

Navigate between sectors, plan missions, and manage fleet resources with a strategic view of Federation space.

### Sector Map

Explore individual sectors on a 3D grid (up to 20x20x5), encounter alien species, dock at starbases, and discover anomalies.

### Combat Mode

Engage in tactical turn-based combat on specialized combat grids with environmental factors and detailed ship system management.

## 🛠️ Technical Requirements

### System Requirements

- **Platform**: Linux (primary target)
- **Python**: 3.14+ (uses latest language features)
- **RAM**: 512MB minimum for base assets
- **Storage**: 200MB for full installation

### Dependencies

- **PyGame 2.5+**: Core game engine for rendering and game loop
- **PySide6 6.7+**: UI framework for menus, dialogs, and main window
- **Python Standard Library**: Primary dependency approach

## 📦 Installation

### Prerequisites

```bash
# Ensure Python 3.14+ is installed
python3 --version

# Install core dependencies
pip install pygame>=2.5 PySide6>=6.7
```

### Quick Start

```bash
# Clone the repository
git clone https://github.com/L3DigitalNet/Star-Trek-Retro-Remake.git
cd Star-Trek-Retro-Remake

# Install package with dependencies (recommended)
pip install -e .

# Or install manually
pip install pygame>=2.5 PySide6>=6.7

# Run the game
cd star_trek_retro_remake
python3 main.py
```

### Development Setup

```bash
# Install with development dependencies
pip install -e .[dev]

# Set up pre-commit hooks
pre-commit install

# Run tests to verify installation
cd star_trek_retro_remake
python3 -m pytest tests/ -v

# Run with coverage report
python3 -m pytest tests/ --cov=src --cov-report=term-missing

# Use Make commands for common tasks
make test          # Run tests
make lint          # Check code quality
make format        # Format code
make check         # Run all checks
```

## 🎯 Quick Gameplay Guide

### Basic Controls

- **Mouse**: Primary interaction method for all game elements
- **Keyboard Shortcuts**: Access common actions and menus
- **Right-click**: Context menus for detailed object information

### Starting Your First Game

1. Launch the game and select "New Game" from the main menu
2. Your ship (USS Enterprise) begins in a starting sector
3. Use the **Sector Map** to explore and find missions
4. Engage enemies in **Combat Mode** for tactical battles
5. Return to **Galaxy Map** for long-distance travel

### Core Mechanics

- **Energy Management**: Allocate power between shields, weapons, and engines
- **Turn-based Movement**: Plan your moves strategically on the grid
- **Ship Systems**: Monitor and repair weapons, shields, engines, and sensors
- **Resource Management**: Manage fuel, supplies, and crew morale

## 🏗️ Architecture Overview

### Design Pattern

**Hybrid State Machine + Game Object + Component + MVC**

```
┌─────────────────────────────────────────┐
│            PySide6 UI Layer             │
│        (Menus, Dialogs, Windows)        │
├─────────────────────────────────────────┤
│             Controller Layer            │
│        (Input, State Management)        │
├─────────────────────────────────────────┤
│              Model Layer                │
│         (Game Logic, Data)              │
├─────────────────────────────────────────┤
│             View Layer                  │
│        (PyGame Rendering)               │
└─────────────────────────────────────────┘
```

### Key Components

- **Game State Machine**: Manages transitions between Galaxy/Sector/Combat modes
- **Game Objects**: Starships, stations, and crew with natural hierarchies
- **Component Systems**: Modular ship systems (weapons, shields, engines, sensors)
- **MVC Separation**: Pure game logic isolated from UI for testability

## 📂 Project Structure

```
star_trek_retro_remake/
├── main.py                 # Game entry point
├── src/
│   ├── game/
│   │   ├── application.py   # Main application controller
│   │   ├── model.py         # Core game logic and state
│   │   ├── view.py          # PySide6 UI and PyGame rendering
│   │   └── controller.py    # Input handling and coordination
│   ├── entities/           # Game objects (ships, stations)
│   ├── components/         # Ship systems and components
│   ├── states/            # State machine implementation
│   └── maps/              # Galaxy, sector, and combat maps
├── config/                # JSON configuration files
├── assets/               # Graphics, audio, and data
├── tests/               # Pytest test suite
└── docs/               # Documentation
```

## 🧪 Testing

The project uses **pytest** with AAA (Arrange-Act-Assert) pattern for comprehensive testing:

```bash
# Run all tests
python3 -m pytest tests/ -v

# Run specific test categories
python3 -m pytest tests/test_entities.py -v      # Entity system tests
python3 -m pytest tests/test_game_model.py -v   # Game logic tests

# Generate coverage report
python3 -m pytest tests/ --cov=src --cov-report=html
```

### Test Coverage

- **Core Logic**: 80%+ coverage for critical game mechanics
- **Entity System**: Full coverage for ship and station classes
- **State Management**: Complete state transition validation
- **Component System**: Comprehensive ship system testing

## 🚧 Development Status

### Current Version: 0.0.2 (Pre-Alpha)

#### ✅ Completed

- [x] Project structure and architecture setup
- [x] Core MVC framework implementation
- [x] Entity system with Game Object pattern
- [x] Component system for ship subsystems
- [x] State machine for game mode transitions
- [x] TOML-based configuration system (migrated from JSON)
- [x] Comprehensive test framework with pytest
- [x] Development tooling (Makefile, pre-commit hooks, CI/CD)
- [x] Custom exception hierarchy and event system
- [x] Command pattern for undo/redo functionality

#### 🔄 In Progress

- [ ] PyGame rendering engine integration
- [ ] PySide6 UI implementation
- [ ] Galaxy and sector map generation
- [ ] Combat system implementation

#### 📋 Planned (v0.1.0)

- [ ] Basic ship movement and exploration
- [ ] Simple combat mechanics
- [ ] Resource management system
- [ ] Save/load functionality

## 🤝 Contributing

This is currently a solo indie project for personal enjoyment. While not actively seeking contributors, suggestions and feedback are welcome through GitHub issues.

### Development Guidelines

- Follow the project's **Python 3.14+** modern syntax standards
- Use **type hints everywhere** for better code clarity
- Write **pytest tests** for all new functionality
- Follow **PEP 8** style guidelines strictly
- Document all functions and classes with proper docstrings

## 📄 Documentation

- **[Game Design Document](docs/DESIGN.md)**: Complete game design specification
- **[Architecture Guide](docs/ARCHITECTURE.md)**: Technical implementation details
- **[Project Documentation](star_trek_retro_remake/docs/PROJECT-DOC.md)**: Detailed project information
- **[Change Log](star_trek_retro_remake/docs/CHANGELOG.md)**: Version history and updates

## ⚖️ Legal Notice

This is a **fan-made project** created for educational and entertainment purposes. All Star Trek intellectual property rights belong to their respective owners (Paramount/CBS). This project is not affiliated with or endorsed by the official Star Trek franchise.

- **No commercial use**: This game is completely free and open source
- **Fair use**: Content follows fan work guidelines and fair use principles
- **Original content**: Focuses on original implementations inspired by Star Trek
- **No copyrighted assets**: Avoids direct copying of official Star Trek material

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Star Trek community** for inspiration and decades of amazing content
- **Classic games** Star Trek (1971) and Super Star Trek (1973) for the foundational gameplay concepts
- **Python gaming community** for excellent frameworks and resources
- **Open source contributors** for the tools that make this project possible

---

**Live long and prosper** 🖖
