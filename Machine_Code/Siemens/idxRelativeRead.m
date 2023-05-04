function Out = idxRelativeRead(FourCC, fid, FrameNumber, idx1)
if (FourCC == 'frh0')
    fseek(fid,0,'bof');
    frh0 = readHeader_frh0(fid, FrameNumber, idx1);
    Out = frh0;
    fseek(fid,0,'bof');
end