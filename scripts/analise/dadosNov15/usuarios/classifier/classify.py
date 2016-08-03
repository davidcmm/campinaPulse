import pandas as pd

from sklearn import datasets
from sklearn.naive_bayes import GaussianNB
from sklearn.cross_validation import train_test_split, StratifiedKFold
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.datasets import make_moons, make_circles, make_classification
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, ExtraTreesClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.metrics import precision_recall_fscore_support, accuracy_score, f1_score
from sklearn.grid_search import GridSearchCV

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

def testComposition(indexesToTrain, predictorsAgrad, currentSet):
	#Testing composition
	young = 0
	adult = 0
	low = 0
	high = 0
	men = 0
	women = 0
	single = 0
	married = 0
	genderDic = {"masculino" : 0, "feminino" : 1}
	incomeDic = {"baixa" : 0, "media baixa" : 1, "media" : 2, "media alta" : 3, "alta" : 4}
	educDic = {"ensino medio" : 0, "graduacao" : 1, "mestrado" : 2, "doutorado" : 3}
	maritalDic = {"solteiro" : 0, "casado" : 1, "divorciado" : 2, "vi\\u00favo" : 3}

	for index in indexesToTrain:
		answer = predictorsAgrad[index]
		if answer[0] <= 24:
			young = young + 1
		elif answer[0] >= 25:
			adult = adult + 1

		if answer[1] == 0:
			men = men + 1
		elif answer[1] == 1:
			women = women + 1

		if answer[2] == 0 or answer[2] == 1:
			low = low + 1
		elif answer[2] == 2 or answer[2] == 3:
			high = high + 1

		if answer[4] == 0:
			single = single + 1
		elif answer[4] == 1:
			married = married + 1

	print ">>>> COMPOSITION OF " + currentSet  + ": Y-" + str(young) + " A-" + str(adult) + " M-" + str(men) + " W-" + str(women) + " L-" + str(low) + " H-" + str(high) + " S-" + str(single) + " M-" + str(married)


#PANDAS OPERATIONS!
	#df[['age', 'gender', 'income', 'education', 'city', 'marital']]
	#df[['street_wid1', 'mov_cars1', 'park_cars1', 'mov_ciclyst1', 'landscape1', 'build_ident1', 'trees1', 'build_height1', 'diff_build1', 'people1', 'graffiti1', 'bairro1', 'mov_cars2', 'park_cars2', 'mov_ciclyst2', 'landscape2', 'build_ident2', 'trees2', 'build_height2', 'diff_build2', 'people2', 'graffiti2', 'bairro2']]

	#res = pd.get_dummies(df['gender'])
	#df.join(res)

	#df[(df.question == 'seguro?')]#filter!
