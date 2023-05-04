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


class Ui_selectRoi(object):
    def setupUi(self, selectRoi):
        if not selectRoi.objectName():
            selectRoi.setObjectName(u"selectRoi")
        selectRoi.resize(1175, 749)
        selectRoi.setStyleSheet(u"QWidget {\n"
"	background: rgb(42, 42, 42);\n"
"}")
        self.sidebar = QWidget(selectRoi)
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
        self.imageFilenameDisplay = QLabel(self.imageSelectionSidebar)
        self.imageFilenameDisplay.setObjectName(u"imageFilenameDisplay")
        self.imageFilenameDisplay.setGeometry(QRect(100, 40, 241, 51))
        self.imageFilenameDisplay.setStyleSheet(u"QLabel {\n"
"	font-size: 14px;\n"
"	color: rgb(255, 255, 255);\n"
"	background-color: rgba(255, 255, 255, 0);\n"
"	border: 0px;\n"
"}")
        self.imageFilenameDisplay.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.phantomFilenameDisplay = QLabel(self.imageSelectionSidebar)
        self.phantomFilenameDisplay.setObjectName(u"phantomFilenameDisplay")
        self.phantomFilenameDisplay.setGeometry(QRect(100, 70, 241, 51))
        self.phantomFilenameDisplay.setStyleSheet(u"QLabel {\n"
"	font-size: 14px;\n"
"	color: rgb(255, 255, 255);\n"
"	background-color: rgba(255, 255, 255, 0);\n"
"	border: 0px;\n"
"}")
        self.phantomFilenameDisplay.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
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
        self.roiSidebarLabel.setGeometry(QRect(0, 0, 341, 51))
        self.roiSidebarLabel.setStyleSheet(u"QLabel {\n"
"	font-size: 21px;\n"
"	color: rgb(255, 255, 255);\n"
"	background-color: rgba(255, 255, 255, 0);\n"
"	border: 0px;\n"
"	font-weight: bold;\n"
"}")
        self.roiSidebarLabel.setAlignment(Qt.AlignCenter)
        self.roiTitleLabel = QLabel(self.roiSidebar)
        self.roiTitleLabel.setObjectName(u"roiTitleLabel")
        self.roiTitleLabel.setGeometry(QRect(-40, 50, 191, 51))
        self.roiTitleLabel.setStyleSheet(u"QLabel {\n"
"	font-size: 16px;\n"
"	color: rgb(255, 255, 255);\n"
"	background-color: rgba(255, 255, 255, 0);\n"
"	border: 0px;\n"
"	font-weight: bold;\n"
"}")
        self.roiTitleLabel.setAlignment(Qt.AlignCenter)
        self.roiNameDisplay = QLabel(self.roiSidebar)
        self.roiNameDisplay.setObjectName(u"roiNameDisplay")
        self.roiNameDisplay.setGeometry(QRect(110, 50, 241, 51))
        self.roiNameDisplay.setStyleSheet(u"QLabel {\n"
"	font-size: 14px;\n"
"	color: rgb(255, 255, 255);\n"
"	background-color: rgba(255, 255, 255, 0);\n"
"	border: 0px;\n"
"}")
        self.roiNameDisplay.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
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
        self.analysisParamsLabel_2 = QLabel(selectRoi)
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
        self.continueButton = QPushButton(selectRoi)
        self.continueButton.setObjectName(u"continueButton")
        self.continueButton.setGeometry(QRect(670, 650, 171, 41))
        self.continueButton.setStyleSheet(u"QPushButton {\n"
"	color: white;\n"
"	font-size: 16px;\n"
"	background: rgb(90, 37, 255);\n"
"	border-radius: 15px;\n"
"}")
        self.minFreqVal = QSpinBox(selectRoi)
        self.minFreqVal.setObjectName(u"minFreqVal")
        self.minFreqVal.setGeometry(QRect(670, 355, 51, 31))
        self.minFreqVal.setStyleSheet(u"QSpinBox {\n"
"	background-color: white;\n"
"}")
        self.frameVal = QSpinBox(selectRoi)
        self.frameVal.setObjectName(u"frameVal")
        self.frameVal.setGeometry(QRect(670, 485, 51, 31))
        self.frameVal.setStyleSheet(u"QSpinBox {\n"
"	background-color: white;\n"
"}")
        self.latWinSizeVal = QSpinBox(selectRoi)
        self.latWinSizeVal.setObjectName(u"latWinSizeVal")
        self.latWinSizeVal.setGeometry(QRect(670, 175, 51, 31))
        self.latWinSizeVal.setStyleSheet(u"QSpinBox {\n"
"	background-color: white;\n"
"}")
        self.endDepthVal = QDoubleSpinBox(selectRoi)
        self.endDepthVal.setObjectName(u"endDepthVal")
        self.endDepthVal.setGeometry(QRect(1050, 240, 61, 21))
        self.endDepthVal.setStyleSheet(u"QDoubleSpinBox {\n"
"	background-color: white;\n"
"}")
        self.maxFreqVal = QSpinBox(selectRoi)
        self.maxFreqVal.setObjectName(u"maxFreqVal")
        self.maxFreqVal.setGeometry(QRect(670, 415, 51, 31))
        self.maxFreqVal.setStyleSheet(u"QSpinBox {\n"
"	background-color: white;\n"
"}")
        self.endHeightVal = QDoubleSpinBox(selectRoi)
        self.endHeightVal.setObjectName(u"endHeightVal")
        self.endHeightVal.setGeometry(QRect(1050, 300, 61, 21))
        self.endHeightVal.setStyleSheet(u"QDoubleSpinBox {\n"
"	background-color: white;\n"
"}")
        self.dynRangeVal = QSpinBox(selectRoi)
        self.dynRangeVal.setObjectName(u"dynRangeVal")
        self.dynRangeVal.setGeometry(QRect(1060, 415, 51, 31))
        self.dynRangeVal.setStyleSheet(u"QSpinBox {\n"
"	background-color: white;\n"
"}")
        self.latOverlapVal = QSpinBox(selectRoi)
        self.latOverlapVal.setObjectName(u"latOverlapVal")
        self.latOverlapVal.setGeometry(QRect(670, 295, 51, 31))
        self.latOverlapVal.setStyleSheet(u"QSpinBox {\n"
"	background-color: white;\n"
"}")
        self.philDepthVal = QDoubleSpinBox(selectRoi)
        self.philDepthVal.setObjectName(u"philDepthVal")
        self.philDepthVal.setGeometry(QRect(1050, 490, 61, 21))
        self.philDepthVal.setStyleSheet(u"QDoubleSpinBox {\n"
"	background-color: white;\n"
"}")
        self.startDepthVal = QDoubleSpinBox(selectRoi)
        self.startDepthVal.setObjectName(u"startDepthVal")
        self.startDepthVal.setGeometry(QRect(1050, 185, 61, 21))
        self.startDepthVal.setStyleSheet(u"QDoubleSpinBox {\n"
"	background-color: white;\n"
"}")
        self.clipFactVal = QDoubleSpinBox(selectRoi)
        self.clipFactVal.setObjectName(u"clipFactVal")
        self.clipFactVal.setGeometry(QRect(1050, 360, 61, 21))
        self.clipFactVal.setStyleSheet(u"QDoubleSpinBox {\n"
"	background-color: white;\n"
"}")
        self.axOverlapVal = QSpinBox(selectRoi)
        self.axOverlapVal.setObjectName(u"axOverlapVal")
        self.axOverlapVal.setGeometry(QRect(670, 235, 51, 31))
        self.axOverlapVal.setStyleSheet(u"QSpinBox {\n"
"	background-color: white;\n"
"}")
        self.tiltVal = QSpinBox(selectRoi)
        self.tiltVal.setObjectName(u"tiltVal")
        self.tiltVal.setGeometry(QRect(670, 555, 51, 31))
        self.tiltVal.setStyleSheet(u"QSpinBox {\n"
"	background-color: white;\n"
"}")
        self.axWinSizeVal = QSpinBox(selectRoi)
        self.axWinSizeVal.setObjectName(u"axWinSizeVal")
        self.axWinSizeVal.setGeometry(QRect(670, 115, 51, 31))
        self.axWinSizeVal.setStyleSheet(u"QSpinBox {\n"
"	background-color: white;\n"
"}")
        self.widthVal = QSpinBox(selectRoi)
        self.widthVal.setObjectName(u"widthVal")
        self.widthVal.setGeometry(QRect(1060, 115, 51, 31))
        self.widthVal.setStyleSheet(u"QSpinBox {\n"
"	background-color: white;\n"
"}")
        self.tiltLabel = QLabel(selectRoi)
        self.tiltLabel.setObjectName(u"tiltLabel")
        self.tiltLabel.setGeometry(QRect(400, 545, 231, 51))
        font = QFont()
        font.setPointSize(18)
        self.tiltLabel.setFont(font)
        self.tiltLabel.setStyleSheet(u"QLabel {\n"
"	color: white;\n"
"	background-color: rgba(0,0,0,0);\n"
"}")
        self.tiltLabel.setAlignment(Qt.AlignCenter)
        self.philWidthVal = QDoubleSpinBox(selectRoi)
        self.philWidthVal.setObjectName(u"philWidthVal")
        self.philWidthVal.setGeometry(QRect(1050, 560, 61, 21))
        self.philWidthVal.setStyleSheet(u"QDoubleSpinBox {\n"
"	background-color: white;\n"
"}")
        self.frameLabel = QLabel(selectRoi)
        self.frameLabel.setObjectName(u"frameLabel")
        self.frameLabel.setGeometry(QRect(400, 480, 231, 51))
        self.frameLabel.setFont(font)
        self.frameLabel.setStyleSheet(u"QLabel {\n"
"	color: white;\n"
"	background-color: rgba(0,0,0,0);\n"
"}")
        self.frameLabel.setAlignment(Qt.AlignCenter)
        self.maxFreqLabel = QLabel(selectRoi)
        self.maxFreqLabel.setObjectName(u"maxFreqLabel")
        self.maxFreqLabel.setGeometry(QRect(400, 410, 231, 51))
        self.maxFreqLabel.setFont(font)
        self.maxFreqLabel.setStyleSheet(u"QLabel {\n"
"	color: white;\n"
"	background-color: rgba(0,0,0,0);\n"
"}")
        self.maxFreqLabel.setAlignment(Qt.AlignCenter)
        self.minFreqLabel = QLabel(selectRoi)
        self.minFreqLabel.setObjectName(u"minFreqLabel")
        self.minFreqLabel.setGeometry(QRect(400, 350, 231, 51))
        self.minFreqLabel.setFont(font)
        self.minFreqLabel.setStyleSheet(u"QLabel {\n"
"	color: white;\n"
"	background-color: rgba(0,0,0,0);\n"
"}")
        self.minFreqLabel.setAlignment(Qt.AlignCenter)
        self.latOverlapLabel = QLabel(selectRoi)
        self.latOverlapLabel.setObjectName(u"latOverlapLabel")
        self.latOverlapLabel.setGeometry(QRect(400, 290, 231, 51))
        self.latOverlapLabel.setFont(font)
        self.latOverlapLabel.setStyleSheet(u"QLabel {\n"
"	color: white;\n"
"	background-color: rgba(0,0,0,0);\n"
"}")
        self.latOverlapLabel.setAlignment(Qt.AlignCenter)
        self.axOverlapLabel = QLabel(selectRoi)
        self.axOverlapLabel.setObjectName(u"axOverlapLabel")
        self.axOverlapLabel.setGeometry(QRect(400, 230, 231, 51))
        self.axOverlapLabel.setFont(font)
        self.axOverlapLabel.setStyleSheet(u"QLabel {\n"
"	color: white;\n"
"	background-color: rgba(0,0,0,0);\n"
"}")
        self.axOverlapLabel.setAlignment(Qt.AlignCenter)
        self.latWinSizeLabel = QLabel(selectRoi)
        self.latWinSizeLabel.setObjectName(u"latWinSizeLabel")
        self.latWinSizeLabel.setGeometry(QRect(400, 170, 231, 51))
        self.latWinSizeLabel.setFont(font)
        self.latWinSizeLabel.setStyleSheet(u"QLabel {\n"
"	color: white;\n"
"	background-color: rgba(0,0,0,0);\n"
"}")
        self.latWinSizeLabel.setAlignment(Qt.AlignCenter)
        self.axWinSizeLabel = QLabel(selectRoi)
        self.axWinSizeLabel.setObjectName(u"axWinSizeLabel")
        self.axWinSizeLabel.setGeometry(QRect(400, 110, 231, 51))
        self.axWinSizeLabel.setFont(font)
        self.axWinSizeLabel.setStyleSheet(u"QLabel {\n"
"	color: white;\n"
"	background-color: rgba(0,0,0,0);\n"
"}")
        self.axWinSizeLabel.setAlignment(Qt.AlignCenter)
        self.startHeightLabel = QLabel(selectRoi)
        self.startHeightLabel.setObjectName(u"startHeightLabel")
        self.startHeightLabel.setGeometry(QRect(790, 110, 231, 51))
        self.startHeightLabel.setFont(font)
        self.startHeightLabel.setStyleSheet(u"QLabel {\n"
"	color: white;\n"
"	background-color: rgba(0,0,0,0);\n"
"}")
        self.startHeightLabel.setAlignment(Qt.AlignCenter)
        self.startDepthLabel = QLabel(selectRoi)
        self.startDepthLabel.setObjectName(u"startDepthLabel")
        self.startDepthLabel.setGeometry(QRect(790, 170, 231, 51))
        self.startDepthLabel.setFont(font)
        self.startDepthLabel.setStyleSheet(u"QLabel {\n"
"	color: white;\n"
"	background-color: rgba(0,0,0,0);\n"
"}")
        self.startDepthLabel.setAlignment(Qt.AlignCenter)
        self.endDepthLabel = QLabel(selectRoi)
        self.endDepthLabel.setObjectName(u"endDepthLabel")
        self.endDepthLabel.setGeometry(QRect(790, 220, 231, 51))
        self.endDepthLabel.setFont(font)
        self.endDepthLabel.setStyleSheet(u"QLabel {\n"
"	color: white;\n"
"	background-color: rgba(0,0,0,0);\n"
"}")
        self.endDepthLabel.setAlignment(Qt.AlignCenter)
        self.endHeightLabel = QLabel(selectRoi)
        self.endHeightLabel.setObjectName(u"endHeightLabel")
        self.endHeightLabel.setGeometry(QRect(790, 280, 231, 51))
        self.endHeightLabel.setFont(font)
        self.endHeightLabel.setStyleSheet(u"QLabel {\n"
"	color: white;\n"
"	background-color: rgba(0,0,0,0);\n"
"}")
        self.endHeightLabel.setAlignment(Qt.AlignCenter)
        self.clipFactorLabel = QLabel(selectRoi)
        self.clipFactorLabel.setObjectName(u"clipFactorLabel")
        self.clipFactorLabel.setGeometry(QRect(790, 340, 231, 51))
        self.clipFactorLabel.setFont(font)
        self.clipFactorLabel.setStyleSheet(u"QLabel {\n"
"	color: white;\n"
"	background-color: rgba(0,0,0,0);\n"
"}")
        self.clipFactorLabel.setAlignment(Qt.AlignCenter)
        self.dynRangeLabel = QLabel(selectRoi)
        self.dynRangeLabel.setObjectName(u"dynRangeLabel")
        self.dynRangeLabel.setGeometry(QRect(790, 400, 231, 51))
        self.dynRangeLabel.setFont(font)
        self.dynRangeLabel.setStyleSheet(u"QLabel {\n"
"	color: white;\n"
"	background-color: rgba(0,0,0,0);\n"
"}")
        self.dynRangeLabel.setAlignment(Qt.AlignCenter)
        self.depthLabel = QLabel(selectRoi)
        self.depthLabel.setObjectName(u"depthLabel")
        self.depthLabel.setGeometry(QRect(790, 470, 231, 51))
        self.depthLabel.setFont(font)
        self.depthLabel.setStyleSheet(u"QLabel {\n"
"	color: white;\n"
"	background-color: rgba(0,0,0,0);\n"
"}")
        self.depthLabel.setAlignment(Qt.AlignCenter)
        self.widthLabel = QLabel(selectRoi)
        self.widthLabel.setObjectName(u"widthLabel")
        self.widthLabel.setGeometry(QRect(790, 540, 231, 51))
        self.widthLabel.setFont(font)
        self.widthLabel.setStyleSheet(u"QLabel {\n"
"	color: white;\n"
"	background-color: rgba(0,0,0,0);\n"
"}")
        self.widthLabel.setAlignment(Qt.AlignCenter)
        self.exportResultsSidebar = QFrame(selectRoi)
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

        self.retranslateUi(selectRoi)

        QMetaObject.connectSlotsByName(selectRoi)
    # setupUi

    def retranslateUi(self, selectRoi):
        selectRoi.setWindowTitle(QCoreApplication.translate("selectRoi", u"Select Region of Interest", None))
