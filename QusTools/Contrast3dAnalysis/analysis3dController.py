from Contrast3dAnalysis.analysis3dGUI import Contrast3dAnalysisGUI
import os
import Contrast3dAnalysis.ParaMapFunctionsParallel_v1 as pm
import Contrast3dAnalysis.lognormalFunctions as lf
from itertools import chain
import platform
from Contrast3dAnalysis.ticEditor import TICEditorGUI
import matlab.engine
import scipy.signal
import scipy.interpolate as interpolate
from scipy.interpolate import griddata
from scipy.io import loadmat
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt, QLine
from PyQt5.QtGui import QPixmap, QImage, QPainter, QBitmap, QColor
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import nibabel as nib
import itk
import cv2
import pyvista as pv
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import shutil
from MCWindowComparison.MCWindowComparison import Ui_MainWindow


# When running for testing, use the below code to silence invalid value in log warning.
# Both warnings are handled in code. However, when making adjustments/debugging, comment out the 
# below warning suppressing code

# import warnings
# warnings.filterwarnings("ignore")

system = platform.system()
eng = matlab.engine.start_matlab()

class Contrast3dAnalysisController(Contrast3dAnalysisGUI):
    def __init__(self):
        super().__init__()

        self.chooseFileButton.clicked.connect(self.getTextInput) #get the text input of nifti path
        self.openIMGButton.clicked.connect(self.openInitialImageSlices) #opens initial slices
        self.clearFileButton.clicked.connect(self.clearInputFilePath) #clear nifti file path

        self.axialScroll.valueChanged.connect(self.changeAxialSlices) #scrolls through slices
        self.sagScroll.valueChanged.connect(self.changeSagSlices)
        self.corScroll.valueChanged.connect(self.changeCorSlices)

        self.expandAxialButton.clicked.connect(self.enlargeAxImg) #expands certain slices
        self.expandSagButton.clicked.connect(self.enlargeSagImg)
        self.expandCorButton.clicked.connect(self.enlargeCorImg)        
        self.closeExpandButton.clicked.connect(self.closeExpandedImg)

        self.acceptPolygonButton.clicked.connect(self.acceptPolygon) #called to exit the paint function
        self.undoLastPtButton.clicked.connect(self.undoLastPoint) #deletes last drawn rectangle if on sag or cor slices

        self.interpolateVOIButton.clicked.connect(self.voi3dInterpolation) #is the current binary masking function, makes whatever is not ROI black
        self.computeTICButton.clicked.connect(self.showTic)
        self.undoLastROIButton.clicked.connect(self.undoLastRectangle)
        self.drawPolygonButton.clicked.connect(self.startROIDraw)

        # self.chooseScrollValAx.currentIndexChanged.connect(self.quickNavigateAxial) #called when combobox clicked
        # self.chooseScrollValSag.currentIndexChanged.connect(self.quickNavigateSag)
        # self.chooseScrollValCor.currentIndexChanged.connect(self.quickNavigateCor)

        self.saveSegImgAx.clicked.connect(self.saveNiftiAxial) #will compile .png masks into single .nii for axial plane
        self.saveSegImgSag.clicked.connect(self.saveNiftiSag)
        self.saveSegImgCor.clicked.connect(self.saveNiftiCor)

        self.xmlOptionSetUp() #setup for Julie's MC code
        # self.motionCorrectionSetUp()
        self.interpolateBetweenMasksButton.clicked.connect(self.interpolating) #just added this function to interpolate masks, nonfunctional yet
        self.interpolateBetweenMasksButton.setHidden(True)

        self.aucParamapButton.clicked.connect(self.showAuc)
        self.peParamapButton.clicked.connect(self.showPe)
        self.tpParamapButton.clicked.connect(self.showTp)
        self.mttParamapButton.clicked.connect(self.showMtt)


    # FIRST STEP: get the input text of the nifti input line edit
#-------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------
    # if file path is entered, check that it exists and get it, otherwise, let user
    # browse themselves for a valid nifti file; also makes directories to store drawings and masks made
    def getTextInput(self) :
        #David edits
        #remove pre-existing files if need be
        if os.path.exists("niftiROIs"):
            shutil.rmtree("niftiROIs") #will also remove all the drawings made
        if os.path.exists("niftiMasks"):
            shutil.rmtree("niftiMasks") #will remove all the masks made from drawings
        if os.path.exists("niftiBinaryMasks"):
            shutil.rmtree("niftiBinaryMasks")

        # Original started here
        os.mkdir("niftiROIs") #for drawings
        os.mkdir("niftiMasks") #was used for the masks that had transparent background, but currently not used
        os.mkdir("niftiBinaryMasks") #for binary masks

        if os.path.exists(self.niftiLineEdit.text()):
            self.inputTextPath = self.niftiLineEdit.text()
            self.feedbackText.setText("valid file chosen - press 'open image'")
        else:
            fileName, _ = QFileDialog.getOpenFileName(None, 'Open File', filter = '*.nii *.rf *.nii.gz *.mat *.dat')
            if fileName != '':
                self.niftiLineEdit.setText(fileName)
                self.inputTextPath = self.niftiLineEdit.text()
                self.feedbackText.setText("valid file chosen - press 'open image'")


# SECOND STEP: does a double check for valid file type and then displays the initial slices into QLabels
#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
    # displays all the initial 2D slices for axial, sag and coronal planes
    # sets the max of scroll bars and gets dimensions of each slice
    def openInitialImageSlices(self):
        if len(self.inputTextPath):
            if (self.inputTextPath.endswith('.nii') or self.inputTextPath.endswith('.nii.gz')):
                self.nibImg = nib.load(self.inputTextPath, mmap=False)
                self.dataNibImg = self.nibImg.get_fdata()
                self.dataNibImg = self.dataNibImg.astype(np.uint8)
                self.windowsComputed = False
                self.is3d = False
            if (self.inputTextPath.endswith('.mat')):
                # s = eng.genpath(str(os.getcwd()+'/Machine_Code/Philips'))
                # eng.addpath(s, nargout=0)
                # path_list = self.inputTextPath.split('/')
                # path_dir = ""
                # for i in range(len(path_list)-1):
                #     path_dir += str(path_list[i]+'/')
                matData = loadmat(self.inputTextPath)['data'][0][0]
                rfdata = matData[0][0]
                numFrame = matData[1][0][0]
                pt = matData[2][0][0]
                multilinefactor = matData[3][0][0]
                numSonoCTAngles = matData[4][0][0]
                tdxBeamperFrame = matData[5][0][0]
                # data_3d = mat_data[6].clip(0,255).astype(np.uint8)
                data3d = matData[6]
                # hi = np.amax(data_3d)
                # self.parsed_data = self.nibImg['data_3d']
                # self.parsed_data = eng.main_parser_stanford(path_dir, path_list[-1],3)
                # self.dataNibImg = np.asarray(self.parsed_data)
                # self.dataNibImg = self.dataNibImg.astype(np.uint8)
                bmode = 20*np.log10(abs(scipy.signal.hilbert(data3d)))
                hi = np.amax(bmode)
                yo = np.amin(bmode)
                self.dataNibImg = bmode
                self.windowsComputed = False
                self.is3d = True
            if (self.inputTextPath.endswith('.dat')):
                header = np.fromfile(self.inputTextPath, np.int32, 3)
                nsamples, multilineFactor, nlines = header
                rfArray = np.fromfile(self.inputTextPath, np.int32, nsamples*multilineFactor*nlines, offset=header.size*np.dtype(np.int32).itemsize)
                rf = np.reshape(rfArray, [nsamples, multilineFactor, nlines], order='F')
                bmode = 20*np.log10(abs(scipy.signal.hilbert(rf)))
                s = eng.genpath(str(os.getcwd()+'../../Machine_Code/Philips'))
                eng.addpath(s, nargout=0)
                test = np.asarray(eng.parseRF(self.inputTextPath, 0, 2000, "-dat"))
                self.dataNibImg = bmode
                self.windowsComputed = False
                self.is3d = True

            self.feedbackText.setText("can use 'draw rectangle' to select ROI by dragging")

            self.OGData4dImg = self.dataNibImg.copy()
            self.data4dImg = self.dataNibImg
            if self.is3d:
                self.x, self.y, self.z = self.data4dImg.shape
            else:
                self.x, self.y, self.z, self.numSlices = self.data4dImg.shape
            self.maskCoverImg = np.zeros([self.x, self.y, self.z,4])
            if not self.is3d:
                self.slicesChanger.setMaximum(self.numSlices-1)
                self.curSlices.setText(str(self.curSlice+1))
                self.totalSlices.setText(str(self.numSlices))
                self.slicesChanger.valueChanged.connect(self.sliceValueChanged)
                self.slicesChanger.setDisabled(False)

            self.x -= 1
            self.y -= 1
            self.z -= 1

            self.axialScroll.setMaximum(self.z)
            self.sagScroll.setMaximum(self.x)
            self.corScroll.setMaximum(self.y)

            self.axialScroll.setValue(0)
            self.sagScroll.setValue(0)
            self.corScroll.setValue(0)

            self.totalFramesAx.setText(str(self.z+1))
            self.totalFramesSag.setText(str(self.x+1))
            self.totalFramesCor.setText(str(self.y+1))

            self.currentFrameAx.setText("1")
            self.currentFrameSag.setText("1")
            self.currentFrameCor.setText("1")

            tempAx = self.maskCoverImg[:,:,0,:] #2D data for axial
            tempAx = np.flipud(tempAx) #flipud
            tempAx = np.rot90(tempAx,3) #rotate ccw 270
            tempAx = np.require(tempAx,np.uint8, 'C')

            tempSag = self.maskCoverImg[0,:,:,:] #2D data for sagittal
            tempSag = np.flipud(tempSag) #flipud
            tempSag = np.rot90(tempSag,2) #rotate ccw 180
            tempSag = np.fliplr(tempSag)
            tempSag = np.require(tempSag,np.uint8,'C')

            tempCor = self.maskCoverImg[:,0,:,:] #2D data for coronal
            tempCor = np.rot90(tempCor,1) #rotate ccw 90
            tempCor = np.flipud(tempCor) #flipud
            tempCor = np.require(tempCor,np.uint8,'C')

            self.maskAxH, self.maskAxW = tempAx[:,:,0].shape #getting height and width for each plane
            self.maskSagH, self.maskSagW = tempSag[:,:,0].shape
            self.maskCorH, self.maskCorW = tempCor[:,:,0].shape

            self.maskBytesLineAx, _ = tempAx[:,:,0].strides #in order to create proper QImage, need to know bytes/line
            self.maskBytesLineSag, _ = tempSag[:,:,0].strides
            self.maskBytesLineCor, _ = tempCor[:,:,0].strides

            self.curMaskAxIm = QImage(tempAx, self.maskAxW, self.maskAxH, self.maskBytesLineAx, QImage.Format_ARGB32) #creating QImage
            self.curMaskSagIm = QImage(tempSag, self.maskSagW, self.maskSagH, self.maskBytesLineSag, QImage.Format_ARGB32)
            self.curMaskCorIm = QImage(tempCor, self.maskCorW, self.maskCorH, self.maskBytesLineCor, QImage.Format_ARGB32)

            self.maskLayerAx.setPixmap(QPixmap.fromImage(self.curMaskAxIm).scaled(331,311)) #displaying QPixmap in the QLabels
            self.maskLayerSag.setPixmap(QPixmap.fromImage(self.curMaskSagIm).scaled(331,311))
            self.maskLayerCor.setPixmap(QPixmap.fromImage(self.curMaskCorIm).scaled(331,311))
            self.maskLayerAx.setMouseTracking(True)
            self.maskLayerSag.setMouseTracking(True)
            self.maskLayerCor.setMouseTracking(True)


            #create a list for frames in combobox for easy navigation
            self.listAxial = []
            for n in range(self.z):
                self.listAxial.append("Slice " + str(n+1))
            self.listSag = []
            for m in range(self.x):
                self.listSag.append("Slice " + str(m+1))
            self.listCor = []
            for l in range(self.y):
                self.listCor.append("Slice " + str(l+1))

            #add these lists to the combobox
            # self.chooseScrollvalAxial.addItems(self.listAxial)
            # self.chooseScrollvalSag.addItems(self.listSag)
            # self.chooseScrollvalCor.addItems(self.listCor)
            # self.chooseScrollvalAxial.setHidden(True)
            # self.chooseScrollvalSag.setHidden(True)
            # self.chooseScrollvalCor.setHidden(True)
            self.drawPolygonButton.setCheckable(True)

            #set current index for combobox
            # self.chooseScrollvalAxial.setCurrentIndex(0)
            # self.chooseScrollvalSag.setCurrentIndex(0)
            # self.chooseScrollvalCor.setCurrentIndex(0)

            #getting initial image data for axial, sag, coronal slices
            if not self.is3d:
                self.data2dAx = self.data4dImg[:,:,0, self.curSlice] #2D data for axial
                self.data2dAx = np.flipud(self.data2dAx) #flipud
                self.data2dAx = np.rot90(self.data2dAx,3) #rotate ccw 270
            else:
                self.data2dAx = self.data4dImg[:,:,0]
            self.data2dAx = np.require(self.data2dAx,np.uint8, 'C')

            if self.is3d:
                self.data2dSag = self.data4dImg[0,:,:]
            else:
                self.data2dSag = self.data4dImg[0,:,:, self.curSlice] #2D data for sagittal
                self.data2dSag = np.flipud(self.data2dSag) #flipud
                self.data2dSag = np.rot90(self.data2dSag,2) #rotate ccw 180
                self.data2dSag = np.fliplr(self.data2dSag)
            self.data2dSag = np.require(self.data2dSag,np.uint8,'C')

            if self.is3d:
                self.data2dCor = self.data4dImg[:,0,:]
            else:
                self.data2dCor = self.data4dImg[:,0,:, self.curSlice] #2D data for coronal
                self.data2dCor = np.rot90(self.data2dCor,1) #rotate ccw 90
                self.data2dCor = np.flipud(self.data2dCor) #flipud
            self.data2dCor = np.require(self.data2dCor,np.uint8,'C')

            self.heightAx, self.widthAx = self.data2dAx.shape #getting height and width for each plane
            self.heightSag, self.widthSag = self.data2dSag.shape
            self.heightCor, self.widthCor = self.data2dCor.shape

            self.bytesLineAx, _ = self.data2dAx.strides #in order to create proper QImage, need to know bytes/line
            self.bytesLineSag, _ = self.data2dSag.strides
            self.bytesLineCor, _ = self.data2dCor.strides

            self.qImgAx = QImage(self.data2dAx, self.widthAx, self.heightAx, self.bytesLineAx, QImage.Format_Grayscale8) #creating QImage
            self.qImgSag = QImage(self.data2dSag, self.widthSag, self.heightSag, self.bytesLineSag, QImage.Format_Grayscale8)
            self.qImgCor = QImage(self.data2dCor, self.widthCor, self.heightCor, self.bytesLineCor, QImage.Format_Grayscale8)

            self.pixmapAx = QPixmap.fromImage(self.qImgAx).scaled(331,311) #creating QPixmap from QImage
            self.pixmapSag = QPixmap.fromImage(self.qImgSag).scaled(331,311)
            self.pixmapCor = QPixmap.fromImage(self.qImgCor).scaled(331,311)

            self.axialPlane.setPixmap(self.pixmapAx) #displaying QPixmap in the QLabels
            self.sagPlane.setPixmap(self.pixmapSag)
            self.corPlane.setPixmap(self.pixmapCor)

            self.imagesOpened = True
            self.scrolling = True
            self.axCoverLabel.setCursor(Qt.BlankCursor)
            self.sagCoverLabel.setCursor(Qt.BlankCursor)
            self.corCoverLabel.setCursor(Qt.BlankCursor)
            self.newXVal = 0
            self.newYVal = 0
            self.newZVal = 0

            self.curAlpha.setDisabled(False)
            self.curAlpha.valueChanged.connect(self.alphaValueChanged)
            self.curAlpha.setValue(255)

        else:
            self.feedbackText.setText("invalid file type - try again")


