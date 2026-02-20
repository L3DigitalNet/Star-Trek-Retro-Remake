#!/usr/bin/env python3
"""
Star Trek Retro Remake - Isometric Grid Renderer

Description:
    Isometric grid rendering system supporting 3D coordinates (x, y, z) with
    z-level visualization for space positioning. Provides conversion between
    world coordinates and screen coordinates, grid drawing, and highlighting.

Author: Star Trek Retro Remake Development Team
Email: development@star-trek-retro-remake.org
GitHub: https://github.com/L3DigitalNet/Star-Trek-Retro-Remake
Date Created: 10-30-2025
Date Changed: 10-31-2025
License: MIT

Features:
    - Isometric projection from 3D grid coordinates to 2D screen coordinates
    - Support for multiple z-levels (vertical space positioning)
    - Grid line rendering with configurable tile size and colors
    - Cell highlighting and selection
    - Camera offset and viewport management
    - Grid bounds checking and validation

Requirements:
    - Linux environment
    - Python 3.14+ for latest language features
    - pygame-ce (Community Edition) for rendering

Known Issues:
    - None currently

Planned Features:
    - Grid scrolling and panning
    - Zoom in/out functionality
    - Animated transitions between z-levels
    - Grid cell hover effects
    - Minimap rendering

Classes:
    - GridRenderer: Main isometric grid rendering system
    - GridPosition: 3D grid position representation (imported from model)

Functions:
    - world_to_screen: Convert 3D world coordinates to 2D screen coordinates
    - screen_to_world: Convert 2D screen coordinates to 3D world coordinates
"""

import logging
from typing import Final, TypeAlias

import pygame

# Import GridPosition from the game entities module
from ..game.entities.base import GridPosition

__version__: Final[str] = "0.0.23"

logger = logging.getLogger(__name__)

# Type aliases
ColorTuple: TypeAlias = tuple[int, int, int] | tuple[int, int, int, int]
ScreenCoord: TypeAlias = tuple[int, int]


