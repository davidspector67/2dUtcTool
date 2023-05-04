function startOffset = getStartOffset(fid,FileAsChars)
% frh0 = readHeader_frh0(fid, FileAsChars)

% Copyright Siemens Ultrasound 2003
% Shelby Brunke
% April 4, 2003
% 

TopOfHeader = getFourCCByteLocation(FileAsChars, 'movi');
fseek(fid,TopOfHeader -1 , 'bof');
startOffset = ftell(fid);

TagName = fscanf(fid,'%c',4); 

if TagName ~= 'movi'
    warning('Start Offset Location Not Found');
end