%clear all;

function[parsed_result] = main_parser_stanford(folderName, fileName, dim)
%folderName = 'C:\Users\david\Documents\MATLAB\Data\';%'W:\Man_Elasto\2018 LFQ\Codes\Parser For Stanford\'; %David
%fileName = 'testDataFile.rf'; %David
% rf = parseRF_new(fullfile(folderName,fileName));
rf = parseRF([folderName,'/',fileName],0,2000);

if (rf.headerInfo.Line_Index(250) == rf.headerInfo.Line_Index(251))
    rf.lineData = rf.lineData(:,3:2:end);
else
    rf.lineData = rf.lineData(:,2:2:end);
end

% Fixed parameters
txBeamperFrame = 125;%125;
NumSonoCTAngles = 5;
ML_out = 2;  ML_in = 32; os = 2256;
%ix2 = [1:8 ; 9:16]; %David
%ix3 = ix2(:); % What's going on here? (David)

% Calculated parameters
NumFrame = floor(size(rf.lineData,2)/txBeamperFrame/NumSonoCTAngles);
multilinefactor = ML_in;
pt = floor((size(rf.lineData,1)-os)/multilinefactor);

rftemp_all_harm = zeros(pt,ML_out*txBeamperFrame);
rftemp_all_fund = zeros(pt,ML_out*txBeamperFrame);

clear rf_data_all_harm  rf_data_all_fund
for k0 = 1:NumFrame
    for k1 = 1:NumSonoCTAngles
        for k2 = 1:txBeamperFrame
            bi = (k0-1)*txBeamperFrame*NumSonoCTAngles + (k1-1)*txBeamperFrame + k2;
            temp = reshape(rf.lineData(os+(1:pt*multilinefactor) ,bi),multilinefactor,pt).';
            rftemp_all_harm((1:pt),(1:ML_out)+(k2-1)*ML_out) = temp(:,[1 3]);
            rftemp_all_fund((1:pt),(1:ML_out)+(k2-1)*ML_out) = temp(:,[1 3]+9);
        end
        
        rf_data_all_harm{k0}{k1} = rftemp_all_harm;
        rf_data_all_fund{k0}{k1} = rftemp_all_fund;
        
    end
end

% Assemble results
% parsed_result.rfData = rf_data_all_fund;
parsed_result.rfData = reshape(rf.echoData(:,1,:),5462,3822);
parsed_result.NumFrame = NumFrame;
parsed_result.pt = pt;
parsed_result.multilinefactor = multilinefactor;
parsed_result.NumSonoCTAngles = NumSonoCTAngles;
parsed_result.txBeamperFrame = txBeamperFrame;

if nargin == 3
    i = 1;
    parsed_result.data_3d = rf.lineData(:,i:i+41);
    i = i + 42;
    while i < size(rf.lineData, 2) - 41
        parsed_result.data_3d = cat(3,parsed_result.data_3d, rf.lineData(:,i:i+41));
        i = i + 42;
    end
end

% figure; H = imagesc(rf_data_all_fund,[(0.95*max(rf_data_all_fund)-55) 0.95*max(rf_data_all_fund)]); colormap('gray');hold on;
%save([fullfile(folderName,fileName(1:end-3))
%'Parsed.mat'],'rf_data_all_fund')%, 'rf_data_all_harm' %David
