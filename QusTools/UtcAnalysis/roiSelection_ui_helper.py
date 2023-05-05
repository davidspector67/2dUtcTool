from UtcAnalysis.roiSelection_ui import *
from UtcAnalysis.editImageDisplay_ui_helper import *

import matlab.engine
import os
import numpy as np
from PIL import Image, ImageEnhance
import shutil
import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib 
import scipy.interpolate as interpolate

eng = matlab.engine.start_matlab()
pointsPlottedX = []
pointsPlottedY = []


class RoiSelectionGUI(QWidget, Ui_constructRoi):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.imageFilenameDisplay.setHidden(True)
        self.phantomFilenameDisplay.setHidden(True)
        self.roiNameDisplay.setHidden(True)

        # Prepare B-Mode display plot
        self.horizontalLayout = QHBoxLayout(self.imDisplayFrame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.horizontalLayout.addWidget(self.canvas)

        self.editImageDisplayGUI = EditImageDisplayGUI()
        self.editImageDisplayGUI.contrastVal.valueChanged.connect(self.changeContrast)
        self.editImageDisplayGUI.brightnessVal.valueChanged.connect(self.changeBrightness)    
        self.editImageDisplayGUI.sharpnessVal.valueChanged.connect(self.changeSharpness)

        self.scatteredPoints = []

        self.redrawRoiButton.setHidden(True)
        
        self.editImageDisplayButton.clicked.connect(self.openImageEditor)
        self.drawRoiButton.clicked.connect(self.recordDrawROIClicked)
        self.undoLastPtButton.clicked.connect(self.undoLastPt)
        self.closeRoiButton.clicked.connect(self.closeInterpolation)
        self.redrawRoiButton.clicked.connect(self.restartROI)

    def changeContrast(self):
        self.editImageDisplayGUI.contrastValDisplay.setValue(int(self.editImageDisplayGUI.contrastVal.value()*10))
        self.updateBModeSettings()

    def changeBrightness(self):
        self.editImageDisplayGUI.brightnessValDisplay.setValue(int(self.editImageDisplayGUI.brightnessVal.value()*10))
        self.updateBModeSettings()

    def changeSharpness(self):
        self.editImageDisplayGUI.sharpnessValDisplay.setValue(int(self.editImageDisplayGUI.sharpnessVal.value()*10))
        self.updateBModeSettings()

    def openImageEditor(self):
        if self.editImageDisplayGUI.isVisible():
            self.editImageDisplayGUI.hide()
        else:
            self.editImageDisplayGUI.show()

    def setFilenameDisplays(self, imageName, phantomName):
        # called in selectImage_ui_helper.py
        self.imageFilenameDisplay.setHidden(False)
        self.phantomFilenameDisplay.setHidden(False)
        self.imageFilenameDisplay.setText(imageName)
        self.phantomFilenameDisplay.setText(phantomName)
    
    def plotOnCanvas(self): # Plot current image on GUI
        self.ax = self.figure.add_subplot(111)
        im = plt.imread(os.path.join("imROIs", "bModeIm.png"))
        plt.imshow(im, cmap='Greys_r')

        if len(pointsPlottedX) > 0:
            self.scatteredPoints.append(self.ax.scatter(pointsPlottedX[-1], pointsPlottedY[-1], marker="o", s=0.5, c="red", zorder=500))
            if len(pointsPlottedX) > 1:
                xSpline, ySpline = calculateSpline(pointsPlottedX, pointsPlottedY)
                self.spline = self.ax.plot(xSpline, ySpline, color = "cyan", zorder=1, linewidth=0.75)
        self.figure.subplots_adjust(left=0,right=1, bottom=0,top=1, hspace=0.2,wspace=0.2)
        global cursor
        cursor = matplotlib.widgets.Cursor(self.ax, color="gold", linewidth=0.4, useblit=True)
        cursor.set_active(False)
        plt.tick_params(bottom=False, left=False, labelbottom=False, labelleft=False)
        self.canvas.draw() # Refresh canvas


    def openImage(self, imageFilePath, phantomFilePath): # Open initial image given data and phantom files previously inputted
        # Assume inputted files are correct 
        # TODO: implement this in image selection page
        # For now, Canon .bin files are not supported
        tmpLocation = imageFilePath.split("/")
        dataFileName = tmpLocation[-1]
        dataFileLocation = imageFilePath[:len(imageFilePath)-len(dataFileName)]
        tmpPhantLocation = phantomFilePath.split("/")
        phantFileName = tmpPhantLocation[-1]
        phantFileLocation = phantomFilePath[:len(phantomFilePath)-len(phantFileName)]
        if dataFileName[-3:] == ".rf": # Check binary signatures at start of .rf files
            dataFile = open(imageFilePath, 'rb')
            phantFile = open(phantomFilePath, 'rb')
            dataSIg = list(dataFile.read(8))
            phantSIg = list(phantFile.read(8))
            if dataSIg != [0,0,0,0,255,255,0,0] and phantSIg != [0,0,0,0,255,255,0,0]: # Philips signature parameters
                # self.invalidPath.setText("Data and Phantom files are both invalid.\nPlease use Philips .rf files.")
                return
            elif phantSIg != [0,0,0,0,255,255,0,0]:
                # self.invalidPath.setText("Invalid phantom file.\nPlease use Philips .rf files.")
                return
            elif dataSIg != [0, 0, 0, 0, 255, 255, 0, 0]:
                # self.invalidPath.setText("Invalid data file.\nPlease use Philips .rf files.")
                return
            else: # Display Philips image and assign relevant default analysis
                s = eng.genpath(str(os.getcwd()+'/Machine_Code/Philips'))
                eng.addpath(s, nargout=0)
                imArray, self.imgDataStruct, self.imgInfoStruct, self.refDataStruct, self.refInfoStruct = eng.philips_getImage(dataFileName, dataFileLocation, phantFileName, phantFileLocation, self.frame, nargout=5)
                self.arHeight = imArray.size[0]
                self.arWidth = imArray.size[1]
                self.imData = np.array(imArray).reshape(self.arHeight, self.arWidth)
                self.imData = np.flipud(self.imData) #flipud
                self.imData = np.require(self.imData,np.uint8,'C')
                self.bytesLine = self.imData.strides[0]
                self.qIm = QImage(self.imData, self.arWidth, self.arHeight, self.bytesLine, QImage.Format_Grayscale8) 

                self.qIm.mirrored().save(os.path.join("imROIs", "bModeImRaw.png")) # Save as .png file

                self.pixSizeAx = self.imgDataStruct['scBmode'].size[0]
                self.pixSizeLat = self.imgDataStruct['scBmode'].size[1]

                self.editImageDisplayGUI.contrastVal.setValue(4)
                self.editImageDisplayGUI.brightnessVal.setValue(0.75)
                self.editImageDisplayGUI.sharpnessVal.setValue(3)

                self.axialOverlap = 0.5
                self.lateralOverlap = 0.5
                self.minFrequency = 3000000
                self.maxFrequency = 4500000
                self.axialWinSize = 1#1480/20000000*10000 # must be at least 10 times wavelength
                self.lateralWinSize = 1#1480/20000000*10000 # must be at least 10 times wavelength
                self.frame = 1
                self.samplingFreq = 20000000
                self.threshold = 95

        elif dataFileName[-4:] == ".mat": # Display Philips image and assign relevant default analysis params
            s = eng.genpath(str(os.getcwd()+'/Machine_Code/Philips'))
            eng.addpath(s, nargout=0)
            imArray, self.imgDataStruct, self.imgInfoStruct, self.refDataStruct, self.refInfoStruct = eng.philips_getImage(dataFileName, dataFileLocation, phantFileName, phantFileLocation, self.frame, nargout=5)
            self.arHeight = imArray.size[0]
            self.arWidth = imArray.size[1]
            self.imData = np.array(imArray).reshape(self.arHeight, self.arWidth)
            self.imData = np.flipud(self.imData) #flipud
            self.imData = np.require(self.imData,np.uint8,'C')
            self.bytesLine = self.imData.strides[0]
            self.qIm = QImage(self.imData, self.arWidth, self.arHeight, self.bytesLine, QImage.Format_Grayscale8) 

            self.qIm.mirrored().save(os.path.join("imROIs", "bModeImRaw.png")) # Save as .png file

            self.pixSizeAx = self.imgDataStruct['Bmode'].size[0] #were both scBmode
            self.pixSizeLat = self.imgDataStruct['Bmode'].size[1]

            self.editImageDisplayGUI.contrastVal.setValue(4)
            self.editImageDisplayGUI.brightnessVal.setValue(0.75)
            self.editImageDisplayGUI.sharpnessVal.setValue(3)

            self.axialOverlap = 0.5
            self.lateralOverlap = 0.5
            self.minFrequency = 3000000
            self.maxFrequency = 4500000
            self.axialWinSize = 10#7#1#1480/20000000*10000 # must be at least 10 times wavelength
            self.lateralWinSize = 10#7#1#1480/20000000*10000 # must be at least 10 times wavelength
            self.frame = 1
            self.samplingFreq = 20000000
            self.threshold = 95

        elif dataFileName[-4:] == ".rfd": # Display Siemens image and assign relevant default analysis params
            s = eng.genpath(str(os.getcwd()+'/Machine_Code/Siemens'))
            eng.addpath(s, nargout=0)
            path = str(os.getcwd() + "/imROIs/bModeImRaw.png")
            self.imgDataStruct, self.imgInfoStruct, self.refDataStruct, self.refInfoStruct = eng.sie_getImage(dataFileName, dataFileLocation, phantFileName, phantFileLocation, path, nargout=4)

            global rfd
            rfd = True
            self.pixSizeAx = self.imgDataStruct['Bmode'].size[0]
            self.pixSizeLat = self.imgDataStruct['Bmode'].size[1]

            self.editImageDisplayGUI.contrastVal.setValue(1)
            self.editImageDisplayGUI.brightnessVal.setValue(1)
            self.editImageDisplayGUI.sharpnessVal.setValue(1)

            self.minFrequency = 7000000
            self.maxFrequency = 17000000
            self.axialWinSize = 3.5#1480/40000000*5000 # must be at least 10 times wavelength
            self.lateralWinSize = 3.5#self.axialWinSize * 6 # must be at least 10 times wavelength
            self.frame = 51
            self.samplingFreq = 40000000
            self.axialOverlap = 0.5
            self.lateralOverlap = 0.5
            self.threshold = 95

        else:
            return

        # Implement correct previously assigned image display settings

        self.cvIm = Image.open(os.path.join("imROIs", "bModeImRaw.png"))
        enhancer = ImageEnhance.Contrast(self.cvIm)

        imOutput = enhancer.enhance(self.editImageDisplayGUI.contrastVal.value())
        bright = ImageEnhance.Brightness(imOutput)
        imOutput = bright.enhance(self.editImageDisplayGUI.brightnessVal.value())
        sharp = ImageEnhance.Sharpness(imOutput)
        imOutput = sharp.enhance(self.editImageDisplayGUI.sharpnessVal.value())
        imOutput.save(os.path.join("imROIs", "bModeIm.png"))

        self.plotOnCanvas()

    def recordDrawROIClicked(self):
        global cursor
        if self.drawRoiButton.isChecked(): # Set up b-mode to be drawn on
            image, =self.ax.plot([], [], marker="o",markersize=3, markerfacecolor="red")
            self.cid = image.figure.canvas.mpl_connect('button_press_event', self.interpolatePoints)
            cursor.set_active(True)
        else: # No longer let b-mode be drawn on
            image, = self.ax.plot([], [], marker="o", markersize=3, markerfacecolor="red")
            image.figure.canvas.mpl_disconnect(self.cid)
            cursor.set_active(False)
        self.canvas.draw()

    def undoLastPt(self): # When drawing ROI, undo last point plotted
        if len(pointsPlottedX) > 0:
            self.scatteredPoints[-1].remove()
            self.scatteredPoints.pop()
            pointsPlottedX.pop()
            pointsPlottedY.pop()
            if len(pointsPlottedX) > 0:
                global finalSplineX
                global finalSplineY
                oldSpline = self.spline.pop(0)
                oldSpline.remove()
                if len(pointsPlottedX) > 1:
                    finalSplineX, finalSplineY = calculateSpline(pointsPlottedX, pointsPlottedY)
                    self.spline = self.ax.plot(finalSplineX, finalSplineY, color = "cyan", linewidth=0.75)
            self.canvas.draw()
            self.drawRoiButton.setChecked(True)
            self.recordDrawROIClicked()

    def closeInterpolation(self): # Finish drawing ROI
        if len(pointsPlottedX) > 2:
            self.ax.clear()
            im = plt.imread(os.path.join("imROIs", "bModeIm.png"))
            plt.imshow(im, cmap='Greys_r')
            pointsPlottedX.append(pointsPlottedX[0])
            pointsPlottedY.append(pointsPlottedY[0])
            global finalSplineX, finalSplineY, cursor
            finalSplineX, finalSplineY = calculateSpline(pointsPlottedX, pointsPlottedY)
            self.ax.plot(finalSplineX, finalSplineY, color = "cyan", linewidth=0.75)
            image, =self.ax.plot([], [], marker="o",markersize=3, markerfacecolor="red")
            image.figure.canvas.mpl_disconnect(self.cid)
            self.figure.subplots_adjust(left=0,right=1, bottom=0,top=1, hspace=0.2,wspace=0.2)
            plt.tick_params(bottom=False, left=False)
            self.canvas.draw()
            self.ROIDrawn = True
            self.drawRoiButton.setChecked(False)
            self.drawRoiButton.setCheckable(False)
            self.redrawRoiButton.setHidden(False)
            self.closeRoiButton.setHidden(True)
            cursor.set_active(False)
            self.undoLastPtButton.clicked.disconnect()
            self.canvas.draw()

    def restartROI(self): # Remove previously drawn roi and prepare user to draw a new one
        self.ax.clear()
        im = plt.imread(os.path.join("imROIs", "bModeIm.png"))
        plt.imshow(im, cmap='Greys_r')
        global pointsPlottedX, pointsPlottedY, finalSplineX, finalSplineY
        finalSplineX = []
        finalSplineY = []
        pointsPlottedX = []
        pointsPlottedY = []
        self.drawRoiButton.setChecked(False)
        image, = self.ax.plot([], [], marker="o", markersize=3, markerfacecolor="red")
        image.figure.canvas.mpl_disconnect(self.cid)
        self.figure.subplots_adjust(left=0,right=1, bottom=0,top=1, hspace=0.2,wspace=0.2)
        plt.tick_params(bottom=False, left=False)
        self.canvas.draw()
        self.drawRoiButton.setCheckable(True)
        self.closeRoiButton.setHidden(False)
        self.redrawRoiButton.setHidden(True)
        self.undoLastPtButton.clicked.connect(self.undoLastPt)

    def updateBModeSettings(self): # Updates background photo when image settings are modified
        self.cvIm = Image.open(os.path.join("imROIs", "bModeImRaw.png"))
        contrast = ImageEnhance.Contrast(self.cvIm)
        imOutput = contrast.enhance(self.editImageDisplayGUI.contrastVal.value())
        brightness = ImageEnhance.Brightness(imOutput)
        imOutput = brightness.enhance(self.editImageDisplayGUI.brightnessVal.value())
        sharpness = ImageEnhance.Sharpness(imOutput)
        imOutput = sharpness.enhance(self.editImageDisplayGUI.sharpnessVal.value())
        imOutput.save(os.path.join("imROIs", "bModeIm.png"))
        self.plotOnCanvas()
    
    def interpolatePoints(self, event): # Update ROI being drawn using spline using 2D interpolation
        pointsPlottedX.append(int(event.xdata))
        pointsPlottedY.append(int(event.ydata))
        plottedPoints = len(pointsPlottedX)

        if plottedPoints > 1:
            if plottedPoints > 2:
                oldSpline = self.spline.pop(0)
                oldSpline.remove()

            xSpline, ySpline = calculateSpline(pointsPlottedX, pointsPlottedY)
            self.spline = self.ax.plot(xSpline, ySpline, color = "cyan", zorder=1, linewidth=0.75)
            plt.subplots_adjust(left=0,right=1, bottom=0,top=1, hspace=0.2,wspace=0.2)
            plt.tick_params(bottom=False, left=False)
        self.scatteredPoints.append(self.ax.scatter(pointsPlottedX[-1], pointsPlottedY[-1], marker="o", s=0.5, c="red", zorder=500))
        self.canvas.draw()

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