# THIRD STEP: if incorrect file path, make easier for user to clear input
#----------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------
    #to clear the file path to input a new one as well as clear all the directories created for saving drawings
    #of ROIs and masks of that particular image
    def clearInputFilePath(self):
        self.niftiLineEdit.clear()
        if os.path.exists("niftiROIs"):
            shutil.rmtree("niftiROIs") #will also remove all the drawings made
        if os.path.exists("niftiMasks"):
            shutil.rmtree("niftiMasks") #will remove all the masks made from drawings
        if os.path.exists("niftiBinaryMasks"):
            shutil.rmtree("niftiBinaryMasks")

    def sliceValueChanged(self):
        self.curSlice = self.slicesChanger.value()
        self.curSlices.setText(str(self.curSlice+1))
        self.changeAxialSlices()
        self.changeSagSlices()
        self.changeCorSlices()

    def alphaValueChanged(self):
        self.alphaTracker.setValue(int(self.curAlpha.value()))
        for i in range(len(self.pointsPlotted)):
            self.maskCoverImg[self.pointsPlotted[i][0], self.pointsPlotted[i][1], self.pointsPlotted[i][2],3] = int(self.curAlpha.value())
        self.changeAxialSlices()
        self.changeSagSlices()
        self.changeCorSlices()


# FOURTH STEP: if correct file path and type, be able to scroll through all slices
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def changeAxialSlices(self):

        # David --> what's the point of this?
        #if image is not expanded
        if self.newZVal > 98 and self.axialTextLabel.isHidden() is False:
            self.currentFrameAx.move(762,340)

        #if image is expanded
        if self.newZVal > 98 and self.axialTextLabel.isHidden() : 
            self.currentFrameAx.move(1040, 680) # David --> was 1032

        self.currentFrameAx.setText(str(self.newZVal+1))

        if not self.is3d:
            self.data2dAx = self.data4dImg[:,:,self.newZVal, self.curSlice]#, self.curSlice] #defining 2D data for axial
            self.data2dAx = np.flipud(self.data2dAx) #flipud
            self.data2dAx = np.rot90(self.data2dAx,3) #rotate
        else:
            self.data2dAx = self.data4dImg[:,:,self.newZVal]
        self.data2dAx = np.require(self.data2dAx,np.uint8,'C')

        self.bytesLineAx, _ = self.data2dAx.strides
        self.qImgAx = QImage(self.data2dAx,self.widthAx, self.heightAx, self.bytesLineAx, QImage.Format_Grayscale8)

        self.outputMaskNameAx = str("maskAx_" + str(self.axialScroll.value())) #defining file name for transparent background masks -- not really used, but left here just in case
        self.output_ax_mask_file = str(self.outputMaskNameAx + ".png")

        self.output_ax_name = str("drawn_ax_" + str(self.axialScroll.value())) #defining file name for images with ROIs -- used
        self.output_ax_name_file = str(self.output_ax_name + ".png")

        tempAx = self.maskCoverImg[:,:,self.newZVal,:] #2D data for axial
        tempAx = np.flipud(tempAx) #flipud
        tempAx = np.rot90(tempAx,3) #rotate ccw 270
        tempAx = np.require(tempAx,np.uint8, 'C')

        self.curMaskAxIm = QImage(tempAx, self.maskAxW, self.maskAxH, self.maskBytesLineAx, QImage.Format_ARGB32) #creating QImage

        if self.id == 0:
            self.maskLayerAx.setPixmap(QPixmap.fromImage(self.curMaskAxIm).scaled(331,311)) #displaying QPixmap in the QLabels
            self.axialPlane.setPixmap(QPixmap.fromImage(self.qImgAx).scaled(331,311)) #otherwise, would just display the normal unmodified q_img
        elif self.id == 1:
            self.maskLayerAx.setPixmap(QPixmap.fromImage(self.curMaskAxIm).scaled(680, 638))
            self.axialPlane.setPixmap(QPixmap.fromImage(self.qImgAx).scaled(680,638)) #otherwise, would just display the normal unmodified q_img


    def changeSagSlices(self):

        #if image is not expanded
        if self.newXVal > 98 and self.axialTextLabel.isHidden() is False:
            self.currentFrameSag.move(1092,340)

        #if image is expanded
        if self.newXVal > 98 and self.axialTextLabel.isHidden() :
            self.currentFrameSag.move(1032, 680)

        self.currentFrameSag.setText(str(self.newXVal+1))

        if not self.is3d:
            self.data2dSag = self.data4dImg[self.newXVal,:,:, self.curSlice]#, self.curSlice]
            self.data2dSag = np.flipud(self.data2dSag) #flipud
            self.data2dSag = np.rot90(self.data2dSag,2) #rotate
            self.data2dSag = np.fliplr(self.data2dSag)
        else:
            self.data2dSag = self.data4dImg[self.newXVal,:,:]
        self.data2dSag = np.require(self.data2dSag,np.uint8,'C')

        self.bytesLineSag, _ = self.data2dSag.strides
        self.qImgSag = QImage(self.data2dSag,self.widthSag, self.heightSag, self.bytesLineSag, QImage.Format_Grayscale8)

        self.output_sag_name = str("drawn_sag_" + str(self.sagScroll.value()))
        self.output_sag_name_file = str(self.output_sag_name + ".png")

        self.outputMaskNameSag = str("maskSag_" + str(self.sagScroll.value()))
        self.output_sag_mask_file = str(self.outputMaskNameSag + ".png")

        tempSag = self.maskCoverImg[self.newXVal,:,:,:] #2D data for sagittal
        tempSag = np.flipud(tempSag) #flipud
        tempSag = np.rot90(tempSag,2) #rotate ccw 180
        tempSag = np.fliplr(tempSag)
        tempSag = np.require(tempSag,np.uint8,'C')
        
        self.curMaskSagIm = QImage(tempSag, self.maskSagW, self.maskSagH, self.maskBytesLineSag, QImage.Format_ARGB32)

        if self.id == 0:
            self.maskLayerSag.setPixmap(QPixmap.fromImage(self.curMaskSagIm).scaled(331,311))
            self.sagPlane.setPixmap(QPixmap.fromImage(self.qImgSag).scaled(331,311))
        elif self.id == 2:
            self.maskLayerSag.setPixmap(QPixmap.fromImage(self.curMaskSagIm).scaled(680, 638))
            self.sagPlane.setPixmap(QPixmap.fromImage(self.qImgSag).scaled(680,638))


    def changeCorSlices(self):

        #if image is not expanded
        if self.newYVal > 98 and self.axialTextLabel.isHidden() is False:
            self.currentFrameCor.move(1090,700)

        #if image is expanded
        if self.newYVal > 98 and self.axialTextLabel.isHidden() :
            self.currentFrameCor.move(1022, 680)

        self.currentFrameCor.setText(str(self.newYVal+1))

        if not self.is3d:
            self.data2dCor = self.data4dImg[:,self.newYVal,:, self.curSlice]#, self.curSlice]
            self.data2dCor = np.rot90(self.data2dCor,1) #rotate
            self.data2dCor = np.flipud(self.data2dCor) #flipud
        else:
            self.data2dCor = self.data4dImg[:,self.newYVal,:]
        self.data2dCor = np.require(self.data2dCor, np.uint8,'C')

        self.bytesLineCor, _ = self.data2dCor.strides
        self.qImgCor = QImage(self.data2dCor,self.widthCor,self.heightCor, self.bytesLineCor, QImage.Format_Grayscale8)

        self.output_cor_name = str("drawn_cor_" + str(self.corScroll.value()))
        self.output_cor_name_file = str(self.output_cor_name + ".png")

        self.outputMaskNameCor = str("maskCor_" + str(self.corScroll.value()))
        self.output_cor_mask_file = str(self.outputMaskNameCor + ".png")

        tempCor = self.maskCoverImg[:,self.newYVal,:,:] #2D data for coronal
        tempCor = np.rot90(tempCor,1) #rotate ccw 90
        tempCor = np.flipud(tempCor) #flipud
        tempCor = np.require(tempCor,np.uint8,'C')

        self.curMaskCorIm = QImage(tempCor, self.maskCorW, self.maskCorH, self.maskBytesLineCor, QImage.Format_ARGB32)

        if self.id == 0:
            self.maskLayerCor.setPixmap(QPixmap.fromImage(self.curMaskCorIm).scaled(331,311))
            self.corPlane.setPixmap(QPixmap.fromImage(self.qImgCor).scaled(331,311))

        elif self.id == 3:
            self.maskLayerCor.setPixmap(QPixmap.fromImage(self.curMaskCorIm).scaled(680, 638))
            self.corPlane.setPixmap(QPixmap.fromImage(self.qImgCor).scaled(680,638))


