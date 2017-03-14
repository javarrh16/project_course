READ ME!
This directory 'project_course' contains scripts for the prediction of the features of an amino acid sequence. Specifically to predict if the amino acids of a certain inputed sequence are buried or exposed within the protein structure.


Instructions for the proper use of my directories:



The first thing to take into account when working with my scripts is that all paths in all scripts work, but since some of the scripts are interconected, in case of downloading one document, please check that the paths still work. It is much easier to download my whole directory 'project_course', which will ensure no problems occuring during the running of the scripts.



For this project I have created TWO PREDICTORS that succesfully predict if the amino acids of a certain inputed sequence are buried or exposed.

--The first predictor: BE_pred can be run as "python /project_course/projects/scripts/BE_pred.py". BE_pred is a very fast predictor, however the accuracy was slightly compromised since no PSI-Blast is run for the sequence analysis.

--The second predictor: BE_pred_plus can be run as "bash /project_course/projects/scripts/BE_pred_plus.sh". BE_pred_plus uses a PSI-Blast analysis for a more accurate prediction of the buried/exposed state. This, makes the program take a bit more time to run but the prediction is much more accurate! It is reccommended to use BE_pred_plus.



Both of this predictors have been designed for a theoretical INPUT FILE WITH ONLY ONE SEQUENCE IN FASTA FORMAT, since this was the aim of this project. However, other scripts can be used one after another (and not automatically) to be able to predict a fasta file with multiple sequences.

Instructions for this additional procedure:
-The scripts can be found in /project_course/projects/scripts
-First run sequence converter.py to convert the sequences to predict in to a svm valid format
-Then run cross_validation.py to predict with a manual leave one out cross validation and svm. In this step the prediction will be done and saved as /project_course/projects/output/predicted_seqs. The predicted sequences will be saved one line at a time. If there is only one sequence to be predicted the output file will have one prediction (for one aa) per line.
-If you want to run a PSI-Blast analysis on your sequences then run /project_course/projects/scripts/psi-blast.sh (as bash)
-If you want to use the PSI-Blast info stead of using cross_validation.py use PSSM_converter.py with a couple modifications from BE_pred_plus for the final printing.

The best option to use is however BE_pred_plus!!!. It would be easy to modify this document slightly so it can be used for multiple sequences as well. This extra task hasnt been done yet due to time difficulties.
