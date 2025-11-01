#!/usr/bin/env python3
"""
Star Trek Retro Remake - Isometric Grid Demo

Description:
    Interactive demonstration of the isometric grid rendering system.
    Shows grid visualization, cell selection, z-level switching, and
    camera panning. Useful for testing and understanding grid behavior.

Author: Star Trek Retro Remake Development Team
Email: development@star-trek-retro-remake.org
GitHub: https://github.com/L3DigitalNet/Star-Trek-Retro-Remake
Date Created: 10-30-2025
Date Changed: 10-30-2025
License: MIT

Features:
    - Interactive isometric grid visualization
    - Mouse click to select grid cells
    - Keyboard controls for z-level switching
    - Arrow keys for camera panning
    - Visual feedback for selected cells
    - Display of current grid position and z-level
    - Multiple demo modes (combat grid, sector grid)

Requirements:
    - Python 3.14+
    - pygame-ce (Community Edition)

Controls:
    - Mouse Click: Select grid cell
    - Up/Down Arrow: Change z-level
    - WASD or Arrow Keys: Pan camera
    - 1/2/3: Switch between grid presets
    - H: Toggle help display
    - ESC or Q: Quit

Usage:
    python demo_isometric_grid.py
"""

import sys
from typing import Final

import pygame

# Add STRR to path for imports
sys.path.insert(0, "/home/chris/GitHub/Star-Trek-Retro-Remake")

from STRR.src.engine.isometric_grid import (
    create_combat_grid,
    create_default_grid,
    create_sector_grid,
)
from STRR.src.game.entities.base import GridPosition

__version__: Final[str] = "0.0.1"

# Display constants
SCREEN_WIDTH: Final[int] = 1024
SCREEN_HEIGHT: Final[int] = 768
FPS: Final[int] = 60
BACKGROUND_COLOR: Final[tuple[int, int, int]] = (20, 20, 30)

# Colors
COLOR_WHITE: Final[tuple[int, int, int]] = (255, 255, 255)
COLOR_YELLOW: Final[tuple[int, int, int]] = (255, 255, 0)
COLOR_GREEN: Final[tuple[int, int, int]] = (0, 255, 0)
COLOR_RED: Final[tuple[int, int, int]] = (255, 0, 0)
COLOR_BLUE: Final[tuple[int, int, int]] = (100, 150, 255)
COLOR_UI_BG: Final[tuple[int, int, int, int]] = (0, 0, 0, 180)

# Camera pan speed
CAMERA_SPEED: Final[int] = 10


