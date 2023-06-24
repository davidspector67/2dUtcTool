# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'rfAnalysis.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_rfAnalysis(object):
    def setupUi(self, rfAnalysis):
        if not rfAnalysis.objectName():
            rfAnalysis.setObjectName(u"rfAnalysis")
        rfAnalysis.resize(1175, 749)
        rfAnalysis.setStyleSheet(u"QWidget {\n"
"	background: rgb(42, 42, 42);\n"
"}")
        self.widget = QWidget(rfAnalysis)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(0, 0, 341, 751))
        self.widget.setStyleSheet(u"QWidget {\n"
"	background-color: rgb(28, 0, 101);\n"
"}")
        self.frame = QFrame(self.widget)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(0, 0, 341, 121))
        self.frame.setStyleSheet(u"QFrame {\n"
"	background-color: rgb(99, 0, 174);\n"
"	border: 1px solid black;\n"
"}")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(70, 0, 191, 51))
        self.label.setStyleSheet(u"QLabel {\n"
"	font-size: 21px;\n"
"	color: rgb(255, 255, 255);\n"
"	background-color: rgba(255, 255, 255, 0);\n"
"	border: 0px;\n"
"	font-weight: bold;\n"
"}")
        self.label.setAlignment(Qt.AlignCenter)
        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(-60, 40, 191, 51))
        self.label_2.setStyleSheet(u"QLabel {\n"
"	font-size: 16px;\n"
"	color: rgb(255, 255, 255);\n"
"	background-color: rgba(255, 255, 255, 0);\n"
"	border: 0px;\n"
"	font-weight: bold;\n"
"}")
        self.label_2.setAlignment(Qt.AlignCenter)
        self.label_3 = QLabel(self.frame)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(-50, 70, 191, 51))
        self.label_3.setStyleSheet(u"QLabel {\n"
"	font-size: 16px;\n"
"	color: rgb(255, 255, 255);\n"
"	background-color: rgba(255, 255, 255, 0);\n"
"	border: 0px;\n"
"	font-weight: bold\n"
"}")
        self.label_3.setAlignment(Qt.AlignCenter)
        self.imagePathInput = QLabel(self.frame)
        self.imagePathInput.setObjectName(u"imagePathInput")
        self.imagePathInput.setGeometry(QRect(100, 40, 241, 51))
        self.imagePathInput.setStyleSheet(u"QLabel {\n"
"	font-size: 14px;\n"
"	color: rgb(255, 255, 255);\n"
"	background-color: rgba(255, 255, 255, 0);\n"
"	border: 0px;\n"
"}")
        self.imagePathInput.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.phantomPathInput = QLabel(self.frame)
        self.phantomPathInput.setObjectName(u"phantomPathInput")
        self.phantomPathInput.setGeometry(QRect(100, 70, 241, 51))
        self.phantomPathInput.setStyleSheet(u"QLabel {\n"
"	font-size: 14px;\n"
"	color: rgb(255, 255, 255);\n"
"	background-color: rgba(255, 255, 255, 0);\n"
"	border: 0px;\n"
"}")
        self.phantomPathInput.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.frame_2 = QFrame(self.widget)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setGeometry(QRect(0, 120, 341, 121))
        self.frame_2.setStyleSheet(u"QFrame {\n"
"	background-color: rgb(99, 0, 174);;\n"
"	border: 1px solid black;\n"
"}")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.label_4 = QLabel(self.frame_2)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(0, 40, 341, 51))
        self.label_4.setStyleSheet(u"QLabel {\n"
"	font-size: 21px;\n"
"	color: rgb(255, 255, 255);\n"
"	background-color: rgba(255, 255, 255, 0);\n"
"	border: 0px;\n"
"	font-weight: bold;\n"
"}")
        self.label_4.setAlignment(Qt.AlignCenter)
        self.frame_4 = QFrame(self.widget)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setGeometry(QRect(0, 360, 341, 121))
        self.frame_4.setStyleSheet(u"QFrame {\n"
"	background-color:  rgb(99, 0, 174);\n"
"	border: 1px solid black;\n"
"}")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.label_7 = QLabel(self.frame_4)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(0, 30, 341, 51))
        self.label_7.setStyleSheet(u"QLabel {\n"
"	font-size: 21px;\n"
"	color: rgb(255, 255, 255);\n"
"	background-color: rgba(255, 255, 255, 0);\n"
"	border: 0px;\n"
"	font-weight: bold;\n"
"}")
        self.label_7.setAlignment(Qt.AlignCenter)
        self.frame_5 = QFrame(self.widget)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setGeometry(QRect(0, 480, 341, 121))
        self.frame_5.setStyleSheet(u"QFrame {\n"
"	background-color:  rgb(49, 0, 124);\n"
"	border: 1px solid black;\n"
"}")
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.label_8 = QLabel(self.frame_5)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(20, 30, 301, 51))
        self.label_8.setStyleSheet(u"QLabel {\n"
"	font-size: 21px;\n"
"	color: rgb(255, 255, 255);\n"
"	background-color: rgba(255, 255, 255, 0);\n"
"	border: 0px;\n"
"	font-weight: bold;\n"
"}")
        self.label_8.setAlignment(Qt.AlignCenter)
        self.frame_3 = QFrame(rfAnalysis)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setGeometry(QRect(0, 240, 341, 121))
        self.frame_3.setStyleSheet(u"QFrame {\n"
"	background-color: rgb(99, 0, 174);\n"
"	border: 1px solid black;\n"
"}")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.label_6 = QLabel(self.frame_3)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(0, 30, 341, 51))
        self.label_6.setStyleSheet(u"QLabel {\n"
"	font-size: 21px;\n"
"	color: rgb(255, 255, 255);\n"
"	background-color: rgba(255, 255, 255, 0);\n"
"	border: 0px;\n"
"	font-weight:bold;\n"
"}")
        self.label_6.setAlignment(Qt.AlignCenter)
        self.imDisplayFrame = QFrame(rfAnalysis)
        self.imDisplayFrame.setObjectName(u"imDisplayFrame")
        self.imDisplayFrame.setGeometry(QRect(400, 180, 721, 501))
        self.imDisplayFrame.setFrameShape(QFrame.StyledPanel)
        self.imDisplayFrame.setFrameShadow(QFrame.Raised)
        self.displayMbfButton = QPushButton(rfAnalysis)
        self.displayMbfButton.setObjectName(u"displayMbfButton")
        self.displayMbfButton.setGeometry(QRect(360, 120, 181, 41))
        self.displayMbfButton.setStyleSheet(u"QPushButton {\n"
"	color: white;\n"
"	font-size: 12px;\n"
"	background: rgb(90, 37, 255);\n"
"	border-radius: 15px;\n"
"}\n"
"QPushButton:checked {\n"
"	color:white; \n"
"	font-size: 12px;\n"
"	background: rgb(45, 0, 110);\n"
"	border-radius: 15px;\n"
"}")
        self.displaySsButton = QPushButton(rfAnalysis)
        self.displaySsButton.setObjectName(u"displaySsButton")
        self.displaySsButton.setGeometry(QRect(560, 120, 181, 41))
        self.displaySsButton.setStyleSheet(u"QPushButton {\n"
"	color: white;\n"
"	font-size: 12px;\n"
"	background: rgb(90, 37, 255);\n"
"	border-radius: 15px;\n"
"}\n"
"QPushButton:checked {\n"
"	color:white; \n"
"	font-size: 12px;\n"
"	background: rgb(45, 0, 110);\n"
"	border-radius: 15px;\n"
"}")
        self.displaySiButton = QPushButton(rfAnalysis)
        self.displaySiButton.setObjectName(u"displaySiButton")
        self.displaySiButton.setGeometry(QRect(760, 120, 181, 41))
        self.displaySiButton.setStyleSheet(u"QPushButton {\n"
"	color: white;\n"
"	font-size: 12px;\n"
"	background: rgb(90, 37, 255);\n"
"	border-radius: 15px;\n"
"}\n"
"QPushButton:checked {\n"
"	color:white; \n"
"	font-size: 12px;\n"
"	background: rgb(45, 0, 110);\n"
"	border-radius: 15px;\n"
"}")
        self.editImageDisplayButton = QPushButton(rfAnalysis)
        self.editImageDisplayButton.setObjectName(u"editImageDisplayButton")
        self.editImageDisplayButton.setGeometry(QRect(990, 700, 181, 41))
        self.editImageDisplayButton.setStyleSheet(u"QPushButton {\n"
"	color: white;\n"
"	font-size: 12px;\n"
"	background: rgb(90, 37, 255);\n"
"	border-radius: 15px;\n"
"}")
        self.avMbfLabel = QLabel(rfAnalysis)
        self.avMbfLabel.setObjectName(u"avMbfLabel")
        self.avMbfLabel.setGeometry(QRect(720, 0, 81, 51))
        font = QFont()
        font.setPointSize(14)
        self.avMbfLabel.setFont(font)
        self.avMbfLabel.setStyleSheet(u"QLabel {\n"
"	color: white;\n"
"	background-color: rgba(0,0,0,0);\n"
"}")
        self.avMbfLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.avSsLabel = QLabel(rfAnalysis)
        self.avSsLabel.setObjectName(u"avSsLabel")
        self.avSsLabel.setGeometry(QRect(720, 35, 91, 51))
        self.avSsLabel.setFont(font)
        self.avSsLabel.setStyleSheet(u"QLabel {\n"
"	color: white;\n"
"	background-color: rgba(0,0,0,0);\n"
"}")
        self.avSsLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.avSiLabel = QLabel(rfAnalysis)
        self.avSiLabel.setObjectName(u"avSiLabel")
        self.avSiLabel.setGeometry(QRect(720, 70, 71, 51))
        self.avSiLabel.setFont(font)
        self.avSiLabel.setStyleSheet(u"QLabel {\n"
"	color: white;\n"
"	background-color: rgba(0,0,0,0);\n"
"}")
        self.avSiLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.avMbfVal = QLabel(rfAnalysis)
        self.avMbfVal.setObjectName(u"avMbfVal")
        self.avMbfVal.setGeometry(QRect(820, 0, 51, 51))
        self.avMbfVal.setFont(font)
        self.avMbfVal.setStyleSheet(u"QLabel {\n"
"	color: white;\n"
"	background-color: rgba(0,0,0,0);\n"
"}")
        self.avMbfVal.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.avSsVal = QLabel(rfAnalysis)
        self.avSsVal.setObjectName(u"avSsVal")
        self.avSsVal.setGeometry(QRect(820, 35, 51, 51))
        self.avSsVal.setFont(font)
        self.avSsVal.setStyleSheet(u"QLabel {\n"
"	color: white;\n"
"	background-color: rgba(0,0,0,0);\n"
"}")
        self.avSsVal.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.avSiVal = QLabel(rfAnalysis)
        self.avSiVal.setObjectName(u"avSiVal")
        self.avSiVal.setGeometry(QRect(820, 70, 51, 51))
        self.avSiVal.setFont(font)
        self.avSiVal.setStyleSheet(u"QLabel {\n"
"	color: white;\n"
"	background-color: rgba(0,0,0,0);\n"
"}")
        self.avSiVal.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.indSiVal = QLabel(rfAnalysis)
        self.indSiVal.setObjectName(u"indSiVal")
        self.indSiVal.setGeometry(QRect(970, 70, 51, 51))
        self.indSiVal.setFont(font)
        self.indSiVal.setStyleSheet(u"QLabel {\n"
"	color: white;\n"
"	background-color: rgba(0,0,0,0);\n"
"}")
        self.indSiVal.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.indMbfVal = QLabel(rfAnalysis)
        self.indMbfVal.setObjectName(u"indMbfVal")
        self.indMbfVal.setGeometry(QRect(970, 0, 51, 51))
        self.indMbfVal.setFont(font)
        self.indMbfVal.setStyleSheet(u"QLabel {\n"
"	color: white;\n"
"	background-color: rgba(0,0,0,0);\n"
"}")
        self.indMbfVal.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.indMbfLabel = QLabel(rfAnalysis)
        self.indMbfLabel.setObjectName(u"indMbfLabel")
        self.indMbfLabel.setGeometry(QRect(870, 0, 81, 51))
        self.indMbfLabel.setFont(font)
        self.indMbfLabel.setStyleSheet(u"QLabel {\n"
"	color: white;\n"
"	background-color: rgba(0,0,0,0);\n"
"}")
        self.indMbfLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.indSiLabel = QLabel(rfAnalysis)
        self.indSiLabel.setObjectName(u"indSiLabel")
        self.indSiLabel.setGeometry(QRect(870, 70, 71, 51))
        self.indSiLabel.setFont(font)
        self.indSiLabel.setStyleSheet(u"QLabel {\n"
"	color: white;\n"
"	background-color: rgba(0,0,0,0);\n"
"}")
        self.indSiLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.indSsVal = QLabel(rfAnalysis)
        self.indSsVal.setObjectName(u"indSsVal")
        self.indSsVal.setGeometry(QRect(970, 35, 51, 51))
        self.indSsVal.setFont(font)
        self.indSsVal.setStyleSheet(u"QLabel {\n"
"	color: white;\n"
"	background-color: rgba(0,0,0,0);\n"
"}")
        self.indSsVal.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.indSsLabel = QLabel(rfAnalysis)
        self.indSsLabel.setObjectName(u"indSsLabel")
        self.indSsLabel.setGeometry(QRect(870, 35, 101, 51))
        self.indSsLabel.setFont(font)
        self.indSsLabel.setStyleSheet(u"QLabel {\n"
"	color: white;\n"
"	background-color: rgba(0,0,0,0);\n"
"}")
        self.indSsLabel.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.chooseWindowButton = QPushButton(rfAnalysis)
        self.chooseWindowButton.setObjectName(u"chooseWindowButton")
        self.chooseWindowButton.setGeometry(QRect(350, 700, 181, 41))
        self.chooseWindowButton.setStyleSheet(u"QPushButton {\n"
"	color: white;\n"
"	font-size: 12px;\n"
"	background: rgb(90, 37, 255);\n"
"	border-radius: 15px;\n"
"}\n"
"QPushButton:checked {\n"
"	color:white; \n"
"	font-size: 12px;\n"
"	background: rgb(45, 0, 110);\n"
"	border-radius: 15px;\n"
"}")
        self.legend = QFrame(rfAnalysis)
        self.legend.setObjectName(u"legend")
        self.legend.setGeometry(QRect(1040, 20, 111, 131))
        self.legend.setFrameShape(QFrame.StyledPanel)
        self.legend.setFrameShadow(QFrame.Raised)
        self.constructRoiLabel = QLabel(rfAnalysis)
        self.constructRoiLabel.setObjectName(u"constructRoiLabel")
        self.constructRoiLabel.setGeometry(QRect(310, -10, 431, 131))
        self.constructRoiLabel.setStyleSheet(u"QLabel {\n"
"	font-size: 29px;\n"
"	color: rgb(255, 255, 255);\n"
"	background-color: rgba(255, 255, 255, 0);\n"
"}")
        self.constructRoiLabel.setTextFormat(Qt.AutoText)
        self.constructRoiLabel.setScaledContents(False)
        self.constructRoiLabel.setAlignment(Qt.AlignCenter)
        self.constructRoiLabel.setWordWrap(True)

        self.retranslateUi(rfAnalysis)

        QMetaObject.connectSlotsByName(rfAnalysis)
    # setupUi

    def retranslateUi(self, rfAnalysis):
        rfAnalysis.setWindowTitle(QCoreApplication.translate("rfAnalysis", u"Radio Frequency Data Analysis", None))
