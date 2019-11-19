"""
-----------------------------------------------------------------------------------------
freesurfer_manual_edit.py
-----------------------------------------------------------------------------------------
Goal of the script:
Run freesurfer-dev version to change pial surface base on manual edits
-----------------------------------------------------------------------------------------
Input(s):
sys.argv[1]: subject
-----------------------------------------------------------------------------------------
Output(s):
new freesurfer segmentation files
-----------------------------------------------------------------------------------------
To run:
cd /home/mszinte/projects/pRFgazeMod/mri_analysis/
python pre_fit/freesurfer_manual_edit.py sub-001 pRFgazeMod 10
-----------------------------------------------------------------------------------------
Written by Martin Szinte (martin.szinte@gmail.com)
-----------------------------------------------------------------------------------------
"""

# imports modules
import os
import ipdb
import sys
import json
opj = os.path.join
deb = ipdb.set_trace

# inputs
subject = sys.argv[1]
project_dir = sys.argv[2]
hour_proc = int(sys.argv[3])

# Analysis parameters
with open('settings.json') as f:
    json_s = f.read()
    analysis_info = json.loads(json_s)

# Define cluster/server specific parameters
cluster_name = 'skylake'
base_dir = analysis_info['base_dir']
main_dir = '/scratch/mszinte/data/'
nb_procs = 8
memory_val = 48
proj_name = 'a161'
log_dir = opj(main_dir,project_dir,'deriv_data','fmriprep','log_outputs')

# define SLURM cmd
slurm_cmd = """\
#!/bin/bash
#SBATCH --mail-type=ALL
#SBATCH -p skylake
#SBATCH --mail-user=martin.szinte@univ-amu.fr
#SBATCH -A a161
#SBATCH --nodes=1
#SBATCH --mem={memory_val}gb
#SBATCH --cpus-per-task={nb_procs}
#SBATCH --time={hour_proc}:00:00
#SBATCH -e {log_dir}/{subject}_freesurfer-manual_edit_%N_%j_%a.err
#SBATCH -o {log_dir}/{subject}_freesurfer-manual_edit_%N_%j_%a.out
#SBATCH -J {subject}_freesurfer-manual_edit
#SBATCH --mail-type=BEGIN,END\n\n""".format(nb_procs = nb_procs, hour_proc = hour_proc, subject = subject,
											memory_val = memory_val, log_dir = log_dir)

# define subject directory
fs_dir = "{main_dir}{project_dir}/deriv_data/fmriprep/freesurfer/".format(main_dir = main_dir, project_dir = project_dir)
fs_licence = '/scratch/mszinte/freesurfer/license.txt'

freesurfer_cmd = """\
export SUBJECTS_DIR={fs_dir}\n\
export FS_LICENSE={fs_licence}\n\
recon-all -autorecon-pial -subjid {subject} -parallel -openmp {nb_procs}""".format(
	fs_dir = fs_dir, fs_licence = fs_licence, subject = subject, nb_procs = nb_procs)

# create sh folder and file
sh_dir = "{main_dir}/{project_dir}/deriv_data/fmriprep/jobs/{subject}_freesurfer-manual_edit.sh".format(main_dir = main_dir, subject = subject,project_dir = project_dir)

try:
	os.makedirs(opj(main_dir,project_dir,'deriv_data','fmriprep','jobs'))
	os.makedirs(opj(main_dir,project_dir,'deriv_data','fmriprep','log_outputs'))
except:
	pass

of = open(sh_dir, 'w')
of.write("{slurm_cmd}{freesurfer_cmd}".format(slurm_cmd = slurm_cmd,freesurfer_cmd = freesurfer_cmd))
of.close()

# Submit jobs
print("Submitting {sh_dir} to queue".format(sh_dir = sh_dir))
os.chdir(log_dir)
os.system("sbatch {sh_dir}".format(sh_dir = sh_dir))
