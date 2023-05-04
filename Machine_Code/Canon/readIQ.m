function [Bmode, ModeIM] = readIQ(Filename)
    %assigned area position
    analypos   = 0.3; % axial position [ratio]
    analywidth = 0.3; %lateral width [ratio]
    analyrange = 0.3; %axial width [ratio]
    
    
    %globalHeader = 7;
    globalHeader = 0;
    headerSize   = 2 * 8; %64Btyte converted with 32bit
    
    fileID = fopen(Filename, 'r'); %read header
    hdr = fread(fileID, 2, 'uint16'); %16bits * 2
    numAcquiredRxBeams = bin2dec(num2str(bitget(hdr(1), 16:-1:1, 'uint16'))); %16bits
    debugtemp          = bin2dec(num2str(bitget(hdr(2), 16:-1:1, 'uint16'))); %16bits
    
    hdr = fread(fileID, 2, 'uint16'); %16bits * 2
    debugtemp               = bin2dec(num2str(bitget(hdr(1), 16:-1:1, 'uint16'))); %16bits
    numParallelAcquisitions = bin2dec(num2str(bitget(hdr(2), 16:-1:1, 'uint16'))); %16bits
    
    hdr = fread(fileID, 2, 'uint16'); %16bits * 2
    numSamplesDrOut  = bin2dec(num2str(bitget(hdr(1), 16:-1:1, 'uint16'))); %16bits
    numSamplesRbfOut = bin2dec(num2str(bitget(hdr(2), 16:-1:1, 'uint16'))); %16bits
    
    hdr = fread(fileID, 4, 'uint8'); %8bits * 4
    isPhaseInvertEn = bitget(hdr(1), 1, 'uint8');
    debugtemp       = bitget(hdr(2), 1, 'uint8');
    debugtemp       = bitget(hdr(3), 1, 'uint8');
    
    hdr = fread(fileID, 5, 'uint32'); %32bits * 5
    decimationFactor = bitget(hdr(1),32:-1:1, 'int32');
    decimationFactor = num2str(decimationFactor);
    decimationFactor = bin2float(decimationFactor);
    %decimationFactor       = bin2float(num2str(bitget(hdr(1),32:-1:1, 'int32'))) %32bits float
    rbfdecimationFactor    = bin2float(num2str(bitget(hdr(2),32:-1:1, 'int32'))); %32bits float
    rbfBeMixerFrequcny     = bin2float(num2str(bitget(hdr(3),32:-1:1, 'int32')));%32bits float
    propagationVelCmPerSec = bin2float(num2str(bitget(hdr(4),32:-1:1, 'int32'))); %32bits float
    digitizingRateHz       = bin2float(num2str(bitget(hdr(5),32:-1:1, 'int32'))); %32bits float
    fclose(fileID);
    
    %read IQ data 
    fileID = fopen(Filename, 'r');
    numSamplesIQAcq = numSamplesDrOut*2;
    dataA = zeros(numSamplesDrOut*2,numAcquiredRxBeams);
    dataB = zeros(numSamplesDrOut*2,numAcquiredRxBeams);
    alldata = zeros(numSamplesDrOut*2,numAcquiredRxBeams*(1+isPhaseInvertEn));
    
    %IQ acquisition, following parameter always zero
    isPhaseInvertEn = 0;
    isRxFreqCompoundEn = 0;
    isDiffplusEn = 0;
    
    for ii = 1:numAcquiredRxBeams/numParallelAcquisitions
        for jj = 1:numParallelAcquisitions
            
            hdr = fread(fileID, headerSize, 'uint32');
            alldata(1:headerSize, (ii-1)*numParallelAcquisitions*(isPhaseInvertEn + 1) + jj) = hdr;
            
            
            dat = fread(fileID, numSamplesIQAcq, 'uint32');
            dat = dat - (dat >= 2^23)*(2^24);
           
            dataA(:,(ii-1)*numParallelAcquisitions+jj) = dat(1:numSamplesDrOut*2);
            
            %temp1 = alldata(headerSize+1:headerSize+1+numSamplesDrOut*2-1,(ii-1)*numParallelAcquisitions*(isPhaseInvertEn + 1) + jj);
            %temp2 = dat(1:numSamplesDrOut*2);
            %num1 = (headerSize+1+numSamplesDrOut*2-1) - (headerSize+1) + 1
            %num2 = headerSize+1+numSamplesDrOut*2-1
            %There's something wrong with this. It's taking 1:2800 of a size
            %2800 vector and putting it into a 2800 size matrix starting at
            %position 17. In MATLAB, this works okay because it just adds
            %another 16 lines, so that's what I did in Python.
            alldata(headerSize+1:headerSize+1+numSamplesDrOut*2-1,(ii-1)*numParallelAcquisitions*(isPhaseInvertEn + 1) + jj) = dat(1:numSamplesDrOut*2);
        end
        
        if 1 == isPhaseInvertEn
            for jj = 1:numParallelAcquisitions
                hdr = fread(fileID, headerSize, 'uint32');
                dat = fread(fileID, numSamplesIQAcq, 'uint32');
                dat = dat - (dat >= 2^23)*(2^24);
    
                dataB(:,(ii-1)*numParallelAcquisitions+jj) = dat(1:numSamplesDrOut*2);
                alldata(1:headerSize, (ii-1)*numParallelAcquisitions*(isPhaseInvertEn + 1) + numParallelAcquisitions*isPhaseInvertEn + jj) = hdr;
                alldata(headerSize+1:headerSize+1+numSamplesDrOut*2-1, (ii-1)*numParallelAcquisitions*(isPhaseInvertEn + 1) + numParallelAcquisitions*isPhaseInvertEn + jj) = dat(1:numSamplesDrOut*2);
            end
        end
    end
    fclose(fileID);
    
    IQ = dataA(1:2:numSamplesDrOut*2-1,:) + 1i*dataA(2:2:numSamplesDrOut*2,:);
    IQPI = dataB(1:2:numSamplesDrOut*2-1,:) + 1i*dataB(2:2:numSamplesDrOut*2,:);
    
    Bmode = 20*log10(abs(IQ));
    ModeIM = IQ;

