"""
-----------------------------------------------------------------------------------------
pre_fit_end.py
-----------------------------------------------------------------------------------------
Goal of the script:
Arrange data and AVG runs
-----------------------------------------------------------------------------------------
Input(s):
sys.argv[1]: subject name
-----------------------------------------------------------------------------------------
Output(s):
# Preprocessed timeseries files
-----------------------------------------------------------------------------------------
Output(s):
new freesurfer segmentation files
-----------------------------------------------------------------------------------------
To run:
1. cd to function
>> cd /home/mszinte/projects/pRFgazeMod/mri_analysis/
2. python pre_fit/pre_fit_end.py sub-001
-----------------------------------------------------------------------------------------
Written by Martin Szinte (martin.szinte@gmail.com)
-----------------------------------------------------------------------------------------
"""

# Stop warnings
# -------------
import warnings
warnings.filterwarnings("ignore")

# General imports
# ---------------
import json
import sys
import os
import glob
import pdb
import platform
import numpy as np
opj = os.path.join
deb = pdb.set_trace

sub_name = sys.argv[1]

# MRI analysis imports
# --------------------
import nibabel as nb
from scipy.signal import savgol_filter

with open('settings.json') as f:
    json_s = f.read()
    analysis_info = json.loads(json_s)
trans_cmd = 'rsync -avuz --progress'

# Define cluster/server specific parameters
# -----------------------------------------
base_dir = analysis_info['base_dir'] 

# Copy files in pp_data folder
# ----------------------------
dest_folder1 = "{base_dir}/pp_data/{sub}/func/fmriprep_dct/".format(base_dir = base_dir, sub = sub_name)
try: os.makedirs(dest_folder1)
except: pass

dest_folder2 = "{base_dir}/pp_data/{sub}/func/fmriprep_dct_pca/".format(base_dir = base_dir, sub = sub_name)
try: os.makedirs(dest_folder2)
except: pass


orig_folder = "{base_dir}/deriv_data/pybest/{sub}".format(base_dir = base_dir, sub = sub_name)

for session in analysis_info['session']:

    for attend_cond in analysis_info['attend_cond']:
        for gaze_cond in analysis_info['gaze_cond']:
            if gaze_cond == 'GazeCenterFS':
                runs = analysis_info['runs']
                run_txt = ['_run-1','_run-2']

            else:
                runs = [analysis_info['runs'][0]]
                run_txt = ['']

            
            for run,run_txt in zip(runs,run_txt):
                # dct func
                orig_file1 = "{orig_fold}/{session}/preproc/{sub}_{session}_task-{attend_cond}{gaze_cond}_space-T1w{run_txt}_desc-preproc_bold.nii.gz".format(
                                        orig_fold = orig_folder, session = session, run = run, run_txt = run_txt,
                                        sub = sub_name, attend_cond = attend_cond, gaze_cond = gaze_cond)
                dest_file1 = "{dest_fold}/{sub}_{session}_task-{attend_cond}{gaze_cond}_{run}_fmriprep_dct.nii.gz".format(
                                        dest_fold = dest_folder1, session = session, run = run,
                                        sub = sub_name, attend_cond = attend_cond, gaze_cond = gaze_cond)

                os.system("{cmd} {orig} {dest}".format(cmd = trans_cmd, orig = orig_file1, dest = dest_file1))

                # dct + denoised func
                orig_file2 = "{orig_fold}/{session}/denoising/{sub}_{session}_task-{attend_cond}{gaze_cond}_space-T1w{run_txt}_desc-denoised_bold.nii.gz".format(
                                        orig_fold = orig_folder, session = session, run = run, run_txt = run_txt,
                                        sub = sub_name, attend_cond = attend_cond, gaze_cond = gaze_cond)
                dest_file2 = "{dest_fold}/{sub}_{session}_task-{attend_cond}{gaze_cond}_{run}_fmriprep_dct_pca.nii.gz".format(
                                        dest_fold = dest_folder2, session = session, run = run,
                                        sub = sub_name, attend_cond = attend_cond, gaze_cond = gaze_cond)

                os.system("{cmd} {orig} {dest}".format(cmd = trans_cmd, orig = orig_file2, dest = dest_file2))

# Average tasks runs
for preproc in analysis_info['preproc']:
    for attend_cond in analysis_info['attend_cond']:
        for gaze_cond in analysis_info['gaze_cond']:
            file_list = sorted(glob.glob("{base_dir}/pp_data/{sub}/func/{preproc}/*{attend_cond}{gaze_cond}_*.nii.gz".format(
                                         base_dir = base_dir, sub = sub_name, preproc = preproc,
                                         attend_cond = attend_cond, gaze_cond = gaze_cond)))
            
            img = nb.load(file_list[0])
            data_avg = np.zeros(img.shape)
        
            for file in file_list:
                print('avg:'+file)
                # load
                data_psc = []
                data_psc_img = nb.load(file)
                data_psc = data_psc_img.get_fdata()
                data_avg += data_psc/len(file_list)

            # save
            new_file = "{base_dir}/pp_data/{sub}/func/{sub}_task-{attend_cond}{gaze_cond}_{preproc}_avg.nii.gz".format(
                        base_dir = base_dir, sub = sub_name, preproc = preproc, 
                        attend_cond = attend_cond, gaze_cond = gaze_cond)
            new_img = nb.Nifti1Image(dataobj = data_avg, affine = img.affine, header = img.header)
            new_img.to_filename(new_file)

for preproc in analysis_info['preproc']:
    file_list = sorted(glob.glob("{base_dir}/pp_data/{sub}/func/{preproc}/*GazeCenterFS_*.nii.gz".format(
                                         base_dir = base_dir, sub = sub_name, preproc = preproc)))

    img = nb.load(file_list[0])
    data_avg = np.zeros(img.shape)
    for file in file_list:
        print('avg:'+file)
        # load
        data_psc = []
        data_psc_img = nb.load(file)
        data_psc = data_psc_img.get_fdata()
        data_avg += data_psc/len(file_list)

    # save
    new_file = "{base_dir}/pp_data/{sub}/func/{sub}_task-GazeCenterFS_{preproc}_avg.nii.gz".format(
                base_dir = base_dir, sub = sub_name, preproc = preproc)
    new_img = nb.Nifti1Image(dataobj = data_avg, affine = img.affine, header = img.header)
    new_img.to_filename(new_file)
                