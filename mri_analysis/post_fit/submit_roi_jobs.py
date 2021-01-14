"""
-----------------------------------------------------------------------------------------
submit_roi_jobs.py
-----------------------------------------------------------------------------------------
Goal of the script:
Create jobscript to analyse data per roi
-----------------------------------------------------------------------------------------
Input(s):
sys.argv[1]: subject name (e.g. 'sub-01')
sys.argv[2]: task (ex: GazeCenterFS)
sys.argv[3]: pre-processing steps (fmriprep_dct or fmriprep_dct_pca)
-----------------------------------------------------------------------------------------
Output(s):
.sh file to execute in server
-----------------------------------------------------------------------------------------
To run:
>> cd to function
>> python fit/submit_fit_fs_jobs.py [subject] [task] [preproc]
-----------------------------------------------------------------------------------------
Exemple:
cd /home/mszinte/projects/pRFgazeMod/mri_analysis/
python post_fit/submit_roi_jobs.py sub-001 GazeCenterFS fmriprep_dct
python post_fit/submit_roi_jobs.py sub-001 GazeCenterFS fmriprep_dct_pca
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
import numpy as np
import os
import glob
import json
import sys
import nibabel as nb
import platform
import ipdb
import datetime
deb = ipdb.set_trace
opj = os.path.join

# Settings
# --------
# Inputs
subject = sys.argv[1]
task = sys.argv[2]
preproc = sys.argv[3]

# Analysis parameters
with open('settings.json') as f:
    json_s = f.read()
    analysis_info = json.loads(json_s)

# Cluster settings
base_dir = analysis_info['base_dir']
sub_command = 'sbatch '
proj_name = 'b161'
job_dur = '04:00:00'

print("ROI analysis: running on Skylake")

# Create job and log output folders
try:
    os.makedirs(opj(base_dir, 'pp_data', subject, 'gauss', 'jobs'))
    os.makedirs(opj(base_dir, 'pp_data', subject, 'gauss', 'log_outputs'))
except:
    pass
log_dir = opj(base_dir,'pp_data',subject,'gauss','log_outputs')

# Determine data to analyse

slurm_cmd = """\
#!/bin/bash
#SBATCH -p skylake
#SBATCH -A {proj_name}
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=48gb
#SBATCH --time={job_dur}
#SBATCH -e {log_dir}/{subject}_{task}_{preproc}_roi_%N_%j_%a.err
#SBATCH -o {log_dir}/{subject}_{task}_{preproc}_roi_%N_%j_%a.out
#SBATCH -J {subject}_{task}_{preproc}_roi\n\n""".format(
            proj_name = proj_name,
            log_dir = log_dir,
            job_dur = job_dur,
            subject = subject,
            preproc = preproc,
            task = task)

# define roi cmd
roi_cmd1 = "python post_fit/roi_to_hdf5.py {subject} {task} {preproc}".format(
                subject = subject,
                task = task,
                preproc = preproc)

roi_cmd2 = "python post_fit/roi_plots.py {subject} {task} {preproc} 0".format(
                subject = subject,
                task = task,
                preproc = preproc)

# create sh folder and file
sh_dir = "{base_dir}/pp_data/{subject}/gauss/jobs/{subject}_{task}_{preproc}_roi.sh".format(
        base_dir = base_dir,
        subject = subject,
        task = task,
        preproc = preproc)

try:
    os.makedirs(opj(base_dir,'pp_data',subject,'gauss','jobs'))
    os.makedirs(opj(base_dir,'pp_data',subject,'gauss','log_outputs'))
except:
    pass

of = open(sh_dir, 'w')
of.write("{slurm_cmd}\n{roi_cmd1}\n{roi_cmd2}".format(
    slurm_cmd = slurm_cmd,
    roi_cmd1 = roi_cmd1,
    roi_cmd2 = roi_cmd2))

of.close()

# Submit jobs
print("Submitting {sh_dir} to queue".format(sh_dir = sh_dir))
os.system("{sub_command} {sh_dir}".format(sub_command = sub_command, sh_dir = sh_dir))