class GridRenderer:
    """
    Isometric grid rendering system with z-level support.

    Renders a 3D grid using isometric projection, converting world coordinates
    (x, y, z) to screen coordinates for display. Supports multiple z-levels
    for representing vertical positioning in space.

    Attributes:
        tile_width: Width of isometric tile in pixels
        tile_height: Height of isometric tile in pixels
        grid_width: Number of tiles in X direction
        grid_height: Number of tiles in Y direction
        max_z_levels: Maximum number of z-levels
        camera_offset: Camera position offset (x, y)
        grid_color: Color for grid lines
        highlight_color: Color for highlighted cells
        z_level_offset: Vertical pixel offset per z-level

    Public methods:
        world_to_screen: Convert 3D world coords to 2D screen coords
        screen_to_world: Convert 2D screen coords to 3D world coords
        render_grid: Draw the isometric grid
        render_cell_highlight: Highlight a specific grid cell
        render_z_level: Render a specific z-level
        render_entity: Draw an entity (starship/station) with orientation and z-reference
        is_in_bounds: Check if position is within grid bounds
        set_camera_offset: Update camera position

    Private methods:
        _draw_grid_lines: Draw the grid lines for a z-level
        _draw_diamond: Draw a diamond shape for a grid cell
        _calculate_cell_corners: Get screen coordinates for cell corners
        _render_z_reference_line: Draw vertical reference line to active layer
        _draw_dashed_line: Draw a dashed line between two points
    """

    # Default colors - Using distinct hues for better z-level differentiation
    DEFAULT_GRID_COLOR: Final[ColorTuple] = (100, 100, 100)
    DEFAULT_HIGHLIGHT_COLOR: Final[ColorTuple] = (255, 255, 0)
    DEFAULT_Z_LEVEL_COLORS: Final[tuple[ColorTuple, ...]] = (
        (60, 60, 140),  # Z=0 - Deep space (dark blue)
        (80, 140, 120),  # Z=1 - Low orbit (cyan-green)
        (140, 100, 140),  # Z=2 - Mid orbit (purple)
        (140, 120, 60),  # Z=3 - High orbit (amber)
        (140, 80, 80),  # Z=4 - Upper atmosphere (reddish)
    )

    def __init__(
        self,
        tile_width: int = 64,
        tile_height: int = 32,
        grid_width: int = 20,
        grid_height: int = 20,
        max_z_levels: int = 4,
        camera_offset: tuple[int, int] = (400, 100),
    ):
        """
        Initialize the isometric grid renderer.

        Args:
            tile_width: Width of each isometric tile in pixels
            tile_height: Height of each isometric tile in pixels
            grid_width: Number of tiles in X direction
            grid_height: Number of tiles in Y direction
            max_z_levels: Maximum number of z-levels (vertical layers)
            camera_offset: Initial camera position (x, y) in screen space
        """
        # Store base tile dimensions
        self.base_tile_width: Final[int] = tile_width
        self.base_tile_height: Final[int] = tile_height
        self.grid_width: Final[int] = grid_width
        self.grid_height: Final[int] = grid_height
        self.max_z_levels: Final[int] = max_z_levels

        # Zoom support
        self.zoom_level: float = 1.0  # 1.0 = 100%, 2.0 = 200%, 0.5 = 50%
        self.min_zoom: Final[float] = 0.5  # 50% minimum (improved precision)
        self.max_zoom: Final[float] = 4.0  # 400% maximum

        # Current tile dimensions (affected by zoom)
        self.tile_width: int = tile_width
        self.tile_height: int = tile_height
        self.z_level_offset: int = 24  # Vertical pixels per z-level

        # Camera and viewport (stored as tuple for immutability)
        self._camera_offset: tuple[int, int] = camera_offset

        # Visual properties
        self.grid_color: ColorTuple = self.DEFAULT_GRID_COLOR
        self.highlight_color: ColorTuple = self.DEFAULT_HIGHLIGHT_COLOR

        # Z-level colors (darker for lower levels)
        self.z_level_colors: tuple[ColorTuple, ...] = self.DEFAULT_Z_LEVEL_COLORS

        logger.info(
            "GridRenderer initialized: %dx%d tiles, %d z-levels",
            grid_width,
            grid_height,
            max_z_levels,
        )

    def world_to_screen(self, position: GridPosition) -> ScreenCoord:
        """
        Convert 3D world coordinates to 2D screen coordinates.

        Uses isometric projection formula:
        screen_x = (world_x - world_y) * (tile_width / 2)
        screen_y = (world_x + world_y) * (tile_height / 2) - (world_z * z_offset)

        Args:
            position: Grid position in world coordinates

        Returns:
            Tuple of (screen_x, screen_y) in pixels
        """
        # Isometric projection
        iso_x = (position.x - position.y) * (self.tile_width // 2)
        iso_y = (position.x + position.y) * (self.tile_height // 2)

        # Apply z-level offset (higher z = higher on screen)
        iso_y -= position.z * self.z_level_offset

        # Apply camera offset
        screen_x = iso_x + self._camera_offset[0]
        screen_y = iso_y + self._camera_offset[1]

        return (screen_x, screen_y)

    def screen_to_world(
        self, screen_pos: ScreenCoord, z_level: int = 0
    ) -> GridPosition:
        """
        Convert 2D screen coordinates to 3D world coordinates.

        Inverse isometric projection to determine which grid cell was clicked.

        Args:
            screen_pos: Screen position (x, y) in pixels
            z_level: Z-level to calculate for (default 0)

        Returns:
            GridPosition in world coordinates
        """
        # Remove camera offset
        screen_x = screen_pos[0] - self._camera_offset[0]
        screen_y = screen_pos[1] - self._camera_offset[1]

        # Adjust for z-level
        screen_y += z_level * self.z_level_offset

        # Inverse isometric projection
        # world_x = (screen_x / (tile_width/2) + screen_y / (tile_height/2)) / 2
        # world_y = (screen_y / (tile_height/2) - screen_x / (tile_width/2)) / 2
        world_x = (
            screen_x / (self.tile_width / 2) + screen_y / (self.tile_height / 2)
        ) / 2
        world_y = (
            screen_y / (self.tile_height / 2) - screen_x / (self.tile_width / 2)
        ) / 2

        # Round to nearest integer
        return GridPosition(round(world_x), round(world_y), z_level)

    def render_grid(
        self, surface: pygame.Surface, visible_z_levels: list[int] | None = None
    ) -> None:
        """
        Render the complete isometric grid.

        Draws grid lines for all or specified z-levels. Renders from bottom
        to top (z=0 to z=max) for proper depth ordering.

        Args:
            surface: pygame Surface to render on
            visible_z_levels: List of z-levels to render (None = all)
        """
        # Determine which z-levels to render
        if visible_z_levels is None:
            visible_z_levels = list(range(self.max_z_levels))

        # Render from bottom to top for proper layering
        for z in sorted(visible_z_levels):
            if 0 <= z < self.max_z_levels:
                self.render_z_level(surface, z)

    def render_z_level(
        self, surface: pygame.Surface, z_level: int, current_z_level: int | None = None
    ) -> None:
        """
        Render a specific z-level of the grid.

        Args:
            surface: pygame Surface to render on
            z_level: Z-level to render (0 to max_z_levels-1)
            current_z_level: Current active z-level for dash calculation (None = solid lines)
        """
        if not 0 <= z_level < self.max_z_levels:
            logger.warning("Z-level %d out of bounds", z_level)
            return

        # Determine color based on whether this is the current z-level
        if current_z_level is not None and z_level == current_z_level:
            # Current level: white
            level_color = (255, 255, 255)
        else:
            # Other levels: gray
            level_color = (128, 128, 128)

        # Draw grid lines with dashing based on distance from current level
        self._draw_grid_lines(surface, z_level, level_color, current_z_level)

    def render_cell_highlight(
        self,
        surface: pygame.Surface,
        position: GridPosition,
        color: ColorTuple | None = None,
    ) -> None:
        """
        Highlight a specific grid cell.

        Draws a filled diamond shape at the specified position.

        Args:
            surface: pygame Surface to render on
            position: Grid position to highlight
            color: Highlight color (None = use default)
        """
        if not self.is_in_bounds(position):
            return

        # Use default highlight color if not specified
        if color is None:
            color = self.highlight_color

        # Get cell corners
        corners = self._calculate_cell_corners(position)

        # Draw filled polygon
        pygame.draw.polygon(surface, color, corners, 0)

        # Draw outline for clarity
        pygame.draw.polygon(surface, (255, 255, 255), corners, 2)

    def render_entity(
        self,
        surface: pygame.Surface,
        position: GridPosition,
        color: ColorTuple,
        size: int = 16,
        orientation: float = 0.0,
        name: str = "",
        current_z_level: int | None = None,
    ) -> None:
        """
        Render an entity (starship, station) on the grid.

        Draws a colored circle/shape at the entity's position with an
        orientation indicator showing facing direction. If the entity is
        on a different z-level than current_z_level, draws a vertical
        reference line to the active layer and displays the z-distance.

        Args:
            surface: pygame Surface to render on
            position: Entity's 3D grid position
            color: RGB color for the entity
            size: Entity size in pixels
            orientation: Facing direction in radians (0 = east)
            name: Entity name to display
            current_z_level: Current active z-level (None = no reference line)
        """
        import math

        if not self.is_in_bounds(position):
            return

        # Convert world position to screen position
        screen_x, screen_y = self.world_to_screen(position)

        # Draw vertical reference line if entity is on different z-level
        if current_z_level is not None and position.z != current_z_level:
            self._render_z_reference_line(
                surface, position, current_z_level, color, screen_x, screen_y
            )

        # Draw entity body (circle)
        pygame.draw.circle(surface, color, (screen_x, screen_y), size // 2)
        # Draw white outline for visibility
        pygame.draw.circle(surface, (255, 255, 255), (screen_x, screen_y), size // 2, 2)

        # Draw orientation indicator (triangle/arrow pointing in facing direction)
        arrow_length = size * 0.8
        arrow_width = size * 0.4

        # Calculate arrow tip position
        tip_x = screen_x + int(math.cos(orientation) * arrow_length)
        tip_y = screen_y + int(math.sin(orientation) * arrow_length)

        # Calculate arrow base corners (perpendicular to facing)
        perp_angle = orientation + math.pi / 2
        base1_x = screen_x + int(math.cos(perp_angle) * arrow_width / 2)
        base1_y = screen_y + int(math.sin(perp_angle) * arrow_width / 2)
        base2_x = screen_x - int(math.cos(perp_angle) * arrow_width / 2)
        base2_y = screen_y - int(math.sin(perp_angle) * arrow_width / 2)

        # Draw orientation arrow
        arrow_points = [(tip_x, tip_y), (base1_x, base1_y), (base2_x, base2_y)]
        pygame.draw.polygon(surface, (255, 255, 255), arrow_points)
        pygame.draw.polygon(surface, (0, 0, 0), arrow_points, 1)  # Black outline

        # Draw z-level distance indicator if on different level
        if current_z_level is not None and position.z != current_z_level:
            z_distance = position.z - current_z_level
            # Format: +N (above) or -N (below)
            z_text = f"{z_distance:+d}"

            # Small font for z-distance indicator
            z_font = pygame.font.Font(None, 18)
            z_label = z_font.render(z_text, True, (255, 255, 100))  # Yellow-ish

            # Position: upper-right of entity circle
            z_label_x = screen_x + size // 2 + 2
            z_label_y = screen_y - size // 2 - 2
            z_label_rect = z_label.get_rect(topleft=(z_label_x, z_label_y))

            # Draw semi-transparent background for visibility
            z_bg_rect = z_label_rect.inflate(2, 1)
            pygame.draw.rect(surface, (0, 0, 0, 200), z_bg_rect)
            pygame.draw.rect(surface, (100, 100, 100), z_bg_rect, 1)  # Border
            surface.blit(z_label, z_label_rect)

        # Draw entity name label
        if name:
            font = pygame.font.Font(None, 20)
            text = font.render(name, True, (255, 255, 255))
            text_rect = text.get_rect(center=(screen_x, screen_y - size))
            # Draw background for text visibility
            bg_rect = text_rect.inflate(4, 2)
            pygame.draw.rect(surface, (0, 0, 0, 180), bg_rect)
            surface.blit(text, text_rect)

    def _render_z_reference_line(
        self,
        surface: pygame.Surface,
        entity_position: GridPosition,
        current_z_level: int,
        entity_color: ColorTuple,
        entity_screen_x: int,
        entity_screen_y: int,
    ) -> None:
        """
        Render a vertical reference line from entity to active layer.

        Draws a dashed line from the entity's position down to where it
        would appear on the current z-level, making it easier to see
        spatial relationships.

        Args:
            surface: pygame Surface to render on
            entity_position: Entity's 3D grid position
            current_z_level: The active z-level to project to
            entity_color: Color of the entity (used for line color)
            entity_screen_x: Entity's screen X coordinate
            entity_screen_y: Entity's screen Y coordinate
        """
        # Calculate the position on the current z-level (same x, y)
        target_position = GridPosition(
            entity_position.x, entity_position.y, current_z_level
        )
        target_screen_x, target_screen_y = self.world_to_screen(target_position)

        # Use entity color but make it semi-transparent
        line_color = (*entity_color[:3], 128)  # Ensure RGB format with alpha

        # Draw dashed line from entity to target position
        self._draw_dashed_line(
            surface,
            (entity_screen_x, entity_screen_y),
            (target_screen_x, target_screen_y),
            line_color,
            dash_length=8,
            gap_length=4,
        )

        # Draw a small circle at the target position to show where it projects
        pygame.draw.circle(surface, entity_color, (target_screen_x, target_screen_y), 4)
        pygame.draw.circle(
            surface, (255, 255, 255), (target_screen_x, target_screen_y), 4, 1
        )

    def is_in_bounds(self, position: GridPosition) -> bool:
        """
        Check if a position is within grid bounds.

        Args:
            position: Grid position to check

        Returns:
            True if position is valid, False otherwise
        """
        return (
            0 <= position.x < self.grid_width
            and 0 <= position.y < self.grid_height
            and 0 <= position.z < self.max_z_levels
        )

    @property
    def camera_offset(self) -> tuple[int, int]:
        """Get the current camera offset."""
        return self._camera_offset

    def set_camera_offset(self, offset: tuple[int, int]) -> None:
        """
        Update the camera position offset.

        Args:
            offset: New camera offset (x, y) in pixels
        """
        self._camera_offset = offset
        logger.debug("Camera offset set to: %s", offset)

    def set_zoom(self, zoom: float) -> None:
        """
        Set the zoom level.

        Args:
            zoom: Zoom level (1.0 = 100%, 2.0 = 200%, 0.5 = 50%)
        """
        # Clamp zoom to valid range
        self.zoom_level = max(self.min_zoom, min(zoom, self.max_zoom))

        # Update tile dimensions based on zoom with minimum enforced
        # Higher minimums (16x8) ensure better coordinate conversion precision
        self.tile_width = max(16, int(self.base_tile_width * self.zoom_level))
        self.tile_height = max(8, int(self.base_tile_height * self.zoom_level))
        self.z_level_offset = max(4, int(24 * self.zoom_level))

        logger.info(
            f"Zoom set to {self.zoom_level:.2f}x (tile: {self.tile_width}x{self.tile_height})"
        )

    def zoom_in(self, factor: float = 1.2) -> None:
        """
        Zoom in by a multiplicative factor.

        Args:
            factor: Zoom multiplication factor (default 1.2 = 20% increase)
        """
        self.set_zoom(self.zoom_level * factor)

    def zoom_out(self, factor: float = 1.2) -> None:
        """
        Zoom out by a multiplicative factor.

        Args:
            factor: Zoom division factor (default 1.2 = 20% decrease)
        """
        self.set_zoom(self.zoom_level / factor)

    def reset_zoom(self) -> None:
        """Reset zoom to 100%."""
        self.set_zoom(1.0)

    def _draw_grid_lines(
        self,
        surface: pygame.Surface,
        z_level: int,
        color: ColorTuple,
        current_z_level: int | None = None,
    ) -> None:
        """
        Draw grid lines for a specific z-level with optional dashing.

        Args:
            surface: pygame Surface to render on
            z_level: Z-level to draw
            color: Color for the grid lines
            current_z_level: Current active z-level (None = solid lines for all)
        """
        # Calculate dash parameters based on distance from current level
        if current_z_level is not None:
            distance = abs(z_level - current_z_level)

            if distance == 0:
                # Current level: solid lines
                dash_length = 0  # 0 means solid
                gap_length = 0
            elif distance == 1:
                # Adjacent level: light dashing
                dash_length = 16
                gap_length = 4
            elif distance == 2:
                # Two levels away: medium dashing
                dash_length = 12
                gap_length = 8
            else:
                # Far levels: heavy dashing (very sparse)
                dash_length = 8
                gap_length = 16
        else:
            # No current level specified: solid lines
            dash_length = 0
            gap_length = 0

        # Draw horizontal lines (X direction)
        for y in range(self.grid_height + 1):
            start_pos = GridPosition(0, y, z_level)
            end_pos = GridPosition(self.grid_width, y, z_level)

            start_screen = self.world_to_screen(start_pos)
            end_screen = self.world_to_screen(end_pos)

            if dash_length == 0:
                # Solid line
                pygame.draw.line(surface, color, start_screen, end_screen, 1)
            else:
                # Dashed line
                self._draw_dashed_line(
                    surface, start_screen, end_screen, color, dash_length, gap_length
                )

        # Draw vertical lines (Y direction)
        for x in range(self.grid_width + 1):
            start_pos = GridPosition(x, 0, z_level)
            end_pos = GridPosition(x, self.grid_height, z_level)

            start_screen = self.world_to_screen(start_pos)
            end_screen = self.world_to_screen(end_pos)

            if dash_length == 0:
                # Solid line
                pygame.draw.line(surface, color, start_screen, end_screen, 1)
            else:
                # Dashed line
                self._draw_dashed_line(
                    surface, start_screen, end_screen, color, dash_length, gap_length
                )

    def _draw_dashed_line(
        self,
        surface: pygame.Surface,
        start: ScreenCoord,
        end: ScreenCoord,
        color: ColorTuple,
        dash_length: int,
        gap_length: int,
    ) -> None:
        """
        Draw a dashed line between two points.

        Args:
            surface: pygame Surface to render on
            start: Start position (x, y)
            end: End position (x, y)
            color: Line color
            dash_length: Length of each dash in pixels
            gap_length: Length of gap between dashes in pixels
        """
        # Calculate line vector
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        distance = (dx * dx + dy * dy) ** 0.5

        if distance == 0:
            return

        # Normalize direction
        dx_norm = dx / distance
        dy_norm = dy / distance

        # Draw dashes
        current_distance = 0.0
        pattern_length = dash_length + gap_length

        while current_distance < distance:
            # Calculate dash start and end
            dash_start_dist = current_distance
            dash_end_dist = min(current_distance + dash_length, distance)

            # Calculate screen positions
            dash_start = (
                int(start[0] + dx_norm * dash_start_dist),
                int(start[1] + dy_norm * dash_start_dist),
            )
            dash_end = (
                int(start[0] + dx_norm * dash_end_dist),
                int(start[1] + dy_norm * dash_end_dist),
            )

            # Draw this dash segment
            pygame.draw.line(surface, color, dash_start, dash_end, 1)

            # Move to next dash
            current_distance += pattern_length

    def _calculate_cell_corners(self, position: GridPosition) -> list[ScreenCoord]:
        """
        Calculate screen coordinates for the four corners of a grid cell.

        Corners are ordered: top, right, bottom, left (clockwise from top).

        Args:
            position: Grid position of the cell

        Returns:
            List of four (x, y) tuples representing corner positions
        """
        # Get center position
        center = self.world_to_screen(position)

        # Calculate corner offsets for isometric diamond
        half_width = self.tile_width // 2
        half_height = self.tile_height // 2

        # Corners in clockwise order from top
        corners = [
            (center[0], center[1] - half_height),  # Top
            (center[0] + half_width, center[1]),  # Right
            (center[0], center[1] + half_height),  # Bottom
            (center[0] - half_width, center[1]),  # Left
        ]

        return corners


# Module-level convenience functions
def create_default_grid() -> GridRenderer:
    """
    Create a grid renderer with default settings.

    Returns:
        GridRenderer instance with default parameters
    """
    return GridRenderer()


def create_combat_grid() -> GridRenderer:
    """
    Create a grid renderer optimized for combat view.

    Returns:
        GridRenderer instance configured for combat
    """
    return GridRenderer(
        tile_width=48,
        tile_height=24,
        grid_width=15,
        grid_height=15,
        max_z_levels=3,
        camera_offset=(400, 200),
    )


def create_sector_grid() -> GridRenderer:
    """
    Create a grid renderer optimized for sector map view.

    Returns:
        GridRenderer instance configured for sector map
    """
    # Grid dimensions match SectorMap: 20x20 grid with 5 z-levels
    # Center the grid in a 1280x900 window
    # Grid center is at (10, 10), window center is (640, 450)
    # Base tile size: 32x16 at zoom 1.0
    # Zoom 2.0 gives: 64x32 tiles for closer view
    # Isometric center point at zoom 2.0: (10-10) * 32 = 0, (10+10) * 16 = 320
    # Camera offset: window_center - iso_center = (640, 450 - 320) = (640, 130)
    grid = GridRenderer(
        tile_width=32,
        tile_height=16,
        grid_width=20,  # Match SectorMap.grid_size[0]
        grid_height=20,  # Match SectorMap.grid_size[1]
        max_z_levels=5,  # Match SectorMap.grid_size[2]
        camera_offset=(640, 130),
    )
    # Set zoom to 2.0 for closer view (testing purposes)
    grid.set_zoom(2.0)
    return grid