# FIFTH STEP: if want to enlarge images of certain cut, can do so
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------------------
    def enlargeAxImg(self):
        if self.id != 0:
            self.closeExpandedImg()
        if self.id != 1 and self.imagesOpened:
            self.id = 1 #to help painter identify which plane was enlarged
            self.axialPlane.setHidden(False)
            self.ofTextAx.setHidden(False)
            self.currentFrameAx.setHidden(False)
            self.totalFramesAx.setHidden(False)
            # self.save_seg_Axial.setHidden(False)
            self.alphaTracker.setHidden(True)
            self.curAlpha.setHidden(True)
            self.curSlices.setHidden(True)
            self.totalSlices.setHidden(True)
            self.slicesChanger.setHidden(True)
            self.legend.setHidden(True)
            self.slicesLabel.setHidden(True)
            self.alphaLabel.setHidden(True)
            self.slicesOf.setHidden(True)
            self.axialPlane.move(470,30)
            self.axialPlane.resize(680,638)
            self.axCoverLabel.move(470, 30)
            self.axCoverLabel.resize(680, 638)
            self.maskLayerAx.move(470, 30)
            self.maskLayerAx.resize(680, 638)
            tempAx = self.maskCoverImg[:,:,self.newZVal,:] #2D data for axial
            tempAx = np.flipud(tempAx) #flipud
            tempAx = np.rot90(tempAx,3) #rotate ccw 270
            tempAx = np.require(tempAx,np.uint8, 'C')
            self.curMaskAxIm = QImage(tempAx, self.maskAxW, self.maskAxH, self.maskBytesLineAx, QImage.Format_ARGB32) #creating QImage
            self.maskLayerAx.setPixmap(QPixmap.fromImage(self.curMaskAxIm).scaled(680,638)) #displaying QPixmap in the QLabels
            self.maskLayerSag.setHidden(True)
            self.maskLayerCor.setHidden(True)
            self.axCoverPixmap = QPixmap(680, 638)
            self.axCoverPixmap.fill(Qt.transparent)
            self.axCoverLabel.setPixmap(self.axCoverPixmap)
            self.sagCoverLabel.setHidden(True)
            self.corCoverLabel.setHidden(True)
            self.compressLabel.setHidden(True)
            self.compressValue.setHidden(True)
            self.windowHeightLabel.setHidden(True)
            self.windowDepthLabel.setHidden(True)
            self.windowWidthLabel.setHidden(True)
            self.windowHeightValue.setHidden(True)
            self.windowDepthValue.setHidden(True)
            self.windowWidthValue.setHidden(True)
            self.legend.setHidden(True)

            self.axialScroll.move(1150,30)
            self.axialScroll.resize(16,638)

            self.sagPlane.setHidden(True) #hide other labels which would get in way of displaying expanded image
            self.corPlane.setHidden(True)

            self.axialTextLabel.setHidden(True)
            self.sagTextLabel.setHidden(True)
            self.corTextLabel.setHidden(True)

            self.ofTextSag.setHidden(True)
            self.ofTextCor.setHidden(True)
            self.currentFrameSag.setHidden(True)
            self.currentFrameCor.setHidden(True)
            self.totalFramesSag.setHidden(True)
            self.totalFramesCor.setHidden(True)

            # self.save_seg_Axial.setHidden(True)
            # self.save_seg_Sag.setHidden(True)
            # self.save_seg_Cor.setHidden(True)

            # self.chooseScrollvalAxial.setHidden(True)
            # self.chooseScrollvalSag.setHidden(True)
            # self.chooseScrollvalCor.setHidden(True)
            self.corScroll.setHidden(True)

            self.currentFrameAx.move(1040, 680)
            self.ofTextAx.move(1060, 680)
            self.totalFramesAx.move(1075, 680)

            self.axialPlane.setPixmap(QPixmap.fromImage(self.qImgAx).scaled(680,638))

            tempAx = self.maskCoverImg[:,:,self.newZVal,:] #2D data for axial
            tempAx = np.flipud(tempAx) #flipud
            tempAx = np.rot90(tempAx,3) #rotate ccw 270  
            tempAx = np.require(tempAx,np.uint8, 'C')

            self.curMaskAxIm = QImage(tempAx, self.maskAxW, self.maskAxH, self.maskBytesLineAx, QImage.Format_ARGB32) #creating QImage
            self.maskLayerAx.setPixmap(QPixmap.fromImage(self.curMaskAxIm).scaled(680,638)) #displaying QPixmap in the QLabels
            self.axCoverLabel.pixmap().fill(Qt.transparent)
            painter = QPainter(self.axCoverLabel.pixmap())
            painter.setPen(Qt.yellow)
            axVertLine = QLine(int(self.newXVal/self.x*680), 0, int(self.newXVal/self.x*680), 638)
            axLatLine = QLine(0, int(self.newYVal/self.y*638), 680, int(self.newYVal/self.y*638))
            painter.drawLines([axVertLine, axLatLine])
            painter.end()

    def enlargeSagImg(self):
        if self.id != 0:
            self.closeExpandedImg()
        if self.id != 2 and self.imagesOpened:
            self.sagCoverLabel.move(470, 30)
            self.sagCoverLabel.resize(680, 638)
            self.sagCoverPixmap = QPixmap(680, 638)
            self.sagCoverPixmap.fill(Qt.transparent)
            self.sagCoverLabel.setPixmap(self.sagCoverPixmap)
            self.axCoverLabel.setHidden(True)
            self.corCoverLabel.setHidden(True)
            self.alphaTracker.setHidden(True)
            self.curAlpha.setHidden(True)
            self.curSlices.setHidden(True)
            self.totalSlices.setHidden(True)
            self.slicesChanger.setHidden(True)
            self.slicesLabel.setHidden(True)
            self.alphaLabel.setHidden(True)
            self.slicesOf.setHidden(True)
            self.legend.setHidden(True)
            self.id = 2
            self.sagPlane.setHidden(False)
            self.ofTextSag.setHidden(False)
            self.currentFrameSag.setHidden(False)
            self.totalFramesSag.setHidden(False)
            # self.save_seg_Sag.setHidden(False)
            self.sagPlane.move(470,30)
            self.sagPlane.resize(680,638)
            self.maskLayerSag.move(470, 30)
            self.maskLayerSag.resize(680, 638)
            self.maskLayerAx.setHidden(True)
            self.maskLayerCor.setHidden(True)
            self.compressLabel.setHidden(True)
            self.compressValue.setHidden(True)
            self.windowHeightLabel.setHidden(True)
            self.windowDepthLabel.setHidden(True)
            self.windowWidthLabel.setHidden(True)
            self.windowHeightValue.setHidden(True)
            self.windowDepthValue.setHidden(True)
            self.windowWidthValue.setHidden(True)
            self.legend.setHidden(True)

            self.sagScroll.move(1150,30)
            self.sagScroll.resize(16,638)
            self.corScroll.resize(16,1)

            self.axialPlane.setHidden(True)
            self.corPlane.setHidden(True)

            self.axialTextLabel.setHidden(True)
            self.sagTextLabel.setHidden(True)
            self.corTextLabel.setHidden(True)

            self.ofTextAx.setHidden(True)
            self.ofTextCor.setHidden(True)
            self.currentFrameAx.setHidden(True)
            self.currentFrameCor.setHidden(True)
            self.totalFramesAx.setHidden(True)
            self.totalFramesCor.setHidden(True)

            # self.save_seg_Axial.setHidden(True)
            # self.save_seg_Sag.setHidden(True)
            # self.save_seg_Cor.setHidden(True)

            # self.chooseScrollvalAxial.setHidden(True)
            # self.chooseScrollvalSag.setHidden(True)
            # self.chooseScrollvalCor.setHidden(True)

            self.currentFrameSag.move(1040, 680)
            self.ofTextSag.move(1060,680)
            self.totalFramesSag.move(1075,680)

            self.sagPlane.setPixmap(QPixmap.fromImage(self.qImgSag).scaled(680,638)) #otherwise, would just display the normal unmodified q_img

            self.sagCoverLabel.pixmap().fill(Qt.transparent)
            painter = QPainter(self.sagCoverLabel.pixmap())
            painter.setPen(Qt.yellow)
            sagVertLine = QLine(int(self.newZVal/self.z*680), 0, int(self.newZVal/self.z*680), 638)
            sagLatLine = QLine(0, int(self.newYVal/self.y*638), 680, int(self.newYVal/self.y*638))
            painter.drawLines([sagVertLine, sagLatLine])
            painter.end()
            
            tempSag = self.maskCoverImg[self.newXVal,:,:,:] #2D data for sagittal
            tempSag = np.flipud(tempSag) #flipud
            tempSag = np.rot90(tempSag,2) #rotate ccw 180
            tempSag = np.fliplr(tempSag)
            tempSag = np.require(tempSag,np.uint8,'C')

            self.curMaskSagIm = QImage(tempSag, self.widthSag, self.heightSag, self.maskBytesLineSag, QImage.Format_ARGB32)
            self.maskLayerSag.setPixmap(QPixmap.fromImage(self.curMaskSagIm).scaled(680, 638))
        self.corScroll.setHidden(True)
       

    def enlargeCorImg(self):
        if self.id != 0:
            self.closeExpandedImg()
        if self.id != 3 and self.imagesOpened:
            self.corCoverLabel.move(470, 30)
            self.corCoverLabel.resize(680, 638)
            self.corCoverPixmap = QPixmap(680, 638)
            self.corCoverPixmap.fill(Qt.transparent)
            self.corCoverLabel.setPixmap(self.corCoverPixmap)
            self.axCoverLabel.setHidden(True)
            self.sagCoverLabel.setHidden(True)
            self.alphaTracker.setHidden(True)
            self.curAlpha.setHidden(True)
            self.curSlices.setHidden(True)
            self.totalSlices.setHidden(True)
            self.slicesChanger.setHidden(True)
            self.slicesLabel.setHidden(True)
            self.alphaLabel.setHidden(True)
            self.slicesOf.setHidden(True)
            self.legend.setHidden(True)
            self.id = 3
            self.corPlane.setHidden(False)
            self.ofTextCor.setHidden(False)
            self.currentFrameCor.setHidden(False)
            self.totalFramesCor.setHidden(False)
            # self.save_seg_Cor.setHidden(False)
            self.corPlane.move(470,30)
            self.corPlane.resize(680,638)
            self.maskLayerCor.move(470, 30)
            self.maskLayerCor.resize(680, 638)
            self.maskLayerAx.setHidden(True)
            self.maskLayerSag.setHidden(True)
            self.compressLabel.setHidden(True)
            self.compressValue.setHidden(True)
            self.windowHeightLabel.setHidden(True)
            self.windowDepthLabel.setHidden(True)
            self.windowWidthLabel.setHidden(True)
            self.windowHeightValue.setHidden(True)
            self.windowDepthValue.setHidden(True)
            self.windowWidthValue.setHidden(True)
            self.legend.setHidden(True)

            self.corScroll.move(1150,30)
            self.corScroll.resize(16,638)

            self.axialPlane.setHidden(True)
            self.sagPlane.setHidden(True)

            self.axialTextLabel.setHidden(True)
            self.sagTextLabel.setHidden(True)
            self.corTextLabel.setHidden(True)

            self.ofTextAx.setHidden(True)
            self.ofTextSag.setHidden(True)
            self.currentFrameAx.setHidden(True)
            self.currentFrameSag.setHidden(True)
            self.totalFramesAx.setHidden(True)
            self.totalFramesSag.setHidden(True)

            # self.save_seg_Axial.setHidden(True)
            # self.save_seg_Sag.setHidden(True)
            # self.save_seg_Cor.setHidden(True)

            # self.chooseScrollvalAxial.setHidden(True)
            # self.chooseScrollvalSag.setHidden(True)
            # self.chooseScrollvalCor.setHidden(True)

            self.currentFrameCor.move(1040,680)
            self.ofTextCor.move(1060,680)
            self.totalFramesCor.move(1075,680)

            self.corPlane.setPixmap(QPixmap.fromImage(self.qImgCor).scaled(680,638)) #otherwise, would just display the normal unmodified q_img

            tempCor = self.maskCoverImg[:,self.newYVal,:,:] #2D data for coronal
            tempCor = np.rot90(tempCor,1) #rotate ccw 90
            tempCor = np.flipud(tempCor) #flipud
            tempCor = np.require(tempCor,np.uint8,'C')

            self.curMaskCorIm = QImage(tempCor, self.maskCorW, self.maskCorH, self.maskBytesLineCor, QImage.Format_ARGB32)
            self.maskLayerCor.setPixmap(QPixmap.fromImage(self.curMaskCorIm).scaled(680,638))

            self.corCoverLabel.pixmap().fill(Qt.transparent)
            painter = QPainter(self.corCoverLabel.pixmap())
            painter.setPen(Qt.yellow)
            corVertLine = QLine(int(self.newXVal/self.x*680), 0, int(self.newXVal/self.x*680), 638)
            corLatLine = QLine(0, int(self.newZVal/self.z*638), 680, int(self.newZVal/self.z*638))
            painter.drawLines([corVertLine, corLatLine])
            painter.end()      


# SIXTH STEP: when close expanded image, return to normal layout and functions
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    def closeExpandedImg(self):
        if self.id != 0 and self.imagesOpened:
            if self.id == 1:
                self.axCoverLabel.move(470, 30)
                self.axCoverLabel.resize(331, 311)
                self.axCoverPixmap = QPixmap(331, 311)
                self.axCoverPixmap.fill(Qt.transparent)
                self.axCoverLabel.setPixmap(self.axCoverPixmap)
                self.xCur = int(self.newXVal*331/(self.widthAx-1)) + 479
                self.yCur = int(self.newYVal*311/(self.heightAx-1)) + 30
                self.maskLayerSag.setHidden(False)
                self.maskLayerCor.setHidden(False)
                self.maskLayerAx.move(470, 30)
                self.maskLayerAx.resize(331, 311)
                tempAx = self.maskCoverImg[:,:,self.newZVal,:] #2D data for axial
                tempAx = np.flipud(tempAx) #flipud
                tempAx = np.rot90(tempAx,3) #rotate ccw 270  
                tempAx = np.require(tempAx,np.uint8, 'C')
                self.curMaskAxIm = QImage(tempAx, self.maskAxW, self.maskAxH, self.maskBytesLineAx, QImage.Format_ARGB32) #creating QImage
                self.maskLayerAx.setPixmap(QPixmap.fromImage(self.curMaskAxIm).scaled(331,311)) #displaying QPixmap in the QLabels
            elif self.id == 2:
                self.sagCoverLabel.move(820, 30)
                self.sagCoverLabel.resize(331, 311)
                self.sagCoverPixmap = QPixmap(331, 311)
                self.sagCoverPixmap.fill(Qt.transparent)
                self.sagCoverLabel.setPixmap(self.sagCoverPixmap)
                self.xCur = int(self.newZVal*331/(self.widthSag-1)) + 820
                self.yCur = int(self.newYVal*311/(self.heightSag-1)) + 30
                self.maskLayerAx.setHidden(False)
                self.maskLayerCor.setHidden(False)
                self.maskLayerSag.move(820, 30)
                self.maskLayerSag.resize(331, 311)
                tempSag = self.maskCoverImg[self.newXVal,:,:,:] #2D data for sagittal
                tempSag = np.flipud(tempSag) #flipud
                tempSag = np.rot90(tempSag,2) #rotate ccw 180
                tempSag = np.fliplr(tempSag)
                tempSag = np.require(tempSag,np.uint8,'C')
                self.curMaskSagIm = QImage(tempSag, self.widthSag, self.heightSag, self.maskBytesLineSag, QImage.Format_ARGB32)
                self.maskLayerSag.setPixmap(QPixmap.fromImage(self.curMaskSagIm).scaled(331, 311))
            elif self.id == 3:
                self.corCoverLabel.move(820, 390)
                self.corCoverLabel.resize(331, 311)
                self.corCoverPixmap = QPixmap(331, 311)
                self.corCoverPixmap.fill(Qt.transparent)
                self.corCoverLabel.setPixmap(self.corCoverPixmap)
                self.maskLayerAx.setHidden(False)
                self.maskLayerSag.setHidden(False)
                self.maskLayerCor.move(820, 390)
                self.maskLayerCor.resize(331, 311)
                tempCor = self.maskCoverImg[:,self.newYVal,:,:] #2D data for coronal
                tempCor = np.rot90(tempCor,1) #rotate ccw 90
                tempCor = np.flipud(tempCor) #flipud
                tempCor = np.require(tempCor,np.uint8,'C')
                self.curMaskCorIm = QImage(tempCor, self.maskCorW, self.maskCorH, self.maskBytesLineCor, QImage.Format_ARGB32)
                self.maskLayerCor.setPixmap(QPixmap.fromImage(self.curMaskCorIm).scaled(331,311))
            self.id = 0

            self.axCoverLabel.pixmap().fill(Qt.transparent)
            painter = QPainter(self.axCoverLabel.pixmap())
            painter.setPen(Qt.yellow)
            axVertLine = QLine(int(self.newXVal/self.x*331), 0, int(self.newXVal/self.x*331), 311)
            axLatLine = QLine(0, int(self.newYVal/self.y*311), 331, int(self.newYVal/self.y*311))
            painter.drawLines([axVertLine, axLatLine])
            painter.end()
            self.sagCoverLabel.pixmap().fill(Qt.transparent)
            painter = QPainter(self.sagCoverLabel.pixmap())
            painter.setPen(Qt.yellow)
            sagVertLine = QLine(int(self.newZVal/self.z*331), 0, int(self.newZVal/self.z*331), 311)
            sagLatLine = QLine(0, int(self.newYVal/self.y*311), 331, int(self.newYVal/self.y*311))
            painter.drawLines([sagVertLine, sagLatLine])
            painter.end()
            self.corCoverLabel.pixmap().fill(Qt.transparent)
            painter = QPainter(self.corCoverLabel.pixmap())
            painter.setPen(Qt.yellow)
            corVertLine = QLine(int(self.newXVal/self.x*331), 0, int(self.newXVal/self.x*331), 311)
            corLatLine = QLine(0, int(self.newZVal/self.z*311), 331, int(self.newZVal/self.z*311))
            painter.drawLines([corVertLine, corLatLine])
            painter.end()
            self.update()

            if self.aucParamapButton.isChecked() or self.peParamapButton.isChecked() or self.tpParamapButton.isChecked() or self.mttParamapButton.isChecked():
                self.legend.setHidden(False)
            self.compressLabel.setHidden(False)
            self.compressValue.setHidden(False)
            self.windowHeightLabel.setHidden(False)
            self.windowDepthLabel.setHidden(False)
            self.windowWidthLabel.setHidden(False)
            self.windowHeightValue.setHidden(False)
            self.windowDepthValue.setHidden(False)
            self.windowWidthValue.setHidden(False)
            if self.ticComputed:
                self.legend.setHidden(False)
            self.axCoverLabel.setHidden(False)
            self.sagCoverLabel.setHidden(False)
            self.corCoverLabel.setHidden(False)
            self.axialPlane.move(470,30)
            self.axialPlane.resize(331,311)
            self.sagPlane.move(820,30)
            self.sagPlane.resize(331,311)
            self.corPlane.move(820,390)
            self.corPlane.resize(331,311)
            self.alphaTracker.setHidden(False)
            self.curAlpha.setHidden(False)
            self.curSlices.setHidden(False)
            self.totalSlices.setHidden(False)
            self.slicesChanger.setHidden(False)
            self.slicesLabel.setHidden(False)
            self.alphaLabel.setHidden(False)
            self.slicesOf.setHidden(False)

            self.axialScroll.move(800,30)
            self.axialScroll.resize(16,311)
            self.sagScroll.move(1150,30)
            self.sagScroll.resize(16,311)
            self.corScroll.move(990,390)
            self.corScroll.resize(20,311)

            self.ofTextAx.move(790,340)
            self.ofTextSag.move(1120,340)
            self.ofTextCor.move(1120,700)

            self.totalFramesAx.move(805,340)
            self.totalFramesAx.resize(31,16)

            self.totalFramesSag.move(1135,340)
            self.totalFramesSag.resize(31,16)

            self.totalFramesCor.move(1135,700)
            self.totalFramesCor.resize(31,16)

            self.currentFrameAx.move(770,340)
            self.currentFrameAx.resize(31,16)

            self.currentFrameSag.move(1100,340)
            self.currentFrameSag.resize(31,16)

            self.currentFrameCor.move(1090,700)
            self.currentFrameCor.resize(31,16)

            self.axialScroll.setMaximum(self.z) #from function of initial images
            self.sagScroll.setMaximum(self.x)
            self.corScroll.setMaximum(self.y)

            self.totalFramesAx.setText(str(self.z+1))
            self.totalFramesSag.setText(str(self.x+1))
            self.totalFramesCor.setText(str(self.y+1))

            self.axialPlane.setHidden(False)
            self.sagPlane.setHidden(False)
            self.corPlane.setHidden(False)

            self.axialTextLabel.setHidden(False)
            self.sagTextLabel.setHidden(False)
            self.corTextLabel.setHidden(False)

            self.ofTextAx.setHidden(False)
            self.ofTextSag.setHidden(False)
            self.ofTextCor.setHidden(False)
            self.currentFrameAx.setHidden(False)
            self.currentFrameSag.setHidden(False)
            self.currentFrameCor.setHidden(False)
            self.totalFramesAx.setHidden(False)
            self.totalFramesSag.setHidden(False)
            self.totalFramesCor.setHidden(False)

            # self.save_seg_Axial.setHidden(False)
            # self.save_seg_Sag.setHidden(False)
            # self.save_seg_Cor.setHidden(False)

            self.axialPlane.setPixmap(QPixmap.fromImage(self.qImgAx).scaled(331,311)) #otherwise, would just display the normal unmodified q_img
            self.sagPlane.setPixmap(QPixmap.fromImage(self.qImgSag).scaled(331,311)) #otherwise, would just display the normal unmodified q_img
            self.corPlane.setPixmap(QPixmap.fromImage(self.qImgCor).scaled(331,311)) #otherwise, would just display the normal unmodified q_img

        self.axialScroll.valueChanged.connect(self.changeAxialSlices)
        self.sagScroll.valueChanged.connect(self.changeSagSlices)
        self.corScroll.valueChanged.connect(self.changeCorSlices)



