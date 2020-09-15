"""
-----------------------------------------------------------------------------------------
pycortex_maps.py
-----------------------------------------------------------------------------------------
Goal of the script:
Display cortical data with pycortex 
-----------------------------------------------------------------------------------------
Input(s):
sys.argv[1]: subject name (e.g. 'sub-001')
sys.argv[2]: task (ex: GazeCenterFS)
sys.argv[3]: pre-processing steps (fmriprep_dct or fmriprep_dct_pca)
sys.argv[4]: save SVG (0  = No, 1 = Yes)
sys.argv[5]: save timecourses
-----------------------------------------------------------------------------------------
Output(s):
pyxortex maps
-----------------------------------------------------------------------------------------
To run:
>> cd to function
>> python post_fit/pycortex_maps.py [subject] [task] [preproc] [svg] [tc]
-----------------------------------------------------------------------------------------
Exemple:
cd /Users/martin/disks/meso_H/projects/pRFgazeMod/mri_analysis/
python post_fit/pycortex_maps.py sub-001 GazeCenterFS fmriprep_dct 0 0
python post_fit/pycortex_maps.py sub-002 GazeCenterFS fmriprep_dct 0 0
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
import os
import shutil
import sys
import json
import numpy as np
import ipdb
import matplotlib.pyplot as plt
opj = os.path.join
deb = ipdb.set_trace

# MRI imports
# -----------
import nibabel as nb
import cortex

# Functions import
# ----------------
from utils import draw_cortex_vertex, set_pycortex_config_file

# Get inputs
# ----------
subject = sys.argv[1]
task = sys.argv[2]
preproc = sys.argv[3]
save_svg = int(sys.argv[4])
if save_svg == 1: save_svg = True
else: save_svg = False
plot_tc = int(sys.argv[5])

# Define analysis parameters
# --------------------------
with open('settings.json') as f:
    json_s = f.read()
    analysis_info = json.loads(json_s)

# Define folder
# -------------
xfm_name = "identity.fmriprep"
base_dir = analysis_info['base_dir_local']
deriv_dir = "{base_dir}/pp_data/{subject}/gauss/fit".format(base_dir = base_dir,subject = subject)
cortex_dir = "{base_dir}/pp_data/cortex/db/{subject}".format(base_dir = base_dir, subject = subject)
fs_dir = "{base_dir}/deriv_data/fmriprep/freesurfer/".format(base_dir = base_dir)
fmriprep_dir = "{base_dir}/deriv_data/fmriprep/".format(base_dir = base_dir)
bids_dir = "{base_dir}/bids_data/".format(base_dir = base_dir)

# Set pycortex db and colormaps
# -----------------------------
set_pycortex_config_file(base_dir)

# Pycortex plots
# --------------
rsq_idx, ecc_idx, polar_real_idx, polar_imag_idx , size_idx, \
    amp_idx, baseline_idx, cov_idx, x_idx, y_idx = 0,1,2,3,4,5,6,7,8,9

cmap_polar = 'hsv'
cmap_uni = 'Reds'
cmap_ecc_size = 'Spectral'
col_offset = 1/14.0
cmap_steps = 255

print('save pycortex flatmaps')
maps_names = []
flatmaps_dir = opj(base_dir,"pp_data",subject,"gauss","pycortex_outputs","flatmaps")
dataset_dir = opj(base_dir,"pp_data",subject,"gauss","pycortex_outputs","dataset")
webviewer_dir = opj(base_dir,"pp_data",subject,"gauss","pycortex_outputs","webviewer","{subject}_{task}_{preproc}".format(subject = subject,
                                                                                                                          task = task,
                                                                                                                          preproc = preproc))

try:
    os.makedirs(flatmaps_dir)
    os.makedirs(dataset_dir)
    os.makedirs(webviewer_dir)
except:
    pass

# Load data
deriv_mat_file = "{deriv_dir}/{subject}_task-{task}_{preproc}_deriv.nii.gz".format(deriv_dir = deriv_dir,
                                                                                   subject = subject, 
                                                                                   task = task, 
                                                                                   preproc = preproc)

img_deriv_mat = nb.load(deriv_mat_file)
deriv_mat = img_deriv_mat.get_fdata()
    
# R-square
rsq_data = deriv_mat[...,rsq_idx]
alpha = rsq_data
param_rsq = {'data': rsq_data, 'cmap': cmap_uni, 'alpha': alpha, 'vmin': 0,'vmax': 1,'cbar': 'discrete',
             'description': 'pRF rsquare', 'curv_brightness': 1, 'curv_contrast': 0.1, 'add_roi': False}
maps_names.append('rsq')

# Polar angle
pol_comp_num = deriv_mat[...,polar_real_idx] + 1j * deriv_mat[...,polar_imag_idx]
polar_ang = np.angle(pol_comp_num)
ang_norm = (polar_ang + np.pi) / (np.pi * 2.0)
ang_norm = np.fmod(ang_norm + col_offset,1)

param_polar = { 'data': ang_norm, 'cmap': cmap_polar, 'alpha': alpha, 'vmin': 0, 'vmax': 1, 'cmap_steps': cmap_steps,
                'cbar': 'polar', 'col_offset': col_offset, 'description': 'pRF polar:{cmap_steps:3.0f} steps'.format(cmap_steps = cmap_steps), 
                'curv_brightness': 0.1, 'curv_contrast': 0.25, 'add_roi': save_svg}
exec('param_polar_{cmap_steps} = param_polar'.format(cmap_steps = int(cmap_steps)))
exec('maps_names.append("polar_{cmap_steps}")'.format(cmap_steps = int(cmap_steps)))

# Eccentricity
ecc_data = deriv_mat[...,ecc_idx]
param_ecc = {'data': ecc_data, 'cmap': cmap_ecc_size, 'alpha': alpha, 'vmin': 0, 'vmax': 15,'cbar': 'ecc', 
             'description': 'pRF eccentricity', 'curv_brightness': 1, 'curv_contrast': 0.1, 'add_roi': save_svg}
maps_names.append('ecc')
add_roi = True

# Size
size_data = deriv_mat[...,size_idx]
param_size = {'data': size_data, 'cmap': cmap_ecc_size, 'alpha': alpha, 'vmin': 0, 'vmax': 8, 'cbar': 'discrete', 
              'description': 'pRF size', 'curv_brightness': 1, 'curv_contrast': 0.1, 'add_roi': False}
maps_names.append('size')
add_roi = False

# Coverage
cov_data = deriv_mat[...,cov_idx]
param_cov = {'data': cov_data, 'cmap': cmap_uni, 'alpha': alpha,'vmin': 0, 'vmax': 1, 'cbar': 'discrete', 
             'description': 'pRF coverage', 'curv_brightness': 1, 'curv_contrast': 0.1, 'add_roi': False}
maps_names.append('cov')
add_roi = False

# Draw flatmaps
volumes = {}


for maps_name in maps_names:
    roi_name = '{maps_name}_{task}_{preproc}'.format(maps_name = maps_name, task = task, preproc = preproc)
    roi_param = {'subject': subject, 'xfmname': xfm_name, 'roi_name': roi_name}
    
    exec('param_{maps_name}.update(roi_param)'.format(maps_name = maps_name))
    exec('volume_{maps_name} = draw_cortex_vertex(**param_{maps_name})'.format(maps_name = maps_name))
    
    exec('plt.savefig(opj(flatmaps_dir, "{maps_name}_{task}_{preproc}.pdf"),facecolor = "w")'.format(maps_name = maps_name, task = task, preproc = preproc))
    plt.close()
    exec('vol_description = param_{maps_name}["description"]'.format(maps_name = maps_name))
    exec('volume = volume_{maps_name}'.format(maps_name = maps_name))
    volumes.update({vol_description:volume})
    
print('save pycortex dataset')
exec('dataset = cortex.Dataset(data = volumes)')
exec('dataset_file = opj(dataset_dir, "{task}_{preproc}.hdf")'.format(task = task, preproc = preproc))
    
    
try: os.remove(dataset_file)
except: pass
dataset.save(dataset_file)
print('save pycortex webviewer')
cortex.webgl.make_static(outpath = webviewer_dir, data = volumes)

# TC data
# -------
if plot_tc == 1:

    # load volume
    print('load: time course')
    tc_file = "{base_dir}/pp_data/{subject}/func/{subject}_task-{task}_{preproc}_avg.nii.gz".format(base_dir = base_dir, subject = subject, task = task, preproc = preproc)
    img_tc = nb.load(tc_file)
    tc = img_tc.get_fdata()

    # create directory
    webviewer_dir = "{base_dir}/pp_data/{subject}/gauss/pycortex_outputs/webviewer/{subject}_{task}_{preproc}_tc/".format(
                            base_dir = base_dir, subject = subject, task = task, preproc = preproc)

    try:
        os.makedirs(webviewer_dir)
    except:
        pass
    
    # create volume
    volume_tc = cortex.Volume(data = tc.transpose((3,2,1,0)),
                              subject = subject,
                              xfmname = xfm_name,
                              cmap = 'BuBkRd',
                              description = 'BOLD')

    # create dataset
    print('save pycortex dataset: time course')
    dataset_tc = cortex.Dataset(data = volume_tc)
    dataset_tc.save("{dataset_dir}_tc.hdf".format(dataset_dir = dataset_dir))

    # create webgl
    print('save pycortex webviewer: time course')
    cortex.webgl.make_static(outpath = webviewer_dir, data = volume_tc)