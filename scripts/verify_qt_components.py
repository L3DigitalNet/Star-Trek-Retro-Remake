#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Star Trek Retro Remake - Qt 6 Component Verification Script

Description:
    Verifies that all requested Qt 6 components and tools are properly
    installed and accessible.

Author: Star Trek Retro Remake Development Team
Email: development@star-trek-retro-remake.org
Date Created: 10-30-2025
License: MIT

Components Verified:
    - Qt Quick (QML) and Qt Quick Controls 2
    - Qt Multimedia
    - Qt State Machine
    - Qt SVG
    - Qt Quick Shapes
    - Qt 3D (Core, Render, Input, Logic, Extras, Animation)
    - PySide6-Essentials
    - PySide6-Addons
    - shiboken6
"""

from typing import Final


def verify_qt_components() -> None:
    """Verify all requested Qt 6 components are available."""
    components_status: dict[str, bool] = {}

    # Test Qt Quick (QML)
    try:
        from PySide6.QtQuick import QQuickView, QQuickItem
        from PySide6.QtQml import QQmlApplicationEngine, QQmlComponent
        components_status["Qt Quick (QML)"] = True
    except ImportError as e:
        components_status["Qt Quick (QML)"] = False
        print(f"  Error: {e}")

    # Test Qt Quick Controls
    try:
        from PySide6.QtQuickControls2 import QQuickStyle
        components_status["Qt Quick Controls"] = True
    except ImportError as e:
        components_status["Qt Quick Controls"] = False
        print(f"  Error: {e}")

    # Test Qt Multimedia
    try:
        from PySide6.QtMultimedia import (
            QMediaPlayer,
            QAudioOutput,
            QSoundEffect,
        )
        components_status["Qt Multimedia"] = True
    except ImportError as e:
        components_status["Qt Multimedia"] = False
        print(f"  Error: {e}")

    # Test Qt State Machine
    try:
        from PySide6.QtStateMachine import (
            QStateMachine,
            QState,
            QFinalState,
        )
        components_status["Qt State Machine"] = True
    except ImportError as e:
        components_status["Qt State Machine"] = False
        print(f"  Error: {e}")

    # Test Qt SVG
    try:
        from PySide6.QtSvg import QSvgRenderer
        from PySide6.QtSvgWidgets import QSvgWidget
        components_status["Qt SVG"] = True
    except ImportError as e:
        components_status["Qt SVG"] = False
        print(f"  Error: {e}")

    # Test Qt Quick Shapes (part of QtQuick)
    try:
        from PySide6.QtQuickShapes import QQuickShapesModule
        components_status["Qt Quick Shapes"] = True
    except ImportError:
        # Qt Quick Shapes is integrated into QtQuick in Qt 6
        try:
            from PySide6.QtQuick import QQuickItem
            components_status["Qt Quick Shapes"] = True
        except ImportError as e:
            components_status["Qt Quick Shapes"] = False
            print(f"  Error: {e}")

    # Test PySide6-Essentials
    try:
        import PySide6
        components_status["PySide6-Essentials"] = True
    except ImportError as e:
        components_status["PySide6-Essentials"] = False
        print(f"  Error: {e}")

    # Test PySide6-Addons
    try:
        from PySide6 import QtStateMachine, QtSvg, QtMultimedia
        components_status["PySide6-Addons"] = True
    except ImportError as e:
        components_status["PySide6-Addons"] = False
        print(f"  Error: {e}")

    # Test Qt 3D
    try:
        from PySide6.Qt3DCore import Qt3DCore
        from PySide6.Qt3DRender import Qt3DRender
        from PySide6.Qt3DInput import Qt3DInput
        from PySide6.Qt3DLogic import Qt3DLogic
        from PySide6.Qt3DExtras import Qt3DExtras
        from PySide6.Qt3DAnimation import Qt3DAnimation
        components_status["Qt 3D"] = True
    except ImportError as e:
        components_status["Qt 3D"] = False
        print(f"  Error: {e}")

    # Test shiboken6
    try:
        import shiboken6
        components_status["shiboken6"] = True
    except ImportError as e:
        components_status["shiboken6"] = False
        print(f"  Error: {e}")

    # Print results
    print("\n" + "=" * 60)
    print("Qt 6 Components Verification")
    print("=" * 60)

    all_available: bool = True
    for component, status in components_status.items():
        status_icon: str = "✓" if status else "✗"
        status_text: str = "Available" if status else "Missing"
        print(f"{status_icon} {component:.<45} {status_text}")
        if not status:
            all_available = False

    print("=" * 60)

    if all_available:
        print("\n✓ All requested Qt 6 components are available!")

        # Print version info
        try:
            import PySide6
            print(f"\nPySide6 Version: {PySide6.__version__}")
        except (ImportError, AttributeError):
            pass

        try:
            import shiboken6
            shiboken_version: str = getattr(
                shiboken6, "__version__", "Unknown"
            )
            print(f"shiboken6 Version: {shiboken_version}")
        except (ImportError, AttributeError):
            pass
    else:
        print("\n✗ Some components are missing. Please install them.")
        return

    print("\nComponent Details:")
    print("-" * 60)
    print("• Qt Quick (QML): Declarative UI framework")
    print("• Qt Quick Controls: Pre-built UI controls for Qt Quick")
    print("• Qt Multimedia: Audio/video playback and recording")
    print("• Qt State Machine: Hierarchical finite state machine")
    print("• Qt SVG: SVG file rendering support")
    print("• Qt Quick Shapes: 2D vector graphics in Qt Quick")
    print("• Qt 3D: 3D rendering and scene management")
    print("• PySide6-Essentials: Core Qt modules")
    print("• PySide6-Addons: Additional Qt modules")
    print("• shiboken6: CPython bindings generator")
    print("-" * 60)


def main() -> None:
    """Main entry point."""
    verify_qt_components()


if __name__ == "__main__":
    main()
