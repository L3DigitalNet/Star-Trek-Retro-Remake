#!/usr/bin/env python3
"""
Tests for engine compatibility layer.

Description:
    Tests for the compat.py module that provides compatibility shims
    for Python 3.11+ features and external dependencies.

Author: Star Trek Retro Remake Development Team  
Email: development@star-trek-retro-remake.org
Date Created: 11-01-2025
Date Changed: 11-01-2025
License: MIT
"""

import pytest


class TestCompatModule:
    """Test compatibility layer module."""

    def test_tomllib_import(self):
        """Test that tomllib can be imported from compat module."""
        # Arrange & Act
        from src.engine.compat import tomllib

        # Assert
        assert tomllib is not None

    def test_tomllib_has_load_method(self):
        """Test that tomllib has the load method."""
        # Arrange
        from src.engine.compat import tomllib

        # Act & Assert
        assert hasattr(tomllib, "load")
        assert callable(tomllib.load)

    def test_tomllib_has_loads_method(self):
        """Test that tomllib has the loads method."""
        # Arrange
        from src.engine.compat import tomllib

        # Act & Assert
        assert hasattr(tomllib, "loads")
        assert callable(tomllib.loads)

    def test_tomllib_can_parse_simple_toml(self):
        """Test that tomllib can parse simple TOML content."""
        # Arrange
        from src.engine.compat import tomllib

        toml_content = """
        [section]
        key = "value"
        number = 42
        """

        # Act
        result = tomllib.loads(toml_content)

        # Assert
        assert result["section"]["key"] == "value"
        assert result["section"]["number"] == 42

    def test_module_has_version(self):
        """Test that compat module has version attribute."""
        # Arrange & Act
        from src.engine import compat

        # Assert
        assert hasattr(compat, "__version__")
        assert isinstance(compat.__version__, str)

    def test_module_exports(self):
        """Test that compat module exports tomllib in __all__."""
        # Arrange & Act
        from src.engine import compat

        # Assert
        assert hasattr(compat, "__all__")
        assert "tomllib" in compat.__all__
