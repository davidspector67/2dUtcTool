import numpy as np
import struct
import math
import matplotlib.pyplot as plt
#from PIL import Image
#import matplotlib.patches as patches
#import scipy
#import statistics
import os

import matlab.engine
matlab.engine
eng2 = matlab.engine.start_matlab()
s = eng2.genpath(str(os.getcwd()+'/Machine_Code/Canon'))
eng2.addpath(s, nargout=0)
import random

#from PyQt5.QtGui import QImage

def assigned_area_position(filePath):
    BITS_IN_BYTES = 8
    
    analypos   = 0.3 #axial position [ratio]
    analywidth = 0.3 #lateral width [ratio]
    analyrange = 0.3 #axial width [ratio]
    
    #globalHeader = 7
    globalHeader = 0
    headerSize   = 2 * 8 #64byte converted with 32bit
    
    file = open(filePath, 'rb') #read header
    #in Matlab, hdr is a column vector, which contains the first two 16-bit chunks
    hdr = file.read(4) #2bytes * 2
    numAcquiredRxBeams = int.from_bytes(hdr[0:2], "little", signed="False")
    debugtemp          = int.from_bytes(hdr[2:4], "little", signed="False")
    
    hdr = file.read(4) #2bytes * 2
    debugtemp               = int.from_bytes(hdr[0:2], "little", signed="False") #2 bytes
    numParallelAcquisitions = int.from_bytes(hdr[2:4], "little", signed="False") #2 bytes
    
    hdr = file.read(4) #2bytes * 2
    numSamplesDrOut  = int.from_bytes(hdr[0:2], "little", signed="False") #2 bytes
    numSamplesRbfOut = int.from_bytes(hdr[2:4], "little", signed="False") #2 bytes
    
    hdr = file.read(4) #1byte * 4
    isPhaseInvertEn = hdr[0]
    debugtemp       = hdr[1]
    debugtemp       = hdr[2]
    
    hdr = file.read(20) #4bytes * 5
    decimationFactor       = struct.unpack('f', hdr[0:4])[0]   #4 bytes float
    rbfdecimationFactor    = struct.unpack('f', hdr[4:8])[0]   #4 bytes float
    rbfBeMixerFrequcny     = struct.unpack('f', hdr[8:12])[0]  #4 bytes float
    propagationVelCmPerSec = struct.unpack('f', hdr[12:16])[0] #4 bytes float
    digitizingRateHz       = struct.unpack('f', hdr[16:20])[0] #4 bytes float
    
    file.close()
    
    return [[numSamplesDrOut, numAcquiredRxBeams, headerSize, isPhaseInvertEn, numParallelAcquisitions, filePath],
            [analypos, analyrange, analywidth, numSamplesDrOut, numAcquiredRxBeams, digitizingRateHz, rbfdecimationFactor, rbfBeMixerFrequcny]]

def read_IQ_data(args):
    numSamplesDrOut         = args[0]
    numAcquiredRxBeams      = args[1]
    headerSize              = args[2]
    isPhaseInvertEn         = args[3]
    numParallelAcquisitions = args[4]
    filePath                = args[5]
    
    
    #read IQ data 
    file = open(filePath, 'rb')
    numSamplesIQAcq = numSamplesDrOut * 2
    dataA = np.zeros([numSamplesIQAcq, numAcquiredRxBeams], dtype = int) #idk about datatype
    dataB = np.zeros([numSamplesIQAcq, numAcquiredRxBeams], dtype = int) #idk about datatype
    #alldata = np.zeros([numSamplesIQAcq, numAcquiredRxBeams * (1 + isPhaseInvertEn)], dtype = int) #idk about datatype
    alldata = np.zeros([numSamplesIQAcq + headerSize, numAcquiredRxBeams * (1 + isPhaseInvertEn)], dtype = int) #idk about datatype
    
    #IQ acquisition, following parameter always zero
    isPhaseInvertEn = 0
    isRxFreqCompoundEn = 0
    isDiffplusEn = 0
    
    for i in range(int(numAcquiredRxBeams/numParallelAcquisitions)):
        for j in range(numParallelAcquisitions):
            hdr = file.read(headerSize * 4)
            temp = []
            for k in range (0, len(hdr), 4):
                temp.append(int.from_bytes(hdr[k:k+4], "little", signed="False"))
            alldata[:headerSize, (i-1) * numParallelAcquisitions * (isPhaseInvertEn+1) + j - 1] = temp
            
            dat_bytes = file.read(numSamplesIQAcq * 4)
            dat = []
            for k in range (0, len(dat_bytes), 4):
                temp1 = int.from_bytes(dat_bytes[k:k+4], "little", signed="False")
                temp2 = temp1 - (temp1 >= pow(2, 23)) * pow(2, 24)
                dat.append(temp2)
            
            dataA[:,i * numParallelAcquisitions + j] = dat[:numSamplesDrOut*2]
            
            alldata[headerSize : headerSize+1 + numSamplesDrOut*2-1, 
                    i * numParallelAcquisitions * (isPhaseInvertEn + 1) + j] = dat[:numSamplesDrOut * 2]
        
        if 1 == isPhaseInvertEn:
            for j in range(numParallelAcquisitions):
                hdr = file.read(headerSize * 4)
                dat = file.read(numSamplesIQAcq * 4)
                dat = dat - (dat >= pow(2, 23)) * pow(2, 24)
                
                dataB[:, i * numParallelAcquisitions + j] = dat[1 : numSamplesDrOut * 2]
                alldata[:headerSize, i * numParallelAcquisitions * (isPhaseInvertEn + 1) +
                        numParallelAcquisitions * isPhaseInvertEn + j] = hdr
                alldata[headerSize + 1 : headerSize + 1 + numSamplesDrOut * 2 - 1,
                        i * numParallelAcquisitions * (isPhaseInvertEn + 1) +
                        numParallelAcquisitions * isPhaseInvertEn + j] = dat[:numSamplesDrOut * 2]
    
    file.close()
    
    return [numSamplesDrOut, dataA, dataB]

