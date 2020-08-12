"""
-----------------------------------------------------------------------------------------
pre_fit.py
-----------------------------------------------------------------------------------------
Goal of the script:
SG filter, PSC, AVG runs and combine data of both hemisphere
-----------------------------------------------------------------------------------------
Input(s):
sys.argv[1]: subject name
sys.argv[2]: start voxel index
sys.argv[3]: end voxel index
sys.argv[4]: data file path
sys.argv[5]: main directory
-----------------------------------------------------------------------------------------
Output(s):
# Preprocessed timeseries files
-----------------------------------------------------------------------------------------
To run:
python pre_fit/pre_fit.py
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
import ipdb
import platform
import numpy as np
opj = os.path.join
deb = ipdb.set_trace

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
for sub_name in analysis_info['subject_list'] :

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

    # Compute percent signal change
    for preproc in analysis_info['preproc']:
        file_list = sorted(glob.glob("{base_dir}/pp_data/{sub}/func/{preproc}/*{preproc}.nii.gz".format(
                                             base_dir = base_dir, sub = sub_name, preproc = preproc)))
        for file in file_list:
            print('psc:'+file)
            img = nb.load(file)
            pp_data = img.get_fdata()
            pp_data_median = np.median(pp_data, axis=3)
            pp_data_median = np.repeat(pp_data_median[:, :, :, np.newaxis], pp_data.shape[3], axis=3)
            pp_data_psc = 100.0 * (pp_data - pp_data_median)/pp_data_median

            # save
            new_file = "{file}_psc.nii.gz".format(file = file[:-7])
            new_img = nb.Nifti1Image(dataobj = pp_data_psc, affine = img.affine, header = img.header)
            new_img.to_filename(new_file)

    # Average tasks runs
    for preproc in analysis_info['preproc']:
        for attend_cond in analysis_info['attend_cond']:
            for gaze_cond in analysis_info['gaze_cond']:
                file_list = sorted(glob.glob("{base_dir}/pp_data/{sub}/func/{preproc}/*{attend_cond}{gaze_cond}_*_psc.nii.gz".format(
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
                new_file = "{base_dir}/pp_data/{sub}/func/{sub}_task-{attend_cond}{gaze_cond}_{preproc}_psc_avg.nii.gz".format(
                            base_dir = base_dir, sub = sub_name, preproc = preproc, 
                            attend_cond = attend_cond, gaze_cond = gaze_cond)
                new_img = nb.Nifti1Image(dataobj = data_avg, affine = img.affine, header = img.header)
                new_img.to_filename(new_file)
                