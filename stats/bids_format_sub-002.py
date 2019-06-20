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
import json
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

# Session 1
# ---------

raw_dir_ses1 		= '/home/raw_data/2019/visual/prf_gazemod/sub-002_ses-01_prfGazeMod/'
raw_behav_dir_ses1 	= '/home/raw_data/2019/visual/prf_gazemod/sub-002_behav/ses-01/func/'

bold_files_ses1 =  ["parrec_task-AFGCFS_run-1_bold_20190605132040_4",		# run 01
					"parrec_task-ASGCFS_run-1_bold_20190605132040_6",		# run 02
					"parrec_task-AFGCFS_run-2_bold_20190605132040_8",		# run 03
					"parrec_task-ASGCFS_run-2_bold_20190605132040_10",		# run 04
					"parrec_task-AFGL_run-1_bold_20190605132040_12",		# run 05
					"parrec_task-ASGL_run-1_bold_20190605132040_14",		# run 06
					"parrec_task-AFGR_run-1_bold_20190605132040_16",		# run 07
					"parrec_task-ASGR_run-1_bold_20190605132040_18",		# run 08
					"parrec_task-AFGC_run-1_bold_20190605132040_20",		# run 09
					"parrec_task-ASGC_run-1_bold_20190605132040_22"]		# run 10

epi_files_ses1 =   ["parrec_dir-TU_run-1_epi_20190605132040_5",				# run 01
					"parrec_dir-TU_run-2_epi_20190605132040_7",				# run 02
					"parrec_dir-TU_run-3_epi_20190605132040_9",				# run 03
					"parrec_dir-TU_run-4_epi_20190605132040_11",			# run 04
					"parrec_dir-TU_run-5_epi_20190605132040_13",			# run 05
					"parrec_dir-TU_run-6_epi_20190605132040_15",			# run 06
					"parrec_dir-TU_run-7_epi_20190605132040_17",			# run 07
					"parrec_dir-TU_run-8_epi_20190605132040_19",			# run 08
					"parrec_dir-TU_run-9_epi_20190605132040_21",			# run 09
					"parrec_dir-TU_run-10_epi_20190605132040_23"]			# run 10


bold_physio_files_ses1 =	[	"SCANPHYSLOG20190605133352",				# run 01
								"SCANPHYSLOG20190605133844",				# run 02
								"SCANPHYSLOG20190605134331",				# run 03
								"SCANPHYSLOG20190605134806",				# run 04
								"SCANPHYSLOG20190605135249",				# run 05
								"SCANPHYSLOG20190605135636",				# run 06
								"SCANPHYSLOG20190605140027",				# run 07
								"SCANPHYSLOG20190605140413",				# run 08
								"SCANPHYSLOG20190605140806",				# run 09
								"SCANPHYSLOG20190605141200"]				# run 10

epi_physio_files_ses1 =	[		"SCANPHYSLOG20190605133743",				# run 01
								"SCANPHYSLOG20190605134235",				# run 02
								"SCANPHYSLOG20190605134722",				# run 03
								"SCANPHYSLOG20190605135157",				# run 04
								"SCANPHYSLOG20190605135602",				# run 05
								"SCANPHYSLOG20190605135949",				# run 06
								"SCANPHYSLOG20190605140341",				# run 07
								"SCANPHYSLOG20190605140727",				# run 08
								"SCANPHYSLOG20190605141120",				# run 09
								"SCANPHYSLOG20190605141514"]				# run 10

# Session 2
# ---------

raw_dir_ses2 	= '/home/raw_data/2019/visual/prf_gazemod/sub-002_ses-02_prfGazeMod/'
raw_behav_dir_ses2 	= '/home/raw_data/2019/visual/prf_gazemod/sub-002_behav/ses-02/func/'
					
bold_files_ses2 =  ["parrec_task-AFGCFS_run-1_bold_20190606152444_4",		# run 01
					"parrec_task-ASGCFS_run-1_bold_20190606152444_6",		# run 02
					"parrec_task-AFGCFS_run-2_bold_20190606152444_8",		# run 03
					"parrec_task-ASGCFS_run-2_bold_20190606152444_10",		# run 04
					"parrec_task-AFGL_run-1_bold_20190606152444_12",		# run 05
					"parrec_task-ASGL_run-1_bold_20190606152444_14",		# run 06
					"parrec_task-AFGR_run-1_bold_20190606152444_16",		# run 07
					"parrec_task-ASGR_run-1_bold_20190606152444_18",		# run 08
					"parrec_task-AFGC_run-1_bold_20190606152444_20",		# run 09
					"parrec_task-ASGC_run-1_bold_20190606152444_22"]		# run 10

