%function Info = read_USXinfo(filename,filepath)
function Info = sie_read_PhilipsInfo(filename,filepath)

    addpath(filepath);
    FileHeader = readHeader([filepath filename]);
    
    % Some Initilization
    studyID = filename(1:(length(filename)-4));
    studyEXT = filename((length(filename)-3):end);
    
    % Temp fix - taken from USX probe list. Assuming similar probe to ultrasonix
    %probeStruct = readprobe('probes.xml',header.probe);
    %info.probeStruct = probeStruct;
    %assignin('base', 'header', header);
    
    % Add final parameters to info struct
    info.studyMode = 'RF';
    info.filename = filename;
    info.filepath = filepath;
    info.probe = 'C5-?'; 
    info.system = 'EPIQ7';
    info.studyID = studyID;
    info.studyEXT = studyEXT;
    info.samples = FileHeader.rfbd.NumSamplesPerVector; %size(rf_data_all_fund{1,1}{1},1); csh0.DataSize - maybe rfbd.NumSamplesPerVector - maybe
    info.lines = FileHeader.rfbd.NumVectorsPerFrame; %size(rf_data_all_fund{1,1}{1},1);
    info.depthOffset = 0.04;% probeStruct.transmitoffset;%wrong
    info.depth = 0.16*10^1; %wrong %1275/8; % in mm; from SonixDataTool.m:603 - is it header.dr?
    info.width = (1/FileHeader.rfbm.LineDensity); %wrong %1827/8; %info.probeStruct.pitch*1e-3*info.probeStruct.numElements; % in mm; pitch is distance between elements center to element center in micrometers
    info.rxFrequency = 40000000;
    info.samplingFrequency = 40000000; %was - 20000000 and was FileHeader.strf.SamplingRate
    info.txFrequency = FileHeader.rfsd.TxFrequencyMhz; %3-3.5MHz was - 3200000
    info.centerFrequency = FileHeader.rfsd.TxFrequencyMhz; %3-3.5MHz was -  3200000
    info.targetFOV = 0;
    info.numFocalZones = FileHeader.rfbm.NumFocalZones; %Hardcoded for now - should be readable was 1
    info.numFrames = FileHeader.avih.dwTotalFrames; %NumFrame;  There are 2 frames, and 5 sonoCTangles - not sure how sonoCT angles work. 
    info.frameSize = NaN;
    info.depthAxis = NaN;
    info.widthhAxis = NaN;
    info.lineDensity = FileHeader.rfbm.LineDensity; %multilinefactor; % wrong? rfbm.LineDensity or rfco.LineDensity
    info.height = ((2 * 1500000)/ 40000000) * info.samples; % wrong? - was 500
    info.pitch = 0; % wrong?
    info.dynRange = 55; 
    info.yOffset = 0;
    info.vOffset = 0;
    info.lowBandFreq = 5000000; %4MHz BW - was 1000000
    info.upBandFreq = 15000000; % was 6000000
    info.gain = 0;
    info.rxGain = 0;
    info.userGain = 0;
    info.txPower = 0;
    info.power = 0;
    info.PRF = 0;
    info.TX = FileHeader.rfsd.TxFocusRangeCm;
 
    
    % Philips Specific - may repeat and need clean up
    %tilt1=0; width1=70; startDepth1=0.04; endDepth1=0.16; endHeight = 500; clip_fact = 0.95; dyn_range = 55;
    info.tilt1 = 0;
    info.width1 = 70;
    info.startDepth1 = 0.04;
    info.endDepth1 = 0.16;
    info.endHeight = 500;
    info.clip_fact = 0.95;
    info.dyn_range = 55;
    info.clip_fact = 0.95;
    info.dyn_range = 55;
    info.numSonoCTAngles = 1; %No seimens equivalent of this, just put 1
    

    % One of these is the preSC, the other is postSC resolutions
    info.yResRF = 1;
    info.xResRF = 1;
    info.yRes = 1;
    info.xRes = 1;
    %info.yRes = ((info.samples/info.rxFrequency*1540/2)/info.samples)*10^3; %>> real resolution based on curvature
    %info.yResRF = info.depth/info.samples; %>> fake resolution - simulating linear probe
    %info.xRes = (info.probeStruct.pitch*1e-6*info.probeStruct.numElements/info.lineDensity)*10^3; %>> real resolution based on curvature 
    %info.xResRF = info.width/info.lines; %>> fake resolution - simulating linear probe

    % Quad 2 or accounting for change in line density 
    info.quad2X = 1;
    
    % Read TGC?
    %...

    % Ultrasonix specific - for scan conversion - from: sdk607/MATLAB/SonixDataTools/SonixDataTools.m:719    
    %info.Apitch = (info.samples/info.rxFrequency*1540/2)/info.samples; % Axial pitch - axial pitch - in metres as expected by scanconvert.m
    %info.Lpitch = info.probeStruct.pitch*1e-6*info.probeStruct.numElements/info.lineDensity; % Lateral pitch - lateral pitch - in meters
    %info.Radius = info.probeStruct.radius*1e-6;
    %info.PixelsPerMM = 8; % Number used to interpolate number of pixels to be placed in a mm in image
    %info.lateralRes = 1/info.PixelsPerMM; % Resolution of postSC
    %info.axialRes = 1/info.PixelsPerMM; % Resolution of postSC

    Info = info;
    clearvars -except Info Files analysisParams
end