#if QT_CONFIG(tooltip)
        self.sidebar.setToolTip(QCoreApplication.translate("selectRoi", u"<html><head/><body><p><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.imageSelectionLabelSidebar.setText(QCoreApplication.translate("selectRoi", u"Image Selection:", None))
        self.imageLabel.setText(QCoreApplication.translate("selectRoi", u"Image:", None))
        self.phantomLabel.setText(QCoreApplication.translate("selectRoi", u"Phantom:", None))
        self.imageFilenameDisplay.setText(QCoreApplication.translate("selectRoi", u"Sample filename ", None))
        self.phantomFilenameDisplay.setText(QCoreApplication.translate("selectRoi", u"Sample filename ", None))
        self.roiSidebarLabel.setText(QCoreApplication.translate("selectRoi", u"Region of Interest (ROI) Selection:", None))
        self.roiTitleLabel.setText(QCoreApplication.translate("selectRoi", u"ROI Name: ", None))
        self.roiNameDisplay.setText(QCoreApplication.translate("selectRoi", u"Sample filename ", None))
        self.analysisParamsLabel.setText(QCoreApplication.translate("selectRoi", u"Analysis Parameter Selection", None))
        self.rfAnalysisLabel.setText(QCoreApplication.translate("selectRoi", u"Radio Frequency Data Analysis", None))
        self.analysisParamsLabel_2.setText(QCoreApplication.translate("selectRoi", u"Select Radio Frequency Analysis Parameters:", None))
        self.continueButton.setText(QCoreApplication.translate("selectRoi", u"Continue", None))
        self.tiltLabel.setText(QCoreApplication.translate("selectRoi", u"Tilt", None))
        self.frameLabel.setText(QCoreApplication.translate("selectRoi", u"Frame", None))
        self.maxFreqLabel.setText(QCoreApplication.translate("selectRoi", u"Maximum Frequency (Hz)", None))
        self.minFreqLabel.setText(QCoreApplication.translate("selectRoi", u"MinimumFrequency (Hz)", None))
        self.latOverlapLabel.setText(QCoreApplication.translate("selectRoi", u"Lateral Overlap (%)", None))
        self.axOverlapLabel.setText(QCoreApplication.translate("selectRoi", u"Axial Overlap (%)", None))
        self.latWinSizeLabel.setText(QCoreApplication.translate("selectRoi", u"Lateral Window Size (mm)", None))
        self.axWinSizeLabel.setText(QCoreApplication.translate("selectRoi", u"Axial Window Size (mm)", None))
        self.startHeightLabel.setText(QCoreApplication.translate("selectRoi", u"Starting Height", None))
        self.startDepthLabel.setText(QCoreApplication.translate("selectRoi", u"Starting Depth", None))
        self.endDepthLabel.setText(QCoreApplication.translate("selectRoi", u"Ending Depth", None))
        self.endHeightLabel.setText(QCoreApplication.translate("selectRoi", u"Ending Height", None))
        self.clipFactorLabel.setText(QCoreApplication.translate("selectRoi", u"Clip Factor", None))
        self.dynRangeLabel.setText(QCoreApplication.translate("selectRoi", u"Dynamic Range", None))
        self.depthLabel.setText(QCoreApplication.translate("selectRoi", u"Depth (m)", None))
        self.widthLabel.setText(QCoreApplication.translate("selectRoi", u"Width (m)", None))
        self.exportResultsLabel.setText(QCoreApplication.translate("selectRoi", u"Export Results", None))
    # retranslateUi

