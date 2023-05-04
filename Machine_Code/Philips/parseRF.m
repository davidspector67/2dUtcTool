function rfdata = parseRF(filePath, readOffset, readSize, saveOption)
% Parses RF Capture file (*.rf)
% 
% Syntax
%       rfdata = parseRF()
%       rfdata = parseRF(filePath)
%       rfdata = parseRF(filePath, readOffset)
%       rfdata = parseRF(filePath, readOffset, readSize)
%       rfdata = parseRF(filePath, readOffset, readSize, saveOption)
%
%
% Inputs:
%   filePath    - Path to rf capture file
%   readOffset  - Start read from offset (in MB)
%   readSize    - Amount to be read (in MB)
%   saveOption  - Save parsed data to file '-mat' or '-dat' format
%
% .dat Format Description:
% Stores only echo data (1 word = 4 bytes)
% Read first three words to get file structure:
% |numSamples|multilineFactor|numLines|***data***|eof
%
% The following numSamples amount of words after the first 
% three words is the multiline data for the first line of 
% beam 0. Right after is numSample amount of words for the 
% multiline data for the first line of beam 1. 
% Pattern repeats until it reaches the last beam which is 
% multilineFactor-1. Then the pattern continues for the 
% second line of data for each beam up to numLines.
%
% Returns:
%   Structure containing rf data
%
% rfdata = 
%
%      lineData: Array containing interleaved line data
%           (Data x XmitEvents)
%
%      lineHeader: Array containing qualifier bits of the interleaved line data
%           (Qualifiers x XmitEvents)
%
%      headerInfo: Structure containing information from the headers
%
%      vdbParams: Structure containing VDB parameters from the FEC
%
%      echoData: Array containing echo line data
%           (Depth x ML x XmitEvent)
%
%      colorData: Array containing color line data
%           (Depth x Pkt x ML x Interleave Factor x Groups x Frames)
%
%      pwData: Array containing Doppler line data
%           (Depth x ML x XmitEvent)
%
% Remarks:
%   Recommended to have 12GB of ram when working with a 2GB file or handle
%   in smaller chunks.
%
%
% Last Modified 5/27/2015 (David Cheung/Joseph Lee)
% Last Modified 4/16/2015 (Scott Dianis)
% Last Modified 9/04/2019 (Mona Shrestha)
% Added a check for DataType_ColorTDI to set ML_Actual to multiLineFactorCf;

if nargin < 4
    saveOption = '-mat';
end

rfdata = struct;

if nargin == 0
    [fn, pn] = uigetfile({'*.rf', 'RF Capture File'},'Load RAW RF file');
    if isequal(fn,0) || isequal(pn,0)
       disp('User pressed cancel');
       return
    end
    fn = strcat(pn,fn);
else
    fn = filePath;
end

display(['Opening: ' fn]);
fid = fopen(fn,'rb');
fileinfo = dir(fn);

%% Voyager or Fusion?
VHeader = [ 0; 0; 0; 0; 255; 255; 0; 0; 255; 255; 255; 255; 0; 0; 255; 255; 255; 255; 160; 160 ];
FHeader = [ 0; 0; 0; 0; 255; 255; 0; 0; 255; 255; 255; 255; 0; 0; 255; 255; 255; 255; 11; 11 ];
fileHeaderSize = length(VHeader);

fileHeader = fread(fid,fileHeaderSize,'*uchar');

if isequal(fileHeader, VHeader)
    display('Header information found ...');
    display('Parsing Voyager RF capture file ...');
    isVoyager = 1;
    hasFileHeader = 1;
elseif isequal(fileHeader, FHeader)
    display('Header information found:');
    display('Parsing Fusion RF capture file ...');
    isVoyager = 0;
    hasFileHeader = 1;
else % Legacy V-ACB file
    display('Parsing Voyager RF capture file ...');
    isVoyager = 1;
    hasFileHeader = 0;
    frewind(fid);
end

%% Load RAW RF data
tic

% Read out file header information
if hasFileHeader
    if isVoyager
        endianness = 'b';
    else %isFusion
        endianness = 'l';
    end
    
    [dbParams, numFileHeaderBytes] = parseFileHeader(fid, endianness);
    totalHeaderSize = fileHeaderSize+8+numFileHeaderBytes; % 8 bytes from fileVersion and numFileHeaderBytes
    fseek(fid, totalHeaderSize, 'bof');
else
    dbParams = [];
    totalHeaderSize = 0;
end

