function [VectorArrayOut, FileHeaderOut] = readFile(FileName, FirstFrame, NumFrames, SuppressOutput, TestOption)
%[VectorArray, FileHeader] = readFile(FileName, FirstFrame, NumFrames, SuppressOutput (optional), TestOption(optional))
% FirstFrame(1): The index of the first frame to be read from file.  
% NumFrames(-1): The integer number of frames to be read in to the file.
%                A negative number denotes, read all frames.
% SuppressOutput(1): When nonzero, suppresses display of file read status information.  
%                 For example, "Currently reading Frame # 37..."
% TestOption(0)  0 ==> Skip plots of beam origin information
%                1 ==> display plots of beam origins


% Copyright Siemens Ultrasound 2003
% Shelby Brunke
% January 30, 2003
%


if nargout >= 1
   VectorArrayOut =[];
end
if nargout >= 2
   FileHeaderOut = [];
end

if nargin<5
    TestOption = 0;
end
if nargin<4
    SuppressOutput = 1;
end
if nargin<3
    NumFrames = -1;
end
if nargin<2
    FirstFrame = 1;
end


% ----Handle GUI File Reader---------------------------------------------------------------------
if nargin<1
	[filename, filepath] = uigetfile('*.bin; *.dat; *.rfd', 'Select the Antares RF file (*.bin, *.dat, or *.rfd)');
	if filename == 0
   	return;
	end
	FileName = strcat(filepath, filename);
	disp(FileName)
elseif ~ischar(FileName)
   DisplayFrameN =FileName;
	[filename, filepath] = uigetfile('*.bin; *.dat; *.rfd', 'Select the Antares RF file (*.bin, *.dat, or *.rfd)');
	if filename == 0
   	return;
	end
	FileName = strcat(filepath, filename);
	disp(FileName)
end
% ----Handle GUI File Reader---------------------------------------------------------------------

FileHeader = readHeader(FileName, SuppressOutput);
disp(FileHeader)

VectorArray = readData(FileName, FileHeader, FirstFrame, NumFrames, SuppressOutput);

disp(VectorArray)
if TestOption ~=0
    readfiletest(FileHeader, VectorArray);
end    
disp('RF Data Load Complete');
        
     
if nargout >= 1
   VectorArrayOut = VectorArray;
end
if nargout >= 2
   FileHeaderOut = FileHeader;
end
return

      
      
