#!/usr/bin/env python3
"""
Star Trek Retro Remake - Application Tests

Description:
    Unit tests for the main game application class, testing initialization,
    lifecycle management, and system coordination.

Author: Star Trek Retro Remake Development Team
Email: development@star-trek-retro-remake.org
GitHub: https://github.com/L3DigitalNet/Star-Trek-Retro-Remake
Date Created: 10-30-2025
Date Changed: 10-30-2025
License: MIT

Test Coverage:
    - StarTrekRetroRemake class initialization
    - MVC component creation and coordination
    - System initialization (pygame-ce, PySide6)
    - Application lifecycle management

Requirements:
    - pytest >= 8.0.0
    - Python 3.14+
"""

from typing import Final
from unittest.mock import MagicMock, patch

from src.game.application import StarTrekRetroRemake

__version__: Final[str] = "0.0.18"


class TestStarTrekRetroRemakeInitialization:
    """Test StarTrekRetroRemake application initialization."""

    @patch("src.game.application.pygame.init")
    @patch("src.game.application.QApplication")
    @patch("src.game.application.GameView")
    @patch("src.game.application.GameController")
    @patch("src.game.application.GameModel")
    def test_application_initialization_creates_mvc_components(
        self, mock_model, mock_controller, mock_view, mock_qapp, mock_pygame_init
    ):
        """Test that initialization creates model, view, and controller."""
        # Arrange
        mock_qapp.instance.return_value = None
        mock_qapp_instance = MagicMock()
        mock_qapp.return_value = mock_qapp_instance

        # Act
        app = StarTrekRetroRemake()

        # Assert
        mock_model.assert_called_once()
        mock_controller.assert_called_once()
        mock_view.assert_called_once()
        assert app.model is not None
        assert app.controller is not None
        assert app.view is not None

    @patch("src.game.application.pygame.init")
    @patch("src.game.application.QApplication")
    @patch("src.game.application.GameView")
    @patch("src.game.application.GameController")
    @patch("src.game.application.GameModel")
    def test_application_initializes_pygame(
        self, mock_model, mock_controller, mock_view, mock_qapp, mock_pygame_init
    ):
        """Test that pygame is initialized during application setup."""
        # Arrange
        mock_qapp.instance.return_value = None
        mock_qapp_instance = MagicMock()
        mock_qapp.return_value = mock_qapp_instance

        # Act
        app = StarTrekRetroRemake()

        # Assert
        mock_pygame_init.assert_called_once()

    @patch("src.game.application.pygame.init")
    @patch("src.game.application.QApplication")
    @patch("src.game.application.GameView")
    @patch("src.game.application.GameController")
    @patch("src.game.application.GameModel")
    def test_application_initializes_qapplication(
        self, mock_model, mock_controller, mock_view, mock_qapp, mock_pygame_init
    ):
        """Test that QApplication is initialized during application setup."""
        # Arrange
        mock_qapp.instance.return_value = None
        mock_qapp_instance = MagicMock()
        mock_qapp.return_value = mock_qapp_instance

        # Act
        app = StarTrekRetroRemake()

        # Assert
        mock_qapp.assert_called_once()
        assert app.qt_app == mock_qapp_instance

    @patch("src.game.application.pygame.init")
    @patch("src.game.application.QApplication")
    @patch("src.game.application.GameView")
    @patch("src.game.application.GameController")
    @patch("src.game.application.GameModel")
    def test_application_uses_existing_qapplication(
        self, mock_model, mock_controller, mock_view, mock_qapp, mock_pygame_init
    ):
        """Test that application uses existing QApplication instance if available."""
        # Arrange
        existing_qapp = MagicMock()
        mock_qapp.instance.return_value = existing_qapp

        # Act
        app = StarTrekRetroRemake()

        # Assert
        assert app.qt_app == existing_qapp

    @patch("src.game.application.pygame.init")
    @patch("src.game.application.QApplication")
    @patch("src.game.application.GameView")
    @patch("src.game.application.GameController")
    @patch("src.game.application.GameModel")
    def test_application_connects_controller_and_view(
        self, mock_model, mock_controller, mock_view, mock_qapp, mock_pygame_init
    ):
        """Test that controller and view are properly connected."""
        # Arrange
        mock_qapp.instance.return_value = None
        mock_qapp_instance = MagicMock()
        mock_qapp.return_value = mock_qapp_instance
        mock_controller_instance = MagicMock()
        mock_controller.return_value = mock_controller_instance

        # Act
        app = StarTrekRetroRemake()

        # Assert
        mock_controller_instance.set_view.assert_called_once_with(app.view)

    @patch("src.game.application.pygame.init")
    @patch("src.game.application.QApplication")
    @patch("src.game.application.GameView")
    @patch("src.game.application.GameController")
    @patch("src.game.application.GameModel")
    def test_application_running_state_is_true_after_init(
        self, mock_model, mock_controller, mock_view, mock_qapp, mock_pygame_init
    ):
        """Test that application running state is True after initialization."""
        # Arrange
        mock_qapp.instance.return_value = None
        mock_qapp_instance = MagicMock()
        mock_qapp.return_value = mock_qapp_instance

        # Act
        app = StarTrekRetroRemake()

        # Assert
        assert app.running is True


