# Scripts Directory

This directory contains utility scripts for development, testing, and build processes for the Star Trek Retro Remake project.

## Files

### compile_ui.py

**Purpose:** Compiles Qt Designer `.ui` files to Python `.py` files

**Description:**
Utility script for converting Qt Designer UI files to Python code. This is an optional workflow - the application can load `.ui` files directly at runtime using `QUiLoader`. Compilation provides slightly better performance and eliminates the need for runtime parsing.

**Usage:**

```bash
# Compile all .ui files
python scripts/compile_ui.py

# Compile specific file
python scripts/compile_ui.py main_window
```

**Input:** `.ui` files from `STRR/src/ui/designer/`
**Output:** `.py` files to `STRR/src/ui/compiled/`

**Version:** 0.0.1
**Linux Only:** Yes

---

### verify_qt_components.py

**Purpose:** Verifies Qt 6 component installation and accessibility

**Description:**
Development utility that checks whether all required Qt 6 components and PySide6 modules are properly installed and importable. Reports which components are available and which are missing. Useful for debugging environment setup issues.

**Usage:**

```bash
python scripts/verify_qt_components.py
```

**Verified Components:**

- Qt Quick (QML) and Qt Quick Controls 2
- Qt Multimedia
- Qt State Machine
- Qt SVG
- Qt Quick Shapes
- Qt 3D (Core, Render, Input, Logic, Extras, Animation)
- PySide6-Essentials
- PySide6-Addons
- shiboken6

**Output:** Console report with component status (✓ available or ✗ missing)

**Version:** 0.0.1
**Linux Only:** Yes

---

### dev_setup.sh

**Purpose:** Automated development environment setup

**Description:**
Bash script that sets up the complete development environment for the project. Installs all dependencies, configures pre-commit hooks, and creates necessary directory structure.

**Usage:**

```bash
# Make executable (if needed)
chmod +x scripts/dev_setup.sh

# Run setup
./scripts/dev_setup.sh
```

**Actions Performed:**

1. Checks Python version (requires 3.14+)
2. Installs package in editable mode with dev dependencies
3. Installs pre-commit hooks
4. Creates necessary directories:
   - `star_trek_retro_remake/logs/`
   - `star_trek_retro_remake/saves/`
   - `star_trek_retro_remake/screenshots/`

**Requirements:**

- Bash shell
- Python 3.14+ installed
- pip package manager

**Output:** Console messages showing setup progress

**Linux Only:** Yes

---

### run_tests.sh

**Purpose:** Runs the test suite with coverage reporting

**Description:**
Bash script that executes the complete pytest test suite with coverage analysis. Generates both terminal output and HTML coverage reports for detailed analysis.

**Usage:**

```bash
# Make executable (if needed)
chmod +x scripts/run_tests.sh

# Run tests
./scripts/run_tests.sh
```

**Actions Performed:**

1. Changes to project directory
2. Runs pytest with coverage tracking
3. Generates terminal coverage report
4. Generates HTML coverage report

**Output:**

- Console test results with coverage summary
- `htmlcov/index.html` - Detailed coverage report

**View Coverage:**

```bash
# Open coverage report in browser
xdg-open htmlcov/index.html
```

**Requirements:**

- Bash shell
- pytest installed
- pytest-cov installed

**Linux Only:** Yes

---

## Common Workflows

### Initial Setup

```bash
# 1. Setup development environment
./scripts/dev_setup.sh

# 2. Verify Qt components
python scripts/verify_qt_components.py

# 3. Run tests to verify installation
./scripts/run_tests.sh
```

### UI Development

```bash
# 1. Design UI in Qt Designer (edit .ui files)

# 2. Optional: Compile UI files to Python
python scripts/compile_ui.py

# 3. Run application to test UI changes
make run
```

### Testing Workflow

```bash
# Run tests with coverage
./scripts/run_tests.sh

# View detailed coverage report
xdg-open htmlcov/index.html

# Make changes based on coverage gaps

# Re-run tests
./scripts/run_tests.sh
```

## Development Commands

These scripts complement the Makefile commands:

```bash
make test       # Run tests (uses pytest directly)
make test-cov   # Run tests with coverage (similar to run_tests.sh)
make lint       # Run linting checks
make format     # Format code
make run        # Run the game
make clean      # Clean build artifacts
```

## Linux Compatibility

All scripts are designed for Linux environments:

- Bash scripts use `#!/bin/bash` shebang
- Python scripts use `#!/usr/bin/env python3` shebang
- Path handling uses pathlib for Linux compatibility
- No Windows-specific commands or paths

**System Requirements:**

- Linux operating system
- Bash shell
- Python 3.14+
- pip package manager
- xdg-utils (for opening HTML reports)

## Adding New Scripts

When adding new scripts to this directory:

1. **Use proper shebang**: `#!/bin/bash` or `#!/usr/bin/env python3`
2. **Make executable**: `chmod +x scripts/your_script.sh`
3. **Add documentation header**: Include purpose, usage, description
4. **Update this README**: Add entry documenting the new script
5. **Linux only**: Ensure script works on Linux systems
6. **Test thoroughly**: Verify script works in clean environment

## Related Documentation

- **Qt Designer Workflow**: `/docs/QT_DESIGNER_WORKFLOW.md`
- **Development Setup**: `README.md` (root)
- **Testing**: `STRR/tests/` directory
- **Build System**: `Makefile` in root directory
