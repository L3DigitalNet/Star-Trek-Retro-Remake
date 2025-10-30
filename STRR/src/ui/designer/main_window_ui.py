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
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGroupBox, QHBoxLayout, QLabel,
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1920, 1080)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.controlPanel = QGroupBox(self.centralwidget)
        self.controlPanel.setObjectName(u"controlPanel")
        self.controlPanel.setMaximumSize(QSize(350, 16777215))
        self.controlPanel.setMinimumSize(QSize(300, 0))
        self.verticalLayout = QVBoxLayout(self.controlPanel)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.titleLabel = QLabel(self.controlPanel)
        self.titleLabel.setObjectName(u"titleLabel")
        self.titleLabel.setAlignment(Qt.AlignCenter)
        self.titleLabel.setTextFormat(Qt.RichText)

        self.verticalLayout.addWidget(self.titleLabel)

        self.shipStatusLabel = QLabel(self.controlPanel)
        self.shipStatusLabel.setObjectName(u"shipStatusLabel")
        self.shipStatusLabel.setStyleSheet(u"padding: 10px; background-color: #1a1a1a; border: 1px solid #333; border-radius: 5px; color: #ccc;")
        self.shipStatusLabel.setWordWrap(True)

        self.verticalLayout.addWidget(self.shipStatusLabel)

        self.zLevelLabel = QLabel(self.controlPanel)
        self.zLevelLabel.setObjectName(u"zLevelLabel")
        self.zLevelLabel.setStyleSheet(u"padding: 8px; background-color: #2a2a2a; border: 1px solid #444; border-radius: 3px; font-weight: bold;")

        self.verticalLayout.addWidget(self.zLevelLabel)

        self.newGameButton = QPushButton(self.controlPanel)
        self.newGameButton.setObjectName(u"newGameButton")

        self.verticalLayout.addWidget(self.newGameButton)

        self.saveGameButton = QPushButton(self.controlPanel)
        self.saveGameButton.setObjectName(u"saveGameButton")

        self.verticalLayout.addWidget(self.saveGameButton)

        self.loadGameButton = QPushButton(self.controlPanel)
        self.loadGameButton.setObjectName(u"loadGameButton")

        self.verticalLayout.addWidget(self.loadGameButton)

        self.settingsButton = QPushButton(self.controlPanel)
        self.settingsButton.setObjectName(u"settingsButton")

        self.verticalLayout.addWidget(self.settingsButton)

        self.messageLabel = QLabel(self.controlPanel)
        self.messageLabel.setObjectName(u"messageLabel")

        self.verticalLayout.addWidget(self.messageLabel)

        self.messageDisplay = QLabel(self.controlPanel)
        self.messageDisplay.setObjectName(u"messageDisplay")
        self.messageDisplay.setMinimumSize(QSize(0, 100))
        self.messageDisplay.setStyleSheet(u"padding: 10px; background-color: #0a0a0a; border: 1px solid #333; border-radius: 5px; color: #00ff00; font-family: monospace;")
        self.messageDisplay.setWordWrap(True)

        self.verticalLayout.addWidget(self.messageDisplay)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.quitButton = QPushButton(self.controlPanel)
        self.quitButton.setObjectName(u"quitButton")
        self.quitButton.setStyleSheet(u"background-color: #aa0000;")

        self.verticalLayout.addWidget(self.quitButton)


        self.horizontalLayout.addWidget(self.controlPanel)

        self.gameContainer = QWidget(self.centralwidget)
        self.gameContainer.setObjectName(u"gameContainer")
        self.verticalLayout_2 = QVBoxLayout(self.gameContainer)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.gameTitle = QLabel(self.gameContainer)
        self.gameTitle.setObjectName(u"gameTitle")
        self.gameTitle.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.gameTitle)

        self.gameDisplay = QLabel(self.gameContainer)
        self.gameDisplay.setObjectName(u"gameDisplay")
        self.gameDisplay.setMinimumSize(QSize(1280, 900))
        self.gameDisplay.setMaximumSize(QSize(1280, 900))
        self.gameDisplay.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.gameDisplay)

        self.instructionsLabel = QLabel(self.gameContainer)
        self.instructionsLabel.setObjectName(u"instructionsLabel")
        self.instructionsLabel.setAlignment(Qt.AlignCenter)
        self.instructionsLabel.setStyleSheet(u"padding: 5px; background-color: #2a2a2a; color: #ccc;")

        self.verticalLayout_2.addWidget(self.instructionsLabel)


        self.horizontalLayout.addWidget(self.gameContainer)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Star Trek Retro Remake", None))
        self.controlPanel.setTitle(QCoreApplication.translate("MainWindow", u"Game Controls", None))
        self.titleLabel.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><h2 style=\"text-align: center; color: #00aaff;\">Star Trek<br/>Retro Remake</h2></body></html>", None))
        self.shipStatusLabel.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:600;\">USS Enterprise</span><br/>Status: Active<br/>Hull: 100%<br/>Shields: 100%<br/>Energy: 5000</p></body></html>", None))
        self.zLevelLabel.setText(QCoreApplication.translate("MainWindow", u"Z-Level: 0", None))
        self.newGameButton.setText(QCoreApplication.translate("MainWindow", u"New Game", None))
        self.saveGameButton.setText(QCoreApplication.translate("MainWindow", u"Save Game", None))
        self.loadGameButton.setText(QCoreApplication.translate("MainWindow", u"Load Game", None))
        self.settingsButton.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.messageLabel.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:600;\">Messages:</span></p></body></html>", None))
        self.messageDisplay.setText(QCoreApplication.translate("MainWindow", u"Ready to explore...", None))
        self.quitButton.setText(QCoreApplication.translate("MainWindow", u"Quit", None))
        self.gameTitle.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><h3 style=\"text-align: center;\">Sector Map View</h3></body></html>", None))
        self.gameDisplay.setText("")
        self.instructionsLabel.setText(QCoreApplication.translate("MainWindow", u"Controls: PageUp/PageDown (Z-levels) | +/- (Zoom) | Arrow Keys (Pan) | Left Click (Select/Move)", None))
    # retranslateUi

