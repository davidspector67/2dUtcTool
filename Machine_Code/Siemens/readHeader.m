function FileHeader = readHeader(FileName, SuppressOutput)
%FileHeader = readHeader(FileName, SuppressOutput (optional))
% FileName: the path\filename of the file to be read.
% SuppressOutput(1): When nonzero, suppresses display of file read status information.  
%                 For example, "Currently reading Frame # 37..."


% Copyright Siemens Ultrasound 2003
% Shelby Brunke
% February 11, 2003
%
% Optimized by Jerome Mai, 7/13/03, (avoid fread twice)

if nargin < 2
    SuppressOutput = 1;
end

if ~SuppressOutput, display('Currently Loading Header, Please Wait...'); end;

fid = fopen(FileName,'r','ieee-le');
if fid == -1
    if exist(FileName, 'file')
        error('Cannot open existing file: %s', FileName)
    else
        error('Missing file: %s', FileName)
    end
end
%worstCaseHeaderSize = 70000;  % 70000 for 8x96
%worstCaseHeaderSize = 90000;  % 90000 for VF13-5 and 19 lines
worstCaseHeaderSize = 100000;
%worstCaseHeaderSize = 110000;
%FileAsChars = zeros(worstCaseHeaderSize,1);
FileAsChars = fread(fid,worstCaseHeaderSize,'uchar');

% do a temporary read to load the idx1 table
FileHeader.rfgi = tmpRead('rfgi',fid,FileAsChars);
FileHeader.idx1 = tmpRead('idx1',fid,FileAsChars);
%FileHeader.idx1(1).Frame(1);
FileHeader.idx1.startOffset = tmpRead('movi',fid,FileAsChars);

%using the idx1 table, we know where the data starts, and we only need part of the data
%up to that point into headers, so the searches in tmpRead can be faster.
% the FRH0 (frame headers) are handled based on the idx1 chunk.
%the 'if' statement is only for older URI data, can be removed once header format finalized.
if (FileHeader.idx1.Frame(1).ChunkOffset + FileHeader.idx1.startOffset)<worstCaseHeaderSize,
   FileAsChars = FileAsChars(1:(FileHeader.idx1.Frame(1).ChunkOffset + FileHeader.idx1.startOffset));
end



FileHeader.rfbd = tmpRead('rfbd',fid,FileAsChars);
FileHeader.avih = tmpRead('avih',fid,FileAsChars);
FileHeader.sffm = tmpRead('sffm',fid,FileAsChars);
FileHeader.strh = tmpRead('strh',fid,FileAsChars);
FileHeader.strf = tmpRead('strf',fid,FileAsChars);
FileHeader.cfh0 = tmpRead('cfh0',fid,FileAsChars);
FileHeader.csh0 = tmpRead('csh0',fid,FileAsChars);
FileHeader.stri = tmpRead('stri',fid,FileAsChars);
FileHeader.rfam = tmpRead('rfam',fid,FileAsChars);
FileHeader.rfsi = tmpRead('rfsi',fid,FileAsChars);
FileHeader.rfbm = tmpRead('rfbm',fid,FileAsChars);
FileHeader.rfmm = tmpRead('rfmm',fid,FileAsChars);
FileHeader.rfdo = tmpRead('rfdo',fid,FileAsChars);
FileHeader.rfco = tmpRead('rfco',fid,FileAsChars);
for set = 1:8
    FourCC = ['RFS' num2str(set-1)];
    FileHeader.rfsd(set) = tmpRead(FourCC,fid,FileAsChars);
end

   

for i = 1:FileHeader.avih.dwTotalFrames
    FileHeader.frh0(i) = idxRelativeRead('frh0',fid,i,FileHeader.idx1);
end


clear FileAsChars; % Memory Management
fclose(fid); % memory management
