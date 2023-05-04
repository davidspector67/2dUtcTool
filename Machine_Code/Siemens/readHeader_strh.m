function strh = readHeader_strh(fid,FileAsChars)
% strh = readHeader_strh(fid, FileAsChars)

% Copyright Siemens Ultrasound 2003
% Shelby Brunke
% January 30, 2003
%

     TopOfHeader = getFourCCByteLocation(FileAsChars, 'strh');
     fseek(fid,TopOfHeader - 1, 'bof');
     strh.TagName = fscanf(fid,'%c',4); 
     strh.DataSize = fread(fid,1,'uint32');   
     strh.fccType = fscanf(fid,'%c',4);
     strh.fccHandler = fscanf(fid,'%c',4);
     strh.dwFlags = fread(fid,1,'uint32');
     strh.dwPriority = fread(fid,1,'uint32');
     strh.dwInitialFrames = fread(fid,1,'uint32');
     strh.dwScale = fread(fid,1,'uint32');
     strh.dwRate = fread(fid,1,'uint32');
     strh.dwStart = fread(fid,1,'uint32');
     strh.dwLength = fread(fid,1,'uint32');
     strh.dwSuggestedBufferSize = fread(fid,1,'uint32');
     strh.Quality = fread(fid,1,'uint32');
     strh.dwSampleSize = fread(fid,1,'uint32');
     strh.rcFrame.bottom = fread(fid,1,'uint32');
     strh.rcFrame.left = fread(fid,1,'uint32');
     strh.rcFrame.right = fread(fid,1,'uint32');
     strh.rcFrame.top = fread(fid,1,'uint32');
 if strh.TagName ~= 'strh'
         warning('STRH Header Not Read Correctly');
     end