class TestStarTrekRetroRemakeShutdown:
    """Test application shutdown and cleanup."""

    @patch("src.game.application.pygame")
    @patch("src.game.application.QApplication")
    @patch("src.game.application.GameView")
    @patch("src.game.application.GameController")
    @patch("src.game.application.GameModel")
    def test_shutdown_stops_controller(
        self, mock_model, mock_controller, mock_view, mock_qapp, mock_pygame
    ):
        """Test that shutdown calls controller.stop()."""
        # Arrange
        mock_qapp.instance.return_value = None
        mock_qapp_instance = MagicMock()
        mock_qapp.return_value = mock_qapp_instance
        mock_controller_instance = MagicMock()
        mock_controller.return_value = mock_controller_instance

        app = StarTrekRetroRemake()

        # Act
        app.shutdown()

        # Assert
        mock_controller_instance.stop.assert_called_once()

    @patch("src.game.application.pygame")
    @patch("src.game.application.QApplication")
    @patch("src.game.application.GameView")
    @patch("src.game.application.GameController")
    @patch("src.game.application.GameModel")
    def test_shutdown_closes_view(
        self, mock_model, mock_controller, mock_view, mock_qapp, mock_pygame
    ):
        """Test that shutdown calls view.close()."""
        # Arrange
        mock_qapp.instance.return_value = None
        mock_qapp_instance = MagicMock()
        mock_qapp.return_value = mock_qapp_instance
        mock_view_instance = MagicMock()
        mock_view.return_value = mock_view_instance

        app = StarTrekRetroRemake()

        # Act
        app.shutdown()

        # Assert
        mock_view_instance.close.assert_called_once()

    @patch("src.game.application.pygame")
    @patch("src.game.application.QApplication")
    @patch("src.game.application.GameView")
    @patch("src.game.application.GameController")
    @patch("src.game.application.GameModel")
    def test_shutdown_sets_running_to_false(
        self, mock_model, mock_controller, mock_view, mock_qapp, mock_pygame
    ):
        """Test that shutdown sets running state to False."""
        # Arrange
        mock_qapp.instance.return_value = None
        mock_qapp_instance = MagicMock()
        mock_qapp.return_value = mock_qapp_instance

        app = StarTrekRetroRemake()

        # Act
        app.shutdown()

        # Assert
        assert app.running is False

    @patch("src.game.application.pygame")
    @patch("src.game.application.QApplication")
    @patch("src.game.application.GameView")
    @patch("src.game.application.GameController")
    @patch("src.game.application.GameModel")
    def test_shutdown_cleans_up_pygame(
        self, mock_model, mock_controller, mock_view, mock_qapp, mock_pygame
    ):
        """Test that shutdown calls pygame.quit()."""
        # Arrange
        mock_qapp.instance.return_value = None
        mock_qapp_instance = MagicMock()
        mock_qapp.return_value = mock_qapp_instance

        app = StarTrekRetroRemake()

        # Act
        app.shutdown()

        # Assert
        mock_pygame.quit.assert_called_once()

    @patch("src.game.application.pygame")
    @patch("src.game.application.QApplication")
    @patch("src.game.application.GameView")
    @patch("src.game.application.GameController")
    @patch("src.game.application.GameModel")
    def test_shutdown_quits_qapplication(
        self, mock_model, mock_controller, mock_view, mock_qapp, mock_pygame
    ):
        """Test that shutdown quits QApplication."""
        # Arrange
        mock_qapp.instance.return_value = None
        mock_qapp_instance = MagicMock()
        mock_qapp.return_value = mock_qapp_instance

        app = StarTrekRetroRemake()

        # Act
        app.shutdown()

        # Assert
        mock_qapp_instance.quit.assert_called_once()


