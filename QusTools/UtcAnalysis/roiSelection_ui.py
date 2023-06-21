# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'roiSelection.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_constructRoi(object):
    def setupUi(self, constructRoi):
        if not constructRoi.objectName():
            constructRoi.setObjectName(u"constructRoi")
        constructRoi.resize(1175, 749)
        constructRoi.setStyleSheet(u"QWidget {\n"
"	background: rgb(42, 42, 42);\n"
"}")
        self.constructRoiLabel = QLabel(constructRoi)
        self.constructRoiLabel.setObjectName(u"constructRoiLabel")
        self.constructRoiLabel.setGeometry(QRect(550, -20, 431, 131))
        self.constructRoiLabel.setStyleSheet(u"QLabel {\n"
"	font-size: 29px;\n"
"	color: rgb(255, 255, 255);\n"
"	background-color: rgba(255, 255, 255, 0);\n"
"}")
        self.constructRoiLabel.setTextFormat(Qt.AutoText)
        self.constructRoiLabel.setScaledContents(False)
        self.constructRoiLabel.setAlignment(Qt.AlignCenter)
        self.constructRoiLabel.setWordWrap(True)
        self.imDisplayFrame = QFrame(constructRoi)
        self.imDisplayFrame.setObjectName(u"imDisplayFrame")
        self.imDisplayFrame.setGeometry(QRect(400, 190, 721, 501))
        self.imDisplayFrame.setFrameShape(QFrame.StyledPanel)
        self.imDisplayFrame.setFrameShadow(QFrame.Raised)
        self.drawRoiButton = QPushButton(constructRoi)
        self.drawRoiButton.setObjectName(u"drawRoiButton")
        self.drawRoiButton.setGeometry(QRect(370, 110, 171, 41))
        self.drawRoiButton.setStyleSheet(u"QPushButton {\n"
"	color: white;\n"
"	font-size: 16px;\n"
"	background: rgb(90, 37, 255);\n"
"	border-radius: 15px;\n"
"}\n"
"QPushButton:checked {\n"
"	color:white; \n"
"	font-size: 16px;\n"
"	background: rgb(45, 0, 110);\n"
"	border-radius: 15px;\n"
"}\n"
"")
        self.drawRoiButton.setCheckable(True)
        self.drawRoiButton.setChecked(False)
        self.undoLastPtButton = QPushButton(constructRoi)
        self.undoLastPtButton.setObjectName(u"undoLastPtButton")
        self.undoLastPtButton.setGeometry(QRect(570, 110, 171, 41))
        self.undoLastPtButton.setStyleSheet(u"QPushButton {\n"
"	color: white;\n"
"	font-size: 16px;\n"
"	background: rgb(90, 37, 255);\n"
"	border-radius: 15px;\n"
"}")
        self.undoLastPtButton.setCheckable(False)
        self.acceptRoiButton = QPushButton(constructRoi)
        self.acceptRoiButton.setObjectName(u"acceptRoiButton")
        self.acceptRoiButton.setGeometry(QRect(970, 110, 171, 41))
        self.acceptRoiButton.setStyleSheet(u"QPushButton {\n"
"	color: white;\n"
"	font-size: 16px;\n"
"	background: rgb(90, 37, 255);\n"
"	border-radius: 15px;\n"
"}")
        self.acceptRoiButton.setCheckable(False)
        self.sidebar = QWidget(constructRoi)
        self.sidebar.setObjectName(u"sidebar")
        self.sidebar.setGeometry(QRect(0, 0, 341, 751))
        self.sidebar.setStyleSheet(u"QWidget {\n"
"	background-color: rgb(28, 0, 101);\n"
"}")
        self.imageSelectionSidebar = QFrame(self.sidebar)
        self.imageSelectionSidebar.setObjectName(u"imageSelectionSidebar")
        self.imageSelectionSidebar.setGeometry(QRect(0, 0, 341, 121))
        self.imageSelectionSidebar.setStyleSheet(u"QFrame {\n"
"	background-color: rgb(99, 0, 174);\n"
"	border: 1px solid black;\n"
"}")
        self.imageSelectionSidebar.setFrameShape(QFrame.StyledPanel)
        self.imageSelectionSidebar.setFrameShadow(QFrame.Raised)
        self.imageSelectionLabelSidebar = QLabel(self.imageSelectionSidebar)
        self.imageSelectionLabelSidebar.setObjectName(u"imageSelectionLabelSidebar")
        self.imageSelectionLabelSidebar.setGeometry(QRect(70, 0, 191, 51))
        self.imageSelectionLabelSidebar.setStyleSheet(u"QLabel {\n"
"	font-size: 21px;\n"
"	color: rgb(255, 255, 255);\n"
"	background-color: rgba(255, 255, 255, 0);\n"
"	border: 0px;\n"
"	font-weight: bold;\n"
"}")
        self.imageSelectionLabelSidebar.setAlignment(Qt.AlignCenter)
        self.imageLabel = QLabel(self.imageSelectionSidebar)
        self.imageLabel.setObjectName(u"imageLabel")
        self.imageLabel.setGeometry(QRect(-60, 40, 191, 51))
        self.imageLabel.setStyleSheet(u"QLabel {\n"
"	font-size: 16px;\n"
"	color: rgb(255, 255, 255);\n"
"	background-color: rgba(255, 255, 255, 0);\n"
"	border: 0px;\n"
"	font-weight: bold;\n"
"}")
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.phantomLabel = QLabel(self.imageSelectionSidebar)
        self.phantomLabel.setObjectName(u"phantomLabel")
        self.phantomLabel.setGeometry(QRect(-50, 70, 191, 51))
        self.phantomLabel.setStyleSheet(u"QLabel {\n"
"	font-size: 16px;\n"
"	color: rgb(255, 255, 255);\n"
"	background-color: rgba(255, 255, 255, 0);\n"
"	border: 0px;\n"
"	font-weight: bold\n"
"}")
        self.phantomLabel.setAlignment(Qt.AlignCenter)
        self.imagePathInput = QLabel(self.imageSelectionSidebar)
        self.imagePathInput.setObjectName(u"imagePathInput")
        self.imagePathInput.setGeometry(QRect(100, 40, 241, 51))
        self.imagePathInput.setStyleSheet(u"QLabel {\n"
"	font-size: 14px;\n"
"	color: rgb(255, 255, 255);\n"
"	background-color: rgba(255, 255, 255, 0);\n"
"	border: 0px;\n"
"}")
        self.imagePathInput.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.phantomPathInput = QLabel(self.imageSelectionSidebar)
        self.phantomPathInput.setObjectName(u"phantomPathInput")
        self.phantomPathInput.setGeometry(QRect(100, 70, 241, 51))
        self.phantomPathInput.setStyleSheet(u"QLabel {\n"
"	font-size: 14px;\n"
"	color: rgb(255, 255, 255);\n"
"	background-color: rgba(255, 255, 255, 0);\n"
"	border: 0px;\n"
"}")
        self.phantomPathInput.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.roiSidebar = QFrame(self.sidebar)
        self.roiSidebar.setObjectName(u"roiSidebar")
        self.roiSidebar.setGeometry(QRect(0, 120, 341, 121))
        self.roiSidebar.setStyleSheet(u"QFrame {\n"
"	background-color: rgb(99, 0, 174);\n"
"	border: 1px solid black;\n"
"}")
        self.roiSidebar.setFrameShape(QFrame.StyledPanel)
        self.roiSidebar.setFrameShadow(QFrame.Raised)
        self.roiSidebarLabel = QLabel(self.roiSidebar)
        self.roiSidebarLabel.setObjectName(u"roiSidebarLabel")
        self.roiSidebarLabel.setGeometry(QRect(0, 30, 341, 51))
        self.roiSidebarLabel.setStyleSheet(u"QLabel {\n"
"	font-size: 21px;\n"
"	color: rgb(255, 255, 255);\n"
"	background-color: rgba(255, 255, 255, 0);\n"
"	border: 0px;\n"
"	font-weight: bold;\n"
"}")
        self.roiSidebarLabel.setAlignment(Qt.AlignCenter)
        self.rfAnalysisSidebar = QFrame(self.sidebar)
        self.rfAnalysisSidebar.setObjectName(u"rfAnalysisSidebar")
        self.rfAnalysisSidebar.setGeometry(QRect(0, 360, 341, 121))
        self.rfAnalysisSidebar.setStyleSheet(u"QFrame {\n"
"	background-color:  rgb(49, 0, 124);\n"
"	border: 1px solid black;\n"
"}")
        self.rfAnalysisSidebar.setFrameShape(QFrame.StyledPanel)
        self.rfAnalysisSidebar.setFrameShadow(QFrame.Raised)
        self.rfAnalysisLabel = QLabel(self.rfAnalysisSidebar)
        self.rfAnalysisLabel.setObjectName(u"rfAnalysisLabel")
        self.rfAnalysisLabel.setGeometry(QRect(0, 30, 341, 51))
        self.rfAnalysisLabel.setStyleSheet(u"QLabel {\n"
"	font-size: 21px;\n"
"	color: rgb(255, 255, 255);\n"
"	background-color: rgba(255, 255, 255, 0);\n"
"	border: 0px;\n"
"	font-weight: bold;\n"
"}")
        self.rfAnalysisLabel.setAlignment(Qt.AlignCenter)
        self.exportResultsSidebar = QFrame(self.sidebar)
        self.exportResultsSidebar.setObjectName(u"exportResultsSidebar")
        self.exportResultsSidebar.setGeometry(QRect(0, 480, 341, 121))
        self.exportResultsSidebar.setStyleSheet(u"QFrame {\n"
"	background-color:  rgb(49, 0, 124);\n"
"	border: 1px solid black;\n"
"}")
        self.exportResultsSidebar.setFrameShape(QFrame.StyledPanel)
        self.exportResultsSidebar.setFrameShadow(QFrame.Raised)
        self.exportResultsLabel = QLabel(self.exportResultsSidebar)
        self.exportResultsLabel.setObjectName(u"exportResultsLabel")
        self.exportResultsLabel.setGeometry(QRect(20, 30, 301, 51))
        self.exportResultsLabel.setStyleSheet(u"QLabel {\n"
"	font-size: 21px;\n"
"	color: rgb(255, 255, 255);\n"
"	background-color: rgba(255, 255, 255, 0);\n"
"	border: 0px;\n"
"	font-weight: bold;\n"
"}")
        self.exportResultsLabel.setAlignment(Qt.AlignCenter)
        self.analysisParamsSidebar = QFrame(constructRoi)
        self.analysisParamsSidebar.setObjectName(u"analysisParamsSidebar")
        self.analysisParamsSidebar.setGeometry(QRect(0, 240, 341, 121))
        self.analysisParamsSidebar.setStyleSheet(u"QFrame {\n"
"	background-color: rgb(49, 0, 124);\n"
"	border: 1px solid black;\n"
"}")
        self.analysisParamsSidebar.setFrameShape(QFrame.StyledPanel)
        self.analysisParamsSidebar.setFrameShadow(QFrame.Raised)
        self.analysisParamsLabel = QLabel(self.analysisParamsSidebar)
        self.analysisParamsLabel.setObjectName(u"analysisParamsLabel")
        self.analysisParamsLabel.setGeometry(QRect(0, 30, 341, 51))
        self.analysisParamsLabel.setStyleSheet(u"QLabel {\n"
"	font-size: 21px;\n"
"	color: rgb(255, 255, 255);\n"
"	background-color: rgba(255, 255, 255, 0);\n"
"	border: 0px;\n"
"	font-weight:bold;\n"
"}")
        self.analysisParamsLabel.setAlignment(Qt.AlignCenter)
        self.editImageDisplayButton = QPushButton(constructRoi)
        self.editImageDisplayButton.setObjectName(u"editImageDisplayButton")
        self.editImageDisplayButton.setGeometry(QRect(940, 700, 181, 41))
        self.editImageDisplayButton.setStyleSheet(u"QPushButton {\n"
"	color: white;\n"
"	font-size: 12px;\n"
"	background: rgb(90, 37, 255);\n"
"	border-radius: 15px;\n"
"}")
        self.closeRoiButton = QPushButton(constructRoi)
        self.closeRoiButton.setObjectName(u"closeRoiButton")
        self.closeRoiButton.setGeometry(QRect(770, 110, 171, 41))
        self.closeRoiButton.setStyleSheet(u"QPushButton {\n"
"	color: white;\n"
"	font-size: 16px;\n"
"	background: rgb(90, 37, 255);\n"
"	border-radius: 15px;\n"
"}")
        self.closeRoiButton.setCheckable(False)
        self.redrawRoiButton = QPushButton(constructRoi)
        self.redrawRoiButton.setObjectName(u"redrawRoiButton")
        self.redrawRoiButton.setGeometry(QRect(770, 110, 171, 41))
        self.redrawRoiButton.setStyleSheet(u"QPushButton {\n"
"	color: white;\n"
"	font-size: 16px;\n"
"	background: rgb(90, 37, 255);\n"
"	border-radius: 15px;\n"
"}")
        self.redrawRoiButton.setCheckable(False)

        self.retranslateUi(constructRoi)

        QMetaObject.connectSlotsByName(constructRoi)
    # setupUi

    def retranslateUi(self, constructRoi):
        constructRoi.setWindowTitle(QCoreApplication.translate("constructRoi", u"Select Region of Interest", None))
        self.constructRoiLabel.setText(QCoreApplication.translate("constructRoi", u"Construct Region of Interest (ROI):", None))
        self.drawRoiButton.setText(QCoreApplication.translate("constructRoi", u"Draw ROI", None))
        self.undoLastPtButton.setText(QCoreApplication.translate("constructRoi", u"Undo Last Point", None))
        self.acceptRoiButton.setText(QCoreApplication.translate("constructRoi", u"Accept ROI", None))
