################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import QCoreApplication, QMetaObject, QRect, QSize, Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QDockWidget,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMenu,
    QMenuBar,
    QProgressBar,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QTabWidget,
    QToolBar,
    QVBoxLayout,
    QWidget,
)


class Ui_MainWindow:
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1600, 1000)
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
        self.actionSettings = QAction(MainWindow)
        self.actionSettings.setObjectName("actionSettings")
        self.actionNewGame = QAction(MainWindow)
        self.actionNewGame.setObjectName("actionNewGame")
        self.actionSaveGame = QAction(MainWindow)
        self.actionSaveGame.setObjectName("actionSaveGame")
        self.actionLoadGame = QAction(MainWindow)
        self.actionLoadGame.setObjectName("actionLoadGame")
        self.actionQuit = QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionToggleRightDock = QAction(MainWindow)
        self.actionToggleRightDock.setObjectName("actionToggleRightDock")
        self.actionToggleRightDock.setCheckable(True)
        self.actionToggleRightDock.setChecked(True)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralLayout = QVBoxLayout(self.centralwidget)
        self.centralLayout.setSpacing(0)
        self.centralLayout.setObjectName("centralLayout")
        self.centralLayout.setContentsMargins(0, 0, 0, 0)
        self.gameDisplay = QLabel(self.centralwidget)
        self.gameDisplay.setObjectName("gameDisplay")
        self.gameDisplay.setMinimumSize(QSize(800, 600))
        sizePolicy = QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
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
        self.endTurnButton.setMinimumSize(QSize(120, 30))
        self.endTurnButton.setStyleSheet(
            "background-color: #0066aa; color: white; font-weight: bold; border-radius: 5px;"
        )

        self.turnBarLayout.addWidget(self.endTurnButton)

        self.actionPointsLabel = QLabel(self.turnBar)
        self.actionPointsLabel.setObjectName("actionPointsLabel")
        self.actionPointsLabel.setStyleSheet(
            "color: #ffcc00; font-weight: bold; font-size: 14pt;"
        )

        self.turnBarLayout.addWidget(self.actionPointsLabel)

        self.turnBarSpacer = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        self.turnBarLayout.addItem(self.turnBarSpacer)

        self.phaseLabel = QLabel(self.turnBar)
        self.phaseLabel.setObjectName("phaseLabel")
        self.phaseLabel.setStyleSheet(
            "color: #00ff99; font-weight: bold; font-size: 14pt;"
        )

        self.turnBarLayout.addWidget(self.phaseLabel)

        self.turnNumberLabel = QLabel(self.turnBar)
        self.turnNumberLabel.setObjectName("turnNumberLabel")
        self.turnNumberLabel.setStyleSheet("color: #cccccc; font-size: 14pt;")

        self.turnBarLayout.addWidget(self.turnNumberLabel)

        self.centralLayout.addWidget(self.turnBar)

        MainWindow.setCentralWidget(self.centralwidget)
        self.mainToolBar = QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        self.mainToolBar.setMovable(False)
        self.mainToolBar.setIconSize(QSize(32, 32))
        MainWindow.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.mainToolBar)
        self.rightDock = QDockWidget(MainWindow)
        self.rightDock.setObjectName("rightDock")
        self.rightDock.setFeatures(
            QDockWidget.DockWidgetClosable
            | QDockWidget.DockWidgetMovable
            | QDockWidget.DockWidgetFloatable
        )
        self.rightDock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.rightDock.setMinimumSize(QSize(300, 0))
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.dockLayout = QVBoxLayout(self.dockWidgetContents)
        self.dockLayout.setSpacing(0)
        self.dockLayout.setObjectName("dockLayout")
        self.dockLayout.setContentsMargins(0, 0, 0, 0)
        self.controlTabWidget = QTabWidget(self.dockWidgetContents)
        self.controlTabWidget.setObjectName("controlTabWidget")
        self.statusTab = QWidget()
        self.statusTab.setObjectName("statusTab")
        self.statusTabLayout = QVBoxLayout(self.statusTab)
        self.statusTabLayout.setObjectName("statusTabLayout")
        self.shipStatusGroup = QGroupBox(self.statusTab)
        self.shipStatusGroup.setObjectName("shipStatusGroup")
        self.shipStatusFormLayout = QFormLayout(self.shipStatusGroup)
        self.shipStatusFormLayout.setObjectName("shipStatusFormLayout")
        self.shipNameLabelText = QLabel(self.shipStatusGroup)
        self.shipNameLabelText.setObjectName("shipNameLabelText")

        self.shipStatusFormLayout.setWidget(
            0, QFormLayout.ItemRole.LabelRole, self.shipNameLabelText
        )

        self.shipNameLabel = QLabel(self.shipStatusGroup)
        self.shipNameLabel.setObjectName("shipNameLabel")
        self.shipNameLabel.setStyleSheet("font-weight: bold; color: #00aaff;")

        self.shipStatusFormLayout.setWidget(
            0, QFormLayout.ItemRole.FieldRole, self.shipNameLabel
        )

        self.hullLabelText = QLabel(self.shipStatusGroup)
        self.hullLabelText.setObjectName("hullLabelText")

        self.shipStatusFormLayout.setWidget(
            1, QFormLayout.ItemRole.LabelRole, self.hullLabelText
        )

        self.hullProgressBar = QProgressBar(self.shipStatusGroup)
        self.hullProgressBar.setObjectName("hullProgressBar")
        self.hullProgressBar.setValue(100)
        self.hullProgressBar.setTextVisible(True)
        self.hullProgressBar.setStyleSheet(
            "QProgressBar::chunk { background-color: #00aa00; }"
        )

        self.shipStatusFormLayout.setWidget(
            1, QFormLayout.ItemRole.FieldRole, self.hullProgressBar
        )

        self.shieldsLabelText = QLabel(self.shipStatusGroup)
        self.shieldsLabelText.setObjectName("shieldsLabelText")

        self.shipStatusFormLayout.setWidget(
            2, QFormLayout.ItemRole.LabelRole, self.shieldsLabelText
        )

        self.shieldsProgressBar = QProgressBar(self.shipStatusGroup)
        self.shieldsProgressBar.setObjectName("shieldsProgressBar")
        self.shieldsProgressBar.setValue(100)
        self.shieldsProgressBar.setTextVisible(True)
        self.shieldsProgressBar.setStyleSheet(
            "QProgressBar::chunk { background-color: #0088ff; }"
        )

        self.shipStatusFormLayout.setWidget(
            2, QFormLayout.ItemRole.FieldRole, self.shieldsProgressBar
        )

        self.energyLabelText = QLabel(self.shipStatusGroup)
        self.energyLabelText.setObjectName("energyLabelText")

        self.shipStatusFormLayout.setWidget(
            3, QFormLayout.ItemRole.LabelRole, self.energyLabelText
        )

        self.energyProgressBar = QProgressBar(self.shipStatusGroup)
        self.energyProgressBar.setObjectName("energyProgressBar")
        self.energyProgressBar.setValue(100)
        self.energyProgressBar.setMaximum(5000)
        self.energyProgressBar.setTextVisible(True)
        self.energyProgressBar.setStyleSheet(
            "QProgressBar::chunk { background-color: #ffcc00; }"
        )

        self.shipStatusFormLayout.setWidget(
            3, QFormLayout.ItemRole.FieldRole, self.energyProgressBar
        )

        self.statusTabLayout.addWidget(self.shipStatusGroup)

        self.positionGroup = QGroupBox(self.statusTab)
        self.positionGroup.setObjectName("positionGroup")
        self.positionFormLayout = QFormLayout(self.positionGroup)
        self.positionFormLayout.setObjectName("positionFormLayout")
        self.coordinatesLabelText = QLabel(self.positionGroup)
        self.coordinatesLabelText.setObjectName("coordinatesLabelText")

        self.positionFormLayout.setWidget(
            0, QFormLayout.ItemRole.LabelRole, self.coordinatesLabelText
        )

        self.coordinatesLabel = QLabel(self.positionGroup)
        self.coordinatesLabel.setObjectName("coordinatesLabel")

        self.positionFormLayout.setWidget(
            0, QFormLayout.ItemRole.FieldRole, self.coordinatesLabel
        )

        self.sectorLabelText = QLabel(self.positionGroup)
        self.sectorLabelText.setObjectName("sectorLabelText")

        self.positionFormLayout.setWidget(
            1, QFormLayout.ItemRole.LabelRole, self.sectorLabelText
        )

        self.sectorLabel = QLabel(self.positionGroup)
        self.sectorLabel.setObjectName("sectorLabel")

        self.positionFormLayout.setWidget(
            1, QFormLayout.ItemRole.FieldRole, self.sectorLabel
        )

        self.statusTabLayout.addWidget(self.positionGroup)

        self.statusTabSpacer = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        self.statusTabLayout.addItem(self.statusTabSpacer)

        self.controlTabWidget.addTab(self.statusTab, "")
        self.actionsTab = QWidget()
        self.actionsTab.setObjectName("actionsTab")
        self.actionsTabLayout = QVBoxLayout(self.actionsTab)
        self.actionsTabLayout.setObjectName("actionsTabLayout")
        self.movementGroup = QGroupBox(self.actionsTab)
        self.movementGroup.setObjectName("movementGroup")
        self.movementLayout = QVBoxLayout(self.movementGroup)
        self.movementLayout.setObjectName("movementLayout")
        self.moveButton = QPushButton(self.movementGroup)
        self.moveButton.setObjectName("moveButton")
        self.moveButton.setMinimumSize(QSize(0, 30))

        self.movementLayout.addWidget(self.moveButton)

        self.rotateButton = QPushButton(self.movementGroup)
        self.rotateButton.setObjectName("rotateButton")
        self.rotateButton.setMinimumSize(QSize(0, 30))

        self.movementLayout.addWidget(self.rotateButton)

        self.actionsTabLayout.addWidget(self.movementGroup)

        self.combatGroup = QGroupBox(self.actionsTab)
        self.combatGroup.setObjectName("combatGroup")
        self.combatLayout = QVBoxLayout(self.combatGroup)
        self.combatLayout.setObjectName("combatLayout")
        self.fireButton = QPushButton(self.combatGroup)
        self.fireButton.setObjectName("fireButton")
        self.fireButton.setMinimumSize(QSize(0, 30))

        self.combatLayout.addWidget(self.fireButton)

        self.scanButton = QPushButton(self.combatGroup)
        self.scanButton.setObjectName("scanButton")
        self.scanButton.setMinimumSize(QSize(0, 30))

        self.combatLayout.addWidget(self.scanButton)

        self.evasiveButton = QPushButton(self.combatGroup)
        self.evasiveButton.setObjectName("evasiveButton")
        self.evasiveButton.setMinimumSize(QSize(0, 30))

        self.combatLayout.addWidget(self.evasiveButton)

        self.actionsTabLayout.addWidget(self.combatGroup)

        self.utilityGroup = QGroupBox(self.actionsTab)
        self.utilityGroup.setObjectName("utilityGroup")
        self.utilityLayout = QVBoxLayout(self.utilityGroup)
        self.utilityLayout.setObjectName("utilityLayout")
        self.dockButton = QPushButton(self.utilityGroup)
        self.dockButton.setObjectName("dockButton")
        self.dockButton.setMinimumSize(QSize(0, 30))

        self.utilityLayout.addWidget(self.dockButton)

        self.hailButton = QPushButton(self.utilityGroup)
        self.hailButton.setObjectName("hailButton")
        self.hailButton.setMinimumSize(QSize(0, 30))

        self.utilityLayout.addWidget(self.hailButton)

        self.actionsTabLayout.addWidget(self.utilityGroup)

        self.actionsTabSpacer = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        self.actionsTabLayout.addItem(self.actionsTabSpacer)

        self.controlTabWidget.addTab(self.actionsTab, "")
        self.mapTab = QWidget()
        self.mapTab.setObjectName("mapTab")
        self.mapTabLayout = QVBoxLayout(self.mapTab)
        self.mapTabLayout.setObjectName("mapTabLayout")
        self.minimapLabel = QLabel(self.mapTab)
        self.minimapLabel.setObjectName("minimapLabel")
        self.minimapLabel.setAlignment(Qt.AlignCenter)
        self.minimapLabel.setMinimumSize(QSize(250, 250))
        self.minimapLabel.setStyleSheet(
            "background-color: #1a1a2e; border: 2px solid #444; color: #888;"
        )

        self.mapTabLayout.addWidget(self.minimapLabel)

        self.legendGroup = QGroupBox(self.mapTab)
        self.legendGroup.setObjectName("legendGroup")
        self.legendLayout = QVBoxLayout(self.legendGroup)
        self.legendLayout.setObjectName("legendLayout")
        self.legendText = QLabel(self.legendGroup)
        self.legendText.setObjectName("legendText")
        self.legendText.setTextFormat(Qt.RichText)

        self.legendLayout.addWidget(self.legendText)

        self.mapTabLayout.addWidget(self.legendGroup)

        self.mapTabSpacer = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        self.mapTabLayout.addItem(self.mapTabSpacer)

        self.controlTabWidget.addTab(self.mapTab, "")

        self.dockLayout.addWidget(self.controlTabWidget)

        self.rightDock.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.rightDock)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName("menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 1600, 22))
        self.menuFile = QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        self.menuView = QMenu(self.menuBar)
        self.menuView.setObjectName("menuView")
        MainWindow.setMenuBar(self.menuBar)

        self.mainToolBar.addAction(self.actionGalaxyMode)
        self.mainToolBar.addAction(self.actionSectorMode)
        self.mainToolBar.addAction(self.actionCombatMode)
        self.mainToolBar.addSeparator()
        self.mainToolBar.addAction(self.actionZoomIn)
        self.mainToolBar.addAction(self.actionZoomOut)
        self.mainToolBar.addAction(self.actionZoomReset)
        self.mainToolBar.addSeparator()
        self.mainToolBar.addAction(self.actionSettings)
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuView.menuAction())
        self.menuFile.addAction(self.actionNewGame)
        self.menuFile.addAction(self.actionSaveGame)
        self.menuFile.addAction(self.actionLoadGame)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuView.addAction(self.actionToggleRightDock)

        self.retranslateUi(MainWindow)
        self.actionToggleRightDock.toggled.connect(self.rightDock.setVisible)

        self.controlTabWidget.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QCoreApplication.translate("MainWindow", "Star Trek Retro Remake", None)
        )
        self.actionGalaxyMode.setText(
            QCoreApplication.translate("MainWindow", "Galaxy", None)
        )
        # if QT_CONFIG(tooltip)
        self.actionGalaxyMode.setToolTip(
            QCoreApplication.translate("MainWindow", "Switch to Galaxy Map Mode", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.actionSectorMode.setText(
            QCoreApplication.translate("MainWindow", "Sector", None)
        )
        # if QT_CONFIG(tooltip)
        self.actionSectorMode.setToolTip(
            QCoreApplication.translate("MainWindow", "Switch to Sector Map Mode", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.actionCombatMode.setText(
            QCoreApplication.translate("MainWindow", "Combat", None)
        )
        # if QT_CONFIG(tooltip)
        self.actionCombatMode.setToolTip(
            QCoreApplication.translate("MainWindow", "Switch to Combat Mode", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.actionZoomIn.setText(
            QCoreApplication.translate("MainWindow", "Zoom In", None)
        )
        # if QT_CONFIG(tooltip)
        self.actionZoomIn.setToolTip(
            QCoreApplication.translate("MainWindow", "Zoom in on the map", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.actionZoomOut.setText(
            QCoreApplication.translate("MainWindow", "Zoom Out", None)
        )
        # if QT_CONFIG(tooltip)
        self.actionZoomOut.setToolTip(
            QCoreApplication.translate("MainWindow", "Zoom out on the map", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.actionZoomReset.setText(
            QCoreApplication.translate("MainWindow", "Reset Zoom", None)
        )
        # if QT_CONFIG(tooltip)
        self.actionZoomReset.setToolTip(
            QCoreApplication.translate("MainWindow", "Reset zoom to 100%", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.actionSettings.setText(
            QCoreApplication.translate("MainWindow", "Settings", None)
        )
        # if QT_CONFIG(tooltip)
        self.actionSettings.setToolTip(
            QCoreApplication.translate("MainWindow", "Open Settings Dialog", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.actionNewGame.setText(
            QCoreApplication.translate("MainWindow", "New Game", None)
        )
        self.actionSaveGame.setText(
            QCoreApplication.translate("MainWindow", "Save Game", None)
        )
        self.actionLoadGame.setText(
            QCoreApplication.translate("MainWindow", "Load Game", None)
        )
        self.actionQuit.setText(QCoreApplication.translate("MainWindow", "Quit", None))
        self.actionToggleRightDock.setText(
            QCoreApplication.translate("MainWindow", "Toggle Control Center", None)
        )
        self.gameDisplay.setText("")
        self.endTurnButton.setText(
            QCoreApplication.translate("MainWindow", "End Turn", None)
        )
        self.actionPointsLabel.setText(
            QCoreApplication.translate("MainWindow", "Action Points: 10", None)
        )
        self.phaseLabel.setText(
            QCoreApplication.translate("MainWindow", "Phase: Planning", None)
        )
        self.turnNumberLabel.setText(
            QCoreApplication.translate("MainWindow", "Turn: 1", None)
        )
        self.mainToolBar.setWindowTitle(
            QCoreApplication.translate("MainWindow", "Main Toolbar", None)
        )
        self.rightDock.setWindowTitle(
            QCoreApplication.translate("MainWindow", "Control Center", None)
        )
        self.shipStatusGroup.setTitle(
            QCoreApplication.translate("MainWindow", "Ship Status", None)
        )
        self.shipNameLabelText.setText(
            QCoreApplication.translate("MainWindow", "Ship:", None)
        )
        self.shipNameLabel.setText(
            QCoreApplication.translate("MainWindow", "USS Enterprise", None)
        )
        self.hullLabelText.setText(
            QCoreApplication.translate("MainWindow", "Hull:", None)
        )
        self.hullProgressBar.setFormat(
            QCoreApplication.translate("MainWindow", "%p%", None)
        )
        self.shieldsLabelText.setText(
            QCoreApplication.translate("MainWindow", "Shields:", None)
        )
        self.shieldsProgressBar.setFormat(
            QCoreApplication.translate("MainWindow", "%p%", None)
        )
        self.energyLabelText.setText(
            QCoreApplication.translate("MainWindow", "Energy:", None)
        )
        self.energyProgressBar.setFormat(
            QCoreApplication.translate("MainWindow", "%v / %m", None)
        )
        self.positionGroup.setTitle(
            QCoreApplication.translate("MainWindow", "Position", None)
        )
        self.coordinatesLabelText.setText(
            QCoreApplication.translate("MainWindow", "Coordinates:", None)
        )
        self.coordinatesLabel.setText(
            QCoreApplication.translate("MainWindow", "X: 10, Y: 10, Z: 2", None)
        )
        self.sectorLabelText.setText(
            QCoreApplication.translate("MainWindow", "Sector:", None)
        )
        self.sectorLabel.setText(
            QCoreApplication.translate("MainWindow", "Sol System", None)
        )
        self.controlTabWidget.setTabText(
            self.controlTabWidget.indexOf(self.statusTab),
            QCoreApplication.translate("MainWindow", "Status", None),
        )
        self.movementGroup.setTitle(
            QCoreApplication.translate("MainWindow", "Movement", None)
        )
        self.moveButton.setText(
            QCoreApplication.translate("MainWindow", "Move Ship", None)
        )
        self.rotateButton.setText(
            QCoreApplication.translate("MainWindow", "Rotate", None)
        )
        self.combatGroup.setTitle(
            QCoreApplication.translate("MainWindow", "Combat", None)
        )
        self.fireButton.setText(
            QCoreApplication.translate("MainWindow", "Fire Weapons", None)
        )
        self.scanButton.setText(
            QCoreApplication.translate("MainWindow", "Scan Target", None)
        )
        self.evasiveButton.setText(
            QCoreApplication.translate("MainWindow", "Evasive Maneuvers", None)
        )
        self.utilityGroup.setTitle(
            QCoreApplication.translate("MainWindow", "Utilities", None)
        )
        self.dockButton.setText(
            QCoreApplication.translate("MainWindow", "Dock at Station", None)
        )
        self.hailButton.setText(
            QCoreApplication.translate("MainWindow", "Hail Ship", None)
        )
        self.controlTabWidget.setTabText(
            self.controlTabWidget.indexOf(self.actionsTab),
            QCoreApplication.translate("MainWindow", "Actions", None),
        )
        self.minimapLabel.setText(
            QCoreApplication.translate("MainWindow", "Mini-Map", None)
        )
        self.legendGroup.setTitle(
            QCoreApplication.translate("MainWindow", "Legend", None)
        )
        self.legendText.setText(
            QCoreApplication.translate(
                "MainWindow",
                "<html><body>\n"
                "<p><span style='color:#00aaff;'>\u25a0</span> Player Ship</p>\n"
                "<p><span style='color:#ff0000;'>\u25a0</span> Enemy Ship</p>\n"
                "<p><span style='color:#ffaa00;'>\u25a0</span> Station</p>\n"
                "<p><span style='color:#888888;'>\u25a0</span> Asteroid</p>\n"
                "</body></html>",
                None,
            )
        )
        self.controlTabWidget.setTabText(
            self.controlTabWidget.indexOf(self.mapTab),
            QCoreApplication.translate("MainWindow", "Map", None),
        )
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", "File", None))
        self.menuView.setTitle(QCoreApplication.translate("MainWindow", "View", None))

    # retranslateUi