#PANDAS
def convertColumnsToDummy(df):
	#Users categorical information to dummy!	
	res = pd.get_dummies(df['gender'])
	df.join(res)
	res = pdf.get_dummies(df['income'])
	df.join(res)
	res = pdf.get_dummies(df['marital'])
	df.join(res)
	res = pdf.get_dummies(df['education'])
	df.join(res)

	#Images categorical information to dummy!
	res = pd.get_dummies(df['bairro1'], prefix="bairro1")
	df.join(res)
	res = pd.get_dummies(df['graffiti1'], prefix="graffiti1")
	df.join(res)
	res = pd.get_dummies(df['bairro2'], prefix="bairro2")
	df.join(res)
	res = pd.get_dummies(df['graffiti2'], prefix="graffiti2")
	df.join(res)
	
	return df

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Uso: <arquivo com dados das preferencias de fotos, dados das fotos e dos usuarios> <phase - train or test> <filter, e.g., <gender, marital, age, income>-masculino>"
		sys.exit(1)

	#df = pd.read_table(sys.argv[1], sep='\t', encoding='utf8', header=0)
	#phase = sys.argv[2].lower()
	#if len(sys.argv) == 3:
	#	filter_group = sys.argv[3]
	#	group = filter_group.split("-")[1]
	#else:
	#	filter_group = ""
	#	group = ""
	#if len(filterGroup) > 0:
	#	if 'gender' in filterGroup:
	#		df_to_use = df[(df.gender == group)]
	#	elif 'marital' in filterGroup:
	#		df_to_use = df[(df.marital == group)]
	#	elif 'income' in filterGroup:
	#		if group == 'media':		
	#			df_to_use = df[(df.income == "media") or (df.income == "media alta")]
	#		elif group == 'baixa':
	#			df_to_use = df[(df.income == "baixa") or (df.income == "media baixa")]
	#	elif 'age' in filterGroup:
	#		if age == 'adulto':
	#			df_to_use = df[(df.age >= 25)]
	#		elif age == 'jovem':
	#			df_to_use = df[(df.age >= 24)]
	#else:
	#	df_to_use = df
	#agrad_df = df_to_use[(df_to_use.question != "seguro?")]
	#agrad_df = convertColumnsToDummy(agrad_df)
	#answerAgrad = agrad_df['choice']    .append(int(lineData[3]))#Preferred image
	#predictorsAgrad = agrad_df[['age', 'masculino', 'feminino', 'baixa', 'media baixa', 'media', 'media alta', 'graduacao', 'mestrado', 'doutorado', 'ensino medio', 'solteiro', 'casado', 'divorciado', 'vi\u00favo', 'street_wid1', 'mov_cars1', 'park_cars1', 'mov_ciclyst1', 'landscape1', 'build_ident1', 'trees1', 'build_height1', 'diff_build1', 'people1', 'graffiti1_No', 'graffiti1_Yes', 'bairro1_catole', 'bairro1_centro', 'bairro1_liberdade', 'mov_cars2', 'park_cars2', 'mov_ciclyst2', 'landscape2', 'build_ident2', 'trees2', 'build_height2', 'diff_build2', 'people2', 'graffiti2_No', 'graffiti2_Yes', 'bairro2_catole', 'bairro2_centro', 'bairro2_liberdade']].values #Predictors
	#seg_df = df_to_use[(df_to_use.question == "seguro?")]
	#seg_df = convertColumnsToDummy(seg_df)
	#answerSeg = seg_df['choice']    .append(int(lineData[3]))#Preferred image
	#predictorsSeg = seg_df[['age', 'masculino', 'feminino', 'baixa', 'media baixa', 'media', 'media alta', 'graduacao', 'mestrado', 'doutorado', 'ensino medio', 'solteiro', 'casado', 'divorciado', 'vi\u00favo', 'street_wid1', 'mov_cars1', 'park_cars1', 'mov_ciclyst1', 'landscape1', 'build_ident1', 'trees1', 'build_height1', 'diff_build1', 'people1', 'graffiti1_No', 'graffiti1_Yes', 'bairro1_catole', 'bairro1_centro', 'bairro1_liberdade', 'mov_cars2', 'park_cars2', 'mov_ciclyst2', 'landscape2', 'build_ident2', 'trees2', 'build_height2', 'diff_build2', 'people2', 'graffiti2_No', 'graffiti2_Yes', 'bairro2_catole', 'bairro2_centro', 'bairro2_liberdade']].values #Predictors

	
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
	#classifiersNames = ["Nearest Neighbors", "Linear SVM", "RBF SVM", "Decision Tree",
        # "Random Forest", "AdaBoost", "Naive Bayes", "Linear Discriminant Analysis",
        # "Quadratic Discriminant Analysis"]

	#classifiers = [
	#    KNeighborsClassifier(3),
	#    SVC(kernel="linear", C=0.025),
	#    SVC(gamma=2, C=1),
	#    DecisionTreeClassifier(max_depth=5),
	#    RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1),
	#    AdaBoostClassifier(),
	#    GaussianNB(),
	#    LinearDiscriminantAnalysis(),
	#    QuadraticDiscriminantAnalysis()]

	parameters_dic = { "Extra Trees" : {
	    'n_estimators': [20, 40, 60],
	    'criterion': ['entropy'],
	    'min_samples_split': [2, 4, 8, 16, 32],
	    'min_samples_leaf': [2, 4, 8, 16, 32]
	}, 
	"Nearest Neighbors" : {
		'n_neighbors' : [2, 4, 8, 16, 32],
		'p' : [2,3]	
	},
	"Linear SVM" : {
		'C' : [0.001, 0.1, 1],
		'class_weight' : ['balanced', None]
	},
	"RBF SVM" : {
		'C' : [0.001, 0.1, 1],
		'gamma' : ['Auto', 'RS*'],
		'class_weight' : ['balanced', None]
	}
	}
	classifiersNames = ["Linear SVM", "RBF SVM", "Naive Bayes"] #["Extra Trees", "Nearest Neighbors", 
	classifiers = [SVC(kernel="linear", C=0.025), SVC(gamma=2, C=1), GaussianNB()]#ExtraTreesClassifier(n_jobs=-1, criterion='entropy'), KNeighborsClassifier(3),  ]
	
	#Pleasantness
	print ">>>>>> Pleasantness "

	i = 0
	predictorsAgrad = np.array(predictorsAgrad)
	answerAgrad = np.array(answerAgrad)
	for classifierIndex in range(0, len(classifiers)):

		print "### Classifier " + str(classifiersNames[classifierIndex])
		if parameters_dic.has_key(classifiersNames[classifierIndex]):
			parameters_to_optimize = parameters_dic[classifiersNames[classifierIndex]]
			print "### Param to opt " + str(parameters_to_optimize)

			for train, test in StratifiedKFold(answerAgrad, n_folds=5): #5folds

				classifier = GridSearchCV(classifiers[classifierIndex], 
				      param_grid=parameters_to_optimize, cv=3)
				predictorsTrain = predictorsAgrad[train]
				answerTrain = answerAgrad[train]
				clf = classifier.fit(predictorsTrain, answerTrain)

				i += 1
				print('Fold', i)
				print(clf.best_estimator_)
				print()
		
				predictorsTest = predictorsAgrad[test]
				answerTest = answerAgrad[test]
				y_pred = clf.predict(predictorsTest)

				#Vamo ver o F1. To usando micro, pode ser o macro. No paper, tem que mostrar os 2 mesmo.
				print('F1 score no teste, nunca use isto para escolher parametros. ' + \
				  'Aceite o valor, tuning de parametros so antes com o grid search', 
				  f1_score(answerTest, y_pred, average='micro'))
				print()
				print()


	#Ok, parece que min_samples_leaf=16, min_samples_split=16 e uma boa. Quais as features importantes?
	#Vou retreinar na base toda e ver. Note que nao vou avaliar nada agora. Poderia fazer a mesma coisa
	#que fiz aqui para cada fold acima e tirar a media, e outra abordagem.
	clf = ExtraTreesClassifier(min_samples_leaf=16, min_samples_split=16)
	clf.fit(predictorsAgrad, answerAgrad)

	#Feature importances me diz a importancia de cada feature. Maior == mais importante.
	#Depois voce pode mapear para o nome das suas features
	print(clf.feature_importances_)

	#indexesToTrain = random.sample( range(0,len(answerAgrad)), int(len(answerAgrad)*train_percent) )#Separating training data and test data!
	#indexesToTest = list( set(range(0, len(answerAgrad))) - set(indexesToTrain) )

	#Testing composition
	#testComposition(indexesToTrain, predictorsAgrad, "TRAIN")  
	#testComposition(indexesToTest, predictorsAgrad, "TEST")  

	#Creating train and test datasets
	#predictorsInput = np.array(predictorsAgrad)[indexesToTrain]
	#answersInput = np.array(answerAgrad)[indexesToTrain]
	#predictorsOutput = np.array(predictorsAgrad)[indexesToTest]
	#answersOutput = np.array(answerAgrad)[indexesToTest]

	#Iterate over classifiers
	#print ">>>>>> Pleasantness " + str(len(indexesToTrain)) + " " + str(len(indexesToTest)) 
	#print "Classifier\tmean accuracy\t(precision,\trecall,\tf1)"
	#for name, clf in zip(classifiersNames, classifiers):
		#clf.fit(predictorsInput, answersInput)
		#y_pred = clf.fit( predictorsInput, answersInput ).predict( predictorsOutput )#Predicted values
		#score = clf.score(predictorsOutput, answersOutput)#Accuracy score
		#myAcc = (answersOutput == y_pred).sum() * 1.0 / (len(y_pred))
		#myAcc = accuracy_score(answersOutput, y_pred)
		#print "CORRE " + str(myAcc)

		#metrics = precision_recall_fscore_support(answersOutput, y_pred, average='macro', labels=['1', '0', '-1'])#Calculates for each label and compute the mean!
		#print name + " " + str(score) + " MACRO " + str(metrics)
		#metrics = precision_recall_fscore_support(answersOutput, y_pred, average='micro', labels=['1', '0', '-1'])#Total false positives, negatives and true positives -> more similar to accuracy
		#print name + " " + str(score) + " MICRO " + str(metrics)

	#Safety
	print ">>>>>> Safety "
	#indexesToTrain = random.sample( range(0,len(answerSeg)), int(len(answerSeg)*train_percent) )#Separating training data and test data!
	#indexesToTest = list( set(range(0, len(answerSeg))) - set(indexesToTrain) )

	#Testing composition
	#testComposition(indexesToTrain, predictorsSeg, "TRAIN")
	#testComposition(indexesToTest, predictorsSeg, "TEST")    

	#Creating train and test datasets
	#predictorsInput = np.array(predictorsSeg)[indexesToTrain]
	#answersInput = np.array(answerSeg)[indexesToTrain]
	#predictorsOutput = np.array(predictorsSeg)[indexesToTest]
	#answersOutput = np.array(answerSeg)[indexesToTest]

	#Iterate over classifiers
	#print ">>>>>> Safety " + str(len(indexesToTrain)) + " " + str(len(indexesToTest)) 
	#print "Classifier\tmean accuracy\t(precision,\trecall,\tf1)"
	#for name, clf in zip(classifiersNames, classifiers):
