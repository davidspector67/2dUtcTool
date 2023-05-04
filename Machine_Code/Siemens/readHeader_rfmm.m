function rfmm = readHeader_rfmm(fid,FileAsChars)
% rfmm = readHeader_rfmm(fid, FileAsChars)

% Copyright Siemens Ultrasound 2003
% Shelby Brunke
% January 30, 2003
%

     TopOfHeader = getFourCCByteLocation(FileAsChars, 'rfmm');
     fseek(fid,TopOfHeader -1 , 'bof');
     rfmm.TagName = fscanf(fid,'%c',4); 
     rfmm.DataSize = fread(fid,1,'uint32');   
     rfmm.HeaderVersion = fread(fid,1,'uint32');
     rfmm.FovShape = fread(fid,1,'int32');
     rfmm.DisplayedAxialMinCm = fread(fid,1,'float32');
     rfmm.DisplayedAxialSpanCm = fread(fid,1,'float32');
     rfmm.ApexLateralCm = fread(fid,1,'float32');
     rfmm.ApexVerticalCm = fread(fid,1,'float32');
     rfmm.RoiLateralMin = fread(fid,1,'float32');
     rfmm.SteeringAngleRad = fread(fid,1,'float32');
     
      if rfmm.TagName ~= 'rfmm'
         warning('RFMM Header Not Read Correctly');
     end