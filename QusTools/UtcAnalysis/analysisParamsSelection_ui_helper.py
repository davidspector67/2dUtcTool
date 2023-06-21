from UtcAnalysis.analysisParamsSelection_ui import *
from UtcAnalysis.rfAnalysis_ui_helper import *
import os
from roiFuncs import *

def selectImageHelper(pathInput):
    if not os.path.exists(pathInput.text()): # check if file path is manually typed
        # NOTE: .bin is currently not supported
        fileName, _ = QFileDialog.getOpenFileName(None, 'Open File', filter = '*.rf *.mat')
        if fileName != '': # If valid file is chosen
            pathInput.setText(fileName)
        else:
            return


class AnalysisParamsGUI(Ui_analysisParams, QWidget):
    def __init__(self):
        # self.selectImage = QWidget()
        super().__init__()
        self.setupUi(self)

        self.rfAnalysisGUI = None

        self.continueButton.clicked.connect(self.continueToRfAnalysis)

    def setFilenameDisplays(self, imageName, phantomName):
        self.imagePathInput.setHidden(False)
        self.phantomPathInput.setHidden(False)
        self.imagePathInput.setText(imageName)
        self.phantomPathInput.setText(phantomName)

    def continueToRfAnalysis(self):
        self.rfAnalysisGUI.axialWinSize = self.axWinSizeVal.value()
        self.rfAnalysisGUI.lateralWinSize = self.latWinSizeVal.value()
        self.rfAnalysisGUI.axialOverlap = self.axOverlapVal.value()/100
        self.rfAnalysisGUI.lateralOverlap = self.latOverlapVal.value()/100
        self.rfAnalysisGUI.threshold = self.clipFactorVal.value()
        self.rfAnalysisGUI.minFrequency = self.minFreqVal.value()*1000000 # MHz -> Hz
        self.rfAnalysisGUI.maxFrequency = self.maxFreqVal.value()*1000000 # MHz -> Hz
        self.rfAnalysisGUI.samplingFreq = self.samplingFreqVal.value()*1000000 # MHz -> Hz
        self.rfAnalysisGUI.setFilenameDisplays(self.imagePathInput.text().split('/')[-1], self.phantomPathInput.text().split('/')[-1])
        self.rfAnalysisGUI.displayROIWindows()
        self.rfAnalysisGUI.show()
        self.hide()

            #      self.analysisParamsGUI.axWinSizeVal.setValue(10)#7#1#1480/20000000*10000 # must be at least 10 times wavelength
            # self.analysisParamsGUI.latWinSizeVal.setValue(10)#7#1#1480/20000000*10000 # must be at least 10 times wavelength
            # self.analysisParamsGUI.axOverlapVal.setValue(5)
            # self.analysisParamsGUI.latOverlapVal.setValue(5)
            # self.analysisParamsGUI.minFreqVal.setValue(3)
            # self.analysisParamsGUI.maxFreqVal.setValue(4.5)
            # self.analysisParamsGUI.startDepthVal.setValue(0.04)
            # self.analysisParamsGUI.endDepthVal.setValue(0.16)
            # self.analysisParamsGUI.clipFactorVal.setValue(95)
            # self.analysisParamsGUI.samplingFreqVal.setValue(20)
            # self.analysisParamsGUI.frameVal.setValue(self.frame)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    # selectWindow = QWidget()
    ui = AnalysisParamsGUI()
    # ui.selectImage.show()
    ui.show()
    sys.exit(app.exec_())