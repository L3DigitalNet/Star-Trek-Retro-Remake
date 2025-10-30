# Qt 6 Module Mapping Reference

## C++ Library to Python Module Mapping

This document maps the Qt C++ library names to their corresponding PySide6 Python modules.

### ✓ All Requested Modules Available

| Qt C++ Library | Python Module | Package | Status |
|----------------|---------------|---------|--------|
| `qt6-quick` | `PySide6.QtQuick` | PySide6-Essentials | ✓ Installed |
| `qt6-quickcontrols2` | `PySide6.QtQuickControls2` | PySide6-Essentials | ✓ Installed |
| `qt6-quickshapes` | `PySide6.QtQuick` (integrated) | PySide6-Essentials | ✓ Installed |
| `qt6-multimedia` | `PySide6.QtMultimedia` | PySide6-Addons | ✓ Installed |
| `qt6-statemachine` | `PySide6.QtStateMachine` | PySide6-Addons | ✓ Installed |
| `qt6-svg` | `PySide6.QtSvg` | PySide6-Addons | ✓ Installed |
| `qt6-3d` | `PySide6.Qt3DCore`, `Qt3DRender`, etc. | PySide6-Addons | ✓ Installed |

## Installed Packages

```text
PySide6            6.10.0
PySide6-Essentials 6.10.0
PySide6-Addons     6.10.0
shiboken6          6.10.0
```

## Import Examples

### Qt Quick (qt6-quick)

```python
from PySide6.QtQuick import QQuickView, QQuickItem, QQuickWindow
from PySide6.QtQml import QQmlApplicationEngine, QQmlComponent
```

### Qt Quick Controls 2 (qt6-quickcontrols2)

```python
from PySide6.QtQuickControls2 import QQuickStyle
```

### Qt Quick Shapes (qt6-quickshapes)

```python
# Integrated into QtQuick - use in QML with:
# import QtQuick.Shapes
from PySide6.QtQuick import QQuickItem
```

### Qt Multimedia (qt6-multimedia)

```python
from PySide6.QtMultimedia import (
    QMediaPlayer,
    QAudioOutput,
    QSoundEffect,
    QAudioSink,
    QMediaDevices,
)
```

### Qt State Machine (qt6-statemachine)

```python
from PySide6.QtStateMachine import (
    QStateMachine,
    QState,
    QFinalState,
    QHistoryState,
    QSignalTransition,
)
```

### Qt SVG (qt6-svg)

```python
from PySide6.QtSvg import QSvgRenderer, QSvgGenerator
from PySide6.QtSvgWidgets import QSvgWidget
```

### Qt 3D (qt6-3d)

```python
from PySide6.Qt3DCore import Qt3DCore, QEntity, QTransform
from PySide6.Qt3DRender import (
    Qt3DRender,
    QCamera,
    QMesh,
    QMaterial,
    QRenderSettings,
)
from PySide6.Qt3DInput import Qt3DInput, QInputSettings
from PySide6.Qt3DLogic import Qt3DLogic, QFrameAction
from PySide6.Qt3DExtras import (
    Qt3DWindow,
    QFirstPersonCameraController,
    QPhongMaterial,
    QSphereMesh,
)
from PySide6.Qt3DAnimation import (
    Qt3DAnimation,
    QAnimationController,
    QMorphingAnimation,
)
```

## Important Notes

1. **No separate installation needed**: The Qt C++ library names (`qt6-*`) refer to system packages. For Python/PySide6 development, all functionality is included in the PySide6 packages.

2. **Package distribution**:
   - **PySide6-Essentials**: Core modules (QtCore, QtGui, QtWidgets, QtQml, QtQuick, etc.)
   - **PySide6-Addons**: Additional modules (Qt3D, QtMultimedia, QtSvg, QtStateMachine, etc.)
   - **shiboken6**: Binding generator tool

3. **Qt Quick Shapes**: In Qt 6, Qt Quick Shapes is integrated into the QtQuick module itself. You don't need a separate import for the Python side; just use `import QtQuick.Shapes` in QML.

4. **Running scripts**: Use `uv run --no-project python3 <script>` to run Python scripts that use these modules in the current uv environment.

## Verification

Run the verification script to confirm all components:

```bash
uv run --no-project python3 scripts/verify_qt_components.py
```

## Documentation Links

- [PySide6 API Reference](https://doc.qt.io/qtforpython-6/api.html)
- [Qt 6 Documentation](https://doc.qt.io/qt-6/)
- [Qt for Python (PySide6) Getting Started](https://doc.qt.io/qtforpython-6/gettingstarted.html)
