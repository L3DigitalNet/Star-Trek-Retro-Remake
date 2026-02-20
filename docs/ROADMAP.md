# Star Trek Retro Remake — Development Roadmap

Current version: v0.0.30 (infrastructure baseline)

## v0.1.0 — Playable Sector Map

**Goal:** Player can actually play a turn.

- [ ] Ship renders on isometric grid at starting position
- [ ] Player clicks grid cell to move ship
- [ ] Movement validated (bounds, obstacles, fuel cost)
- [ ] Turn counter advances
- [ ] Ship stats (shields, hull) visible in side panel

## v0.2.0 — Combat Prototype

**Goal:** Ships can fight.

- [ ] Enemy ship placed in sector
- [ ] Player selects enemy as target
- [ ] Fire phasers: damage calculated and applied
- [ ] Fire torpedoes: separate damage model
- [ ] Combat log shows results
- [ ] Win condition: enemy destroyed
- [ ] Lose condition: player hull = 0

## v0.3.0 — Galaxy Map + Sector Travel

**Goal:** Multiple sectors to explore.

- [ ] Galaxy map renders (overview of sectors)
- [ ] Player ship visible on galaxy map
- [ ] Player can warp to adjacent sector
- [ ] Each sector has different composition (stars, stations, enemies)

## v0.4.0 — Mission System

**Goal:** Things to do.

- [ ] Mission briefing shown at game start
- [ ] Mission tracker shows current objective
- [ ] Complete a mission (reach location, defeat enemy)
- [ ] Mission rewards (crew XP, resources)

## v0.5.0 — Save/Load

**Goal:** Games persist between sessions.

- [ ] Save game to file (TOML)
- [ ] Load game from file
- [ ] Game over screen with restart option

## Infrastructure Debt (ongoing)

- [ ] All tests pass: `uv run pytest` green
- [ ] Type check clean: `uv run mypy STRR/src/`
- [ ] No ruff errors: `uv run ruff check STRR/`
- [ ] Graphics assets for ships (at minimum placeholder sprites)