# SEVENTH STEP: user can select a single or multiple rectangular regions of interest by dragging and releasing mouse over specific label, can draw when
# the images are expanded as well; this paints directly on the QImage of the slices and displays the drawing on a scaled QPixmap -- fully functional now
#---------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------
    def paintEvent(self,event):
        scrolling = "none"
        if self.id ==0 and self.imagesOpened and self.scrolling:
            if self.xCur < 811 and self.xCur > 478 and self.yCur < 342 and self.yCur > 29 and (self.painted == "none" or self.painted == "ax"):
                self.actualX = int((self.xCur - 479)*(self.widthAx-1)/331)
                self.actualY = int((self.yCur - 30)*(self.heightAx-1)/311)
                scrolling = "ax"
                self.axCoverLabel.pixmap().fill(Qt.transparent)
                painter = QPainter(self.axCoverLabel.pixmap())
                painter.setPen(Qt.yellow)
                axVertLine = QLine(self.xCur - 479, 0, self.xCur - 479, 311)
                axLatLine = QLine(0, self.yCur - 30, 331, self.yCur - 30)
                painter.drawLines([axVertLine, axLatLine])
                painter.end()
            elif self.xCur < 1152 and self.xCur > 819 and self.yCur < 342 and self.yCur > 29 and (self.painted == "none" or self.painted == "sag"):
                self.actualX = int((self.xCur-820)*(self.widthSag-1)/331)
                self.actualY = int((self.yCur-30)*(self.heightSag-1)/311)
                scrolling = "sag"
                self.sagCoverLabel.pixmap().fill(Qt.transparent)
                painter = QPainter(self.sagCoverLabel.pixmap())
                painter.setPen(Qt.yellow)
                sagVertLine = QLine(self.xCur - 820, 0, self.xCur - 820, 311)
                sagLatLine = QLine(0, self.yCur - 30, 331, self.yCur - 30)
                painter.drawLines([sagVertLine, sagLatLine])
                painter.end()
            elif self.xCur < 1152 and self.xCur > 819 and self.yCur < 702 and self.yCur > 389 and (self.painted == "none" or self.painted == "cor"):
                self.actualX = int((self.xCur-820)*(self.widthCor-1)/331)
                self.actualY = int((self.yCur-390)*(self.heightCor-1)/311)
                scrolling = "cor"
                self.corCoverLabel.pixmap().fill(Qt.transparent)
                painter = QPainter(self.corCoverLabel.pixmap())
                painter.setPen(Qt.yellow)
                corVertLine = QLine(self.xCur - 820, 0, self.xCur - 820, 311)
                corLatLine = QLine(0, self.yCur - 390, 331, self.yCur-390)
                painter.drawLines([corVertLine, corLatLine])
                painter.end()

        elif self.id != 0 and self.imagesOpened and self.scrolling:
            if self.xCur < 1151 and self.xCur > 469 and self.yCur < 669 and self.yCur > 29:
                if self.id == 1:
                    self.actualX = int((self.widthAx-1)*(self.xCur-470)/680)
                    self.actualY = int((self.heightAx-1)*(self.yCur-30)/638)
                    scrolling = "ax"
                    self.axCoverLabel.pixmap().fill(Qt.transparent)
                    painter = QPainter(self.axCoverLabel.pixmap())
                    painter.setPen(Qt.yellow)
                    axVertLine = QLine(self.xCur - 470, 0, self.xCur - 470, 638)
                    axLatLine = QLine(0, self.yCur - 30, 680, self.yCur - 30)
                    painter.drawLines([axVertLine, axLatLine])
                    painter.end()
                elif self.id == 2:
                    self.actualX = int((self.widthSag-1)*(self.xCur-470)/680)
                    self.actualY = int((self.heightSag-1)*(self.yCur-30)/638)
                    scrolling = "sag"
                    self.sagCoverLabel.pixmap().fill(Qt.transparent)
                    painter = QPainter(self.sagCoverLabel.pixmap())
                    painter.setPen(Qt.yellow)
                    axVertLine = QLine(self.xCur - 470, 0, self.xCur - 470, 638)
                    axLatLine = QLine(0, self.yCur - 30, 680, self.yCur - 30)
                    painter.drawLines([axVertLine, axLatLine])
                    painter.end()
                elif self.id == 3:
                    self.actualX = int((self.widthCor-1)*(self.xCur-470)/680)
                    self.actualY = int((self.heightCor-1)*(self.yCur-30)/638)
                    scrolling = "cor"
                    self.corCoverLabel.pixmap().fill(Qt.transparent)
                    painter = QPainter(self.corCoverLabel.pixmap())
                    painter.setPen(Qt.yellow)
                    axVertLine = QLine(self.xCur - 470, 0, self.xCur - 470, 638)
                    axLatLine = QLine(0, self.yCur - 30, 680, self.yCur - 30)
                    painter.drawLines([axVertLine, axLatLine])
                    painter.end()

        if scrolling == "ax":
            self.newXVal = self.actualX
            self.newYVal = self.actualY
            self.changeSagSlices()
            self.changeCorSlices()
            self.sagCoverLabel.pixmap().fill(Qt.transparent)
            painter = QPainter(self.sagCoverLabel.pixmap())
            painter.setPen(Qt.yellow)
            sagVertLine = QLine(int(self.newZVal/self.z*331), 0, int(self.newZVal/self.z*331), 311)
            sagLatLine = QLine(0, int(self.newYVal/self.y*311), 331, int(self.newYVal/self.y*311))
            painter.drawLines([sagVertLine, sagLatLine])
            painter.end()
            
            self.corCoverLabel.pixmap().fill(Qt.transparent)
            painter = QPainter(self.corCoverLabel.pixmap())
            painter.setPen(Qt.yellow)
            corVertLine = QLine(int(self.newXVal/self.x*331), 0, int(self.newXVal/self.x*331), 311)
            corLatLine = QLine(0, int(self.newZVal/self.z*311), 331, int(self.newZVal/self.z*311))
            painter.drawLines([corVertLine, corLatLine])
            painter.end()
            self.update()

        elif scrolling == "sag":
            self.newZVal = self.actualX
            self.newYVal = self.actualY
            self.changeAxialSlices()
            self.changeCorSlices()
            self.axCoverLabel.pixmap().fill(Qt.transparent)
            painter = QPainter(self.axCoverLabel.pixmap())
            painter.setPen(Qt.yellow)
            axVertLine = QLine(int(self.newXVal/self.x*331), 0, int(self.newXVal/self.x*331), 311)
            axLatLine = QLine(0, int(self.newYVal/self.y*311), 331, int(self.newYVal/self.y*311))
            painter.drawLines([axVertLine, axLatLine])
            painter.end()
            
            self.corCoverLabel.pixmap().fill(Qt.transparent)
            painter = QPainter(self.corCoverLabel.pixmap())
            painter.setPen(Qt.yellow)
            corVertLine = QLine(int(self.newXVal/self.x*331), 0, int(self.newXVal/self.x*331), 311)
            corLatLine = QLine(0, int(self.newZVal/self.z*311), 331, int(self.newZVal/self.z*311))
            painter.drawLines([corVertLine, corLatLine])
            painter.end()
            self.update()

        elif scrolling == "cor":
            self.newXVal = self.actualX
            self.newZVal = self.actualY
            self.changeAxialSlices()
            self.changeSagSlices()
            self.axCoverLabel.pixmap().fill(Qt.transparent)
            painter = QPainter(self.axCoverLabel.pixmap())
            painter.setPen(Qt.yellow)
            axVertLine = QLine(int(self.newXVal/self.x*331), 0, int(self.newXVal/self.x*331), 311)
            axLatLine = QLine(0, int(self.newYVal/self.y*311), 331, int(self.newYVal/self.y*311))
            painter.drawLines([axVertLine, axLatLine])
            painter.end()

            self.sagCoverLabel.pixmap().fill(Qt.transparent)
            painter = QPainter(self.sagCoverLabel.pixmap())
            painter.setPen(Qt.yellow)
            sagVertLine = QLine(int(self.newZVal/self.z*331), 0, int(self.newZVal/self.z*331), 311)
            sagLatLine = QLine(0, int(self.newYVal/self.y*311), 331, int(self.newYVal/self.y*311))
            painter.drawLines([sagVertLine, sagLatLine])
            painter.end()
            self.update()


#----------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------
# defines mouse events here so that paint function works
    def mousePressEvent(self,event):
        self.xCur = event.x()
        self.yCur = event.y()
        self.newPointPlotted = False
        if self.drawPolygonButton.isChecked() and self.scrolling:
            # Plot ROI points
            if self.id == 0:
                if (self.xCur < 811 and self.xCur > 478 and self.yCur < 342 and self.yCur > 29) and (self.painted == "none" or self.painted == "ax"):
                    self.actualX = int((self.xCur - 479)*(self.widthAx-1)/331)
                    self.actualY = int((self.yCur - 30)*(self.heightAx-1)/311)
                    self.maskCoverImg[self.actualX, self.actualY, self.newZVal] = [0, 0, 255,int(self.curAlpha.value())]
                    self.curPointsPlottedX.append(self.actualX)
                    self.curPointsPlottedY.append(self.actualY)
                    self.newPointPlotted = True
                    self.painted = "ax"
                    self.sagCoverLabel.setCursor(Qt.ArrowCursor)
                    self.corCoverLabel.setCursor(Qt.ArrowCursor)
                    self.curROIDrawn = False
                elif (event.x() < 1152 and event.x() > 819 and event.y() < 342 and event.y() > 29) and (self.painted == "none" or self.painted == "sag"):
                    self.actualX = int((self.xCur-820)*(self.widthSag-1)/331)
                    self.actualY = int((self.yCur-30)*(self.heightSag-1)/311)
                    self.maskCoverImg[self.newXVal, self.actualY, self.actualX] = [0,0,255,int(self.curAlpha.value())]
                    self.curPointsPlottedX.append(self.actualX)
                    self.curPointsPlottedY.append(self.actualY)
                    self.newPointPlotted = True
                    self.painted = "sag"
                    self.axCoverLabel.setCursor(Qt.ArrowCursor)
                    self.corCoverLabel.setCursor(Qt.ArrowCursor)
                    self.curROIDrawn = False
                elif (event.x() < 1152 and event.x() > 819 and event.y() < 702 and event.y() > 389) and (self.painted == "none" or self.painted == "cor"):
                    self.actualX = int((self.xCur-820)*(self.widthCor-1)/331)
                    self.actualY = int((self.yCur-390)*(self.heightCor-1)/311)
                    self.maskCoverImg[self.actualX, self.newYVal, self.actualY] = [0,0,255,int(self.curAlpha.value())]
                    self.curPointsPlottedX.append(self.actualX)
                    self.curPointsPlottedY.append(self.actualY)
                    self.newPointPlotted = True
                    self.painted = "cor"
                    self.axCoverLabel.setCursor(Qt.ArrowCursor)
                    self.sagCoverLabel.setCursor(Qt.ArrowCursor)
                    self.curROIDrawn = False
            elif self.id != 0 and self.xCur < 1151 and self.xCur > 469 and self.yCur < 669 and self.yCur > 29:
                if self.id == 1 and self.axialPlane.isHidden() is False and self.sagPlane.isHidden()  and self.corPlane.isHidden() :
                    self.actualX = int((self.widthAx-1)*(self.xCur-470)/680)
                    self.actualY = int((self.heightAx-1)*(self.yCur-30)/638)
                    self.maskCoverImg[self.actualX, self.actualY, self.newZVal] = [0,0,255,int(self.curAlpha.value())]
                    self.curPointsPlottedX.append(self.actualX)
                    self.curPointsPlottedY.append(self.actualY)
                    self.newPointPlotted = True
                    self.painted = "ax"
                elif self.id == 2 and self.sagPlane.isHidden() is False and self.corPlane.isHidden()  and self.axialPlane.isHidden() :
                    self.actualX = int((self.widthSag-1)*(self.xCur-470)/680)
                    self.actualY = int((self.heightSag-1)*(self.yCur-30)/638)
                    self.maskCoverImg[self.newXVal, self.actualY, self.actualX] = [0,0,255,int(self.curAlpha.value())]
                    self.curPointsPlottedX.append(self.actualX)
                    self.curPointsPlottedY.append(self.actualY)
                    self.newPointPlotted = True
                    self.painted = "sag"
                elif self.id == 3 and self.corPlane.isHidden() is False and self.axialPlane.isHidden()  and self.sagPlane.isHidden() :
                    self.actualX = int((self.widthCor-1)*(self.xCur-470)/680)
                    self.actualY = int((self.heightCor-1)*(self.yCur-30)/638)
                    self.maskCoverImg[self.actualX, self.newYVal, self.actualY] = [0,0,255,int(self.curAlpha.value())]
                    self.curPointsPlottedX.append(self.actualX)
                    self.curPointsPlottedY.append(self.actualY)
                    self.newPointPlotted = True
                    self.painted = "cor"
            self.changeSagSlices()
            self.changeCorSlices()
            self.changeAxialSlices()


    def mouseDoubleClickEvent(self, event):
        if self.scrolling:
            # Stop cross-hair pointer updates
            self.scrolling = False
            self.axCoverLabel.setCursor(Qt.ArrowCursor)
            self.sagCoverLabel.setCursor(Qt.ArrowCursor)
            self.corCoverLabel.setCursor(Qt.ArrowCursor)
        else:
            # Re-start cross-hair pointer updates
            self.scrolling = True
            if self.painted == "ax":
                self.axCoverLabel.setCursor(Qt.BlankCursor)
            elif self.painted == "sag":
                self.sagCoverLabel.setCursor(Qt.BlankCursor)
            elif self.painted == "cor":
                self.corCoverLabel.setCursor(Qt.BlankCursor)
            else:
                self.axCoverLabel.setCursor(Qt.BlankCursor)
                self.sagCoverLabel.setCursor(Qt.BlankCursor)
                self.corCoverLabel.setCursor(Qt.BlankCursor)
            self.paintEvent(event)
        if self.drawPolygonButton.isChecked():
            # Disregard previously plotted point
            if self.id == 0:
                if self.xCur < 811 and self.xCur > 478 and self.yCur < 342 and self.yCur > 29 and (self.painted == "none" or self.painted == "ax"):
                    self.actualX = int((self.xCur - 479)*(self.widthAx-1)/331)
                    self.actualY = int((self.yCur - 30)*(self.heightAx-1)/311)
                elif self.xCur < 1152 and self.xCur > 819 and self.yCur < 342 and self.yCur > 29 and (self.painted == "none" or self.painted == "sag"):
                    self.actualX = int((self.xCur-820)*(self.widthSag-1)/331)
                    self.actualY = int((self.yCur-30)*(self.heightSag-1)/311)
                elif self.xCur < 1152 and self.xCur > 819 and self.yCur < 702 and self.yCur > 389 and (self.painted == "none" or self.painted == "cor"):
                    self.actualX = int((self.xCur-820)*(self.widthCor-1)/331)
                    self.actualY = int((self.yCur-390)*(self.heightCor-1)/311)
            elif self.id != 0 and self.xCur < 1151 and self.xCur > 469 and self.yCur < 669 and self.yCur > 29:
                if self.id == 1 and self.axialPlane.isHidden() is False and self.sagPlane.isHidden()  and self.corPlane.isHidden() :
                    self.actualX = int((self.widthAx-1)*(self.xCur-470)/680)
                    self.actualY = int((self.heightAx-1)*(self.yCur-30)/638)
                elif self.id == 2 and self.sagPlane.isHidden() is False and self.corPlane.isHidden()  and self.axialPlane.isHidden() :
                    self.actualX = int((self.widthSag-1)*(self.xCur-470)/680)
                    self.actualY = int((self.heightSag-1)*(self.yCur-30)/638)
                elif self.id == 3 and self.corPlane.isHidden() is False and self.axialPlane.isHidden()  and self.sagPlane.isHidden() :
                    self.actualX = int((self.widthCor-1)*(self.xCur-470)/680)
                    self.actualY = int((self.heightCor-1)*(self.yCur-30)/638)
            self.changeAxialSlices()
            self.changeSagSlices()
            self.changeCorSlices()
            if self.newPointPlotted:
                self.undoLastPoint()
            self.newPointPlotted = False
        if len(self.curPointsPlottedX) == 0:
            self.painted = "none"


    def mouseMoveEvent(self, event):
        self.xCur = event.x()
        self.yCur = event.y()


