# Qt Designer Quick Reference

## Opening Qt Designer

```bash
# Method 1: Standalone Qt Designer
designer

# Method 2: PySide6 Designer
pyside6-designer

# Method 3: Open specific file
pyside6-designer STRR/src/ui/designer/main_window.ui
```

## Current UI Files

- **main_window.ui** - Main application window

## Important Widget Object Names

These object names are used in the code and must not be changed:

| Widget Name | Type | Purpose |
|------------|------|---------|
| `shipStatusLabel` | QLabel | Ship status information |
| `zLevelLabel` | QLabel | Current z-level display |
| `messageDisplay` | QLabel | Game messages area |
| `gameDisplay` | QLabel | Placeholder (replaced with GameDisplay) |
| `newGameButton` | QPushButton | New game button |
| `saveGameButton` | QPushButton | Save game button |
| `loadGameButton` | QPushButton | Load game button |
| `settingsButton` | QPushButton | Settings button |
| `quitButton` | QPushButton | Quit button |

## Common Tasks

### Edit Main Window

```bash
pyside6-designer STRR/src/ui/designer/main_window.ui
```

### Test Changes

```bash
# Changes are loaded automatically - just run the app
python STRR/main.py
```

### Compile UI (Optional)

```bash
# Compile all .ui files
python scripts/compile_ui.py

# Compile specific file
python scripts/compile_ui.py main_window
```

## Widget Properties to Set

### All Widgets

- **objectName**: Descriptive camelCase name
- **sizePolicy**: How widget resizes

### Buttons

- **text**: Button label
- **styleSheet**: CSS-like styling (optional)

### Labels

- **text**: Label content (can include HTML)
- **alignment**: Text alignment
- **wordWrap**: Enable for multi-line text

### Layouts

- **margins**: Space around layout (px)
- **spacing**: Space between widgets (px)

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl+R | Preview form |
| Ctrl+S | Save |
| F4 | Edit signals/slots |
| F3 | Edit buddies |
| F2 | Edit tab order |

## Tips

1. **Always use layouts** - Never use absolute positioning
2. **Set object names** - For all interactive widgets
3. **Test responsiveness** - Resize window in preview
4. **Use spacers** - For flexible spacing
5. **Preview often** - Press Ctrl+R to test

## Full Documentation

See: `/docs/QT_DESIGNER_WORKFLOW.md`
