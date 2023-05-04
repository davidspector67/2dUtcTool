function[xpts_spline, ypts_spline] = calculateSpline(xpts, ypts)

q = 0:length(xpts)-1;
qq = 0:0.1:length(xpts)-1;                          % Increase the number of points 10 times using spline interpolation
xpts_spline = spline(q,xpts,qq);
ypts_spline = spline(q,ypts,qq);