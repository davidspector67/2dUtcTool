# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'nameROI.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_nameROI(object):
    def setupUi(self, nameROI):
        if not nameROI.objectName():
            nameROI.setObjectName(u"nameROI")
        nameROI.resize(525, 368)
        nameROI.setStyleSheet(u"QWidget {\n"
"	background-color: rgb(42, 42, 42);\n"
"}")
        self.nameRoiLabel = QLabel(nameROI)
        self.nameRoiLabel.setObjectName(u"nameRoiLabel")
        self.nameRoiLabel.setGeometry(QRect(60, -20, 431, 131))
        self.nameRoiLabel.setStyleSheet(u"QLabel {\n"
"	font-size: 29px;\n"
"	color: rgb(255, 255, 255);\n"
"	background-color: rgba(255, 255, 255, 0);\n"
"}")
        self.nameRoiLabel.setTextFormat(Qt.AutoText)
        self.nameRoiLabel.setScaledContents(False)
        self.nameRoiLabel.setAlignment(Qt.AlignCenter)
        self.nameRoiLabel.setWordWrap(True)
        self.nameRoiInput = QLineEdit(nameROI)
        self.nameRoiInput.setObjectName(u"nameRoiInput")
        self.nameRoiInput.setGeometry(QRect(230, 130, 271, 31))
        self.nameRoiInput.setStyleSheet(u"QLineEdit {\n"
"	background-color: rgb(249, 249, 249);\n"
"}")
        self.nameRoiPrompt = QLabel(nameROI)
        self.nameRoiPrompt.setObjectName(u"nameRoiPrompt")
        self.nameRoiPrompt.setGeometry(QRect(-20, 120, 271, 51))
        self.nameRoiPrompt.setStyleSheet(u"QLabel {\n"
"	background-color: rgba(255, 255, 255, 0);\n"
"	color: white;\n"
"	font-size: 17px;\n"
"}")
        self.nameRoiPrompt.setAlignment(Qt.AlignCenter)
        self.nameRoiPrompt.setTextInteractionFlags(Qt.NoTextInteraction)
        self.nameRoiContinueButton = QPushButton(nameROI)
        self.nameRoiContinueButton.setObjectName(u"nameRoiContinueButton")
        self.nameRoiContinueButton.setGeometry(QRect(200, 230, 131, 41))
        self.nameRoiContinueButton.setStyleSheet(u"QPushButton {\n"
"	color: white;\n"
"	font-size: 16px;\n"
"	background: rgb(90, 37, 255);\n"
"	border-radius: 15px;\n"
"}")
        self.nameRoiErrorMsg = QLabel(nameROI)
        self.nameRoiErrorMsg.setObjectName(u"nameRoiErrorMsg")
        self.nameRoiErrorMsg.setGeometry(QRect(210, 290, 111, 41))
        self.nameRoiErrorMsg.setStyleSheet(u"QLabel {\n"
"	color: rgb(255, 0, 23);\n"
"	font-size: 21px;\n"
"	background-color: rgba(255, 255, 255, 0);\n"
"}")
        self.nameRoiErrorMsg.setAlignment(Qt.AlignCenter)

        self.retranslateUi(nameROI)

        QMetaObject.connectSlotsByName(nameROI)
    # setupUi

    def retranslateUi(self, nameROI):
        nameROI.setWindowTitle(QCoreApplication.translate("nameROI", u"Name Region of Interest", None))
        self.nameRoiLabel.setText(QCoreApplication.translate("nameROI", u"Name Region of Interest:", None))
        self.nameRoiPrompt.setText(QCoreApplication.translate("nameROI", u"ROI Name:", None))
        self.nameRoiContinueButton.setText(QCoreApplication.translate("nameROI", u"Continue", None))
        self.nameRoiErrorMsg.setText(QCoreApplication.translate("nameROI", u"Error Msg", None))
    # retranslateUi

