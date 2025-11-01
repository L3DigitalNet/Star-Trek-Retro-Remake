################################################################################
## Form generated from reading UI file 'main_window_complete.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QMetaObject,
    QRect,
    QSize,
    Qt,
)
from PySide6.QtGui import (
    QAction,
)
from PySide6.QtWidgets import (
    QDockWidget,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMenu,
    QMenuBar,
    QProgressBar,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QStatusBar,
    QToolBar,
    QVBoxLayout,
    QWidget,
)


class Ui_MainWindow:
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1600, 1000)
        MainWindow.setStyleSheet(
            "\n"
            "    QMainWindow {\n"
            "        background-color: #1a1a2e;\n"
            "    }\n"
            "    QDockWidget {\n"
            "        background-color: #2a2a2a;\n"
            "        color: #ffffff;\n"
            "        font-size: 12px;\n"
            "    }\n"
            "    QDockWidget::title {\n"
            "        background-color: #333;\n"
            "        padding: 5px;\n"
            "        text-align: center;\n"
            "    }\n"
            "    QPushButton {\n"
            "        background-color: #444;\n"
            "        color: #ffffff;\n"
            "        border: 1px solid #666;\n"
            "        padding: 5px 15px;\n"
            "        min-height: 25px;\n"
            "        border-radius: 3px;\n"
            "    }\n"
            "    QPushButton:hover {\n"
            "        background-color: #555;\n"
            "    }\n"
            "    QPushButton:pressed {\n"
            "        background-color: #333;\n"
            "    }\n"
            "    QLabel {\n"
            "        color: #ffffff;\n"
            "    }\n"
            "    QProgressBar {\n"
            "        border: 1px solid #666;\n"
            "        border-radius: 3px;\n"
            "        text-align: center;\n"
            "        background-color: #333;\n"
            "        color: #ffffff;\n"
            "    }\n"
            "    QProgressBar::chunk {\n"
            "        background-color: #4CAF"
            "50;\n"
            "    }\n"
            "   "
        )
        self.actionNewGame = QAction(MainWindow)
        self.actionNewGame.setObjectName("actionNewGame")
        self.actionSaveGame = QAction(MainWindow)
        self.actionSaveGame.setObjectName("actionSaveGame")
        self.actionLoadGame = QAction(MainWindow)
        self.actionLoadGame.setObjectName("actionLoadGame")
        self.actionQuit = QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionGalaxyMode = QAction(MainWindow)
        self.actionGalaxyMode.setObjectName("actionGalaxyMode")
        self.actionSectorMode = QAction(MainWindow)
        self.actionSectorMode.setObjectName("actionSectorMode")
        self.actionCombatMode = QAction(MainWindow)
        self.actionCombatMode.setObjectName("actionCombatMode")
        self.actionZoomIn = QAction(MainWindow)
        self.actionZoomIn.setObjectName("actionZoomIn")
        self.actionZoomOut = QAction(MainWindow)
        self.actionZoomOut.setObjectName("actionZoomOut")
        self.actionZoomReset = QAction(MainWindow)
        self.actionZoomReset.setObjectName("actionZoomReset")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralLayout = QVBoxLayout(self.centralwidget)
        self.centralLayout.setSpacing(0)
        self.centralLayout.setObjectName("centralLayout")
        self.centralLayout.setContentsMargins(0, 0, 0, 0)
        self.gameDisplay = QLabel(self.centralwidget)
        self.gameDisplay.setObjectName("gameDisplay")
        self.gameDisplay.setMinimumSize(QSize(1280, 900))
        self.gameDisplay.setMaximumSize(QSize(1280, 900))
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gameDisplay.sizePolicy().hasHeightForWidth())
        self.gameDisplay.setSizePolicy(sizePolicy)
        self.gameDisplay.setAlignment(Qt.AlignCenter)
        self.gameDisplay.setStyleSheet(
            "background-color: #1a1a2e; border: 2px solid #333;"
        )

        self.centralLayout.addWidget(self.gameDisplay)

        self.turnBar = QWidget(self.centralwidget)
        self.turnBar.setObjectName("turnBar")
        self.turnBar.setMinimumSize(QSize(0, 50))
        self.turnBar.setMaximumSize(QSize(16777215, 50))
        self.turnBar.setStyleSheet(
            "background-color: #2a2a2a; border-top: 2px solid #444;"
        )
        self.turnBarLayout = QHBoxLayout(self.turnBar)
        self.turnBarLayout.setSpacing(10)
        self.turnBarLayout.setObjectName("turnBarLayout")
        self.turnBarLayout.setContentsMargins(10, 5, 10, 5)
        self.endTurnButton = QPushButton(self.turnBar)
        self.endTurnButton.setObjectName("endTurnButton")
        self.endTurnButton.setMinimumSize(QSize(100, 30))

        self.turnBarLayout.addWidget(self.endTurnButton)

        self.turnNumberLabel = QLabel(self.turnBar)
        self.turnNumberLabel.setObjectName("turnNumberLabel")
        self.turnNumberLabel.setMinimumWidth(80)

        self.turnBarLayout.addWidget(self.turnNumberLabel)

        self.phaseLabel = QLabel(self.turnBar)
        self.phaseLabel.setObjectName("phaseLabel")
        self.phaseLabel.setMinimumWidth(120)

        self.turnBarLayout.addWidget(self.phaseLabel)

        self.actionPointsLabel = QLabel(self.turnBar)
        self.actionPointsLabel.setObjectName("actionPointsLabel")
        self.actionPointsLabel.setMinimumWidth(60)

        self.turnBarLayout.addWidget(self.actionPointsLabel)

        self.horizontalSpacer = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        self.turnBarLayout.addItem(self.horizontalSpacer)

        self.centralLayout.addWidget(self.turnBar)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName("menubar")
        self.menubar.setGeometry(QRect(0, 0, 1600, 24))
        self.menuGame = QMenu(self.menubar)
        self.menuGame.setObjectName("menuGame")
        self.menuView = QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.mainToolBar = QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        self.mainToolBar.setMovable(False)
        MainWindow.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.mainToolBar)
        self.rightDock = QDockWidget(MainWindow)
        self.rightDock.setObjectName("rightDock")
        self.rightDock.setFeatures(QDockWidget.DockWidgetMovable)
        self.rightDock.setAllowedAreas(Qt.RightDockWidgetArea)
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.rightDockLayout = QVBoxLayout(self.dockWidgetContents)
        self.rightDockLayout.setSpacing(10)
        self.rightDockLayout.setObjectName("rightDockLayout")
        self.rightDockLayout.setContentsMargins(10, 10, 10, 10)
        self.shipNameLabel = QLabel(self.dockWidgetContents)
        self.shipNameLabel.setObjectName("shipNameLabel")
        self.shipNameLabel.setStyleSheet(
            "font-size: 16px; font-weight: bold; color: #4CAF50;"
        )
        self.shipNameLabel.setAlignment(Qt.AlignCenter)

        self.rightDockLayout.addWidget(self.shipNameLabel)

        self.line1 = QFrame(self.dockWidgetContents)
        self.line1.setObjectName("line1")
        self.line1.setFrameShape(QFrame.Shape.HLine)
        self.line1.setFrameShadow(QFrame.Shadow.Sunken)

        self.rightDockLayout.addWidget(self.line1)

        self.hullLabel = QLabel(self.dockWidgetContents)
        self.hullLabel.setObjectName("hullLabel")

        self.rightDockLayout.addWidget(self.hullLabel)

        self.hullProgressBar = QProgressBar(self.dockWidgetContents)
        self.hullProgressBar.setObjectName("hullProgressBar")
        self.hullProgressBar.setValue(100)
        self.hullProgressBar.setTextVisible(True)

        self.rightDockLayout.addWidget(self.hullProgressBar)

        self.shieldsLabel = QLabel(self.dockWidgetContents)
        self.shieldsLabel.setObjectName("shieldsLabel")

        self.rightDockLayout.addWidget(self.shieldsLabel)

        self.shieldsProgressBar = QProgressBar(self.dockWidgetContents)
        self.shieldsProgressBar.setObjectName("shieldsProgressBar")
        self.shieldsProgressBar.setValue(100)
        self.shieldsProgressBar.setTextVisible(True)
        self.shieldsProgressBar.setStyleSheet(
            "QProgressBar::chunk { background-color: #2196F3; }"
        )

        self.rightDockLayout.addWidget(self.shieldsProgressBar)

        self.energyLabel = QLabel(self.dockWidgetContents)
        self.energyLabel.setObjectName("energyLabel")

        self.rightDockLayout.addWidget(self.energyLabel)

        self.energyProgressBar = QProgressBar(self.dockWidgetContents)
        self.energyProgressBar.setObjectName("energyProgressBar")
        self.energyProgressBar.setValue(100)
        self.energyProgressBar.setTextVisible(True)
        self.energyProgressBar.setStyleSheet(
            "QProgressBar::chunk { background-color: #FF9800; }"
        )

        self.rightDockLayout.addWidget(self.energyProgressBar)

        self.line2 = QFrame(self.dockWidgetContents)
        self.line2.setObjectName("line2")
        self.line2.setFrameShape(QFrame.Shape.HLine)
        self.line2.setFrameShadow(QFrame.Shadow.Sunken)

        self.rightDockLayout.addWidget(self.line2)

        self.coordinatesLabel = QLabel(self.dockWidgetContents)
        self.coordinatesLabel.setObjectName("coordinatesLabel")

        self.rightDockLayout.addWidget(self.coordinatesLabel)

        self.sectorLabel = QLabel(self.dockWidgetContents)
        self.sectorLabel.setObjectName("sectorLabel")

        self.rightDockLayout.addWidget(self.sectorLabel)

        self.line3 = QFrame(self.dockWidgetContents)
        self.line3.setObjectName("line3")
        self.line3.setFrameShape(QFrame.Shape.HLine)
        self.line3.setFrameShadow(QFrame.Shadow.Sunken)

        self.rightDockLayout.addWidget(self.line3)

        self.actionsLabel = QLabel(self.dockWidgetContents)
        self.actionsLabel.setObjectName("actionsLabel")
        self.actionsLabel.setStyleSheet("font-weight: bold;")

        self.rightDockLayout.addWidget(self.actionsLabel)

        self.moveButton = QPushButton(self.dockWidgetContents)
        self.moveButton.setObjectName("moveButton")

        self.rightDockLayout.addWidget(self.moveButton)

        self.rotateButton = QPushButton(self.dockWidgetContents)
        self.rotateButton.setObjectName("rotateButton")

        self.rightDockLayout.addWidget(self.rotateButton)

        self.fireButton = QPushButton(self.dockWidgetContents)
        self.fireButton.setObjectName("fireButton")

        self.rightDockLayout.addWidget(self.fireButton)

        self.scanButton = QPushButton(self.dockWidgetContents)
        self.scanButton.setObjectName("scanButton")

        self.rightDockLayout.addWidget(self.scanButton)

        self.evasiveButton = QPushButton(self.dockWidgetContents)
        self.evasiveButton.setObjectName("evasiveButton")

        self.rightDockLayout.addWidget(self.evasiveButton)

        self.dockButton = QPushButton(self.dockWidgetContents)
        self.dockButton.setObjectName("dockButton")

        self.rightDockLayout.addWidget(self.dockButton)

        self.hailButton = QPushButton(self.dockWidgetContents)
        self.hailButton.setObjectName("hailButton")

        self.rightDockLayout.addWidget(self.hailButton)

        self.verticalSpacer = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        self.rightDockLayout.addItem(self.verticalSpacer)

        self.rightDock.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.rightDock)

        self.menubar.addAction(self.menuGame.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menuGame.addAction(self.actionNewGame)
        self.menuGame.addAction(self.actionSaveGame)
        self.menuGame.addAction(self.actionLoadGame)
        self.menuGame.addSeparator()
        self.menuGame.addAction(self.actionQuit)
        self.menuView.addAction(self.actionGalaxyMode)
        self.menuView.addAction(self.actionSectorMode)
        self.menuView.addAction(self.actionCombatMode)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionZoomIn)
        self.menuView.addAction(self.actionZoomOut)
        self.menuView.addAction(self.actionZoomReset)
        self.mainToolBar.addAction(self.actionGalaxyMode)
        self.mainToolBar.addAction(self.actionSectorMode)
        self.mainToolBar.addAction(self.actionCombatMode)
        self.mainToolBar.addSeparator()
        self.mainToolBar.addAction(self.actionZoomIn)
        self.mainToolBar.addAction(self.actionZoomOut)
        self.mainToolBar.addAction(self.actionZoomReset)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QCoreApplication.translate("MainWindow", "Star Trek Retro Remake", None)
        )
        self.actionNewGame.setText(
            QCoreApplication.translate("MainWindow", "New Game", None)
        )
        # if QT_CONFIG(shortcut)
        self.actionNewGame.setShortcut(
            QCoreApplication.translate("MainWindow", "Ctrl+N", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.actionSaveGame.setText(
            QCoreApplication.translate("MainWindow", "Save Game", None)
        )
        # if QT_CONFIG(shortcut)
        self.actionSaveGame.setShortcut(
            QCoreApplication.translate("MainWindow", "Ctrl+S", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.actionLoadGame.setText(
            QCoreApplication.translate("MainWindow", "Load Game", None)
        )
        # if QT_CONFIG(shortcut)
        self.actionLoadGame.setShortcut(
            QCoreApplication.translate("MainWindow", "Ctrl+O", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.actionQuit.setText(QCoreApplication.translate("MainWindow", "Quit", None))
        # if QT_CONFIG(shortcut)
        self.actionQuit.setShortcut(
            QCoreApplication.translate("MainWindow", "Ctrl+Q", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.actionGalaxyMode.setText(
            QCoreApplication.translate("MainWindow", "Galaxy Map", None)
        )
        # if QT_CONFIG(tooltip)
        self.actionGalaxyMode.setToolTip(
            QCoreApplication.translate("MainWindow", "Switch to Galaxy Map view", None)
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(shortcut)
        self.actionGalaxyMode.setShortcut(
            QCoreApplication.translate("MainWindow", "F1", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.actionSectorMode.setText(
            QCoreApplication.translate("MainWindow", "Sector Map", None)
        )
        # if QT_CONFIG(tooltip)
        self.actionSectorMode.setToolTip(
            QCoreApplication.translate("MainWindow", "Switch to Sector Map view", None)
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(shortcut)
        self.actionSectorMode.setShortcut(
            QCoreApplication.translate("MainWindow", "F2", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.actionCombatMode.setText(
            QCoreApplication.translate("MainWindow", "Combat Mode", None)
        )
        # if QT_CONFIG(tooltip)
        self.actionCombatMode.setToolTip(
            QCoreApplication.translate("MainWindow", "Switch to Combat view", None)
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(shortcut)
        self.actionCombatMode.setShortcut(
            QCoreApplication.translate("MainWindow", "F3", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.actionZoomIn.setText(
            QCoreApplication.translate("MainWindow", "Zoom In", None)
        )
        # if QT_CONFIG(tooltip)
        self.actionZoomIn.setToolTip(
            QCoreApplication.translate("MainWindow", "Zoom in on the map", None)
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(shortcut)
        self.actionZoomIn.setShortcut(
            QCoreApplication.translate("MainWindow", "+", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.actionZoomOut.setText(
            QCoreApplication.translate("MainWindow", "Zoom Out", None)
        )
        # if QT_CONFIG(tooltip)
        self.actionZoomOut.setToolTip(
            QCoreApplication.translate("MainWindow", "Zoom out on the map", None)
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(shortcut)
        self.actionZoomOut.setShortcut(
            QCoreApplication.translate("MainWindow", "-", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.actionZoomReset.setText(
            QCoreApplication.translate("MainWindow", "Reset Zoom", None)
        )
        # if QT_CONFIG(tooltip)
        self.actionZoomReset.setToolTip(
            QCoreApplication.translate(
                "MainWindow", "Reset zoom to default level", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(shortcut)
        self.actionZoomReset.setShortcut(
            QCoreApplication.translate("MainWindow", "0", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.gameDisplay.setText("")
        self.endTurnButton.setText(
            QCoreApplication.translate("MainWindow", "End Turn", None)
        )
        self.turnNumberLabel.setText(
            QCoreApplication.translate("MainWindow", "Turn: 1", None)
        )
        self.phaseLabel.setText(
            QCoreApplication.translate("MainWindow", "Phase: Movement", None)
        )
        self.actionPointsLabel.setText(
            QCoreApplication.translate("MainWindow", "AP: 5", None)
        )
        self.menuGame.setTitle(QCoreApplication.translate("MainWindow", "Game", None))
        self.menuView.setTitle(QCoreApplication.translate("MainWindow", "View", None))
        self.mainToolBar.setWindowTitle(
            QCoreApplication.translate("MainWindow", "Main Toolbar", None)
        )
        self.rightDock.setWindowTitle(
            QCoreApplication.translate("MainWindow", "Ship Status", None)
        )
        self.shipNameLabel.setText(
            QCoreApplication.translate("MainWindow", "U.S.S. Enterprise", None)
        )
        self.hullLabel.setText(
            QCoreApplication.translate("MainWindow", "Hull Integrity:", None)
        )
        self.hullProgressBar.setFormat(
            QCoreApplication.translate("MainWindow", "%p%", None)
        )
        self.shieldsLabel.setText(
            QCoreApplication.translate("MainWindow", "Shields:", None)
        )
        self.shieldsProgressBar.setFormat(
            QCoreApplication.translate("MainWindow", "%p%", None)
        )
        self.energyLabel.setText(
            QCoreApplication.translate("MainWindow", "Energy:", None)
        )
        self.energyProgressBar.setFormat(
            QCoreApplication.translate("MainWindow", "%p%", None)
        )
        self.coordinatesLabel.setText(
            QCoreApplication.translate("MainWindow", "X: 0, Y: 0, Z: 0", None)
        )
        self.sectorLabel.setText(
            QCoreApplication.translate("MainWindow", "Sector: Unknown", None)
        )
        self.actionsLabel.setText(
            QCoreApplication.translate("MainWindow", "Ship Actions:", None)
        )
        self.moveButton.setText(
            QCoreApplication.translate("MainWindow", "Move Ship", None)
        )
        # if QT_CONFIG(tooltip)
        self.moveButton.setToolTip(
            QCoreApplication.translate(
                "MainWindow", "Move ship to a new location (1 AP)", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.rotateButton.setText(
            QCoreApplication.translate("MainWindow", "Rotate Ship", None)
        )
        # if QT_CONFIG(tooltip)
        self.rotateButton.setToolTip(
            QCoreApplication.translate(
                "MainWindow", "Change ship orientation (1 AP)", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.fireButton.setText(
            QCoreApplication.translate("MainWindow", "Fire Weapons", None)
        )
        # if QT_CONFIG(tooltip)
        self.fireButton.setToolTip(
            QCoreApplication.translate(
                "MainWindow", "Fire phasers (1 AP) or torpedoes (2 AP)", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.scanButton.setText(
            QCoreApplication.translate("MainWindow", "Scan Target", None)
        )
        # if QT_CONFIG(tooltip)
        self.scanButton.setToolTip(
            QCoreApplication.translate(
                "MainWindow", "Scan selected target for details (1 AP)", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.evasiveButton.setText(
            QCoreApplication.translate("MainWindow", "Evasive Maneuvers", None)
        )
        # if QT_CONFIG(tooltip)
        self.evasiveButton.setToolTip(
            QCoreApplication.translate(
                "MainWindow", "Execute evasive pattern (1 AP)", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.dockButton.setText(
            QCoreApplication.translate("MainWindow", "Dock at Station", None)
        )
        # if QT_CONFIG(tooltip)
        self.dockButton.setToolTip(
            QCoreApplication.translate("MainWindow", "Initiate docking procedure", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.hailButton.setText(
            QCoreApplication.translate("MainWindow", "Hail Ship", None)
        )
        # if QT_CONFIG(tooltip)
        self.hailButton.setToolTip(
            QCoreApplication.translate("MainWindow", "Open communication channel", None)
        )


# endif // QT_CONFIG(tooltip)
# retranslateUi
