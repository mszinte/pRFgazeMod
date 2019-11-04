"""
-----------------------------------------------------------------------------------------
mriqc_sbatch.py
-----------------------------------------------------------------------------------------
Goal of the script:
Run frmiqc on mesocentre using job mode
-----------------------------------------------------------------------------------------
Input(s):
sys.argv[1]: main project directory
sys.argv[2]: project name (correspond to directory)
sys.argv[3]: bids subject num (e.g. 001)
sys.argv[4]: server nb of processor to use (e.g 32)
sys.argv[5]: server nb of hour to request (e.g 10)
-----------------------------------------------------------------------------------------
Output(s):
QC html files
-----------------------------------------------------------------------------------------
To run:
1. cd to function
>> cd /home/mszinte/projects/pRFgazeMod/mri_analysis/pre_fit/
2. run python command
python mriqc_sbatch.py [main directory] [project name] [subject num] 
					   [nb proc.] [hour proc.]
-----------------------------------------------------------------------------------------
Written by Martin Szinte (martin.szinte@gmail.com)
-----------------------------------------------------------------------------------------
"""

# imports modules
import sys
import os
import time
import ipdb
opj = os.path.join
deb = ipdb.set_trace

# inputs
singularity_dir = '/scratchw/mszinte/softwares/mriqc-0.15.1.simg'
main_dir = sys.argv[1]
project_dir = sys.argv[2]
subject = sys.argv[3]
sub_num = subject[-3:]
nb_procs = int(sys.argv[4])
job_dur = int(sys.argv[5])
cluster_name = 'westmere'
proj_name = 'westmere'

# create sh folder and file
jobs_dir = opj(main_dir,project_dir,'deriv_data','mriqc','jobs') 
log_dir = opj(main_dir,project_dir,'deriv_data','mriqc','log_outputs')
try:
	os.makedirs(jobs_dir)
	os.makedirs(log_dir)
except:
	pass

trans_cmd = 'rsync -avuz --progress'
orig_folder = "/scratch/mszinte/data/{project_dir}/bids_data/".format(project_dir = project_dir)
dest_folder = "/scratchw/mszinte/data/{project_dir}/bids_data".format(project_dir = project_dir)
os.system("{cmd} {orig} {dest}".format(cmd = trans_cmd, orig = orig_folder, dest = dest_folder))

slurm_cmd = """\
#!/bin/bash
#SBATCH -p {cluster_name}
#SBATCH -A {proj_name}
#SBATCH --nodes=1
#SBATCH --cpus-per-task={nb_procs}
#SBATCH --time={job_dur}
#SBATCH -e {log_dir}/{subject}_mriqc_%N_%j_%a.err
#SBATCH -o {log_dir}/{subject}_mriqc_%N_%j_%a.out
#SBATCH -J {subject}_mriqc\n\n""".format(
                    cluster_name = cluster_name,        proj_name = proj_name,
                    nb_procs = nb_procs,                log_dir = log_dir,
                    job_dur = job_dur,                  subject = subject)


# define singularity cmd
singularity_cmd = "singularity run --bind {main_dir}:/work_dir {simg} /work_dir/{project_dir}/bids_data/ /work_dir/{project_dir}/deriv_data/mriqc/ participant --participant_label {sub_num} -w /work_dir/{project_dir}/temp_data/ --n_procs {nb_procs:.0f} --verbose-reports -m bold T1w T2w --no-sub".format(
									main_dir = main_dir,
									project_dir = project_dir,
									simg = singularity_dir, 
									sub_num = sub_num,
									nb_procs = nb_procs,
									)

sh_dir = "{main_dir}/{project_dir}/deriv_data/mriqc/jobs/sub-{sub_num}_mriqc.sh".format(main_dir = main_dir, project_dir = project_dir, sub_num = sub_num)
of = open(sh_dir, 'w')
of.write("{slurm_cmd}{singularity_cmd}".format(slurm_cmd = slurm_cmd,singularity_cmd = singularity_cmd))
of.close()

# Submit jobs
print("Submitting {sh_dir} to queue".format(sh_dir = sh_dir))
os.chdir(log_dir)
os.system("sbatch {sh_dir}".format(sh_dir = sh_dir))
