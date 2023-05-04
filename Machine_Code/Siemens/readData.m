function VectorArray = readData(FileName, FileHeader, FirstFrame, NumFrames, SuppressOutput)
% VectorArray = readData(FileName, FileHeader, FirstFrame, NumFrames, SuppressOutput (optional))
% FileName: the path\filename of the file to be read.
% FirstFrame(1): The index of the first frame to be read from file.  
% NumFrames(-1): The integer number of frames to be read in to the file.
%                A negative number denotes, read all frames.
% SuppressOutput(1): When nonzero, suppresses display of file read status information.  
%                 For example, "Currently reading Frame # 37..."

% Copyright Siemens Ultrasound 2003
% Shelby Brunke
% February 11, 2003
%
if nargin<5
    SuppressOutput = 1;
end
if nargin<4
    NumFrames = -1;
end
if nargin<3
    FirstFrame = 1;
end



ReqNumFrames = NumFrames;
fid = fopen(FileName,'r','ieee-le');

if ~SuppressOutput, display('FileHeader Loaded ... Now Loading RF Data, Please Wait...'); end;
% Check to see if FirstFrame value is feasible
if FirstFrame > FileHeader.avih.dwTotalFrames
    warning('FirstFrame cannot be greater than the number of frames acquired');
    return;
end
% If NumFrames input variable is negative, collect all frames in file
if ReqNumFrames < 0
    NumFrames = FileHeader.avih.dwTotalFrames;
end
% Check to see that the total num frames requested is available in file.  If not
% Set the NumFrames to the maximum available.
if (FirstFrame + NumFrames -1) > (FileHeader.avih.dwTotalFrames)
    warning(['Cannot Acquire ', num2str(NumFrames), ' Frames']);
    NumFrames = FileHeader.avih.dwTotalFrames - FirstFrame + 1;
    warning(['NumFrames reset to ', num2str(NumFrames)]); 
end
% Get the frame data for the requested frames.
for j = 1:NumFrames
    if ~SuppressOutput, display(['Currently loading Frame# ', num2str(j), ' of ', num2str(NumFrames),' (True Frame Index = [',num2str((FirstFrame + j -1)),'])'  ]); end;
    [data, header] = ExtractFrameData(fid,FileHeader,FirstFrame + j -1);
    VectorArray.RfData(:,:,j) = data;
    VectorArray.Header(:,:,j) = header;
end

fclose(fid); % memory management
