%load('RF_ans.mat');
slice = 2;
echoRF = [rf_data_all_fund{1,1}{slice}];%rftemp_all_fund;%
echoData = echoRF;
 
bmode = 20*log10(abs(hilbert(echoData)));
 
tilt1=0; width1=70; startDepth1=0.04; endDepth1=0.16; endHeight = 500;
 
[sc1, Hcm1, Wcm1, SCmap]=scanConvert(bmode,width1,tilt1,startDepth1,endDepth1, endHeight); %guowei
maxval = max(sc1(:));
clip_fact = 0.95;
dyn_range = 55;
%close all
figure;
imagesc([0 Wcm1],[0 Hcm1],sc1, [(clip_fact*maxval-dyn_range) clip_fact*maxval]); colormap gray;


%% OLD
% echoRF.echoData = rftemp_all_fund;
% rx_ML = uint16(echoRF.dbParams.azimuthMultilineFactorXbrOut(1));  %number receive multilines per transmit
%  
% rf_decimation = 2;  %rf decimation factor
%  
% %initiate final data based on expected columns (accounting for dummy
% %columns, multilines, and rf buffer padding)
% echoData = zeros(floor(size(echoRF.echoData,1)/rf_decimation),rx_ML*(echoRF.dbParams.num2dCols(1,1)-echoRF.dbParams.numCfDummies(1)));
% num_cols = size(echoData,2);
% num_rows = size(echoData,1);
%  
% %Draw line assignment from headerInfo.Line_Index
% for line_index = 1:(num_cols/rx_ML)
%     echoData(:,(1:rx_ML) + echoRF.headerInfo.Line_Index(line_index)*rx_ML) = echoRF.echoData(1:num_rows,:,line_index);
% end