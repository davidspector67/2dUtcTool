function window = compute_spec_windows(imgRF, refRF, ROI_positions, analysis_params, IMGinfo, REFinfo, frame) % added input & output arguments ~Harold
      
    % Dependent code
    %compute_powerSpec.m >> NEEDED
    %spectral_analysis.m >> For old code 01
    %spectral_analysis_default6db.m >> For old code 02

    % Set some flags
    PSFlag = 2; % Set Flag to 1 for PS method 1 and flag to 2 for method 2; changed to support +/- 6dB algorithm for ROI as well ~Harold
    DefaultRefFlag = 1; %Flag for using default reference included in folder - This is hardcoded for now. 
    shouldLogNormalization = 1;
    popupShownFlag = 0;
    dB6_lowF = IMGinfo.lowBandFreq; %.txFrequency - 3000000; %hardcoded
    dB6_highF = IMGinfo.upBandFreq; %.txFrequency + 3000000;%hardcoded

    % Output pre-allocation
    window(length(ROI_positions.top)).NPS = [];
    window(length(ROI_positions.top)).PS = [];
    window(length(ROI_positions.top)).f = [];
    
    fs = IMGinfo.samplingFrequency*2; % Not sure why multiply by two here, but it's the only way it works - same as Exact Imaging and others. 
    f0 = analysis_params.minFrequency;
    f1 = analysis_params.maxFrequency;
       
    % Compute spectral parameters for each window
    for i = 1:length(ROI_positions.top)
        
        % Make some adjustments and find the window to use. 
        imgWindow = imgRF(ROI_positions.top(i):ROI_positions.bottom(i),...
            ROI_positions.left(i):ROI_positions.right(i));
        refWindow = refRF(ROI_positions.top(i):ROI_positions.bottom(i),...
            ROI_positions.left(i):ROI_positions.right(i));
        
        % This is old - 8*top/bottom dim. - not sure why that was. 
        %spec_window = Bmode(ROI_positions.top(i)*8:ROI_positions.bottom(i)*8,...
        %ROI_positions.left(i):ROI_positions.right(i));

        % Get PS and NPS - There are two methods to compute the PS. See notes.
        % Method #1:
        %[f, PS] = NPS_Comp(imgWindow,fs, f0, f1,gain); %> (1) DIVISION: None log data
        %[f, rPS] = NPS_Comp(refWindow,fs, f0, f1,gain); %> (1) DIVISION: None log data
        %NPS = PS./rPS;%> (1) DIVISION: None log data
        % Method #2:
        [f, PS] = compute_powerSpec(imgWindow, f0, f1, fs, round(IMGinfo.gain)); %> (2) SUBSTRACTION: log data
        [f, rPS] = compute_powerSpec(refWindow, f0, f1, fs, round(REFinfo.gain)); %> (2) SUBSTRACTION: log data
        NPS = PS - rPS;%> (2) SUBSTRACTION: log data
                
        % Get ready to send output 
        window(i).frame = frame;
        window(i).NPS = NPS;
        window(i).PS = PS;
        window(i).rPS = rPS;
        window(i).f = f;
        window(i).winTopBottomDepth = [ROI_positions.top(i) ,ROI_positions.bottom(i)];  
        window(i).winLeftRightWidth = [ROI_positions.left(i) ,ROI_positions.right(i)];  
        window(i).imgWindow = imgWindow;
        window(i).refWindow = refWindow;
        
        % Computer QUS parameters
        [mbfit, ~, ~, p, ~, ~] = spectral_analysis_default6dB(NPS, f, dB6_lowF, dB6_highF, PSFlag);
        window(i).MBF = mbfit;
        window(i).SS = p(1);
        window(i).SI = p(2);

    end
end
