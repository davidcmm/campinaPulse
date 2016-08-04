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
	df = df.join(res)
	res = pd.get_dummies(df['income'])
	df = df.join(res)
	res = pd.get_dummies(df['marital'])
	df = df.join(res)
	res = pd.get_dummies(df['education'])
	df = df.join(res)

	#Images categorical information to dummy!
	res = pd.get_dummies(df['bairro1'], prefix="bairro1")
	df = df.join(res)
	res = pd.get_dummies(df['graffiti1'], prefix="graffiti1")
	df = df.join(res)
	res = pd.get_dummies(df['bairro2'], prefix="bairro2")
	df = df.join(res)
	res = pd.get_dummies(df['graffiti2'], prefix="graffiti2")
	df = df.join(res)
	
	return df

def train_classifiers(question, predictors, answer, parameters_dic, classifiers_names, classifiers):
	#Question being evaluated
	print ">>>>>> " + question

	i = 0
	predictors = np.array(predictors)
	answer = np.array(answer)
	classifiers_to_scale = ["Nearest Neighbors", "Linear SVM", "RBF SVM", "Naive Bayes"]
	for classifier_index in range(0, len(classifiers)):

		print "### Classifier " + str(classifiers_names[classifier_index])
		if parameters_dic.has_key(classifiers_names[classifier_index]):
			parameters_to_optimize = parameters_dic[classifiers_names[classifier_index]]
			print "### Param to opt " + str(parameters_to_optimize)

			for train, test in StratifiedKFold(answer, n_folds=5): #5folds

				if classifier_names[classifier_index] in classifiers_to_scale:#Some classifiers needs to scale input!
					predictors = StandardScaler().fit_transform(predictors)
				
				classifier = GridSearchCV(classifiers[classifier_index], 
				      param_grid=parameters_to_optimize, cv=3)
				predictors_train = predictors[train]
				answer_train = answer[train]
				clf = classifier.fit(predictors_train, answer_train)

				i += 1
				print('Fold', i)
				print(clf.best_estimator_)
				print()
		
				predictors_test = predictors[test]
				answer_test = answer[test]
				y_pred = clf.predict(predictors_test)

				#Vamo ver o F1. To usando micro, pode ser o macro. No paper, tem que mostrar os 2 mesmo.
				print('F1 score no teste, nunca use isto para escolher parametros. ' + \
				  'Aceite o valor, tuning de parametros so antes com o grid search', 
				  f1_score(answer_test, y_pred, average='micro'))
				print()
				print()


