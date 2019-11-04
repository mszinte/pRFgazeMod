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
2. run mriqc on mesocentre using mri_analysis/pre_fit/mriqc_srun.py or mriqc_sbatch<br/>
2. run fmriprep on mesocenter using mri_analysis/pre_fit/fmriprep_sbatch - use first anat-only option<br/>
