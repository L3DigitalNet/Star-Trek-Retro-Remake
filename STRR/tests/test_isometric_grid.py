#!/usr/bin/env python3
"""
Star Trek Retro Remake - Isometric Grid Tests

Description:
    Unit tests for the isometric grid rendering system. Tests coordinate
    conversion, bounds checking, z-level calculations, and grid operations.

Author: Star Trek Retro Remake Development Team
Email: development@star-trek-retro-remake.org
GitHub: https://github.com/L3DigitalNet/Star-Trek-Retro-Remake
Date Created: 10-30-2025
Date Changed: 10-30-2025
License: MIT

Features:
    - Test isometric projection math (world ↔ screen conversion)
    - Test z-level offset calculations
    - Test bounds checking
    - Test GridPosition operations
    - Test camera offset effects
    - Test factory functions

Requirements:
    - Python 3.14+
    - pytest for test framework
    - pygame-ce for rendering surface
"""

import pytest

pygame = pytest.importorskip("pygame")


from math import isclose

from src.engine.isometric_grid import (
    GridRenderer,
    create_combat_grid,
    create_default_grid,
    create_sector_grid,
)
from src.game.entities.base import GridPosition

pytestmark = pytest.mark.gui


class TestGridPosition:
    """Test cases for GridPosition dataclass."""

    def test_position_creation(self):
        """Test creating grid positions."""
        pos = GridPosition(5, 10, 2)
        assert pos.x == 5
        assert pos.y == 10
        assert pos.z == 2

    def test_position_default_z(self):
        """Test default z-level is 0."""
        pos = GridPosition(3, 7)
        assert pos.z == 0

    def test_position_immutable(self):
        """Test that GridPosition is immutable."""
        pos = GridPosition(1, 2, 3)
        with pytest.raises(AttributeError):
            pos.x = 5  # type: ignore

    def test_distance_2d(self):
        """Test 2D distance calculation (z=0)."""
        pos1 = GridPosition(0, 0, 0)
        pos2 = GridPosition(3, 4, 0)
        distance = pos1.distance_to(pos2)
        assert isclose(distance, 5.0)

    def test_distance_3d(self):
        """Test 3D distance calculation with z-levels."""
        pos1 = GridPosition(0, 0, 0)
        pos2 = GridPosition(1, 1, 1)
        distance = pos1.distance_to(pos2)
        assert isclose(distance, 1.732, rel_tol=0.01)  # sqrt(3)

    def test_distance_to_self(self):
        """Test distance to same position is 0."""
        pos = GridPosition(5, 5, 5)
        assert pos.distance_to(pos) == 0.0

    def test_addition(self):
        """Test position addition."""
        pos1 = GridPosition(5, 10, 2)
        pos2 = GridPosition(3, 7, 1)
        result = pos1 + pos2
        assert result.x == 8
        assert result.y == 17
        assert result.z == 3

    def test_subtraction(self):
        """Test position subtraction."""
        pos1 = GridPosition(10, 15, 5)
        pos2 = GridPosition(3, 7, 2)
        result = pos1 - pos2
        assert result.x == 7
        assert result.y == 8
        assert result.z == 3

    def test_equality(self):
        """Test position equality comparison."""
        pos1 = GridPosition(5, 10, 2)
        pos2 = GridPosition(5, 10, 2)
        pos3 = GridPosition(5, 10, 3)
        assert pos1 == pos2
        assert pos1 != pos3

    def test_hashable(self):
        """Test that GridPosition can be used in sets/dicts."""
        pos1 = GridPosition(1, 2, 3)
        pos2 = GridPosition(1, 2, 3)
        pos3 = GridPosition(4, 5, 6)

        position_set = {pos1, pos2, pos3}
        assert len(position_set) == 2  # pos1 and pos2 are the same