class IsometricGridDemo:
    """
    Interactive demonstration of isometric grid rendering.

    Provides visual and interactive testing of the GridRenderer class,
    allowing users to explore grid features like cell selection, z-levels,
    and camera movement.

    Attributes:
        screen: pygame display surface
        clock: pygame clock for FPS control
        renderer: Current GridRenderer instance
        current_z_level: Currently active z-level
        selected_cell: Currently selected grid position
        show_help: Whether to display help overlay
        demo_mode: Current demo mode (0=default, 1=combat, 2=sector)
        running: Main loop control flag
        font: Font for text rendering
        font_small: Smaller font for UI text
    """

    def __init__(self):
        """Initialize the demo application."""
        pygame.init()

        # Display setup
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Star Trek Retro Remake - Isometric Grid Demo")
        self.clock = pygame.time.Clock()

        # Grid setup
        self.renderer = create_default_grid()
        self.current_z_level = 0
        self.selected_cell: GridPosition | None = None

        # UI state
        self.show_help = True
        self.demo_mode = 0  # 0=default, 1=combat, 2=sector
        self.running = True

        # Fonts
        self.font = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)

        print("Isometric Grid Demo initialized")
        print("Press H for help")

    def run(self) -> None:
        """Run the main demo loop."""
        while self.running:
            self._handle_events()
            self._update()
            self._render()
            self.clock.tick(FPS)

        pygame.quit()
        print("Demo ended")

    def _handle_events(self) -> None:
        """Handle input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                self._handle_keypress(event.key)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_click(event.pos)

    def _handle_keypress(self, key: int) -> None:
        """
        Handle keyboard input.

        Args:
            key: pygame key constant
        """
        # Quit
        if key in (pygame.K_ESCAPE, pygame.K_q):
            self.running = False

        # Toggle help
        elif key == pygame.K_h:
            self.show_help = not self.show_help

        # Change z-level
        elif key == pygame.K_UP:
            self._change_z_level(1)
        elif key == pygame.K_DOWN:
            self._change_z_level(-1)

        # Camera panning
        elif key in (pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d):
            self._pan_camera(key)

        # Switch demo modes
        elif key == pygame.K_1:
            self._set_demo_mode(0)
        elif key == pygame.K_2:
            self._set_demo_mode(1)
        elif key == pygame.K_3:
            self._set_demo_mode(2)

    def _handle_mouse_click(self, mouse_pos: tuple[int, int]) -> None:
        """
        Handle mouse click for cell selection.

        Args:
            mouse_pos: Mouse position (x, y)
        """
        # Convert screen to world coordinates
        grid_pos = self.renderer.screen_to_world(mouse_pos, self.current_z_level)

        # Validate position
        if self.renderer.is_in_bounds(grid_pos):
            self.selected_cell = grid_pos
            print(f"Selected cell: {grid_pos}")
        else:
            print(f"Click out of bounds: {grid_pos}")

    def _change_z_level(self, delta: int) -> None:
        """
        Change the current z-level.

        Args:
            delta: Z-level change (+1 or -1)
        """
        new_z = self.current_z_level + delta
        if 0 <= new_z < self.renderer.max_z_levels:
            self.current_z_level = new_z
            print(f"Z-level changed to: {self.current_z_level}")

            # Update selected cell if it exists
            if self.selected_cell:
                self.selected_cell = GridPosition(
                    self.selected_cell.x, self.selected_cell.y, self.current_z_level
                )

    def _pan_camera(self, key: int) -> None:
        """
        Pan the camera based on key press.

        Args:
            key: pygame key constant
        """
        offset = self.renderer.camera_offset

        if key == pygame.K_w:
            offset[1] += CAMERA_SPEED
        elif key == pygame.K_s:
            offset[1] -= CAMERA_SPEED
        elif key == pygame.K_a:
            offset[0] += CAMERA_SPEED
        elif key == pygame.K_d:
            offset[0] -= CAMERA_SPEED

        self.renderer.set_camera_offset(tuple(offset))

    def _set_demo_mode(self, mode: int) -> None:
        """
        Switch to a different demo mode.

        Args:
            mode: Demo mode number (0=default, 1=combat, 2=sector)
        """
        self.demo_mode = mode
        self.selected_cell = None
        self.current_z_level = 0

        if mode == 0:
            self.renderer = create_default_grid()
            print("Switched to Default Grid")
        elif mode == 1:
            self.renderer = create_combat_grid()
            print("Switched to Combat Grid")
        elif mode == 2:
            self.renderer = create_sector_grid()
            print("Switched to Sector Grid")

    def _update(self) -> None:
        """Update demo state."""
        # No continuous updates needed for this demo
        pass

    def _render(self) -> None:
        """Render the demo display."""
        # Clear screen
        self.screen.fill(BACKGROUND_COLOR)

        # Render grid
        self.renderer.render_grid(self.screen, visible_z_levels=[self.current_z_level])

        # Render selected cell
        if self.selected_cell:
            self.renderer.render_cell_highlight(
                self.screen, self.selected_cell, COLOR_GREEN
            )

        # Render mouse hover (show which cell mouse is over)
        mouse_pos = pygame.mouse.get_pos()
        hover_pos = self.renderer.screen_to_world(mouse_pos, self.current_z_level)
        if self.renderer.is_in_bounds(hover_pos) and hover_pos != self.selected_cell:
            self.renderer.render_cell_highlight(self.screen, hover_pos, COLOR_BLUE)

        # Render UI overlays
        self._render_info_panel()
        if self.show_help:
            self._render_help_panel()

        # Update display
        pygame.display.flip()

    def _render_info_panel(self) -> None:
        """Render the information panel."""
        # Create semi-transparent background
        info_surface = pygame.Surface((300, 180))
        info_surface.set_alpha(180)
        info_surface.fill((0, 0, 0))
        self.screen.blit(info_surface, (10, 10))

        # Render text
        y_offset = 20

        # Mode info
        mode_names = ["Default Grid", "Combat Grid", "Sector Grid"]
        mode_text = self.font_small.render(
            f"Mode: {mode_names[self.demo_mode]}", True, COLOR_WHITE
        )
        self.screen.blit(mode_text, (20, y_offset))
        y_offset += 30

        # Z-level info
        z_text = self.font_small.render(
            f"Z-Level: {self.current_z_level}/{self.renderer.max_z_levels - 1}",
            True,
            COLOR_YELLOW,
        )
        self.screen.blit(z_text, (20, y_offset))
        y_offset += 30

        # Grid dimensions
        grid_text = self.font_small.render(
            f"Grid: {self.renderer.grid_width}x{self.renderer.grid_height}",
            True,
            COLOR_WHITE,
        )
        self.screen.blit(grid_text, (20, y_offset))
        y_offset += 30

        # Camera position
        cam_text = self.font_small.render(
            f"Camera: {self.renderer.camera_offset}", True, COLOR_WHITE
        )
        self.screen.blit(cam_text, (20, y_offset))
        y_offset += 30

        # Selected cell
        if self.selected_cell:
            sel_text = self.font_small.render(
                f"Selected: ({self.selected_cell.x}, {self.selected_cell.y}, {self.selected_cell.z})",
                True,
                COLOR_GREEN,
            )
        else:
            sel_text = self.font_small.render("Selected: None", True, COLOR_WHITE)
        self.screen.blit(sel_text, (20, y_offset))

    def _render_help_panel(self) -> None:
        """Render the help overlay."""
        # Create semi-transparent background
        help_surface = pygame.Surface((400, 400))
        help_surface.set_alpha(200)
        help_surface.fill((0, 0, 0))
        self.screen.blit(help_surface, (SCREEN_WIDTH - 410, 10))

        # Help text
        help_lines = [
            "CONTROLS",
            "",
            "Mouse Click - Select cell",
            "Up/Down - Change z-level",
            "W/A/S/D - Pan camera",
            "1/2/3 - Switch grid mode",
            "H - Toggle this help",
            "ESC/Q - Quit",
            "",
            "GRID MODES",
            "",
            "1 - Default Grid",
            "   64x32 tiles, 20x20",
            "2 - Combat Grid",
            "   48x24 tiles, 15x15",
            "3 - Sector Grid",
            "   32x16 tiles, 30x30",
        ]

        y_offset = 20
        for line in help_lines:
            if line:
                if line.isupper():
                    color = COLOR_YELLOW
                    font = self.font_small
                else:
                    color = COLOR_WHITE
                    font = self.font_small

                text = font.render(line, True, color)
                self.screen.blit(text, (SCREEN_WIDTH - 390, y_offset))

            y_offset += 22


def main() -> None:
    """Main entry point for the demo."""
    print("=" * 60)
    print("Star Trek Retro Remake - Isometric Grid Demo")
    print("=" * 60)
    print("\nStarting interactive demo...")
    print("Press H in the application for help\n")

    try:
        demo = IsometricGridDemo()
        demo.run()
    except Exception as e:
        print(f"Error running demo: {e}")
        import traceback

        traceback.print_exc()
        return 1

    print("\nDemo completed successfully")
    return 0


if __name__ == "__main__":
    sys.exit(main())
