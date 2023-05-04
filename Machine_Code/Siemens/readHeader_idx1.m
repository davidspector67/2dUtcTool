function idx1 = readHeader_idx1(fid,NumFramesAcquired)
% idx1 = readHeader_idx1(fid, NumFramesAcquired)

% Copyright Siemens Ultrasound 2003
% Shelby Brunke
% January 30, 2003
%

    OffsetIdx1ToEofInBytes = (NumFramesAcquired * 4 * 4) + 2*4;
     TopOfIdx1 = fseek(fid, -(OffsetIdx1ToEofInBytes), 'eof');   
     idx1.TagName = fscanf(fid,'%c',4) ;
       if idx1.TagName ~= 'idx1'
         warning('IDX1 Header Not Read Correctly');
         return;
       end
     idx1.DataSize = fread(fid,1,'uint32');   
     for i = 1:NumFramesAcquired
         idx1.Frame(i).ckid = fscanf(fid,'%c',4);
         idx1.Frame(i).dwFlags = fread(fid,1,'uint32');
         idx1.Frame(i).ChunkOffset = fread(fid,1,'uint32');
         idx1.Frame(i).ChunkLength = fread(fid,1,'uint32');
     end
   