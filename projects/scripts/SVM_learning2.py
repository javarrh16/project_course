import numpy as np
from sklearn.svm import SVC
from sklearn import svm
from sklearn import preprocessing 
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import OneHotEncoder
enc = preprocessing.OneHotEncoder()

#In this step we are loading the data from the saved files with the words and structures and converting them to lists.
sepn = list(open('/home/u2208/project_course/projects/output/sepn_list7.txt', 'r'))
sepn_list = []
for line in sepn:
	newline = line.strip('\n')
	a = list(newline)
	for b in range (0, len(a)):
		a[b] = int(a[b])
		
	sepn_list.append(a)
	a = list()


#In this step we convert the word list into an array
sepn_list_array = enc.fit_transform(sepn_list).toarray()


##Here we convert the feature list into integers cause it comes from a file as well as a string.
mfeature_list = list(open('/home/u2208/project_course/projects/output/mfeature_list7.txt', 'r'))

for i in range (0, len(mfeature_list)):
	mfeature_list[i] = mfeature_list[i].strip('\n')
	mfeature_list[i] = int(mfeature_list[i])


#In this step the machine learning is performed and the score is printed as the output
lin_clf = svm.LinearSVC()
Lin1= (lin_clf.fit(sepn_list, mfeature_list))
print(lin_clf.score(sepn_list, mfeature_list))
