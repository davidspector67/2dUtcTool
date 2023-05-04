% This function is called when we perform spectral analysis on data file
% within a DEFINED 6dB window, either from reference file or
% custom-user-defined.
% This function is NOT called if no reference file is
% assigned to data file under analysis. ~Harold
function [mbfit, f_band, NPS_linfit, p, Rsqu, IB] = spectral_analysis_default6dB(NPS_normalized, f, dB6_lowF, dB6_highF, PSFlag)

    % NOTE: Currently, PSFlag = 2 for both ROI and single-point spectra
    % computations of spectral parameters ~Harold
    
    if PSFlag == 1
        NPS_normalized = 10*log10(NPS_normalized); %> (1) DIVISION: None log data
    else
        % NPS_normalized = NPS_normalized;
    end

    if PSFlag == 1
        %% METHOD a) (old)
        % Old linear regression method - ROI doesn't work with the new +/- 6 dB window
        
        % f0 and f1 inputs (which define the start and end frequencies to create the x-axis vector, f) seem to be treated as indices to access f - which may be incorrect ~Harold
        %f_band = f(f0:f1);
    
        %IB = 0;
    
        %[p, S] = polyfit(f_band,NPS_normalized(f0:f1),1);
        %NPS_linfit = polyval(p(:),f_band);
        %measurement = NPS_normalized(f0:f1);
        %mbfit = p(1)*f_band(round(end/2))+p(2);

        %for i=f0:f1
        %    IB = IB + NPS_normalized(i)*i;
        %end

        %Serr = sum((NPS_linfit-measurement).^2);
        %Stot = sum((measurement-mean(measurement)).^2);
        %Rsqu = 1-Serr/Stot;
    
        %% METHOD b) (new)
        % below is alternative method for defining f-band
    
        %smallestDiff = 999999999;
        %for i = 1 : size(f,1)
        %    currentDiff = abs(f0 - f(i));
        %    if currentDiff < smallestDiff
        %        smallestDiff = currentDiff;
        %        f0_ind = i;
        %        continue;
        %    else
        %        continue;
        %    end
        %end
    
        %smallestDiff = 999999999;
        %for i = size(f,1) : -1 : f0_ind
        %    currentDiff = abs(f(i)-f1);
        %    if currentDiff < smallestDiff
        %        smallestDiff = currentDiff;
        %        f1_ind = i;
        %        continue;
        %    else
        %        continue;
        %    end
        %end
    
        %f_band = f(f0_ind:f1_ind);
    
        %IB = 0;
    
        %[p, S] = polyfit(f_band,NPS_normalized(f0_ind:f1_ind),1);
        %NPS_linfit = polyval(p(:),f_band);
        %measurement = NPS_normalized(f0_ind:f1_ind);
        %mbfit = p(1)*f_band(round(end/2))+p(2);

        %for i=f0_ind:f1_ind
        %    IB = IB + NPS_normalized(i)*i;
        %end

        %Serr = sum((NPS_linfit-measurement).^2);
        %Stot = sum((measurement-mean(measurement)).^2);
        %Rsqu = 1-Serr/Stot;

    else % if PSFlag == 2
        
    % 1. in one scan / run-through of data file's f array, find the data
    % points on the frequency axis closest to reference file's 6dB window's
    % LOWER bound and UPPER bounds
    smallestDiff_dB6_lowF = 999999999;
    smallestDiff_dB6_highF = 999999999;
    
    for i = 1 : size(f,2)
        
        currentDiff_dB6_lowF = abs(dB6_lowF - f(1,i));
        currentDiff_dB6_highF = abs(dB6_highF - f(1,i));
        
        if currentDiff_dB6_lowF < smallestDiff_dB6_lowF
            smallestDiff_dB6_lowF = currentDiff_dB6_lowF;
            smallestDiffIndex_dB6_lowF = i;
        end
        
        if currentDiff_dB6_highF < smallestDiff_dB6_highF
            smallestDiff_dB6_highF = currentDiff_dB6_highF;
            smallestDiffIndex_dB6_highF = i;
            continue;
        else
            continue;
        end
        
    end
        
    % 2. compute linear regression within the 6dB window
    f_band = f(1,smallestDiffIndex_dB6_lowF:smallestDiffIndex_dB6_highF)'; % transpose row vector f in order for it to have same dimensions as column vector NPS
    [p, S] = polyfit(f_band,NPS_normalized(smallestDiffIndex_dB6_lowF:smallestDiffIndex_dB6_highF),1);    
    NPS_linfit = polyval(p(:),f_band);  % y_linfit is a column vector
             
    % 3. compute linear regression residuals   
    NPS_resid = NPS_normalized(smallestDiffIndex_dB6_lowF:smallestDiffIndex_dB6_highF) - NPS_linfit;
    NPS_SSresid = sum(NPS_resid.^2);
    NPS_SStotal = (length(NPS_normalized)-1) * var(NPS_normalized);
    Rsqu = 1 - NPS_SSresid / NPS_SStotal;

    % 4. compute spectral parameters
    IB = 0;
    for i = smallestDiffIndex_dB6_lowF : smallestDiffIndex_dB6_highF
        IB = IB + NPS_normalized(i) * i;
    end

    mbfit = p(1)*f_band(round(size(f_band,1)/2))+p(2);
    
    %below is for debugging ~Harold
    %figure
    %plot(f, NPS_normalized)
    %hold
    %plot(f_band,NPS_normalized(smallestDiffIndex_dB6_lowF:smallestDiffIndex_dB6_highF))
    
    end

end