# EIGHTH STEP: when accept polygon is clicked, the draw polygon button
# returns to normal - is unchecked
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------
    def acceptPolygon(self):
        # 2d interpolation
        if len(self.curPointsPlottedX) and self.imagesOpened and self.voiComputed == False:
            self.drawPolygonButton.setChecked(False)
            self.feedbackScrollBar.setHidden(True)
            self.feedbackText.setText("rectangular shape accepted")
            self.curPointsPlottedX.append(self.curPointsPlottedX[0])
            self.curPointsPlottedY.append(self.curPointsPlottedY[0])
            self.maskCoverImg.fill(0)
            x, y = calculateSpline(self.curPointsPlottedX, self.curPointsPlottedY)
            newROI = []
            for i in range(len(x)):
                if self.painted == "ax":
                    if len(newROI) == 0 or newROI[-1] != (int(x[i]), int(y[i]), self.newZVal):
                        newROI.append([int(x[i]), int(y[i]), self.newZVal])
                elif self.painted == "sag":
                    if len(newROI) == 0 or newROI[-1] != (self.newXVal, int(y[i]), int (x[i])):
                        newROI.append([self.newXVal, int(y[i]), int(x[i])])
                elif self.painted == "cor":
                    if len(newROI) == 0 or newROI[-1] != (int(x[i]), self.newYVal, int(y[i])):
                        newROI.append([int(x[i]), self.newYVal, int(y[i])])
            self.pointsPlotted.append(newROI)
            for i in range(len(self.pointsPlotted)):
                for j in range(len(self.pointsPlotted[i])):
                    self.maskCoverImg[self.pointsPlotted[i][j][0], self.pointsPlotted[i][j][1], self.pointsPlotted[i][j][2]] = [0,0,255,int(self.curAlpha.value())]
            self.changeAxialSlices()
            self.changeSagSlices()
            self.changeCorSlices()
            self.curPointsPlottedX = []
            self.curPointsPlottedY = []
            self.planesDrawn.append(self.painted)
            self.painted = "none"
            self.curROIDrawn = True
            self.undoLastROIButton.setHidden(False)
            self.acceptPolygonButton.setHidden(True)


# NINTH STEP: able to undo the painting done on temp files (Sag and Cor)
# but cannot undo on the axial, only way would be to clear the path and
# retry drawing
#-------------------------------------------------------------------------
#-------------------------------------------------------------------------

    def undoLastPoint(self):
        if len(self.curPointsPlottedX) != 0:
            self.maskCoverImg[self.curPointsPlottedX[-1]]
            self.curPointsPlottedX.pop()
            self.curPointsPlottedY.pop()
            self.maskCoverImg.fill(0)
            for i in range(len(self.pointsPlotted)):
                for j in range(len(self.pointsPlotted[i])):
                    self.maskCoverImg[self.pointsPlotted[i][j][0], self.pointsPlotted[i][j][1], self.pointsPlotted[i][j][2]] = [0,0,255, int(self.curAlpha.value())]
            for i in range(len(self.curPointsPlottedX)):
                if self.painted == "ax":
                    self.maskCoverImg[int(self.curPointsPlottedX[i]), int(self.curPointsPlottedY[i]), self.newZVal] = [0,0,255,int(self.curAlpha.value())]
                elif self.painted == "sag":
                    self.maskCoverImg[self.newXVal, int(self.curPointsPlottedY[i]), int(self.curPointsPlottedX[i])] = [0,0,255,int(self.curAlpha.value())]
                elif self.painted == "cor":
                    self.maskCoverImg[int(self.curPointsPlottedX[i]), self.newYVal, int(self.curPointsPlottedY[i])] = [0,0,255,int(self.curAlpha.value())]
            self.changeAxialSlices()
            self.changeSagSlices()
            self.changeCorSlices()
        if len(self.curPointsPlottedX) == 0:
            self.painted == "none"


    def startROIDraw(self):
        if self.acceptPolygonButton.isHidden() and self.drawPolygonButton.isCheckable():
            self.acceptPolygonButton.setHidden(False)
            self.undoLastROIButton.setHidden(True)
        elif len(self.curPointsPlottedX) == 0 and len(self.pointsPlotted) != 0:
            self.acceptPolygonButton.setHidden(True)
            self.undoLastROIButton.setHidden(False)

    def undoLastRectangle(self):
        if self.imagesOpened and self.voiComputed == False:

            if len(self.pointsPlotted) == 0:
                self.feedbackText.setText("Unable to remove rectangle")
            else:
                self.pointsPlotted.pop()
                self.planesDrawn.pop()
                self.maskCoverImg.fill(0)
                for i in range(len(self.pointsPlotted)):
                    for j in range(len(self.pointsPlotted[i])):
                        self.maskCoverImg[self.pointsPlotted[i][j][0], self.pointsPlotted[i][j][1], self.pointsPlotted[i][j][2]] = [0,0,255,int(self.curAlpha.value())]
                self.changeAxialSlices()
                self.changeSagSlices()
                self.changeCorSlices()
            self.update() #David

# TENTH STEP: able to mask images, so will only keep the white rectangle drawn on the image
#-----------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------
    #these 3 masking functions below are used for creating transparent background -- are not used
    def createMaskedImgAxial(self):
        if self.axialScroll.value() == 0:
            self.pmAx = QPixmap.fromImage(self.qImgAx).scaled(331,311)
            self.maskAx = QBitmap(self.pmAx.createMaskFromColor(QColor(Qt.white), Qt.MaskOutColor))
            self.pmAx.setMask(self.maskAx)
            self.axialPlane.setPixmap(self.pmAx)

            self.outputMaskNameAx = str("maskAx_0")
            self.pmAx.save(os.path.join("niftiMasks", str(self.outputMaskNameAx + ".png")))

        elif self.axialScroll.value() != 0:
            self.pmAxSlices = QPixmap.fromImage(self.qImgAx_slices).scaled(331,311)
            self.maskAxSlices = QBitmap(self.pmAxSlices.createMaskFromColor(QColor(Qt.white), Qt.MaskOutColor))
            self.pmAxSlices.setMask(self.maskAxSlices)
            self.axialPlane.setPixmap(self.pmAxSlices)

            self.outputMaskNameAx = str("maskAx_" + str(self.axialScroll.value()))
            self.pmAxSlices.save(os.path.join("niftiMasks", str(self.outputMaskNameAx + ".png")))

    def createMaskedImgSag(self):
        if self.sagScroll.value() == 0:
            self.pmSag = QPixmap.fromImage(self.qImgSag).scaled(331,311)
            self.maskSag = QBitmap(self.pmSag.createMaskFromColor(QColor(Qt.white), Qt.MaskOutColor))
            self.pmSag.setMask(self.maskSag)
            self.sagPlane.setPixmap(self.pmSag)

            self.outputMaskNameSag = str("maskSag_0")
            self.pmSag.save(os.path.join("niftiMasks", str(self.outputMaskNameSag + ".png")))

        elif self.sagScroll.value() != 0:
            self.pmSagSlices = QPixmap.fromImage(self.qImgSag_slices).scaled(331,311)
            self.maskSagSlices = QBitmap(self.pmSagSlices.createMaskFromColor(QColor(Qt.white), Qt.MaskOutColor))
            self.pmSagSlices.setMask(self.maskSagSlices)
            self.sagPlane.setPixmap(self.pmSagSlices)

            self.outputMaskNameSag = str("maskSag_" + str(self.sagScroll.value()))
            self.pmSagSlices.save(os.path.join("niftiMasks", str(self.outputMaskNameSag + ".png")))

    def createMaskedImgCor(self):
        if self.corScroll.value() == 0:
            self.pmCor = QPixmap.fromImage(self.qImgCor).scaled(331,311)
            self.maskCor = QBitmap(self.pmCor.createMaskFromColor(QColor(Qt.white), Qt.MaskOutColor))
            self.pmCor.setMask(self.maskCor)
            self.corPlane.setPixmap(self.pmCor)

            self.outputMaskNameCor = str("maskCor_0")
            self.pmCor.save(os.path.join("niftiMasks", str(self.outputMaskNameCor + ".png")))

        elif self.sagScroll.value() != 0:
            self.pmCorSlices = QPixmap.fromImage(self.qImgCor_slices).scaled(331,311)
            self.maskCorSlices = QBitmap(self.pmCorSlices.createMaskFromColor(QColor(Qt.white), Qt.MaskOutColor))
            self.pmCorSlices.setMask(self.maskCorSlices)
            self.corPlane.setPixmap(self.pmCorSlices)

            self.outputMaskNameCor = str("maskCor_" + str(self.corScroll.value()))
            self.pmCorSlices.save(os.path.join("niftiMasks", str(self.outputMaskNameCor + ".png")))

