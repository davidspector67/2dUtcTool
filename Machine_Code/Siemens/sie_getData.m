function [imgInfo, refInfo, imgData, refData] = sie_getData(Files,refFiles, analysisParams, Frame)
    % Read IMG
    imgInfo = sie_read_PhilipsInfo(Files.name, Files.directory);
    [imgData, imgInfo] = sie_read_PhilipsImg(imgInfo, Frame, analysisParams.focus);
    
    % Read REF
    refInfo = sie_read_PhilipsInfo(refFiles.name, refFiles.directory);
    [refData, refInfo] = sie_read_PhilipsImg(refInfo, Frame, analysisParams.focus);
    
end
