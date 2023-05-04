function strf = readHeader_strf(fid,FileAsChars)
% strf = readHeader_strf(fid, FileAsChars)

% Copyright Siemens Ultrasound 2003
% Shelby Brunke
% January 30, 2003
%

     TopOfHeader = getFourCCByteLocation(FileAsChars, 'strf');
     fseek(fid,TopOfHeader - 1, 'bof');
     strf.TagName = fscanf(fid,'%c',4); 
     strf.DataSize = fread(fid,1,'uint32');   
     strf.HeaderVersion = fread(fid,1,'uint32');
     strf.SamplingRate = fread(fid,1,'float32');
     strf.BitCountPerSample = fread(fid,1,'uint32');
     strf.SampleMask = fread(fid,1,'uint32');
     strf.VectorHeaderLengthBytes = fread(fid,1,'uint32');
     strf.Compression = fread(fid,1,'uint32');
      if strf.TagName ~= 'strf'
         warning('STRF Header Not Read Correctly');
     end
     
     