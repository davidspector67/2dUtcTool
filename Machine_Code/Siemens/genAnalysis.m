%% Dev To Do:

%% Info:
%Copywright Ahmed El Kaffas (c) - March 2019. 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% Initialize dependent directories:
function[NPS, PS, f, frame, rPS, winTopBottomDepth, winLeftRightWidth, imgWindow, refWindow, MBF, SS, SI] = genAnalysis(fileName, filedirectory, refname, refdirectory)

    clear all; close all;
    Keep = [];
    
    % Set path for directory with code
    if ismac
        addpath(genpath('/Users/elizabethszeto/Downloads/CanaryCRESTProgram/ThyroidQUS'))
    else
        addpath(genpath(''));
    end
    
    % CD to data
    if ismac
        cd('/Users/elizabethszeto/Downloads/CanaryCRESTProgram/ThyroidQUS_data');
    %     cd('/Volumes/General/FatQuantData/');
    else
        cd('');
    end
    
    %% Gain curve compensation for Usx data [NOT YET AVAIALBLE]:
    
    %% Read Data:
    % Read needed data
        % uigetfile will not work in python so commented out _ 06/28/22
    %[Files.name, Files.directory] = uigetfile({'*.rfd', 'Load Philips Data'}, 'Must Be *Parsed.mat','MultiSelect','off');
    %Files.name = 'uri_SpV2232_VpF512_FpA90_20200803131445.rfd';
    %Files.directory = '/Users/elizabethszeto/Downloads/CanaryCRESTProgram/ThyroidQUS_data/';
    
    CurrentPath = pwd;
    [Files.name, Files.directory] = uigetfile('*.rfd', 'Select xxx.rfd', CurrentPath);

    disp(Files.name)
    disp(Files.directory)
    Files.xmlName = 0; %[Files.xmlName] = uigetfile({'*.xml', 'Load the .png.xml'}, 'Load the .png.xml','MultiSelect','off');
    % Label each file - needed if multiselect on
    
    % clearvars -except rf_data_all_fund
    
    %% Read Reference
    %[refFiles.name, refFiles.directory] = uigetfile({'*.rfd', 'Load Philips Reference'}, 'Must Be *Parsed.mat','MultiSelect','off');
    %disp(refFiles.name);
    %disp(refFiles.directory);
    %refFiles.xmlName = 0; %[refFiles.xmlName] = uigetfile({'*.xml', 'Load the .png.xml'}, 'Load the .png.xml','MultiSelect','off');
    
    % clearvars -except rf_data_all_fund
    
    %% Initilize constants:
    
    %clearvars -except Files refFiles Keep
    %clearvars -except Files Keep
    
    % DONT FORGET THAT NORMALIZATION IS CURRENTLY TURNED OFF, EVEN IF
    % SELECTED!
    
    % Set manual analysis parameters
    analysisParams.axialWinSize = 2; % in mm pixel size is 0.075mm %orig 2
    analysisParams.lateralWinSize =  2; % in mm, orig 2
    analysisParams.axialOverlap = 0; %in percent; orig 0
    analysisParams.lateralOverlap = 0; % orig 0
    analysisParams.minFrequency =  3000000;% orig 7000000
    analysisParams.maxFrequency = 4500000;% orig 17000000
    analysisParams.frame = 51; %Here you set the first frame you want to look at
    analysisParams.frameFreq = 40; %Here you set the step size you want to use
    imgInfo = sie_read_PhilipsInfo(Files.name, Files.directory); 
    analysisParams.endFrame = imgInfo.numFrames; %Here you set the frame you want to end on, this will be imgInfo.numFrames if you want to go through all frames
    analysisParams.focus = 0;
    disp(analysisParams.endFrame)
    % Philips temp parameters
    analysisParams.tilt1 = 0;
    analysisParams.width1 = 70;
    analysisParams.startDepth = 0.04;
    analysisParams.endDepth = 0.16;
    analysisParams.endHeight = 500;
    analysisParams.clip_fact = 0.95;
    analysisParams.dyn_range = 55;
    analysisParams.clip_fact = 0.95;
    analysisParams.dyn_range = 55;
    analysisParams.depth = 0.16; % in meters (m)
    analysisParams.width = 0.265; % in meters (m)
    
    %refFiles.directory = '/Users/work/Desktop/Reference/';
%     refFiles.directory = 'x';
%     if imgInfo.samples <= 1224
%         refFiles.name = 'uri_SpV1192_VpF512_FpA167_20210127114723.rfd';
%     elseif imgInfo.samples <= 2004
%         refFiles.name = 'uri_SpV2232_VpF512_FpA75_20210127114515.rfd';
%     else
%         refFiles.name = 'uri_SpV2232_VpF512_FpA90_20210129103614.rfd';
%     end
    [refFiles.name, refFiles.directory] = uigetfile('*.rfd', 'Select xxx.rfd', CurrentPath);

    
    FinalOutput = repmat([],analysisParams.endFrame);
    %% Run Analysis
    % Loop through each file, load data and add info to table
    for frame = analysisParams.frame:analysisParams.frameFreq:analysisParams.endFrame
        [Data, refData, Window] = sie_Analysis(Files, refFiles, analysisParams, frame);
        FinalOutput{frame} = Window;
        %close all
    end
    %string = split(refFiles.name,',');
    %fileName = string(1);
    %save(string(1), FinalOutput);
    %save('usxData.mat', 'usxData', '-v7.3');
    
    NPS = Window.NPS;
    PS = Window.PS;
    f = Window.f;
    rPS = Window.rPS;
    winTopBottomDepth = Window.winTopBottomDepth;
    winLeftRightWidth = Window.winLeftRightWidth;
    imgWindow = Window.imgWindow;
    refWindow = Window.refWindow;
    MBF = Window.MBF;
    SS = Window.SS;
    SI = Window.SI;
    
    disp(Data.imgInfo.studyID);
    disp(refData.refInfo.studyID);
    % [X,Y,T,AUC] = perfcurve([Labels == 3],x(:,2),'false','ProcessNaN','ignore');

    
    
    %% Close Up:
    %clearvars -except FixData1
    if ismac
        rmpath(genpath('/Users/work/Desktop/May3'))
    else
        rmpath(genpath(''));
end
