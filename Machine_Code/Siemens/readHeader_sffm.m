function sffm = readHeader_sffm(fid,FileAsChars)
% sffm = readHeader_sffm(fid, FileAsChars)

% Copyright Siemens Ultrasound 2003
% Shelby Brunke
% January 30, 2003
%

     TopOfHeader = getFourCCByteLocation(FileAsChars, 'sffm');
     fseek(fid,TopOfHeader -1 , 'bof');
     sffm.TagName = fscanf(fid,'%c',4); 
     sffm.DataSize = fread(fid,1,'uint32');   
     sffm.SffVersion = fread(fid,1,'uint32');
     sffm.PlatformName = fread(fid,1,'int32');
     sffm.PlatformVersion = fread(fid,1,'int32');
     sffm.OperatingSystem = fread(fid,1,'int32');
     sffm.OperatingSystemVersion = fread(fid,1,'int32');
     sffm.Cpu = fread(fid,1,'int32');
      if sffm.TagName ~= 'sffm'
         warning('SFFM Header Not Read Correctly');
     end
   
     