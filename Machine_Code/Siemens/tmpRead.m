function Out = tmpRead(FourCC, fid, FileAsChars)
% Out = tmpRead(FourCC, fid, FileAsChars)

% Copyright Siemens Ultrasound 2003
% Shelby Brunke
% January 30, 2003
%
% edited by Jerome Mai 7/12/03

switch FourCC
	  case 'rfgi'
         fseek(fid,0,'bof');
         Out = readHeader_rfgi(fid, FileAsChars);
         fseek(fid,0,'bof');
     case 'movi'
         fseek(fid,0,'bof');
         Out = getStartOffset(fid, FileAsChars);
         fseek(fid,0,'bof');
     case 'avih'
         fseek(fid,0,'bof');
         Out = readHeader_avih(fid, FileAsChars);
         fseek(fid,0,'bof');
     case 'sffm'
         fseek(fid,0,'bof');
         Out = readHeader_sffm(fid, FileAsChars);
         fseek(fid,0,'bof');
     case 'cfh0'
         fseek(fid,0,'bof');
         Out = readHeader_cfh0(fid, FileAsChars);
         fseek(fid,0,'bof');
     case 'csh0'
         fseek(fid,0,'bof');
         Out = readHeader_csh0(fid, FileAsChars);
         fseek(fid,0,'bof');
     case 'strh'
         fseek(fid,0,'bof');
         Out = readHeader_strh(fid, FileAsChars);
         fseek(fid,0,'bof');
     case 'strf'
         fseek(fid,0,'bof');
         Out = readHeader_strf(fid, FileAsChars);
         fseek(fid,0,'bof');
     case 'rfbd'
         fseek(fid,0,'bof');
         Out = readHeader_rfbd(fid, FileAsChars);
         fseek(fid,0,'bof');
     case 'idx1'
         fseek(fid,0,'bof');
         if ~exist('avih')
            avih = readHeader_avih(fid, FileAsChars);
        end 
         Out = readHeader_idx1(fid, avih.dwTotalFrames);
         fseek(fid,0,'bof');
     
    case '00db'
        fseek(fid,0,'bof');
         Out = readHeader_00db(fid, FileAsChars);
         fseek(fid,0,'bof');
     
    case 'stri'
         fseek(fid,0,'bof');
         Out = readHeader_stri(fid, FileAsChars);
         fseek(fid,0,'bof');
    
     case 'rfam'
         fseek(fid,0,'bof');
         Out = readHeader_rfam(fid, FileAsChars);
         fseek(fid,0,'bof');
     case 'rfsi'
         fseek(fid,0,'bof');
         Out = readHeader_rfsi(fid, FileAsChars);
         fseek(fid,0,'bof');
     case 'rfbm'
         fseek(fid,0,'bof');
         Out = readHeader_rfbm(fid, FileAsChars);
         fseek(fid,0,'bof');
     case 'rfmm'
         fseek(fid,0,'bof');
         Out = readHeader_rfmm(fid, FileAsChars);
         fseek(fid,0,'bof');
     case 'rfdo'
         fseek(fid,0,'bof');
         Out = readHeader_rfdo(fid, FileAsChars);
         fseek(fid,0,'bof');
     case 'rfco'
         fseek(fid,0,'bof');
         Out = readHeader_rfco(fid, FileAsChars);
         fseek(fid,0,'bof');
     case 'RFS0'
         fseek(fid,0,'bof');
         Out = readHeader_rfsd(fid, FileAsChars, FourCC);
         fseek(fid,0,'bof');
      case 'RFS1'
         fseek(fid,0,'bof');
         Out = readHeader_rfsd(fid, FileAsChars, FourCC);
         fseek(fid,0,'bof');
     case 'RFS2'
         fseek(fid,0,'bof');
         Out = readHeader_rfsd(fid, FileAsChars, FourCC);
         fseek(fid,0,'bof');
     case 'RFS3'
         fseek(fid,0,'bof');
         Out = readHeader_rfsd(fid, FileAsChars, FourCC);
         fseek(fid,0,'bof');
     case 'RFS4'
         fseek(fid,0,'bof');
         Out = readHeader_rfsd(fid, FileAsChars, FourCC);
         fseek(fid,0,'bof');
     case 'RFS5'
         fseek(fid,0,'bof');
         Out = readHeader_rfsd(fid, FileAsChars, FourCC);
         fseek(fid,0,'bof');
     case 'RFS6'
         fseek(fid,0,'bof');
         Out = readHeader_rfsd(fid, FileAsChars, FourCC);
         fseek(fid,0,'bof');
     case 'RFS7'
         fseek(fid,0,'bof');
         Out = readHeader_rfsd(fid, FileAsChars, FourCC);
         fseek(fid,0,'bof');
  end
 
 
 
