#!/usr/bin/env python3
"""
Star Trek Retro Remake - Compatibility Layer

Description:
    Compatibility layer for Python 3.11+ features and external dependencies.
    Provides a single import point for tomllib/tomli compatibility.

Author: Star Trek Retro Remake Development Team
Email: development@star-trek-retro-remake.org
GitHub: https://github.com/L3DigitalNet/Star-Trek-Retro-Remake
Date Created: 11-01-2025
Date Changed: 11-01-2025
License: MIT

Features:
    - Single import point for TOML reading (tomllib/tomli compatibility)
    - Eliminates try/except import duplication across codebase
    - Simplified future migration when Python 3.14+ is minimum

Requirements:
    - Python 3.14+ for tomllib in standard library
    - tomli as fallback for older Python versions (not needed for this project)

Known Issues:
    - None

Planned Features:
    - Additional compatibility shims as needed

Classes:
    - None

Functions:
    - None
"""

from typing import Final

__version__: Final[str] = "0.0.29"

# Import tomllib from stdlib (Python 3.14+ guaranteed for this project)
import tomllib

__all__ = ["tomllib"]