#----------------------------------------------------------------------------------------------------------------------
    #these 3 masking functions below create black background, relies on itk function -- are used!


    def voi3dInterpolation(self):
        if self.imagesOpened and self.voiComputed == False:
            if len(self.pointsPlotted) >= 2:
                if len(self.pointsPlotted) == 2 and self.planesDrawn[0]==self.planesDrawn[1]:
                    self.feedbackText.setText("Must have at least 3 ROIs if all plotted in same plane")
                else:
                    points = calculateSpline3D(list(chain.from_iterable(self.pointsPlotted)))
                    # ar = np.array(list(chain.from_iterable(self.pointsPlotted)))
                    # points = create_enclosing_surface_of_best_fit(ar[:,0], ar[:,1], ar[:,2])
                    self.pointsPlotted = []
                    self.maskCoverImg.fill(0)
                    tempPoints = []
                    for point in points:
                        if max(self.data4dImg[point]) != 0:
                            self.maskCoverImg[point] = [0,0,255,int(self.curAlpha.value())]
                            self.pointsPlotted.append(point)
                        tempPoints.append(point)
                    if len(self.pointsPlotted) == 0:
                        self.feedbackText.setText("VOI not in US image.\nDraw new VOI over US image")
                        self.maskCoverImg.fill(0)
                        self.changeAxialSlices()
                        self.changeSagSlices()
                        self.changeCorSlices()
                        return
                    tempPoints.sort(key=lambda x: (x[1], x[2], x[0]))
                    curY = tempPoints[0][1]
                    curZ = tempPoints[0][2]
                    curX = tempPoints[0][0]
                    filledInPoints = []
                    for i in range(len(tempPoints)):
                        if tempPoints[i][1] == curY and tempPoints[i][2] == curZ and (tempPoints[i][0] - curX) > 1:
                            for j in range(1, tempPoints[i][0] - curX, 1):
                                if max(self.data4dImg[curX+j, curY, curZ]) != 0:
                                    self.maskCoverImg[curX+j, curY, curZ] = [0,0,255,int(self.curAlpha.value())]
                                    filledInPoints.append([curX+j, curY, curZ])
                        if tempPoints[i][1] != curY:
                            curY = tempPoints[i][1]
                        if tempPoints[i][2] != curZ:
                            curZ = tempPoints[i][2]
                        if tempPoints[i][0] != curX:
                            curX = tempPoints[i][0]
                    for i in range(len(filledInPoints)):
                        self.pointsPlotted.append(filledInPoints[i])
                    self.changeAxialSlices()
                    self.changeSagSlices()
                    self.changeCorSlices()
                    self.voiComputed = True
                    self.drawPolygonButton.setCheckable(False)
            else:
                self.feedbackText.setText("Must have either 2 ROIs in different planes or 3 ROIs in the same plane")

        # PixelType = itk.ctype("unsigned char")
        # Dimension = 2
        # ImageType = itk.Image[PixelType, Dimension]

        # #---- creating empty array for compiling .png to .nii
        # try:
        #     print(self.emptyArrayMaskAxial.shape)
        # except AttributeError:
        #     self.emptyArrayMaskAxial = np.zeros([self.widthAx,self.heightAx,self.z+1])
        # #print("array of empty axial mask is: " + str(self.emptyArrayMaskAxial.shape)) # 164, 160, 82

        # reader = itk.ImageFileReader[ImageType].New()
        # self.output_ax_name = str("drawn_ax_" + str(self.axialScroll.value()))

        # if os.path.exists(os.path.join("niftiROIs", str(self.output_ax_name + ".png"))):
        #     reader.SetFileName(os.path.join("niftiROIs", str(self.output_ax_name + ".png")))
        #     thresholdFilter = itk.BinaryThresholdImageFilter[ImageType, ImageType].New()
        #     thresholdFilter.SetInput(0,reader.GetOutput())
        #     thresholdFilter.SetLowerThreshold(255)
        #     thresholdFilter.SetUpperThreshold(255)
        #     thresholdFilter.SetOutsideValue(0)
        #     thresholdFilter.SetInsideValue(255)

        #     writer = itk.ImageFileWriter[ImageType].New()
        #     writer.SetFileName(os.path.join("niftiBinaryMasks", str(self.output_ax_name + ".png")))
        #     writer.SetInput(thresholdFilter.GetOutput())
        #     writer.Update()

        #     #img_mask = mpimg.imread(os.path.join("niftiBinaryMasks", str(self.output_ax_name + ".png")))
        #     img_mask = cv2.imread(os.path.join("niftiBinaryMasks", str(self.output_ax_name + ".png")))
        #     img_mask = img_mask[:,:,0]
        #     img_mask = np.flipud(img_mask)
        #     im = Image.fromarray(img_mask)
        #     im.save(os.path.join("niftiBinaryMasks", str(self.output_ax_name + ".png")))

        #     # print("shape of image mask png is: " + str(img_mask.shape)) #164, 160
        #     # print("heightAx is: " + str(self.heightAx) + " and widthAx is: " + str(self.widthAx)) #h is 164 and w is 160

        #     for h in range(self.heightAx):
        #         for w in range(self.widthAx):
        #             self.emptyArrayMaskAxial[w][h][self.axialScroll.value()] = img_mask[h][w]
            

        #     self.data_drawn_nibImg_ax = np.array(Image.open(os.path.join("niftiBinaryMasks", self.output_ax_name_file)))
        #     self.data_drawn_nibImg_ax = self.data_drawn_nibImg_ax.astype(np.uint8)
        #     # self.data_drawn_nibImg_ax = np.flipud(self.data_drawn_nibImg_ax)
        #     self.data_drawn_nibImg_ax = np.require(self.data_drawn_nibImg_ax,np.uint8,'C')
        #     self.bytesLineAxdrawn, _ = self.data_drawn_nibImg_ax.strides
        #     temp_pic = QImage(self.data_drawn_nibImg_ax, self.widthAx, self.heightAx, self.bytesLineAxdrawn, QImage.Format_Grayscale8)
        #     self.axialPlane.setPixmap(QPixmap.fromImage(temp_pic).scaled(331,311))

        #     # print("done copying mask into array")

        # else:
        #     self.feedbackText.setText("mask only generated from modified image")

    def acceptTIC(self):
        ax = self.fig.add_subplot(111)
        firstIndex = self.ticEditor.t0[2]
        ticFrontX = self.ticX[:,0][:firstIndex]
        ticFrontY = self.ticY[:firstIndex]
        ax.plot(np.concatenate((ticFrontX, self.ticEditor.ticX[:,0])), np.concatenate((ticFrontY, self.ticEditor.ticY)))
        self.usedSlices = self.ticEditor.ticX[:,1].astype(np.int32)
        numUsedSlices = len(self.usedSlices)
        self.slicesChanger.setMaximum(numUsedSlices-1)
        self.totalSlices.setText(str(numUsedSlices))
        new_4dData = np.zeros((self.x+1, self.y+1, self.z+1, numUsedSlices))
        for i in range(numUsedSlices):
            new_4dData[:,:,:,i] = self.data4dImg[:,:,:,self.usedSlices[i]]
        self.data4dImg = new_4dData
        if system == 'Windows':
            ax.set_xlabel("Time (s)", fontsize=8, labelpad=0.5)
            ax.set_ylabel("Signal Amplitude", fontsize=8, labelpad=0.5)
            ax.set_title("Time Intensity Curve (TIC)", fontsize=10, pad=1.5)
            ax.tick_params('both', pad=0.3, labelsize=7.2)
            plt.xticks(fontsize=6)
            plt.yticks(fontsize=6)
        else:
            ax.set_xlabel("Time (s)", fontsize=4, labelpad=0.5)
            ax.set_ylabel("Signal Amplitude", fontsize=4, labelpad=0.5)
            ax.set_title("Time Intensity Curve (TIC)", fontsize=5, pad=1.5)
            ax.tick_params('both', pad=0.3, labelsize=3.6)
            plt.xticks(fontsize=3)
            plt.yticks(fontsize=3)
        # normalizer = (np.exp(np.max(self.OGData4dImg)/self.compressValue.value()))/self.voxelScale;
        # minData = (np.exp(np.min(self.OGData4dImg)/self.compressValue.value()))/self.voxelScale;
        # if minData < 0:
        #     normalizer += np.abs(minData)
        # else:
        #     normalizer -= minData
        ticNormalizer = np.max(self.ticY)
        self.ticEditor.ticY = self.ticEditor.ticY/ticNormalizer;

        # Bunch of checks
        if np.isnan(np.sum(self.ticEditor.ticY)):
            print('STOPPED:NaNs in the VOI')
            return;
        if np.isinf(np.sum(self.ticEditor.ticY)):
            print('STOPPED:InFs in the VOI')
            return;

        # Do the fitting
        # TIC = [np.array([self.ticEditor.ticX[i], self.ticEditor.ticY[i]]) for i in range(len(self.ticEditor.ticX))]
        # test = TIC[:,1]
        # hi = TIC[:,0]
        try:
            params, popt, wholecurve = lf.data_fit([self.ticEditor.ticX[:,0], self.ticEditor.ticY], ticNormalizer);
            # params, popt, RMSE, wholecurve = pm.data_fit([self.ticEditor.ticX, self.ticEditor.ticY],'BolusLognormal',normalizer, self.header[4])
            ax.plot(self.ticEditor.ticX[:,0], wholecurve)
            # params, popt, RMSE, wholecurve = pm.data_fit(TIC,'BolusLognormal',normalizer, self.header[4]);
            # ax.plot(TIC[:,0], wholecurve)
        except RuntimeError:
            print('RunTimeError')
            params = np.array([np.max(self.ticEditor.ticY)*ticNormalizer, np.trapz(self.ticEditor.ticY*ticNormalizer, x=self.ticEditor.ticX[:,0]), self.ticEditor.ticX[:,0][np.argmax(self.ticEditor.ticY),0], np.max(self.ticEditor.ticX[:,0])*2, 0]);
        actualNormalizer = (np.exp(np.max(self.OGData4dImg)/self.compressValue.value()))/self.voxelScale;
        params[0] *= actualNormalizer
        popt[0] *= actualNormalizer
        self.ticComputed = True
        self.fig.subplots_adjust(left=0.1, right=0.97, top=0.85, bottom=0.25)
        self.canvas.draw()
        self.feedbackLabel.setHidden(True)
        self.feedbackText.setHidden(True)
        self.ticAucLabel.setHidden(False)
        self.ticVarLabel.setHidden(False)
        self.ticPeLabel.setHidden(False)
        self.ticTpLabel.setHidden(False)
        self.ticMttLabel.setHidden(False)
        self.ticAucVal.setHidden(False)
        self.ticPeVal.setHidden(False)
        self.ticTpVal.setHidden(False)
        self.ticMttVal.setHidden(False)
        self.ticAucVal.setText(str(int(popt[0]*1000)/1000))
        self.ticPeVal.setText(str(int(params[0]*1000)/1000))
        self.ticTpVal.setText(str(int(params[2]*100)/100))
        self.ticMttVal.setText(str(int(params[3]*100)/100))
        self.aucParamapButton.setCheckable(True)
        self.peParamapButton.setCheckable(True)
        self.tpParamapButton.setCheckable(True)
        self.mttParamapButton.setCheckable(True)
        xlist = []
        ylist = []
        zlist = []
        for i in self.pointsPlotted:
            xlist.append(i[0])
            ylist.append(i[1])
            zlist.append(i[2])
        # self.masterParamap = pm.new_paramap(self.OGData4dImg, xlist, ylist, zlist, self.header[1:4], self.header[4], 'BolusLognormal', self.compressValue.value(), int(self.windowHeightValue.value()*self.header[1]), int(self.windowWidthValue.value()*self.header[2]), int(self.windowDepthValue.value()*self.header[3]))
        # self.maxAuc = 0
        # self.minAuc = 9999
        # self.maxPe = 0
        # self.minPe = 9999
        # self.maxTp = 0
        # self.minTp = 9999
        # self.maxMtt = 0
        # self.minMtt = 9999
        # for i in range(len(self.pointsPlotted)):
        #     if self.masterParamap[self.pointsPlotted[i][0], self.pointsPlotted[i][1],self.pointsPlotted[i][2]][0] > self.maxAuc:
        #         self.maxAuc = self.masterParamap[self.pointsPlotted[i][0],self.pointsPlotted[i][1],self.pointsPlotted[i][2]][0]
        #     if self.masterParamap[self.pointsPlotted[i][0],self.pointsPlotted[i][1],self.pointsPlotted[i][2]][0] < self.minAuc:
        #         self.minAuc = self.masterParamap[self.pointsPlotted[i][0],self.pointsPlotted[i][1],self.pointsPlotted[i][2]][0]
        #     if self.masterParamap[self.pointsPlotted[i][0],self.pointsPlotted[i][1],self.pointsPlotted[i][2]][1] > self.maxPe:
        #         self.maxPe = self.masterParamap[self.pointsPlotted[i][0],self.pointsPlotted[i][1],self.pointsPlotted[i][2]][1]
        #     if self.masterParamap[self.pointsPlotted[i][0],self.pointsPlotted[i][1],self.pointsPlotted[i][2]][1] < self.minPe:
        #         self.minPe = self.masterParamap[self.pointsPlotted[i][0],self.pointsPlotted[i][1],self.pointsPlotted[i][2]][1] 
        #     if self.masterParamap[self.pointsPlotted[i][0],self.pointsPlotted[i][1],self.pointsPlotted[i][2]][2] > self.maxTp:
        #         self.maxTp = self.masterParamap[self.pointsPlotted[i][0],self.pointsPlotted[i][1],self.pointsPlotted[i][2]][2]
        #     if self.masterParamap[self.pointsPlotted[i][0],self.pointsPlotted[i][1],self.pointsPlotted[i][2]][2] < self.minTp:
        #         self.minTp = self.masterParamap[self.pointsPlotted[i][0],self.pointsPlotted[i][1],self.pointsPlotted[i][2]][2]
        #     if self.masterParamap[self.pointsPlotted[i][0],self.pointsPlotted[i][1],self.pointsPlotted[i][2]][3] > self.maxMtt:
        #         self.maxMtt = self.masterParamap[self.pointsPlotted[i][0],self.pointsPlotted[i][1],self.pointsPlotted[i][2]][3]
        #     if self.masterParamap[self.pointsPlotted[i][0],self.pointsPlotted[i][1],self.pointsPlotted[i][2]][3] < self.minMtt:
        #         self.minMtt = self.masterParamap[self.pointsPlotted[i][0],self.pointsPlotted[i][1],self.pointsPlotted[i][2]][3]
        self.windowsComputed = True
        self.ticEditor.close()
        if self.curSlice >= numUsedSlices:
            self.slicesChanger.setValue(numUsedSlices)
            self.sliceValueChanged()

    def showTic(self):
        if not self.windowsComputed and self.imagesOpened and self.voiComputed:
            self.header = self.nibImg.header['pixdim'] # [dims, voxel dims (3 vals), timeconst, 0, 0, 0]
            times = [i*self.header[4] for i in range(1, self.OGData4dImg.shape[3]+1)]
            self.voxelScale = self.header[1]*self.header[2]*self.header[3]
            simplifiedMask = self.maskCoverImg[:,:,:,2]
            TIC = pm.generate_TIC(self.OGData4dImg, simplifiedMask, times, self.compressValue.value(),  self.voxelScale)
            # xStruct = np.array([(TIC[:,0][i],i) for i in range(len(TIC[:,0]))])

            # Bunch of checks
            if np.isnan(np.sum(TIC[:,1])):
                print('STOPPED:NaNs in the VOI')
                return;
            if np.isinf(np.sum(TIC[:,1])):
                print('STOPPED:InFs in the VOI')
                return;

            self.ticEditor = TICEditorGUI()
            self.ticEditor.show()
            self.ticEditor.accept.clicked.connect(self.acceptTIC)
            self.ticX = np.array([[TIC[i,0],i] for i in range(len(TIC[:,0]))])
            self.ticY = TIC[:,1]
            self.ticEditor.graph(self.ticX, self.ticY)

    def showAuc(self):
        if self.aucParamapButton.isChecked():
            if self.id == 0:
                self.legend.setHidden(False)
            self.peParamapButton.setChecked(False)
            self.tpParamapButton.setChecked(False)
            self.mttParamapButton.setChecked(False)
            cmapStruct = plt.get_cmap('viridis')
            cmap = cmapStruct.colors
            self.maskCoverImg.fill(0)

            for i in range(len(self.pointsPlotted)):
                color = cmap[int((255/(self.maxAuc-self.minAuc))*(self.masterParamap[self.pointsPlotted[i][0], self.pointsPlotted[i][1], self.pointsPlotted[i][2]][0]-self.minAuc))]
                color = [color[i]*255 for i in range(len(color))]
                self.maskCoverImg[self.pointsPlotted[i][0], self.pointsPlotted[i][1], self.pointsPlotted[i][2]] = [color[2], color[1], color[0], int(self.curAlpha.value())]

            self.figLeg.clear()
            a = np.array([[0,1]])
            self.figLeg = plt.figure()
            img = plt.imshow(a, cmap='viridis')
            plt.gca().set_visible(False)
            if system == 'Windows':
                cax = plt.axes([0, 0.1, 0.35, 0.8])
                cbar = plt.colorbar(orientation='vertical', cax=cax)
                plt.text(3, 0.45, "AUC", rotation=270, size=9) 
                plt.tick_params('y', labelsize=8, pad=0.5)
            else:
                cax = plt.axes([0, 0.1, 0.25, 0.8])
                cbar = plt.colorbar(orientation='vertical', cax=cax)
                plt.text(3.1, 0.45, "AUC", rotation=270, size=4.5) 
                plt.tick_params('y', labelsize=4, pad=0.5)
            cax.set_yticks([0,0.25, 0.5, 0.75, 1])
            cax.set_yticklabels([int(self.minAuc*10)/10,int((((self.maxAuc-self.minAuc)/4)+self.minAuc)*10)/10,int((((self.maxAuc - self.minAuc)/2)+self.minAuc)*10)/10,int(((3*(self.maxAuc-self.minAuc)/4)+self.minAuc)*10)/10,int(self.maxAuc*10)/10])
            self.horizLayoutLeg.removeWidget(self.canvasLeg)
            self.canvasLeg = FigureCanvas(self.figLeg)
            self.horizLayoutLeg.addWidget(self.canvasLeg)
            self.canvasLeg.draw()

            self.changeAxialSlices()
            self.changeSagSlices()
            self.changeCorSlices()

        elif self.aucParamapButton.isCheckable():
            self.maskCoverImg.fill(0)
            for i in range(len(self.pointsPlotted)):
                self.maskCoverImg[self.pointsPlotted[i][0], self.pointsPlotted[i][1], self.pointsPlotted[i][2]] = [0,0,255,int(self.curAlpha.value())]
            self.legend.setHidden(True)

            self.changeAxialSlices()
            self.changeSagSlices()
            self.changeCorSlices()

            
    def showPe(self):
        if self.peParamapButton.isChecked():
            if self.id == 0:
                self.legend.setHidden(False)
            self.aucParamapButton.setChecked(False)
            self.tpParamapButton.setChecked(False)
            self.mttParamapButton.setChecked(False)
            cmapStruct = plt.get_cmap('magma')
            cmap = cmapStruct.colors
            self.maskCoverImg.fill(0)

            for i in range(len(self.pointsPlotted)):
                color = cmap[int((255/(self.maxPe-self.minPe))*(self.masterParamap[self.pointsPlotted[i][0], self.pointsPlotted[i][1], self.pointsPlotted[i][2]][1]-self.minPe))]
                color = [color[i]*255 for i in range(len(color))]
                self.maskCoverImg[self.pointsPlotted[i][0], self.pointsPlotted[i][1], self.pointsPlotted[i][2]] = [color[2], color[1], color[0], int(self.curAlpha.value())]

            self.figLeg.clear()
            a = np.array([[0,1]])
            self.figLeg = plt.figure()
            img = plt.imshow(a, cmap='magma')
            plt.gca().set_visible(False)
            if system == 'Windows':
                cax = plt.axes([0,0.1,0.35,0.8])
                cbar = plt.colorbar(orientation='vertical', cax=cax)
                plt.text(3,0.45,"PE", rotation=270, size=9)
                plt.tick_params('y', labelsize=8, pad=0.5)
            else:
                cax = plt.axes([0, 0.1, 0.25, 0.8])
                cbar = plt.colorbar(orientation='vertical', cax=cax)
                plt.text(3.1, 0.45, "PE", rotation=270, size=4.5) 
                plt.tick_params('y', labelsize=4, pad=0.5)
            cax.set_yticks([0,0.25, 0.5, 0.75, 1])
            cax.set_yticklabels([int(self.minPe*10)/10,int((((self.maxPe-self.minPe)/4)+self.minPe)*10)/10,int((((self.maxPe - self.minPe)/2)+self.minPe)*10)/10,int(((3*(self.maxPe-self.minPe)/4)+self.minPe)*10)/10,int(self.maxPe*10)/10])
            self.horizLayoutLeg.removeWidget(self.canvasLeg)
            self.canvasLeg = FigureCanvas(self.figLeg)
            self.horizLayoutLeg.addWidget(self.canvasLeg)
            self.canvasLeg.draw()

            self.changeAxialSlices()
            self.changeSagSlices()
            self.changeCorSlices()

        elif self.peParamapButton.isCheckable():
            self.maskCoverImg.fill(0)
            self.figLeg = plt.figure()
            for i in range(len(self.pointsPlotted)):
                self.maskCoverImg[self.pointsPlotted[i][0], self.pointsPlotted[i][1], self.pointsPlotted[i][2]] = [0,0,255,int(self.curAlpha.value())]
            self.legend.setHidden(True)

            self.changeAxialSlices()
            self.changeSagSlices()
            self.changeCorSlices()

    def showTp(self):
        if self.tpParamapButton.isChecked():
            if self.id == 0:
                self.legend.setHidden(False)
            self.aucParamapButton.setChecked(False)
            self.peParamapButton.setChecked(False)
            self.mttParamapButton.setChecked(False)
            cmapStruct = plt.get_cmap('plasma')
            cmap = cmapStruct.colors
            self.maskCoverImg.fill(0)

            for i in range(len(self.pointsPlotted)):
                color = cmap[int((255/(self.maxTp-self.minTp))*(self.masterParamap[self.pointsPlotted[i][0], self.pointsPlotted[i][1], self.pointsPlotted[i][2]][2]-self.minTp))]
                color = [color[i]*255 for i in range(len(color))]
                self.maskCoverImg[self.pointsPlotted[i][0], self.pointsPlotted[i][1], self.pointsPlotted[i][2]] = [color[2], color[1], color[0], int(self.curAlpha.value())]

            self.figLeg.clear()
            a = np.array([[0,1]])
            self.figLeg = plt.figure()
            img = plt.imshow(a, cmap='plasma')
            plt.gca().set_visible(False)
            if system == 'Windows':
                cax = plt.axes([0,0.1,0.35,0.8])
                cbar = plt.colorbar(orientation='vertical', cax=cax)
                plt.text(3,0.45,"TP",rotation=270,size=9)
                plt.tick_params('y', labelsize=8, pad=0.5)
            else:
                cax = plt.axes([0, 0.1, 0.25, 0.8])
                cbar = plt.colorbar(orientation='vertical', cax=cax)
                plt.text(3, 0.45, "TP", rotation=270, size=4.5) 
                plt.tick_params('y', labelsize=4, pad=0.5)
            cax.set_yticks([0,0.25, 0.5, 0.75, 1])
            cax.set_yticklabels([int(self.minTp*10)/10,int((((self.maxTp-self.minTp)/4)+self.minTp)*10)/10,int((((self.maxTp - self.minTp)/2)+self.minTp)*10)/10,int(((3*(self.maxTp-self.minTp)/4)+self.minTp)*10)/10,int(self.maxTp*10)/10])
            self.horizLayoutLeg.removeWidget(self.canvasLeg)
            self.canvasLeg = FigureCanvas(self.figLeg)
            self.horizLayoutLeg.addWidget(self.canvasLeg)
            self.canvasLeg.draw()

            self.changeAxialSlices()
            self.changeSagSlices()
            self.changeCorSlices()

        elif self.tpParamapButton.isCheckable():
            self.maskCoverImg.fill(0)
            for i in range(len(self.pointsPlotted)):
                self.maskCoverImg[self.pointsPlotted[i][0], self.pointsPlotted[i][1], self.pointsPlotted[i][2]] = [0,0,255,int(self.curAlpha.value())]
            self.legend.setHidden(True)

            self.changeAxialSlices()
            self.changeSagSlices()
            self.changeCorSlices()

    def showMtt(self):
        if self.mttParamapButton.isChecked():
            if self.id == 0:
                self.legend.setHidden(False)
            self.aucParamapButton.setChecked(False)
            self.peParamapButton.setChecked(False)
            self.tpParamapButton.setChecked(False)
            cmapStruct = plt.get_cmap('cividis')
            cmap = cmapStruct.colors
            self.maskCoverImg.fill(0)

            for i in range(len(self.pointsPlotted)):
                color = cmap[int((255/(self.maxMtt-self.minMtt))*(self.masterParamap[self.pointsPlotted[i][0], self.pointsPlotted[i][1], self.pointsPlotted[i][2]][3]-self.minMtt))]
                color = [color[i]*255 for i in range(len(color))]
                self.maskCoverImg[self.pointsPlotted[i][0], self.pointsPlotted[i][1], self.pointsPlotted[i][2]] = [color[2], color[1], color[0], int(self.curAlpha.value())]

            self.figLeg.clear()
            a = np.array([[0,1]])
            self.figLeg = plt.figure()
            img = plt.imshow(a, cmap='cividis')
            plt.gca().set_visible(False)
            if system == 'Windows':
                cax = plt.axes([0,0.1,0.35,0.8])
                cbar = plt.colorbar(orientation='vertical', cax=cax)
                plt.text(3,0.43,"MTT",rotation=270,size=9)
                plt.tick_params('y',labelsize=8,pad=0.5)
            else:
                cax = plt.axes([0, 0.1, 0.25, 0.8])
                cbar = plt.colorbar(orientation='vertical', cax=cax)
                plt.text(3, 0.43, "MTT", rotation=270, size=4.5) 
                plt.tick_params('y', labelsize=4, pad=0.5)
            cax.set_yticks([0,0.25, 0.5, 0.75, 1])
            cax.set_yticklabels([int(self.minMtt*10)/10,int((((self.maxMtt-self.minMtt)/4)+self.minMtt)*10)/10,int((((self.maxMtt - self.minMtt)/2)+self.minMtt)*10)/10,int(((3*(self.maxMtt-self.minMtt)/4)+self.minMtt)*10)/10,int(self.maxMtt*10)/10])
            self.horizLayoutLeg.removeWidget(self.canvasLeg)
            self.canvasLeg = FigureCanvas(self.figLeg)
            self.horizLayoutLeg.addWidget(self.canvasLeg)
            self.canvasLeg.draw()

            self.changeAxialSlices()
            self.changeSagSlices()
            self.changeCorSlices()

        elif self.mttParamapButton.isCheckable():
            self.maskCoverImg.fill(0)
            for i in range(len(self.pointsPlotted)):
                self.maskCoverImg[self.pointsPlotted[i][0], self.pointsPlotted[i][1], self.pointsPlotted[i][2]] = [0,0,255,int(self.curAlpha.value())]
            self.legend.setHidden(True)

            self.changeAxialSlices()
            self.changeSagSlices()
            self.changeCorSlices()

    def createBinaryMaskCor(self):
        PixelType = itk.ctype("unsigned char")
        Dimension = 2
        ImageType = itk.Image[PixelType, Dimension]

        #---- creating empty array for compiling .png to .nii
        try:
            print(self.emptyArrayMaskCor.shape)
        except AttributeError:
            self.emptyArrayMaskCor = np.zeros([self.widthCor, self.y+1, self.heightCor])

        reader = itk.ImageFileReader[ImageType].New()
        self.output_cor_name = str("drawn_cor_" + str(self.corScroll.value()))

        if os.path.exists(os.path.join("niftiROIs", str(self.output_cor_name + ".png"))):
            reader.SetFileName(os.path.join("niftiROIs", str(self.output_cor_name + ".png")))
            thresholdFilter = itk.BinaryThresholdImageFilter[ImageType,ImageType].New()
            thresholdFilter.SetInput(0,reader.GetOutput())
            thresholdFilter.SetLowerThreshold(255)
            thresholdFilter.SetUpperThreshold(255)
            thresholdFilter.SetOutsideValue(0)
            thresholdFilter.SetInsideValue(255)

            writer = itk.ImageFileWriter[ImageType].New()
            writer.SetFileName(os.path.join("niftiBinaryMasks", str(self.output_cor_name + ".png")))
            writer.SetInput(thresholdFilter.GetOutput())
            writer.Update()

            img_mask = cv2.imread(os.path.join("niftiBinaryMasks", str(self.output_cor_name + ".png")))
            img_mask = img_mask[:,:,0]
            img_mask = np.flipud(img_mask)
            im = Image.fromarray(img_mask)
            im.save(os.path.join("niftiBinaryMasks", str(self.output_cor_name + ".png")))

            for h in range(self.heightCor):
                for w in range(self.widthCor):
                    self.emptyArrayMaskCor[w][self.corScroll.value()][h] = img_mask[h][w]
            

            self.data_drawn_nibImg_cor = np.array(Image.open(os.path.join("niftiBinaryMasks", self.output_cor_name_file)))
            self.data_drawn_nibImg_cor = self.data_drawn_nibImg_cor.astype(np.uint8)
            self.data_drawn_nibImg_cor = np.require(self.data_drawn_nibImg_cor,np.uint8,'C')
            self.bytesLineCordrawn, _ = self.data_drawn_nibImg_cor.strides
            temp_pic = QImage(self.data_drawn_nibImg_cor, self.widthCor, self.heightCor, self.bytesLineCordrawn, QImage.Format_Grayscale8)
            self.corPlane.setPixmap(QPixmap.fromImage(temp_pic).scaled(331,311))

        else:
            self.feedbackText.setText("mask only generated from modified image")


