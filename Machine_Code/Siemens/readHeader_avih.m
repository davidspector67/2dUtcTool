function avih = readHeader_avih(fid,FileAsChars)
% avih = readHeader_avih(fid, FileAsChars)

% Copyright Siemens Ultrasound 2003
% Shelby Brunke
% January 30, 2003
%
     TopOfHeader = getFourCCByteLocation(FileAsChars, 'avih');
     fseek(fid,TopOfHeader -1 , 'bof');
     avih.TagName = fscanf(fid,'%c',4); 
     avih.DataSize = fread(fid,1,'uint32');   
     avih.dwMicroSecPerFrame = fread(fid,1,'uint32');
     avih.dwMaxBytesPerSec = fread(fid,1,'uint32');
     avih.Reserved1 = fread(fid,1,'uint32');
     avih.dwFlags = fread(fid,1,'uint32');
     avih.dwTotalFrames = fread(fid,1,'uint32');
     avih.dwInitialFrames = fread(fid,1,'uint32');
     avih.dwStreams = fread(fid, 1, 'uint32');
     avih.dwSuggestedBufferSize = fread(fid,1,'uint32');
     avih.dwWidth = fread(fid,1,'uint32');
     avih.dwHeight = fread(fid, 1, 'uint32');
     avih.dwReserved = fread(fid, 4, 'uint32');
     
     if avih.TagName ~= 'avih'
         warning('AVIH Header Not Read Correctly');
     end
     
     
     
     