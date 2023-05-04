function [preSC,SplineCurve] = choose_ROI_SC(AxisHandle, RfData)
% Spline ROI on scanconverted Bmode from RF; the coordinates of spline are then
% mapped to RF data pre scan conversion. 

% Written by Ahmed El Kaffas
% Last modified: 21-05-2016
%
% INPUTS
% AxisHandle -> Handle for image where ROI will be chosen; image needs to
% be plotted in figure 
% RFData -> Matrix array with RF data pre scan conversion
%
% OUTPUTS
% xpts_spline -> Spline across the x-axis mapped to pre scan conversion 
% ypts_spline -> Spline across the y-axis mapped to pre scan conversion 
%
% EXAMPLE SYNTAX:
% RDIinfo = read_rdi
% ------------------------------------------------------------

    Position = get(gca(),'Position'); %get(AxisHandle,'Position');
    FigureHandle = gcf(); %get(AxisHandle, 'Parent'))
    PointHandles = [];
    xpts = [];
    ypts = [];
    NbrOfPoints = 0;
    done = 0;
    %skip_status = 0;
    ImageHandle = get(AxisHandle,'children');
    set(ImageHandle,'ButtonDownFcn','');

    hold on

    set(gcf(), 'pointer', 'crosshair'); drawnow;
    set(AxisHandle,'Position',Position)

    while ~done;

        UserInput = waitforbuttonpress;                            % Wait for user input
        SelectionType = get(FigureHandle,'SelectionType');         % Get information about the last button press
        CharacterType = get(FigureHandle,'CurrentCharacter');      % Get information about the character entered

        % Left mouse button was pressed, add a point
        if UserInput == 0 && strcmp(SelectionType,'normal')

            % Get the new point and store it
            CurrentPoint  = get(AxisHandle, 'CurrentPoint');
            xpts = [xpts CurrentPoint(2,1)];
            ypts = [ypts CurrentPoint(2,2)];
            NbrOfPoints = NbrOfPoints + 1;

            % Plot the new point
            h = plot(CurrentPoint(2,1),CurrentPoint(2,2),'r.');
            set(AxisHandle,'Position',Position)                   % For some reason, Matlab moves the Title text when the first point is plotted, which in turn resizes the image slightly. This line restores the original size of the image
            PointHandles = [PointHandles h];

            % If there are any points, and the right mousebutton or the backspace key was pressed, remove a point
        elseif NbrOfPoints > 0 && ((UserInput == 0 && strcmp(SelectionType,'alt')) || (UserInput == 1 && CharacterType == char(8)))   % The ASCII code for backspace is 8

            NbrOfPoints = NbrOfPoints - 1;
            xpts = xpts(1:end-1);
            ypts = ypts(1:end-1);
            delete(PointHandles(end));
            PointHandles = PointHandles(1:end-1);

            % Enter key was pressed, manual outlining done, and the number of points are at least 3
        elseif NbrOfPoints >= 3 && UserInput == 1 && CharacterType == char(13)

            % Indicate that we are done
            done = 1;

            % Close the curve by making the first and last points the same
            xpts = [xpts xpts(1)];
            ypts = [ypts ypts(1)];

            % Remove plotted points
            if ~isempty(PointHandles)         
                delete(PointHandles(:));
            end
        end

        % Remove old spline and draw new    
        if exist('SplineCurve','var')
            if ishghandle(SplineCurve)
                delete(SplineCurve)     % Delete the graphics object
            end
            clear SplineCurve
        end
        if NbrOfPoints > 1
            q = 0:length(xpts)-1;
            qq = 0:0.1:length(xpts)-1;                          % Increase the number of points 10 times using spline interpolation
            xpts_spline = spline(q,xpts,qq);
            ypts_spline = spline(q,ypts,qq);
            SplineCurve = plot(xpts_spline,ypts_spline,'g','LineWidth',2);
            drawnow
            out = 0;

        else
            xpts_spline = xpts;
            ypts_spline = ypts;
        end

    end

    hold off
    set(gcf(), 'pointer', 'arrow'); drawnow;

    preSC.xspline = xpts;
    preSC.yspline = ypts;


    % MSplineCurve = plot(xmpts_spline,ympts_spline,'g','LineWidth',2);
    % hold off;
    % figure(eks_fig);
    % set(ImageHandle,'ButtonDownFcn','CPimagetool');
end