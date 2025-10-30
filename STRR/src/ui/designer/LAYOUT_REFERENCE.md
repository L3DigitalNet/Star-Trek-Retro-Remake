# Star Trek Retro Remake - UI Layout Reference

## Layout Overview

The main application window implements **Layout Option 2: "Right-Rail Tactical"** from DESIGN.md.

This layout provides a focused, simple interface optimized for turn-based tactical gameplay.

## Window Structure

```text
+---------------------------------------------------------------+
| Menu Bar: File, View                                          |
+---------------------------------------------------------------+
| Toolbar: [Galaxy] [Sector] [Combat] | [+] [-] [Reset] | [⚙] |
+---------------------------------------------------------------+
|                               |  Right Dock (300px min)       |
|                               |  +--------------------------+ |
|                               |  | Tabs:                    | |
|    Central Game Display       |  | ┌────────────────────┐   | |
|    (Expanding, min 800x600)   |  | │ Status | Actions |  │   | |
|                               |  | │        | Map     |  │   | |
|                               |  | └────────────────────┘   | |
|                               |  |                          | |
|                               |  | [Tab Content Area]       | |
|                               |  |                          | |
|                               |  |                          | |
+-------------------------------+  +--------------------------+ |
| Turn Bar: [End Turn] AP: 10 | Phase: Planning | Turn: 1    |
+---------------------------------------------------------------+
```

## Component Details

### 1. Menu Bar

**Location:** Top of window

**Menus:**

- **File:** New Game, Save Game, Load Game, Quit
- **View:** Toggle Control Center (show/hide right dock)

### 2. Main Toolbar

**Location:** Below menu bar

**Sections:**

1. **Mode Switcher:** Galaxy | Sector | Combat
2. **Zoom Controls:** Zoom In (+) | Zoom Out (-) | Reset Zoom
3. **Settings:** Settings button

**Properties:**

- Fixed (not movable)
- Icon size: 32x32
- Top toolbar area

### 3. Central Game Display

**Location:** Main window area (central widget)

**Properties:**