epi_files_ses2 =   ["parrec_dir-TU_run-1_epi_20190606152444_5",				# run 01
					"parrec_dir-TU_run-2_epi_20190606152444_7",				# run 02
					"parrec_dir-TU_run-3_epi_20190606152444_9",				# run 03
					"parrec_dir-TU_run-4_epi_20190606152444_11",			# run 04
					"parrec_dir-TU_run-5_epi_20190606152444_13",			# run 05
					"parrec_dir-TU_run-6_epi_20190606152444_15",			# run 06
					"parrec_dir-TU_run-7_epi_20190606152444_17",			# run 07
					"parrec_dir-TU_run-8_epi_20190606152444_19",			# run 08
					"parrec_dir-TU_run-9_epi_20190606152444_21",			# run 09
					"parrec_dir-TU_run-10_epi_20190606152444_23"]			# run 10

bold_physio_files_ses2 =	[	"SCANPHYSLOG20190606154225",				# run 01
								"SCANPHYSLOG20190606154656",				# run 02
								"SCANPHYSLOG20190606155129",				# run 03
								"SCANPHYSLOG20190606155559",				# run 04
								"SCANPHYSLOG20190606160030",				# run 05
								"SCANPHYSLOG20190606160419",				# run 06
								"SCANPHYSLOG20190606160816",				# run 07
								"SCANPHYSLOG20190606161202",				# run 08
								"SCANPHYSLOG20190606161814",				# run 09
								"SCANPHYSLOG20190606162211"]				# run 10

epi_physio_files_ses2 =	[		"SCANPHYSLOG20190606154616",				# run 01
								"SCANPHYSLOG20190606155047",				# run 02
								"SCANPHYSLOG20190606155520",				# run 03
								"SCANPHYSLOG20190606155950",				# run 04
								"SCANPHYSLOG20190606160344",				# run 05
								"SCANPHYSLOG20190606160733",				# run 06
								"SCANPHYSLOG20190606161129",				# run 07
								"SCANPHYSLOG20190606161706",				# run 08
								"SCANPHYSLOG20190606162129",				# run 09
								"SCANPHYSLOG20190606162525"]				# run 10

for session in ['ses-01','ses-02']:
	if session == 'ses-01':
		raw_dir_ses = raw_dir_ses1
		bold_files_ses = bold_files_ses1
		epi_files_ses = epi_files_ses1
		bold_physio_files_ses = bold_physio_files_ses1
		epi_physio_files_ses = epi_physio_files_ses1
		raw_behav_dir_ses = raw_behav_dir_ses1
	elif session == 'ses-02':
		raw_dir_ses = raw_dir_ses2
		bold_files_ses = bold_files_ses2
		epi_files_ses = epi_files_ses2
		bold_physio_files_ses = bold_physio_files_ses2
		epi_physio_files_ses = epi_physio_files_ses2
		raw_behav_dir_ses = raw_behav_dir_ses2

	# create bids folders
	bids_dir = opj(shared_dir,'bids_data')
	for bids_folder in ['anat','fmap','func']:
		exec("{bids_folder}_dir = opj(bids_dir,sub_name_bids,'{ses_name}','{bids_folder}')".format(bids_folder = bids_folder, ses_name = session))
		try: exec("os.makedirs({}_dir)".format(bids_folder))
		except: pass

	# t1w data
	raw_t1w = '/home/shared/2017/visual/pRF_gazeMod/sourcedata/sub-002/anat/sub-002_T1w.nii.gz'
	bids_t1w = opj(anat_dir,"{sub}_{session}_T1w.nii.gz".format(sub = sub_name_bids, session = session))
	os.system("{cmd} {orig} {dest}".format(cmd = trans_cmd, orig = raw_t1w, dest = bids_t1w))


	for type_data in ['nii.gz','json']:

		# bold files
		for run_num,bold_file in enumerate(bold_files_ses):
			bold_run_raw = opj(raw_dir_ses,'parrec','nifti',"{bold_file}.{type_data}".format(bold_file = bold_file, type_data = type_data))
			bold_run_bids = opj(func_dir,"{sub}_{session}_{task_cond}_bold.{type_data}".format(sub = sub_name_bids, task_cond = task_cond[run_num], type_data = type_data, session = session))
			os.system("{cmd} {orig} {dest}".format(cmd = trans_cmd, orig = bold_run_raw, dest = bold_run_bids))
	
		# epi files
		for run_num,epi_file in enumerate(epi_files_ses):
			epi_run_raw = opj(raw_dir_ses,'parrec','nifti',"{epi_file}.{type_data}".format(epi_file = epi_file, type_data = type_data))
			epi_run_bids = opj(fmap_dir,"{sub}_{session}_{epi_cond}_epi.{type_data}".format(sub = sub_name_bids, epi_cond = epi_cond[run_num], type_data = type_data, session = session))
			os.system("{cmd} {orig} {dest}".format(cmd = trans_cmd, orig = epi_run_raw, dest = epi_run_bids))

			# add entry to epi json files
			if type_data == 'json':
				add_entry = False

				with open(epi_run_bids) as f:
					json_s = f.read()
					json_dict = json.loads(json_s)

				if 'PhaseEncodingDirection' in json_dict: None
				else: 
					json_dict.update({"PhaseEncodingDirection": "i-"})
					add_entry = True

				if 'TotalReadoutTime' in json_dict: None
				else:
					json_dict.update({"TotalReadoutTime": 0.0322})
					add_entry = True

				if 'IntendedFor' in json_dict: None
				else: 
					json_dict.update({"IntendedFor": ["{session}/func/{sub}_{session}_{task_cond}_bold.nii.gz".format(sub = sub_name_bids, task_cond = task_cond[run_num], session = session)]})
					add_entry = True

				if add_entry == True:
					with open(epi_run_bids, 'w') as json_file:
						json.dump(json_dict, json_file)

	# bold physio
	for run_num,bold_physio_file in enumerate(bold_physio_files_ses):
		bold_physio_run_raw = opj(raw_dir_ses,'scanphysiolog_all',"{bold_physio_file}.log".format(bold_physio_file = bold_physio_file))
		bold_physio_run_bids = opj(func_dir,"{sub}_{session}_{task_cond}_physio.log".format(sub = sub_name_bids, task_cond = task_cond[run_num], session = session))
		os.system("{cmd} {orig} {dest}".format(cmd = trans_cmd, orig = bold_physio_run_raw, dest = bold_physio_run_bids))
		
	# epi physio
	for run_num,epi_physio_file in enumerate(epi_physio_files_ses):
		epi_physio_run_raw = opj(raw_dir_ses,'scanphysiolog_all',"{epi_physio_file}.log".format(epi_physio_file = epi_physio_file))
		epi_physio_run_bids = opj(fmap_dir,"{sub}_{session}_{epi_cond}_physio.log".format(sub = sub_name_bids, epi_cond = epi_cond[run_num], session = session))
		os.system("{cmd} {orig} {dest}".format(cmd = trans_cmd, orig = epi_physio_run_raw, dest = epi_physio_run_bids))

	# behavior and log
	os.system("{cmd} {orig} {dest}".format(cmd = trans_cmd, orig = raw_behav_dir_ses, dest = func_dir))
	

