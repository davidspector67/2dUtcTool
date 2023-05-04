function csh0 = readHeader_csh0(fid,FileAsChars)
% csh0 = readHeader_csh0(fid, FileAsChars)

% Copyright Siemens Ultrasound 2003
% Shelby Brunke
% January 30, 2003
%

     TopOfHeader = getFourCCByteLocation(FileAsChars, 'csh0');
     fseek(fid,TopOfHeader - 1, 'bof');
     csh0.TagName = fscanf(fid,'%c',4); %cellstr(fread(fid,4,'char'));
     csh0.DataSize = fread(fid,1,'uint32');   
     csh0.HeaderVersion = fread(fid,1,'uint32');
     csh0.FrameClockAtStartStream = fread(fid,1,'uint32');
     csh0.RequestForDataTimestamp = fread(fid,1,'uint32');
     csh0.NumCustomStreamHeaders = fread(fid,1,'uint32');
     csh0.NumCustomFrameHeaders = fread(fid,1,'uint32');
     csh0.NumFramesInStream = fread(fid,1,'uint32');
     csh0.NumVectorsPerStreamFrame = fread(fid,1,'uint32');
    
      if csh0.TagName ~= 'csh0'
         warning('CSH0 Header Not Read Correctly');
     end