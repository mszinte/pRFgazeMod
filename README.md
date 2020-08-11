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
0. convert data to nifti using /mri_analysis/pre_fit/bids/convert2niigz.py<br/>
1. make bids format using /mri_analysis/pre_fit/bids/bids_format_sub-001.py to bids_format_sub-008.py<br/>
2. run mriqc on mesocentre using mri_analysis/pre_fit/mriqc_sbatch.py<br/>
3. run fmriprep on mesocenter using mri_analysis/pre_fit/fmriprep_sbatch.py - use first anat-only option<br/>
4. make sagital png and video of segmentation before edit using /pre_fit/freeview.py<br/>
5. run freesurfer-dev version to use t2w image for the pial surface using pre_fit/freesurfer_dev.py<br/>
6. make sagital png and video of segmentation after freesurfer-dev using /pre_fit/freeview.py<br/>
7. manual edition of the pial surface for occipital lobe edges using freeview launched with /pre_fit/pial_edit.py and following the rules of http://surfer.nmr.mgh.harvard.edu/fswiki/FsTutorial/PialEditsV6.0 <br/>
8. re-run pial edition using freesurfer-dev version with pre_fit/freesurfer_dev.sh<br/>
9. make sagital png and video of segmentation after manual edit using /pre_fit/freeview.py<br/>
10. run fmriprep with correct anatomical segmentation<br/>
11. run pybest (modified to save niftis) to high pass filter and denoised the data with /pre_fit/pybest_sbatch.py<br/>
12. change to percent signal and averaged runs with pre_fit/pp_fit.py<br/>
