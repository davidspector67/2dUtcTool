from UtcAnalysis.roiSelection_ui import *
from UtcAnalysis.editImageDisplay_ui_helper import *
from UtcAnalysis.rfAnalysis_ui import *
from Utils.roiFuncs import *

import os
import numpy as np
from PIL import Image, ImageEnhance
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib
import scipy.interpolate as interpolate


roisLeft = []
roisRight = []
roisTop = []
roisBottom = []
mbf = []
ss = []
si = []
minMBF = 0
minSS = 0
minSI = 0
maxMBF = 0
maxSS = 0
maxSI = 0
curDisp = ""
cmap = []
tempROISelected = False
selectedROI = -1
indMBF = None
indSI = None
indSS = None


class RfAnalysisGUI(QWidget, Ui_rfAnalysis):
    def __init__(self, splineX, splineY):
        super().__init__()
        self.setupUi(self)
        self.splineX = splineX
        self.splineY = splineY
        self.imgDataStruct = None
        self.imgInfoStruct = None
        self.refDataStruct = None
        self.refInfoStruct = None

        self.axialWinSize = None
        self.lateralWinSize = None
        self.axialOverlap = None
        self.lateralOverlap = None
        self.threshold = None
        self.minFrequency = None
        self.maxFrequency = None
        self.samplingFreq = None

        self.indMbfVal.setText("")
        self.indSiVal.setText("")
        self.indSsVal.setText("")

        global indMBF, indSS, indSI
        indMBF = self.indMbfVal
        indSS = self.indSsVal
        indSI = self.indSiVal

        # Display B-Mode
        self.horizontalLayout = QHBoxLayout(self.imDisplayFrame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.horizontalLayout.addWidget(self.canvas)
        self.plotOnCanvas()

        self.editImageDisplayGUI = EditImageDisplayGUI()
        self.editImageDisplayButton.clicked.connect(self.openImageEditor)

        self.chooseWindowButton.setCheckable(True)
        self.displayMbfButton.setCheckable(True)
        self.displaySiButton.setCheckable(True)
        self.displaySsButton.setCheckable(True)

        self.displayMbfButton.clicked.connect(self.mbfChecked)
        self.displaySsButton.clicked.connect(self.ssChecked)
        self.displaySiButton.clicked.connect(self.siChecked)
        self.chooseWindowButton.clicked.connect(self.chooseWindow)
        
        # Prepare heatmap legend plot
        self.horizLayoutLeg = QHBoxLayout(self.legend)
        self.horizLayoutLeg.setObjectName("horizLayoutLeg")
        self.figLeg = plt.figure()
        self.canvasLeg = FigureCanvas(self.figLeg)
        self.horizLayoutLeg.addWidget(self.canvasLeg)
        self.canvasLeg.draw()
        

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
        self.imagePathInput.setHidden(False)
        self.phantomPathInput.setHidden(False)
        self.imagePathInput.setText(imageName)
        self.phantomPathInput.setText(phantomName)

    def cleanStructs(self): # Discard windows outside of scan-converted ultrasound image
        splineList = [self.roiWindowSplinesStruct.top, self.roiWindowSplinesStruct.bottom, self.roiWindowSplinesStruct.left, self.roiWindowSplinesStruct.right]
        splineListPreSC = [self.roiWindowSplinesStructPreSC.top, self.roiWindowSplinesStructPreSC.bottom, self.roiWindowSplinesStructPreSC.left, self.roiWindowSplinesStructPreSC.right]
        numWindows = len(splineList[0])
        bottom = None
        left = None
        right = None
        for i in range(numWindows - 1, -1, -1):
            axes = [0, 0, 1, 1]
            vals1 = [splineList[0][i], splineList[1][i], splineList[2][i], splineList[3][i]]
            vals2 = [splineListPreSC[0][i], splineListPreSC[1][i], splineListPreSC[2][i], splineListPreSC[3][i]]
            if not (self.inBounds(vals1, vals2, axes, bottom, left, right)):
                for j in range(4):
                    splineList[j].pop(i)
                    splineListPreSC[j].pop(i)
        self.roiWindowSplinesStruct.top = splineList[0]
        self.roiWindowSplinesStruct.bottom = splineList[1]
        self.roiWindowSplinesStruct.left = splineList[2]
        self.roiWindowSplinesStruct.right = splineList[3]
        self.roiWindowSplinesStructPreSC.top = splineListPreSC[0]
        self.roiWindowSplinesStructPreSC.bottom = splineListPreSC[1]
        self.roiWindowSplinesStructPreSC.left = splineListPreSC[2]
        self.roiWindowSplinesStructPreSC.right = splineListPreSC[3]

    def inBounds(self, vals1, vals2, axes, bottom, left, right):
        if (len(vals2) != len(axes)):
            return False
        for i in range(len(vals2)):
            if not (vals2[i] > 0 and vals2[i] < self.imgDataStruct.rf.shape[axes[i]]):
                return False
        return True
    
    def plotOnCanvas(self): # Plot current image on GUI
        self.figure.clear()
        self.ax = self.figure.add_subplot(111)
        im = plt.imread(os.path.join("imROIs", "bModeIm.png"))
        self.ax.imshow(im, cmap='Greys_r')

        self.ax.plot(self.splineX, self.splineY, color = "cyan", zorder=1, linewidth=0.75)
        self.figure.subplots_adjust(left=0,right=1, bottom=0,top=1, hspace=0.2,wspace=0.2)
        self.cursor = matplotlib.widgets.Cursor(self.ax, color="gold", linewidth=0.4, useblit=True)
        self.cursor.set_active(False)
        plt.tick_params(bottom=False, left=False, labelbottom=False, labelleft=False)
        self.canvas.draw() # Refresh canvas

    def updateBModeSettings(self): # Updates background photo when image settings are modified
        self.cvIm = Image.open(os.path.join("imROIs", "bModeImRaw.png"))
        contrast = ImageEnhance.Contrast(self.cvIm)
        hi = self.editImageDisplayGUI.contrastVal.value()
        imOutput = contrast.enhance(self.editImageDisplayGUI.contrastVal.value())
        brightness = ImageEnhance.Brightness(imOutput)
        hi = self.editImageDisplayGUI.brightnessVal.value()
        imOutput = brightness.enhance(self.editImageDisplayGUI.brightnessVal.value())
        sharpness = ImageEnhance.Sharpness(imOutput)
        hi = self.editImageDisplayGUI.sharpnessVal.value()
        imOutput = sharpness.enhance(self.editImageDisplayGUI.sharpnessVal.value())
        imOutput.save(os.path.join("imROIs", "bModeIm.png"))
        self.plotOnCanvas()

    def mbfChecked(self):
        global curDisp
        if self.displayMbfButton.isChecked():
            if self.displaySsButton.isChecked() or self.displaySiButton.isChecked():
                self.displaySsButton.setChecked(False)
                self.displaySiButton.setChecked(False)
            curDisp = "MBF"
        else:
            curDisp = "clear"
        updateWindows(self.ax)
        self.updateLegend()

    def ssChecked(self):
        global curDisp
        if self.displaySsButton.isChecked():
            if self.displayMbfButton.isChecked() or self.displaySiButton.isChecked():
                self.displayMbfButton.setChecked(False)
                self.displaySiButton.setChecked(False)
            curDisp = "SS"
        else:
            curDisp = "clear"
        updateWindows(self.ax)
        self.updateLegend()

    def siChecked(self):
        global curDisp
        if self.displaySiButton.isChecked():
            if self.displayMbfButton.isChecked() or self.displaySsButton.isChecked():
                self.displayMbfButton.setChecked(False)
                self.displaySsButton.setChecked(False)
            curDisp = "SI"
        else:
            curDisp = "clear"
        updateWindows(self.ax)
        self.updateLegend()

    def computeROIWindows(self): 
        # Compute ROI windows
        # self.roiWindowSplinesStruct, self.roiWindowSplinesStructPreSC = roiWindowsGenerator(finalSplineX, finalSplineY, self.imgDataStruct['scBmode'].size[0], self.imgDataStruct['scBmode'].size[1], self.axialWinSize, self.lateralWinSize, self.imgInfoStruct['axialRes'], self.imgInfoStruct['lateralRes'], self.axialOverlap, self.lateralOverlap, self.threshold, np.asarray(self.imgDataStruct['scRF']['xmap']), np.asarray(self.imgDataStruct['scRF']['ymap']))
        self.roiWindowSplinesStruct, self.roiWindowSplinesStructPreSC = roiWindowsGenerator(self.splineX, self.splineY, self.imgDataStruct.scBmode.shape[0], self.imgDataStruct.scBmode.shape[1], self.axialWinSize, self.lateralWinSize, self.imgInfoStruct.axialRes, self.imgInfoStruct.lateralRes, self.axialOverlap, self.lateralOverlap, self.threshold, self.imgDataStruct.scRF.xmap, self.imgDataStruct.scRF.ymap)
        self.cleanStructs()
        self.ax.plot(self.splineX, self.splineY, color = "cyan", linewidth=0.75) # re-plot drawn ROI

    def displayROIWindows(self):
        self.computeROIWindows()
        if len(self.roiWindowSplinesStruct.left) > 0:
            global roisLeft, roisRight, roisTop, roisBottom
            # Prepare ROI window coordinate arrays for graphing
            # Global variables important for matplotlib functions

            for i in range(len(self.roiWindowSplinesStruct.left)):
                roisLeft.append(self.roiWindowSplinesStruct.left[i])
                roisRight.append(self.roiWindowSplinesStruct.right[i])
                roisTop.append(self.roiWindowSplinesStruct.top[i])
                roisBottom.append(self.roiWindowSplinesStruct.bottom[i])
            self.computeWindowSpec()

            # Populate parameters in av. spectral parameter textbox
            imMBF = str(int(np.average(mbf)*10)/10)
            imSS = str(int(np.average(ss)*100000000)/100)
            imSI = str(int(np.average(si)*10)/10)
            self.avMbfVal.setText("{0}".format(imMBF))
            self.avSsVal.setText("{0}".format(imSS))
            self.avSiVal.setText("{0}".format(imSI))

            updateWindows(self.ax)
            self.updateLegend()
        # else:
            # self.invalidPath.setText("No statistically significant windows have been found in the\ncurrently drawn ROI.")
        self.figure.subplots_adjust(left=0,right=1, bottom=0,top=1, hspace=0.2,wspace=0.2)
        plt.tick_params(bottom=False, left=False)
        self.canvas.draw()

    def computeWindowSpec(self):
        global mbf, ss, si, minMBF, maxMBF, minSS, maxSS, minSI, maxSI
        self.winTopBottomDepth, self.winLeftRightWidth, mbf, ss, si = computeSpecWindows(self.imgDataStruct.rf,self.refDataStruct.rf, self.roiWindowSplinesStructPreSC.top, self.roiWindowSplinesStructPreSC.bottom, self.roiWindowSplinesStructPreSC.left, self.roiWindowSplinesStructPreSC.right, self.minFrequency, self.maxFrequency, self.imgInfoStruct.lowBandFreq, self.imgInfoStruct.upBandFreq, self.samplingFreq)
        minMBF = min(mbf)
        maxMBF = max(mbf)
        minSS = min(ss)
        maxSS = max(ss)
        minSI = min(si)
        maxSI = max(si)

    def updateLegend(self):
        self.figLeg.clear()
        a = np.array([[0,1]])
        self.figLeg = plt.figure()
        if curDisp == "MBF":
            img = plt.imshow(a, cmap='viridis')
            plt.gca().set_visible(False)
            cax = plt.axes([0,0.1,0.35, 0.8])
            # cax = plt.axes([0, 0.1, 0.25, 0.8])
            cbar = plt.colorbar(orientation='vertical', cax=cax)
            plt.text(2.1,0.21,"Midband Fit", rotation = 270, size=9)
            plt.tick_params('y',labelsize=7,pad=0.5)
            # plt.text(3, 0.17, "Midband Fit", rotation=270, size=5) 
            # plt.tick_params('y', labelsize=5, pad=0.7)
            cax.set_yticks([0,0.25, 0.5, 0.75, 1])
            cax.set_yticklabels([int(minMBF*10)/10,int((((maxMBF-minMBF)/4)+minMBF)*10)/10,int((((maxMBF - minMBF)/2)+minMBF)*10)/10,int(((3*(maxMBF-minMBF)/4)+minMBF)*10)/10,int(maxMBF*10)/10])
        elif curDisp == "SS":
            img = plt.imshow(a, cmap='magma')
            plt.gca().set_visible(False)
            cax = plt.axes([0,0.1,0.35,0.8])
            # cax = plt.axes([0, 0.1, 0.25, 0.8])
            cbar = plt.colorbar(orientation='vertical', cax=cax)
            plt.text(2.2,0,"Spectral Slope (1e-6)", rotation = 270, size=6)
            plt.tick_params('y',labelsize=7,pad=0.7)
            # plt.text(3, 0.02, "Spectral Slope (1e-6)", rotation=270, size=4)
            # plt.tick_params('y', labelsize=4, pad=0.3)
            cax.set_yticks([0,0.25, 0.5, 0.75, 1])
            cax.set_yticklabels([int(minSS*100000000)/100,int((((maxSS-minSS)/4)+minSS)*10000000)/100,int((((maxSS - minSS)/2)+minSS)*100000000)/100,int(((3*(maxSS-minSS)/4)+minSS)*100000000)/100,int(maxSS*100000000)/100])
        elif curDisp == "SI":
            img = plt.imshow(a, cmap='plasma')
            plt.gca().set_visible(False)
            cax = plt.axes([0,0.1,0.35,0.8])
            # cax = plt.axes([0, 0.1, 0.25, 0.8])
            cbar = plt.colorbar(orientation='vertical', cax=cax)
            plt.text(2.2, 0.09, 'Spectral Intercept', rotation=270, size = 6)
            plt.tick_params('y', labelsize=7, pad=0.7)
            # plt.text(3, 0, "Spectral Intercept", rotation=270, size=5)
            # plt.tick_params('y', labelsize=5, pad=0.7)
            cax.set_yticks([0,0.25, 0.5, 0.75, 1])
            cax.set_yticklabels([int(minSI*10)/10,int((((maxSI-minSI)/4)+minSI)*10)/10,int((((maxSI - minSI)/2)+minSI)*10)/10,int(((3*(maxSI-minSI)/4)+minSI)*10)/10,int(maxSI*10)/10])
        elif curDisp == "" or curDisp == "clear":
            self.figLeg.set_visible(False)
        self.horizLayoutLeg.removeWidget(self.canvasLeg)
        self.canvasLeg = FigureCanvas(self.figLeg)
        self.horizLayoutLeg.addWidget(self.canvasLeg)
        self.canvasLeg.draw()

    def chooseWindow(self): # select previously computed ROI window to run analysis on
        global tempROISelected
        if self.chooseWindowButton.isChecked():
            image, =self.ax.plot([], [], marker="o",markersize=3, markerfacecolor="red")
            self.cid = image.figure.canvas.mpl_connect('button_press_event', onSelect)
            if (selectedROI != -1):
                tempROISelected = True
                updateWindows(self.ax)
        else:
            image, = self.ax.plot([], [], marker="o", markersize=3, markerfacecolor="red")
            if curDisp != "clear" and curDisp != "" and selectedROI != -1:
                self.ax.patches.pop()
            self.canvas.draw()
            self.indMbfVal.setText("")
            self.indSsVal.setText("")
            self.indSiVal.setText("")
            tempROISelected = False
            image.figure.canvas.mpl_disconnect(self.cid)
    
    
def onSelect(event): # Update ROI window selected after computation
    global curDisp, coloredROI, tempROISelected, selectedROI, indMBF, indSI, indSS
    temp = curDisp
    curDisp = "clear"
    updateWindows(event.inaxes)
    curDisp = temp
    # Find top window selected
    for i in range(len(roisLeft)-1, -1, -1): 
        p = matplotlib.path.Path([(roisLeft[i], roisBottom[i]), (roisLeft[i], roisTop[i]), (roisRight[i], roisTop[i]), (roisRight[i], roisBottom[i])])
        if p.contains_points([(event.xdata, event.ydata)]):
            if curDisp == "MBF":
                coloredROI = matplotlib.patches.Rectangle((roisLeft[i], roisBottom[i]), (roisRight[i]-roisLeft[i]), (roisTop[i]-roisBottom[i]), linewidth=1, fill = True, facecolor=cmap[int((255/(maxMBF-minMBF))*(mbf[i]-minMBF))], edgecolor='white')
            elif curDisp == "SS":
                coloredROI = matplotlib.patches.Rectangle((roisLeft[i], roisBottom[i]), (roisRight[i]-roisLeft[i]), (roisTop[i]-roisBottom[i]), linewidth=1, fill = True, facecolor=cmap[int((255/(maxSS-minSS))*(ss[i]-minSS))], edgecolor='white')
            elif curDisp == "SI":
                coloredROI = matplotlib.patches.Rectangle((roisLeft[i], roisBottom[i]), (roisRight[i]-roisLeft[i]), (roisTop[i]-roisBottom[i]), linewidth=1, fill = True, facecolor=cmap[int((255/(maxSI-minSI))*(si[i]-minSI))], edgecolor='white')
            selectedROI = i
            indMBF.setText("{0}".format(round(mbf[i], 2)))
            indSS.setText("{0}".format(round(ss[i]*1000000, 2)))
            indSI.setText("{0}".format(round(si[i], 2)))
            tempROISelected = True
            break
    
    # Display all ROI windows
    for i in range(len(roisLeft)):
        if curDisp == "MBF":
            if maxMBF == minMBF:
                rect = matplotlib.patches.Rectangle((roisLeft[i], roisBottom[i]), (roisRight[i]-roisLeft[i]), (roisTop[i]-roisBottom[i]), linewidth=1, fill = True, color=cmap[125])
            else:
                rect = matplotlib.patches.Rectangle((roisLeft[i], roisBottom[i]), (roisRight[i]-roisLeft[i]), (roisTop[i]-roisBottom[i]), linewidth=1, fill = True, color=cmap[int((255/(maxMBF-minMBF))*(mbf[i]-minMBF))])
            event.inaxes.add_patch(rect)
        elif curDisp == "SS":
            if maxSS == minSS:
                rect = matplotlib.patches.Rectangle((roisLeft[i], roisBottom[i]), (roisRight[i]-roisLeft[i]), (roisTop[i]-roisBottom[i]), linewidth=1, fill = True, color=cmap[125])
            else:
                rect = matplotlib.patches.Rectangle((roisLeft[i], roisBottom[i]), (roisRight[i]-roisLeft[i]), (roisTop[i]-roisBottom[i]), linewidth=1, fill = True, color=cmap[int((255/(maxSS-minSS))*(ss[i]-minSS))])
            event.inaxes.add_patch(rect)
        elif curDisp == "SI":
            if maxSI == minSI:
                rect = matplotlib.patches.Rectangle((roisLeft[i], roisBottom[i]), (roisRight[i]-roisLeft[i]), (roisTop[i]-roisBottom[i]), linewidth=1, fill = True, color=cmap[125])
            else:
                rect = matplotlib.patches.Rectangle((roisLeft[i], roisBottom[i]), (roisRight[i]-roisLeft[i]), (roisTop[i]-roisBottom[i]), linewidth=1, fill = True, color=cmap[int((255/(maxSI-minSI))*(si[i]-minSI))])
            event.inaxes.add_patch(rect)
    event.inaxes.add_patch(coloredROI)
    event.inaxes.figure.canvas.draw()

def updateWindows(curAx):
    global cmap
    if curDisp == "":
        return
    # Initialize correct spectral parameter heatmap
    if len(curAx.patches) != 0:
        for i in range(len(curAx.patches)):
            curAx.patches.pop()
    if curDisp == "clear":
        curAx.figure.canvas.draw()
        return
    # Prepare correct spectral parameter colormap
    if curDisp == "MBF":
        cmapStruct = plt.get_cmap('viridis')
    elif curDisp == "SS":
        cmapStruct = plt.get_cmap('magma')
    elif curDisp == "SI":
        cmapStruct = plt.get_cmap('plasma')
    cmap = cmapStruct.colors
    for i in range(len(roisLeft)):
        # Create a Rectangle patch (format of bottom-left anchor, width, height)
        if curDisp == "MBF":
            if maxMBF == minMBF:
                rect = matplotlib.patches.Rectangle((roisLeft[i], roisBottom[i]), (roisRight[i]-roisLeft[i]), (roisTop[i]-roisBottom[i]), linewidth=1, fill = True, color=cmap[125])
            else:
                rect = matplotlib.patches.Rectangle((roisLeft[i], roisBottom[i]), (roisRight[i]-roisLeft[i]), (roisTop[i]-roisBottom[i]), linewidth=1, fill = True, color=cmap[int((255/(maxMBF-minMBF))*(mbf[i]-minMBF))])
        elif curDisp == "SS":
            if maxSS == minSS:
                rect = matplotlib.patches.Rectangle((roisLeft[i], roisBottom[i]), (roisRight[i]-roisLeft[i]), (roisTop[i]-roisBottom[i]), linewidth=1, fill = True, color=cmap[125])
            else:
                rect = matplotlib.patches.Rectangle((roisLeft[i], roisBottom[i]), (roisRight[i]-roisLeft[i]), (roisTop[i]-roisBottom[i]), linewidth=1, fill = True, color=cmap[int((255/(maxSS-minSS))*(ss[i]-minSS))])
        elif curDisp == "SI":
            if maxSI == minSI:
                rect = matplotlib.patches.Rectangle((roisLeft[i], roisBottom[i]), (roisRight[i]-roisLeft[i]), (roisTop[i]-roisBottom[i]), linewidth=1, fill = True, color=cmap[125])
            else:
                rect = matplotlib.patches.Rectangle((roisLeft[i], roisBottom[i]), (roisRight[i]-roisLeft[i]), (roisTop[i]-roisBottom[i]), linewidth=1, fill = True, color=cmap[int((255/(maxSI-minSI))*(si[i]-minSI))])
        curAx.add_patch(rect)
    if tempROISelected: # Highlight selected ROI
        global coloredROI
        if curDisp == "MBF":
            if maxMBF == minMBF:
                coloredROI = matplotlib.patches.Rectangle((roisLeft[selectedROI], roisBottom[selectedROI]), (roisRight[selectedROI]-roisLeft[selectedROI]), (roisTop[selectedROI]-roisBottom[selectedROI]), linewidth=1, fill = True, facecolor=cmap[125], edgecolor='white')
            else:
                coloredROI = matplotlib.patches.Rectangle((roisLeft[selectedROI], roisBottom[selectedROI]), (roisRight[selectedROI]-roisLeft[selectedROI]), (roisTop[selectedROI]-roisBottom[selectedROI]), linewidth=1, fill = True, facecolor=cmap[int((255/(maxMBF-minMBF))*(mbf[selectedROI]-minMBF))], edgecolor='white')
        elif curDisp == "SS":
            if maxSS == minSS:
                coloredROI = matplotlib.patches.Rectangle((roisLeft[selectedROI], roisBottom[selectedROI]), (roisRight[selectedROI]-roisLeft[selectedROI]), (roisTop[selectedROI]-roisBottom[selectedROI]), linewidth=1, fill = True, facecolor=cmap[125], edgecolor='white')
            else:
                coloredROI = matplotlib.patches.Rectangle((roisLeft[selectedROI], roisBottom[selectedROI]), (roisRight[selectedROI]-roisLeft[selectedROI]), (roisTop[selectedROI]-roisBottom[selectedROI]), linewidth=1, fill = True, facecolor=cmap[int((255/(maxSS-minSS))*(ss[selectedROI]-minSS))], edgecolor='white')
        elif curDisp == "SI":
            if maxSI == minSI:
                coloredROI = matplotlib.patches.Rectangle((roisLeft[selectedROI], roisBottom[selectedROI]), (roisRight[selectedROI]-roisLeft[selectedROI]), (roisTop[selectedROI]-roisBottom[selectedROI]), linewidth=1, fill = True, facecolor=cmap[125], edgecolor='white')
            else:
                coloredROI = matplotlib.patches.Rectangle((roisLeft[selectedROI], roisBottom[selectedROI]), (roisRight[selectedROI]-roisLeft[selectedROI]), (roisTop[selectedROI]-roisBottom[selectedROI]), linewidth=1, fill = True, facecolor=cmap[int((255/(maxSI-minSI))*(si[selectedROI]-minSI))], edgecolor='white')
        curAx.add_patch(coloredROI)
    curAx.figure.canvas.draw()

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