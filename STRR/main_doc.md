# Main Entry Point Documentation

**File:** `STRR/main.py`
**Version:** 0.0.10
**Last Updated:** 10-30-2025

---

## Purpose

The `main.py` file is the **primary entry point** for the Star Trek Retro Remake game application. When you run the game, this is where execution begins. Its responsibilities are:

- Configure the Python import path for the `src/` directory
- Import the main application class
- Create and launch the game application
- Provide the standard `if __name__ == "__main__"` entry point

This is a **thin bootstrapping layer** that sets up the environment and delegates to the actual application implementation.

---

## Architecture

### Bootstrap Pattern

This file follows the **Bootstrap Pattern** - it's kept minimal and focused solely on:

1. **Environment setup** (Python path configuration)
2. **Application instantiation** (creating the game object)
3. **Application execution** (starting the game loop)

The actual game logic lives in `src/game/application.py` and other modules.

### Import Path Configuration

```python
sys.path.insert(0, str(Path(__file__).parent / "src"))
```

This line is critical - it adds the `STRR/src/` directory to Python's module search path, allowing imports like:

```python
from src.game.application import StarTrekRetroRemake
```

Without this, Python wouldn't find the `src` package.

---

## Functions

### main() -> None

**Purpose:** Primary entry point that launches the game

**Parameters:** None

**Returns:** None

**Behavior:**

1. Creates an instance of `StarTrekRetroRemake` (the main application class)
2. Calls the `run()` method to start the game loop
3. Blocks until the game exits

**Example:**

```python
def main() -> None:
    """
    Main entry point for the Star Trek Retro Remake game.

    Initializes the game application and starts the main game loop.
    """
    # Create and run the game application
    game = StarTrekRetroRemake()
    game.run()
```

---

## Usage Examples

### Example 1: Running the Game

From the command line:

```bash
cd /path/to/Star-Trek-Retro-Remake/STRR
python main.py
```

Or using the shebang:

```bash
./main.py  # If executable permission is set
```

### Example 2: Running with Python Module Syntax

```bash
cd /path/to/Star-Trek-Retro-Remake
python -m STRR.main
```

### Example 3: Programmatic Launch

```python
from STRR.main import main

# Launch the game programmatically
main()
```

### Example 4: Adding Command-Line Arguments

To extend with argument parsing:

```python
import argparse

def main() -> None:
    """Main entry point with argument parsing."""
    parser = argparse.ArgumentParser(description="Star Trek Retro Remake")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("--fullscreen", action="store_true", help="Start in fullscreen")
    args = parser.parse_args()

    # Create and configure game
    game = StarTrekRetroRemake()
    if args.debug:
        game.enable_debug_mode()
    if args.fullscreen:
        game.set_fullscreen(True)

    # Run the game
    game.run()
```

---

## Integration Points

### Dependencies

**Standard library:**

- `sys` - Used for Python path manipulation
- `pathlib.Path` - Modern path handling
- `typing.Final` - Type annotation for constants

**Project modules:**

- `src.game.application.StarTrekRetroRemake` - Main application class

**Why these dependencies:**

- `sys.path` manipulation is required to make `src/` importable
- `Path` provides cross-platform path handling
- `StarTrekRetroRemake` is the core application that this file launches

### Used By

**Direct execution:**

- Command line: `python main.py`
- Shell scripts: `./scripts/run_game.sh`
- IDE run configurations

**Package tools:**

- Entry point in `pyproject.toml` (if configured)
- Desktop launcher scripts

---

## Configuration

### Environment Requirements

- **Python:** 3.14+ (uses modern type hints and stdlib features)
- **Platform:** Linux only (not compatible with Windows or macOS)
- **Dependencies:** pygame-ce (Community Edition), PySide6 (installed in virtual environment)

### Path Structure

The file assumes this directory structure:

```
STRR/
├── main.py              ← This file
└── src/
    └── game/
        └── application.py
```

If `src/` is moved or renamed, update the path configuration.

---

## Common Patterns

### Pattern 1: Entry Point with Error Handling

```python
def main() -> None:
    """Main entry point with error handling."""
    try:
        game = StarTrekRetroRemake()
        game.run()
    except KeyboardInterrupt:
        print("\nGame interrupted by user")
    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
```

### Pattern 2: Entry Point with Logging

```python
import logging

def main() -> None:
    """Main entry point with logging setup."""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    logger = logging.getLogger(__name__)
    logger.info("Starting Star Trek Retro Remake")

    # Create and run game
    game = StarTrekRetroRemake()
    game.run()

    logger.info("Game shutdown complete")
```

### Pattern 3: Development vs Production

```python
import os

def main() -> None:
    """Main entry point with environment-based behavior."""
    # Check environment
    is_dev = os.getenv("STRR_ENV") == "development"

    # Create game with appropriate settings
    game = StarTrekRetroRemake()

    if is_dev:
        game.enable_debug_mode()
        game.enable_hot_reload()

    game.run()
```

---

## Troubleshooting

### Issue: ImportError - No module named 'src'

**Symptom:** `ImportError: No module named 'src'` or `ModuleNotFoundError: No module named 'src'`

**Cause:** Python path not set up correctly

**Solution:** Ensure the path manipulation code is present:

```python
sys.path.insert(0, str(Path(__file__).parent / "src"))
```

### Issue: Game doesn't start, no error message

**Symptom:** Running `main.py` does nothing or exits immediately

**Cause:** Exception silently caught or application not calling `run()`

**Solution:** Add error handling and print statements:

```python
def main() -> None:
    print("Starting game...")
    try:
        game = StarTrekRetroRemake()
        print("Game object created, starting loop...")
        game.run()
    except Exception as e:
        print(f"Error: {e}")
        raise
```

### Issue: Wrong Python version

**Symptom:** Syntax errors or "invalid syntax" messages

**Cause:** Running with Python < 3.14

**Solution:** Check Python version:

```bash
python --version  # Should be 3.14+
python3.14 main.py  # Use specific version
```

### Issue: Display/Graphics errors on startup

**Symptom:** pygame-ce or display-related errors

**Cause:** Missing display environment (especially when SSH'd into a machine)

**Solution:** Ensure X11 display is available or run in virtual display:

```bash
# Check display
echo $DISPLAY

# Use virtual display (if needed)
xvfb-run python main.py
```

---

## Notes

### Why Keep This File Simple?

The main entry point is intentionally minimal for several reasons:

1. **Clarity:** Easy to understand what happens when the game starts
2. **Maintainability:** Logic lives in the appropriate modules, not scattered in the entry point
3. **Testability:** Complex logic in `application.py` can be tested without running the full application
4. **Flexibility:** Easy to add CLI arguments, logging, or other startup behavior later

### Alternative Entry Points

For development, you might create additional entry points:

- `dev_main.py` - Development mode with debug features
- `test_main.py` - Test harness entry point
- `profile_main.py` - Performance profiling entry point

### Package Installation

If the game is installed as a package, you can define a console entry point in `pyproject.toml`:

```toml
[project.scripts]
strr = "STRR.main:main"
```

Then users can run: `strr` instead of `python main.py`

---

## Change History

- **10-30-2025** - Updated documentation to version 0.0.10, clarified Linux-only compatibility, enhanced inline comments
- **10-30-2025** - Initial documentation created
- **10-29-2025** - File created with basic entry point implementation