if nargin >= 3
    if ischar(readOffset)
        readOffset = str2double(readOffset);
    end
    if ischar(readSize)
        readSize = str2double(readSize);
    end
    readOffset = readOffset * 2^20;
    readSize = readSize * 2^20; 
elseif nargin == 2
    if ischar(readOffset)
        readOffset = str2double(readOffset);
    end
    readOffset = readOffset * 2^20;
    readSize = fileinfo.bytes - totalHeaderSize - readOffset;
else
    readOffset = 0;
    readSize = fileinfo.bytes - totalHeaderSize;
end

if isVoyager
    % Align read offset and size
    alignment = 0:36:(fileinfo.bytes-totalHeaderSize);
    offsetDiff = alignment - readOffset;
    readDiff = alignment - readSize;
    readOffset = alignment(find(offsetDiff >= 0, 1, 'first'));
    readSize = alignment(find(readDiff >= 0, 1, 'first'));
    if isempty(readSize)
        readSize = fileinfo.bytes - totalHeaderSize;
    end
    
    fseek(fid, readOffset, 'cof');    
    % Start reading
    rawrfdata = fread(fid,readSize,'*uchar');
    
else %isFusion
    % Align read offset and size
    alignment = 0:32:(fileinfo.bytes-totalHeaderSize);
    offsetDiff = alignment - readOffset;
    readDiff = alignment - readSize;
    readOffset = alignment(find(offsetDiff >= 0, 1, 'first'));
    readSize = alignment(find(readDiff >= 0, 1, 'first'));
    if isempty(readSize)
        readSize = fileinfo.bytes - totalHeaderSize;
    end
    
    numClumps = floor(readSize/32);%256 bit clumps
    tapPoint = 0;
    if isfield(dbParams, 'tapPoint')
        tapPoint = dbParams.tapPoint;
    end
    
    fseek(fid, readOffset, 'cof');
    if(tapPoint == 7) % For per channel capture, words are are 16bits
        rawrfdata = fread(fid, [16, numClumps], 'uint16'); % 16 16bit words by 256 bit clumps
    else
        % Read first 252 bits of each 256 bit word
        partA = fread(fid, [12, numClumps], '12*ubit21',4);

        % Rewind to beginning of file
        frewind(fid);
        fseek(fid, totalHeaderSize+readOffset, 'cof')

        % Read last 4 bits of each 256 bit word
        partB = fread(fid, [1, numClumps], '1*ubit4', 252);

        % Combine the parts
        rawrfdata = cat(1, partA, partB);
    end
end

fclose(fid);

%% Reshape Raw RF Data
if isVoyager
    numClumps = floor(length(rawrfdata)/36);  % 1 Clump = 12 Samples (1 Sample = 3 bytes)
    
    rlimit = 180000000; % Limit ~172MB for reshape workload, otherwise large memory usuage
    if (length(rawrfdata) > rlimit)
        numChunks = floor(length(rawrfdata)/rlimit);
        numremBytes = mod(length(rawrfdata), rlimit);
        numClumpGroup = rlimit/36;

        temp = cell(numChunks+1,1);
        m = 1;
        n = 1;
        % Reshape array into clumps
        for i = 1:numChunks
            temp{i} = reshape(rawrfdata(m:m+rlimit-1), [3, 12, numClumpGroup]);
            m = m + rlimit;
            n = n + numClumpGroup;
        end
        
        % Handle the remaining bytes
        if (numremBytes > 0)
            temp{numChunks+1} = reshape(rawrfdata(m:numClumps*36), [3, 12, numClumps-n+1]);
        end
        
        % Combine the reshaped arrays
        rawrfdata = cat(3,temp{:});
    else
        % Reshape array into clumps
        rawrfdata = reshape(rawrfdata(1:numClumps*36),[3, 12, numClumps]);
    end
end
toc
%% Parse Header
% Extract header info
display('Parsing header info ...');
if isVoyager
    headerInfo = parseHeaderV(rawrfdata);
else %isFusion
    if tapPoint == 7
        headerInfo = parseHeaderAdcF(rawrfdata);
    else
        headerInfo = parseHeaderF(rawrfdata);
    end
end
toc
%% Parse RF Data
% Extract RF data
display('Parsing RF data ...');
drawnow
Tap_Point = headerInfo.Tap_Point(1);
if isVoyager
    [lineData, lineHeader] = parseDataV(rawrfdata, headerInfo);
