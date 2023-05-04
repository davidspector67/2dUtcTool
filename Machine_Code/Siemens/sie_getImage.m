%% Dev To Do:

%% Info:
%Copywright Ahmed El Kaffas (c) - March 2019. 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% Initialize dependent directories:
function[imgData, imgInfo, refData, refInfo] = sie_getImage(filename, filedirectory, refname, refdirectory, path)
    
%     disp(class(filename))
%     disp(class(filedirectory))
%     disp(class(refname))
%     disp(class(refdirectory))

    %addpath(genpath(pwd))
    
    %% Gain curve compensation for Usx data [NOT YET AVAIALBLE]:
    
    %% Read Data:
    % Read needed data
        % uigetfile will not work in python so commented out _ 06/28/22
    %[Files.name, Files.directory] = uigetfile({'*.rfd', 'Load Philips Data'}, 'Must Be *Parsed.mat','MultiSelect','off');
    %Files.name = 'uri_SpV2232_VpF512_FpA90_20200803131445.rfd';
    %Files.directory = '/Users/elizabethszeto/Downloads/CanaryCRESTProgram/ThyroidQUS_data/';
    
    CurrentPath = pwd;
    Files.name = filename;
    Files.directory = filedirectory;

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
    
    % DONT FORGET THAT NORMALIZATION IS CURRENTLY TURNED OFF, EVEN IF
    % SELECTED!
    
    % Set manual analysis parameters
    analysisParams.axialWinSize = 2; % in mm pixel size is 0.075mm
    analysisParams.lateralWinSize =  2; % in mm 
    analysisParams.axialOverlap = 0; %in percent;
    analysisParams.lateralOverlap = 0; 
    analysisParams.minFrequency = 7000000;
    analysisParams.maxFrequency = 17000000;
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
    
    
    refFiles.directory = refdirectory;
    refFiles.name = refname;
    Frame = analysisParams.frame;
    
    %FinalOutput = repmat([],analysisParams.endFrame);
    %% Run Analysis
    % Loop through each file, load data and add info to table
    [imgInfo, refInfo, imgData, refData] = sie_getData(Files,refFiles, analysisParams, Frame);
    fig = figure('visible', 'off'); hImageDisplay = axes('Units','Pixels','Position',[20,20,530,390],'Color',[0 0 0],'XColor',[0 0 0],'YColor',[0 0 0]);
    H = imagesc(imgData.Bmode,[(imgInfo.clip_fact*imgInfo.maxval-imgInfo.dyn_range) imgInfo.clip_fact*imgInfo.maxval]); colormap('gray');hold on;
    axis off; exportgraphics(fig, path);
%     /Users/elizabethszeto/Downloads/CanaryCRESTProgram/uiag_temp0804/
    %string = split(refFiles.name,',');
    %filename = string(1);
    %save(string(1), FinalOutput);
    %save('usxData.mat', 'usxData', '-v7.3');
    
%     NPS = Window.NPS;
%     PS = Window.PS;
%     f = Window.f;
%     rPS = Window.rPS;
%     winTopBottomDepth = Window.winTopBottomDepth;
%     winLeftRightWidth = Window.winLeftRightWidth;
%     imgWindow = Window.imgWindow;
%     refWindow = Window.refWindow;
%     MBF = Window.MBF;
%     SS = Window.SS;
%     SI = Window.SI;
%     
%     disp(refData.refInfo.studyID);
%     disp(imgData.imgInfo.studyID); %studyID (philinfo), imgInfo (getdata)
     
    % [X,Y,T,AUC] = perfcurve([Labels == 3],x(:,2),'false','ProcessNaN','ignore');
    
    
    %% Close Up:
    %clearvars -except FixData1
%     if ismac
%         rmpath(genpath('/Users/work/Desktop/May3'))
%     else
%         rmpath(genpath(''));
end
