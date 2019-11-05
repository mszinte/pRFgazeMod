"""
-----------------------------------------------------------------------------------------
mriqc_sbatch.py
-----------------------------------------------------------------------------------------
Goal of the script:
Run fMRIprep on mesocentre using job mode
-----------------------------------------------------------------------------------------
Input(s):
sys.argv[1]: main data directory
sys.argv[2]: project name (correspond to directory)
sys.argv[3]: cluster name ('westmere','skylake')
sys.argv[4]: subject (e.g. sub-001)
sys.argv[5]: server nb of hour to request (e.g 10)
sys.argv[6]: anat only (1) or not (0)
sys.argv[7]: use of aroma (1) or not (0)
sys.argv[8]: Use Use fieldmap-free distortion correction
-----------------------------------------------------------------------------------------
Output(s):
preprocessed files
-----------------------------------------------------------------------------------------
To run:
1. cd to function
>> cd /scratch/mszinte/projects/pRFseqTest/mri_analysis/pre_fit/
2. run python command
python fmriprep_sbatch.py [main directory] [project name] [cluster name] [subject num]
						  [hour proc.] [anat_only] [use_aroma] [fmapfree]
-----------------------------------------------------------------------------------------
Written by Martin Szinte (martin.szinte@gmail.com)
-----------------------------------------------------------------------------------------
"""

# imports modules
import sys
import os
import time
import ipdb
import json
import ipdb
opj = os.path.join
deb = ipdb.set_trace

# inputs
singularity_dir = '/scratch/mszinte/softwares/fmriprep-1.5.0.simg'
main_dir = sys.argv[1]
project_dir = sys.argv[2]
cluster_name = sys.argv[3]
subject = sys.argv[4]
sub_num = subject[-3:]
hour_proc = int(sys.argv[5])
anat = int(sys.argv[6])
aroma = int(sys.argv[7])
fmapfree = int(sys.argv[8])

# Analysis parameters
with open('settings.json') as f:
    json_s = f.read()
    analysis_info = json.loads(json_s)

# Define cluster/server specific parameters
if cluster_name  == 'skylake':
    nb_procs = 32
    memory_val = 48
    proj_name = 'a161'
    os.system("rsync -az --no-g --no-p --progress {scratchw}/ {scratch}".format(
                scratch = analysis_info['base_dir'],
                scratchw  = analysis_info['base_dir_westmere']))

elif cluster_name  == 'westmere':
	proj_name = 'westmere'
    nb_procs = 12
    memory_val = 24
    os.system("rsync -az --no-g --no-p --progress {scratch}/ {scratchw}".format(
        scratch = analysis_info['base_dir'],
        scratchw  = base_dir))

# special input
anat_only, use_aroma, use_fmapfree, anat_only_end = '','','', ''
if anat == 1:
	anat_only = ' --anat-only'
	anat_only_end = '_anat'
if aroma == 1:
	use_aroma = ' --use-aroma'
if fmapfree == 1:
	use_fmapfree= ' --use-syn-sdc'

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
#SBATCH -e  %N.%j.%a.err
#SBATCH -o %N.%j.%a.out
#SBATCH -J sub-{sub_num}_fmriprep{anat_only_end}
#SBATCH --mail-type=BEGIN,END\n\n""".format(nb_procs = nb_procs, hour_proc = hour_proc, sub_num = sub_num,anat_only_end = anat_only_end, memory_val = memory_val)

# define singularity cmd
singularity_cmd = "singularity run --cleanenv -B {main_dir}:/work_dir {simg} --fs-license-file /work_dir/freesurfer/license.txt /work_dir/{project_dir}/bids_data/ /work_dir/{project_dir}/deriv_data/fmriprep/ participant --participant-label {sub_num} -w /work_dir/{project_dir}/temp_data/ --output-space T1w fsaverage --cifti-output --low-mem --mem-mb 32000 --nthreads {nb_procs:.0f}{anat_only}{use_aroma}{use_fmapfree}".format(
									main_dir = main_dir,
									project_dir = project_dir,
									simg = singularity_dir,
									sub_num = sub_num,
									nb_procs = nb_procs,
									anat_only = anat_only,
									use_aroma = use_aroma,
									use_fmapfree = use_fmapfree)

# create sh folder and file
sh_dir = "{main_dir}/{project_dir}/deriv_data/fmriprep/jobs/sub-{sub_num}_fmriprep.sh".format(main_dir = main_dir, sub_num = sub_num,project_dir = project_dir,)

try:
	os.makedirs(opj(main_dir,project_dir,'deriv_data','fmriprep','jobs'))
	os.makedirs(opj(main_dir,project_dir,'deriv_data','fmriprep','log_outputs'))
except:
	pass
of = open(sh_dir, 'w')
of.write("{slurm_cmd}{singularity_cmd}".format(slurm_cmd = slurm_cmd,singularity_cmd = singularity_cmd))
of.close()

# Submit jobs
print("Submitting {sh_dir} to queue".format(sh_dir = sh_dir))
os.chdir(opj(main_dir,project_dir,'deriv_data','fmriprep','log_outputs'))
os.system("sbatch {sh_dir}".format(sh_dir = sh_dir))