else %isFusion
    if Tap_Point == 7 %Post-ADC capture
        [lineData, lineHeader] = parseDataAdcF(rawrfdata, headerInfo);
    else
        [lineData, lineHeader] = parseDataF(rawrfdata, headerInfo);
        Tap_Point = headerInfo.Tap_Point(1);
        if Tap_Point == 0 % Correct for MS 19 bits of 21 real data bits
            %If Matlab complains on the following line, you might need to
            %upgrade your version (e.g. to R2012b) for bitshift() to support
            %[singed int] as an input parameter
            lineData = bitshift(lineData(:,:), 2);
        end
    end
end

toc   
%% Pack Data
rfdata = struct('lineData', lineData, ...
                'lineHeader', lineHeader, ...
                'headerInfo', headerInfo, ...
                'dbParams', dbParams);
%% Free-up Memory
clear rawrfdata;
clear temp;

%% Sort into Data Types
% De-interleave rfdata
display('Organizing based on data type ...');

% see \vgrcommon\inc\acqc\fec\feccommondef.h for definitions
DataType_ECHO = 1:14;
DataType_EchoMMode = 26;

DataType_COLOR = [17 21:24];
DataType_ColorMMode = [27 28];
DataType_ColorTDI = 24;

DataType_CW = 16;
DataType_PW = [18 19];

DataType_Dummy = [20 25 29 30 31];

DataType_SWI = [90 91];

% OCI and phantoms
DataType_Misc = [15 88 89];

if Tap_Point == 7
    ML_Capture = 128;
else
    ML_Capture = double(rfdata.headerInfo.Multilines_Capture(1));
end

if ML_Capture == 0
    SAMPLE_RATE = double(rfdata.headerInfo.RF_Sample_Rate(1));
    if SAMPLE_RATE == 0
        ML_Capture = 16;
    else % 20MHz Capture
        ML_Capture = 32;
    end
end

Tap_Point = rfdata.headerInfo.Tap_Point(1);
if Tap_Point == 7 % Hardware is saving the tap point as 7 and now we convert it back to 4
    Tap_Point = 4;
end
namePoint = { 'PostShepard', 'PostAGNOS', 'PostXBR', 'PostQBP', 'PostADC' };
fprintf('\t%s: \n\t\tCapture_ML:\t%ix\n', ...
            namePoint{Tap_Point+1}, ML_Capture)

xmitEvents = length(rfdata.headerInfo.Data_Type);

%% Find Echo Data
echo_index = false(xmitEvents,1);
for i = 1:length(DataType_ECHO)
    %index = rfdata.headerInfo.Data_Type == DataType_ECHO(i);
    index =  bitand(rfdata.headerInfo.Data_Type,255) == DataType_ECHO(i);
    echo_index = echo_index | index;
end
if (sum(echo_index) > 0)
    %Remove false gate data at the beginning of the line
    if (~strcmp(saveOption,'-dat')) && Tap_Point ~= 4
        echoData = pruneData(rfdata.lineData(:,echo_index),rfdata.lineHeader(:,echo_index),ML_Capture);
    else
        echoData = rfdata.lineData(:,echo_index);
    end
    % pre-XBR Sort
    if (Tap_Point == 0 || Tap_Point == 1)
        ML_Actual = dbParams.azimuthMultilineFactorXbrIn(1) * dbParams.elevationMultilineFactor(1);
        fprintf('\t\tEcho_ML:\t%ix\n', ML_Actual)
        CRE = 1;
        rfdata.echoData = SortRF(echoData, ...
                             ML_Capture, ...
                             ML_Actual, ...
                             CRE,...
                             isVoyager);

    % post-XBR Sort
    elseif (Tap_Point == 2)
        ML_Actual = dbParams.azimuthMultilineFactorXbrOut(1) * dbParams.elevationMultilineFactor(1);
        fprintf('\t\tEcho_ML:\t%ix\n', ML_Actual)
        CRE = dbParams.acqNumActiveScChannels2d(1);
        fprintf('\t\tCRE:\t%i\n', CRE)
        [rfdata.echoData, ...
         rfdata.echoData1,...
         rfdata.echoData2,...
         rfdata.echoData3] = SortRF(echoData, ...
                             ML_Capture, ...
                             ML_Actual, ...
                             CRE,...
                             isVoyager);
    % post-ADC sort
    elseif (Tap_Point == 4)
        ML_Actual = 128;
        fprintf('\t\tEcho_ML:\t%ix\n', ML_Actual)
        CRE = 1;
        rfdata.echoData = SortRF(echoData, ...
                             ML_Actual, ...
                             ML_Actual, ...
                             CRE,...
                             isVoyager);
    else
        warning('Do not know how to sort this data set');
    end
end

