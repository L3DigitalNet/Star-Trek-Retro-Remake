---
mode: "agent"
description: "Create or update a Qt Designer .ui file representing the current state of the Qt UI as defined in Python code"
---

# Create Qt Designer .ui File from Python Code

## Objective

Generate a complete Qt Designer `.ui` file (XML format) that accurately represents all UI widgets, layouts, actions, and properties currently referenced in the project's Python view code.

## Process

### 1. Analyze View Code

Read and analyze the main view file(s) to identify:

- **File Location**: `STRR/src/game/view.py` (or current view module)
- **UI Loading Method**: Check `_load_ui()` method to find where `.ui` file is loaded from
- **Widget References**: All `findChild()` calls that retrieve UI elements
- **Action References**: All `QAction` objects referenced (menus, toolbars)
- **Layout Structure**: Central widget, dock widgets, toolbars, status bars, menu bars

### 2. Extract Widget Inventory

Create a comprehensive list of ALL widgets referenced in code:

**Widget Types to Check**:
- `QLabel` - Display text, images, game surface
- `QPushButton` - Action buttons, turn controls
- `QProgressBar` - Hull, shields, energy status
- `QDockWidget` - Side panels for status/controls
- `QAction` - Menu items, toolbar actions
- `QToolBar` - Main toolbar
- `QMenuBar` and `QMenu` - Menu structure
- `QStatusBar` - Status information

**Common Patterns**:
```python
# Look for these patterns in view code:
self.widget_name = self.main_window.findChild(QWidgetType, "objectName")
self.main_window.findChild(QAction, "actionName")
```

### 3. Identify Required Properties

For each widget, capture:

- **objectName**: Must match Python findChild() call exactly
- **text**: Default display text
- **toolTip**: Hover help text (if set in code)
- **minimumSize/maximumSize**: Size constraints
- **styleSheet**: CSS-like styling
- **shortcuts**: Keyboard shortcuts for actions
- **enabled/visible**: Default state

### 4. Build UI File Structure

Create XML following this hierarchy:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">...</property>
  <property name="windowTitle">...</property>

  <!-- Central Widget -->
  <widget class="QWidget" name="centralwidget">
   <layout class="QVBoxLayout">...</layout>
  </widget>

  <!-- Menu Bar -->
  <widget class="QMenuBar" name="menubar">
   <widget class="QMenu" name="menuName">...</widget>
  </widget>

  <!-- Status Bar -->
  <widget class="QStatusBar" name="statusbar"/>

  <!-- Toolbars -->
  <widget class="QToolBar" name="toolbarName">...</widget>

  <!-- Dock Widgets -->
  <widget class="QDockWidget" name="dockName">...</widget>

  <!-- Actions (defined at bottom) -->
  <action name="actionName">...</action>
 </widget>
</ui>
```

### 5. Widget-Specific Guidelines

**Game Display (pygame surface placeholder)**:
```xml
<widget class="QLabel" name="gameDisplay">
 <property name="minimumSize">
  <size><width>1280</width><height>900</height></size>
 </property>
 <property name="alignment">
  <set>Qt::AlignCenter</set>
 </property>
</widget>
```
*Note: Will be replaced by custom GameDisplay widget at runtime*

**Progress Bars (ship status)**:
```xml
<widget class="QProgressBar" name="hullProgressBar">
 <property name="value"><number>100</number></property>
 <property name="textVisible"><bool>true</bool></property>
 <property name="format"><string>%p%</string></property>
</widget>
```

**Actions (menu/toolbar)**:
```xml
<action name="actionZoomIn">
 <property name="text"><string>Zoom In</string></property>
 <property name="toolTip"><string>Zoom in on the map</string></property>
 <property name="shortcut"><string>+</string></property>
</action>
```

**Dock Widgets**:
```xml
<widget class="QDockWidget" name="rightDock">
 <property name="allowedAreas">
  <set>Qt::RightDockWidgetArea</set>
 </property>
 <attribute name="dockWidgetArea"><number>2</number></attribute>
 <widget class="QWidget" name="dockWidgetContents">
  <layout class="QVBoxLayout">...</layout>
 </widget>
</widget>
```

### 6. Styling and Theme

Include project-appropriate styling:

```xml
<property name="styleSheet">
 <string notr="true">
  QMainWindow { background-color: #1a1a2e; }
  QPushButton {
   background-color: #444;
   color: #ffffff;
   border-radius: 3px;
  }
  /* ... Star Trek theme colors ... */
 </string>
</property>
```

### 7. Validation Checklist

Before finalizing, verify:

- [ ] Every `findChild()` call in Python code has matching objectName in .ui
- [ ] All QAction references are defined as `<action>` elements
- [ ] Layout types match (QVBoxLayout, QHBoxLayout, etc.)
- [ ] Dock widget areas are correct (Left=1, Right=2, Top=4, Bottom=8)
- [ ] Toolbar areas are specified
- [ ] Signal/slot connections are defined if needed
- [ ] Spacers are included to control layout stretching

### 8. File Output

**Location**: `STRR/src/ui/designer/main_window_complete.ui`
**Format**: UTF-8 encoded XML, properly indented
**Usage**: Can be opened directly in Qt Designer for manual editing

### 9. Common Widget Object Names

Based on Star Trek Retro Remake project:

**Turn Bar**:
- `turnBar`, `endTurnButton`, `turnNumberLabel`, `phaseLabel`, `actionPointsLabel`

**Ship Status**:
- `shipNameLabel`, `hullProgressBar`, `shieldsProgressBar`, `energyProgressBar`
- `coordinatesLabel`, `sectorLabel`

**Action Buttons**:
- `moveButton`, `rotateButton`, `fireButton`, `scanButton`
- `evasiveButton`, `dockButton`, `hailButton`

**View Actions**:
- `actionGalaxyMode`, `actionSectorMode`, `actionCombatMode`
- `actionZoomIn`, `actionZoomOut`, `actionZoomReset`

**Game Actions**:
- `actionNewGame`, `actionSaveGame`, `actionLoadGame`, `actionQuit`

**Dock Widgets**:
- `rightDock` (ship status and controls)

**Central Widget**:
- `gameDisplay` (replaced at runtime with GameDisplay widget)

## Important Notes

1. **Runtime Widget Replacement**: The `gameDisplay` QLabel is replaced at runtime with a custom `GameDisplay` widget that handles pygame surface rendering and input events. The .ui file only needs the placeholder QLabel.

2. **Dynamic Loading**: The project uses `QUiLoader` to load the .ui file dynamically at runtime, so no Python compilation step is needed.

3. **Testing**: After creating/updating the .ui file:
   ```bash
   # Test in Qt Designer
   pyside6-designer STRR/src/ui/designer/main_window_complete.ui

   # Test in application
   cd /home/chris/GitHub/Star-Trek-Retro-Remake
   python STRR/main.py
   ```

4. **No Code Changes Needed**: When updating the .ui file, Python code should require NO changes if widget objectNames remain consistent.

## Output Format

Generate complete, valid XML that:
- Is properly formatted and indented
- Includes XML declaration: `<?xml version="1.0" encoding="UTF-8"?>`
- Uses Qt Designer 4.0 format: `<ui version="4.0">`
- Contains ALL required widgets and actions
- Is immediately usable in Qt Designer