function rfdo = readHeader_rfdo(fid,FileAsChars)
% rfdo = readHeader_rfdo(fid, FileAsChars)

% Copyright Siemens Ultrasound 2003
% Shelby Brunke
% January 30, 2003
%

     TopOfHeader = getFourCCByteLocation(FileAsChars, 'rfdo');
     fseek(fid,TopOfHeader -1 , 'bof');
     rfdo.TagName = fscanf(fid,'%c',4); 
     rfdo.DataSize = fread(fid,1,'uint32');   
     rfdo.HeaderVersion = fread(fid,1,'uint32');
     rfdo.FovShape = fread(fid,1,'int32');
     rfdo.GateStartCm = fread(fid,1,'float32');
     rfdo.GateSizeCm = fread(fid,1,'float32');
     rfdo.ApexLateralCm = fread(fid,1,'float32');
     rfdo.ApexVerticalCm = fread(fid,1,'float32');
     rfdo.RoiLateralMin = fread(fid,1,'float32');
     rfdo.SteeringAngleRad = fread(fid,1,'float32');
     rfdo.SampleVolumeWidth = fread(fid,1,'float32');
     rfdo.DopplerType = fread(fid,1,'int32');
     
      if rfdo.TagName ~= 'rfdo'
         warning('RFDO Header Not Read Correctly');
     end