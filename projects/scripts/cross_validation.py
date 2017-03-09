import numpy as np
from sklearn.svm import LinearSVC
from sklearn import svm
from sklearn.model_selection import cross_val_score
from Bio import pairwise2
import math

#In this step we are loading the data from the saved files with the words and structures and converting them to lists.
sepn = list(open('/home/u2208/project_course/projects/output/sepn_list19.txt', 'r'))
mfeature_list = list(open('/home/u2208/project_course/projects/output/mfeature_list19.txt', 'r'))

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
for i in range (0, len(mfeature_list)):
	mfeature_list[i] = mfeature_list[i].strip('\n')
	mfeature_list[i] = int(mfeature_list[i])

#Before doing the cross validation I am going to perform a homology check for my sequences since I have very few (56) so I can make sure that none of my sets during cv are biased.
#csepn_list= sepn_list.copy()
#alignments = pairwise2.align.localxx(sepn_list, csepn_list)

#This step performs the crossvalidation for the word,feature lists. With kernel you change the kernel type and cv shows how many sets are created for the cross validation.
clf = svm.LinearSVC(C=1)
clf.fit(sepn_list, mfeature_list)
scores = cross_val_score(clf, sepn_list, mfeature_list, cv=10)
#print(scores)
print('The mean score after cross-validation is: ', sum(scores)/10)

#####################################################################################################
#This step is done to safe the model so it doesn't have to be trained every time we want to predict something
from sklearn.externals import joblib
joblib.dump(clf, '')

#To call back the model (and give it the name again of clf) we use the following:
clf = joblib.load('')

######################################################################################################
#To predict an example of sequences first convert the document with the list to be predicted into list
predicted_list = []
xxsepn = list(open('/home/u2208/project_course/projects/output/xxsepn_list19.txt', 'r'))
for line in xxsepn:
	newline = line.strip('\n')
	a = list(newline)
	for b in range (0, len(a)):
		a[b] = int(a[b])
		
	predicted_list.append(a)
	a = list()

#creates a list the prediction
pred_val = clf.predict(predicted_list)
#print(pred_val)

#saves the prediction in predmfeature... document
with open('/home/u2208/project_course/projects/output/predmfeature_list.txt', 'w+') as mfl:
	for i in pred_val:
		mfl.write(str(i)+'\n')


#WAYS TO OPTIMIZE THE PREDICTION:
#- kernel function (linear)
#- number of cv sets (10 is slightly better than 5 but it takes considerably longer)
#- wordsize (19)
#- different encodings for amino acids grouping them according to their feature
