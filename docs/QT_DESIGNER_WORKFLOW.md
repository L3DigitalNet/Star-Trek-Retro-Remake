# Qt Designer Workflow Guide

## Overview

The Star Trek Retro Remake project uses Qt Designer for UI design and PySide6 for runtime UI management. This document describes the workflow for designing, compiling, and using UI files.

## Directory Structure

```
STRR/src/ui/
├── designer/          # Qt Designer .ui files (XML format)
│   ├── main_window.ui
│   └── dialogs/       # Dialog UI files
├── compiled/          # Compiled Python files (optional)
│   └── main_window_ui.py
├── dialogs/           # Custom dialog classes
└── widgets/           # Custom widget classes
```

## Qt Designer Workflow

### 1. Designing UI in Qt Designer

**Opening Qt Designer:**

```bash
# Launch Qt Designer
designer

# Or using PySide6's designer
pyside6-designer
```

**Editing UI Files:**

- UI files are located in `STRR/src/ui/designer/`
- Main window: `main_window.ui`
- Open files with: File → Open → Select .ui file

**Important Widget Names:**
The following widget object names are used by the application and must not be changed:

- `shipStatusLabel` - Displays ship status information
- `zLevelLabel` - Shows current z-level
- `messageDisplay` - Game messages area
- `gameDisplay` - Placeholder for pygame surface (replaced at runtime)
- `newGameButton` - New game button
- `saveGameButton` - Save game button
- `loadGameButton` - Load game button
- `settingsButton` - Settings button
- `quitButton` - Quit button

**Design Guidelines:**

- Use descriptive object names in camelCase
- Set minimum/maximum sizes for fixed-size widgets
- Use layouts (QVBoxLayout, QHBoxLayout, QGridLayout)
- Test with different window sizes
- Use stylesheets for colors and spacing

### 2. Two Integration Methods

#### Method A: Direct Loading (Recommended)

Load .ui files directly at runtime without compilation:

**Advantages:**

- No compilation step required
- Changes visible immediately
- Simpler workflow for rapid iteration
- Used by default in the application

**How it works:**

```python
from PySide6.QtUiTools import QUiLoader
from pathlib import Path

loader = QUiLoader()
ui_file = Path("STRR/src/ui/designer/main_window.ui")
window = loader.load(ui_file.open("r"))
```

**Current Implementation:**
See `STRR/src/game/view.py` → `_load_ui()` method

#### Method B: Compilation to Python (Optional)

Compile .ui files to Python modules:

**Advantages:**

- Slightly faster load times
- No runtime XML parsing
- Can be version controlled as .py files
- Better for production builds

**Compilation Script:**

```bash
# Compile all .ui files
python scripts/compile_ui.py

# Compile specific file
python scripts/compile_ui.py main_window

# Manual compilation with pyside6-uic
pyside6-uic STRR/src/ui/designer/main_window.ui -o STRR/src/ui/compiled/main_window_ui.py
```

**Using Compiled UI:**

```python
from ui.compiled.main_window_ui import Ui_MainWindow

class GameView:
    def __init__(self):
        self.main_window = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_window)
```

### 3. Modifying Existing UI

**Workflow:**

1. Open `main_window.ui` in Qt Designer
2. Make your changes (add widgets, modify layouts, etc.)
3. Save the file (Ctrl+S)
4. Run the application - changes will load automatically
5. Optional: Recompile if using Method B

**Testing Changes:**

```bash
# Run the application
python STRR/main.py

# Or run with debug logging
python STRR/main.py --debug
```

### 4. Creating New UI Files

**Dialog Example:**

```bash
# Create new dialog UI
designer STRR/src/ui/designer/dialogs/settings_dialog.ui
```

**Dialog Template Structure:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>SettingsDialog</class>
 <widget class="QDialog" name="SettingsDialog">
  <property name="windowTitle">
   <string>Settings</string>
  </property>
  <!-- Add your widgets here -->
 </widget>
</ui>
```

**Loading Custom Dialog:**

```python
from pathlib import Path
from PySide6.QtUiTools import QUiLoader

def load_settings_dialog(parent):
    ui_file = Path("STRR/src/ui/designer/dialogs/settings_dialog.ui")
    loader = QUiLoader()
    dialog = loader.load(ui_file.open("r"), parent)
    return dialog
