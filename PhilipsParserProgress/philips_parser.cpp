#include <iostream>
#include <vector>
#include <cmath>
#include <fstream>

using namespace std;

class Parsed_result {
    public:
        vector<int> rfData;
        int numFrame;
        int pt;
        int multilinefactor;
        int numSonoCTAngles;
        int txBeamperFrame;
};

class HeaderInfo {
    public:
        int rf_captureVersion;
        vector<int> tap_point;
        int data_gate;
        vector<int> multilines_capture;
        int steer;
        int elevationPlaneOffset;
        int pm_index;
        int data_format;
        vector<int> data_type;
        int header_tag;
        int threed_pos;
        int mode_info;
        int frame_id;
        int csid;
        int line_type;
        int time_stamp;
        vector<int> rf_sample_rate;
};

class dbParams {
    public:
        vector<int> acqNumActiveScChannels2d;
        vector<int> azimuthMultilineFactorXbrOut;
        vector<int> azimuthMultilineFactorXbrIn;
        vector<int> numOfSonoCTAngles2dActual;
        vector<int> elevationMultilineFactor;
        vector<int> numPiPulses;
        vector<int> num2DCols;
        vector<int> fastPiEnabled;
        vector<int> numZones2d;
        int numSubVols;
        int numPlanes;
        int zigZagEnabled;
        vector<int> azimuthMultilineFactorXbrOutCf;
        vector<int> azimuthMultilineFactorXbrInCf;
        vector<int> multilLineFactorCf;
        vector<int> linesPerEnsCf;
        vector<int> ensPerSeqCf;
        vector<int> numCfCols;
        vector<int> numCfEntries;
        vector<int> numCfDummies;
        vector<int> elevationMultilineFactorCf;
        vector<int> Planes;
        vector<int> multiLineFactorCf;
        int tapPoint;
};

class Rfdata {
    public:
        vector<int> lineData;
        vector<int> lineHeader;
        HeaderInfo headerInfo;
        vector<int> echoData;
        dbParams dbParams;
        vector<int> echoData1;
        vector<int> echoData2;
        vector<int> echoData3;
        vector<int> echoMModeData;
};

void parseRF(string filepath) {
    Rfdata rfdata;
    string fn = filepath;
    cout << "Opening: " << fn;
    
}