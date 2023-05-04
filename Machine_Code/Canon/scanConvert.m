function [OutIm, HCm, WCm, OutImStruct]=scanConvert(InIm,Width,Tilt,StartDepth,EndDepth, DesiredHeight)

%% ScanConvert sector image
%   
%   Inputs:
%     InIm          Input image
%     Width         Sector width of input image in degrees 
%     Tilt          Tilt of sector image in degrees  
%     StartDepth    Axial depth of first sample in meters 
%     EndDepth      Axial depth of last sample in meters   
%     DesiredHeight Desired vertical size of output image in pixels 
%     (default 500)
%
%   Outputs:
%     OutIm         Output (scanconverted) image(s)  
%     HCm,WCm       Height and Width of image in centimeters 

if nargin<6   %nargin
    DesiredHeight = 500;
end;
 
% Convert to radians
Width=Width/180*pi;
Tilt = Tilt/180*pi;
 
Linear=0;
Sector=1;
[Samples, Beams, Frames]=size(InIm); %David
%Samples = 56; %David
%Beams = 89; %David
%Frames = 34; %David
if Samples > 1
    DepthIncrement=(EndDepth-StartDepth)/(Samples-1);
else
    DepthIncrement=(EndDepth-StartDepth)/Samples;
end
StartAngle = 3*pi/2 + Tilt - Width/2;
AngleIncrement=Width/(Beams+1);
 
OutIm=InIm;%clear('InIm');
Transpose = 0; 
Background = 0;
Height = DesiredHeight;
Width = 0;
 
%% Set size of image if not defined  
StopAngle=StartAngle+((Beams-1)*AngleIncrement);
StopDepth=StartDepth+((Samples-1)*DepthIncrement);
AngleRange=[StartAngle:AngleIncrement:StopAngle];

xmin=-1*max( cos(rem(StartAngle,pi))*[StartDepth StopDepth]);
xmax=-1*min( cos(rem(StopAngle,pi))*[StartDepth StopDepth]);
ymin=min(sin(rem(AngleRange,pi))*StartDepth);
ymax=max(sin(rem(AngleRange,pi))*StopDepth);
if (xmax == xmin)
    Widthscale = 0;
else
    Widthscale=abs((xmax-xmin)/(ymax-ymin));
end
%clear('xmin','xmax','ymin','ymax','AngleRange','StopAngle','StopDepth');

if Width==0, Width=ceil(Height*Widthscale);end;  
clear('Widthscale');
 
%% Interpolate image  
RadI = 1;% Original was 2
LatI = 1;% Original was 2
radsize = Samples;
latsize = Beams;
if (RadI>1 | LatI>1),
    x=1:radsize; y=1:latsize;
    xi=1:(1/RadI):radsize; yi=1:(1/LatI):latsize;

    if Transpose,
        NyIm=zeros(length(yi),length(xi),Frames);
    else
        NyIm=zeros(length(xi),length(yi),Frames);
    end;
    for n=1:Frames,
        if Transpose,
            NyIm(:,:,n)=interp2(x,y,double(OutIm(:,:,n)),xi',yi,'linear');
        else
            NyIm(:,:,n)=interp2(y,x,double(OutIm(:,:,n)),yi',xi,'linear'); 
        end;
    end; %for n
    OutIm=NyIm;
    %clear('NyIm');
end;

Nr= (Samples+((Samples-1)*(RadI-1)));
Nb= (Beams+((Beams-1)*(LatI-1)));
t0= StartAngle;
dt= AngleIncrement*(Beams)/(Nb);
r0= StartDepth;
dr= DepthIncrement*(Samples)/(Nr);
NbF=Nb;
NrF=Nr;
t0F=t0;
dtF=dt;
r0F=r0;
drF=dr;
 
%% Subtract 180 degrees to get transducer in top of image if StartAngle > pi  
t0=rem(t0,pi); t0F=rem(t0F,pi);

%% Define physical limits of image 
StopAngle=t0+((Nb)*dt);StopDepth=r0+((Nr)*dr);
AngleRange=[t0:dt:StopAngle];
y0=min(r0*sin(AngleRange));
ymax=max(StopDepth*sin(AngleRange));
x0=min(-StopDepth*cos(t0),-StartDepth*cos(t0));
xmax=max(-StartDepth*cos(StopAngle),-StopDepth*cos(StopAngle));

HeightCm=(ymax-y0)*100;
WidthCm=(xmax-x0)*100;
%clear('StopAngle','StopDepth','AngleRange');

%% Make (x,y)-plane representation of physical image
Xmat=(ones(1,Height)'*[0:1:Width-1])./(Width-1);
Ymat=([0:1:Height-1]'*ones(1,Width))./(Height-1);
Xmat=(Xmat*(xmax-x0))+x0;
Ymat=(Ymat*(ymax-y0))+y0;
%clear('x0','y0','xmax','ymax');

%% Transform into polar koordinates (angle,range) 
Anglemat=atan2(Ymat,-Xmat);
Rmat=sqrt(Xmat.^2 + Ymat.^2);
%clear('Xmat','Ymat');

%% Convert phys. angle and range into beam and sample
Anglemat=ceil((Anglemat-t0F)./dtF);
Rmat=ceil((Rmat-r0F)./drF);

%% Find pixels outside active sector  
Backgr=([find(Rmat<1);find(Rmat>=NrF)]);
Backgr=([Backgr;find(Anglemat<1);find(Anglemat>NbF)]);
if Transpose
    SCmap=(Rmat-1)*NbF + Anglemat;
else
    SCmap=(Anglemat-1)*NrF + Rmat;
end
%clear('Anglemat','Rmat');
SCmap(Backgr)=((NbF*NrF)+1)*ones(size(Backgr)); clear('Backgr');
if max(max(SCmap))<((NbF*NrF)+1)
    SCmap(1)=(NbF*NrF)+1;
end
%clear('Nr','Nb','t0','dt','r0','dr','NrF','NbF','t0F','dtF','r0F','drF');

% Mapping system added by Ahmed El Kaffas - April 1st, 2019
InIm_indy = zeros(size(OutIm)); InIm_indy = repmat([1:size(OutIm,1)]',1,size(OutIm,2)); % <-- maps (y,x) in Iout to indr in Iin
InIm_indx = zeros(size(OutIm)); InIm_indx = repmat([1:size(OutIm,2)],size(OutIm,1),1); % <-- maps (y,x) in Iin to indt in Iin

if Frames>1
    ScIm=zeros(Height,Width,Frames);
    for n=1:Frames
        Out=OutIm(:,:,n);
        Out=[Out(:);Background];
        ScIm(:,:,n)=Out(SCmap);
    end
    OutIm=ScIm;
    %clear('ScIm','Out');
else
    OutIm=[OutIm(:);Background];
    InIm_indy=[InIm_indy(:);Background];
    InIm_indx=[InIm_indx(:);Background];
    
    OutIm=OutIm(SCmap);
    InIm_indy=InIm_indy(SCmap);
    InIm_indx=InIm_indx(SCmap);
    
    OutIm=reshape(OutIm,Height,Width);
    InIm_indy=reshape(InIm_indy,Height,Width);
    InIm_indx=reshape(InIm_indx,Height,Width);
end

HCm=HeightCm;
WCm=WidthCm;

OutImStruct = struct('data', OutIm,...
                'orig', InIm,...
                'ymap', InIm_indy,...
                'xmap', InIm_indx);