#if QT_CONFIG(tooltip)
        self.sidebar.setToolTip(QCoreApplication.translate("constructRoi", u"<html><head/><body><p><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.imageSelectionLabelSidebar.setText(QCoreApplication.translate("constructRoi", u"Image Selection:", None))
        self.imageLabel.setText(QCoreApplication.translate("constructRoi", u"Image:", None))
        self.phantomLabel.setText(QCoreApplication.translate("constructRoi", u"Phantom:", None))
        self.imagePathInput.setText(QCoreApplication.translate("constructRoi", u"Sample filename ", None))
        self.phantomPathInput.setText(QCoreApplication.translate("constructRoi", u"Sample filename ", None))
        self.roiSidebarLabel.setText(QCoreApplication.translate("constructRoi", u"Region of Interest (ROI) Selection", None))
        self.rfAnalysisLabel.setText(QCoreApplication.translate("constructRoi", u"Radio Frequency Data Analysis", None))
        self.exportResultsLabel.setText(QCoreApplication.translate("constructRoi", u"Export Results", None))
        self.analysisParamsLabel.setText(QCoreApplication.translate("constructRoi", u"Analysis Parameter Selection", None))
        self.editImageDisplayButton.setText(QCoreApplication.translate("constructRoi", u"Edit Image Display", None))
        self.closeRoiButton.setText(QCoreApplication.translate("constructRoi", u"Close ROI", None))
        self.redrawRoiButton.setText(QCoreApplication.translate("constructRoi", u"Redraw ROI", None))
    # retranslateUi

