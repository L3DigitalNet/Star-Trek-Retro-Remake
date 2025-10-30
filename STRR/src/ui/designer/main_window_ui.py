# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QDockWidget, QFormLayout, QGroupBox,
    QHBoxLayout, QLabel, QMainWindow, QMenu,
    QMenuBar, QProgressBar, QPushButton, QSizePolicy,
    QSpacerItem, QTabWidget, QToolBar, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1600, 1000)
        self.actionGalaxyMode = QAction(MainWindow)
        self.actionGalaxyMode.setObjectName(u"actionGalaxyMode")
        self.actionSectorMode = QAction(MainWindow)
        self.actionSectorMode.setObjectName(u"actionSectorMode")
        self.actionCombatMode = QAction(MainWindow)
        self.actionCombatMode.setObjectName(u"actionCombatMode")
        self.actionZoomIn = QAction(MainWindow)
        self.actionZoomIn.setObjectName(u"actionZoomIn")
        self.actionZoomOut = QAction(MainWindow)
        self.actionZoomOut.setObjectName(u"actionZoomOut")
        self.actionZoomReset = QAction(MainWindow)
        self.actionZoomReset.setObjectName(u"actionZoomReset")
        self.actionSettings = QAction(MainWindow)
        self.actionSettings.setObjectName(u"actionSettings")
        self.actionNewGame = QAction(MainWindow)
        self.actionNewGame.setObjectName(u"actionNewGame")
        self.actionSaveGame = QAction(MainWindow)
        self.actionSaveGame.setObjectName(u"actionSaveGame")
        self.actionLoadGame = QAction(MainWindow)
        self.actionLoadGame.setObjectName(u"actionLoadGame")
        self.actionQuit = QAction(MainWindow)
        self.actionQuit.setObjectName(u"actionQuit")
        self.actionToggleRightDock = QAction(MainWindow)
        self.actionToggleRightDock.setObjectName(u"actionToggleRightDock")
        self.actionToggleRightDock.setCheckable(True)
        self.actionToggleRightDock.setChecked(True)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralLayout = QVBoxLayout(self.centralwidget)
        self.centralLayout.setSpacing(0)
        self.centralLayout.setObjectName(u"centralLayout")
        self.centralLayout.setContentsMargins(0, 0, 0, 0)
        self.gameDisplay = QLabel(self.centralwidget)
        self.gameDisplay.setObjectName(u"gameDisplay")
        self.gameDisplay.setMinimumSize(QSize(800, 600))
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.gameDisplay.sizePolicy().hasHeightForWidth())
        self.gameDisplay.setSizePolicy(sizePolicy)
        self.gameDisplay.setAlignment(Qt.AlignCenter)
        self.gameDisplay.setStyleSheet(u"background-color: #1a1a2e; border: 2px solid #333;")

        self.centralLayout.addWidget(self.gameDisplay)

        self.turnBar = QWidget(self.centralwidget)
        self.turnBar.setObjectName(u"turnBar")
        self.turnBar.setMinimumSize(QSize(0, 50))
        self.turnBar.setMaximumSize(QSize(16777215, 50))
        self.turnBar.setStyleSheet(u"background-color: #2a2a2a; border-top: 2px solid #444;")
        self.turnBarLayout = QHBoxLayout(self.turnBar)
        self.turnBarLayout.setSpacing(10)
        self.turnBarLayout.setObjectName(u"turnBarLayout")
        self.turnBarLayout.setContentsMargins(10, 5, 10, 5)
        self.endTurnButton = QPushButton(self.turnBar)
        self.endTurnButton.setObjectName(u"endTurnButton")
        self.endTurnButton.setMinimumSize(QSize(120, 30))
        self.endTurnButton.setStyleSheet(u"background-color: #0066aa; color: white; font-weight: bold; border-radius: 5px;")

        self.turnBarLayout.addWidget(self.endTurnButton)

        self.actionPointsLabel = QLabel(self.turnBar)
        self.actionPointsLabel.setObjectName(u"actionPointsLabel")
        self.actionPointsLabel.setStyleSheet(u"color: #ffcc00; font-weight: bold; font-size: 14pt;")

        self.turnBarLayout.addWidget(self.actionPointsLabel)

        self.turnBarSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.turnBarLayout.addItem(self.turnBarSpacer)

        self.phaseLabel = QLabel(self.turnBar)
        self.phaseLabel.setObjectName(u"phaseLabel")
        self.phaseLabel.setStyleSheet(u"color: #00ff99; font-weight: bold; font-size: 14pt;")

        self.turnBarLayout.addWidget(self.phaseLabel)

        self.turnNumberLabel = QLabel(self.turnBar)
        self.turnNumberLabel.setObjectName(u"turnNumberLabel")
        self.turnNumberLabel.setStyleSheet(u"color: #cccccc; font-size: 14pt;")

        self.turnBarLayout.addWidget(self.turnNumberLabel)


        self.centralLayout.addWidget(self.turnBar)

        MainWindow.setCentralWidget(self.centralwidget)
        self.mainToolBar = QToolBar(MainWindow)
        self.mainToolBar.setObjectName(u"mainToolBar")
        self.mainToolBar.setMovable(False)
        self.mainToolBar.setIconSize(QSize(32, 32))
        MainWindow.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.mainToolBar)
        self.rightDock = QDockWidget(MainWindow)
        self.rightDock.setObjectName(u"rightDock")
        self.rightDock.setFeatures(QDockWidget.DockWidgetClosable|QDockWidget.DockWidgetMovable|QDockWidget.DockWidgetFloatable)
        self.rightDock.setAllowedAreas(Qt.LeftDockWidgetArea|Qt.RightDockWidgetArea)
        self.rightDock.setMinimumSize(QSize(300, 0))
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName(u"dockWidgetContents")
        self.dockLayout = QVBoxLayout(self.dockWidgetContents)
        self.dockLayout.setSpacing(0)
        self.dockLayout.setObjectName(u"dockLayout")
        self.dockLayout.setContentsMargins(0, 0, 0, 0)
        self.controlTabWidget = QTabWidget(self.dockWidgetContents)
        self.controlTabWidget.setObjectName(u"controlTabWidget")
        self.statusTab = QWidget()
        self.statusTab.setObjectName(u"statusTab")
        self.statusTabLayout = QVBoxLayout(self.statusTab)
        self.statusTabLayout.setObjectName(u"statusTabLayout")
        self.shipStatusGroup = QGroupBox(self.statusTab)
        self.shipStatusGroup.setObjectName(u"shipStatusGroup")
        self.shipStatusFormLayout = QFormLayout(self.shipStatusGroup)
        self.shipStatusFormLayout.setObjectName(u"shipStatusFormLayout")
        self.shipNameLabelText = QLabel(self.shipStatusGroup)
        self.shipNameLabelText.setObjectName(u"shipNameLabelText")

        self.shipStatusFormLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.shipNameLabelText)

        self.shipNameLabel = QLabel(self.shipStatusGroup)
        self.shipNameLabel.setObjectName(u"shipNameLabel")
        self.shipNameLabel.setStyleSheet(u"font-weight: bold; color: #00aaff;")

        self.shipStatusFormLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.shipNameLabel)

        self.hullLabelText = QLabel(self.shipStatusGroup)
        self.hullLabelText.setObjectName(u"hullLabelText")

        self.shipStatusFormLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.hullLabelText)

        self.hullProgressBar = QProgressBar(self.shipStatusGroup)
        self.hullProgressBar.setObjectName(u"hullProgressBar")
        self.hullProgressBar.setValue(100)
        self.hullProgressBar.setTextVisible(True)
        self.hullProgressBar.setStyleSheet(u"QProgressBar::chunk { background-color: #00aa00; }")

        self.shipStatusFormLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.hullProgressBar)

        self.shieldsLabelText = QLabel(self.shipStatusGroup)
        self.shieldsLabelText.setObjectName(u"shieldsLabelText")

        self.shipStatusFormLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.shieldsLabelText)

        self.shieldsProgressBar = QProgressBar(self.shipStatusGroup)
        self.shieldsProgressBar.setObjectName(u"shieldsProgressBar")
        self.shieldsProgressBar.setValue(100)
        self.shieldsProgressBar.setTextVisible(True)
        self.shieldsProgressBar.setStyleSheet(u"QProgressBar::chunk { background-color: #0088ff; }")

        self.shipStatusFormLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.shieldsProgressBar)

        self.energyLabelText = QLabel(self.shipStatusGroup)
        self.energyLabelText.setObjectName(u"energyLabelText")

        self.shipStatusFormLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.energyLabelText)

        self.energyProgressBar = QProgressBar(self.shipStatusGroup)
        self.energyProgressBar.setObjectName(u"energyProgressBar")
        self.energyProgressBar.setValue(100)
        self.energyProgressBar.setMaximum(5000)
        self.energyProgressBar.setTextVisible(True)
        self.energyProgressBar.setStyleSheet(u"QProgressBar::chunk { background-color: #ffcc00; }")

        self.shipStatusFormLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.energyProgressBar)


        self.statusTabLayout.addWidget(self.shipStatusGroup)

        self.positionGroup = QGroupBox(self.statusTab)
        self.positionGroup.setObjectName(u"positionGroup")
        self.positionFormLayout = QFormLayout(self.positionGroup)
        self.positionFormLayout.setObjectName(u"positionFormLayout")
        self.coordinatesLabelText = QLabel(self.positionGroup)
        self.coordinatesLabelText.setObjectName(u"coordinatesLabelText")

        self.positionFormLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.coordinatesLabelText)

        self.coordinatesLabel = QLabel(self.positionGroup)
        self.coordinatesLabel.setObjectName(u"coordinatesLabel")

        self.positionFormLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.coordinatesLabel)

        self.sectorLabelText = QLabel(self.positionGroup)
        self.sectorLabelText.setObjectName(u"sectorLabelText")

        self.positionFormLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.sectorLabelText)

        self.sectorLabel = QLabel(self.positionGroup)
        self.sectorLabel.setObjectName(u"sectorLabel")

        self.positionFormLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.sectorLabel)


        self.statusTabLayout.addWidget(self.positionGroup)

        self.statusTabSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.statusTabLayout.addItem(self.statusTabSpacer)

        self.controlTabWidget.addTab(self.statusTab, "")
        self.actionsTab = QWidget()
        self.actionsTab.setObjectName(u"actionsTab")
        self.actionsTabLayout = QVBoxLayout(self.actionsTab)
        self.actionsTabLayout.setObjectName(u"actionsTabLayout")
        self.movementGroup = QGroupBox(self.actionsTab)
        self.movementGroup.setObjectName(u"movementGroup")
        self.movementLayout = QVBoxLayout(self.movementGroup)
        self.movementLayout.setObjectName(u"movementLayout")
        self.moveButton = QPushButton(self.movementGroup)
        self.moveButton.setObjectName(u"moveButton")
        self.moveButton.setMinimumSize(QSize(0, 30))

        self.movementLayout.addWidget(self.moveButton)

        self.rotateButton = QPushButton(self.movementGroup)
        self.rotateButton.setObjectName(u"rotateButton")
        self.rotateButton.setMinimumSize(QSize(0, 30))

        self.movementLayout.addWidget(self.rotateButton)


        self.actionsTabLayout.addWidget(self.movementGroup)

        self.combatGroup = QGroupBox(self.actionsTab)
        self.combatGroup.setObjectName(u"combatGroup")
        self.combatLayout = QVBoxLayout(self.combatGroup)
        self.combatLayout.setObjectName(u"combatLayout")
        self.fireButton = QPushButton(self.combatGroup)
        self.fireButton.setObjectName(u"fireButton")
        self.fireButton.setMinimumSize(QSize(0, 30))

        self.combatLayout.addWidget(self.fireButton)

        self.scanButton = QPushButton(self.combatGroup)
        self.scanButton.setObjectName(u"scanButton")
        self.scanButton.setMinimumSize(QSize(0, 30))

        self.combatLayout.addWidget(self.scanButton)

        self.evasiveButton = QPushButton(self.combatGroup)
        self.evasiveButton.setObjectName(u"evasiveButton")
        self.evasiveButton.setMinimumSize(QSize(0, 30))

        self.combatLayout.addWidget(self.evasiveButton)


        self.actionsTabLayout.addWidget(self.combatGroup)

        self.utilityGroup = QGroupBox(self.actionsTab)
        self.utilityGroup.setObjectName(u"utilityGroup")
        self.utilityLayout = QVBoxLayout(self.utilityGroup)
        self.utilityLayout.setObjectName(u"utilityLayout")
        self.dockButton = QPushButton(self.utilityGroup)
        self.dockButton.setObjectName(u"dockButton")
        self.dockButton.setMinimumSize(QSize(0, 30))

        self.utilityLayout.addWidget(self.dockButton)

        self.hailButton = QPushButton(self.utilityGroup)
        self.hailButton.setObjectName(u"hailButton")
        self.hailButton.setMinimumSize(QSize(0, 30))

        self.utilityLayout.addWidget(self.hailButton)


        self.actionsTabLayout.addWidget(self.utilityGroup)

        self.actionsTabSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.actionsTabLayout.addItem(self.actionsTabSpacer)

        self.controlTabWidget.addTab(self.actionsTab, "")
        self.mapTab = QWidget()
        self.mapTab.setObjectName(u"mapTab")
        self.mapTabLayout = QVBoxLayout(self.mapTab)
        self.mapTabLayout.setObjectName(u"mapTabLayout")
        self.minimapLabel = QLabel(self.mapTab)
        self.minimapLabel.setObjectName(u"minimapLabel")
        self.minimapLabel.setAlignment(Qt.AlignCenter)
        self.minimapLabel.setMinimumSize(QSize(250, 250))
        self.minimapLabel.setStyleSheet(u"background-color: #1a1a2e; border: 2px solid #444; color: #888;")

        self.mapTabLayout.addWidget(self.minimapLabel)

        self.legendGroup = QGroupBox(self.mapTab)
        self.legendGroup.setObjectName(u"legendGroup")
        self.legendLayout = QVBoxLayout(self.legendGroup)
        self.legendLayout.setObjectName(u"legendLayout")
        self.legendText = QLabel(self.legendGroup)
        self.legendText.setObjectName(u"legendText")
        self.legendText.setTextFormat(Qt.RichText)

        self.legendLayout.addWidget(self.legendText)


        self.mapTabLayout.addWidget(self.legendGroup)

        self.mapTabSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.mapTabLayout.addItem(self.mapTabSpacer)

        self.controlTabWidget.addTab(self.mapTab, "")

        self.dockLayout.addWidget(self.controlTabWidget)

        self.rightDock.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.rightDock)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 1600, 22))
        self.menuFile = QMenu(self.menuBar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuView = QMenu(self.menuBar)
        self.menuView.setObjectName(u"menuView")
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
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Star Trek Retro Remake", None))
        self.actionGalaxyMode.setText(QCoreApplication.translate("MainWindow", u"Galaxy", None))
#if QT_CONFIG(tooltip)
        self.actionGalaxyMode.setToolTip(QCoreApplication.translate("MainWindow", u"Switch to Galaxy Map Mode", None))
#endif // QT_CONFIG(tooltip)
        self.actionSectorMode.setText(QCoreApplication.translate("MainWindow", u"Sector", None))
#if QT_CONFIG(tooltip)
        self.actionSectorMode.setToolTip(QCoreApplication.translate("MainWindow", u"Switch to Sector Map Mode", None))
#endif // QT_CONFIG(tooltip)
        self.actionCombatMode.setText(QCoreApplication.translate("MainWindow", u"Combat", None))
#if QT_CONFIG(tooltip)
        self.actionCombatMode.setToolTip(QCoreApplication.translate("MainWindow", u"Switch to Combat Mode", None))
#endif // QT_CONFIG(tooltip)
        self.actionZoomIn.setText(QCoreApplication.translate("MainWindow", u"Zoom In", None))
#if QT_CONFIG(tooltip)
        self.actionZoomIn.setToolTip(QCoreApplication.translate("MainWindow", u"Zoom in on the map", None))
#endif // QT_CONFIG(tooltip)
        self.actionZoomOut.setText(QCoreApplication.translate("MainWindow", u"Zoom Out", None))
#if QT_CONFIG(tooltip)
        self.actionZoomOut.setToolTip(QCoreApplication.translate("MainWindow", u"Zoom out on the map", None))
#endif // QT_CONFIG(tooltip)
        self.actionZoomReset.setText(QCoreApplication.translate("MainWindow", u"Reset Zoom", None))
#if QT_CONFIG(tooltip)
        self.actionZoomReset.setToolTip(QCoreApplication.translate("MainWindow", u"Reset zoom to 100%", None))
#endif // QT_CONFIG(tooltip)
        self.actionSettings.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
#if QT_CONFIG(tooltip)
        self.actionSettings.setToolTip(QCoreApplication.translate("MainWindow", u"Open Settings Dialog", None))
#endif // QT_CONFIG(tooltip)
        self.actionNewGame.setText(QCoreApplication.translate("MainWindow", u"New Game", None))
        self.actionSaveGame.setText(QCoreApplication.translate("MainWindow", u"Save Game", None))
        self.actionLoadGame.setText(QCoreApplication.translate("MainWindow", u"Load Game", None))
        self.actionQuit.setText(QCoreApplication.translate("MainWindow", u"Quit", None))
        self.actionToggleRightDock.setText(QCoreApplication.translate("MainWindow", u"Toggle Control Center", None))
        self.gameDisplay.setText("")
        self.endTurnButton.setText(QCoreApplication.translate("MainWindow", u"End Turn", None))
        self.actionPointsLabel.setText(QCoreApplication.translate("MainWindow", u"Action Points: 10", None))
        self.phaseLabel.setText(QCoreApplication.translate("MainWindow", u"Phase: Planning", None))
        self.turnNumberLabel.setText(QCoreApplication.translate("MainWindow", u"Turn: 1", None))
        self.mainToolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"Main Toolbar", None))
        self.rightDock.setWindowTitle(QCoreApplication.translate("MainWindow", u"Control Center", None))
        self.shipStatusGroup.setTitle(QCoreApplication.translate("MainWindow", u"Ship Status", None))
        self.shipNameLabelText.setText(QCoreApplication.translate("MainWindow", u"Ship:", None))
        self.shipNameLabel.setText(QCoreApplication.translate("MainWindow", u"USS Enterprise", None))
        self.hullLabelText.setText(QCoreApplication.translate("MainWindow", u"Hull:", None))
        self.hullProgressBar.setFormat(QCoreApplication.translate("MainWindow", u"%p%", None))
        self.shieldsLabelText.setText(QCoreApplication.translate("MainWindow", u"Shields:", None))
        self.shieldsProgressBar.setFormat(QCoreApplication.translate("MainWindow", u"%p%", None))
        self.energyLabelText.setText(QCoreApplication.translate("MainWindow", u"Energy:", None))
        self.energyProgressBar.setFormat(QCoreApplication.translate("MainWindow", u"%v / %m", None))
        self.positionGroup.setTitle(QCoreApplication.translate("MainWindow", u"Position", None))
        self.coordinatesLabelText.setText(QCoreApplication.translate("MainWindow", u"Coordinates:", None))
        self.coordinatesLabel.setText(QCoreApplication.translate("MainWindow", u"X: 10, Y: 10, Z: 2", None))
        self.sectorLabelText.setText(QCoreApplication.translate("MainWindow", u"Sector:", None))
        self.sectorLabel.setText(QCoreApplication.translate("MainWindow", u"Sol System", None))
        self.controlTabWidget.setTabText(self.controlTabWidget.indexOf(self.statusTab), QCoreApplication.translate("MainWindow", u"Status", None))
        self.movementGroup.setTitle(QCoreApplication.translate("MainWindow", u"Movement", None))
        self.moveButton.setText(QCoreApplication.translate("MainWindow", u"Move Ship", None))
        self.rotateButton.setText(QCoreApplication.translate("MainWindow", u"Rotate", None))
        self.combatGroup.setTitle(QCoreApplication.translate("MainWindow", u"Combat", None))
        self.fireButton.setText(QCoreApplication.translate("MainWindow", u"Fire Weapons", None))
        self.scanButton.setText(QCoreApplication.translate("MainWindow", u"Scan Target", None))
        self.evasiveButton.setText(QCoreApplication.translate("MainWindow", u"Evasive Maneuvers", None))
        self.utilityGroup.setTitle(QCoreApplication.translate("MainWindow", u"Utilities", None))
        self.dockButton.setText(QCoreApplication.translate("MainWindow", u"Dock at Station", None))
        self.hailButton.setText(QCoreApplication.translate("MainWindow", u"Hail Ship", None))
        self.controlTabWidget.setTabText(self.controlTabWidget.indexOf(self.actionsTab), QCoreApplication.translate("MainWindow", u"Actions", None))
        self.minimapLabel.setText(QCoreApplication.translate("MainWindow", u"Mini-Map", None))
        self.legendGroup.setTitle(QCoreApplication.translate("MainWindow", u"Legend", None))
        self.legendText.setText(QCoreApplication.translate("MainWindow", u"<html><body>\n"
"<p><span style='color:#00aaff;'>\u25a0</span> Player Ship</p>\n"
"<p><span style='color:#ff0000;'>\u25a0</span> Enemy Ship</p>\n"
"<p><span style='color:#ffaa00;'>\u25a0</span> Station</p>\n"
"<p><span style='color:#888888;'>\u25a0</span> Asteroid</p>\n"
"</body></html>", None))
        self.controlTabWidget.setTabText(self.controlTabWidget.indexOf(self.mapTab), QCoreApplication.translate("MainWindow", u"Map", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuView.setTitle(QCoreApplication.translate("MainWindow", u"View", None))
    # retranslateUi

