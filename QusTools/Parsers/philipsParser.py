from scipy.io import loadmat
from scipy.signal import hilbert
from scipy.interpolate import RectBivariateSpline
import numpy as np
from numpy.matlib import repmat

class AnalysisParamsStruct():
    def __init__(self, frame):
        self.frame = frame
        self.t_tilt= 0
        self.t_width = 70
        self.startDepth = 0.04
        self.endDepth = 0.16
        self.endHeight = 500
        self.clip_fact = 0.95
        self.dyn_range = 55
        self.depth = 0.16
        self.width = 0.265

class FileStruct():
    def __init__(self, filedirectory, filename):
        self.name = filename
        self.directory = filedirectory

class OutImStruct():
    def __init__(self):
        self.data = None
        self.orig = None
        self.xmap = None
        self.ymap = None

class DataOutputStruct():
    def __init__(self):
        self.scRF = None
        self.scBmode = None
        self.rf = None
        self.bMode = None

class InfoStruct():
    def __init__(self):
        self.studyMode = None
        self.filename = None
        self.filepath = None
        self.probe = None
        self.system = None
        self.studyID = None
        self.studyEXT = None
        self.samples = None
        self.lines = None
        self.depthOffset = None
        self.depth = None
        self.width = None
        self.rxFrequency = None
        self.samplingFrequency = None
        self.txFrequency = None
        self.centerFrequency = None
        self.targetFOV = None
        self.numFocalZones = None
        self.numFrames = None
        self.frameSize = None
        self.depthAxis = None
        self.widthAxis = None
        self.lineDensity = None
        self.height = None
        self.pitch = None
        self.dynRange = None
        self.yOffset = None
        self.xOffset = None
        self.lowBandFreq = None
        self.upBandFreq = None
        self.gain = None
        self.rxGain = None
        self.userGain = None
        self.txPower = None
        self.power = None
        self.PRF = None
        self.width = None
        self.lateralRes = None
        self.axialRes = None
        self.maxval = None

        # Philips Specific - may repeat and need clean up
        self.tilt1 = None
        self.width1 = None
        self.startDepth1 = None
        self.endDepth1 = None
        self.endHeight = None
        self.clip_fact = None
        self.dyn_range = None
        self.numSonoCTAngles = None

        # One if preSC, the other is postSC resolutions
        self.yResRF = None 
        self.xResRF = None
        self.yRes = None
        self.xRes = None

        # Quad 2 or accounting for change in line density
        self.quad2x = None



def getImage(filename, filedirectory, refname, refdirectory, frame):
    AnalysisParams = AnalysisParamsStruct(frame)
    Files = FileStruct(filedirectory, filename)
    RefFiles = FileStruct(refdirectory, refname)

    [ImgInfo, RefInfo, ImgData, RefData] = getData(Files, RefFiles, AnalysisParams)
    
    return ImgData.scBmode, ImgData, ImgInfo, RefData, RefInfo



def getData(Files, RefFiles, AnalysisParams):
    input = loadmat(str(Files.directory + Files.name))
    ImgInfo = readFileInfo(Files.name, Files.directory, input)
    [ImgData, ImgInfo] = readFileImg(ImgInfo, AnalysisParams.frame, input)

    input = loadmat(str(RefFiles.directory + RefFiles.name))
    RefInfo = readFileInfo(RefFiles.name, RefFiles.directory, input)
    [RefData, RefInfo] = readFileImg(RefInfo, AnalysisParams.frame, input)

    return [ImgInfo, RefInfo, ImgData, RefData]

def readFileInfo(filename, filepath, input):
    if filename[-4:] == ".mat":        
        studyID = filename[:-4]
        studyEXT = filename[-4:]

        Info = InfoStruct()
        Info.studyMode = "RF"
        Info.filename = filename
        Info.filepath = filepath
        Info.probe = "C5-?"
        Info.system = "EPIQ7"
        Info.studyID = studyID
        Info.studyEXT = studyEXT
        Info.samples = input["pt"][0]
        Info.lines = np.array(input["rf_data_all_fund"][0][0][0][0]).shape[0]
        Info.depthOffset = 0.04 # probeStruct.transmitoffset
        Info.depth = 0.16 #?
        Info.width = 70 #?
        Info.rxFrequency = 20000000
        Info.samplingFrequency = 20000000
        Info.txFrequency = 3200000
        Info.centerFrequency = 3200000
        Info.targetFOV = 0
        Info.numFocalZones = 1
        Info.numFrames = input["NumFrame"][0]
        Info.frameSize = np.nan
        Info.depthAxis = np.nan
        Info.widthAxis = np.nan
        Info.lineDensity = input["multilinefactor"][0]
        Info.height = 500
        Info.pitch = 0
        Info.dynRange = 55
        Info.yOffset = 0
        Info.xOffset = 0
        Info.lowBandFreq = 1000000
        Info.upBandFreq = 6000000
        Info.gain = 0
        Info.rxGain = 0
        Info.userGain = 0
        Info.txPower = 0
        Info.power = 0
        Info.PRF = 0

        # Philips Specific
        Info.tilt1 = 0
        Info.width1 = 70
        Info.startDepth1 = 0.04
        Info.endDepth1 = 0.16
        Info.endHeight = 500
        Info.clip_fact = 0.95
        Info.numSonoCTAngles = input["NumSonoCTAngles"][0]
        
        Info.yResRF = 1
        Info.xResRF = 1
        Info.yRes = 1
        Info.xRes = 1
        Info.quad2x = 1

        return Info

