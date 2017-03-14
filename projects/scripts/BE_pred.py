import math
import numpy as np
from sklearn import preprocessing
from sklearn.externals import joblib


print(' BE_Pred  is a reliable and fast predictor designed specifically to predict if the amino acids of transmembrane alpha proteins are either buried (B) or exposed (E) within the protein structure.')
print()
print('Designed by Javier Arroyo')
print()
print()

input_seq = input('For sequence prediction, please input directory path followed by the file name in fasta format: \n')

input_seq = open(input_seq, 'r')

list_all = list()
#remove line breaks
for line in input_seq:
	newline = line.replace('\n', '')
	list_all.append(newline)

#list_title = [] We commented this list out since we never used it.
list_seq = []
list_title = []
word_list = []
mfeature_list = []
cword_list = []
sepn_list = []
list_length = []
list_seq_normal = []

#define window size
#windows = int(input('Input window size as an odd integer number: '))
windows = int(15)

#create 3 different list separating titles, sequences and structures. In the process we have added 'X' to the begining and end of the sequences (depending on the windowsize) so we can predict the structure features for the first and last characters of the sequence as well.
for i in range (0, len(list_all), 2):
    list_title.append(list_all[i])
    list_length.append(len(list_all[i+1]))
    list_seq.append((math.floor(windows/2))*'X'+list_all[i+1]+(math.floor(windows/2))*'X')
    list_seq_normal.append(list_all[i+1])

#makes a list of every sequence so that each element is one aa
for seq in list_seq:
	aa_list = list(seq)
#takes the window size number of aa to form words for each sequence list 
	for aa in range(0, len(aa_list)-(windows-1)):
		word_list.append(aa_list[aa:aa+windows])

#translate amino acids into numerical code
from aa_dictionary import aa_dict
for a in range (0, len(word_list)):
	for b in range(0, windows):
		for key in aa_dict:
			if key == word_list[a][b]:	
				word_list[a][b] = aa_dict[key]

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


#To call back the model (and give it the name again of clf) we use the following:
print()
print('Importing model for prediction...')
clf = joblib.load('model_15_1.04')

#creates a list the prediction
pred_val = clf.predict(sepn_list)

#translate values (0,1) back in to B, E.
pred_stru_dict = {0:'B', 1:'E'}
pred_val_stru = []
for number in pred_val:
    number = pred_stru_dict[number]
    pred_val_stru.append(number)
final_stru =''.join(pred_val_stru)

print()
print('The predicted structure for this protein is as follows:')
print()
final_seq = []
final_seq = ''.join(list_seq_normal)
print(final_seq)
print(final_stru)
print()

out_file_name = input('Please name and give a format to your output file for the prediction: \n')
with open('%s' %out_file_name, 'a') as document:
    for i in list_title:
        document.write(str(i)+'\n')	
    document.write(str(final_seq)+'\n')
    document.write(str(final_stru)+'\n')

print("Your prediction has been succesfully completed and saved into", out_file_name)












