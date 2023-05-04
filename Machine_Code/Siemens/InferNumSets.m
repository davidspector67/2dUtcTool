function NumSets = InferNumSets(rfbd)
%NumSets = InferNumSets(rfbd)

% Copyright Siemens Ultrasound 2003
% Shelby Brunke
% January 30, 2003
%
NumSets = 0;
for j = 0:8,
    if(find(rfbd.Set == j)),
        NumSets = NumSets + 1;  
    end
end
