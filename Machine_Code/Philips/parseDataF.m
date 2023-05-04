function [lineData, lineHeader] = parseDataF(rawrfdata, headerInfo)
% For use with Fusion RF capture data
%       [lineData, lineHeader] = parseDataF(rawrfdata)
%
% Parses for rf line data
% 
% Input: rawrfdata (32 x N)
%   N = number of 32 bytes clumps
%   32bytes for x64 memory interface
%
%
% Output: lineData
%   Array containing line data
%       Data x XmitEvents
%
% Output: lineHeader
%   Array containing qualifier bits of the line data
%       Qualifiers x XmitEvents
%
%
% Last Modified 5/27/2015 (David Cheung/Joseph Lee)
% Last Modified 04/16/2015 (Scott Dianis)

%% Definitions
minNeg = 2^18;  % Used to convert offset integers to 2's complement

%% Find header clumps
% iHeader pts to the index of the header clump
% Note that each Header is exactly 1 "Clump" long
iHeader = find( bitand(rawrfdata(1,:),1572864) == 524288);
numHeaders = length(iHeader) - 1; % Ignore last header as it part of a partial line

%Get maximun number of samples between consecutive headers
maxNumSamples = 0;
for m = 1:numHeaders
    tempMax = iHeader(m+1) - iHeader(m) - 1;
    
    if (tempMax > maxNumSamples) 
        maxNumSamples = tempMax;
    end
end
numSamples = maxNumSamples * 12;

%% Preallocate arrays
lineData    = zeros(numSamples, numHeaders, 'int32');
lineHeader  = zeros(numSamples, numHeaders, 'uint8');

%% Extract data
for m = 1:numHeaders

    % Get data in between headers
    iStartData  = iHeader(m)+2; %[iHeader(m)+1] is always 0s, so skip
    iStopData   = iHeader(m+1)-1;

    % push pulses not currently supported on Mst, that may change
    % push pulses (DT 0x5a) are very long, and have no valid RX data
    if(headerInfo.Data_Type(m) == hex2dec('5a'))
        % set stop data to a reasonable value to keep file size from
        % blowing up.
        iStopData = iStartData + 10000;
    end
	
    % Get Data for current line and convert to 2's complement values
    lineData_u32    = rawrfdata(1:12,iStartData:iStopData);
    lineData_s32    = int32(bitand(lineData_u32(:,:),524287));
    iNeg            = find(lineData_s32>=minNeg);
    lineData_s32(iNeg) = lineData_s32(iNeg)-2*minNeg;
    lineHeader_u8      = bitshift(bitand(lineData_u32(:,:),1572864),-19);
    
    lineData(1:numel(lineData_s32),m) = lineData_s32(1:numel(lineData_s32));
    lineHeader(1:numel(lineHeader_u8),m) = lineHeader_u8(1:numel(lineHeader_u8));
end;