def readFileImg(Info, frame, input):
    if Info.filename[-4:] == '.mat':
        slice = 1
        echoData = input["rf_data_all_fund"][0][0][0][frame]

        transformed = abs(hilbert(echoData[:,0]))
        bmode = np.zeros(echoData.shape)

        # Do Hilbert Transform on each column
        for i in range(echoData.shape[1]):
            bmode[:,i] = 20*np.log10(abs(hilbert(echoData[:,i])))

        ModeIM = echoData

        [scBmode, hCm1, wCm1, _] = scanConvert(bmode, Info.width1, Info.tilt1, Info.startDepth1, Info.endDepth1, Info.endHeight)
        # TODO: Left off here (line 23, philips_read_PhilipsImg.m). Was not able to check final outim, inIm_ind(x/y). If something's off, look here
        [_, hCm1, wCm1, scModeIM] = scanConvert(ModeIM, Info.width1, Info.tilt1, Info.startDepth1, Info.endDepth1, Info.endHeight)

        Info.height = hCm1
        Info.width = wCm1
        Info.lateralRes = wCm1*10/scBmode.shape[1]
        Info.axialRes = hCm1*10/scBmode.shape[0]
        Info.maxval = np.amax(scBmode)

        Data = DataOutputStruct()
        Data.scRF = scModeIM
        Data.scBmode = scBmode
        Data.rf = ModeIM
        Data.bMode = bmode

        return Data, Info



