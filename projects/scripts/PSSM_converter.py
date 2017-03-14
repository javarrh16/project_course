import os
import sys
import time
import math
import numpy as np
from datetime import datetime
from sklearn.svm import LinearSVC
from sklearn import svm
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.metrics import matthews_corrcoef
from sklearn.model_selection import GridSearchCV
from sklearn.externals import joblib
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import matthews_corrcoef
from sklearn.ensemble import RandomForestClassifier


start = datetime.now()

f = open ('/home/u2208/project_course/projects/datasets/buried_exposed_alpha.3line.txt', 'r')

list_all = list()
cword_list = []
sepn_list = []
list_all = list()

#remove line breaks
for line in f:
	newline = line.replace('\n', '')
	list_all.append(newline)


#define window size. It is commented out since we make a loop later to test different window sizes.
#windows = int(input('Input window size as an odd integer number: '))

# Import and parse PSSM
print(datetime.now() - start)

#here I am creating a loop to test the different windows
for all_windows in range(5,13,2):
    windows = all_windows
    print('The window size for this seq is: ', windows)
    list_title = []
    list_stru = []
    word_list = []
    mfeature_list = []
    ordered_stru= []
    word_listflat=[]

    #create 3 different list separating titles, sequences and structures
    for i in range (0, len(list_all), 3):
    	list_title.append(list_all[i])
    	list_stru.append((math.floor(windows/2))*'X'+list_all[i+2]+(math.floor(windows/2))*'X')


    #calls PSSMs by title only if they exist in directory
    for title in list_title:
    	#title = title.strip('>')
    	#newtitle = '%s.fasta.pssm' %title
	
        if os.path.isfile("/home/u2208/project_course/projects/output/psiblast_output/'%s'.fasta.pssm" %title):		
            #print("Running: '%s'.fasta.pssm" %title)		
            f= list(open("/home/u2208/project_course/projects/output/psiblast_output/'%s'.fasta.pssm" %title, 'r'))
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
    		
    		#we determine the index of the title and extract the corresponding structure-seq by using the same index. The structure-seq is saved in a new list
            index = list_title.index(title) #Leo use newtitle!!
            ordered_stru.append(list_stru[index])

    #creates mfeature list containing only the middle feature of the structure words depending on the window size.  
    print('We have created mfeature list containing only the middle feature of the structure words depending on the window size')
    for structure in ordered_stru:
	    feat_list = list (structure)
	    for feature in range (int(windows/2), len(feat_list)-math.floor(windows/2)):
		    mfeature_list.append([feat_list[feature]])		

    #translate structure features into numerical code and in the last step also change them into integers
    print('translate structure features into numerical code and in the last step also change them into integers')
    from structure_dict import structure_dict
    for feature in range(0, len(mfeature_list)):
        for key in structure_dict:
            if key == mfeature_list [feature][0]:
                mfeature_list[feature][0] = int(structure_dict[key])
    print(datetime.now() - start)


#Cross validation in form of a manual Leave One Out and linear svm.
#########################################################################################################################
###This is an attempt to do the manual leave one out. The problem is probably in the lengthf list!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    #open list of length of each protein
    list_length = list(open('/home/u2208/project_course/projects/output/list_length.txt', 'r'))

#Here we convert the seq length list into integers cause it comes from a file as well as a string.
    for i in range (0, len(list_length)):
    	list_length[i] = list_length[i].strip('\n')
    	list_length[i] = int(list_length[i])

    #Here we convert the list of the protein lengths in an additive form so each number represents the sum of all the previous ones. This is needed so in the cross validation we can separate the words depending on what sequence they come from, so we dont train and test with words from the same protein.
    list_lengthf= [0]
    for i in range(0,len(list_length)):
        list_lengthf.append(list_length[i] + sum(list_length[0:i]))


    precision = 0
    recall = 0
    fscore = 0
    support = 0
    counter= 0
    complete_mcc = 0
    
    #clf = RandomForestClassifier().fit(X_train, Y_train)
    #clf = svm.LinearSVC(C=1)
    print("Machine learning with leave one out in process...")
    print()
    for i in range(1, len(list_lengthf)):
        X_test = word_listflat[list_lengthf[i-1]:list_lengthf[i]]
        Y_test = mfeature_list[list_lengthf[i-1]:list_lengthf[i]]
        X_train = word_listflat[0:list_lengthf[i-1]]+word_listflat[list_lengthf[i]:len(list_lengthf)]
        Y_train = mfeature_list[0:list_lengthf[i-1]]+mfeature_list[list_lengthf[i]:len(list_lengthf)]
        parameters = {'n_estimators': [70, 100, 500, 1000]}
        clf = GridSearchCV(RandomForestClassifier(), parameters)
        Y_train = [j for i in Y_train for j in i] 
        clf.fit(X_train, Y_train)
        Y_pred = clf.predict(X_test)
        Y_test = [j for i in Y_test for j in i]    
        p, r, f, s = precision_recall_fscore_support(Y_test, Y_pred)
        precision = precision + p
        recall = recall + r
        fscore = fscore + f
        support = support + s
        counter = counter + 1
        mcc = matthews_corrcoef(Y_test, Y_pred)
        complete_mcc = complete_mcc + mcc
    print()
    print('Best parameters set found on development set: ')
    print(clf.best_estimator_)
    print('Summarized results:')
    print('The mean precision with the model is: ', precision/56)
    print('The mean recall with the model is: ', recall/56)
    print('The mean fscore with the model is: ', fscore/56)
    print('The mean support with the model is: ', support/56)
    print('The Matthews correlation coefficient is: ', complete_mcc/56)

sys.exit()
###############################################################################################################################
#This way of doint the svm works!!! but cross validation is not optimal for me because leave one out is not happening. worst case i could do a loop over the train_test_split so that this process is repeated e.g.56 times and then just mean the scores for more precision.............

#simple linear SVM learning to test if program works, later include cross-val
#    X_train, X_test, Y_train, Y_test = train_test_split(word_listflat, mfeature_list, test_size=0.2)
#    clf = svm.LinearSVC(C=12.8175).fit(X_train, Y_train)
#    score = clf.score(X_test, Y_test)
#    print('The score is: ', score)
#    predicted_f = clf.predict(X_test)
#    Y_test = [j for i in Y_test for j in i]
#    print(classification_report(Y_test, predicted_f))
#    mcc = matthews_corrcoef(Y_test, predicted_f)
#    print('The matthews correlation coefficient is: ', mcc)
    
#    print(datetime.now() - start)


#GridSearchCV was used to optimize all the different parameters of the svm.
#    X_train, X_test, Y_train, Y_test = train_test_split(word_listflat, mfeature_list, test_size=0.5)
#    parameters = [{'C': [10, 12.8, 12.8175, 12.82, 12.85, 13, 20]}]
#    clf = GridSearchCV(LinearSVC(C=1), parameters)
#    Y_train = [j for i in Y_train for j in i]
#    clf.fit(X_train, Y_train)
#    print('Best parameters set found on development set: ')
#    print()
#    print(clf.best_estimator_)
#    Y_test = [j for i in Y_test for j in i]
#    Y_true, predicted_f = Y_test, clf.predict(X_test)
#    mcc = matthews_corrcoef(Y_true, predicted_f)
#    print('The matthews correlation coefficient is: ', mcc)


#This step is done to safe the model so it doesn't have to be trained every time we want to predict something

joblib.dump(clf, 'modelpssm_9_C1')

#To call back the model (and give it the name again of clf) we use the following:
#clf = joblib.load('modelpssm_9_C1')


