function cfh0 = readHeader_cfh0(fid,FileAsChars)
% cfh0 = readHeader_cfh0(fid, FileAsChars)

% Copyright Siemens Ultrasound 2003
% Shelby Brunke
% January 30, 2003
%

     TopOfHeader = getFourCCByteLocation(FileAsChars, 'cfh0');
     fseek(fid,TopOfHeader - 1, 'bof');
     cfh0.TagName = fscanf(fid,'%c',4); %cellstr(fread(fid,4,'char'));
     cfh0.DataSize = fread(fid,1,'uint32');   
     cfh0.HeaderVersion = fread(fid,1,'uint32');
     cfh0.SequencingMode = fread(fid,1,'int32');
     cfh0.UserName = fscanf(fid,'%c',14);
     cfh0.VersionURI = fread(fid,1,'int32');
     cfh0.VersionURIFileFormat = fread(fid,1,'int32');
     cfh0.VersionRtcFirmware = fread(fid,1,'int32');
     cfh0.VersionSipFirmware = fread(fid,1,'int32');
     cfh0.VersionPciFirmware = fread(fid,1,'int32');
     cfh0.SuppressPatientID = fread(fid,1,'int8');
     
     
     if cfh0.TagName ~= 'cfh0'
         warning('CFH0 Header Not Read Correctly');
     end