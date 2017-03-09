import math
import numpy as np
from sklearn import preprocessing 
from datetime import datetime
from sklearn.svm import LinearSVC
from sklearn import svm


start = datetime.now()

f = open ('/home/u2208/project_course/projects/datasets/1examplepssm.txt', 'r')

list_all = list()
#remove line breaks
for line in f:
	newline = line.replace('\n', '')
	list_all.append(newline)

list_title = []
list_seq = []
list_stru = []
word_list = []
mfeature_list = []
cword_list = []
sepn_list = []


#define window size
windows = int(input('Input window size as an odd integer number: '))

#create 3 different list separating titles, sequences and structures
print('create 3 different list separating titles, sequences and structures')
for i in range (0, len(list_all), 3):
	list_title.append(list_all[i])
	list_seq.append(list_all[i+1])
	list_stru.append(list_all[i+2])
list_all = list()


################################################################################################################
# Import and parse PSSM

pssm_list = []
#for title in list_title:
f = list(open("/home/u2208/project_course/projects/output/psiblast_output/'>d1b8dk_.a.1.1.3'.fasta.pssm", 'r'))

for i in range(4,220):
	pssm_list.append(f[i][92:(len(f[i])-11)])

pssm_freq_list = []
for position in pssm_list:
	newposition = position.split()
	for element in range (0, len(newposition)):
		newposition[element] = int(newposition[element])/100
	pssm_freq_list.append(newposition)
	


############################################################################################


#takes the window size number of aa to form words for each sequence list
print('takes the window size number of aa to form words for each sequence list')

for aa in range(0, len(pssm_freq_list)-(windows-1)):
	word_list.append(pssm_freq_list[aa:aa+windows])
sumaalist=[]
word_listflat=[]
for word in word_list:
	sumaalist=list()
	for aa in word:
		sumaalist = sumaalist+aa 
	word_listflat.append(sumaalist)
print(word_listflat)


#We have created mfeature list containing only the middle feature of the structure words depending on the window size.  
print('We have created mfeature list containing only the middle feature of the structure words depending on the window size')
for structure in list_stru:
	feat_list = list (structure)
	for feature in range (int(windows/2), len(feat_list)-math.floor(windows/2)):
		mfeature_list.append([feat_list[feature]])		
#print (mfeature_list)


#translate structure features into numerical code and in the last step also change them into integers
print('translate structure features into numerical code and in the last step also change them into integers')
from structure_dict import structure_dict
for feature in range(0, len(mfeature_list)):
    for key in structure_dict:
        if key == mfeature_list [feature][0]:
            mfeature_list[feature][0] = int(structure_dict[key])
#print(mfeature_list)
print(len(mfeature_list))
print(len(word_listflat))
sys.exit()
clf = svm.LinearSVC(C=1).fit(word_listflat, mfeature_list)
score = clf.score(word_listflat, mfeature_list)
print(score)
sys.exit()
# #We have joined the individual codes for every amino acid in to a codeword and saved in cword_list.
# print('We have joined the individual codes for every amino acid in to a codeword and saved in cword_list.')
# cword = str()
# for word in word_list:
    # for aa in range(0, len(word)):
        # cword = cword + str(word[aa])
    # cword_list.append(cword) 
    # cword = str()

# #We have taken our list of translated and 'put together' words and we have splitted them in to the single elements (that are still a string)
# print('We have taken our list of translated and put together words and we have splitted them in to the single elements (that are still a string)')
# for word in cword_list:
	# position_list = list(word)	
	# sepn_list.append(position_list)

#We have converted the single elements from each word and converted them into integers.
# for a in range(0, len(sepn_list)):
	# for b in range (0, (windows*20)):
		# sepn_list[a][b]=int(sepn_list[a][b])

		

#save the lists as a document (needed to be string for that); before using the lists reconvert into integers 
print('save the lists as a document (needed to be string for that); before using the lists reconvert into integers ')
a = str()
with open('C:\\Users\\Leonie\\OneDrive\\Master Life Science\\python\\project\\output\\sepn_list%d.txt' %windows, 'w+') as sepn_list_doc:
	for i in sepn_list:
		for j in range (0, len(i)):
			a = a + str(i[j])
		sepn_list_doc.write(a + '\n')
		a = str()
with open('C:\\Users\\Leonie\\OneDrive\\Master Life Science\\python\\project\\output\\mfeature_list%d.txt' %windows, 'w+') as mfl:
	for i in mfeature_list:
		mfl.write(str(i)+'\n')
print('finished')
print(datetime.now() - start)

#WAYS TO IMPROVE SCRIPT:
#-remove aa_list and do the same operations with seq_list instead -> removes some loops
#-To optimize it is good if we can have as many processes in every step as possible to reduce time and storing space

