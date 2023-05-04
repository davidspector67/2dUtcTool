function stri = readHeader_stri(fid,FileAsChars)
% stri = readHeader_stri(fid, FileAsChars)

% Copyright Siemens Ultrasound 2003
% Shelby Brunke
% January 30, 2003
%

     TopOfHeader = getFourCCByteLocation(FileAsChars, 'stri');
     fseek(fid,TopOfHeader - 1, 'bof');
     stri.TagName = fscanf(fid,'%c',4); %cellstr(fread(fid,4,'char'));
     stri.DataSize = fread(fid,1,'uint32');   
     stri.StartStreamTimestamp.Year = fread(fid,1,'uint16');
     stri.StartStreamTimestamp.Month = fread(fid,1,'uint16');
     stri.StartStreamTimestamp.DayOfWeek = fread(fid, 1, 'uint16');
     stri.StartStreamTimestamp.Day = fread(fid,1,'uint16');
     stri.StartStreamTimestamp.Hour = fread(fid,1,'uint16');
     stri.StartStreamTimestamp.Minute = fread(fid,1,'uint16');
     stri.StartStreamTimestamp.Second = fread(fid,1,'uint16');
     stri.StartStreamTimestamp.Millisecond = fread(fid,1,'uint16');
     
     stri.EndStreamTimestamp.Year = fread(fid,1,'uint16');
     stri.EndStreamTimestamp.Month = fread(fid,1,'uint16');
     stri.EndStreamTimestamp.DayOfWeek = fread(fid, 1, 'uint16');
     stri.EndStreamTimestamp.Day = fread(fid,1,'uint16');
     stri.EndStreamTimestamp.Hour = fread(fid,1,'uint16');
     stri.EndStreamTimestamp.Minute = fread(fid,1,'uint16');
     stri.EndStreamTimestamp.Second = fread(fid,1,'uint16');
     stri.EndStreamTimestamp.Millisecond = fread(fid,1,'uint16');
     stri.StreamType = fread(fid,1,'int32');
    
      if stri.TagName ~= 'stri'
         warning('STRI Header Not Read Correctly');
     end