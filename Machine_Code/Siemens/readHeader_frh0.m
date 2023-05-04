function frh0 = readHeader_frh0(fid,FrameNumber,idx1)
% frh0 = readHeader_frh0(fid, FrameNumber, idx1)

% Copyright Siemens Ultrasound 2003
% Shelby Brunke
% January 30, 2003
%
Frh0Size = 22;
fseek(fid, (idx1.Frame(FrameNumber).ChunkOffset ) - Frh0Size + idx1.startOffset, 'bof'); 
frh0.TagName = fscanf(fid,'%c',4);
frh0.DataSize = fread(fid,1,'uint32');
frh0.HeaderVersion = fread(fid,1,'uint32');
frh0.FrameTimeStamp = fread(fid,1,'uint32');
frh0.IsTriggeredFrame = fread(fid,1,'uint8');
frh0.FutureParameter7 = fread(fid,1,'uint32');
frh0.FutureParameter8 = fread(fid,1,'uint8');

if frh0.TagName ~= 'frh0'
    warning('FRH0 Header Not Read Correctly');
end