import matlab.engine
eng = matlab.engine.start_matlab()

#where is the refdirectory? from genAnalysis ... doesn't exist
#eng.genAnalysis('uri_SpV2232_VpF512_FpA90_20200803131445.rfd', 'Users/elizabethszeto/Downloads/CanaryCRESTProgram/ThyroidQUS_data', 'uri_SpV1192_VpF512_FpA167_20210127114723.rfd', 'Users/work/Desktop/Reference/')

eng.genAnalysis(nargout = 11)


#eng.quit()


