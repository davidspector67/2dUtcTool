function rfbm = readHeader_rfbm(fid,FileAsChars)
% rfbm = readHeader_rfbm(fid, FileAsChars)

% Copyright Siemens Ultrasound 2003
% Shelby Brunke
% January 30, 2003
%

     TopOfHeader = getFourCCByteLocation(FileAsChars, 'rfbm');
     fseek(fid,TopOfHeader -1 , 'bof');
     rfbm.TagName = fscanf(fid,'%c',4);
     rfbm.DataSize = fread(fid,1,'uint32');   
     rfbm.HeaderVersion = fread(fid,1,'uint32');
     rfbm.NumFocalZones = fread(fid,1,'int32');
     rfbm.AcousticFrameRateHz = fread(fid,1,'float32');
     rfbm.NumParallelAcquisitions = fread(fid,1,'int32');
     rfbm.FovShape = fread(fid,1,'int32');
     rfbm.ApexLateralCm = fread(fid,1,'float32');
     rfbm.ApexVerticalCm = fread(fid,1,'float32');
     rfbm.DisplayedLateralMin = fread(fid,1,'float32');
     rfbm.DisplayedLateralSpan = fread(fid,1,'float32');
     rfbm.DisplayedAxialMinCm = fread(fid,1,'float32');
     rfbm.DisplayedAxialSpanCm = fread(fid,1,'float32');
     rfbm.SteeringAngleRad = fread(fid,1,'float32');
     rfbm.LineDensity = fread(fid,1,'float32');
     rfbm.PhaseInvertMode = fread(fid,1,'int32');

      if rfbm.TagName ~= 'rfbm'
         warning('RFBM Header Not Read Correctly');
     end
     