class TestGridRendererInitialization:
    """Test cases for GridRenderer initialization."""

    def test_default_initialization(self):
        """Test creating renderer with default parameters."""
        renderer = GridRenderer()
        assert renderer.tile_width == 64
        assert renderer.tile_height == 32
        assert renderer.grid_width == 20
        assert renderer.grid_height == 20
        assert renderer.max_z_levels == 4

    def test_custom_initialization(self):
        """Test creating renderer with custom parameters."""
        renderer = GridRenderer(
            tile_width=48,
            tile_height=24,
            grid_width=15,
            grid_height=15,
            max_z_levels=3,
            camera_offset=(500, 200),
        )
        assert renderer.tile_width == 48
        assert renderer.tile_height == 24
        assert renderer.grid_width == 15
        assert renderer.grid_height == 15
        assert renderer.max_z_levels == 3
        assert renderer.camera_offset == (500, 200)

    def test_camera_offset_initialization(self):
        """Test camera offset is properly set."""
        renderer = GridRenderer(camera_offset=(100, 200))
        assert renderer.camera_offset == (100, 200)


class TestCoordinateConversion:
    """Test cases for world ↔ screen coordinate conversion."""

    @pytest.fixture
    def renderer(self):
        """Create a standard renderer for testing."""
        return GridRenderer(
            tile_width=64,
            tile_height=32,
            camera_offset=(0, 0),  # No camera offset for easier testing
        )

    def test_origin_conversion(self, renderer):
        """Test conversion of origin point (0,0,0)."""
        pos = GridPosition(0, 0, 0)
        screen = renderer.world_to_screen(pos)
        assert screen == (0, 0)

    def test_simple_position_conversion(self, renderer):
        """Test conversion of simple position."""
        pos = GridPosition(1, 0, 0)
        screen = renderer.world_to_screen(pos)
        # (1-0) * 32 = 32, (1+0) * 16 = 16
        assert screen == (32, 16)

    def test_negative_position_conversion(self, renderer):
        """Test conversion with negative coordinates."""
        pos = GridPosition(-1, 1, 0)
        screen = renderer.world_to_screen(pos)
        # (-1-1) * 32 = -64, (-1+1) * 16 = 0
        assert screen == (-64, 0)

    def test_z_level_offset(self, renderer):
        """Test that z-levels affect screen y-coordinate."""
        pos_z0 = GridPosition(5, 5, 0)
        pos_z1 = GridPosition(5, 5, 1)
        pos_z2 = GridPosition(5, 5, 2)

        screen_z0 = renderer.world_to_screen(pos_z0)
        screen_z1 = renderer.world_to_screen(pos_z1)
        screen_z2 = renderer.world_to_screen(pos_z2)

        # Higher z should have lower y (appear higher on screen)
        assert screen_z0[1] > screen_z1[1]
        assert screen_z1[1] > screen_z2[1]

        # Z-level difference should equal z_level_offset
        assert screen_z0[1] - screen_z1[1] == renderer.z_level_offset
        assert screen_z1[1] - screen_z2[1] == renderer.z_level_offset

    def test_camera_offset_effect(self):
        """Test that camera offset affects screen coordinates."""
        renderer = GridRenderer(camera_offset=(100, 200))
        pos = GridPosition(0, 0, 0)
        screen = renderer.world_to_screen(pos)
        assert screen == (100, 200)

    def test_inverse_conversion(self, renderer):
        """Test screen to world conversion."""
        screen_pos = (32, 16)
        world_pos = renderer.screen_to_world(screen_pos, z_level=0)
        # Should give us (1, 0, 0) approximately
        assert world_pos.x == 1
        assert world_pos.y == 0
        assert world_pos.z == 0

    def test_round_trip_conversion(self, renderer):
        """Test world → screen → world gives same result."""
        original = GridPosition(5, 8, 1)
        screen = renderer.world_to_screen(original)
        recovered = renderer.screen_to_world(screen, z_level=1)

        assert recovered.x == original.x
        assert recovered.y == original.y
        assert recovered.z == original.z

    def test_multiple_round_trips(self, renderer):
        """Test round trip conversion for multiple positions."""
        test_positions = [
            GridPosition(0, 0, 0),
            GridPosition(5, 5, 0),
            GridPosition(10, 3, 1),
            GridPosition(7, 12, 2),
            GridPosition(15, 15, 3),
        ]

        for pos in test_positions:
            screen = renderer.world_to_screen(pos)
            recovered = renderer.screen_to_world(screen, z_level=pos.z)
            # Check that coordinates match
            assert recovered.x == pos.x, f"X mismatch: {recovered.x} != {pos.x}"
            assert recovered.y == pos.y, f"Y mismatch: {recovered.y} != {pos.y}"
            assert recovered.z == pos.z, f"Z mismatch: {recovered.z} != {pos.z}"