%% Find Echo MMode Data
echoMMode_index =   rfdata.headerInfo.Data_Type == DataType_EchoMMode;
if (sum(echoMMode_index) > 0)
    echoMModeData = pruneData(rfdata.lineData(:,echoMMode_index),rfdata.lineHeader(:,echoMMode_index),ML_Capture);
    ML_Actual = 1;
    fprintf('\t\tEchoMMode_ML:\t%ix\n', ML_Actual)
    CRE = 1;
    rfdata.echoMModeData = SortRF(echoMModeData, ...
                             ML_Capture, ...
                             ML_Actual, ...
                             CRE,...
                             isVoyager);

end

%% Find Color Data
color_index = false(xmitEvents,1);
for i = 1:length(DataType_COLOR)
    index =  rfdata.headerInfo.Data_Type == DataType_COLOR(i);
    color_index = color_index | index;
end
if (sum(color_index) > 0)
    colorData = pruneData(rfdata.lineData(:,color_index),rfdata.lineHeader(:,color_index),ML_Capture);
    if ((isfield(dbParams, 'multiLineFactorCf')) & (rfdata.headerInfo.Data_Type(color_index) == DataType_ColorTDI))
            ML_Actual = dbParams.multiLineFactorCf(1);       
    elseif (Tap_Point == 0 || Tap_Point == 1)
        ML_Actual = dbParams.azimuthMultilineFactorXbrInCf(1) * dbParams.elevationMultilineFactorCf(1);
    else
        ML_Actual = dbParams.azimuthMultilineFactorXbrOutCf(1) * dbParams.elevationMultilineFactorCf(1);
    end
    fprintf('\t\tColor_ML:\t%ix\n', ML_Actual)
    CRE = 1;
    rfdata.colorData = SortRF(colorData, ...
                             ML_Capture, ...
                             ML_Actual, ...
                             CRE,...
                             isVoyager);

    pkt  = dbParams.linesPerEnsCf(1);	% flow packet size (ensemble)
    nlv  = dbParams.ensPerSeqCf(1);	% flow interleave factor
    grp  = dbParams.numCfCols(1)/dbParams.ensPerSeqCf(1);	% flow interleave groups per frame
    depth = size(rfdata.colorData,1);
    
    % Extract and rearrange flow RF data.
    frm = floor( size( rfdata.colorData, 3 ) / ( nlv * pkt * grp ) ); % whole frames
    if (frm == 0)
        warning('Cannot fully parse color data. RF capture does not contain at least one whole color frame.');
        frm = 1;
        grp = floor( size( rfdata.colorData, 3 ) / ( nlv * pkt ) ); % whole groups
    end 
    rfdata.colorData = rfdata.colorData( :, :, 1 : pkt * nlv * grp * frm );
    rfdata.colorData = reshape( rfdata.colorData, [ depth, ML_Actual, nlv, pkt, grp, frm ] );
    rfdata.colorData = permute( rfdata.colorData, [ 1, 4, 2, 3, 5, 6 ] ); % Depth x Packet x Multiline x Interleave Factor x Groups x Frames
    % Final Reshape - Depth x Packet x Receive Lines in Frame x Frames
    %rfdata.colorData = reshape( rfdata.colorData, [ depth, pkt, ML_Actual * nlv * grp, frm ] );
end

%% Find Color MMode Data
colorMMode_index = false(xmitEvents,1);
for i = 1:length(DataType_ColorMMode)
    index =  rfdata.headerInfo.Data_Type == DataType_ColorMMode(i);
    colorMMode_index = colorMMode_index | index;
end
if (sum(colorMMode_index) > 0)
    colorMModeData = pruneData(rfdata.lineData(:,colorMMode_index),rfdata.lineHeader(:,colorMMode_index),ML_Capture);
    ML_Actual = 1;
    CRE = 1;
    rfdata.colorMModeData = SortRF(colorMModeData, ...
                             ML_Capture, ...
                             ML_Actual, ...
                             CRE,...
                             isVoyager);

end

%% Find CW Doppler Data
cw_index = false(xmitEvents,1);
for i = 1:length(DataType_CW)
    index =  rfdata.headerInfo.Data_Type == DataType_CW(i);
    cw_index = cw_index | index;
end
if (sum(cw_index) > 0)
    cwData = pruneData(rfdata.lineData(:,cw_index),rfdata.lineHeader(:,cw_index),ML_Capture);
    ML_Actual = 1;
    CRE = 1;
    rfdata.cwData = SortRF(cwData, ...
                             ML_Capture, ...
                             ML_Actual, ...
                             CRE,...
                             isVoyager);

end