%     %Show reconstructed B-image
%     figure(1)
%     colormap(gray);
%     imagesc(20*log10(abs(IQ)));
%     ar = getImData(20*log10(abs(IQ)));
%     exportgraphics(figure(1), "/Users/chloejeon/Downloads/CREST_Internship/new_USImgAnalysisGUI-Newest/im_ROIs/bMode_im.png");
%     
%     %Show Frequency Spectrum
%     analycenter = ceil(analypos * numSamplesDrOut);
%     analyaxsta = analycenter - ceil(0.5 * analyrange * numSamplesDrOut);
%     analyaxend =  analycenter + ceil(0.5 * analyrange * numSamplesDrOut);
%     analylatsta = ceil(0.5 * numAcquiredRxBeams) - ceil(0.5 * analywidth * numAcquiredRxBeams);
%     analylatend  = ceil(0.5 * numAcquiredRxBeams) + ceil(0.5 * analywidth * numAcquiredRxBeams);
%     numSamplesFT = analyaxend - analyaxsta + 1;
%     numSamplesFT = numSamplesFT - mod(numSamplesFT, 2);
%     rectangle('Position', [analylatsta analyaxsta (analylatend - analylatsta) (analyaxend - analyaxsta)], 'EdgeColor', 'c');
%     %freqIQ = fft(IQ);
%     freqIQ = fft(IQ(analyaxsta:analyaxsta+numSamplesFT-1,:));
%     %freqIQ = mean(freqIQ, 2);
%     temp = freqIQ(:,analylatsta:analylatend)
%     temp = abs(temp)
%     freqIQ = mean(temp, 2);
%     %freqIQ = mean(abs(freqIQ(:,analylatsta:analylatend)), 2);
%     
%     scaledfreqIQ = 20 * log10(freqIQ / numSamplesFT);
%     %samplingfreq = 160e6 / 3 / rbfdecimationfactor;
%     samplingfreq = digitizingRateHz / rbfdecimationFactor;
%     freq = zeros(numSamplesFT, 1);
%     if mod(numSamplesFT, 2) == 0
%        freq(1:numSamplesFT / 2) = samplingfreq * (0:(numSamplesFT/2 - 1))/numSamplesFT; %160/3 MHz machine sampling frequency
%        freq(numSamplesFT / 2 + 1:numSamplesFT) = -samplingfreq * ((numSamplesFT:-1:numSamplesFT/2+1) - numSamplesFT/2)/numSamplesFT;
%        
%        tempbuf = scaledfreqIQ(1:numSamplesFT / 2);
%        scaledfreqIQ(1:numSamplesFT / 2) = scaledfreqIQ(numSamplesFT / 2 + 1:numSamplesFT);
%        scaledfreqIQ(numSamplesFT / 2 + 1:numSamplesFT) = tempbuf(1:numSamplesFT / 2);
%        tempbuf = freq(1:numSamplesFT / 2);
%        freq(1:numSamplesFT / 2) = freq(numSamplesFT / 2 + 1:numSamplesFT);
%        freq(numSamplesFT / 2 + 1:numSamplesFT) = tempbuf(1:numSamplesFT / 2);
%     else %TBD
%        freq(1:floor(numSamplesFT/ 2)) = samplingfreq * (0:(floor(numSamplesFT/2) - 1))/numSamplesFT; %160/3 MHz machine sampling frequency
%        freq(floor(numSamplesFT/ 2)+1:numSamplesFT) = -samplingfreq * ((numSamplesFT:-1:numSamplesFT/2+1) - numSamplesFT/2)/numSamplesFT;
%        
%        tempbuf = scaledfreqIQ(1:floor(numSamplesFT / 2));
%        scaledfreqIQ(1:floor(numSamplesFT / 2)) = scaledfreqIQ(floor(numSamplesFT / 2) + 1:numSamplesFT);
%        scaledfreqIQ(floor(numSamplesFT / 2) + 1:numSamplesFT) = tempbuf(1:floor(numSamplesFT / 2));
%        tempbuf = freq(1:floor(numSamplesFT / 2));
%        freq(1:floor(numSamplesFT / 2)) = freq(floor(numSamplesFT / 2) + 1:numSamplesFT);
%        freq(floor(numSamplesFT / 2) + 1:numSamplesFT) = tempbuf(1:floor(numSamplesFT / 2));
%     end
%     freq = freq + rbfBeMixerFrequcny;
%     figure(2)
%     plot(freq,scaledfreqIQ);
%     xlim([-samplingfreq/2 + rbfBeMixerFrequcny samplingfreq/2 + rbfBeMixerFrequcny]);
%     ylim([0 100]);
%     xlabel('[Hz]');
%     ylabel('[dB]');
%     %frequency analysis end
%     %signal analysis in time domain
%     figure(3)
%     time = (0:numSamplesDrOut-1);
%     time = time / samplingfreq;
%     plot(time, real(IQ(:,int16(numAcquiredRxBeams/2)-24)), time, imag(IQ(:,int16(numAcquiredRxBeams/2)-24)));
end

%binary to float
function [out] = bin2float(x)
    
    out = double( typecast(uint32(bin2dec(x)),'single') );
       
end
