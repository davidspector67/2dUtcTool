function rfbd = readHeader_rfbd(fid,FileAsChars)
% rfbd = readHeader_rfbd(fid, FileAsChars)

% Copyright Siemens Ultrasound 2003
% Shelby Brunke
% January 30, 2003
%

     TopOfHeader = getFourCCByteLocation(FileAsChars, 'rfbd');
     fseek(fid,TopOfHeader -1 , 'bof');
     rfbd.TagName = fscanf(fid,'%c',4);
     rfbd.DataSize = fread(fid,1,'uint32');   
     rfbd.HeaderVersion = fread(fid,1,'uint32');
     rfbd.NumSamplesPerVector = fread(fid,1,'uint32') + 32;
     rfbd.NumVectorsPerFrame = fread(fid,1,'uint32');
     NumVectorsPerFrame = rfbd.NumVectorsPerFrame;
     modeTmp = fscanf(fid,'%c',2*NumVectorsPerFrame);
     rfbd.Mode = modeTmp(1:2:end)';
     rfbd.Set = fread(fid,NumVectorsPerFrame,'uint32');
     rfbd.PositionX = fread(fid,NumVectorsPerFrame,'float32');
     rfbd.PositionZ = fread(fid,NumVectorsPerFrame,'float32');
     rfbd.ThetaRad = fread(fid,NumVectorsPerFrame,'float32');
      if rfbd.TagName ~= 'rfbd'
         warning('RFBD Header Not Read Correctly');
     end