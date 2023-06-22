# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'analysisParamsSelection.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_analysisParams(object):
    def setupUi(self, analysisParams):
        if not analysisParams.objectName():
            analysisParams.setObjectName(u"analysisParams")
        analysisParams.resize(1175, 749)
        analysisParams.setStyleSheet(u"QWidget {\n"
"	background: rgb(42, 42, 42);\n"
"}")
        self.sidebar = QWidget(analysisParams)
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
        self.analysisParamsSidebar = QFrame(self.sidebar)
        self.analysisParamsSidebar.setObjectName(u"analysisParamsSidebar")
        self.analysisParamsSidebar.setGeometry(QRect(0, 240, 341, 121))
        self.analysisParamsSidebar.setStyleSheet(u"QFrame {\n"
"	background-color: rgb(99, 0, 174);\n"
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
        self.analysisParamsLabel_2 = QLabel(analysisParams)
        self.analysisParamsLabel_2.setObjectName(u"analysisParamsLabel_2")
        self.analysisParamsLabel_2.setGeometry(QRect(460, -20, 571, 131))
        self.analysisParamsLabel_2.setStyleSheet(u"QLabel {\n"
"	font-size: 29px;\n"
"	color: rgb(255, 255, 255);\n"
"	background-color: rgba(255, 255, 255, 0);\n"
"}")
        self.analysisParamsLabel_2.setTextFormat(Qt.AutoText)
        self.analysisParamsLabel_2.setScaledContents(False)
        self.analysisParamsLabel_2.setAlignment(Qt.AlignCenter)
        self.analysisParamsLabel_2.setWordWrap(True)
        self.continueButton = QPushButton(analysisParams)
        self.continueButton.setObjectName(u"continueButton")
        self.continueButton.setGeometry(QRect(670, 620, 171, 41))
        self.continueButton.setStyleSheet(u"QPushButton {\n"
"	color: white;\n"
"	font-size: 16px;\n"
"	background: rgb(90, 37, 255);\n"
"	border-radius: 15px;\n"
"}")
        self.frameVal = QSpinBox(analysisParams)
        self.frameVal.setObjectName(u"frameVal")
        self.frameVal.setGeometry(QRect(1060, 425, 51, 31))
        self.frameVal.setStyleSheet(u"QSpinBox {\n"
"	background-color: white;\n"
"	color: black;\n"
"}")
        self.endDepthVal = QDoubleSpinBox(analysisParams)
        self.endDepthVal.setObjectName(u"endDepthVal")
        self.endDepthVal.setGeometry(QRect(1050, 200, 61, 21))
        self.endDepthVal.setStyleSheet(u"QDoubleSpinBox {\n"
"	background-color: white;\n"
"	color: black;\n"
"}")
        self.latOverlapVal = QSpinBox(analysisParams)
        self.latOverlapVal.setObjectName(u"latOverlapVal")
        self.latOverlapVal.setGeometry(QRect(670, 345, 51, 31))
        self.latOverlapVal.setStyleSheet(u"QSpinBox {\n"
"	background-color: white;\n"
"	color: black;\n"
"}")
        self.startDepthVal = QDoubleSpinBox(analysisParams)
        self.startDepthVal.setObjectName(u"startDepthVal")
        self.startDepthVal.setGeometry(QRect(1050, 125, 61, 21))
        self.startDepthVal.setStyleSheet(u"QDoubleSpinBox {\n"
"	background-color: white;\n"
"	color: black;\n"
"}")
        self.axOverlapVal = QSpinBox(analysisParams)
        self.axOverlapVal.setObjectName(u"axOverlapVal")
        self.axOverlapVal.setGeometry(QRect(670, 265, 51, 31))
        self.axOverlapVal.setStyleSheet(u"QSpinBox {\n"
"	background-color: white;\n"
"	color: black;\n"
"}")
        self.frameLabel = QLabel(analysisParams)
        self.frameLabel.setObjectName(u"frameLabel")
        self.frameLabel.setGeometry(QRect(790, 420, 231, 51))
        font = QFont()
        font.setPointSize(18)
        self.frameLabel.setFont(font)
        self.frameLabel.setStyleSheet(u"QLabel {\n"
"	color: white;\n"
"	background-color: rgba(0,0,0,0);\n"
"}")
        self.frameLabel.setAlignment(Qt.AlignCenter)
        self.maxFreqLabel = QLabel(analysisParams)
        self.maxFreqLabel.setObjectName(u"maxFreqLabel")
        self.maxFreqLabel.setGeometry(QRect(580, 500, 231, 51))
        self.maxFreqLabel.setFont(font)
        self.maxFreqLabel.setStyleSheet(u"QLabel {\n"
"	color: white;\n"
"	background-color: rgba(0,0,0,0);\n"
"}")
        self.maxFreqLabel.setAlignment(Qt.AlignCenter)
        self.minFreqLabel = QLabel(analysisParams)
        self.minFreqLabel.setObjectName(u"minFreqLabel")
        self.minFreqLabel.setGeometry(QRect(400, 420, 231, 51))
        self.minFreqLabel.setFont(font)
        self.minFreqLabel.setStyleSheet(u"QLabel {\n"
"	color: white;\n"
"	background-color: rgba(0,0,0,0);\n"
"}")
        self.minFreqLabel.setAlignment(Qt.AlignCenter)
        self.latOverlapLabel = QLabel(analysisParams)
        self.latOverlapLabel.setObjectName(u"latOverlapLabel")
        self.latOverlapLabel.setGeometry(QRect(400, 340, 231, 51))
        self.latOverlapLabel.setFont(font)
        self.latOverlapLabel.setStyleSheet(u"QLabel {\n"
"	color: white;\n"
"	background-color: rgba(0,0,0,0);\n"
"}")
        self.latOverlapLabel.setAlignment(Qt.AlignCenter)
        self.axOverlapLabel = QLabel(analysisParams)
        self.axOverlapLabel.setObjectName(u"axOverlapLabel")
        self.axOverlapLabel.setGeometry(QRect(400, 260, 231, 51))
        self.axOverlapLabel.setFont(font)
        self.axOverlapLabel.setStyleSheet(u"QLabel {\n"
"	color: white;\n"
"	background-color: rgba(0,0,0,0);\n"
"}")
        self.axOverlapLabel.setAlignment(Qt.AlignCenter)
        self.latWinSizeLabel = QLabel(analysisParams)
        self.latWinSizeLabel.setObjectName(u"latWinSizeLabel")
        self.latWinSizeLabel.setGeometry(QRect(400, 180, 231, 51))
        self.latWinSizeLabel.setFont(font)
        self.latWinSizeLabel.setStyleSheet(u"QLabel {\n"
"	color: white;\n"
"	background-color: rgba(0,0,0,0);\n"
"}")
        self.latWinSizeLabel.setAlignment(Qt.AlignCenter)
        self.axWinSizeLabel = QLabel(analysisParams)
        self.axWinSizeLabel.setObjectName(u"axWinSizeLabel")
        self.axWinSizeLabel.setGeometry(QRect(400, 110, 231, 51))
        self.axWinSizeLabel.setFont(font)
        self.axWinSizeLabel.setStyleSheet(u"QLabel {\n"
"	color: white;\n"
"	background-color: rgba(0,0,0,0);\n"
"}")
        self.axWinSizeLabel.setAlignment(Qt.AlignCenter)
        self.startDepthLabel = QLabel(analysisParams)
        self.startDepthLabel.setObjectName(u"startDepthLabel")
        self.startDepthLabel.setGeometry(QRect(790, 110, 231, 51))
        self.startDepthLabel.setFont(font)
        self.startDepthLabel.setStyleSheet(u"QLabel {\n"
"	color: white;\n"
"	background-color: rgba(0,0,0,0);\n"
"}")
        self.startDepthLabel.setAlignment(Qt.AlignCenter)
        self.endDepthLabel = QLabel(analysisParams)
        self.endDepthLabel.setObjectName(u"endDepthLabel")
        self.endDepthLabel.setGeometry(QRect(790, 180, 231, 51))
        self.endDepthLabel.setFont(font)
        self.endDepthLabel.setStyleSheet(u"QLabel {\n"
"	color: white;\n"
"	background-color: rgba(0,0,0,0);\n"
"}")
        self.endDepthLabel.setAlignment(Qt.AlignCenter)
        self.clipFactorLabel = QLabel(analysisParams)
        self.clipFactorLabel.setObjectName(u"clipFactorLabel")
        self.clipFactorLabel.setGeometry(QRect(790, 250, 231, 51))
        self.clipFactorLabel.setFont(font)
        self.clipFactorLabel.setStyleSheet(u"QLabel {\n"
"	color: white;\n"
"	background-color: rgba(0,0,0,0);\n"
"}")
        self.clipFactorLabel.setAlignment(Qt.AlignCenter)
        self.samplingFreqLabel = QLabel(analysisParams)
        self.samplingFreqLabel.setObjectName(u"samplingFreqLabel")
        self.samplingFreqLabel.setGeometry(QRect(790, 340, 231, 51))
        self.samplingFreqLabel.setFont(font)
        self.samplingFreqLabel.setStyleSheet(u"QLabel {\n"
"	color: white;\n"
"	background-color: rgba(0,0,0,0);\n"
"}")
        self.samplingFreqLabel.setAlignment(Qt.AlignCenter)
        self.exportResultsSidebar = QFrame(analysisParams)
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
        self.minFreqVal = QDoubleSpinBox(analysisParams)
        self.minFreqVal.setObjectName(u"minFreqVal")
        self.minFreqVal.setGeometry(QRect(670, 440, 61, 21))
        self.minFreqVal.setStyleSheet(u"QDoubleSpinBox {\n"
"	background-color: white;\n"
"	color: black;\n"
"}")
        self.maxFreqVal = QDoubleSpinBox(analysisParams)
        self.maxFreqVal.setObjectName(u"maxFreqVal")
        self.maxFreqVal.setGeometry(QRect(850, 510, 61, 21))
        self.maxFreqVal.setStyleSheet(u"QDoubleSpinBox {\n"
"	background-color: white;\n"
"	color: black;\n"
"}")
        self.samplingFreqVal = QDoubleSpinBox(analysisParams)
        self.samplingFreqVal.setObjectName(u"samplingFreqVal")
        self.samplingFreqVal.setGeometry(QRect(1060, 350, 61, 21))
        self.samplingFreqVal.setStyleSheet(u"QDoubleSpinBox {\n"
"	background-color: white;\n"
"	color: black;\n"
"}")
        self.axWinSizeVal = QDoubleSpinBox(analysisParams)
        self.axWinSizeVal.setObjectName(u"axWinSizeVal")
        self.axWinSizeVal.setGeometry(QRect(670, 130, 61, 21))
        self.axWinSizeVal.setStyleSheet(u"QDoubleSpinBox {\n"
"	background-color: white;\n"
"	color: black;\n"
"}")
        self.latWinSizeVal = QDoubleSpinBox(analysisParams)
        self.latWinSizeVal.setObjectName(u"latWinSizeVal")
        self.latWinSizeVal.setGeometry(QRect(670, 190, 61, 21))
        self.latWinSizeVal.setStyleSheet(u"QDoubleSpinBox {\n"
"	background-color: white;\n"
"	color: black;\n"
"}")
        self.clipFactorVal = QSpinBox(analysisParams)
        self.clipFactorVal.setObjectName(u"clipFactorVal")
        self.clipFactorVal.setGeometry(QRect(1060, 260, 51, 31))
        self.clipFactorVal.setStyleSheet(u"QSpinBox {\n"
"	background-color: white;\n"
"	color: black;\n"
"}")

        self.retranslateUi(analysisParams)

        QMetaObject.connectSlotsByName(analysisParams)
    # setupUi

    def retranslateUi(self, analysisParams):
        analysisParams.setWindowTitle(QCoreApplication.translate("analysisParams", u"Select Region of Interest", None))
#if QT_CONFIG(tooltip)
        self.sidebar.setToolTip(QCoreApplication.translate("analysisParams", u"<html><head/><body><p><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.imageSelectionLabelSidebar.setText(QCoreApplication.translate("analysisParams", u"Image Selection:", None))
        self.imageLabel.setText(QCoreApplication.translate("analysisParams", u"Image:", None))
        self.phantomLabel.setText(QCoreApplication.translate("analysisParams", u"Phantom:", None))
        self.imagePathInput.setText(QCoreApplication.translate("analysisParams", u"Sample filename ", None))
        self.phantomPathInput.setText(QCoreApplication.translate("analysisParams", u"Sample filename ", None))
        self.roiSidebarLabel.setText(QCoreApplication.translate("analysisParams", u"Region of Interest (ROI) Selection", None))
        self.analysisParamsLabel.setText(QCoreApplication.translate("analysisParams", u"Analysis Parameter Selection", None))
        self.rfAnalysisLabel.setText(QCoreApplication.translate("analysisParams", u"Radio Frequency Data Analysis", None))
        self.analysisParamsLabel_2.setText(QCoreApplication.translate("analysisParams", u"Select Radio Frequency Analysis Parameters:", None))
        self.continueButton.setText(QCoreApplication.translate("analysisParams", u"Continue", None))
        self.frameLabel.setText(QCoreApplication.translate("analysisParams", u"Frame", None))
        self.maxFreqLabel.setText(QCoreApplication.translate("analysisParams", u"Maximum Frequency (MHz)", None))
        self.minFreqLabel.setText(QCoreApplication.translate("analysisParams", u"MinimumFrequency (MHz)", None))
        self.latOverlapLabel.setText(QCoreApplication.translate("analysisParams", u"Lateral Overlap (%)", None))
        self.axOverlapLabel.setText(QCoreApplication.translate("analysisParams", u"Axial Overlap (%)", None))
        self.latWinSizeLabel.setText(QCoreApplication.translate("analysisParams", u"Lateral Window Size (mm)", None))
        self.axWinSizeLabel.setText(QCoreApplication.translate("analysisParams", u"Axial Window Size (mm)", None))
        self.startDepthLabel.setText(QCoreApplication.translate("analysisParams", u"Starting Depth (mm)", None))
        self.endDepthLabel.setText(QCoreApplication.translate("analysisParams", u"Ending Depth (mm)", None))
        self.clipFactorLabel.setText(QCoreApplication.translate("analysisParams", u"Clip Factor (%)", None))
        self.samplingFreqLabel.setText(QCoreApplication.translate("analysisParams", u"Sampling Frequency (MHz)", None))
        self.exportResultsLabel.setText(QCoreApplication.translate("analysisParams", u"Export Results", None))
    # retranslateUi

