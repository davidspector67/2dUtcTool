function rfgi = readHeader_rfgi(fid,FileAsChars)
% rfgi = readHeader_rfgi(fid, FileAsChars)

% Copyright Siemens Ultrasound 2003
% Shelby Brunke
% January 30, 2003
%

     TopOfHeader = getFourCCByteLocation(FileAsChars, 'rfgi');
     fseek(fid,TopOfHeader -1 , 'bof');
     rfgi.TagName = fscanf(fid,'%c',4);
     rfgi.DataSize = fread(fid,1,'uint32');   
     rfgi.HeaderVersion = fread(fid,1,'uint32');
     rfgi.RfAcqGain = fread(fid,1,'int32');
     rfgi.MinDataVectorRange = fread(fid,1,'uint32');
     rfgi.NumFramesAcquired = fread(fid,1,'uint32');
     rfgi.RfAxialMinCm = fread(fid, 1, 'float32');
     rfgi.RfAxialSpanCm = fread(fid, 1, 'float32');
     rfgi.IsBModeInfoFrameDep = fread(fid,1,'uint8');
     rfgi.IsMModeInfoFrameDep = fread(fid,1,'uint8');
     rfgi.IsColorInfoFrameDep = fread(fid,1,'uint8');
     rfgi.IsDopplerInfoFrameDep = fread(fid,1,'uint8');
     rfgi.IsSetDepInfoFrameDep = fread(fid,1,'uint8');
     rfgi.IsBeamDepInfoFrameDep = fread(fid,1,'uint8');
      if rfgi.TagName ~= 'rfgi'
         warning('RFGI Header Not Read Correctly');
     end
     

     