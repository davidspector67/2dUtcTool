function rfsd = readHeader_rfsd(fid,FileAsChars,FourCC)
% rfsd = readHeader_rfsd(fid, FileAsChars)

% Copyright Siemens Ultrasound 2003
% Shelby Brunke
% January 30, 2003
%

     TopOfHeader = getFourCCByteLocation(FileAsChars, FourCC);
     fseek(fid,TopOfHeader -1 , 'bof');
     rfsd.TagName = fscanf(fid,'%c',4); 
     rfsd.DataSize = fread(fid,1,'uint32');   
     rfsd.HeaderVersion = fread(fid,1,'uint32');
     rfsd.IsDynamicFocusEn = fread(fid,1,'uint8');
     rfsd.RxFNum = fread(fid,1,'float32');
     rfsd.RxFocusRangeCm = fread(fid,1,'float32');
     rfsd.IsAperGrowthEn = fread(fid,1,'uint8');
     rfsd.RxApodization = fread(fid,1,'int32');
     rfsd.TxFocusRangeCm = fread(fid,1,'float32');
     rfsd.TxFNum = fread(fid,1,'float32');
     rfsd.TxFrequencyMhz = fread(fid,1,'float32');
     rfsd.NumTxCycles = fread(fid,1,'float32');
     rfsd.TxWaveformStyle = fread(fid,1,'int32');
     rfsd.PrfHz = fread(fid,1,'float32');
     rfsd.TxApodization = fread(fid,1,'int32');
     rfsd.PulseAmplitude = fread(fid,1,'float32');
     rfsd.AnalogGain = fread(fid,512,'float32');
     if rfsd.TagName ~= FourCC
         warning([FourCC, ' Header Not Read Correctly']);
     end
