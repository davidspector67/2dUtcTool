function Out = readfiletest(FileHeader, VectorArray)
%Out = readFiletest(FileHeader)
%
% Copyright Siemens Ultrasound 2003
% Shelby Brunke
% January 30, 2003
%
disp(['Set Number for each Beam = ']);
      FileHeader.rfbd.Set
      disp(['NumFramesAcquired = ', num2str(FileHeader.avih.dwTotalFrames)]);
      disp(['RfAxialMinSamples = ', num2str(FileHeader.rfgi.MinDataVectorRange)]);
      disp(['RfAxialSpanSamples = ', num2str(FileHeader.rfbd.NumSamplesPerVector)]);
      disp(['NumVectorsPerFrame = ', num2str(FileHeader.rfbd.NumVectorsPerFrame)]);
      figure(1)
      subplot(311)
      plot(FileHeader.rfbd.PositionX)
      title('Lateral Position of Beam Origin in Millimeters')
      xlabel('Beam Index')
      ylabel('Lateral (x) Position (mm)')
      
      subplot(312)
      plot(FileHeader.rfbd.PositionZ)
      title('Axial Position of Beam Origin in Millimeters')
      xlabel('Beam Index')
      ylabel('Axial Position (z) (mm)')
      
      subplot(313)
      plot(FileHeader.rfbd.ThetaRad*180/pi)
      title('Angular Orientation of Beam in Degrees')
      xlabel('BeamIndex')
      ylabel('Angle of Beam (degrees)')
      Out = 0;
      
      figure(2)
      for i = 1:FileHeader.rfbd.NumVectorsPerFrame
          position(i) = i;
          vectorIndex(i) = double(VectorArray.Header(45,i,1)) + ...
              256*double(bitand(VectorArray.Header(46,i,1),1));
      end
      title('Vector Index for each vector in First Frame')
      plot(position,vectorIndex);
      xlabel('Vector Position in First Frame')
      ylabel('Vector Index as recorded in Vector Header')
          
      