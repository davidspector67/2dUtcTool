# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'welcomeScreen.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_welcomeScreen(object):
    def setupUi(self, welcomeScreen):
        if not welcomeScreen.objectName():
            welcomeScreen.setObjectName(u"welcomeScreen")
        welcomeScreen.resize(1175, 749)
        welcomeScreen.setStyleSheet(u"QWidget {\n"
"	background: rgb(42, 42, 42);\n"
"}")
        self.selectProgramLabel = QLabel(welcomeScreen)
        self.selectProgramLabel.setObjectName(u"selectProgramLabel")
        self.selectProgramLabel.setGeometry(QRect(330, 40, 501, 131))
        self.selectProgramLabel.setStyleSheet(u"QLabel {\n"
"	font-size: 29px;\n"
"	color: rgb(255, 255, 255);\n"
"	background-color: rgba(255, 255, 255, 0);\n"
"}")
        self.selectProgramLabel.setTextFormat(Qt.AutoText)
        self.selectProgramLabel.setScaledContents(False)
        self.selectProgramLabel.setAlignment(Qt.AlignCenter)
        self.selectProgramLabel.setWordWrap(True)
        self.rf2dAnalysisButton = QPushButton(welcomeScreen)
        self.rf2dAnalysisButton.setObjectName(u"rf2dAnalysisButton")
        self.rf2dAnalysisButton.setGeometry(QRect(360, 240, 441, 61))
        self.rf2dAnalysisButton.setStyleSheet(u"QPushButton {\n"
"	color: white;\n"
"	font-size: 20px;\n"
"	background: rgb(90, 37, 255);\n"
"	border-radius: 15px;\n"
"}")
        self.constrast2dAnalysisButton = QPushButton(welcomeScreen)
        self.constrast2dAnalysisButton.setObjectName(u"constrast2dAnalysisButton")
        self.constrast2dAnalysisButton.setGeometry(QRect(360, 390, 441, 61))
        self.constrast2dAnalysisButton.setStyleSheet(u"QPushButton {\n"
"	color: white;\n"
"	font-size: 20px;\n"
"	background: rgb(90, 37, 255);\n"
"	border-radius: 15px;\n"
"}")
        self.contrast3dAnalysisButton = QPushButton(welcomeScreen)
        self.contrast3dAnalysisButton.setObjectName(u"contrast3dAnalysisButton")
        self.contrast3dAnalysisButton.setGeometry(QRect(360, 540, 441, 61))
        self.contrast3dAnalysisButton.setStyleSheet(u"QPushButton {\n"
"	color: white;\n"
"	font-size: 20px;\n"
"	background: rgb(90, 37, 255);\n"
"	border-radius: 15px;\n"
"}")

        self.retranslateUi(welcomeScreen)

        QMetaObject.connectSlotsByName(welcomeScreen)
    # setupUi

    def retranslateUi(self, welcomeScreen):
        welcomeScreen.setWindowTitle(QCoreApplication.translate("welcomeScreen", u"Select Ultrasound Image", None))
        self.selectProgramLabel.setText(QCoreApplication.translate("welcomeScreen", u"Quantitative Ultrasound Analysis Tools:", None))
        self.rf2dAnalysisButton.setText(QCoreApplication.translate("welcomeScreen", u"2D Radiofrequency Analysis", None))
        self.constrast2dAnalysisButton.setText(QCoreApplication.translate("welcomeScreen", u"2D Contrast Analysis", None))
        self.contrast3dAnalysisButton.setText(QCoreApplication.translate("welcomeScreen", u"3D Contrast Analysis", None))
    # retranslateUi

