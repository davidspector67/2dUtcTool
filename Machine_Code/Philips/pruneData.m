function prunedData = pruneData(lineData, lineHeader, ML_Capture)
% For use with RF capture data
%       prunedData = prunedata(rfdata)
%
% Remove false gate data at the beginning of the line
%
% Inputs:
%   lineData    - unsorted line data
%   lineHeader  - unsorted line header info
%   ML_Capture  - ML capture setting
%
% Returns: prunedData
%   Removes false gate data at the beginning and end of the line
%
%
% Last Modified 3/11/2014 (David Cheung)
               
%% Remove false gate data at beginning of the line
% Waste first 1.5% of the line
numSamples = size(lineData,1);
referenceLine = ceil(size(lineData,2) * 0.2);
startPoint = ceil(numSamples * 0.015);
iFirstSample = find(lineHeader(startPoint:numSamples,referenceLine)==3,1)+startPoint-1;
if (isempty(iFirstSample))
    iFirstSample = 1;
end
% Align the pruning
alignment = 1:double(ML_Capture):numSamples;
diff = alignment - iFirstSample;
iFirstSample = alignment(find(diff >= 0, 1, 'first'));

% Prune data
prunedData = lineData(iFirstSample:numSamples,:);
lineHeader = lineHeader(iFirstSample:numSamples,:);

%% Remove zero data at end of the line
% Start from last 1% of the line
numSamples = size(prunedData,1);
startPoint = floor(numSamples * 0.99);
iLastSample = find(lineHeader(startPoint:numSamples,referenceLine)==0,1)+startPoint-1;
if (isempty(iLastSample))
    iLastSample = size(prunedData, 1);
else
    % Align the pruning
    alignment = 1:double(ML_Capture):numSamples;
    diff = alignment - iLastSample;
    iLastSample = alignment(find(diff >= 0, 1, 'first')) - 1;
end
if (isempty(iLastSample))
    iLastSample = size(prunedData, 1);
end

% Prune data
prunedData = prunedData(1:iLastSample,:);