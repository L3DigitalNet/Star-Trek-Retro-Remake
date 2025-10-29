---
description: "Custom instructions for Star Trek Retro Remake Game development with Python"
applyTo: "**"
---

# Star Trek Retro Remake Game Development Guidelines

*Note: This file extends the common requirements found in `common-requirements.instructions.md`. All shared requirements (headers, testing, etc.) are defined there.*

## Game Requirements
- **MUST** implement ECS or Game Object pattern for Star Trek entities (ships, stations, crew)
- **MUST** use PyGame for game engine (justify alternatives with comments)
- **MUST** use PyQt6 for UI/menus/settings/dialogs (justify alternatives with comments)
- **MUST** implement game loop: input → update → render (fixed timestep)
- **MUST** implement game state machine (main menu, bridge view, tactical, paused, etc.)
- **MUST** separate game logic from rendering
- **MUST** use object pooling and proper memory management
- **MUST** test game logic separately from graphics/audio
- **MUST** validate game state transitions and logic independently of rendering
- **MUST** test collision detection, physics, and game mechanics in isolation

## Game Header Requirements
- **MUST** include Game-specific Features section with:
  - Game loop with fixed timestep for consistent physics
  - State machine for main menu, bridge view, tactical, paused, game over states
  - ECS (Entity-Component-System) architecture for Star Trek game objects
  - Object pooling for efficient memory management
  - Separated game logic from rendering for testability
  - PyGame for game engine, PyQt6 for UI/menus

## Game Code Generation Focus
- **Framework:** Start with PyGame for engine, PyQt6 for UI, justify alternatives
- **Architecture:** Separate logic/rendering/input, use ECS/GameObject patterns for Star Trek entities
- **Pattern:** Follow template below

## Game Development Template

```python
class Game:
    """Main game controller implementing game loop."""

    def __init__(self):
        self.running = True
        self.clock = pygame.time.Clock()
        self.state_manager = GameStateManager()
        self.resource_manager = ResourceManager()

    def run(self):
        """Main game loop with fixed timestep."""
        while self.running:
            dt = self.clock.tick(60) / 1000.0  # Convert to seconds

            self.handle_events()
            self.update(dt)
            self.render()

    def handle_events(self):
        """Process input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.state_manager.current_state.handle_event(event)

    def update(self, dt: float):
        """Update game logic with delta time."""
        self.state_manager.current_state.update(dt)

    def render(self):
        """Render current game state."""
        self.state_manager.current_state.render()
        pygame.display.flip()
```
