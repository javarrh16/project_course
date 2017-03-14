#The aim of this file is to transform the document buried_exposed_alpha.3line.txt in fasta format. For this we have to take the title and sequence information but not the feature info.
f = open ('/home/u2208/project_course/projects/input/50_prot_stru', 'r')
list_all = list()

#remove line breaks
for line in f:
    newline = line.replace('\n', '')
    list_all.append(newline)

#rewrites each protein of the list a single fasta file (only title(i) and seq info(i+1)). To write different fasta files each with only one title and seq I only have to change 'a' per 'w+' when opening the document.
for i in range(0, len(list_all), 3):
    a = list_all[i]
    with open('/home/u2208/project_course/projects/input/fasta_50_prot/%r.fasta' %a, 'w+') as fasta:
        fasta.write(list_all[i]+'\n' + list_all[i+1]+'\n')
print('Transformation in fasta format completed. Document safed in input/fasta_50_prot')
