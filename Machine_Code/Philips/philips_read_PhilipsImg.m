function [Data Info] = philips_read_PhilipsImg(Info, frame)

    if Info.filename(length(Info.filename)-3:length(Info.filename)) == '.mat'

        % Solution for .mat data
    
        % Read the image data - Get RF data file path using the metadata in Info
        load([Info.filepath Info.filename]);
        slice = 1; % hardcoded for now. 
        echoData = [rf_data_all_fund{1,frame}{slice}];
    
        % Create a straightforward Bmode without scan conversion for frame number frame
        %Bmode = rf2bmode(echoData); % pre-scan converted b-mode Ultrasonix
        Bmode = 20*log10(abs(hilbert(echoData)));
    
        % Make ModeIM just one frame - the chosen frame
        ModeIM = echoData;
    
        % Get the map of coordinates xmap and ymap to be able to plot a point in scanconvert back to original 
        %scBmode = scanconvert(Bmode, Info); % Ultrasonix
        %scModeIM = scanconvert_mapped(ModeIM, Info);
        %tilt1=0; width1=70; startDepth1=0.04; endDepth1=0.16; endHeight = 500; clip_fact = 0.95; dyn_range = 55;
        [scBmode, Hcm1, Wcm1, ~]=scanConvert(Bmode,Info.width1,Info.tilt1,Info.startDepth1,Info.endDepth1, Info.endHeight); %guowei
        [~, Hcm1, Wcm1, scModeIM]=scanConvert(ModeIM,Info.width1,Info.tilt1,Info.startDepth1,Info.endDepth1, Info.endHeight); %guowei   
        
        Info.height = Hcm1;
        Info.width = Wcm1;
        Info.lateralRes =  Wcm1*10^1/size(scBmode,2); %*10^1
        Info.axialRes =  Hcm1*10^1/size(scBmode,1);
        Info.maxval = max(scBmode(:));
        
        % Ouput
        Data.scRF = scModeIM;
        Data.scBmode = scBmode;
        Data.RF = ModeIM;
        Data.Bmode = Bmode;
        
        clearvars -except Info Data Files analysisParams

    else

        % Solution for .rf data
    
        % Read the image data - Get RF data file path using the metadata in Info
        %parsed_results = main_parser_stanford([Info.filepath Info.filename]);
        %%David. was importdata
        slice = 1; % hardcoded for now. 
%         echoData = [Info.rfData{1,frame}{slice}]; %David
        echoData = Info.rfData;
    
        % Create a straightforward Bmode without scan conversion for frame number frame
        %Bmode = rf2bmode(echoData); % pre-scan converted b-mode Ultrasonix
        Bmode = 20*log10(abs(hilbert(echoData))); %David
    
        % Make ModeIM just one frame - the chosen frame
        ModeIM = echoData;
    
        % Get the map of coordinates xmap and ymap to be able to plot a point in scanconvert back to original 
        %scBmode = scanconvert(Bmode, Info); % Ultrasonix
        %scModeIM = scanconvert_mapped(ModeIM, Info);
        %tilt1=0; width1=70; startDepth1=0.04; endDepth1=0.16; endHeight = 500; clip_fact = 0.95; dyn_range = 55;
        [scBmode, ~, ~, ~]=scanConvert(Bmode,Info.width1,Info.tilt1,Info.startDepth1,Info.endDepth1, Info.endHeight); %guowei %Hcm1 and Wcm1 are hidden (David)
        [~, Hcm1, Wcm1, scModeIM]=scanConvert(ModeIM,Info.width1,Info.tilt1,Info.startDepth1,Info.endDepth1, Info.endHeight); %guowei   
        
        Info.height = Hcm1;
        Info.width = Wcm1;
        Info.lateralRes =  Wcm1*10^1/size(scBmode,2); %*10^1
        Info.axialRes =  Hcm1*10^1/size(scBmode,1);
        Info.maxval = max(scBmode(:));
        
        % Ouput
        Data.scRF = scModeIM;
        Data.scBmode = scBmode;
        Data.RF = ModeIM;
        Data.Bmode = Bmode;
        
        %clearvars -except Info Data Files analysisParams %David
    end
end
