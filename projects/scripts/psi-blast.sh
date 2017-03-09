#The aim of this bash is to run a psi-blast search with buried_exposed_alpha.3line.txt. For this, the document had to be transformed in previous steps into multiple fasta files.
#To run it i have to write in the terminal: export BLASTDB=/scratch/blastdb (so i have to check that the terminal is on scratch)

#First we change directory to uniref90 and then from the folder with all the fasta_seqs we can do the loop for the psi-blast run:

for seq in ~/project_course/projects/datasets/fasta_seqs/*.fasta ; do

#This step is the actual psiblast run creating the pssm. In this step i have included a "safety measure" to check if the files have been created already in the output directory in case that the computer shuts down or something happens (so they dont have to be created twice)
if [ ! -f $output_directory/$base.psi ]; then
	echo "Running psiblast on $seq at $(date)..."
	time psiblast -query $seq -db uniref90.db -num_iterations 3 -evalue 0.001 -out $seq.psiblast -out_ascii_pssm $seq.pssm -num_threads 8
	echo "Finished running psiblast on $seq at $(date)."
fi
done

#Since it can take a long time, to know when the iterations are done we will echo:
echo 'PSI-BLAST run is complete'

#All the files have been created in the folder datasets so with the following steps I move them to output/psiblast_output
cd ~/project_course/projects/datasets/fasta_seqs/
mv *.psiblast ../../output/psiblast_output
mv *.pssm ../../output/psiblast_output																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																								
