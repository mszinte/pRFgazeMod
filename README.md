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
* run fmriprpep with anat-only option on mesocentre using mri_analysis/preproc/fmriprep_sbatch.py<br/>
* make a "before_edit" video of the fmriprep/freesurfer segmentation using mri_analysis/preproc/freeview.py<br>
* manual edition of the pial surface using freeview launched with /preproc/pial_edits.py and following the rules of http://surfer.nmr.mgh.harvard.edu/fswiki/FsTutorial/PialEditsV6.0 <br/>
* re-run freesurfer to include the manual change of the pial surface using preproc/freesurfer_pial.py<br/>
* make a "after_edit" video of the fmriprep/freesurfer segmentation using mri_analysis/preproc/freeview.py<br>
* Cut brains with https://docs.google.com/document/d/1mbx3EzTEYr4MIROWbgyklW_a7F6B4NX23bvk7VM7zeY/edit<br/>
* Flatten hemispheres with preproc/flatten_sbatch.py<br/>
* Import in pycortex and save t1w/t2w maps as pycortex webviewer
* run pybest (modified to save niftis) to high pass filter and denoised the data with /preproc/pybest_sbatch.py
* Save time courses as pycortex webviewer