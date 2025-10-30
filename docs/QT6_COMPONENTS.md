# Qt 6 Components Reference

## Installed Components

All requested Qt 6 components are installed and available (version 6.10.0):

- ✓ Qt Quick (QML) - `PySide6.QtQuick`
- ✓ Qt Quick Controls 2 - `PySide6.QtQuickControls2`
- ✓ Qt Multimedia - `PySide6.QtMultimedia`
- ✓ Qt State Machine - `PySide6.QtStateMachine`
- ✓ Qt SVG - `PySide6.QtSvg`
- ✓ Qt Quick Shapes - Integrated in `PySide6.QtQuick`
- ✓ Qt 3D - `PySide6.Qt3DCore`, `Qt3DRender`, `Qt3DInput`, etc.
- ✓ PySide6-Essentials (Core Qt modules)
- ✓ PySide6-Addons (Additional Qt modules)
- ✓ shiboken6 (CPython bindings generator)

### Module Mapping

Python packages vs Qt C++ libraries:

| Python Module | Qt C++ Library | Description |
|--------------|----------------|-------------|
| `PySide6.QtQuick` | qt6-quick | QML/declarative UI |
| `PySide6.QtQuickControls2` | qt6-quickcontrols2 | UI controls |
| `PySide6.QtMultimedia` | qt6-multimedia | Audio/video |
| `PySide6.QtStateMachine` | qt6-statemachine | State machines |
| `PySide6.QtSvg` | qt6-svg | SVG rendering |
| `PySide6.Qt3D*` | qt6-3d | 3D rendering |

## Usage Examples

### Qt Quick (QML)

```python
from PySide6.QtQuick import QQuickView, QQuickItem
from PySide6.QtQml import QQmlApplicationEngine, QQmlComponent
from PySide6.QtCore import QUrl

# Create QML engine
engine = QQmlApplicationEngine()
engine.load(QUrl.fromLocalFile("main.qml"))
```

### Qt Quick Controls

```python
from PySide6.QtQuickControls2 import QQuickStyle

# Set application style
QQuickStyle.setStyle("Material")  # or "Fusion", "Imagine", etc.
```

### Qt Multimedia

```python
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput, QSoundEffect
from PySide6.QtCore import QUrl

# Audio playback
player = QMediaPlayer()
audio_output = QAudioOutput()
player.setAudioOutput(audio_output)
player.setSource(QUrl.fromLocalFile("sound.mp3"))
player.play()

# Sound effects
effect = QSoundEffect()
effect.setSource(QUrl.fromLocalFile("effect.wav"))
effect.play()
```

### Qt State Machine

```python
from PySide6.QtStateMachine import QStateMachine, QState, QFinalState
from PySide6.QtCore import QObject

# Create state machine for game states
machine = QStateMachine()

# Define states
main_menu = QState(machine)
galaxy_map = QState(machine)
sector_map = QState(machine)
combat = QState(machine)
final = QFinalState(machine)

# Set initial state
machine.setInitialState(main_menu)

# Add transitions
main_menu.addTransition(galaxy_map)
galaxy_map.addTransition(sector_map)
sector_map.addTransition(combat)

# Start machine
machine.start()
```

### Qt SVG

```python
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtCore import QByteArray

# Render SVG
renderer = QSvgRenderer()
renderer.load("image.svg")

# Display SVG widget
widget = QSvgWidget()
widget.load("image.svg")
widget.show()
```

### Qt Quick Shapes

```python
# Qt Quick Shapes is integrated into QtQuick in Qt 6
from PySide6.QtQuick import QQuickItem

# Use in QML:
"""
import QtQuick
import QtQuick.Shapes

Shape {
    ShapePath {
        strokeWidth: 4
        strokeColor: "red"
        fillColor: "transparent"
        PathLine { x: 100; y: 0 }
        PathLine { x: 100; y: 100 }
        PathLine { x: 0; y: 100 }
        PathLine { x: 0; y: 0 }
    }
}
"""
```

### Qt 3D

