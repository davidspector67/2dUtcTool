function [im_array, imgData, imgInfo, refData, refInfo] = getImage(filename, filedirectory, refname, refdirectory, frame)

    %clearvars -except filename filedirectory refname refdirectory axWinSize latWinSize

    %clear all; close all; 
    
    % Set path for directory with code
    %}
    
    %% Gain curve compensation for Usx data [NOT YET AVAIALBLE]:
    
    %% Read Data:
    % Read needed data
    %[Files.name, Files.directory] = uigetfile({'*.rf', 'Load Philips Data'}, 'Must Be *Parsed.mat','MultiSelect','off');
    %}
    Files.name = filename;
    Files.directory = filedirectory;
    %[Files.xmlName] = uigetfile({'*.xml', 'Load the .png.xml'}, 'Load the .png.xml','MultiSelect','off');%Files.xmlName = 0; %[Files.xmlName] = uigetfile({'*.xml', 'Load the .png.xml'}, 'Load the .png.xml','MultiSelect','off');
    % Label each file - needed if multiselect on
    
    % clearvars -except rf_data_all_fund
    
    %% Read Reference
    %[refFiles.name, refFiles.directory] = uigetfile({'*.rf', 'Load Philips Reference'}, 'Must Be *Parsed.mat','MultiSelect','off');
    refFiles.name = refname;
    refFiles.directory = refdirectory;
    %[refFiles.xmlName] = uigetfile({'*.xml', 'Load the .png.xml'}, 'Load the .png.xml','MultiSelect','off');%refFiles.xmlName = 0; %[refFiles.xmlName] = uigetfile({'*.xml', 'Load the .png.xml'}, 'Load the .png.xml','MultiSelect','off');
    
    % clearvars -except rf_data_all_fund
    
    %% Initilize constants:
    
    %clearvars -except Files refFiles NumFrame rf_data_all_fund pt Keep
    
    % DON"T FORGET THAT NORMALIZATION IS CURRENTLY TURNED OFF, EVEN IF
    % SELECTED!
    
    % Set manual analysis parameters
%     analysisParams.axialWinSize = axWinSize; % in mm
%     analysisParams.lateralWinSize =  latWinSize; % in mm 
%     analysisParams.axialOverlap = axOverlap; %in percent;
%     analysisParams.lateralOverlap = latOverlap; 
%     analysisParams.minFrequency =  minFreq;%  
%     analysisParams.maxFrequency = maxFreq;% 
    analysisParams.frame = frame;
% %     
    % Philips temp parameters
    analysisParams.tilt1 = 0;
    analysisParams.width1 = 70;
    analysisParams.startDepth = 0.04;
    analysisParams.endDepth = 0.16;
    analysisParams.endHeight = 500;
    analysisParams.clip_fact = 0.95;
    analysisParams.dyn_range = 55;
    analysisParams.depth = 0.16; % in meters (m)
    analysisParams.width = 0.265; % in meters (m)

    [imgInfo, refInfo, imgData, refData] = philips_getData(Files,refFiles, analysisParams);

    im_array = getImData(imgData.scBmode,[(imgInfo.clip_fact*imgInfo.maxval-imgInfo.dyn_range) imgInfo.clip_fact*imgInfo.maxval]);

end    
