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
shared_dir 		= '/home/shared/2018/visual/pRFgazeMod/'

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

epi_cond = 	[	"dir-TU_run-01",								# run 01
				"dir-TU_run-02",								# run 02
				"dir-TU_run-03",								# run 03
				"dir-TU_run-04",								# run 04
				"dir-TU_run-05",								# run 05
				"dir-TU_run-06",								# run 06
				"dir-TU_run-07",								# run 07
				"dir-TU_run-08",								# run 08
				"dir-TU_run-09",								# run 09
				"dir-TU_run-10"]								# run 10

sub_name_bids = 'sub-002'

# Anat
# ----
# T1w


# Func
# ----
# bold runs
raw_dir_ses1 	= '/home/raw_data/2019/visual/prf_gazemod/sub-02_ses-01_prfGazeMod/'

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


raw_dir_ses2 	= '/home/raw_data/2019/visual/prf_gazemod/sub-02_ses-02_prfGazeMod/'
bold_files_ses2 =  ["sub-02_ses-01_prfGazeMod_task-AFGCFS_run-1_bold_20190605132040_401",		# run 01
					"sub-02_ses-01_prfGazeMod_task-ASGCFS_run-1_bold_20190605132040_601",		# run 02
					"sub-02_ses-01_prfGazeMod_task-AFGCFS_run-2_bold_20190605132040_801",		# run 03
					"sub-02_ses-01_prfGazeMod_task-ASGCFS_run-2_bold_20190605132040_1001",		# run 04
					"sub-02_ses-01_prfGazeMod_task-AFGL_run-1_bold_20190605132040_1201",		# run 05
					"sub-02_ses-01_prfGazeMod_task-ASGL_run-1_bold_20190605132040_1401",		# run 06
					"sub-02_ses-01_prfGazeMod_task-AFGR_run-1_bold_20190605132040_1601",		# run 07
					"sub-02_ses-01_prfGazeMod_task-ASGR_run-1_bold_20190605132040_1801",		# run 08
					"sub-02_ses-01_prfGazeMod_task-AFGC_run-1_bold_20190605132040_2001",		# run 09
					"sub-02_ses-01_prfGazeMod_task-ASGC_run-1_bold_20190605132040_2201"]		# run 10
					


for session in ['ses-01','ses-02']:
	if session == 'ses-01':
		raw_dir_ses = raw_dir_ses1
		bold_files_ses = bold_files_ses1
		epi_files_ses = epi_files_ses1
	elif session == 'ses-02':
		raw_dir_ses = raw_dir_ses2
		bold_files_ses = bold_files_ses2
		epi_files_ses = epi_files_ses2

	# create bids folders
	bids_dir = opj(shared_dir,'bids_data')
	for bids_folder in ['anat','fmap','func']:
		exec("{bids_folder}_dir = opj(bids_dir,sub_name_bids,'{ses_name}','{bids_folder}')".format(bids_folder = bids_folder, ses_name = session))
		try: exec("os.makedirs({}_dir)".format(bids_folder))
		except: pass

	for type_data in ['nii.gz','json']:

		# bold files
		for run_num,bold_file in enumerate(bold_files_ses):
			bold_run_raw = opj(raw_dir_ses,'nifti',"{bold_file}.{type_data}".format(bold_file = bold_file, type_data = type_data))
			bold_run_bids = opj(func_dir,"{sub}_{session}_{task_cond}_bold.{type_data}".format(sub = sub_name_bids, task_cond = task_cond[run_num], type_data = type_data, session = session))

			os.system("{cmd} {orig} {dest}".format(cmd = trans_cmd, orig = bold_run_raw, dest = bold_run_bids))
	
		# epi files
		for run_num,epi_file in enumerate(epi_files_ses):
			epi_run_raw = opj(raw_dir_ses,'nifti',"{epi_file}.{type_data}".format(epi_file = epi_file, type_data = type_data))
			epi_run_bids = opj(fmap_dir,"{sub}_{session}_{epi_cond}_epi.{type_data}".format(sub = sub_name_bids, epi_cond = epi_cond[run_num], type_data = type_data, session = session))

			os.system("{cmd} {orig} {dest}".format(cmd = trans_cmd, orig = epi_run_raw, dest = epi_run_bids))
	

	deb()