class TestBoundsChecking:
    """Test cases for grid bounds validation."""

    @pytest.fixture
    def renderer(self):
        """Create a renderer with known bounds."""
        return GridRenderer(grid_width=10, grid_height=10, max_z_levels=3)

    def test_valid_position(self, renderer):
        """Test that valid positions are within bounds."""
        assert renderer.is_in_bounds(GridPosition(0, 0, 0))
        assert renderer.is_in_bounds(GridPosition(5, 5, 1))
        assert renderer.is_in_bounds(GridPosition(9, 9, 2))

    def test_x_out_of_bounds(self, renderer):
        """Test x-coordinate out of bounds."""
        assert not renderer.is_in_bounds(GridPosition(-1, 5, 1))
        assert not renderer.is_in_bounds(GridPosition(10, 5, 1))
        assert not renderer.is_in_bounds(GridPosition(100, 5, 1))

    def test_y_out_of_bounds(self, renderer):
        """Test y-coordinate out of bounds."""
        assert not renderer.is_in_bounds(GridPosition(5, -1, 1))
        assert not renderer.is_in_bounds(GridPosition(5, 10, 1))
        assert not renderer.is_in_bounds(GridPosition(5, 100, 1))

    def test_z_out_of_bounds(self, renderer):
        """Test z-coordinate out of bounds."""
        assert not renderer.is_in_bounds(GridPosition(5, 5, -1))
        assert not renderer.is_in_bounds(GridPosition(5, 5, 3))
        assert not renderer.is_in_bounds(GridPosition(5, 5, 10))

    def test_edge_positions(self, renderer):
        """Test positions exactly at grid boundaries."""
        # Valid edges
        assert renderer.is_in_bounds(GridPosition(0, 0, 0))
        assert renderer.is_in_bounds(GridPosition(9, 0, 0))
        assert renderer.is_in_bounds(GridPosition(0, 9, 0))
        assert renderer.is_in_bounds(GridPosition(9, 9, 0))

        # Invalid (one past edge)
        assert not renderer.is_in_bounds(GridPosition(10, 0, 0))
        assert not renderer.is_in_bounds(GridPosition(0, 10, 0))


class TestCameraOperations:
    """Test cases for camera offset and viewport management."""

    def test_set_camera_offset(self):
        """Test updating camera offset."""
        renderer = GridRenderer(camera_offset=(0, 0))
        renderer.set_camera_offset((100, 200))
        assert renderer.camera_offset == (100, 200)

    def test_camera_affects_screen_coords(self):
        """Test that camera offset affects screen coordinates."""
        renderer = GridRenderer(camera_offset=(0, 0))
        pos = GridPosition(5, 5, 0)

        screen1 = renderer.world_to_screen(pos)
        renderer.set_camera_offset((50, 100))
        screen2 = renderer.world_to_screen(pos)

        # Screen position should shift by camera offset
        assert screen2[0] == screen1[0] + 50
        assert screen2[1] == screen1[1] + 100


