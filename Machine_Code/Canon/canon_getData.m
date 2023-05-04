function [imgInfo, refInfo, imgData, refData] = canon_getData(Files,refFiles, analysisParams)

    % Read IMG
    imgInfo = canon_readInfo(Files.name, Files.directory, analysisParams);
    [imgData, imgInfo] = canon_readImg(imgInfo, analysisParams.frame);
    
    % Read REF
    refInfo = canon_readInfo(refFiles.name, refFiles.directory, analysisParams);
    [refData, refInfo] = canon_readImg(refInfo, analysisParams.frame);

end