from sklearn import datasets
from sklearn.naive_bayes import GaussianNB
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_moons, make_circles, make_classification
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.metrics import precision_recall_fscore_support

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

import sys
import numpy as np
import json
import random

#Map user profile information into numbers!
genderDic = {"masculino" : 0, "feminino" : 1}
incomeDic = {"baixa" : 0, "media baixa" : 1, "media" : 2, "media alta" : 3, "alta" : 4}
educDic = {"ensino medio" : 0, "graduacao" : 1, "mestrado" : 2, "doutorado" : 3}
maritalDic = {"solteiro" : 0, "casado" : 1, "divorciado" : 2, "vi\\u00favo" : 3}

train_percent = 0.8

def convertUserInfo(userInfo):
	#age, gender, income, education, city, marital status
	age = userInfo[0].strip(' \t\n\r')
	gender = userInfo[1].strip(' \t\n\r')
	income = userInfo[2].strip(' \t\n\r')
	education = userInfo[3].strip(' \t\n\r')
	marital = userInfo[5].strip(' \t\n\r')

	return [int(age), genderDic[gender], incomeDic[income], educDic[education], maritalDic[marital]]

#Map image urban elements into numbers!
def convertImageInfo(imageInfo):
	neigDic = {"centro" : 0, "liberdade" : 1, "catole" : 2}
	graffitiDic = {"Yes" : 1, "No" : 0}
	
	newValues = []
	for i in range(0, len(imageInfo)):
		if i == 10 or i == 22:
			newValues.append(graffitiDic[imageInfo[i].strip(' \t\n\r')])
		elif i == 11 or i == 23:
			newValues.append(neigDic[imageInfo[i].strip(' \t\n\r')])
		else:
			newValues.append(float(imageInfo[i].strip(' \t\n\r')))

	return newValues

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Uso: <arquivo com dados das preferencias de fotos, dados das fotos e dos usuarios> <filter, e.g., <gender, marital, age, income>-masculino>"
		sys.exit(1)

	#Reading data for Como e Campina images!
	inputLines = open(sys.argv[1], 'r').readlines()
	answerAgrad = []
	predictorsAgrad = []
	answerSeg = []
	predictorsSeg = []

	if len(sys.argv) == 3:
		filterGroup = sys.argv[2]
		group = filterGroup.split("-")[1]
	else:
		filterGroup = ""
		group = ""

	for line in inputLines[1:]:
		lineData = line.split("\t")
		question = lineData[0]

		userInfoConverted = convertUserInfo(lineData[5:11])
		#userInfoConverted = []
		imageInfoConverted = convertImageInfo(lineData[11:])
		addExecution = False

		#Filtering groups to evaluate
		if len(filterGroup) > 0:
			#print str(userInfoConverted[1]) + " " + group + " " + str(userInfoConverted[1] == group)
			if 'gender' in filterGroup and userInfoConverted[1] == genderDic[group]:
				userInfoConverted.extend(imageInfoConverted)
				addExecution = True
			elif 'marital' in filterGroup and userInfoConverted[4] == maritalDic[group]:
				userInfoConverted.extend(imageInfoConverted)
				addExecution = True
			elif 'age' in filterGroup and ( (group == 'jovem' and userInfoConverted[0] <= 24) or (group == 'adulto' and userInfoConverted[0] >= 25) ):
				userInfoConverted.extend(imageInfoConverted)
				addExecution = True
			elif 'income' in filterGroup and ( (group == 'media' and (userInfoConverted[2] == incomeDic['media'] or userInfoConverted[2] == incomeDic['media alta'])) or (group == 'baixa' and (userInfoConverted[2] == incomeDic['baixa'] or userInfoConverted[2] == incomeDic['media baixa'])) ):	
				userInfoConverted.extend(imageInfoConverted)
				addExecution = True
		elif len(filterGroup) == 0:
			userInfoConverted.extend(imageInfoConverted)
			addExecution = True

		#Grouping per question
		if 'agrad' in question.lower() and addExecution:
			answerAgrad.append(int(lineData[3]))#Preferred image
			predictorsAgrad.append(userInfoConverted)#Predictors
		elif addExecution:
			answerSeg.append(int(lineData[3]))#Preferred image
			predictorsSeg.append(userInfoConverted)#Predictors

	#Building classifiers
	classifiersNames = ["Nearest Neighbors", "Linear SVM", "RBF SVM", "Decision Tree",
         "Random Forest", "AdaBoost", "Naive Bayes", "Linear Discriminant Analysis",
         "Quadratic Discriminant Analysis"]

	classifiers = [
	    KNeighborsClassifier(3),
	    SVC(kernel="linear", C=0.025),
	    SVC(gamma=2, C=1),
	    DecisionTreeClassifier(max_depth=5),
	    RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
	    AdaBoostClassifier(),
	    GaussianNB(),
	    LinearDiscriminantAnalysis(),
	    QuadraticDiscriminantAnalysis()]

	#Pleasantness
	indexesToTrain = random.sample( range(0,len(answerAgrad)), int(len(answerAgrad)*train_percent) )#Separating training data and test data!
	indexesToTest = list( set(range(0, len(answerAgrad))) - set(indexesToTrain) )

	predictorsInput = np.array(predictorsAgrad)[indexesToTrain]
	answersInput = np.array(answerAgrad)[indexesToTrain]
	predictorsOutput = np.array(predictorsAgrad)[indexesToTest]
	answersOutput = np.array(answerAgrad)[indexesToTest]

	#Iterate over classifiers
	print ">>>>>> Pleasantness " + str(len(indexesToTrain)) + " " + str(len(indexesToTest)) 
	print "Classifier\tmean accuracy\t(precision,\trecall,\tf1)"
	for name, clf in zip(classifiersNames, classifiers):
		clf.fit(predictorsInput, answersInput)
		y_pred = clf.fit( predictorsInput, answersInput ).predict( predictorsOutput )
		score = clf.score(predictorsOutput, answersOutput)
		myAcc = (answersOutput == y_pred).sum() * 1.0 / (len(y_pred))
		print "CORRE " + str((answersOutput == y_pred).sum()) + " " + str(len(y_pred))

		metrics = precision_recall_fscore_support(answersOutput, y_pred, average='macro')
		print name + " " + str(score) + " " + str(metrics)


	#Safety
	indexesToTrain = random.sample( range(0,len(answerSeg)), int(len(answerSeg)*train_percent) )#Separating training data and test data!
	indexesToTest = list( set(range(0, len(answerSeg))) - set(indexesToTrain) )

	predictorsInput = np.array(predictorsSeg)[indexesToTrain]
	answersInput = np.array(answerSeg)[indexesToTrain]
	predictorsOutput = np.array(predictorsSeg)[indexesToTest]
	answersOutput = np.array(answerSeg)[indexesToTest]

	#Iterate over classifiers
	print ">>>>>> Safety " + str(len(indexesToTrain)) + " " + str(len(indexesToTest)) 
	print "Classifier\tmean accuracy\t(precision,\trecall,\tf1)"
	for name, clf in zip(classifiersNames, classifiers):
		clf.fit(predictorsInput, answersInput)
		y_pred = clf.fit( predictorsInput, answersInput ).predict( predictorsOutput )
		score = clf.score(predictorsOutput, answersOutput)

		metrics = precision_recall_fscore_support(answersOutput, y_pred, average='macro')
		print name + " " + str(score) + " " + str(metrics)

	#>>>> Example with iris dataset
	#iris = datasets.load_iris()
	#print str(iris.data) + " " + str(len(iris.data))
	#print str(iris.target) + " " + str(len(iris.target))

	#gnb = GaussianNB()
	#y_pred = gnb.fit(iris.data, iris.target).predict(iris.data)
	#print str(type(iris.data)) + " " + str(type(iris.target))
	#print("Number of mislabeled points out of a total %d points : %d" % (iris.data.shape[0],(iris.target != y_pred).sum()))
