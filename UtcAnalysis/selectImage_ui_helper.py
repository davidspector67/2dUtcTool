from UtcAnalysis.selectImage_ui import *
from UtcAnalysis.roiSelection_ui_helper import *
import os
import shutil

def selectImageHelper(pathInput):
    if not os.path.exists(pathInput.text()): # check if file path is manually typed
        # NOTE: .bin is currently not supported
        fileName, _ = QFileDialog.getOpenFileName(None, 'Open File', filter = '*.rf *.mat')
        if fileName != '': # If valid file is chosen
            pathInput.setText(fileName)
        else:
            return


class SelectImageGUI(Ui_selectImage, QWidget):
    def __init__(self):
        # self.selectImage = QWidget()
        super().__init__()
        self.setupUi(self)
        self.chooseImageFileButton.setHidden(True)
        self.choosePhantomFileButton.setHidden(True)
        self.chooseImageFolderButton.setHidden(True)
        self.choosePhantomFolderButton.setHidden(True)
        self.clearImagePathButton.setHidden(True)
        self.clearPhantomPathButton.setHidden(True)
        self.selectImageErrorMsg.setHidden(True)
        self.generateImageButton.setHidden(True)
        self.imagePathFolderLabel.setHidden(True)
        self.phantomPathFolderLabel.setHidden(True)
        self.imagePathInput.setHidden(True)
        self.phantomPathInput.setHidden(True)
        self.imagePathLabel.setHidden(True)
        self.phantomPathLabel.setHidden(True)
        self.selectDataLabel.setHidden(True)
        self.imageFilenameDisplay.setHidden(True)
        self.phantomFilenameDisplay.setHidden(True)

        self.choosingIndividualFiles = False
        self.roiSelectionGUI = RoiSelectionGUI()
        
        self.selectIndFilesButton.clicked.connect(self.fileOptionSelected)
        self.selectFoldersButton.clicked.connect(self.folderOptionSelected)
        self.chooseImageFileButton.clicked.connect(self.selectImageFile)
        self.choosePhantomFileButton.clicked.connect(self.selectPhantomFile)
        self.clearImagePathButton.clicked.connect(self.clearImagePath)
        self.clearPhantomPathButton.clicked.connect(self.clearPhantomPath)
        self.generateImageButton.clicked.connect(self.moveToRoiSelection)

    def moveToRoiSelection(self):
        if os.path.exists(self.imagePathInput.text()) and os.path.exists(self.phantomPathInput.text()):
            self.roiSelectionGUI.setFilenameDisplays(self.imagePathInput.text().split('/')[-1], self.phantomPathInput.text().split('/')[-1])
            self.roiSelectionGUI.openImage(self.imagePathInput.text(), self.phantomPathInput.text())
            self.roiSelectionGUI.show()
            self.hide()
        
    def clearImagePath(self):
        self.imagePathInput.clear()

    def clearPhantomPath(self):
        self.phantomPathInput.clear()

    def chooseImagePrep(self):
        self.selectFoldersButton.setHidden(True)
        self.selectIndFilesButton.setHidden(True)
        self.imagePathInput.setHidden(False)
        self.phantomPathInput.setHidden(False)
        self.clearImagePathButton.setHidden(False)
        self.clearPhantomPathButton.setHidden(False)
        self.generateImageButton.setHidden(False)
        self.selectImageMethodLabel.setHidden(True)

    def fileOptionSelected(self): # Move user to screen to select individual files to generate image
        self.chooseImagePrep()
        self.selectDataLabel.setHidden(False)
        self.imagePathLabel.setHidden(False)
        self.phantomPathLabel.setHidden(False)
        self.chooseImageFileButton.setHidden(False)
        self.choosePhantomFileButton.setHidden(False)

        self.choosingIndividualFiles = True

    def folderOptionSelected(self): 
        # Move user to screen to select folders to find compatible files to generate image
        self.chooseImagePrep()
        self.selectDataLabel.setHidden(False)
        self.chooseImageFolderButton.setHidden(False)
        self.choosePhantomFolderButton.setHidden(False)
        self.imagePathFolderLabel.setHidden(False)
        self.phantomPathFolderLabel.setHidden(False)

        self.validPairs = []

    def selectImageFile(self):
        if not self.choosingIndividualFiles:
            return

        # Create folder to store ROI drawings
        if os.path.exists("imROIs"):
            shutil.rmtree("imROIs")
        os.mkdir("imROIs")

        selectImageHelper(self.imagePathInput)

    def selectPhantomFile(self):
        if not self.choosingIndividualFiles:
            return
        selectImageHelper(self.phantomPathInput)




if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    # selectWindow = QWidget()
    ui = SelectImageGUI()
    # ui.selectImage.show()
    ui.show()
    sys.exit(app.exec_())