def stripDataFrame(df):
	df['gender'] = [x.lstrip(' \t\n\r').rstrip(' \t\n\r') for x in df['gender']]
	df['marital'] = [x.lstrip(' \t\n\r').rstrip(' \t\n\r') for x in df['marital']]
	df['income'] = [x.lstrip(' \t\n\r').rstrip(' \t\n\r') for x in df['income']]
	df['graffiti1'] = [x.lstrip(' \t\n\r').rstrip(' \t\n\r') for x in df['graffiti1']]
	df['graffiti2'] = [x.lstrip(' \t\n\r').rstrip(' \t\n\r') for x in df['graffiti2']]
	df['bairro1'] = [x.lstrip(' \t\n\r').rstrip(' \t\n\r') for x in df['bairro1']]
	df['bairro2'] = [x.lstrip(' \t\n\r').rstrip(' \t\n\r') for x in df['bairro2']]

	return df

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print "Uso: <arquivo com dados das preferencias de fotos, dados das fotos e dos usuarios> <phase - train or test> <filter, e.g., <gender, marital, age, income>-masculino>"
		sys.exit(1)

	df = pd.read_table(sys.argv[1], sep='\t', encoding='utf8', header=0)
	phase = sys.argv[2].lower()

	#Remove unecessary chars!
	df = stripDataFrame(df)

	if len(sys.argv) == 4:
		filter_group = sys.argv[3]
		group = filter_group.split("-")[1]
	else:
		filter_group = ""
		group = ""

	if len(filter_group) > 0:
		if 'gender' in filterGroup:
			df_to_use = df[(df.gender == group)]
		elif 'marital' in filterGroup:
			df_to_use = df[(df.marital == group)]
		elif 'income' in filterGroup:
			if group == 'media':		
				df_to_use = df[(df.income == "media") or (df.income == "media alta")]
			elif group == 'baixa':
				df_to_use = df[(df.income == "baixa") or (df.income == "media baixa")]
		elif 'age' in filterGroup:
			if age == 'adulto':
				df_to_use = df[(df.age >= 25)]
			elif age == 'jovem':
				df_to_use = df[(df.age >= 24)]
	else:
		df_to_use = df

	agrad_df = df_to_use[(df_to_use.question != "seguro?")]
	agrad_df = convertColumnsToDummy(agrad_df)
	answer_agrad = agrad_df['choice']#Preferred images
	predictors_agrad = agrad_df[['age', 'masculino', 'feminino', 'baixa', 'media baixa', 'media', 'media alta', 'graduacao', 'mestrado', 'doutorado', 'ensino medio', 'solteiro', 'casado', 'divorciado', 'vi\u00favo', 'street_wid1', 'mov_cars1', 'park_cars1', 'mov_ciclyst1', 'landscape1', 'build_ident1', 'trees1', 'build_height1', 'diff_build1', 'people1', 'graffiti1_No', 'graffiti1_Yes', 'bairro1_catole', 'bairro1_centro', 'bairro1_liberdade', 'mov_cars2', 'park_cars2', 'mov_ciclyst2', 'landscape2', 'build_ident2', 'trees2', 'build_height2', 'diff_build2', 'people2', 'graffiti2_No', 'graffiti2_Yes', 'bairro2_catole', 'bairro2_centro', 'bairro2_liberdade']].values #Predictors

	seg_df = df_to_use[(df_to_use.question == "seguro?")]
	seg_df = convertColumnsToDummy(seg_df)
	answer_seg = seg_df['choice']#Preferred images
	predictors_seg = seg_df[['age', 'masculino', 'feminino', 'baixa', 'media baixa', 'media', 'media alta', 'graduacao', 'mestrado', 'doutorado', 'ensino medio', 'solteiro', 'casado', 'divorciado', 'vi\u00favo', 'street_wid1', 'mov_cars1', 'park_cars1', 'mov_ciclyst1', 'landscape1', 'build_ident1', 'trees1', 'build_height1', 'diff_build1', 'people1', 'graffiti1_No', 'graffiti1_Yes', 'bairro1_catole', 'bairro1_centro', 'bairro1_liberdade', 'mov_cars2', 'park_cars2', 'mov_ciclyst2', 'landscape2', 'build_ident2', 'trees2', 'build_height2', 'diff_build2', 'people2', 'graffiti2_No', 'graffiti2_Yes', 'bairro2_catole', 'bairro2_centro', 'bairro2_liberdade']].values #Predictors

	#Classifiers to be used
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
		#'gamma' : ['Auto', 'RS*'],
		'gamma' : [0.25, 0.5, 1, 2, 4],
		'class_weight' : ['balanced', None]
	}
	}
	classifiers_names = ["Extra Trees", "Nearest Neighbors", "Linear SVM", "RBF SVM", "Naive Bayes"] #["Extra Trees", "Nearest Neighbors", "Linear SVM", 
	classifiers = [ExtraTreesClassifier(n_jobs=-1, criterion='entropy'), KNeighborsClassifier(3), SVC(kernel="linear", C=0.025), SVC(gamma=2, C=1), GaussianNB()]#ExtraTreesClassifier(n_jobs=-1, criterion='entropy'), KNeighborsClassifier(3), SVC(kernel="linear", C=0.025) ]
	
	if phase == 'train':
		train_classifiers("Pleasantness", predictors_agrad, answer_agrad, parameters_dic, classifiers_names, classifiers)
		train_classifiers("Safety", predictors_seg, answer_seg, parameters_dic, classifiers_names, classifiers)
	elif phase == 'test':

		for pair in [ ["Pleasantness", predictors_agrad, answer_agrad], ["Safety", predictors_seg, answer_seg] ]:
			for classifier_index in range(0, len(classifiers)):
				clf = classifiers[classifier_index]
				clf_name = classifiers_names[classifier_index]

				#Ok, parece que min_samples_leaf=16, min_samples_split=16 e uma boa. Quais as features importantes?
				#Vou retreinar na base toda e ver. Note que nao vou avaliar nada agora. Poderia fazer a mesma coisa
				#que fiz aqui para cada fold acima e tirar a media, e outra abordagem.
				#clf = ExtraTreesClassifier(min_samples_leaf=16, min_samples_split=16)
				clf.fit(pair[1], pair[2])

				#Feature importances me diz a importancia de cada feature. Maior == mais importante.
				#Depois voce pode mapear para o nome das suas features
				print ">>>> " + pair[0] + " " + clf_name
				print(clf.feature_importances_)
	else:
		print "Phase not selected correctly: train or test!"
		sys.exit(1)

	
	#>>>> Example with iris dataset
	#iris = datasets.load_iris()
	#print str(iris.data) + " " + str(len(iris.data))
	#print str(iris.target) + " " + str(len(iris.target))

	#gnb = GaussianNB()
	#y_pred = gnb.fit(iris.data, iris.target).predict(iris.data)
	#print str(type(iris.data)) + " " + str(type(iris.target))
	#print("Number of mislabeled points out of a total %d points : %d" % (iris.data.shape[0],(iris.target != y_pred).sum()))
