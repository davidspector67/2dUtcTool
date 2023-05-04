i = 1;
while i < size(lineData, 2) - 41
    figure; h = image(lineData(:,i:i+41)); colormap('gray');
    i = i + 42;
end