class TestStarTrekRetroRemakeRun:
    """Test application run method."""

    @patch("src.game.application.sys.exit")
    @patch("src.game.application.pygame")
    @patch("src.game.application.QApplication")
    @patch("src.game.application.GameView")
    @patch("src.game.application.GameController")
    @patch("src.game.application.GameModel")
    def test_run_initializes_new_game(
        self, mock_model, mock_controller, mock_view, mock_qapp, mock_pygame, mock_exit
    ):
        """Test that run() calls controller.start_new_game()."""
        # Arrange
        mock_qapp.instance.return_value = None
        mock_qapp_instance = MagicMock()
        mock_qapp_instance.exec.return_value = 0
        mock_qapp.return_value = mock_qapp_instance
        mock_controller_instance = MagicMock()
        mock_controller.return_value = mock_controller_instance

        app = StarTrekRetroRemake()

        # Act
        app.run()

        # Assert
        mock_controller_instance.start_new_game.assert_called_once()

    @patch("src.game.application.sys.exit")
    @patch("src.game.application.pygame")
    @patch("src.game.application.QApplication")
    @patch("src.game.application.GameView")
    @patch("src.game.application.GameController")
    @patch("src.game.application.GameModel")
    def test_run_shows_view(
        self, mock_model, mock_controller, mock_view, mock_qapp, mock_pygame, mock_exit
    ):
        """Test that run() calls view.run()."""
        # Arrange
        mock_qapp.instance.return_value = None
        mock_qapp_instance = MagicMock()
        mock_qapp_instance.exec.return_value = 0
        mock_qapp.return_value = mock_qapp_instance
        mock_view_instance = MagicMock()
        mock_view.return_value = mock_view_instance

        app = StarTrekRetroRemake()

        # Act
        app.run()

        # Assert
        mock_view_instance.run.assert_called_once()

    @patch("src.game.application.sys.exit")
    @patch("src.game.application.pygame")
    @patch("src.game.application.QApplication")
    @patch("src.game.application.GameView")
    @patch("src.game.application.GameController")
    @patch("src.game.application.GameModel")
    def test_run_executes_qapplication_event_loop(
        self, mock_model, mock_controller, mock_view, mock_qapp, mock_pygame, mock_exit
    ):
        """Test that run() starts QApplication event loop."""
        # Arrange
        mock_qapp.instance.return_value = None
        mock_qapp_instance = MagicMock()
        mock_qapp_instance.exec.return_value = 0
        mock_qapp.return_value = mock_qapp_instance

        app = StarTrekRetroRemake()

        # Act
        app.run()

        # Assert
        mock_qapp_instance.exec.assert_called_once()
        mock_exit.assert_called_once_with(0)
