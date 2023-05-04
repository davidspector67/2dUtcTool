function [ROI_positions] = compute_roi_windows(...  
    ~,... % contains coordinates xmap and ymap for preSC conversion
    ... %scConversion,... contains coordinates xmap and ymap for preSC conversion
    xspline, yspline, ... % The spline parameters
    axial_NUM, lateral_NUM, ... % number of pixels along the axial and lateral size of the image e.g. size(cf.RfData,1)
    axial_rsize, lateral_rsize, ...  % window size in mm - user input from window parameters   
    axial_RES, lateral_RES, ...     % IMGinfo.XRes in mm/pixel - width/lines, height/samples
    axial_overlap, lateral_overlap)  % Percent (%) - Overlap - AEK: Currently symmetrical. 
     
    % Some axial/lateral dims
    axial_size = round(axial_rsize/axial_RES); % in pixels :: mm/(mm/pixel)
    lateral_size = round(lateral_rsize/lateral_RES);
    % next four are 1d matrices
    axial = (1:1:axial_NUM);
    lateral = (1:1:lateral_NUM);
    region_xcoords = xspline;
    region_ycoords = yspline;

    % Overlap fraction determines the incremental distance between ROIs
    axial_increment = axial_size * ( 1 - axial_overlap );
    lateral_increment = lateral_size * ( 1 - lateral_overlap );

    % ROI Sizes in Pixels
    axial_ROI_size_pixels = round( axial_size / (axial(2) - axial(1)) );
    lateral_ROI_size_pixels = round( lateral_size / (lateral(2) - lateral(1)) );

    % Determine ROIs - Find Region to Iterate Over
    axial_start = max( min(region_ycoords), axial(1) );
    axial_end = min( max(region_ycoords), axial(end) - axial_size );
    lateral_start = max( min(region_xcoords), lateral(1) ) ;                  
    lateral_end = min( max(region_xcoords), lateral(end) - lateral_size );

    % Determine ROI Set
    ROI_positions.left = []; ROI_positions.right = [];
    ROI_positions.top = []; ROI_positions.bottom = [];
    %preSC_ROI_positions.left = []; preSC_ROI_positions.right = [];
   % preSC_ROI_positions.top = []; preSC_ROI_positions.bottom = [];
    
    % Determine all points inside the user-defined polygon that defines
    % analysis region.  The 'mask' matrix - "1" inside region and "0" outside region.
    [ x_grid, y_grid ] = meshgrid( lateral, axial );
     
    % Regular in polygon
    %mask = inpolygon( x_grid, y_grid, region_xcoords, region_ycoords);
    
    % Try other option: https://www.mathworks.com/matlabcentral/fileexchange/27840-2d-polygon-interior-detection?s_tid=FX_rc3_behav
    mask = insidepoly( x_grid, y_grid, region_xcoords, region_ycoords);

    % GPU in polygon
    %x_gridGPU = gpuArray(x_grid); y_gridGPU = gpuArray(y_grid); 
    %region_xcoordsGPU = gpuArray(region_xcoords); region_ycoordsGPU = gpuArray(region_ycoords);
    %mask = inpolygon_for_gpu(x_gridGPU, y_gridGPU, region_xcoordsGPU, region_ycoordsGPU); 
    
    for axial_pos = axial_start:axial_increment:axial_end

        for lateral_pos = lateral_start:lateral_increment:lateral_end

            % Convert Axial and Lateral Positions in mm to Indices
            [~, axial_ind] = min( abs(axial - axial_pos) );
            [~, lateral_ind] = min( abs(lateral - lateral_pos) );

            % Determine if ROI is Inside Analysis Region
            mask_vals = mask(axial_ind:(axial_ind + axial_ROI_size_pixels - 1), ...
                             lateral_ind:(lateral_ind + lateral_ROI_size_pixels - 1));          

            % Define Percentage Threshold
            thresholdPercentage = 95.0;
            totalNumberOfElementsInRegion = size(mask_vals, 1) * size(mask_vals, 2);
            numberOfOnesInRegion = length( find( mask_vals == 1) );
            percentageOnes = numberOfOnesInRegion / totalNumberOfElementsInRegion * 100;

            if ( percentageOnes > thresholdPercentage )

                % Add ROI to output structure, quantize back to valid distances
                ROI_positions.left =[ROI_positions.left; lateral(lateral_ind)];
                ROI_positions.right = [ROI_positions.right; lateral(lateral_ind+lateral_ROI_size_pixels-1)];
                ROI_positions.top = [ROI_positions.top; axial(axial_ind)];
                ROI_positions.bottom = [ROI_positions.bottom; axial(axial_ind+axial_ROI_size_pixels-1)];
                
                % PreSC Conversion
                %preSC_ROI_positions.left = [preSC_ROI_positions.left; scConversion.xmap(floor(axial_ind), floor(lateral_ind))];
                %preSC_ROI_positions.right = [preSC_ROI_positions.right; scConversion.xmap(floor(axial_ind),floor(lateral_ind+lateral_ROI_size_pixels-1))];
                %preSC_ROI_positions.top = [preSC_ROI_positions.top; scConversion.ymap(floor(axial_ind),floor(lateral_ind))];
                %preSC_ROI_positions.bottom = [preSC_ROI_positions.bottom; scConversion.ymap(floor(axial_ind+axial_ROI_size_pixels-1),floor(lateral_ind))];
                

            end  % End:  if all(mask_vals(:) == 1)

        end  % End:  for lateral_pos = lateral_start:lateral_increment:lateral_end

    end  % End:  for axial_pos = axial_start:axial_increment:axial_end
    
end