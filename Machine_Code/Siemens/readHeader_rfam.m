function rfam = readHeader_rfam(fid,FileAsChars)
% rfam = readHeader_rfam(fid, FileAsChars)

% Copyright Siemens Ultrasound 2003
% Shelby Brunke
% January 30, 2003
%

     TopOfHeader = getFourCCByteLocation(FileAsChars, 'rfam');
     fseek(fid,TopOfHeader -1 , 'bof');
     rfam.TagName = fscanf(fid,'%c',4); 
     rfam.DataSize = fread(fid,1,'uint32');   
     rfam.HeaderVersion = fread(fid,1,'uint32');
     rfam.ExamIndex = fread(fid,1,'int32');
     probeTmp = fscanf(fid,'%c',32);
     rfam.ProbeName = probeTmp(1:2:end);
     rfam.ProbeRadiusCm = fread(fid,1,'float32');
     rfam.IsTrigger1On = fread(fid,1,'uint8');
     rfam.IsTrigger2On = fread(fid,1,'uint8');
     rfam.Trigger1DelaySec = fread(fid,1,'float32');
     rfam.Trigger2DelaySec = fread(fid,1,'float32');
     rfam.Trigger1WaveCount = fread(fid,1,'int32');
     rfam.Trigger2WaveCount = fread(fid,1,'int32');
     rfam.FutureParameter1 = fread(fid,1,'uint8');
     rfam.FutureParameter2 = fread(fid,1,'uint8');
     rfam.FutureParameter3 = fread(fid,1,'float32');
     rfam.FutureParameter4 = fread(fid,1,'float32');
     rfam.FutureParameter5 = fread(fid,1,'int32');
     rfam.FutureParameter6 = fread(fid,1,'float32');
 if rfam.TagName ~= 'rfam'
         warning('RFAM Header Not Read Correctly');
     end

   
    