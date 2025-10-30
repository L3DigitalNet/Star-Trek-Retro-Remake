#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Star Trek Retro Remake - UI Compiler Script

Description:
    Compiles Qt Designer .ui files to Python .py files.
    This is an optional workflow - the application can load .ui files directly.

Usage:
    python scripts/compile_ui.py              # Compile all .ui files
    python scripts/compile_ui.py main_window  # Compile specific file

Author: Star Trek Retro Remake Development Team
Email: development@star-trek-retro-remake.org
GitHub: https://github.com/L3DigitalNet/Star-Trek-Retro-Remake
Date Created: 10-30-2025
Date Changed: 10-30-2025
License: MIT
"""

import sys
from pathlib import Path
from typing import Final

__version__: Final[str] = "0.0.1"


def compile_ui_file(ui_file: Path, output_dir: Path) -> bool:
    """
    Compile a single .ui file to Python.

    Args:
        ui_file: Path to .ui file
        output_dir: Directory for output .py file

    Returns:
        True if successful, False otherwise
    """
    try:
        # Import PySide6 UI compiler
        from PySide6.QtUiTools import QUiLoader
        import subprocess

        # Use pyside6-uic command line tool
        output_file = output_dir / f"{ui_file.stem}_ui.py"

        result = subprocess.run(
            ["pyside6-uic", str(ui_file), "-o", str(output_file)],
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            print(f"✓ Compiled: {ui_file.name} -> {output_file.name}")
            return True
        else:
            print(f"✗ Failed to compile {ui_file.name}:")
            print(result.stderr)
            return False

    except ImportError:
        print("Error: PySide6 not installed. Install with: pip install PySide6")
        return False
    except FileNotFoundError:
        print("Error: pyside6-uic not found. Ensure PySide6 is properly installed.")
        return False
    except Exception as e:
        print(f"Error compiling {ui_file.name}: {e}")
        return False


def compile_all_ui_files(ui_dir: Path, output_dir: Path) -> tuple[int, int]:
    """
    Compile all .ui files in a directory.

    Args:
        ui_dir: Directory containing .ui files
        output_dir: Directory for output .py files

    Returns:
        Tuple of (successful_count, failed_count)
    """
    ui_files = list(ui_dir.glob("*.ui"))

    if not ui_files:
        print(f"No .ui files found in {ui_dir}")
        return 0, 0

    print(f"Found {len(ui_files)} .ui file(s) to compile\n")

    successful = 0
    failed = 0

    for ui_file in ui_files:
        if compile_ui_file(ui_file, output_dir):
            successful += 1
        else:
            failed += 1

    return successful, failed


def main() -> int:
    """
    Main entry point for UI compilation script.

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    # Get project root directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    # Define paths
    ui_dir = project_root / "STRR" / "src" / "ui" / "designer"
    output_dir = project_root / "STRR" / "src" / "ui" / "compiled"

    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("Star Trek Retro Remake - UI Compiler")
    print("=" * 60)
    print(f"UI Directory: {ui_dir}")
    print(f"Output Directory: {output_dir}")
    print("=" * 60 + "\n")

    # Check for specific file argument
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        if not filename.endswith(".ui"):
            filename += ".ui"

        ui_file = ui_dir / filename

        if not ui_file.exists():
            print(f"Error: File not found: {ui_file}")
            return 1

        success = compile_ui_file(ui_file, output_dir)
        return 0 if success else 1

    # Compile all .ui files
    successful, failed = compile_all_ui_files(ui_dir, output_dir)

    print("\n" + "=" * 60)
    print(f"Compilation complete: {successful} successful, {failed} failed")
    print("=" * 60)

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
