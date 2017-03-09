import math
import numpy as np
from sklearn import preprocessing 
from sklearn.preprocessing import OneHotEncoder
enc = preprocessing.OneHotEncoder()

f = open ('/home/u2208/project_course/projects/datasets/buried_exposed_alpha.3line.txt', 'r')

list_all = list()
#remove line breaks
for line in f:
	newline = line.replace('\n', '')
	list_all.append(newline)

#list_title = [] We commented this list out since we never used it.
list_seq = []
list_stru = []
word_list = []
mfeature_list = []
cword_list = []
sepn_list = []


#define window size
windows = int(input('Input window size as an odd integer number: '))

#create 3 different list separating titles, sequences and structures. In the process we have added 'X' to the begining and end of the sequences (depending on the windowsize) so we can predict the structure features for the first and last characters of the sequence as well.
for i in range (0, len(list_all), 3):
	#list_title.append(list_all[i])
	list_seq.append((math.floor(windows/2))*'X'+list_all[i+1]+(math.floor(windows/2))*'X')
	list_stru.append((math.floor(windows/2))*'X'+list_all[i+2]+(math.floor(windows/2))*'X')

#makes a list of every sequence so that each element is one aa
for seq in list_seq:
	aa_list = list(seq)
#takes the window size number of aa to form words for each sequence list 
	for aa in range(0, len(aa_list)-(windows-1)):
		word_list.append(aa_list[aa:aa+windows])

#We have created mfeature list containing only the middle feature of the structure words depending on the window size.  
for structure in list_stru:
	feat_list = list (structure)
	for feature in range (int(windows/2), len(feat_list)-math.floor(windows/2)):
		mfeature_list.append(feat_list[feature])

#translate amino acids into numerical code
from aa_dictionary import aa_dict
for a in range (0, len(word_list)):
	for b in range(0, windows):
		for key in aa_dict:
			if key == word_list[a][b]:	
				word_list[a][b] = aa_dict[key]

#translate structure features into numerical code and in the last step also change them into integers
from structure_dict import structure_dict
for feature in range(0, len(mfeature_list)):
    for key in structure_dict:
        if key == mfeature_list [feature]:
            mfeature_list[feature] = int(structure_dict[key])

#We have joined the individual codes for every amino acid in to a codeword and saved in cword_list.
cword = str()
for word in word_list:
    for aa in range(0, len(word)):
        cword = cword + str(word[aa])
    cword_list.append(cword) 
    cword = str()

#We have taken our list of translated and 'put together' words and we have splitted them in to the single elements (that are still a string)
for word in cword_list:
	position_list = list(word)	
	sepn_list.append(position_list)

#We have converted the single elements from each word and converted them into integers.
for a in range(0, len(sepn_list)):
	for b in range (0, (windows*20)):
		sepn_list[a][b]=int(sepn_list[a][b])

#transforming list sepn_list into an array
#sepn_list_array = enc.fit_transform(sepn_list).toarray()

#save the lists as a document (needed to be string for that); before using the lists reconvert into integers 
#print (sepn_list)
a = str()
with open('/home/u2208/project_course/projects/output/sepn_list%d.txt' %windows, 'w+') as sepn_list_doc:
	for i in sepn_list:
		for j in range (0, len(i)):
			a = a + str(i[j])
		sepn_list_doc.write(a + '\n')
		a = str()
with open('/home/u2208/project_course/projects/output/mfeature_list%d.txt' %windows, 'w+') as mfl:
	for i in mfeature_list:
		mfl.write(str(i)+'\n')




#WAYS TO IMPROVE SCRIPT:
#-remove aa_list and do the same operations with seq_list instead -> removes some loops
#-To optimize it is good if we can have as many processes in every step as possible to reduce time and storing space