- Widget Type: QLabel (replaced by custom GameDisplay)
- Minimum Size: 800x600
- Size Policy: Expanding/Expanding (stretch=1)
- Background: Dark space (#1a1a2e)
- Border: 2px solid #333

**Purpose:**

- Hosts pygame-ce rendering surface
- Captures mouse clicks and keyboard input
- Displays isometric sector map

### 4. Right Dock Widget

**Location:** Right side of window

**Properties:**

- Minimum Width: 300px
- Dock Areas: Left or Right (allowed)
- Features: Closable, Movable, Floatable
- Title: "Control Center"

**Contains:** QTabWidget with 3 tabs

#### Tab 1: Status

**Layout:** QVBoxLayout with QGroupBox widgets

**Ship Status Group:**

- Ship name label (bold, blue)
- Hull progress bar (green)
- Shields progress bar (blue)
- Energy progress bar (yellow, shows value/max)

**Position Group:**

- Coordinates: X, Y, Z
- Sector name

#### Tab 2: Actions

**Layout:** QVBoxLayout with grouped action buttons

**Movement Group:**

- Move Ship button
- Rotate button

**Combat Group:**

- Fire Weapons button
- Scan Target button
- Evasive Maneuvers button

**Utilities Group:**

- Dock at Station button
- Hail Ship button

**Button Properties:**

- Minimum height: 30px
- Full width

#### Tab 3: Map

**Layout:** QVBoxLayout

**Components:**

- Mini-map display (250x250, placeholder)
- Legend group with color-coded symbols:
  - Blue square: Player Ship
  - Red square: Enemy Ship
  - Orange square: Station
  - Gray square: Asteroid

### 5. Bottom Turn Bar

**Location:** Bottom of window

**Properties:**

- Fixed Height: 50px
- Background: #2a2a2a
- Border Top: 2px solid #444

**Components (left to right):**

1. **End Turn Button:**
   - Size: 120x30
   - Color: Blue (#0066aa)
   - Bold text

2. **Action Points Label:**
   - Text: "Action Points: 10"
   - Color: Yellow (#ffcc00)
   - Bold, 14pt

3. **Spacer** (expanding)

4. **Phase Label:**
   - Text: "Phase: Planning"
   - Color: Green (#00ff99)
   - Bold, 14pt

5. **Turn Number Label:**
   - Text: "Turn: 1"
   - Color: Gray (#cccccc)
   - 14pt

## UI Element Naming Convention

All UI elements follow consistent naming:

### Labels

- Ship name: `shipNameLabel`
- Coordinates: `coordinatesLabel`
- Sector: `sectorLabel`
- Action points: `actionPointsLabel`
- Phase: `phaseLabel`
- Turn number: `turnNumberLabel`

### Progress Bars

- Hull: `hullProgressBar`
- Shields: `shieldsProgressBar`
- Energy: `energyProgressBar`

### Buttons

- End turn: `endTurnButton`
- Move: `moveButton`
- Rotate: `rotateButton`
- Fire: `fireButton`
- Scan: `scanButton`
- Evasive: `evasiveButton`
- Dock: `dockButton`
- Hail: `hailButton`

### Actions (Toolbar/Menu)

- Galaxy mode: `actionGalaxyMode`
- Sector mode: `actionSectorMode`
- Combat mode: `actionCombatMode`
- Zoom in: `actionZoomIn`
- Zoom out: `actionZoomOut`
- Zoom reset: `actionZoomReset`
- New game: `actionNewGame`
- Save game: `actionSaveGame`
- Load game: `actionLoadGame`
- Quit: `actionQuit`
- Toggle dock: `actionToggleRightDock`

### Containers

- Central widget: `centralwidget`
- Game display: `gameDisplay`
- Turn bar: `turnBar`
- Right dock: `rightDock`
- Tab widget: `controlTabWidget`
- Status tab: `statusTab`
- Actions tab: `actionsTab`
- Map tab: `mapTab`

## Color Scheme

### Backgrounds

- Main window: Default Qt theme
- Game display: Dark space (#1a1a2e)
- Turn bar: Dark gray (#2a2a2a)

### Borders

- Game display: #333 (2px)
- Turn bar top: #444 (2px)

### Text Colors

- Ship name: Blue (#00aaff)
- Action points: Yellow (#ffcc00)
- Phase: Green (#00ff99)
- Turn number: Light gray (#cccccc)

### Progress Bars

- Hull: Green (#00aa00)
- Shields: Blue (#0088ff)
- Energy: Yellow (#ffcc00)

### Buttons

- End Turn: Blue background (#0066aa)
- Other buttons: Default Qt theme

## Integration with GameView

The `view.py` module integrates with this UI structure:

### Initialization

1. Loads `main_window.ui` via QUiLoader
2. Finds all UI elements by name
3. Connects signals to handler methods
4. Replaces `gameDisplay` QLabel with custom `GameDisplay` widget

### Update Methods

- `show_ship_status(ship)`: Updates status tab progress bars
- `update_turn_info(turn, phase, ap)`: Updates turn bar labels
- `render_sector_map(sector, objects)`: Renders to game display

### Signal Handlers

- Mode switchers: `_on_galaxy_mode()`, `_on_sector_mode()`, `_on_combat_mode()`
- Zoom controls: `_on_zoom_in()`, `_on_zoom_out()`, `_on_zoom_reset()`
- Game actions: `_on_new_game()`, `_on_save_game()`, `_on_load_game()`, `_on_quit()`
- Turn action: `_on_end_turn()`
- Ship actions: `_on_move()`, `_on_rotate()`, `_on_fire()`, `_on_scan()`, `_on_evasive()`, `_on_dock()`, `_on_hail()`

## Customization

### Changing Dock Position

The right dock can be moved by the user to the left side or floated as a separate window.

### Hiding the Dock

Use **View → Toggle Control Center** or the dock's close button.

### Resizing

- Main window can be resized (minimum 1600x1000 recommended)
- Game display expands to fill available space
- Right dock maintains minimum 300px width
- Turn bar maintains fixed 50px height

## Future Enhancements

Planned improvements (from DESIGN.md):

- Mini-map rendering in Map tab
- Real-time status updates during combat
- Animation feedback for button clicks
- Dialog systems for mission briefings
- Status bar for messages (replacing removed message display)
- Context menus for ship actions
- Keyboard shortcuts display

## Version

- **Created:** 2025-10-30
- **Version:** 0.0.16
- **Layout:** Right-Rail Tactical (Option 2)
