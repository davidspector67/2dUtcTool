function ffdb = readHeader_00db(fid,FileAsChars)
%ffdb = readHeader_00db(fid,FileAsChars)

% Copyright Siemens Ultrasound 2003
% Shelby Brunke
% January 30, 2003
%
     TopOfHeader = getFourCCByteLocation(FileAsChars, '00db');
     fseek(fid,TopOfHeader -1 , 'bof');
     ffdb.TagName = fscanf(fid,'%c',4) %cellstr(fread(fid,4,'char'));
     ffdb.DataSize = fread(fid,1,'uint32');  
     ffdb.StartOfFrameData = ftell(fid);
     
     