function [Data, Info] = sie_read_PhilipsImg(Info , Frame, Focus)
    % Read the image data - Get RF data file path using the metadata in Info
    fid = fopen(Info.filename, 'r', 'ieee-le');
    FileHeader = readHeader(Info.filename);
    [data, ~] = ExtractFrameData(fid,FileHeader, Frame);
    echoData = splitData(double(data), Focus);
    % Create a straightforward Bmode without scan conversion for frame number frame
    %Bmode = rf2bmode(echoData); % pre-scan converted b-mode Ultrasonix
    Bmode = 20*log10(abs(hilbert(echoData)));

    % Make ModeIM just one frame - the chosen frame
    ModeIM = echoData;

    % Get the map of coordinates xmap and ymap to be able to plot a point in scanconvert back to original 
    %scBmode = scanconvert(Bmode, Info); % Ultrasonix
    %scModeIM = scanconvert_mapped(ModeIM, Info);
    %tilt1=0; width1=70; startDepth1=0.04; endDepth1=0.16; endHeight = 500; clip_fact = 0.95; dyn_range = 55;
    %[scBmode, Hcm1, Wcm1, ~]=scanConvert(Bmode,Info.width1,Info.tilt1,Info.startDepth1,Info.endDepth1, Info.endHeight); %guowei
    %[~, Hcm1, Wcm1, scModeIM]=scanConvert(ModeIM,Info.width1,Info.tilt1,Info.startDepth1,Info.endDepth1, Info.endHeight); %guowei 


%     InIm_indy = zeros(size(ModeIM)); InIm_indy = repmat([1:size(ModeIM,1)]',1,size(ModeIM,2)); % <-- maps (y,x) in Iout to indr in Iin
%     InIm_indx = zeros(size(ModeIM)); InIm_indx = repmat([1:size(ModeIM,2)],size(ModeIM,1),1); % <-- maps (y,x) in Iin to indt in Iin
% 
%     OutImStruct = struct('data', ModeIM,...
%                 'orig', ModeIM,...
%                 'ymap', InIm_indy,...
%                 'xmap', InIm_indx);
    
    %Info.height = Hcm1;
    %Info.width = Wcm1;
    %Info.lateralRes =  Wcm1*10^1/size(scBmode,2); %*10^1
    %Info.axialRes =  Hcm1*10^1/size(scBmode,1);
    %Info.maxval = max(scBmode(:));
    Info.lateralRes = 10/Info.lineDensity;
    disp(Info.lateralRes)
    Info.width = Info.lateralRes * size(Bmode,2); %*10^1
    Info.axialRes =  ((1500000)/ 40000000);
    Info.height = Info.axialRes * size(Bmode,1);
    Info.maxval = max(Bmode(:));
    
    % Ouput
    %Data.scRF = scModeIM;
    %Data.scBmode = scBmode;
    Data.RF = ModeIM;
    Data.Bmode = Bmode;
    
    clearvars -except Info Data Files analysisParams
end
function newData = splitData(imgData, focus)
    if (focus == 1) 
        for i = 1:2:512
            a = i/2;
            newData(:,a) = imgData(:,i);
        end
    else 
        for j = 2:2:512
            b = j/2;
            newData(:,b) = imgData(:,j);
        end
    end
end