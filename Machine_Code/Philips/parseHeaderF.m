function HeaderInfo = parseHeaderM(rawrfdata)
% For use with Mustang RF capture data
%       HeaderInfo = parseHeaderM(rawrfdata)
%
% Find header information and store it into a structure.
% 
% Input: rawrfdata (32 x N)
%   N = number of 32 bytes clumps
%   32bytes for x64 memory interface
%
% Output: HeaderInfo
%   Structure containing information from the headers
%
%
% Last Modified 10/28/2013 (David Cheung)
%% Find header clumps
% iHeader pts to the index of the header clump
% Note that each Header is exactly 1 "Clump" long
iHeader = find( bitand(rawrfdata(1,:),1572864) == 524288);
numHeaders = length(iHeader) - 1; % Ignore last header as it part of a partial line

%% Preallocate arrays
RF_CaptureVersion   = zeros(numHeaders, 1, 'uint8');
Tap_Point           = zeros(numHeaders, 1, 'uint8');
Data_Gate           = zeros(numHeaders, 1, 'uint8');
Multilines_Capture  = zeros(numHeaders, 1, 'uint8');
RF_Sample_Rate      = zeros(numHeaders, 1, 'uint8');
Steer               = zeros(numHeaders, 1, 'uint8');
elevationPlaneOffset= zeros(numHeaders, 1, 'uint8');
PM_Index            = zeros(numHeaders, 1, 'uint8');
Line_Index          = zeros(numHeaders, 1, 'uint16');
Pulse_Index         = zeros(numHeaders, 1, 'uint16');
Data_Format         = zeros(numHeaders, 1, 'uint16');
Data_Type           = zeros(numHeaders, 1, 'uint16');
Header_Tag          = zeros(numHeaders, 1, 'uint16');
Threed_Pos          = zeros(numHeaders, 1, 'uint16');
Mode_Info           = zeros(numHeaders, 1, 'uint16');
Frame_ID            = zeros(numHeaders, 1, 'uint32');
CSID                = zeros(numHeaders, 1, 'uint16');
Line_Type           = zeros(numHeaders, 1, 'uint16');
Time_Stamp          = zeros(numHeaders, 1, 'uint32');                   

%% Get Info for Each Header
for m=1:numHeaders,

    packedheader = dec2bin(rawrfdata(13,iHeader(m)),4);
    for i = 12:-1:1
        packedheader = strcat(packedheader, dec2bin(rawrfdata(i,iHeader(m)),21));
    end;
   
    iBit = 2;
    RF_CaptureVersion(m)    = bin2dec(packedheader((iBit+1):(iBit+4)));  iBit = iBit+4;
    Tap_Point(m)            = bin2dec(packedheader((iBit+1):(iBit+3)));  iBit = iBit+3;
    Data_Gate(m)            = bin2dec(packedheader((iBit+1):(iBit+1)));  iBit = iBit+1;
    Multilines_Capture(m)   = bin2dec(packedheader((iBit+1):(iBit+4)));  iBit = iBit+4;
    iBit = iBit+15;         %Waste 15 bits (unused)
    RF_Sample_Rate(m)       = bin2dec(packedheader((iBit+1):(iBit+1)));  iBit = iBit+1;
    Steer(m)                = bin2dec(packedheader((iBit+1):(iBit+6)));  iBit = iBit+6;
    elevationPlaneOffset(m) = bin2dec(packedheader((iBit+1):(iBit+8)));  iBit = iBit+8;
    PM_Index(m)             = bin2dec(packedheader((iBit+1):(iBit+2)));  iBit = iBit+2;
    Line_Index(m)           = bin2dec(packedheader((iBit+1):(iBit+16)));  iBit = iBit+16;
    Pulse_Index(m)          = bin2dec(packedheader((iBit+1):(iBit+16)));  iBit = iBit+16;
    Data_Format(m)          = bin2dec(packedheader((iBit+1):(iBit+16)));  iBit = iBit+16;
    Data_Type(m)            = bin2dec(packedheader((iBit+1):(iBit+16)));  iBit = iBit+16;
    Header_Tag(m)           = bin2dec(packedheader((iBit+1):(iBit+16)));  iBit = iBit+16;
    Threed_Pos(m)           = bin2dec(packedheader((iBit+1):(iBit+16)));  iBit = iBit+16;
    Mode_Info(m)            = bin2dec(packedheader((iBit+1):(iBit+16)));  iBit = iBit+16;
    Frame_ID(m)             = bin2dec(packedheader((iBit+1):(iBit+32)));  iBit = iBit+32;
    CSID(m)                 = bin2dec(packedheader((iBit+1):(iBit+16)));  iBit = iBit+16;
    Line_Type(m)            = bin2dec(packedheader((iBit+1):(iBit+16)));  iBit = iBit+16;
    Time_Stamp(m)           = bin2dec(packedheader([(iBit+1):(iBit+13),(iBit+16):(iBit+34)]));
end;

%% Define the structure
HeaderInfo = struct('RF_CaptureVersion', RF_CaptureVersion, ...
                    'Tap_Point', Tap_Point, ...
                    'Data_Gate', Data_Gate, ...
                    'Multilines_Capture', Multilines_Capture, ...
                    'RF_Sample_Rate', RF_Sample_Rate, ...
                    'Steer', Steer, ...
                    'elevationPlaneOffset', elevationPlaneOffset, ...
                    'PM_Index', PM_Index, ...
                    'Line_Index', Line_Index, ...
                    'Pulse_Index', Pulse_Index, ...
                    'Data_Format', Data_Format, ...
                    'Data_Type', Data_Type, ...
                    'Header_Tag', Header_Tag, ...
                    'Threed_Pos', Threed_Pos, ...
                    'Mode_Info', Mode_Info, ...
                    'Frame_ID', Frame_ID, ...
                    'CSID', CSID, ...
                    'Line_Type', Line_Type, ...
                    'Time_Stamp', Time_Stamp);
