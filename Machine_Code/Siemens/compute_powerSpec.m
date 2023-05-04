function  [freqChop, PS] =  compute_powerSpec(RFData, startFrequency, endFrequency, samplingFrequency, gain)

    % Create Hanning Window Function
    WindType = 'hann';
    unrmWind = window(WindType, size(RFData,1));
    windFunc = repmat(unrmWind * sqrt(length(unrmWind) / sum(unrmWind.^2)), 1, size(RFData,2));
    
    % Frequency Range
%     frequency=linspace(0,(samplingFrequency*1e6)/2/1e6,2048);
%     fLow=round(startFrequency*(2048/((samplingFrequency*1e6)/2/1e6)));
%     fHigh=round(endFrequency*(2048/((samplingFrequency*1e6)/2/1e6)));
%     freqChop=frequency(fLow:fHigh);
    frequency=linspace(0,samplingFrequency,4096);
    fLow=round(startFrequency*(4096/samplingFrequency));
    fHigh=round(endFrequency*(4096/samplingFrequency));
    freqChop=frequency(fLow:fHigh);

    % Get PS
%     disp("printing RFData size")
%     disp(size(RFData))
    fullPS = 10*log10(mean(abs(fft(double(RFData).*windFunc,4096)).^2,2)); % I think gain is being removed in RemoveTGCGain
    %fullPS = 10*log10(mean(abs(fft(RFData.*windFunc,4096)).^2,2))-gain;
    
    %Or use gain curve like >>>>>> + (gain/abs(gain))*10^(7.4425+abs(gain)*0.0025); % see gain_power_curve.m for gain compensation derivation
    %fullPS = 10*log10(mean(abs(fft(RFData.*windFunc,8192)).^2,2)) + (gain/abs(gain))*10^(m(2)+abs(gain)*m(1));
    
    PS = fullPS(fLow:fHigh,1);
    
end