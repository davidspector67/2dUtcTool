% rfsi = readHeader_rfsi(fid, FileAsChars)

% Copyright Siemens Ultrasound 2003
% Shelby Brunke
% January 30, 2003

function rfsi = readHeader_rfsi(fid,FileAsChars)
     TopOfHeader = getFourCCByteLocation(FileAsChars, 'rfsi');
     fseek(fid,TopOfHeader -1 , 'bof');
     rfsi.TagName = fscanf(fid,'%c',4); 
     rfsi.DataSize = fread(fid,1,'uint32');   
     rfsi.HeaderVersion = fread(fid,1,'uint32');
     rfsi.Notes = fscanf(fid,'%c',10);
     rfsi.Script = fscanf(fid,'%c',12);
 if rfsi.TagName ~= 'rfsi'
         warning('RFSI Header Not Read Correctly');
     end