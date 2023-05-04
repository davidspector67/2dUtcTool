% FOR PHILIPS
function [imgData, refData, Window] = sie_Analysis(Files, refFiles, analysisParams, Frame)

    disp('******* STARTING ********');
    disp(Files.name);
    disp(refFiles.name);
    
    % Frame to look at

    % Get the RF and meta info
    disp('READING DATA');
    [imgInfo, refInfo, imgData, refData] = getData(Files,refFiles, analysisParams, Frame);
    
    % Draw ROI on Bmode generated from RF - Get windows per ROI; With some display
    %imagesc([0 imgInfo.width],[0 imgInfo.height],sc1, [... ...]); colormap gray;
    disp('DISPLAY BMODE');
    figure(1); hImageDisplay = axes('Units','Pixels','Position',[20,20,530,390],'Color',[0 0 0],'XColor',[0 0 0],'YColor',[0 0 0]);
    H = imagesc(imgData.Bmode,[(imgInfo.clip_fact*imgInfo.maxval-imgInfo.dyn_range) imgInfo.clip_fact*imgInfo.maxval]); colormap('gray');hold on;
    exportgraphics(figure(1), "/Users/elizabethszeto/Downloads/CanaryCRESTProgram/bMode_im.png");
    
    % Get pre-scan-converstion spline coordinates
    disp('READY TO SELECT ROI >>>>>');
    [preSC, ~] = choose_ROI_SC(hImageDisplay, imgData.RF); % Function adjusted for scan converted data
    disp('ROI SELECTED');
    %set(H, 'pointer', 'watch'); drawnow;

    %exportgraphics(figure, "BMode.png"); %added to export image 07/20 -- not 'figure' -- produces second window called 'figure'
    
    % SC >> Get all smaller window splines within ROI on original RF (post-scan-conversion)
    disp('GETTING WINDOWS');
    [roiWindowSplinesPreSC] = compute_roi_windows(...  
      imgData.RF,... % contains coordinates xmap and ymap for preSC conversion  
      preSC.xspline,preSC.yspline, ... % The spline parameters axial(rows-2), lateral (coloms-1)
      size(imgData.Bmode,1), size(imgData.Bmode,2), ... % number of pixels along the axial and lateral size of the image 
      analysisParams.axialWinSize, analysisParams.lateralWinSize, ... % window size in mm - user input from window parameters   
      imgInfo.axialRes, imgInfo.lateralRes, ... % IMGinfo.XRes in mm/pixel - height/samples, width/lines
      analysisParams.axialOverlap, analysisParams.lateralOverlap);
      draw_roi_windows(hImageDisplay,roiWindowSplinesPreSC);
    
    % Display the pre-SC
    %disp('DISPLAY WINDOWS ON SC and PRE-SC IMAGES');
    %figure;
    %hImageDisplay2 = axes('Units','Pixels','Position',[20,20,530,390],'Color', [0 0 0], 'XColor',[0 0 0], 'YColor',[0 0 0]);
    %H2 = imagesc(imgData.Bmode); colormap('gray'); hold on;
    %MSplineCurve = plot(preSC.xspline,preSC.yspline,'g','LineWidth',2);
    %draw_roi_windows(hImageDisplay2,roiWindowSplinesPreSC);

    % Computed preSC >> Get all smaller window splines within ROI on original RF (pre-scan-conversion)
    %roiWindowSplines2 = compute_roi_windows(...   
    %    preSC.xspline,preSC.yspline, ... % The spline parameters axial(rows-2), lateral (coloms-1)
    %    size(Data.RF,1), size(Data.RF,2), ... % number of pixels along the axial and lateral size of the image 
    %    analysisParams.axialWinSize, analysisParams.lateralWinSize, ... % window size in mm - user input from window parameters   
    %    imgInfo.yRes, imgInfo.xRes, ... % IMGinfo.XRes in mm/pixel - height/samples, width/lines
    %    analysisParams.axialOverlap, analysisParams.lateralOverlap);
    %draw_roi_windows(hImageDisplay2,roiWindowSplines2);

    % For each ROI window, get the QUS power spectrums
    disp('COMPUTING NPS');
    Window = compute_spec_windows(imgData.RF, refData.RF, roiWindowSplinesPreSC, analysisParams, imgInfo, refInfo, Frame);
    % For each ROI window, get features
    %...

    % For each ROI window, get wavelet PS
    %...

    imgData.imgInfo = imgInfo;
    refData.refInfo = refInfo;
    disp('DONE');

end

function [imgInfo, refInfo, imgData, refData] = sie_getData(Files,refFiles, analysisParams, Frame)
    % Read IMG
    imgInfo = read_PhilipsInfo(Files.name, Files.directory);
    [imgData, imgInfo] = read_PhilipsImg(imgInfo, Frame, analysisParams.focus);
    
    % Read REF
    refInfo = read_PhilipsInfo(refFiles.name, refFiles.directory);
    [refData, refInfo] = read_PhilipsImg(refInfo, Frame, analysisParams.focus);
    
end

function [tempTable, roiWindowSplines] = getWindowPS(imgInfo,refInfo, I, Q, Iref, Qref, analysisParams)
    
end


