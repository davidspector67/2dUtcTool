function [out0, out1, out2, out3] = SortRF(RFinput,Stride,ML,CRE, isVoyager)
% De-interleave RF line data
%
% Syntax
%       out = SortRF(RFinput,Stride,MLs)
%       [out ...] = SortRF(RFinput,Stride,MLs,CRE)
%
% Inputs:
%       RFinput - MxN matrix of interleaved line data x transmit event
%       Stride - ML capture setting
%       MLs - Actual ML
%       CRE - Number of CRE channels
%       
% Returns:
%       out - de-interleaved data in the format of
%               Depth x ML x XmitEvents
%
%
% Last Modified 5/6/2014 (David Cheung)
% Last Modified 4/16/2015 (Scott Dianis)


%% Initialize default parameters
[N,xmitEvents] = size(RFinput);
Depth = floor(N/Stride);
MLs = 0:1:(ML-1);    

% Make into Column Vector
MLs = MLs(:);

%% Determine sorting order
if nargin < 4
    CRE = 1;
end

if nargin <5
	isVoyager = 1;
end

% Preallocate output array, but only those that will be used
switch CRE
    case 4,
        out3 = zeros(Depth,ML,xmitEvents);
        out2 = zeros(Depth,ML,xmitEvents);
        out1 = zeros(Depth,ML,xmitEvents);
        out0 = zeros(Depth,ML,xmitEvents);
    case 3,
        out2 = zeros(Depth,ML,xmitEvents);
        out1 = zeros(Depth,ML,xmitEvents);
        out0 = zeros(Depth,ML,xmitEvents);
    case 2,
        out1 = zeros(Depth,ML,xmitEvents);
        out0 = zeros(Depth,ML,xmitEvents);
    case 1,
        out0 = zeros(Depth,ML,xmitEvents);
end

if ( (CRE ~= 1) && (CRE ~= 2) && (CRE ~= 4) )
    error('no sort list for this CRE')
end

if Stride == 128,
    ML_SortList = 0:127;    
elseif Stride==32,
    switch CRE
        case 1,
            if isVoyager == 1
                % Voyager 20 MHz Sorting
                ML_SortList = [16 18 20 22 24 26 28 30 17 19 21 23 25 27 29 31 0 2 4 6 8 10 12 14 1 3 5 7 9 11 13 15];    
            else
                % Mustang 20 MHz Sorting
                %ML_SortList = [1 3 5 7 1 3 5 7 0 2 4 6 8 10 12 14 1 3 5 7 9 11 13 15 0 2 4 6 0 2 4 6 ];
                ML_SortList = [16 18 20 22 24 26 28 30 17 19 21 23 25 27 29 31 0 2 4 6 8 10 12 14 1 3 5 7 9 11 13 15];    
            end
            
            % Maybe a shifted version of Voyager 20 MHz Sorting
            %ML_SortList = [0 2 4 6 8 10 12 14 1 3 5 7 9 11 13 15 16 18 20 22 24 26 28 30 17 19 21 23 25 27 29 31];
                        
            % Debug sort list, use to figure out unknown ordering
            %ML_SortList = [0:31];
        case 2,
            ML_SortList = [0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15];

        case 4,
            ML_SortList = [4 4 5 5 6 6 7 7 4 4 5 5 6 6 7 7 0 0 1 1 2 2 3 3 0 0 1 1 2 2 3 3];

    end
elseif Stride==16,
    switch CRE
        case 1,
            ML_SortList = [0 2 4 6 8 10 12 14 1 3 5 7 9 11 13 15];
        case 2,
            ML_SortList = [0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7];
        case 4,
            ML_SortList = [0 0 1 1 2 2 3 3 0 0 1 1 2 2 3 3];
    end
elseif Stride==12,
    switch CRE
        case 1,
            ML_SortList = [0 2 4 6 8 10 1 3 5 7 9 11];
        case 2,
            ML_SortList = [0 1 2 3 4 5 0 1 2 3 4 5];
        case 4,
            ML_SortList = [0 0 1 1 2 2 0 0 1 1 2 2];
    end        
elseif Stride==8,
    switch CRE
        case 1,
            ML_SortList = [0 2 4 6 1 3 5 7];
        case 2,
            ML_SortList = [0 1 2 3 0 1 2 3];
        case 4,
            ML_SortList = [0 0 1 1 0 0 1 1];
    end
elseif Stride==4,
    switch CRE
        case 1,
            ML_SortList = [0 2 1 3];
        case 2,
            ML_SortList = [0 1 0 1];
        case 4,
            ML_SortList = [0 0 0 0];
    end
elseif Stride==2,
    switch CRE
        case 1,
            ML_SortList = [0 1];
        case 2,
            ML_SortList = [0 0];
        case 4,
            ML_SortList = [0 0];
    end
else
    error('no sort list for this stride');
end;

if ((ML-1) > max(ML_SortList) || CRE == 4 && Stride < 16 || CRE == 2 && Stride < 4 )
    error('Captured ML is insufficient, some ML were not captured');
end
%% Sort
for k = 1:ML,
    iML = find(ML_SortList==MLs(k));       
    out0(1:Depth, k, :) = RFinput(iML(1):Stride:(Depth*Stride),:);
    switch CRE
        case 2,
            out1(1:Depth, k, :) = RFinput(iML(2):Stride:(Depth*Stride),:);
            out2(1:Depth, k, :) = RFinput(iML(2):Stride:(Depth*Stride),:);
            out3(1:Depth, k, :) = RFinput(iML(2):Stride:(Depth*Stride),:);
        case 4,
            out2(1:Depth, k, :) = RFinput(iML(3):Stride:(Depth*Stride),:);
            out3(1:Depth, k, :) = RFinput(iML(4):Stride:(Depth*Stride),:);
    end
end;
