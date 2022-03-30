## pRFgazeMod

By :      Martin SZINTE<br/>
Projet :  pRFseqTest<br/>
With :    Ines Verissimo & Tomas KNAPEN<br/>
Version:  4.0<br/>

## Version description

Experiment in which we first used a full screen 4 direction (left/right/up/down)
bar pass stimuli in a attetion to fixation or attention to the bar experiment.
Next, we use the same task but this time using a bar pass restricted to an aperture and 
displayed at 3 different position surrounding the fixation target put at the screen center 
or displaced to the left or to the right.

## MRI analysis

# pre-processing
* convert data in bids, see pre_fit/bids/bids_format_sub-00X.py
* run fmriprpep with anat-only option on mesocentre using mri_analysis/pre_fit/fmriprep_sbatch.py<br/>
* make a "before_edit" video of the fmriprep/freesurfer segmentation using mri_analysis/pre_fit/freeview.py<br>
* manual edition of the pial surface using freeview launched with /pre_fit/pial_edits.py and following the rules of http://surfer.nmr.mgh.harvard.edu/fswiki/FsTutorial/PialEditsV6.0 <br/>
* re-run freesurfer to include the manual change of the pial surface using pre_fit/freesurfer_pial.py<br/>
* make a "after_edit" video of the fmriprep/freesurfer segmentation using mri_analysis/pre_fit/freeview.py<br>
* Cut brains with https://docs.google.com/document/d/1mbx3EzTEYr4MIROWbgyklW_a7F6B4NX23bvk7VM7zeY/edit, see cortex_cuts.sh<br/>
* Flatten hemispheres with pre_fit/flatten_sbatch.py<br/>
* run fmriprpep for functionnal runs on mesocentre using mri_analysis/pre_fit/fmriprep_sbatch.py<br/>
* run pybest (modified to save niftis) to z-scores, high pass filter and denoise the data using /pre_fit/pybest_sbatch.py
* arrange data in pp_data folder, and average runs using pre_fit/pre_fit_end.py
* Import in pycortex surfaces and flatmaps using pre_fit/pycortex_import.py
* [optional] Save time courses as pycortex webviewer using pre_fit/save_tc.py

# initial post-processing
* launch pRF fit of GazeCenterFS [fmriprep_dct + fmriprep_dct_pca] averaged runs using fit/submit_fit_jobs.py
* combine fit files of GazeCenterFS [fmriprep_dct + fmriprep_dct_pca] and compute pRF derivatives using pos_fit/post_fit.py
* plot pycortex flatmaps of GazeCenterFS [fmriprep_dct + fmriprep_dct_pca] and save webgls using LOCALLY post_fit/pycortex_maps.py
* draw ROIS using inkscape (V1/V2/V3/V3AB/LO/VO/hMT+/iIPS/sIPS/mPCS/sPCS/iPCS)
* create ROIs masks and H5 files per ROIS of GazeCenterFS [fmriprep_dct + fmriprep_dct_pca] using post_fit/roi_to_hdf5.py
* plot pRF metrics per ROIS of GazeCenterFS [fmriprep_dct + fmriprep_dct_pca] using post_fit/roi_plots.py
* save pandas dataframes using post_fit/roi_to_pandas.py

#  app processing see app/pRFgazeMod
* plot prf summary graphs and put dashboard on [heroku](https://prfgazemod.herokuapp.com/apps/prf_app)

# to do
* run full screen task fit
* create batch code for h5 and roi codes
* do change to fit only the x value and import the y value