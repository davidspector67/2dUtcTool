function FourCCByteLocation = getFourCCByteLocationNew(FileAsChars, FourCC);
%FourCCByteLocation = getFourcCByteLocation(FileAsChars, FourCC)

% Copyright Siemens Ultrasound 2003
% Shelby Brunke
% January 30, 2003
% Optimized July 11, 2003 (find() function is much faster than while loop)
%
% Optimized by Jerome Mai, 7/13/03, (use findstr instead)


FourCCByteLocation = findstr(FileAsChars', FourCC);

if isempty(FourCCByteLocation)
   FourCCByteLocation = 0;
   warning([FourCC, ' Not Found']);
end
