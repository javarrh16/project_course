
f = open ('buried_exposed_alpha.3line.txt', 'r')

list_all = list()
#remove line breaks
for line in f:
	newline = line.replace('\n', '')
	list_all.append(newline)

list_title = []
list_seq = []
list_stru = []
word_list = []
wordst_list = []

#create 3 different list separating titles, sequences and structures
for i in range (0, len(list_all), 3):
	list_title.append(list_all[i])
	list_seq.append(list_all[i+1])
	list_stru.append(list_all[i+2])
	
#join 3 lists to another list [[title1, seq1, structure1],[..]]
zipped = zip(list_title, list_seq, list_stru)
joined_list = list(zipped)

#define window size
windows = 3

#makes a list of every sequence so that each element is one aa
for seq in list_seq:
	aa_list = list(seq)
#takes the window size number of aa to form words for each sequence list 
	for aa in range(0, len(aa_list)-(windows-1)):
		word_list.append(aa_list[aa:aa+windows])
a = set ()	
#create the structure words based on windowsize
#We changed the last lines from our original script so we could make a set and check exactly what structural features we had in order to be able to create a diccionary in the next steps
for structure in list_stru:
	feat_list = list (structure)
	for feature in range (0, len(feat_list)-(windows-1)):
		wordst_list.append(feat_list[feature:feature+windows])
		a.update(str(feat_list[feature:feature+windows]))
print(a)
