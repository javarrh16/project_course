import time
import math
import sys
import numpy as np
from sklearn import svm
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
#from Bio import pairwise2
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import matthews_corrcoef
#from sklearn.model_selection import train_test_split
#from sklearn.model_selection import GridSearchCV
from sklearn.externals import joblib


#In this step we are loading the data from the saved files with the words, structures and length of the sequences and converting them to lists.
sepn = list(open('/home/u2208/project_course/projects/output/sepn_list15.txt', 'r'))
#mfeature_list = list(open('/home/u2208/project_course/projects/output/mfeature_list15.txt', 'r'))
list_length = list(open('/home/u2208/project_course/projects/output/list_length.txt', 'r'))

#Here we convert the word list into integers again since it comes from a file in a string form.
sepn_list = []
for line in sepn:
	newline = line.strip('\n')
	a = list(newline)
	for b in range (0, len(a)):
		a[b] = int(a[b])
		
	sepn_list.append(a)
	a = list()

#Here we convert the feature list into integers cause it comes from a file as well as a string.
#for i in range (0, len(mfeature_list)):
#	mfeature_list[i] = mfeature_list[i].strip('\n')
#	mfeature_list[i] = int(mfeature_list[i])

#Here we convert the seq length list into integers cause it comes from a file as well as a string.
for i in range (0, len(list_length)):
	list_length[i] = list_length[i].strip('\n')
	list_length[i] = int(list_length[i])

#Here we convert the list of the protein lengths in an additive form so each number represents the sum of all the previous ones. This is needed so in the cross validation we can separate the words depending on what sequence they come from, so we dont train and test with words from the same protein.
list_lengthf= [0]
for i in range(0,len(list_length)):
    list_lengthf.append(list_length[i] + sum(list_length[0:i]))


#Before doing the cross validation I am going to perform a homology check for my sequences since I have very few (56) so I can make sure that none of my sets during cv are biased.
#csepn_list= sepn_list.copy()
#alignments = pairwise2.align.localxx(sepn_list, csepn_list)

#sys.exit()
#In this step i have made a loop so I can manually do a leave one out. In each loop one sequence is taken out for testing and the rest is used for training. To be able to do this I had to use the list lengthf wich has the lengths of all proteins (which is the same as the word nr) so i could take all the words from the same sequence out of the training set when that sequence is used as the test set. I am evaluating the svm with the mean values of the precision, recall, fscore, support and matthews correlation coefficient.
#precision = 0
#recall = 0
#fscore = 0
#support = 0
#counter= 0
#complete_mcc = 0

#clf = svm.LinearSVC(C=1.04)
#print("Machine learning with leave one out in process...")
#print()
#for i in range(1, len(list_lengthf)):
#	start = time.time()
#	X_test = sepn_list[list_lengthf[i-1]:list_lengthf[i]]
#	Y_test = mfeature_list[list_lengthf[i-1]:list_lengthf[i]]
#	X_train = sepn_list[0:list_lengthf[i-1]]+sepn_list[list_lengthf[i]:len(list_lengthf)]
#	Y_train = mfeature_list[0:list_lengthf[i-1]]+mfeature_list[list_lengthf[i]:len(list_lengthf)]
#	clf.fit(X_train, Y_train)
#	Y_pred = clf.predict(X_test)    
#	p, r, f, s = precision_recall_fscore_support(Y_test, Y_pred)
#	precision = precision + p
#	recall = recall + r
#	fscore = fscore + f
#	support = support + s
#	end = time.time()
#	counter = counter + 1
#	mcc = matthews_corrcoef(Y_test, Y_pred)
#	complete_mcc = complete_mcc + mcc
#print('Summarized results:')
#print()
#print(counter)
#print('The mean precision with the model is: ', precision/56)
#print('The mean recall with the model is: ', recall/56)
#print('The mean fscore with the model is: ', fscore/56)
#print('The mean support with the model is: ', support/56)
#print('The Matthews correlation coefficient is; ', complete_mcc/56)

#This step is done to safe the model so it doesn't have to be trained every time we want to predict something

#joblib.dump(clf, 'model_15_1.04')
#sys.exit()
#To call back the model (and give it the name again of clf) we use the following:
clf = joblib.load('model_15_1.04')

######################################################################################################

#X_train, X_test, Y_train, Y_test = train_test_split(sepn_list, mfeature_list, test_size=0.5)
#parameters = [{'C': [0.5, 1, 1.04, 2, 5, 10]}]
#clf = GridSearchCV(LinearSVC(C=1), parameters)
#clf.fit(X_train, Y_train)
#print('Best parameters set found on development set: ')
#print()
#print(clf.best_estimator_)
#Y_true, predicted_f = Y_test, clf.predict(X_test)
#mcc = matthews_corrcoef(Y_true, predicted_f)
#print('The matthews correlation coefficient is: ', mcc)



#creates a list the prediction
pred_val = clf.predict(sepn_list)
#print(pred_val)

#translate values (0,1) back in to B, E.
final_stru = []
pred_stru_dict = {0:'B', 1:'E'}
pred_val_stru = []
for number in pred_val:
    number = pred_stru_dict[number]
    pred_val_stru.append(number)
final_stru =''.join(pred_val_stru)

#saves the prediction in predmfeature... document
with open('/home/u2208/project_course/projects/output/predicted_seqs.txt', 'w+') as mfl:
    for i in final_stru:
        mfl.write(str(i)+'\n')








