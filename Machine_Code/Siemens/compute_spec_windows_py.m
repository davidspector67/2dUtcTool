function [im_NPS, im_PS, im_f, im_rPS, im_winTopBottomDepth, im_winLeftRightWidth, im_MBF, im_SS, im_SI] = compute_spec_windows_py(imgRF, refRF, top, bottom, left, ...
    right, minFrequency, maxFrequency, img_lowBandFreq, img_upBandFreq, ...
    img_samplingFreq,  img_gain, ref_gain) % added input & output arguments ~Harold
      
%     % Dependent code
%     %compute_powerSpec.m >> NEEDED
%     %spectral_analysis.m >> For old code 01
%     %spectral_analysis_default6db.m >> For old code 02
% 
      % Set some flags
      PSFlag = 2; % Set Flag to 1 for PS method 1 and flag to 2 for method 2; changed to support +/- 6dB algorithm for ROI as well ~Harold
      DefaultRefFlag = 1; %Flag for using default reference included in folder - This is hardcoded for now. 
      shouldLogNormalization = 1;
      popupShownFlag = 0;
      dB6_lowF = img_lowBandFreq; %.txFrequency - 3000000; %hardcoded
      dB6_highF = img_upBandFreq; %.txFrequency + 3000000;%hardcoded
% 
%     % Output pre-allocation
      if length(top) >= 1
        im_NPS = zeros(513,length(top));
        im_PS = zeros(513,length(top));
        im_f = zeros(513,length(top));
        im_rPS = zeros(513,length(top));
        im_winTopBottomDepth = zeros(length(top), 2);
        im_winLeftRightWidth = zeros(length(top), 2);
        im_MBF = zeros(1, length(top));
        im_SS = zeros(1, length(top));
        im_SI = zeros(1,length(top));
    else
        im_NPS = [];
        im_PS = [];
        im_f = [];
        im_rPS = [];
        im_winTopBottomDepth = [];
        im_winLeftRightWidth = [];
    end
      
      fs = img_samplingFreq*2; % Not sure why multiply by two here, but it's the only way it works - same as Exact Imaging and others. 
      f0 = minFrequency;
      f1 = maxFrequency;
         
      % Compute spectral parameters for each window
      for i = 1:length(top)
          
          % Make some adjustments and find the window to use. 
          imgWindow = imgRF(top(i):bottom(i),...
              left(i):right(i));
          refWindow = refRF(top(i):bottom(i),...
              left(i):right(i));
          
          % This is old - 8*top/bottom dim. - not sure why that was. 
%         %spec_window = Bmode(ROI_positions.top(i)*8:ROI_positions.bottom(i)*8,...
%         %ROI_positions.left(i):ROI_positions.right(i));
% 
%         % Get PS and NPS - There are two methods to compute the PS. See notes.
%         % Method #1:
%         %[f, PS] = NPS_Comp(imgWindow,fs, f0, f1,gain); %> (1) DIVISION: None log data
%         %[f, rPS] = NPS_Comp(refWindow,fs, f0, f1,gain); %> (1) DIVISION: None log data
%         %NPS = PS./rPS;%> (1) DIVISION: None log data
%         % Method #2:
          [f, PS] = compute_powerSpec(imgWindow, f0, f1, fs, round(img_gain)); %> (2) SUBSTRACTION: log data
          [f, rPS] = compute_powerSpec(refWindow, f0, f1, fs, round(ref_gain)); %> (2) SUBSTRACTION: log data
          NPS = PS - rPS;%> (2) SUBSTRACTION: log data
                  
          % Get ready to send output 
          im_NPS(:,i) = NPS;%window.NPS = [window.NPS NPS];%window(i).NPS = NPS;
          im_PS(:,i)= PS;%window.PS = [window.PS PS];%window(i).PS = PS;
          im_rPS(:,i) = rPS;%window.rPS = [window.rPS rPS];%window(i).rPS = rPS;
          im_f(:,i) = f;%window.f = [window.f f];%window(i).f = f;
          im_winTopBottomDepth(i, :) = [top(i) ,bottom(i)];  %window.winTopBottomDepth = [window.winTopBottomDepth [ROI_positions.top(i), ROI_positions.bottom(i)]];%window(i).winTopBottomDepth = [ROI_positions.top(i) ,ROI_positions.bottom(i)];  
          im_winLeftRightWidth(i, :) = [left(i) ,right(i)];  %window.winLeftRightWidth = [window.winLeftRightWidth [ROI_positions.left(i), ROI_positions.right(i)]];%window(i).winLeftRightWidth = [ROI_positions.left(i) ,ROI_positions.right(i)];  
%           window(i).imgWindow = imgWindow;%window.imgWindow = [window.imgWindow imgWindow];%window(i).imgWindow = imgWindow;
%           window(i).refWindow = refWindow;%window.refWindow = [window.refWindow refWindow];%window(i).refWindow = refWindow;
          
%         % Computer QUS parameters
          [mbfit, ~, ~, p, ~, ~] = spectral_analysis_default6dB(NPS, f, dB6_lowF, dB6_highF, PSFlag);
          im_MBF(i) = mbfit;%window.MBF = [window.MBF mbfit];%window(i).MBF = mbfit;
          im_SS(i) = p(1);%window.SS = [window.SS p(1)];%window(i).SS = p(1);
          im_SI(i) = p(2);%window.SI = [window.SI p(2)];%window(i).SI = p(2);
  
  
      end
      im_NPS = im_NPS.';
      im_PS = im_PS.';
      im_f = im_f.';
      im_rPS = im_rPS.';
end