# Session 3
# ---------
raw_dir_ses3 = '/home/raw_data/2019/visual/prf_gazemod/sub-002_anat/'

anat_cond = [	'acq-ADNI_run-1_T1w',							# T1 weighted ADNI run 01
				'acq-ADNI_run-2_T1w',							# T1 weighted ADNI run 02
				'acq-PHILLIPS_run-1_T1w',						# T1 weighted Phillips run 01
				'acq-PHILLIPS_run-2_T1w',						# T1 weighted Phillips run 02
				'T2w',											# T2 weighted
				'FLAIR']										# 3D FLAIR


anat_files_ses3 = [	'parrec_acq-1mm-sag_T1w_6m12s_ADNI_20190620105436_3',	# T1 weighted ADNI run 01
					'parrec_acq-1mm-sag_T1w_6m12s_ADNI_20190620105436_9',	# T1 weighted ADNI run 02
					'parrec_acq-1mm-sag_T1w_3m54s_Philips_20190620105436_5',# T1 weighted Phillips run 01
					'parrec_acq-1mm-sag_T1w_3m54s_Philips_20190620105436_8',# T1 weighted Phillips run 02
					'parrec_3DT2_1mm_20190620105436_7',						# T2 weighted
					'parrec_3DFLAIR_recon1mm_6min_20190620105436_6']		# 3D FLAIR

for session in ['ses-03']:
	if session == 'ses-03':
		raw_dir_ses = raw_dir_ses3
		anat_files_ses = anat_files_ses3
		
	# create bids folders
	bids_dir = opj(shared_dir,'bids_data')
	for bids_folder in ['anat']:
		exec("{bids_folder}_dir = opj(bids_dir,sub_name_bids,'{ses_name}','{bids_folder}')".format(bids_folder = bids_folder, ses_name = session))
		try: exec("os.makedirs({}_dir)".format(bids_folder))
		except: pass


	for type_data in ['nii.gz','json']:

		# anat files
		for run_num,anat_file in enumerate(anat_files_ses):
			anat_run_raw = opj(raw_dir_ses,'parrec','nifti',"{anat_file}.{type_data}".format(anat_file = anat_file, type_data = type_data))
			anat_run_bids = opj(anat_dir,"{sub}_{session}_{anat_cond}.{type_data}".format(sub = sub_name_bids, anat_cond = anat_cond[run_num], type_data = type_data, session = session))
			os.system("{cmd} {orig} {dest}".format(cmd = trans_cmd, orig = anat_run_raw, dest = anat_run_bids))
		
