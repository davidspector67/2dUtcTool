# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'psGraphDisplay.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_psGraphWidget(object):
    def setupUi(self, psGraphWidget):
        if not psGraphWidget.objectName():
            psGraphWidget.setObjectName(u"psGraphWidget")
        psGraphWidget.resize(400, 300)
        psGraphWidget.setStyleSheet(u"QWidget {\n"
"	background-color: rgb(42, 42, 42);\n"
"}")
        self.psGraphLabel = QLabel(psGraphWidget)
        self.psGraphLabel.setObjectName(u"psGraphLabel")
        self.psGraphLabel.setGeometry(QRect(-10, -30, 431, 131))
        self.psGraphLabel.setStyleSheet(u"QLabel {\n"
"	font-size: 29px;\n"
"	color: rgb(255, 255, 255);\n"
"	background-color: rgba(255, 255, 255, 0);\n"
"}")
        self.psGraphLabel.setTextFormat(Qt.AutoText)
        self.psGraphLabel.setScaledContents(False)
        self.psGraphLabel.setAlignment(Qt.AlignCenter)
        self.psGraphLabel.setWordWrap(True)
        self.psGraphFrame = QFrame(psGraphWidget)
        self.psGraphFrame.setObjectName(u"psGraphFrame")
        self.psGraphFrame.setGeometry(QRect(60, 80, 281, 191))
        self.psGraphFrame.setToolTipDuration(10)
        self.psGraphFrame.setFrameShape(QFrame.StyledPanel)
        self.psGraphFrame.setFrameShadow(QFrame.Raised)

        self.retranslateUi(psGraphWidget)

        QMetaObject.connectSlotsByName(psGraphWidget)
    # setupUi

    def retranslateUi(self, psGraphWidget):
        psGraphWidget.setWindowTitle(QCoreApplication.translate("psGraphWidget", u"Power Spectrum Graph", None))
        self.psGraphLabel.setText(QCoreApplication.translate("psGraphWidget", u"Power Spectrum Graph:", None))
    # retranslateUi

