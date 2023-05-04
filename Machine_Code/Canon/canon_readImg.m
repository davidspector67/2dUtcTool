function [Data, Info] = canon_readImg(Info, frame)
    % Solution for .bin data
    [Bmode, ModeIM] = readIQ(strcat(Info.filepath, Info.filename));

    % Get the map of coordinates xmap and ymap to be able to plot a point in scanconvert back to original 
    %scBmode = scanconvert(Bmode, Info); % Ultrasonix
    %scModeIM = scanconvert_mapped(ModeIM, Info);
    [scBmode, Info.height, Info.width, ~]        = scanConvert(Bmode, Info.width1,Info.tilt1,Info.startDepth1,Info.endDepth1, Info.endHeight); %guowei
    [~,       Info.height, Info.width, scModeIM] = scanConvert(ModeIM,Info.width1,Info.tilt1,Info.startDepth1,Info.endDepth1, Info.endHeight); %guowei   
    
    Info.lateralRes = Info.width*10^1/size(scBmode,2); %*10^1
    Info.axialRes   = Info.height*10^1/size(scBmode,1);
    Info.maxval     = max(scBmode(:));
    
    % Output
    Data.scRF    = scModeIM;
    Data.scBmode = scBmode;
    Data.RF      = ModeIM;
    Data.Bmode   = Bmode;
end
