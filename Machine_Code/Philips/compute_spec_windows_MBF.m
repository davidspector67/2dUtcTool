function [im_NPS, im_PS, im_f, im_rPS, im_winTopBottomDepth, im_winLeftRightWidth, ...
    im_MBF, im_SS, im_SI] = compute_spec_windows_init(top, minFrequency, maxFrequency, img_lowBandFreq, img_upBandFreq, ...
    img_samplingFreq) % added input & output arguments ~Harold
      
    % Dependent code
    %compute_powerSpec.m >> NEEDED
    %spectral_analysis.m >> For old code 01
    %spectral_analysis_default6db.m >> For old code 02

    % Output pre-allocation
    if length(top) >= 1
        im_NPS = zeros(length(top), 155);
        im_PS = zeros(length(top),155);
        im_f = zeros(length(top), 155);
        im_rPS = zeros(length(top), 155);
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
end
