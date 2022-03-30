"""
-----------------------------------------------------------------------------------------
roi_to_padas.py
-----------------------------------------------------------------------------------------
Goal of the script:
Create dataframe per subject for dash app
-----------------------------------------------------------------------------------------
Input(s):
sys.argv[1]: floating number (e.g. 2)
-----------------------------------------------------------------------------------------
Output(s):
csv compressed dataframes
-----------------------------------------------------------------------------------------
To run:
>> cd to function
>> python post_fit/roi_to_pandas.py [float_num]
-----------------------------------------------------------------------------------------
Exemple:
cd /home/mszinte/projects/pRFgazeMod/mri_analysis/
python post_fit/roi_to_pandas.py2
-----------------------------------------------------------------------------------------
Written by Martin Szinte (martin.szinte@gmail.com)
-----------------------------------------------------------------------------------------
"""

# general imports
import sys
import os
import numpy as np
import h5py
import pandas as pd
import json

# input
float_num = int(sys.argv[1])

# define analysis parameters
with open('settings.json') as f:
    json_s = f.read()
    analysis_info = json.loads(json_s)

base_dir = analysis_info['base_dir']
app_dir = analysis_info['app_data_dir']

for subject in analysis_info['subject_list']:

    # data
    h5_dir = "{base_dir}/pp_data/{subject}/gauss/h5".format(base_dir = base_dir, subject = subject)
    pandas_dir = "{base_dir}/pp_data/{subject}/gauss/pandas".format(base_dir = base_dir, subject = subject)
    try: os.makedirs(pandas_dir)
    except: pass

    # load deriv data
    rsq_idx, ecc_idx, polar_real_idx, polar_imag_idx , size_idx, \
        amp_idx, baseline_idx, cov_idx, x_idx, y_idx, hemi_idx = 0,1,2,3,4,5,6,7,8,9,10
    rsq_dict, ecc_dict, polar_real_dict, polar_imag_dict, size_dict, x_dict, y_dict, hemi_dict = {}, {}, {}, {}, {}, {}, {}, {}
    ecc_sample_dict, size_sample_dict = {}, {}

    # create raw dataframe
    df_raw = pd.DataFrame()
    for task in analysis_info['analysis_tasks']:
        for preproc in analysis_info['preproc']:

            for roi in analysis_info['rois']:
                
                h5_file = h5py.File("{h5_dir}/{roi}_{task}_{preproc}.h5".format(h5_dir = h5_dir, roi = roi, task = task, preproc = preproc),'r')
                deriv_data = h5_file['{folder_alias}/derivatives'.format(folder_alias = 'pRF')]
                df_roi = pd.DataFrame(deriv_data,columns = ['rsq','ecc','polar_real','polar_imag','size','amp','baseline','cov','x','y','hemi'])
                df_roi['roi']=[roi for x in range(df_roi.shape[0])]
                df_roi['subject']=[subject for x in range(df_roi.shape[0])]
                df_roi['task']=[task for x in range(df_roi.shape[0])]
                df_roi['preproc']=[preproc for x in range(df_roi.shape[0])]
                df_raw = pd.concat([df_raw, df_roi],ignore_index=True, axis = 0)

            # save dataframe
            df_filename = '{pandas_dir}/{subject}_{task}_{preproc}.gz'.format(pandas_dir=pandas_dir, subject=subject, task=task, preproc=preproc)
            df_app_filename = '{app_dir}/{subject}_{task}_{preproc}.gz'.format(app_dir=app_dir, subject=subject, task=task, preproc=preproc)
            print('saving {}'.format(df_filename))
            df_raw.to_csv(df_filename, compression='gzip', float_format='%.{}f'.format(float_num))
            print('saving {}'.format(df_app_filename))
            df_raw.to_csv(df_app_filename, compression='gzip', float_format='%.{}f'.format(float_num))