# ELEVENTH STEP: able to quickly navigate to slices clicking through comboboxes at top of scroll bar
#-----------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------
    # def quickNavigateAxial(self):
    #     # self.axCurrIndex = self.chooseScrollvalAxial.currentIndex()
    #     self.axialScroll.setValue(self.axCurrIndex)
    # def quickNavigateSag(self):
    #     # self.sag_currIndex = self.chooseScrollvalSag.currentIndex()
    #     self.sagScroll.setValue(self.sag_currIndex)
    # def quickNavigateCor(self):
    #     # self.cor_currIndex = self.chooseScrollvalCor.currentIndex()
    #     self.corScroll.setValue(self.cor_currIndex)

# TWELVTH STEP: after done masking ROIs, need to save all .pngs into single segmentation img (.nii)
#-----------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------
    def saveNiftiAxial(self):
        #insert some function here
        # print("entering saving .nii function")
        # self.emptyArrayMaskAxial = np.swapaxes(self.emptyArrayMaskAxial,0,1)
        # print("swapped axes are: " + str(self.emptyArrayMaskAxial.shape))
        self.newSavedImgAxial = nib.Nifti1Image(self.emptyArrayMaskAxial, affine=np.eye(4))
        nib.Nifti1
        nib.save(self.newSavedImgAxial,'segmentedAxialImageCv.nii.gz')
        self.feedbackText.setText("Saved image as\nsegmentedAxialImageCv.nii.gz")
        # print("saved image as segmentedAxialImageCv.nii")

    def saveNiftiSag(self):
        # self.emptyArrayMaskSag = np.swapaxes(self.emptyArrayMaskSag,0,1)
        self.newSavedImgSag = nib.Nifti1Image(self.emptyArrayMaskSag, affine=np.eye(4))
        nib.save(self.newSavedImgSag, 'segmentedSagImageCv.nii.gz')
        self.feedbackText.setText("Saved image as\nsegmentedSagImageCv.nii.gz")

    def saveNiftiCor(self):
        # self.emptyArrayMaskCor = np.swapaxes(self.emptyArrayMaskCor, 0, 1)
        self.newSavedImgCor = nib.Nifti1Image(self.emptyArrayMaskCor, affine=np.eye(4))
        nib.save(self.newSavedImgCor, 'segmentedCorImageCv.nii.gz')
        self.feedbackText.setText("Saved image as\nsegmentedCorImageCv.nii.gz")

    def saveOverallNifti(self):
        #---- creating empty array for compiling .png to .nii
        try:
            print(self.emptyArrayMaskAxial.shape)
        except AttributeError:
            self.emptyArrayMaskAxial = np.zeros([self.widthAx,self.heightAx,self.z+1])
        try:
            print(self.emptyArrayMaskSag.shape)
        except AttributeError:
            self.emptyArrayMaskSag = np.zeros([self.x+1,self.heightSag, self.widthSag])
        try:
            print(self.emptyArrayMaskCor.shape)
        except AttributeError:
            self.emptyArrayMaskCor = np.zeros([self.widthCor, self.y+1, self.heightCor])
        totalMask = self.emptyArrayMaskAxial + self.emptyArrayMaskSag + self.emptyArrayMaskCor
        (totalMask > 0).astype(int)
        newSavedMask = nib.Nifti1Image(totalMask, affine=np.eye(4))
        nib.save(newSavedMask, 'segmentedOverallImageCv.nii.gz')
        self.feedbackText.setText("Saved image as\nsegmentedOverallImageCv.nii.gz")
        