#		clf.fit(predictorsInput, answersInput)
#		y_pred = clf.fit( predictorsInput, answersInput ).predict( predictorsOutput )
#		score = clf.score(predictorsOutput, answersOutput)
#
#		metrics = precision_recall_fscore_support(answersOutput, y_pred, average='macro', labels=['1', '0', '-1'])#Calculates for each label and compute the mean!
#		print name + " " + str(score) + " MACRO " + str(metrics)
#		metrics = precision_recall_fscore_support(answersOutput, y_pred, average='micro', labels=['1', '0', '-1'])#Total false positives, negatives and true positives -> more similar to accuracy
#		print name + " " + str(score) + " MICRO " + str(metrics)
	i = 0
	predictorsSeg = np.array(predictorsSeg)
	answerSeg = np.array(answerSeg)
	for classifierIndex in range(0, len(classifiers)):

		print "### Classifier " + str(classifiersNames[classifierIndex])
		if parameters_dic.has_key(classifiersNames[classifierIndex]):
			parameters_to_optimize = parameters_dic[classifiersNames[classifierIndex]]

			for train, test in StratifiedKFold(answerSeg, n_folds=5): #5folds

				classifier = GridSearchCV(classifiers[classifierIndex], 
				      param_grid=parameters_to_optimize, cv=3)
				predictorsTrain = predictorsSeg[train]
				answerTrain = answerSeg[train]
				clf = classifier.fit(predictorsTrain, answerTrain)

				i += 1
				print('Fold', i)
				print(clf.best_estimator_)
				print()
		
				predictorsTest = predictorsSeg[test]
				answerTest = answerSeg[test]
				y_pred = clf.predict(predictorsTest)

				#Vamo ver o F1. To usando micro, pode ser o macro. No paper, tem que mostrar os 2 mesmo.
				print('F1 score no teste, nunca use isto para escolher parametros. ' + \
				  'Aceite o valor, tuning de parametros so antes com o grid search', 
				  f1_score(answerTest, y_pred, average='micro'))
				print()
				print()



	clf = ExtraTreesClassifier(min_samples_leaf=16, min_samples_split=16)
	clf.fit(predictorsSeg, answerSeg)

	#Feature importances me diz a importancia de cada feature. Maior == mais importante.
	#Depois voce pode mapear para o nome das suas features
	print(clf.feature_importances_)




	#>>>> Example with iris dataset
	#iris = datasets.load_iris()
	#print str(iris.data) + " " + str(len(iris.data))
	#print str(iris.target) + " " + str(len(iris.target))

	#gnb = GaussianNB()
	#y_pred = gnb.fit(iris.data, iris.target).predict(iris.data)
	#print str(type(iris.data)) + " " + str(type(iris.target))
	#print("Number of mislabeled points out of a total %d points : %d" % (iris.data.shape[0],(iris.target != y_pred).sum()))
