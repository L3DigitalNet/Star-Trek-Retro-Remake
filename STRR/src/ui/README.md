# UI Directory Structure

This directory contains all UI-related files for the Star Trek Retro Remake project.

## Directory Layout

```text
ui/
├── designer/          # Qt Designer .ui files (XML format)
│   ├── main_window.ui # Main application window
│   └── dialogs/       # Dialog UI files (future)
├── compiled/          # Compiled Python files from .ui (optional)
│   └── main_window_ui.py
├── dialogs/           # Custom dialog classes
└── widgets/           # Custom widget classes
```

## Workflow

### Qt Designer Files (`designer/`)

Design UI files in Qt Designer:

```bash
# Launch Qt Designer
designer

# Or using PySide6's designer
pyside6-designer
```

**Current Files:**

- `main_window.ui` - Main game window with control panel and game display

### Compiled UI Files (`compiled/`)

Optional: Compile .ui files to Python for faster loading:

```bash
# Compile all .ui files
python scripts/compile_ui.py

# Compile specific file
python scripts/compile_ui.py main_window
```

### Custom Dialogs (`dialogs/`)

Python modules containing custom dialog classes that extend or use UI files.

**Planned:**

- `combat_dialog.py` - Combat results
- `settings_dialog.py` - Game settings
- `ship_status_dialog.py` - Detailed ship status

### Custom Widgets (`widgets/`)

Python modules containing custom widget classes.

**Current:**

- `GameDisplay` - In `view.py`, replaces placeholder for pygame rendering

**Planned:**

- `MiniMap` - Sector overview
- `ScannerDisplay` - Long-range scanner
- `DamageReport` - Ship systems status

## Integration

The main application loads UI files in `game/view.py`:

```python
from PySide6.QtUiTools import QUiLoader

def _load_ui(self):
    ui_file = Path("STRR/src/ui/designer/main_window.ui")
    loader = QUiLoader()
    self.main_window = loader.load(ui_file.open("r"))
```

## Documentation

See `/docs/QT_DESIGNER_WORKFLOW.md` for complete Qt Designer workflow documentation.

## Version

- **Created:** 2025-10-30
- **Last Updated:** 2025-10-30
