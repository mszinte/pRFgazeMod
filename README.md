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
0. convert data to nifti using /mri_analysis/pre_fit/bids/convert2niigz.py<br/>
1. make bids format using /mri_analysis/pre_fit/bids/bids_format_sub-001.py to bids_format_sub-008.py<br/>
2. run mriqc on mesocentre using mri_analysis/pre_fit/mriqc_sbatch.py<br/>
3. run fmriprep on mesocenter using mri_analysis/pre_fit/fmriprep_sbatch.py - use first anat-only option<br/>
4. make sagital png and video of segmentation before edit using /pre_fit/freeview.py<br/>
5. run freesurfer-dev version to use t2w image for the pial surface using pre_fit/freesurfer_dev.py<br/>
6. make sagital png and video of segmentation after freesurfer-dev using /pre_fit/freeview.py<br/>