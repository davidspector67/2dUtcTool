function [imgInfo, refInfo, imgData, refData] = philips_getData(Files,refFiles, analysisParams)

    % Read IMG
    imgInfo = philips_read_PhilipsInfo(Files.name, Files.directory);
    [imgData, imgInfo] = philips_read_PhilipsImg(imgInfo, analysisParams.frame);
    
    % Read REF
    refInfo = philips_read_PhilipsInfo(refFiles.name, refFiles.directory);
    [refData, refInfo] = philips_read_PhilipsImg(refInfo, analysisParams.frame);

end