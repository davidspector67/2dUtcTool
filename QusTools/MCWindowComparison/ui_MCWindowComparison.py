# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MCWindowComparison.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(659, 620)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.corScroll = QScrollBar(self.centralwidget)
        self.corScroll.setObjectName(u"corScroll")
        self.corScroll.setGeometry(QRect(470, 330, 20, 241))
        self.corScroll.setOrientation(Qt.Vertical)
        self.axialScroll = QScrollBar(self.centralwidget)
        self.axialScroll.setObjectName(u"axialScroll")
        self.axialScroll.setGeometry(QRect(310, 30, 16, 271))
        self.axialScroll.setOrientation(Qt.Vertical)
        self.sagittalPlane = QLabel(self.centralwidget)
        self.sagittalPlane.setObjectName(u"sagittalPlane")
        self.sagittalPlane.setGeometry(QRect(330, 30, 281, 271))
        self.sagittalPlane.setFrameShape(QFrame.Box)
        self.sagittalPlane.setFrameShadow(QFrame.Sunken)
        self.label2 = QLabel(self.centralwidget)
        self.label2.setObjectName(u"label2")
        self.label2.setGeometry(QRect(300, 10, 331, 16))
        self.label2.setAlignment(Qt.AlignCenter)
        self.label2.setTextInteractionFlags(Qt.NoTextInteraction)
        self.label1 = QLabel(self.centralwidget)
        self.label1.setObjectName(u"label1")
        self.label1.setGeometry(QRect(-10, 10, 331, 16))
        self.label1.setAlignment(Qt.AlignCenter)
        self.label1.setTextInteractionFlags(Qt.NoTextInteraction)
        self.sagScroll = QScrollBar(self.centralwidget)
        self.sagScroll.setObjectName(u"sagScroll")
        self.sagScroll.setGeometry(QRect(620, 30, 16, 271))
        self.sagScroll.setOrientation(Qt.Vertical)
        self.coronalPlane = QLabel(self.centralwidget)
        self.coronalPlane.setObjectName(u"coronalPlane")
        self.coronalPlane.setGeometry(QRect(170, 330, 291, 241))
        self.coronalPlane.setFrameShape(QFrame.Box)
        self.coronalPlane.setFrameShadow(QFrame.Sunken)
        self.label3 = QLabel(self.centralwidget)
        self.label3.setObjectName(u"label3")
        self.label3.setGeometry(QRect(160, 310, 331, 16))
        self.label3.setAlignment(Qt.AlignCenter)
        self.label3.setTextInteractionFlags(Qt.NoTextInteraction)
        self.axialPlane = QLabel(self.centralwidget)
        self.axialPlane.setObjectName(u"axialPlane")
        self.axialPlane.setGeometry(QRect(30, 30, 281, 271))
        self.axialPlane.setFrameShape(QFrame.Box)
        self.axialPlane.setFrameShadow(QFrame.Sunken)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 659, 22))
        self.menuMotion_Corrected_Image = QMenu(self.menubar)
        self.menuMotion_Corrected_Image.setObjectName(u"menuMotion_Corrected_Image")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuMotion_Corrected_Image.menuAction())

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.sagittalPlane.setText("")
        self.label2.setText(QCoreApplication.translate("MainWindow", u"Sagittal Plane", None))
        self.label1.setText(QCoreApplication.translate("MainWindow", u"Axial Plane", None))
        self.coronalPlane.setText("")
        self.label3.setText(QCoreApplication.translate("MainWindow", u"Coronal Plane", None))
        self.axialPlane.setText("")
        self.menuMotion_Corrected_Image.setTitle(QCoreApplication.translate("MainWindow", u"Motion Corrected Image", None))
    # retranslateUi