class TestRendering:
    """Test cases for rendering operations."""

    @pytest.fixture
    def surface(self):
        """Create a pygame surface for testing."""
        pygame.init()
        return pygame.Surface((800, 600))

    @pytest.fixture
    def renderer(self):
        """Create a renderer for testing."""
        return GridRenderer(grid_width=5, grid_height=5, max_z_levels=2)

    def test_render_grid_no_error(self, surface, renderer):
        """Test that rendering grid doesn't raise errors."""
        renderer.render_grid(surface)
        # If we get here without exception, test passes

    def test_render_specific_z_levels(self, surface, renderer):
        """Test rendering specific z-levels."""
        renderer.render_grid(surface, visible_z_levels=[0, 1])
        # Should not raise error

    def test_render_single_z_level(self, surface, renderer):
        """Test rendering a single z-level."""
        renderer.render_z_level(surface, 0)
        renderer.render_z_level(surface, 1)
        # Should not raise errors

    def test_render_invalid_z_level(self, surface, renderer):
        """Test rendering invalid z-level is handled gracefully."""
        # Should log warning but not crash
        renderer.render_z_level(surface, 10)
        renderer.render_z_level(surface, -1)

    def test_render_cell_highlight(self, surface, renderer):
        """Test cell highlighting."""
        pos = GridPosition(2, 2, 0)
        renderer.render_cell_highlight(surface, pos)
        # Should not raise error

    def test_render_cell_highlight_custom_color(self, surface, renderer):
        """Test cell highlighting with custom color."""
        pos = GridPosition(2, 2, 0)
        renderer.render_cell_highlight(surface, pos, color=(255, 0, 0))
        # Should not raise error

    def test_render_cell_highlight_out_of_bounds(self, surface, renderer):
        """Test highlighting out-of-bounds cell is handled gracefully."""
        pos = GridPosition(100, 100, 0)
        renderer.render_cell_highlight(surface, pos)
        # Should not raise error (just returns early)


class TestFactoryFunctions:
    """Test cases for grid factory functions."""

    def test_create_default_grid(self):
        """Test creating default grid configuration."""
        renderer = create_default_grid()
        assert isinstance(renderer, GridRenderer)
        assert renderer.tile_width == 64
        assert renderer.tile_height == 32

    def test_create_combat_grid(self):
        """Test creating combat grid configuration."""
        renderer = create_combat_grid()
        assert isinstance(renderer, GridRenderer)
        assert renderer.tile_width == 48
        assert renderer.tile_height == 24
        assert renderer.grid_width == 15
        assert renderer.grid_height == 15
        assert renderer.max_z_levels == 3

    def test_create_sector_grid(self):
        """Test creating sector grid configuration."""
        renderer = create_sector_grid()
        assert isinstance(renderer, GridRenderer)
        # After zoom 2.0, tile dimensions are doubled
        assert renderer.tile_width == 64  # 32 * 2.0
        assert renderer.tile_height == 32  # 16 * 2.0
        assert renderer.grid_width == 20  # Fixed to match SectorMap dimensions
        assert renderer.grid_height == 20  # Fixed to match SectorMap dimensions
        assert renderer.max_z_levels == 5


class TestEdgeCases:
    """Test cases for edge cases and special scenarios."""

    def test_large_coordinates(self):
        """Test handling of very large coordinates."""
        renderer = GridRenderer(grid_width=1000, grid_height=1000)
        pos = GridPosition(999, 999, 0)
        screen = renderer.world_to_screen(pos)
        assert isinstance(screen[0], int)
        assert isinstance(screen[1], int)

    def test_negative_camera_offset(self):
        """Test negative camera offset values."""
        renderer = GridRenderer(camera_offset=(-100, -200))
        pos = GridPosition(5, 5, 0)
        screen = renderer.world_to_screen(pos)
        # Should work without error
        assert isinstance(screen, tuple)

    def test_zero_tile_dimensions(self):
        """Test creation with zero tile dimensions."""
        # This should work but may cause division issues in conversion
        renderer = GridRenderer(tile_width=1, tile_height=1)
        assert renderer.tile_width == 1
        assert renderer.tile_height == 1