%% Find PW Doppler Data
pw_index = false(xmitEvents,1);
for i = 1:length(DataType_PW)
    index =  rfdata.headerInfo.Data_Type == DataType_PW(i);
    pw_index = pw_index | index;
end
if (sum(pw_index) > 0)
    pwData = pruneData(rfdata.lineData(:,pw_index),rfdata.lineHeader(:,pw_index),ML_Capture);
    ML_Actual = 1;
    CRE = 1;
    rfdata.pwData = SortRF(pwData, ...
                             ML_Capture, ...
                             ML_Actual, ...
                             CRE,...
                             isVoyager);

end

%% Find Dummy Data
dummy_index = zeros(xmitEvents,1);
for i = 1:length(DataType_Dummy)
    index =  rfdata.headerInfo.Data_Type == DataType_Dummy(i);
    dummy_index = dummy_index | index;
end
if (sum(dummy_index) > 0)
    dummyData = pruneData(rfdata.lineData(:,dummy_index),rfdata.lineHeader(:,dummy_index),ML_Capture);
    ML_Actual = 2;
    CRE = 1;
    rfdata.dummyData = SortRF(dummyData, ...
                             ML_Capture, ...
                             ML_Actual, ...
                             CRE,...
                             isVoyager);

end

%% Find Shearwave Data
swi_index = false(xmitEvents,1);
for i = 1:length(DataType_SWI)
    index =  rfdata.headerInfo.Data_Type == DataType_SWI(i);
    swi_index = swi_index | index;
end
if (sum(swi_index) > 0)
    swiData = pruneData(rfdata.lineData(:,swi_index),rfdata.lineHeader(:,swi_index),ML_Capture);
    ML_Actual = ML_Capture;
    CRE = 1;
    rfdata.swiData = SortRF(swiData, ...
                             ML_Capture, ...
                             ML_Actual, ...
                             CRE,...
                             isVoyager);
end

%% Find Misc Data
misc_index = false(xmitEvents,1);
for i = 1:length(DataType_Misc)
    index =  rfdata.headerInfo.Data_Type == DataType_Misc(i);
    misc_index = misc_index | index;
end
if (sum(misc_index) > 0)
    miscData = pruneData(rfdata.lineData(:,misc_index),rfdata.lineHeader(:,misc_index),ML_Capture);
    ML_Actual = ML_Capture;
    CRE = 1;
    rfdata.miscData = SortRF(miscData, ...
                             ML_Capture, ...
                             ML_Actual, ...
                             CRE,...
                             isVoyager);

end

toc

%% Clean up empty fields in struct
elements = fieldnames(rfdata);
count = 1;
removal = {};
for i = 1:numel(elements)
    if isempty(rfdata.(elements{i}))
        removal{count} = elements{i}; %#ok<AGROW>
        count = count + 1;
    end
end
rfdata = rmfield(rfdata, removal);
%% Save?
if nargin == 4
   switch saveOption
       case '-mat'
           display('Saving rfdata into .mat file');
           file = strrep(fn,'.rf','.mat');
           save(file,'rfdata');
       case '-dat'
           if isfield(rfdata, 'echoData')
               display('Outputing to .dat format');
               file = strrep(fn,'.rf','.dat');
               fid = fopen(file, 'w');

               numSamples = size(rfdata.echoData,1);
               multilineFactor = size(rfdata.echoData,2);
               numLines = size(rfdata.echoData,3);
               fprintf('\tnumSamples: %u\n\tmultilineFactor: %u\n\tnumLines: %u\n', ... 
                   numSamples,multilineFactor,numLines);

               fwrite(fid, numSamples, 'int32');
               fwrite(fid, multilineFactor, 'int32');
               fwrite(fid, numLines, 'int32');
               fwrite(fid, rfdata.echoData(:), 'int32');
               fclose(fid);
           end
           if isfield(rfdata, 'echoData3')
               display('Outputing to .dat format');
               file = strrep(fn,'.rf','_CRE3.dat');
               fid = fopen(file, 'w');

               numSamples = size(rfdata.echoData3,1);
               multilineFactor = size(rfdata.echoData3,2);
               numLines = size(rfdata.echoData3,3);
               fprintf('\tnumSamples: %u\n\tmultilineFactor: %u\n\tnumLines: %u\n', ... 
                   numSamples,multilineFactor,numLines);

               fwrite(fid, numSamples, 'int32');
               fwrite(fid, multilineFactor, 'int32');
               fwrite(fid, numLines, 'int32');
               fwrite(fid, rfdata.echoData3, 'int32');
               fclose(fid);
           end
   end
   toc
end
%% Done
display('Done');