def scanConvert(inIm, width, tilt, startDepth, endDepth, desiredHeight=500):
    # ScanConvert sector image
    # Inputs:
    #      InIm          Input image
    #      Width         Sector width of input image in degrees 
    #      Tilt          Tilt of sector image in degrees  
    #      StartDepth    Axial depth of first sample in meters 
    #      EndDepth      Axial depth of last sample in meters   
    #      DesiredHeight Desired vertical size of output image in pixels 
    #      (default 500)
    # 
    #    Outputs:
    #      OutIm         Output (scanconverted) image(s)  
    #      HCm,WCm       Height and Width of image in centimeters 

    #Convert to radians
    width = width*np.pi/180
    tilt = tilt*np.pi/180

    frames = 1
    [samples, beams] = inIm.shape
    depthIncrement = (endDepth-startDepth)/(samples - 1)
    startAngle = 3*np.pi/2 + tilt - width/2
    angleIncrement = width/(beams+1)

    outIm = inIm
    transpose = 0
    background = 0
    height = desiredHeight
    width = 0

    # Set size of image if not defined
    stopAngle = startAngle+((beams-1)*angleIncrement)
    stopDepth = startDepth+((samples-1)*depthIncrement)
    angleRange = np.arange(startAngle, stopAngle+angleIncrement, angleIncrement)

    xmin = -1*max(np.cos((startAngle%np.pi))*np.array([startDepth, stopDepth]))
    xmax = -1*min(np.cos((stopAngle%np.pi))*np.array([startDepth, stopDepth]))
    ymin = min(np.sin((angleRange%np.pi))*startDepth)
    ymax = max(np.sin((angleRange%np.pi))*stopDepth)
    widthScale = abs((xmax-xmin)/(ymax-ymin))

    if not width:
        width = int(np.ceil(height*widthScale))
    
    # Interpolate Image
    radI = 1
    latI = 1
    radSize = samples
    latSize = beams
    if radI > 1 or latI > 1:
        # WARNING: this code has not been tested and may not work. It's not needed for current project
        x = np.array(list(range(radSize)))
        y = np.array(list(range(latSize)))
        xi = np.array(list(range(0, radSize, 1/radI)))
        yi = np.array(list(range(0, latSize, 1/latI)))

        if transpose:
            nyIm = np.zeros((len(yi), len(xi), frames))
        else:
            nyIm = np.zeros((len(xi), len(yi), frames))

        for i in range(frames):
            if transpose:
                nyIm[:,:,i] = RectBivariateSpline(x, y, np.double(outIm[:,:,i])).ev(xi, yi)
            else:
                nyIm[:,:,i] = RectBivariateSpline(y, x, np.double(outIm[:,:,i])).ev(yi, xi)

        outIm = nyIm
    
    nr = (samples+((samples-1)*(radI-1)))
    nb = (beams+((beams-1)*(latI-1)))
    t0 = startAngle
    dt = angleIncrement*(beams)/(nb)
    r0 = startDepth
    dr = depthIncrement*(samples)/(nr)
    nbF = nb
    nrF = nr
    t0F = t0
    dtF = dt
    r0F = r0
    drF = dr

    # Subtract 180 degrees to get transudcer in top of image if startAngle > pi
    t0 = t0 % np.pi
    t0F = t0F % np.pi

    # Define physical limits of image
    stopAngle = t0 + (nb*dt)
    stopDepth = r0 + (nr*dr)
    angleRange = np.arange(t0, stopAngle+dt, dt)
    y0 = min(r0*np.sin(angleRange))
    ymax = max(stopDepth*np.sin(angleRange))
    x0 = min([-1*stopDepth*np.cos(t0), -1*startDepth*np.cos(t0)])
    xmax = max(-1*startDepth*np.cos(stopAngle), -1*stopDepth*np.cos(stopAngle))

    heightCm = (ymax-y0)*100
    widthCm = (xmax-x0)*100

    # Make (x,y)-plane representation of physical image
    xmat = (np.transpose(np.ones((1, height)))*np.arange(0, width, 1))/(width-1)
    ymat = (np.transpose(np.arange(0, height, 1).reshape((1, height)))*np.ones((1, width)))/(height-1)
    xmat = (xmat*(xmax-x0)) + x0
    ymat = (ymat*(ymax-y0)) + y0

    # Transform into polar coordinates (angle, range)
    anglemat = np.arctan2(ymat, -1*xmat)
    rmat = np.sqrt((xmat**2) + (ymat**2))

    # Convert phys. angle and range into beam and sample
    anglemat = np.ceil((anglemat - t0F)/dtF)
    rmat = np.ceil((rmat - r0F)/drF)

    # Find pixels outside active sector
    backgr = np.argwhere((rmat<1))
    backgr = np.concatenate((backgr, np.argwhere(rmat>=nrF)), axis=0)
    backgr = np.concatenate((backgr, np.argwhere(anglemat<1)), axis=0)
    backgr = np.concatenate((backgr, np.argwhere(anglemat>nbF)), axis=0)
    if transpose:
        scMap = (rmat-1)*nbF + anglemat
    else:
        scMap = (anglemat-1)*nrF + rmat

    # Mapping system added to Matlab by Ahmed El Kaffas - April 1st, 2019
    for i in range(backgr.shape[0]):
        scMap[backgr[i,0],backgr[i,1]] = (nbF*nrF)+1
    if np.amax(scMap)<((nbF*nrF)+1):
        scMap[0] = (nbF*nrF)+1
    # inIm_indy = np.zeros(outIm.shape)
    inIm_indx = repmat(np.arange(0, outIm.shape[1]), int(outIm.shape[0]), 1) # <-- maps (y,x) in Iin to indt in Iin
    inIm_indy = np.transpose(repmat(np.arange(0, outIm.shape[0]), int(outIm.shape[1]), 1)) # <-- maps (y,x) in Iout to indr in Iin

    if frames > 1:
        # WARNING: Not tested yet
        scIm = np.zeros((height, width, frames))
        for i in range(frames):
            out = outIm[:,:,i]
            out = np.append(out, background) #?
            scIm[:,:,i] = out[scMap]
        outIm = scIm
    else:
        outIm = np.append(np.transpose(outIm), background)
        inIm_indy = np.append(np.transpose(inIm_indy), background)
        inIm_indx = np.append(np.transpose(inIm_indx), background)

        scMap = np.array(scMap).astype(np.uint64) - 1
        outIm = outIm[scMap]
        inIm_indy = inIm_indy[scMap]
        inIm_indx = inIm_indx[scMap]

        outIm = np.reshape(outIm, (height, width))
        inIm_indy = np.reshape(inIm_indy, (height, width))
        inIm_indx = np.reshape(inIm_indx, (height, width))
    
    hCm = heightCm
    wCm = widthCm
    
    OutIm = OutImStruct()
    OutIm.data = outIm
    OutIm.orig = inIm
    OutIm.ymap = inIm_indy
    OutIm.xmap = inIm_indx
    return outIm, hCm, wCm, OutIm

if __name__ == "__main__":
    getImage('FatQuantData1.mat', '/Users/davidspector/Documents/MATLAB/Data/', 'FatQuantPhantom1.mat', '/Users/davidspector/Documents/MATLAB/Data/', 0)