```

## Custom Widgets Integration

### GameDisplay Widget

The `GameDisplay` widget is a custom `QLabel` subclass that handles pygame surface rendering and input:

**Replacement Process:**

1. Qt Designer creates placeholder `gameDisplay` QLabel
2. At runtime, `_setup_game_display()` replaces it with `GameDisplay`
3. Custom widget inherits size, position, and layout from placeholder

**Implementation:**
See `STRR/src/game/view.py` → `GameDisplay` class and `_setup_game_display()` method

### Creating Custom Widgets

**Pattern:**

1. Design base widget in Qt Designer
2. Replace at runtime with custom class
3. Preserve layout and properties

**Example:**

```python
def _setup_custom_widget(self):
    # Find placeholder
    placeholder = self.main_window.findChild(QWidget, "customWidgetPlaceholder")
    parent_layout = placeholder.parent().layout()

    # Get position in layout
    index = parent_layout.indexOf(placeholder)

    # Create custom widget
    custom_widget = CustomWidget(self)

    # Replace
    parent_layout.removeWidget(placeholder)
    placeholder.deleteLater()
    parent_layout.insertWidget(index, custom_widget)
```

## Signal/Slot Connections

### In Code (Current Method)

Connections are made in `view.py` → `_connect_signals()`:

```python
def _connect_signals(self):
    self.new_game_btn.clicked.connect(self._on_new_game)
    self.save_game_btn.clicked.connect(self._on_save_game)
    # ... more connections
```

### In Qt Designer (Alternative)

Qt Designer can define connections visually:

1. Switch to "Edit Signals/Slots" mode (F4)
2. Drag from source widget to destination widget
3. Select signal and slot
4. Connections are saved in .ui file

**Note:** Code-based connections are more flexible and recommended for complex logic.

## Styling

### Inline Stylesheets (Qt Designer)

Set in Qt Designer property editor:

- Select widget → styleSheet property → Edit

**Example:**

```css
padding: 10px;
background-color: #1a1a1a;
border: 1px solid #333;
border-radius: 5px;
color: #ccc;
```

### External Stylesheets (Future)

For global styling:

```python
with open("STRR/assets/styles/main.qss") as f:
    app.setStyleSheet(f.read())
```

## Best Practices

### Design

- Use layouts, never absolute positioning
- Set object names for all interactive widgets
- Test responsive behavior (resize window)
- Use size policies appropriately
- Group related controls with QGroupBox

### Development

- Keep .ui files in version control
- Document widget object names
- Test UI changes before committing
- Use direct loading for development
- Consider compilation for production

### Performance

- Pre-allocate buffers for frequent updates
- Cache references to frequently accessed widgets
- Use batch updates with `setUpdatesEnabled(False/True)`
- Minimize layout recalculations

## Troubleshooting

### UI File Not Found

```
Error: UI file not found: /path/to/file.ui
```

**Solution:** Check file path in `_load_ui()` method

### Widget Not Found

```
Error: gameDisplay label not found in UI file
```

**Solution:** Verify object name in Qt Designer matches code

### Layout Issues

**Problem:** Widgets overlapping or misaligned
**Solution:**

- Ensure all widgets are in layouts
- Check size policies and constraints
- Use spacers for flexible spacing

### Signal Connection Failed

**Problem:** Button clicks not working
**Solution:**

- Verify object name is correct
- Check signal connection in `_connect_signals()`
- Ensure widget reference is valid

## Migration Notes

### Before (Programmatic)

```python
def _setup_ui(self):
    button = QPushButton("New Game")
    button.clicked.connect(self._on_new_game)
    layout.addWidget(button)
```

### After (Qt Designer)

```python
def _load_ui(self):
    loader = QUiLoader()
    self.main_window = loader.load(ui_file)
    self.new_game_btn = self.main_window.findChild(QPushButton, "newGameButton")

def _connect_signals(self):
    self.new_game_btn.clicked.connect(self._on_new_game)
```

## References

- Qt Designer Manual: <https://doc.qt.io/qt-6/qtdesigner-manual.html>
- PySide6 Documentation: <https://doc.qt.io/qtforpython-6/>
- UI Files Reference: <https://doc.qt.io/qt-6/designer-ui-file-format.html>
- QUiLoader: <https://doc.qt.io/qtforpython-6/PySide6/QtUiTools/QUiLoader.html>

## Version History

- **0.0.1** (2025-10-30): Initial Qt Designer integration