#Julie's code for interpolate button begins here
#--------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------
    def interpolating(self):
            fname = QFileDialog.getOpenFileName(None, 'Select Segmented Nifti File')
            fileName = fname[0]
            image = itk.imread(fileName)
            castImage = image.astype(itk.ctype("unsigned char"))

            filled = itk.morphological_contour_interpolator(castImage)
            itk.imwrite(filled, "interpolatedResultNewCv.nii.gz")
            print("saved as interpolatedResultNewCv.nii.gz")




# Julie's code for MC functions begins here
#--------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------
    def xmlOptionSetUp(self):
        self.fileLocation = ""
        self.chooseFolderButton.clicked.connect(self.browseFiles)
        self.clearFolderButton.clicked.connect(self.clearBrowsing)
        self.convertXmlButton.clicked.connect(self.convertXmltoNifti)
        self.openXmlNiiButton.clicked.connect(self.showNifti)
        self.saveXmlNiiButton.clicked.connect(self.savingXMLNifti)
        self.saveBeamshapeMaskButton.clicked.connect(self.savingBeamshapeNifti)
        self.saveMipMaskButton.clicked.connect(self.savingMIPNifti)

    def browseFiles(self): #just added an if statement for user feedback
        fname = QFileDialog.getExistingDirectory(None, 'Select Directory')
        if fname != '':
            self.xmlLineEdit.setText(fname)
            self.fileLocation = fname
            self.feedbackText.setText("Valid Folder Chosen")

    def clearBrowsing(self):
        self.xmlLineEdit.setText("")
        self.fileLocation = ""

    def convertXmltoNifti(self):
        pythonName = "python3.9" # David --> find a way to prompt user to input their preferred python interpreter command name
        os.system("{0} xml2nii.py {1}" .format(pythonName, self.fileLocation))

        tmpLocation = self.fileLocation.split("/")
        tmpName = tmpLocation[len(tmpLocation)-1]
        #tmpName = tmpLocation[len(tmpLocation)-2] #David

        cwd = os.getcwd()
        newDataPath = ("{0}/{1}" .format(cwd, tmpName))
        if os.path.exists(newDataPath): #David
           shutil.rmtree(newDataPath) #will also remove all the drawings made
        os.mkdir(newDataPath)

        # David --> initialize nifti files for xml conversion files

        if os.path.exists("niftiROIs"):
            shutil.rmtree("niftiROIs") #will also remove all the drawings made
        if os.path.exists("niftiMasks"):
            shutil.rmtree("niftiMasks") #will remove all the masks made from drawings
        if os.path.exists("niftiBinaryMasks"):
            shutil.rmtree("niftiBinaryMasks")

        # Original started here
        os.mkdir("niftiROIs") #for drawings
        os.mkdir("niftiMasks") #was used for the masks that had transparent background, but currently not used
        os.mkdir("niftiBinaryMasks") #for binary masks

        # Everything below is commented out because .nii.gz file is made in savingBeamshapeNifti function

        dataPath = ("{0}/{1}_maskMIP.nii.gz" .format(cwd, tmpName))
        shutil.move(dataPath, newDataPath)

        dataPath = ("{0}/{1}_maskBeamshape.nii.gz" .format(cwd, tmpName))
        shutil.move(dataPath, newDataPath) # Don't need to move since cwd is now in the right place (David)

        # David --> following two lines are redundant with dataPath earlier. Problem was fixed by changing working directory of os.system
        dataPath = ("{0}/{1}.nii.gz" .format(cwd, tmpName))
        shutil.move(dataPath, newDataPath)

    def showNifti(self):
        tmpLocation = self.fileLocation.split("/")
        tmpName = tmpLocation[len(tmpLocation)-1]
        #tmpName = tmpLocation[len(tmpLocation)-2] #David (also changed the other tmpName)
        cwd = os.getcwd()
        currentDataPath = ("{0}/{1}/{1}.nii.gz" .format(cwd, tmpName))
        
        # Save currentDataPath for purposes of undo last rectangle
        self.inputTextPath = currentDataPath

        self.feedbackText.setText("displaying xml2nii created nifti")

        self. nib.load(currentDataPath, mmap=False)
        self.dataNibImg = self.nibImg.get_fdata()
        self.dataNibImg = self.dataNibImg.astype(np.uint8)

        self.curSlice = 0
        #Get dimensions of XML files
        self.data4dImg = self.dataNibImg[:,:,:,self.curSlice]
        self.OGData4dImg = self.data4dImg.copy()
        self.x,self.y,self.z = self.data4dImg.shape
        self.x = self.x-1
        self.y = self.y-1
        self.z = self.z-1

        #Set scroll range to account for all pictures in each plane
        self.axialScroll.setMaximum(self.z)
        self.sagScroll.setMaximum(self.x)
        self.corScroll.setMaximum(self.y)

        #Set all scrolls to the top
        self.axialScroll.setValue(0)
        self.sagScroll.setValue(0)
        self.corScroll.setValue(0)

        self.totalFramesAx.setText(str(self.z+1))
        self.totalFramesSag.setText(str(self.x+1))
        self.totalFramesCor.setText(str(self.y+1))

        self.currentFrameAx.setText("1")
        self.currentFrameSag.setText("1")
        self.currentFrameCor.setText("1")

        self.data2dAx = self.data4dImg[:,:,0, self.curSlice] #Get images from correct plane
        self.data2dAx = np.flipud(self.data2dAx) #flipud (flip order)
        self.data2dAx = np.rot90(self.data2dAx,3) #rotate ccw 90
        self.data2dAx = np.require(self.data2dAx,np.uint8, 'C') #move array into contiguous memory
        self.data2dSag = self.data4dImg[0,:,:, self.curSlice] #Get images from correct plane
        self.data2dSag = np.flipud(self.data2dSag) #flipud
        self.data2dSag = np.rot90(self.data2dSag,2) #rotate ccw 90
        self.data2dSag = np.fliplr(self.data2dSag)
        self.data2dSag = np.require(self.data2dSag,np.uint8,'C') #move array into contiguous memory
        self.data2dCor = self.data4dImg[:,0,:, self.curSlice] #Get images from correct plane
        self.data2dCor = np.rot90(self.data2dCor,1) #rotate ccw 90
        self.data2dCor = np.flipud(self.data2dCor) #flipud
        # self.data2dCor = np.fliplr(self.data2dCor)
        self.data2dCor = np.require(self.data2dCor,np.uint8,'C') #move array into contiguous memory

        self.heightAx, self.widthAx = self.data2dAx.shape
        self.heightSag, self.widthSag = self.data2dSag.shape
        self.heightCor, self.widthCor = self.data2dCor.shape

        bytesLineAx, _ = self.data2dAx.strides
        bytesLineSag, _ = self.data2dSag.strides
        bytesLineCor, _ = self.data2dCor.strides

        self.qImgAx = QImage(self.data2dAx, self.widthAx, self.heightAx, bytesLineAx, QImage.Format_Grayscale8)
        self.qImgSag = QImage(self.data2dSag, self.widthSag, self.heightSag, bytesLineSag, QImage.Format_Grayscale8)
        self.qImgCor = QImage(self.data2dCor, self.widthCor, self.heightCor, bytesLineCor, QImage.Format_Grayscale8)

        self.pixmapAx = QPixmap.fromImage(self.qImgAx).scaled(331,311) #changed to self. to be able to draw on top of
        self.pixmapSag = QPixmap.fromImage(self.qImgSag).scaled(331,311)
        self.pixmapCor = QPixmap.fromImage(self.qImgCor).scaled(331,311)

        self.axialPlane.setPixmap(self.pixmapAx)
        self.sagPlane.setPixmap(self.pixmapSag)
        self.corPlane.setPixmap(self.pixmapCor)

    def savingXMLNifti(self):
        fnameXML = QFileDialog.getExistingDirectory(None, 'Select Directory For Nifti')

        tmpLocation = self.fileLocation.split("/")
        tmpName = tmpLocation[len(tmpLocation)-1]
        cwd = os.getcwd()
        currentDataPath = ("{0}/{1}/{1}.nii.gz" .format(cwd, tmpName))

        shutil.copy(currentDataPath, fnameXML)

    def savingBeamshapeNifti(self):
        fnameXML = QFileDialog.getExistingDirectory(None, 'Select Directory For Beamshape Nifti Mask')

        tmpLocation = self.fileLocation.split("/")
        tmpName = tmpLocation[len(tmpLocation)-2]
        cwd = os.getcwd()
        currentDataPath = ("{0}/{1}/{1}_maskBeamshape.nii.gz" .format(cwd, tmpName))

        shutil.copy(currentDataPath, fnameXML)

    def savingMIPNifti(self):
        fnameXML = QFileDialog.getExistingDirectory(None, 'Select Directory For MIP Nifti Mask')

        tmpLocation = self.fileLocation.split("/")
        tmpName = tmpLocation[len(tmpLocation)-2]
        cwd = os.getcwd()
        currentDataPath = ("{0}/{1}_maskMIP.nii.gz" .format(cwd, tmpName))

        shutil.copy(currentDataPath, fnameXML)

    # def motionCorrectionSetUp(self):
    #     if self.ticComputed:
    #         self.start_MC.clicked.connect(self.motionCorrect)
    #         self.display_Comparison.clicked.connect(self.compare)
    #         self.save_MC.clicked.connect(self.saveMotionResults)

    def motionCorrect(self):
        msg = QMessageBox()
        msg.setWindowTitle("Copy the text to the shell. Type 'exit' once done.")
        msg.setText("./MotionCorrection.sh <input1> <input2> <input3>\n\ninput1 = Name of directory with nifti data and frames\ninput2 = Name of nifti data\ninput3 = Number of windows (Recommended is 5)\n\n\n Set up shell environment according to MotionCorrectionInstructions.md")
        x = msg.exec_()

        os.system("ubuntu")

        self.feedbackScrollBar.setHidden(False)
        self.feedbackText.setText("Finished Motion Correction.")

    def compare(self):
        self.MainWindow = QMainWindow()
        self.ticEditor = Ui_MainWindow()
        self.ticEditor.setupUi(self.MainWindow)
        self.MainWindow.show()

    def saveMotionResults(self):
        fnameXML = QFileDialog.getExistingDirectory(None, 'Select Directory To Save Motion Correction Results')
        fname = QFileDialog.getOpenFileName(None, 'Select Motion Corrected File')
        fileName = fname[0]
        shutil.copy(fileName, fnameXML)

    # def calculateSpline3D(self, xpts, ypts, zpts):
    #     x_grid = np.arange(0, self.x+1, 1)
    #     y_grid = np.arange(0, self.y+1, 1)
    #     b_1, b_2 = np.meshgrid(x_grid, y_grid)
    #     spline = interpolate.Rbf(xpts,ypts,zpts,function='thin_plate',smooth=5, episilon=5)
    #     z_spline = spline(b_1, b_2)

    #     # x,y,z = np.array(interpolate.splev(np.linspace(0, 1, 1000), tck))
    #     return x,y,z

def calculateSpline(xpts, ypts): # 2D spline interpolation
    cv = []
    for i in range(len(xpts)):
        cv.append([xpts[i], ypts[i]])
    cv = np.array(cv)
    if len(xpts) == 2:
        tck, u_ = interpolate.splprep(cv.T, s=0.0, k=1)
    elif len(xpts) == 3:
        tck, u_ = interpolate.splprep(cv.T, s=0.0, k=2)
    else:
        tck, u_ = interpolate.splprep(cv.T, s=0.0, k=3)
    x,y = np.array(interpolate.splev(np.linspace(0, 1, 1000), tck))
    return x, y

def create_enclosing_surface_of_best_fit(x, y, z, resolution=100):
    """Create an enclosing surface of best fit for 3D data using spline interpolation."""

    # Generate a regular grid for the x and y data
    x_range = np.linspace(np.min(x), np.max(x), resolution)
    y_range = np.linspace(np.min(y), np.max(y), resolution)
    x_grid, y_grid = np.meshgrid(x_range, y_range)

    # Generate a 1D grid for the z data
    z_grid = np.zeros_like(x_grid)
    for i, xi in enumerate(x_range):
        mask = x == xi
        if np.any(mask):
            z_values = z[mask]
            y_values = y[mask]
            sorted_indices = np.argsort(y_values)
            z_values = z_values[sorted_indices]
            y_values = y_values[sorted_indices]
            z_values = np.pad(z_values, (0, resolution - len(z_values)), mode='edge')
            z_grid[:, i] = z_values

    # Interpolate the 1D grid to the 2D grid using cubic spline interpolation
    z_interp = griddata((x.ravel(), y.ravel()), z.ravel(), (x_grid, y_grid), method='cubic')

    return [[int(x_grid[i]), int(y_grid[i]), int(z_interp[i])] for i in range(len(x_grid))]

def ellipsoidFitLS(pos):

    # centre coordinates on origin
    pos = pos - np.mean(pos, axis=0)

    # build our regression matrix
    A = pos**2

    # vector of ones
    O = np.ones(len(A))

    # least squares solver
    B, resids, rank, s = np.linalg.lstsq(A, O, rcond=None)

    # solving for a, b, c
    a_ls = np.sqrt(1.0/B[0])
    b_ls = np.sqrt(1.0/B[1])
    c_ls = np.sqrt(1.0/B[2])

    return (a_ls, b_ls, c_ls)

def calculateSpline3D(points):
    # Calculate ellipsoid of best fit
    # points = np.array(points)
    # a,b,c = ellipsoidFitLS(points)
    # output = set()


    # u = np.linspace(0., np.pi*2., 1000)
    # v = np.linspace(0., np.pi, 1000)
    # u, v = np.meshgrid(u,v)

    # x = a*np.cos(u)*np.sin(v)
    # y = b*np.sin(u)*np.sin(v)
    # z = c*np.cos(v)

    # # turn this data into 1d arrays
    # x = x.flatten()
    # y = y.flatten()
    # z = z.flatten()
    # x += np.mean(points, axis=0)[0]
    # y += np.mean(points, axis=0)[1]
    # z += np.mean(points, axis=0)[2]

    # for i in range(len(x)):
    #     output.add((int(x[i]), int(y[i]), int(z[i])))
    # return output
    cloud = pv.PolyData(points, force_float=False)
    volume = cloud.delaunay_3d(alpha=100.)
    shell = volume.extract_geometry()
    final = shell.triangulate()
    # final.smooth(n_iter=1000)
    faces = final.faces.reshape((-1, 4))
    faces = faces[:, 1:]
    arr = final.points[faces]
    arr = np.array(arr)
    output = set()
    for tri in arr:
        slope_2 = (tri[2]-tri[1])
        start_2 = tri[1]
        slope_3 = (tri[0]-tri[1])
        start_3 = tri[1]
        for i in range(100, -1, -1):
            bound_one = start_2 + ((i/100)*slope_2)
            bound_two = start_3 + ((i/100)*slope_3)
            cur_slope = bound_one-bound_two
            cur_start = bound_two
            for j in range(100, -1, -1):
                cur_pos = cur_start + ((j/100)*cur_slope)
                output.add((int(cur_pos[0]), int(cur_pos[1]), int(cur_pos[2])))
    return output

def bolusLognormal(x, auc, mu, sigma, t0):        
    curve_fit=(auc/(2.5066*sigma*(x-t0)))*np.exp(-1*(((np.log(x-t0)-mu)**2)/(2*sigma*sigma))) 
    return np.nan_to_num(curve_fit)