function[x,y] = read_sie_files(filepath, Frame)

    if filepath(length(filepath)-3:length(filepath)) == '.rfd'
        fid = fopen(filepath, 'r', 'ieee-le');
        FileHeader = readHeader(filepath);
        [data, ~] = ExtractFrameData(fid,FileHeader, Frame);
        x = size(data,2);
        y = size(data,1);
    end