#if QT_CONFIG(tooltip)
        self.widget.setToolTip(QCoreApplication.translate("rfAnalysis", u"<html><head/><body><p><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label.setText(QCoreApplication.translate("rfAnalysis", u"Image Selection:", None))
        self.label_2.setText(QCoreApplication.translate("rfAnalysis", u"Image:", None))
        self.label_3.setText(QCoreApplication.translate("rfAnalysis", u"Phantom:", None))
        self.imagePathInput.setText(QCoreApplication.translate("rfAnalysis", u"Sample filename ", None))
        self.phantomPathInput.setText(QCoreApplication.translate("rfAnalysis", u"Sample filename ", None))
        self.label_4.setText(QCoreApplication.translate("rfAnalysis", u"Region of Interest (ROI) Selection", None))
        self.label_7.setText(QCoreApplication.translate("rfAnalysis", u"Radio Frequency Data Analysis", None))
        self.label_8.setText(QCoreApplication.translate("rfAnalysis", u"Export Results", None))
        self.label_6.setText(QCoreApplication.translate("rfAnalysis", u"Analysis Parameter Selection", None))
        self.displayMbfButton.setText(QCoreApplication.translate("rfAnalysis", u"Display Midband Fit (MBF)", None))
        self.displaySsButton.setText(QCoreApplication.translate("rfAnalysis", u"Display Spectral Slope (SS)", None))
        self.displaySiButton.setText(QCoreApplication.translate("rfAnalysis", u"Display Spectral Intercept (SI)", None))
        self.editImageDisplayButton.setText(QCoreApplication.translate("rfAnalysis", u"Edit Image Display", None))
        self.avMbfLabel.setText(QCoreApplication.translate("rfAnalysis", u"Av.  MBF", None))
        self.avSsLabel.setText(QCoreApplication.translate("rfAnalysis", u"Av.  SS (1e-6)", None))
        self.avSiLabel.setText(QCoreApplication.translate("rfAnalysis", u"Av.  SI", None))
        self.avMbfVal.setText(QCoreApplication.translate("rfAnalysis", u"0", None))
        self.avSsVal.setText(QCoreApplication.translate("rfAnalysis", u"0", None))
        self.avSiVal.setText(QCoreApplication.translate("rfAnalysis", u"0", None))
        self.indSiVal.setText(QCoreApplication.translate("rfAnalysis", u"0", None))
        self.indMbfVal.setText(QCoreApplication.translate("rfAnalysis", u"0", None))
        self.indMbfLabel.setText(QCoreApplication.translate("rfAnalysis", u"Ind.  MBF", None))
        self.indSiLabel.setText(QCoreApplication.translate("rfAnalysis", u"Ind.  SI", None))
        self.indSsVal.setText(QCoreApplication.translate("rfAnalysis", u"0", None))
        self.indSsLabel.setText(QCoreApplication.translate("rfAnalysis", u"Ind.  SS (1e-6)", None))
        self.chooseWindowButton.setText(QCoreApplication.translate("rfAnalysis", u"Choose Window to Analyze", None))
        self.constructRoiLabel.setText(QCoreApplication.translate("rfAnalysis", u"Radio Frequency Analysis:", None))
    # retranslateUi

