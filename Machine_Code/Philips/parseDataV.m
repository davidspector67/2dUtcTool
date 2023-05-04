function [lineData, lineHeader] = parseDataV(rawrfdata, headerInfo)
% For use with Voyager RF capture data
%       [lineData, lineHeader] = parseDataV(rawrfdata)
%
% Parses for rf line data
% 
% Input: rawrfdata (3 x 12 x N)
%   N = number of 36 bytes clumps
%   12 samples of 3 byte each
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
% Last Modified 7/9/2014 (David Cheung / Scott Dianis)
% Last Modified 4/16/2015 (Scott Dianis)

%% Definitions
minNeg = 16*2^16;  % Used to convert offset integers to 2's complement

%% Find header clumps
% iHeader pts to the index of the header clump
% Note that each Header is exactly 1 "Clump" long
iHeader = find(bitand(rawrfdata(3,1,:),224) == 64);
numHeaders = length(iHeader) - 1; % Ignore last header as it part of a partial line
numSamples = (iHeader(2) - iHeader(1) - 1) * 12;

%% Preallocate arrays
lineData    = zeros(numSamples, numHeaders, 'int32');
lineHeader  = zeros(numSamples, numHeaders, 'uint8');

%% Extract data
for m = 1:numHeaders

    % Get data inbetween headers
    iStartData  = iHeader(m)+1;
    iStopData   = iHeader(m+1)-1;

    % push pulses (DT 0x5a) are very long, and have no valid RX data
    if(headerInfo.Data_Type(m) == hex2dec('5a'))
        % set stop data to a reasonable value to keep file size from
        % blowing up.
        iStopData = iStartData + 10000;
    end

    % Get Data for current line and convert to 2's complement values
    lineData_u8     = rawrfdata(:,:,iStartData:iStopData);
    lineData_s32    = int32(lineData_u8(1,:,:)) + int32(lineData_u8(2,:,:))*2^8 + int32(bitand(lineData_u8(3,:,:),uint8(31)))*2^16;
    iNeg            = find(lineData_s32>=minNeg);
    lineData_s32(iNeg) = lineData_s32(iNeg)-2*minNeg;
    lineHeader_u8      = bitshift(bitand(lineData_u8(3,:,:),224),-6);
    
    lineData(1:numel(lineData_s32),m) = lineData_s32(1:numel(lineData_s32));
    lineHeader(1:numel(lineHeader_u8),m) = lineHeader_u8(1:numel(lineHeader_u8));
end;
