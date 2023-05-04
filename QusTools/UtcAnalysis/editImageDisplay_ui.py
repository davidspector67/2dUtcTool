# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'editImageDisplay.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_editBmode(object):
    def setupUi(self, editBmode):
        if not editBmode.objectName():
            editBmode.setObjectName(u"editBmode")
        editBmode.resize(406, 300)
        editBmode.setStyleSheet(u"QWidget {\n"
"	background-color: rgb(42, 42, 42);\n"
"}")
        self.editImageDisplayLabel = QLabel(editBmode)
        self.editImageDisplayLabel.setObjectName(u"editImageDisplayLabel")
        self.editImageDisplayLabel.setGeometry(QRect(-10, -20, 431, 131))
        self.editImageDisplayLabel.setStyleSheet(u"QLabel {\n"
"	font-size: 29px;\n"
"	color: rgb(255, 255, 255);\n"
"	background-color: rgba(255, 255, 255, 0);\n"
"}")
        self.editImageDisplayLabel.setTextFormat(Qt.AutoText)
        self.editImageDisplayLabel.setScaledContents(False)
        self.editImageDisplayLabel.setAlignment(Qt.AlignCenter)
        self.editImageDisplayLabel.setWordWrap(True)
        self.contrastValDisplay = QProgressBar(editBmode)
        self.contrastValDisplay.setObjectName(u"contrastValDisplay")
        self.contrastValDisplay.setGeometry(QRect(190, 110, 201, 16))
        self.contrastValDisplay.setStyleSheet(u"QProgressBar {\n"
"     border: 2px solid grey;\n"
"     border-radius: 5px;\n"
"     background-color: rgb(229, 229, 229);\n"
" }\n"
"\n"
" QProgressBar::chunk {\n"
"     background-color: rgb(90, 37, 255);;\n"
"     width: 20px;\n"
"	font-size: 0px;\n"
" }")
        self.contrastValDisplay.setValue(24)
        self.brightnessValDisplay = QProgressBar(editBmode)
        self.brightnessValDisplay.setObjectName(u"brightnessValDisplay")
        self.brightnessValDisplay.setGeometry(QRect(190, 170, 201, 16))
        self.brightnessValDisplay.setStyleSheet(u"QProgressBar {\n"
"     border: 2px solid grey;\n"
"     border-radius: 5px;\n"
"     background-color: rgb(229, 229, 229);\n"
" }\n"
"\n"
" QProgressBar::chunk {\n"
"     background-color: rgb(90, 37, 255);;\n"
"     width: 20px;\n"
"	font-size: 0px;\n"
" }")
        self.brightnessValDisplay.setValue(24)
        self.sharpnessValDisplay = QProgressBar(editBmode)
        self.sharpnessValDisplay.setObjectName(u"sharpnessValDisplay")
        self.sharpnessValDisplay.setGeometry(QRect(190, 230, 201, 16))
        self.sharpnessValDisplay.setStyleSheet(u"QProgressBar {\n"
"     border: 2px solid grey;\n"
"     border-radius: 5px;\n"
"     background-color: rgb(229, 229, 229);\n"
" }\n"
"\n"
" QProgressBar::chunk {\n"
"     background-color: rgb(90, 37, 255);;\n"
"     width: 20px;\n"
"	font-size: 0px;\n"
" }")
        self.sharpnessValDisplay.setValue(24)
        self.contrastLabel = QLabel(editBmode)
        self.contrastLabel.setObjectName(u"contrastLabel")
        self.contrastLabel.setGeometry(QRect(10, 100, 71, 41))
        self.contrastLabel.setStyleSheet(u"QLabel {\n"
"	font-size: 15px;\n"
"	color: rgb(255, 255, 255);\n"
"	background-color: rgba(255, 255, 255, 0);\n"
"}")
        self.contrastLabel.setTextFormat(Qt.AutoText)
        self.contrastLabel.setScaledContents(False)
        self.contrastLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.contrastLabel.setWordWrap(True)
        self.brightnessLabel = QLabel(editBmode)
        self.brightnessLabel.setObjectName(u"brightnessLabel")
        self.brightnessLabel.setGeometry(QRect(10, 160, 151, 41))
        self.brightnessLabel.setStyleSheet(u"QLabel {\n"
"	font-size: 15px;\n"
"	color: rgb(255, 255, 255);\n"
"	background-color: rgba(255, 255, 255, 0);\n"
"}")
        self.brightnessLabel.setTextFormat(Qt.AutoText)
        self.brightnessLabel.setScaledContents(False)
        self.brightnessLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.brightnessLabel.setWordWrap(True)
        self.sharpnessLabel = QLabel(editBmode)
        self.sharpnessLabel.setObjectName(u"sharpnessLabel")
        self.sharpnessLabel.setGeometry(QRect(10, 220, 151, 41))
        self.sharpnessLabel.setStyleSheet(u"QLabel {\n"
"	font-size: 15px;\n"
"	color: rgb(255, 255, 255);\n"
"	background-color: rgba(255, 255, 255, 0);\n"
"}")
        self.sharpnessLabel.setTextFormat(Qt.AutoText)
        self.sharpnessLabel.setScaledContents(False)
        self.sharpnessLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.sharpnessLabel.setWordWrap(True)
        self.sharpnessVal = QDoubleSpinBox(editBmode)
        self.sharpnessVal.setObjectName(u"sharpnessVal")
        self.sharpnessVal.setGeometry(QRect(110, 230, 61, 21))
        self.sharpnessVal.setStyleSheet(u"QDoubleSpinBox {\n"
"	background-color: white;\n"
"	color: black;\n"
"}")
        self.sharpnessVal.setMaximum(10.000000000000000)
        self.brightnessVal = QDoubleSpinBox(editBmode)
        self.brightnessVal.setObjectName(u"brightnessVal")
        self.brightnessVal.setGeometry(QRect(110, 170, 61, 21))
        self.brightnessVal.setStyleSheet(u"QDoubleSpinBox {\n"
"	background-color: white;\n"
"	color: black;\n"
"}")
        self.brightnessVal.setMaximum(10.000000000000000)
        self.contrastVal = QDoubleSpinBox(editBmode)
        self.contrastVal.setObjectName(u"contrastVal")
        self.contrastVal.setGeometry(QRect(110, 110, 61, 21))
        self.contrastVal.setStyleSheet(u"QDoubleSpinBox {\n"
"	background-color: white;\n"
"	color: black;\n"
"}")
        self.contrastVal.setMaximum(10.000000000000000)

        self.retranslateUi(editBmode)

        QMetaObject.connectSlotsByName(editBmode)
    # setupUi

    def retranslateUi(self, editBmode):
        editBmode.setWindowTitle(QCoreApplication.translate("editBmode", u"Edit B-Mode Image", None))
        self.editImageDisplayLabel.setText(QCoreApplication.translate("editBmode", u"Edit B-Mode Image Display", None))
        self.contrastLabel.setText(QCoreApplication.translate("editBmode", u"Contrast", None))
        self.brightnessLabel.setText(QCoreApplication.translate("editBmode", u"Brightness", None))
        self.sharpnessLabel.setText(QCoreApplication.translate("editBmode", u"Sharpness", None))
    # retranslateUi

