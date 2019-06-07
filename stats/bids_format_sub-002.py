"""
-----------------------------------------------------------------------------------------
bids_generator.py
-----------------------------------------------------------------------------------------
Goal of the script:
Convert data in BIDS format
-----------------------------------------------------------------------------------------
Input(s):
sys.argv[1]: base directory (e.g. /home/shared/2018/visual/fMRIcourse/)
sys.argv[2]: subject raw name (e.g. pilot)
sys.argv[3]: subject bids number (e.g. sub-001)
sys.argv[4]: task name
-----------------------------------------------------------------------------------------
Output(s):
BIDS files
-----------------------------------------------------------------------------------------
To run:
cd to bids_generator.py folder
python bids_generator.py /home/shared/2018/visual/fMRIcourse/ pilot sub-001 StopSignal
-----------------------------------------------------------------------------------------
Written by Martin Szinte (martin.szinte@gmail.com)
-----------------------------------------------------------------------------------------
"""

# imports modules
import sys
import os
import glob
import nibabel as nb
import ipdb
opj = os.path.join
deb = ipdb.set_trace

# define data transfer command
trans_cmd = 'rsync -avuz --progress'


shared_dir 		= '/Users/martin/disks/ae_S/2018/visual/pRFgazeMod/'
raw_dir_ses1 	= '/Users/martin/disks/ae_R/2019/visual/prf_gazemod/sub-02_ses-01_prfGazeMod'
raw_dir_ses2 	= '/Users/martin/disks/ae_R/2019/visual/prf_gazemod/sub-02_ses-02_prfGazeMod'

task_cond = [	"task-AttendFixGazeCenterFS_run-1",				# run 01
				"task-AttendStimGazeCenterFS_run-1",			# run 02
				"task-AttendFixGazeCenterFS_run-2",				# run 03
				"task-AttendStimGazeCenterFS_run-2",			# run 04
				"task-AttendFixGazeLeft_run-1",					# run 05
				"task-AttendStimGazeLeft_run-1",				# run 06
				"task-AttendFixGazeRight_run-1",				# run 07
				"task-AttendStimGazeRight_run-1",				# run 08
				"task-AttendFixGazeCenter_run-1",				# run 09
				"task-AttendStimGazeCenter_run-1"]				# run 10

sub_name_bids = 'sub-002'

# create bids folders
bids_dir = opj(shared_dir,'bids_data')
for bids_folder in ['anat','fmap','func']:
	exec("{bids_folder}_dir = opj(bids_dir,sub_name_bids,'{ses_name}','{bids_folder}')".format(bids_folder = bids_folder, ses_name = 'ses-01'))
	try: exec("os.makedirs({}_dir)".format(bids_folder))
	except: pass

# Anat
# ----
# T1w


# Func
# ----
# bold runs
bold_files_ses1 =  ["sub-02_ses-01_prfGazeMod_task-AFGCFS_run-1_bold_20190605132040_401",		# run 01
					"sub-02_ses-01_prfGazeMod_task-ASGCFS_run-1_bold_20190605132040_601",		# run 02
					"sub-02_ses-01_prfGazeMod_task-AFGCFS_run-2_bold_20190605132040_801",		# run 03
					"sub-02_ses-01_prfGazeMod_task-ASGCFS_run-2_bold_20190605132040_1001",		# run 04
					"sub-02_ses-01_prfGazeMod_task-AFGL_run-1_bold_20190605132040_1201",		# run 05
					"sub-02_ses-01_prfGazeMod_task-ASGL_run-1_bold_20190605132040_1401",		# run 06
					"sub-02_ses-01_prfGazeMod_task-AFGR_run-1_bold_20190605132040_1601",		# run 07
					"sub-02_ses-01_prfGazeMod_task-ASGR_run-1_bold_20190605132040_1801",		# run 08
					"sub-02_ses-01_prfGazeMod_task-AFGC_run-1_bold_20190605132040_2001",		# run 09
					"sub-02_ses-01_prfGazeMod_task-ASGC_run-1_bold_20190605132040_2201"]		# run 10
					
epi_files_ses1 =   ["sub-02_ses-01_prfGazeMod_dir-TU_run-1_epi_20190605132040_501",				# run 01
					"sub-02_ses-01_prfGazeMod_dir-TU_run-2_epi_20190605132040_701",				# run 02
					"sub-02_ses-01_prfGazeMod_dir-TU_run-3_epi_20190605132040_901",				# run 03
					"sub-02_ses-01_prfGazeMod_dir-TU_run-4_epi_20190605132040_1101",			# run 04
					"sub-02_ses-01_prfGazeMod_dir-TU_run-5_epi_20190605132040_1301",			# run 05
					"sub-02_ses-01_prfGazeMod_dir-TU_run-6_epi_20190605132040_1501",			# run 06
					"sub-02_ses-01_prfGazeMod_dir-TU_run-7_epi_20190605132040_1701",			# run 07
					"sub-02_ses-01_prfGazeMod_dir-TU_run-8_epi_20190605132040_1901",			# run 08
					"sub-02_ses-01_prfGazeMod_dir-TU_run-9_epi_20190605132040_2101",			# run 09
					"sub-02_ses-01_prfGazeMod_dir-TU_run-10_epi_20190605132040_2301"]			# run 10


for run_num,bold_file in enumerate(bold_files_ses1):
	bold_run_raw = opj(raw_dir_ses1,'nifti',"{}.nii.gz".format(bold_file))
	bold_run_bids = opj(func_dir,"{sub}_ses-01_{task}_bold.nii.gz".format(sub = sub_name_bids, task = task_cond[run_num]))
	
	os.system("{cmd} {orig} {dest}".format(cmd = trans_cmd, orig = bold_run_raw, dest = bold_run_bids))
	deb()

# events runs
events_runs_raw = glob.glob(opj(raw_dir,sub_name_raw,'*events*'))
for run_num,events_run_raw in enumerate(events_runs_raw):
	events_run_bids = opj(func_dir,"{sub}_task-{task}_run-{run:.0f}_events.tsv".format(sub = sub_name_bids, task = task_name, run = run_num+1))
	os.system("{cmd} {orig} {dest}".format(cmd = trans_cmd, orig = events_run_raw, dest = events_run_bids))
