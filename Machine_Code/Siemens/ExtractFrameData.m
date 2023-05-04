function [Tmp, Tmp2] = ExtractFrameDataNEW(fid,FileHeader,FrameNumber)
%VectorArray = ExtractFrameData(fid,FileHeader,FrameNumber)

% Copyright Siemens Ultrasound 2003
% Shelby Brunke
% January 30, 2003
%
%modified by Jerome Mai, 5/12/03 to read vector by vector to accommodate large files.

if nargin < 3
    FrameNumber = 1;
end
Tmp = int16(zeros(FileHeader.rfbd.NumSamplesPerVector-FileHeader.strf.VectorHeaderLengthBytes/2,...
   FileHeader.csh0.NumVectorsPerStreamFrame));
Tmp2 =uint8(zeros(FileHeader.strf.VectorHeaderLengthBytes,FileHeader.csh0.NumVectorsPerStreamFrame));
VectorTmp = int16(zeros(FileHeader.rfbd.NumSamplesPerVector,1));



fseek(fid, FileHeader.idx1.Frame(FrameNumber).ChunkOffset + FileHeader.idx1.startOffset, 'bof'); 
TagName = fscanf(fid,'%c',4);
DataSize = fread(fid,1,'uint32');
if TagName ~= FileHeader.idx1.Frame(FrameNumber).ckid
    warning('File Read Unsuccesful: Frame location does not match Index Chunk');
    
elseif DataSize ~= FileHeader.idx1.Frame(FrameNumber).ChunkLength
    warning('File Read Unsuccessful: Frame size does not match Index Chunk');
    
    
    
else    
    
	for VectorN = 1:FileHeader.csh0.NumVectorsPerStreamFrame
		VectorTmp = fread(fid,FileHeader.rfbd.NumSamplesPerVector ,'int16');    
		Tmp(:,VectorN) = int16(VectorTmp(FileHeader.strf.VectorHeaderLengthBytes/2+1:end));
		%convert Tmp from int16 to uint8 for reading vector header, have to turn the "negative sign bit" to value
		VectorTmp = VectorTmp(1:FileHeader.strf.VectorHeaderLengthBytes/2)+...
   		65536*(VectorTmp(1:FileHeader.strf.VectorHeaderLengthBytes/2)<0);
		%above is slightly faster but same as Tmp = mod(Tmp(1:FileHeader.strf.VectorHeaderLengthBytes/2,:),65536);
		Tmp2(1:2:FileHeader.strf.VectorHeaderLengthBytes,VectorN) = uint8(rem(VectorTmp,256));
		Tmp2(2:2:FileHeader.strf.VectorHeaderLengthBytes,VectorN) = uint8(floor(VectorTmp/256));
	end
   
   
%%the following does the same thing as above, easier to understand, but runs slower   
%   for VectorN = 1:FileHeader.csh0.NumVectorsPerStreamFrame
%		TopOfFrameData = ftell(fid);
%		VectorTmp = fread(fid,FileHeader.rfbd.NumSamplesPerVector ,'int16');    
%		Tmp(:,VectorN) = int16(VectorTmp(FileHeader.strf.VectorHeaderLengthBytes/2+1:end));
%		fseek(fid,TopOfFrameData,'bof');
%		VectorTmp = fread(fid,FileHeader.rfbd.NumSamplesPerVector*2 ,'uint8');    
%		Tmp2(:,VectorN) = uint8(VectorTmp(1:FileHeader.strf.VectorHeaderLengthBytes));
%	end
   
   
end    


