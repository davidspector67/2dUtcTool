
################################
#Copywright Ahmed El Kaffas - September 16, 2017
#Converts Philips xml/raw to nifit format
#Places time constant in ms as fourth pixdim
#Dependent on ParaMapFunctionsParallel - needs this absolutly in sam directory, or specifcy in sys.path
################################
# Specify path where ParaMapFUnctionsParallel is if not already in same directory - comment this on sherlock. 
import sys
import os
#sys.path.insert(0, '/Users/sjuli/Documents/')
#sys.path.insert(0, '/home/sjuli/bin')
#sys.path.insert(0, '~/Documents/Repositories/MotionCorrection3D/')
################################

import QusTools.Contrast3dAnalysis.ParaMapFunctionsParallel_v1 as pm
import nibabel as nib
from datetime import datetime
import numpy as np
from skimage.morphology import closing,ball

if __name__ == "__main__":
	# CODE ACTIVATOR
	print('Started xml2nii:');print(sys.argv[1]);print(str(datetime.now()));
	path = os.path.normpath(sys.argv[1]);
	splitpath = path.split(os.sep);
	type = 'Bolus'
	format = '3D'
	maskflag = 'no' # flag to indicate auto-masking yes/no
	name = splitpath[-1];

	# Read data	
	newres = np.array([1, 1, 1]);
	imarray_org, orgres, time = pm.read3D(sys.argv[1],0,[[-1,-1,5,5],[-1,-1,25,5],[-1,-1,5,5]]);#[[0,0,0,0],[0,0,0,0],[0,0,0,0]]); #or [[-1,-1,5,5],[-1,-1,25,5],[-1,-1,5,5]]);#
	#imarray, orgres, time, imarray_org = pm.prep_img(sys.argv[1],type,format, maskflag, newres);
	timeconst = time/(imarray_org.shape[1]+1);
	print('Done 3D to 4D:');print(str(datetime.now()));

	# # Save the 4D image without masking
	# print('Saving 4D:');print(str(datetime.now()));
	# #imarray_swap = np.reshape(imarray_org[0,:,0,:,:,:],(imarray_org.shape[1], imarray_org.shape[3], imarray_org.shape[4],imarray_org.shape[5]));
	# imarray_org2 = np.squeeze(imarray_org);
	# imarray_org2 = imarray_org2.swapaxes(0,3);imarray_org2 = imarray_org2.swapaxes(1,2);
	# affine = np.eye(4)
	# niiarray = nib.Nifti1Image(imarray_org2.astype('uint8'),affine);
	# niiarray.header['pixdim'] = [4.,orgres[0], orgres[1], orgres[2], timeconst, 0., 0., 0.];
	# #niiarray.header['slice_duration'] = time;
	# nib.save(niiarray, (name + '.nii.gz'));
	
	# ## Save 3D Mask 00: Ball
	# maskname='ballshape'
	# imShapes = imarray_org.shape;
	# smlShape = min(imShapes)
	# ballSize = abs(smlShape/4)
	# ballMask = ball(ballSize)
	# ballMask = np.lib.pad(ballMask, ((imShapes[5]/2,imShapes[5]/2), (imShapes[4],imShapes[4]), (imShapes[3],imShapes[3])), 'constant', constant_values=0);
	# print('Saving Mask 00:');print(str(datetime.now()));
	# affine = np.eye(4);
	# niiarray = nib.Nifti1Image(ballMask.astype('uint8'),affine);
	# niiarray.header['pixdim'] = [3., orgres[0], orgres[1], orgres[2], 0., 0., 0., 0.];
	# nib.save(niiarray, (name + '_mask' + maskname + '.nii.gz'));

	# ## Run pre-MC correction
	# del imarray_org, imarray_org2;
	# print('Starting shell script for Pre-MC');
	# head, tail = os.path.split(sys.argv[1]);
	# print(head);print(tail);
	# os.system("sh ~/Documents/Repositories/MotionCorrection3D/PreMC.sh %s %s" % (head,tail));
	# #os.system("sh /home/elkaffas/bin/PreMC.sh %s %s" % (head,tail));
	# #os.system("sh PreMC.sh %s %s" % (head,tail));

	# ## Re-load corrected 4D and clean up before creating mask
	# print('Done shell script for Pre-MC; re-load 4D for clean up:');
	# img = nib.load((name + '.nii.gz'));
	# data1 = img.get_data();
	# data2 = data1.swapaxes(0,3);
	# data3 = data2.swapaxes(1,2);
	# imarray_org = data3[np.newaxis,:,np.newaxis,:,:,:]; #Output# Needs to be 1,t,1,z,y,x
	# del data1, data2, data3;

	## Clean up image and save new 4d
	imarray_tosub = np.min(imarray_org[:,:,:,:,:,:],axis=1);
	imarray_org = (imarray_org - imarray_tosub).astype('int16'); del imarray_tosub;
	# imarray_tosub = np.max(imarray_org[:,0:5,:,:,:,:],axis=1);
	# imarray_org = (imarray_org - imarray_tosub).astype('int16'); 
	imarray_org[imarray_org < 0]=0;
	imarray_org = imarray_org.astype('uint8');
	imarray_org2 = np.squeeze(imarray_org);
	imarray_org2 = imarray_org2.swapaxes(0,3);imarray_org2 = imarray_org2.swapaxes(1,2);
	print('Saving cleaned up 4D:');print(str(datetime.now()));
	affine = np.eye(4)
	niiarray = nib.Nifti1Image(imarray_org2.astype('uint8'),affine);
	niiarray.header['pixdim'] = [4.,orgres[0], orgres[1], orgres[2], timeconst, 0., 0., 0.];
	#niiarray.header['slice_duration'] = time;
	nib.save(niiarray, (name + '.nii.gz'));

	## Save 3D Mask 01: Full Beam Shape-like
	## Make a mask out of 4D - WRITE LATER
	maskname='beamshape'
	MIP = np.std(imarray_org2[:,:,:,:],axis=3);
	MASK1 = MIP > 7;
	MASK1 = closing(MASK1, ball(16));
	print('Saving Mask 01:');print(str(datetime.now()));
	affine = np.eye(4);
	niiarray = nib.Nifti1Image(MASK1.astype('uint8'),affine);
	niiarray.header['pixdim'] = [3., orgres[0], orgres[1], orgres[2], 0., 0., 0., 0.];
	nib.save(niiarray, (name + '_mask_' + maskname + '.nii.gz'));

	# ## Save 3D Mask 02: Tighter Beam Shape - Conservative
	# print('Create Mask 02:');print(str(datetime.now()));
	# maskname='tightbeam'
	# imm, MASK2 = pm.masking(imarray_org,orgres);
	# MASK2 = MASK2.swapaxes(0,2);
	# print('Saving Mask 02:');print(str(datetime.now()));
	# affine = np.eye(4);
	# niiarray = nib.Nifti1Image(MASK2.astype('uint8'),affine);
	# niiarray.header['pixdim'] = [3., orgres[0], orgres[1], orgres[2], 0., 0., 0., 0.];
	# nib.save(niiarray, (name + '_mask' + maskname + '.nii.gz'));

	## Save 3D Projection: Max IP
	## Make a mask out of 4D - WRITE LATER
	maskname='MIP'
	MIP = np.max(imarray_org2[:,:,:,:],axis=3);
	print('Saving MIP:');print(str(datetime.now()));
	affine = np.eye(4);
	niiarray = nib.Nifti1Image(MIP.astype('uint8'),affine);
	niiarray.header['pixdim'] = [3., orgres[0], orgres[1], orgres[2], 0., 0., 0., 0.];
	nib.save(niiarray, (name + '_mask_' + maskname + '.nii.gz'));
