function rfco = readHeader_rfco(fid,FileAsChars)
% rfco = readHeader_rfco(fid, FileAsChars)

% Copyright Siemens Ultrasound 2003
% Shelby Brunke
% January 30, 2003
%

     TopOfHeader = getFourCCByteLocation(FileAsChars, 'rfco');
     fseek(fid,TopOfHeader -1 , 'bof');
     rfco.TagName = fscanf(fid,'%c',4); 
     rfco.DataSize = fread(fid,1,'uint32');   
     rfco.HeaderVersion = fread(fid,1,'uint32');
     rfco.AcousticFrameRateHz = fread(fid,1,'float32');
     rfco.NumParallelAcquisitions = fread(fid,1,'int32');
     rfco.FovShape = fread(fid,1,'int32');
     rfco.ApexLateralCm = fread(fid,1,'float32');
     rfco.ApexVerticalCm = fread(fid,1,'float32');
     rfco.DisplayedLateralMin = fread(fid,1,'float32');
     rfco.DisplayedLateralSpan = fread(fid,1,'float32');
     rfco.DisplayedAxialMinCm = fread(fid,1,'float32');
     rfco.DisplayedAxialSpanCm = fread(fid,1,'float32');
     rfco.SteeringAngleRad = fread(fid,1,'float32');
     rfco.LineDensity = fread(fid,1,'float32');
     rfco.InterleaveFactor = fread(fid,1,'int32');
     rfco.AlternateInterleaveFactor = fread(fid,1,'int32');
     rfco.IsFrameInterleaveEn = fread(fid,1,'uint8');
     rfco.EnsembleSize = fread(fid,1,'uint32');
      if rfco.TagName ~= 'rfco'
         warning('RFCO Header Not Read Correctly');
     end

     