def plot1(args1, args2):
    numSamplesDrOut = args1[0]
    dataA           = args1[1]
    dataB           = args1[2]
    
    IQ = np.zeros((numSamplesDrOut, dataA.shape[1]), dtype = np.complex128)
    for i in range(numSamplesDrOut):
        IQ[i] = dataA[i * 2] + 1j * dataA[i * 2 + 1]
    
    IQPI = np.zeros((numSamplesDrOut, dataB.shape[1]), dtype = np.complex128)
    for i in range(numSamplesDrOut):
        IQPI[i] = dataB[i * 2] + 1j * dataB[i * 2 + 1]
    
    #Show reconstructed B-image
    logAbsIQ = np.absolute(IQ)
    for i in range(len(IQ)):
        for j in range (len(IQ[i])):
            try:
                logAbsIQ[i][j] = math.log10(logAbsIQ[i][j])
            except:
                print("Exception triggered, likely because the value is 0 but make sure!")
                print("i = %d, j = %d"%(i, j))
                print("logAbsIQ[i][j] = %f"%logAbsIQ[i][j])
    scIQ = eng2.scanConvert(matlab.double(20 * logAbsIQ), matlab.double(70), matlab.double(0), matlab.double(0.04), matlab.double(0.16), matlab.double(500))

    returnList = args2.copy()
    returnList.append(scIQ)
    return scIQ

def plot2_3(my_args):
    my_args = my_args.copy()
    my_args[8] = matlab.double(my_args[8], is_complex=True)
    #for i in range(len(my_args) - 1):
        #my_args[i] = matlab.double(my_args[i])
    eng2.plot2_3(my_args)

def getDriveFiles():
    files = [["001/20220427104128_IQ.bin", "001/20220427104252_IQ.bin", "001/20220427104338_IQ.bin",
              "001/20220427104353_IQ.bin", "001/20220427104410_IQ.bin", "001/20220427104425_IQ.bin",
              "001/20220427104439_IQ.bin", "001/20220427104514_IQ.bin", "001/20220427104541_IQ.bin",
              "001/20220427104609_IQ.bin"],
             ["002/20220429105307_IQ.bin", "002/20220429105324_IQ.bin", "002/20220429105349_IQ.bin",
              "002/20220429105603_IQ.bin", "002/20220429105621_IQ.bin", "002/20220429105639_IQ.bin",
              "002/20220429105722_IQ.bin", "002/20220429105743_IQ.bin", "002/20220429105757_IQ.bin",
              "002/20220429105812_IQ.bin", "002/20220429110000_IQ.bin", "002/20220429110042_IQ.bin",
              "002/20220429110106_IQ.bin", "002/20220429110126_IQ.bin"], 
             ["003/20220503084651_IQ.bin", "003/20220503084712_IQ.bin", "003/20220503084842_IQ.bin",
              "003/20220503084910_IQ.bin", "003/20220503084926_IQ.bin", "003/20220503084946_IQ.bin",
              "003/20220503085050_IQ.bin", "003/20220503085116_IQ.bin", "003/20220503085142_IQ.bin",
              "003/20220503085158_IQ.bin", "003/20220503085226_IQ.bin", "003/20220503085249_IQ.bin"]]
    return files

def main1(currentPath, index="random"): #index is an integer
    if index == "random":
        index = random.randint(0,8)
    if index > 8:
        print("%d is not a valid index"%index)
        return
    files = ["20220110145409_IQ.bin", "20220110145439_IQ.bin", "20220111111831_IQ.bin",
             "20220112095507_IQ.bin", "20220112112149_IQ.bin", "20220112112155_IQ.bin",
             "20220112112305_IQ.bin", "20220112112311_IQ.bin", "20220112112513_IQ.bin"]
    fileName = files[index]
    filePath = currentPath + "500P-2163/" + fileName
    #print("File #%d: %s"%(index, fileName))
    #print("Absolute Path: %s"%filePath)
    args = assigned_area_position(filePath)
    plot1(read_IQ_data(args[0]), args[1])
    #plot2_3(plot1(read_IQ_data(args[0]), args[1]));

def main2(currentPath, patient="random", fileName="random"): #patient is an integer, fileName is a
    files = getDriveFiles()                     #string that includes the patient folder
    filePath = currentPath + "drive-download-20220624T161557Z-001/"
    
    index = 0
    if (fileName == "random"):
        if (patient == "random"):
            patient = random.randint(1,len(files))
        if (patient > len(files)):
            print("00%d is not a patient"%patient)
            return
        
        index = random.randint(0,len(files[patient - 1]) - 1)
        fileName = files[patient - 1][index]
    elif (patient == "random"):
        print("Can't find non-random file for random patient")
        return
    
    filePath += fileName
    
    print("Patient #%d, File #%d: %s"%(patient, index, fileName))
    print("Absolute Path: %s"%filePath)
    args = assigned_area_position(filePath)
    plot2_3(plot1(read_IQ_data(args[0]), args[1]));

def main(fileName):
    #print("Absolute Path: %s"%fileName)
    args = assigned_area_position(fileName)
    return plot1(read_IQ_data(args[0]), args[1])
    #plot2_3(plot1(read_IQ_data(args[0]), args[1]));
