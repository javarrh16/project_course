import os
import sys
import math
import numpy as np
from sklearn import preprocessing
from sklearn.externals import joblib


fasta_file = sys.argv[1]
input_seq = open(fasta_file, 'r')

#remove line breaks
list_all = list()
for line in input_seq:
	newline = line.replace('\n', '')
	list_all.append(newline)


#define window size. It is commented out since we make a loop later to test different window sizes.
windows = int(7)


list_title = []
list_seq = []
list_seq_normal = []
word_list = []
mfeature_list = []
ordered_stru= []
word_listflat=[]

#create 3 different list separating titles, sequences and structures
for i in range (0, len(list_all), 2):
    list_title.append(list_all[i])
    list_seq.append((math.floor(windows/2))*'X'+list_all[i+1]+(math.floor(windows/2))*'X')
    list_seq_normal.append(list_all[i+1])

#calls PSSMs by title only if they exist in directory
for title in list_title:
    #title = title.strip('>')
    #newtitle = '%s.fasta.pssm' %title
	
    if os.path.isfile("%s.pssm" %fasta_file):		
        #print("Running: '%s'.fasta.pssm" %title)		
        f= list(open("%s.pssm" %fasta_file, 'r'))
        pssm_list = []
        word_list = []

        #takes the desired positions from the PSSM and puts them into a list
        for i in range(3,(len(f)-6)):
            if i == 3:
                pssm_list.extend((math.floor(windows/2))*[list(np.zeros(20))])
            elements= f[i].split()
            pssm_list.append(list(elements[22:-2]))
            if i == (len(f)-7):		
                pssm_list.extend((math.floor(windows/2))*[list(np.zeros(20))])
		
        #splits the lines of the PSSM in single numbers and normalizes them 
        for position in pssm_list:
            for element in range (0, len(position)):
                position[element] = int(position[element])/100
            #pssm_freq_list.append(position)
    
        #takes the window size number of aa to form words for each sequence
        for aa in range(0, len(pssm_list)-(windows-1)):
            word_list.append(pssm_list[aa:aa+windows])
    
        for word in word_list:
            sumaalist=list()
            for aa in word:
                sumaalist = sumaalist+aa 
            word_listflat.append(sumaalist) #word_listflat will contain all numbers of all called PSSMs, sequences cannot be separated anymore, only words are joined in sublists 			


#To call back the model (and give it the name again of clf) we use the following:
print()
print('Importing model for prediction...')
clf = joblib.load('/home/u2208/project_course/projects/scripts/modelpssm_ran_7_1000') #Final optimized model!

#creates a list the prediction
pred_val = clf.predict(word_listflat)

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












