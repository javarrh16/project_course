echo ""
echo " BE_Pred_plus  is a reliable and fast predictor designed specifically to predict if the amino acids of transmembrane alpha proteins are either buried (B) or exposed (E) within the protein structure. This is the improved version of BE_Pred since it uses PSI-Blast and will therefore take a couple minutes longer.."
echo ""
echo "Designed by Javier Arroyo"
echo ""
echo ""
echo ""
echo "Please input directory path followed by the file name in fasta format for the analysis. It is very important that the name of the document is .fasta"
read -p "Fasta file: " fasta_file
directory= "$(dirname "$fasta_file")"
echo ""
echo ""
echo "Running PSI-BLAST on input sequence. This step can take a couple minutes..."
echo ""
export BLASTDB=/local_uniref/uniref/uniref90

#First we change directory to uniref90 and then from the folder with all the fasta_seqs we can do the loop for the psi-blast run:
echo "If you get a Warning in the next seconds, don't worry.. It happens sometimes!"
time psiblast -query $fasta_file -db uniref90.db -num_iterations 3 -evalue 0.001 -out $fasta_file.psiblast -out_ascii_pssm $fasta_file.pssm -num_threads 8

#Since it can take a long time, to know when the iterations are done we will echo:
echo ""
echo "PSI-BLAST run is complete!!"
echo ""
#here we change to the directory from wich the input file was inputed because the .pssm documents are going to be created in that directory
cd $directory
#by adding at the end $fasta_file we can use that variable later in BE_pred_plus.py with argv[].
python /home/u2208/project_course/projects/scripts/BE_pred_plus.py $fasta_file
																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																							