```python
from PySide6.Qt3DCore import Qt3DCore
from PySide6.Qt3DRender import Qt3DRender, QCamera, QMesh
from PySide6.Qt3DInput import Qt3DInput
from PySide6.Qt3DLogic import Qt3DLogic
from PySide6.Qt3DExtras import (
    Qt3DWindow,
    QFirstPersonCameraController,
    QPhongMaterial,
)
from PySide6.Qt3DAnimation import Qt3DAnimation
from PySide6.QtCore import Qt
from PySide6.QtGui import QVector3D

# Create 3D window
view = Qt3DWindow()
view.defaultFrameGraph().setClearColor(Qt.black)

# Root entity
root_entity = Qt3DCore.QEntity()

# Camera setup
camera = view.camera()
camera.lens().setPerspectiveProjection(45.0, 16.0 / 9.0, 0.1, 1000.0)
camera.setPosition(QVector3D(0, 0, 20.0))
camera.setViewCenter(QVector3D(0, 0, 0))

# Camera controller
cam_controller = QFirstPersonCameraController(root_entity)
cam_controller.setCamera(camera)

# 3D mesh
mesh = QMesh()
mesh.setSource(QUrl.fromLocalFile("spaceship.obj"))

# Material
material = QPhongMaterial()
material.setDiffuse(QColor(0, 120, 255))

# Entity
entity = Qt3DCore.QEntity(root_entity)
entity.addComponent(mesh)
entity.addComponent(material)

# Set root and show
view.setRootEntity(root_entity)
view.show()
```

## Integration with Game Architecture

### Using Qt State Machine for Game States

The Qt State Machine can be used alongside the game's existing state machine:

```python
from PySide6.QtStateMachine import QStateMachine, QState
from game.states.state_machine import GameState

# UI state machine (PySide6)
ui_machine = QStateMachine()

# Game logic state machine (custom)
game_state = GameState.MAIN_MENU

# Sync states between UI and game logic
```

### Using Qt Quick for Menus and Dialogs

Qt Quick (QML) is ideal for the UI layer while keeping game logic separate:

```python
# MVC Architecture maintained:
# - Model: game/model.py (game logic)
# - View: Qt Quick QML files (UI/menus)
# - Controller: game/controller.py (input handling)
```

### Using Qt Multimedia for Audio

Replace or complement PyGame's audio with Qt Multimedia:

```python
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput

class AudioManager:
    def __init__(self) -> None:
        self.music_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.music_player.setAudioOutput(self.audio_output)

    def play_music(self, file_path: str) -> None:
        self.music_player.setSource(QUrl.fromLocalFile(file_path))
        self.music_player.play()
```

## Running Scripts with Qt Components

Use `uv run --no-project` to run Python scripts that use these components:

```bash
uv run --no-project python3 scripts/verify_qt_components.py
```

## Verification

To verify all components are installed correctly:

```bash
uv run --no-project python3 scripts/verify_qt_components.py
```

## Dependencies in pyproject.toml

```toml
dependencies = [
    "pygame>=2.5.0",
    "PySide6>=6.10.0",
    "PySide6-Essentials>=6.10.0",
    "PySide6-Addons>=6.10.0",
    "shiboken6>=6.10.0",
    "tomli-w>=1.0.0",
]
```

### Using Qt 3D for Space Visualization

Qt 3D can visualize 3D space sectors alongside the 2D grid-based game logic:

```python
# Game logic (3D grid coordinates)
ship_position: tuple[int, int, int] = (10, 5, 2)  # x, y, z

# Qt 3D visualization (transform to 3D scene)
from PySide6.QtGui import QVector3D
from PySide6.Qt3DCore import QTransform

transform = QTransform()
transform.setTranslation(QVector3D(ship_position[0], ship_position[1], ship_position[2]))
ship_entity.addComponent(transform)
```

## Additional Resources

- [PySide6 Documentation](https://doc.qt.io/qtforpython-6/)
- [Qt Quick Documentation](https://doc.qt.io/qt-6/qtquick-index.html)
- [Qt Quick Controls Documentation](https://doc.qt.io/qt-6/qtquickcontrols-index.html)
- [Qt Multimedia Documentation](https://doc.qt.io/qt-6/qtmultimedia-index.html)
- [Qt State Machine Documentation](https://doc.qt.io/qt-6/qtstatemachine-index.html)
- [Qt SVG Documentation](https://doc.qt.io/qt-6/qtsvg-index.html)
- [Qt 3D Documentation](https://doc.qt.io/qt-6/qt3d-index.html)
- [Qt Quick Shapes Documentation](https://doc.qt.io/qt-6/qtquick-shapes-qmlmodule.html)
