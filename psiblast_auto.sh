
database_file=/home/sarah/Desktop/prot.proj.scilifecomp/BLAST_proj/uniref90.fasta     
input_dir=/home/sarah/Desktop/prot.proj.scilifecomp/prot.proj/FASTA_files          
output_dir=/home/sarah/Desktop/prot.proj.scilifecomp/prot.proj/outputs_BLAST

#use .blastpgp or .psi? <-- blastpgp

for i in $input_dir/*.fasta ; do
base=`basename $i .fasta`
if [ ! -f $output_dir/$base.psi ] ; then      #making sure files don't already exist in directory, in case computer restarts or something you won't have to start over
	blastpgp -i $i -j 3 -d $database_file -i $i -o $output_dir/$base.blastpgp -Q $output_dir/$base.psi
fi
done
echo "All done!!!!" #echo when everything's finished. Took about 5 days for all files