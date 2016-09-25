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
from sklearn.metrics import precision_recall_fscore_support, accuracy_score, f1_score, confusion_matrix
from sklearn.grid_search import GridSearchCV
from sklearn.feature_selection import RFECV, SelectFromModel

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

import sys
import numpy as np
import json
import random
import collections
import operator

from scipy import stats
from sets import Set

#PANDAS OPERATIONS!
	#df[['age', 'gender', 'income', 'education', 'city', 'marital']]
	#df[['street_wid1', 'mov_cars1', 'park_cars1', 'mov_ciclyst1', 'landscape1', 'build_ident1', 'trees1', 'build_height1', 'diff_build1', 'people1', 'graffiti1', 'bairro1', 'mov_cars2', 'park_cars2', 'mov_ciclyst2', 'landscape2', 'build_ident2', 'trees2', 'build_height2', 'diff_build2', 'people2', 'graffiti2', 'bairro2']]

	#res = pd.get_dummies(df['gender'])
	#df.join(res)

	#df[(df.question == 'seguro?')]#filter!
#PANDAS

classifiers_to_scale = ["Nearest Neighbors", "Linear SVM", "RBF SVM", "Naive Bayes"]

def load_classifiers_wodraw(group):
	#Building classifiers according to best configuration per group (SO EXTRA ATUALIZADO!)
	if group == 'masculino':
		classifiers_agrad = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy', max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=8, min_samples_split=2, min_weight_fraction_leaf=0.0, n_estimators=60, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False), KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', metric_params=None, n_jobs=1, n_neighbors=4, p=2, weights='uniform'), SVC(C=1, cache_size=200, class_weight='balanced', coef0=0.0, decision_function_shape=None, degree=3, gamma=0.25, kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True,  tol=0.001, verbose=False), GaussianNB(), SVC(C=0.001, cache_size=200, class_weight=None, gamma='auto', kernel='linear') ]
		classifiers_seg = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy', max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=4, min_samples_split=8,           min_weight_fraction_leaf=0.0, n_estimators=40, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False), KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', metric_params=None, n_jobs=1, n_neighbors=16, p=2, weights='uniform'), SVC(C=1, cache_size=200, class_weight=None, coef0=0.0, decision_function_shape=None, degree=3, gamma=0.5, kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False), GaussianNB(), SVC(C=0.001, cache_size=200, class_weight=None, gamma='auto', kernel='linear') ]

	elif group == 'feminino':
		classifiers_agrad = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy', max_depth=None, max_features='auto', max_leaf_nodes=None,  min_samples_leaf=2, min_samples_split=4,           min_weight_fraction_leaf=0.0, n_estimators=40, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False), KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', metric_params=None, n_jobs=1, n_neighbors=32, p=2, weights='uniform'), SVC(C=1, cache_size=200, class_weight='balanced', coef0=0.0, decision_function_shape=None, degree=3, gamma=0.25, kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False), GaussianNB(), SVC(C=0.001, cache_size=200, class_weight=None, gamma='auto', kernel='linear') ]
		classifiers_seg = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy', max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=4, min_samples_split=8,            min_weight_fraction_leaf=0.0, n_estimators=20, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False), KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', metric_params=None, n_jobs=1, n_neighbors=32, p=2, weights='uniform'), SVC(C=1, cache_size=200, class_weight=None, coef0=0.0, decision_function_shape=None, degree=3, gamma=0.25, kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False), GaussianNB(), SVC(C=0.001, cache_size=200, class_weight=None, gamma='auto', kernel='linear') ]

	elif group == 'jovem':
		classifiers_agrad = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy', max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=2, min_samples_split=32, min_weight_fraction_leaf=0.0, n_estimators=60, n_jobs=-1,           oob_score=False, random_state=None, verbose=0, warm_start=False), KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', metric_params=None, n_jobs=1, n_neighbors=32, p=2,           weights='uniform'), SVC(C=1, cache_size=200, class_weight='balanced', coef0=0.0, decision_function_shape=None, degree=3, gamma=0.25, kernel='rbf',   max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False), GaussianNB(), SVC(C=0.1, cache_size=200, class_weight=None, coef0=0.0, decision_function_shape=None, degree=3, gamma='auto', kernel='linear',   max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False) ]
		classifiers_seg = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy', max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=2, min_samples_split=16, min_weight_fraction_leaf=0.0, n_estimators=40, n_jobs=-1,            oob_score=False, random_state=None, verbose=0, warm_start=False), KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', metric_params=None, n_jobs=1, n_neighbors=16, p=2,           weights='uniform'), SVC(C=1, cache_size=200, class_weight='balanced', coef0=0.0, decision_function_shape=None, degree=3, gamma=0.25, kernel='rbf',   max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False), GaussianNB(), SVC(C=0.001, cache_size=200, class_weight=None, coef0=0.0, decision_function_shape=None, degree=3, gamma='auto', kernel='linear',   max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False) ]

	elif group == 'adulto':
		classifiers_agrad = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy', max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=8, min_samples_split=16,            min_weight_fraction_leaf=0.0, n_estimators=20, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False), KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', metric_params=None, n_jobs=1, n_neighbors=16, p=2, weights='uniform'), SVC(C=1, cache_size=200, class_weight=None, coef0=0.0, decision_function_shape=None, degree=3, gamma=0.25, kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False), GaussianNB(), SVC(C=0.001, cache_size=200, class_weight=None, gamma='auto', kernel='linear') ]
		classifiers_seg = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy', max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=8, min_samples_split=4,            min_weight_fraction_leaf=0.0, n_estimators=60, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False), KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', metric_params=None, n_jobs=1, n_neighbors=32, p=2, weights='uniform'), SVC(C=1, cache_size=200, class_weight=None, coef0=0.0, decision_function_shape=None, degree=3, gamma=0.25, kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False), GaussianNB(), SVC(C=0.001, cache_size=200, class_weight=None, gamma='auto', kernel='linear') ]
	
	elif group == 'baixa':
		classifiers_agrad = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy', max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=2, min_samples_split=32,            min_weight_fraction_leaf=0.0, n_estimators=60, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False), KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski',  metric_params=None, n_jobs=1, n_neighbors=32, p=2, weights='uniform'), SVC(C=1, cache_size=200, class_weight=None, coef0=0.0, decision_function_shape=None, degree=3, gamma=0.25, kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False), GaussianNB(), SVC(C=0.001, cache_size=200, class_weight=None, gamma='auto', kernel='linear') ]
		classifiers_seg = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy', max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=4, min_samples_split=2,            min_weight_fraction_leaf=0.0, n_estimators=20, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False), KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', metric_params=None, n_jobs=1, n_neighbors=16, p=3, weights='uniform'), SVC(C=1, cache_size=200, class_weight='balanced', coef0=0.0, decision_function_shape=None, degree=3, gamma=0.25, kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False), GaussianNB(), SVC(C=0.001, cache_size=200, class_weight=None, gamma='auto', kernel='linear') ]

	elif group == 'media':
		classifiers_agrad = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy', max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=8, min_samples_split=2,           min_weight_fraction_leaf=0.0, n_estimators=60, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False), KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', metric_params=None, n_jobs=1, n_neighbors=16, p=2, weights='uniform'), SVC(C=1, cache_size=200, class_weight='balanced', coef0=0.0, decision_function_shape=None, degree=3, gamma=0.25, kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False), GaussianNB(), SVC(C=0.001, cache_size=200, class_weight=None, gamma='auto', kernel='linear') ]
		classifiers_seg = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy', max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=4, min_samples_split=4,            min_weight_fraction_leaf=0.0, n_estimators=40, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False), KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', metric_params=None, n_jobs=1, n_neighbors=8, p=3, weights='uniform'), SVC(C=1, cache_size=200, class_weight=None, coef0=0.0, decision_function_shape=None, degree=3, gamma=0.25, kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False), GaussianNB(), SVC(C=0.001, cache_size=200, class_weight=None, gamma='auto', kernel='linear') ]

	elif group == 'solteiro':
		classifiers_agrad = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy', max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=2, min_samples_split=8,            min_weight_fraction_leaf=0.0, n_estimators=60, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False), KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', metric_params=None, n_jobs=1, n_neighbors=8, p=2, weights='uniform'), SVC(C=1, cache_size=200, class_weight=None, coef0=0.0, decision_function_shape=None, degree=3, gamma=0.25, kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False), GaussianNB(), SVC(C=0.001, cache_size=200, class_weight=None, gamma='auto', kernel='linear') ]
		classifiers_seg = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy', max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=4, min_samples_split=2,            min_weight_fraction_leaf=0.0, n_estimators=40, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False), KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', metric_params=None, n_jobs=1, n_neighbors=32, p=2, weights='uniform'), SVC(C=1, cache_size=200, class_weight=None, coef0=0.0, decision_function_shape=None, degree=3, gamma=0.25, kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False), GaussianNB(), SVC(C=0.001, cache_size=200, class_weight=None, gamma='auto', kernel='linear') ]
	
	elif group == 'casado':
		classifiers_agrad = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy', max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=8, min_samples_split=4,            min_weight_fraction_leaf=0.0, n_estimators=20, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False), KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', metric_params=None, n_jobs=1, n_neighbors=16, p=2, weights='uniform'), SVC(C=1, cache_size=200, class_weight='balanced', coef0=0.0, decision_function_shape=None, degree=3, gamma=0.25, kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False), GaussianNB(), SVC(C=0.001, cache_size=200, class_weight=None, gamma='auto', kernel='linear') ]
		classifiers_seg = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy', max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=2, min_samples_split=16,            min_weight_fraction_leaf=0.0, n_estimators=60, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False), KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', metric_params=None, n_jobs=1, n_neighbors=32, p=3, weights='uniform'), SVC(C=1, cache_size=200, class_weight=None, coef0=0.0, decision_function_shape=None, degree=3, gamma=0.25, kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False), GaussianNB(), SVC(C=0.001, cache_size=200, class_weight=None, gamma='auto', kernel='linear') ]

	elif group == "modal-80":#All users (more common param for each group - Extra)
		classifiers_agrad = [ ExtraTreesClassifier(class_weight=None, criterion='entropy', min_samples_leaf=8, min_samples_split=2, n_estimators=60, n_jobs=-1, oob_score=False) ]

		classifiers_seg = [ ExtraTreesClassifier(class_weight=None, criterion='entropy', min_samples_leaf=4, min_samples_split=8, n_estimators=40, n_jobs=-1, oob_score=False) ]
	
	elif group == "modal-leave":#All users (more common param for each group - Extra)
		classifiers_agrad = [ ExtraTreesClassifier(class_weight=None, criterion='entropy', max_features="auto", max_depth=None, min_samples_leaf=8, min_samples_split=32, n_estimators=60, n_jobs=-1, oob_score=False) ]

		classifiers_seg = [ ExtraTreesClassifier(class_weight=None, criterion='entropy', max_features="auto", max_depth=None, min_samples_leaf=4, min_samples_split=8, n_estimators=60, n_jobs=-1, oob_score=False) ]

	elif group == "all":#All features in best configuration 80-20
		classifiers_agrad = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy',           max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=2, min_samples_split=32,         min_weight_fraction_leaf=0.0, n_estimators=60, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False) ]

		classifiers_seg = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy',           max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=2, min_samples_split=4,           min_weight_fraction_leaf=0.0, n_estimators=60, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False) ]
	
	else:
		classifiers_agrad = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy',           max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=8, min_samples_split=8,          min_weight_fraction_leaf=0.0, n_estimators=60, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False) ]

		classifiers_seg = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy',           max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=8, min_samples_split=8,            min_weight_fraction_leaf=0.0, n_estimators=60, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False) ]


	return [classifiers_agrad, classifiers_seg]

def load_classifiers_3classes(group):
	#Building classifiers according to best configuration per group (FALTA LINEAR!)
	if group == 'masculino':
		classifiers_agrad = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy', max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=8, min_samples_split=4, min_weight_fraction_leaf=0.0, n_estimators=20, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False), KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', metric_params=None, n_jobs=1, n_neighbors=32, p=2, weights='uniform'), SVC(C=1, cache_size=200, class_weight=None, coef0=0.0, decision_function_shape=None, degree=3, gamma=0.25, kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False), GaussianNB(), SVC(C=0.001, cache_size=200, class_weight=None, gamma='auto', kernel='linear') ]
		classifiers_seg = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy', max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=8, min_samples_split=32, min_weight_fraction_leaf=0.0, n_estimators=40, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False), KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', metric_params=None, n_jobs=1, n_neighbors=32, p=3, weights='uniform'), SVC(C=1, cache_size=200, class_weight=None, coef0=0.0, decision_function_shape=None, degree=3, gamma=0.5, kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False), GaussianNB(), SVC(C=0.001, cache_size=200, class_weight=None, gamma='auto', kernel='linear') ]

	elif group == 'feminino':
		classifiers_agrad = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy', max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=8, min_samples_split=16, min_weight_fraction_leaf=0.0, n_estimators=60, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False), KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', metric_params=None, n_jobs=1, n_neighbors=4, p=2, weights='uniform'), SVC(C=1, cache_size=200, class_weight=None, coef0=0.0, decision_function_shape=None, degree=3, gamma=0.25, kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False), GaussianNB(), SVC(C=0.001, cache_size=200, class_weight=None, gamma='auto', kernel='linear') ]
		classifiers_seg = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy', max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=8, min_samples_split=2, min_weight_fraction_leaf=0.0, n_estimators=60, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False), KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', metric_params=None, n_jobs=1, n_neighbors=32, p=2, weights='uniform'), SVC(C=1, cache_size=200, class_weight=None, coef0=0.0, decision_function_shape=None, degree=3, gamma=0.25, kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False), GaussianNB(), SVC(C=0.001, cache_size=200, class_weight=None, gamma='auto', kernel='linear') ]

	elif group == 'jovem':
		classifiers_agrad = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy', max_depth=None, max_features='auto',  max_leaf_nodes=None, min_samples_leaf=4, min_samples_split=16, min_weight_fraction_leaf=0.0, n_estimators=20, n_jobs=-1,            oob_score=False, random_state=None, verbose=0, warm_start=False), KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', metric_params=None, n_jobs=1, n_neighbors=4, p=3,           weights='uniform'), SVC(C=1, cache_size=200, class_weight=None, coef0=0.0, decision_function_shape=None, degree=3, gamma=0.25, kernel='rbf',   max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False), GaussianNB(), SVC(C=0.001, cache_size=200, class_weight=None, gamma='auto', kernel='linear') ]
		classifiers_seg = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy', max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=8, min_samples_split=4, min_weight_fraction_leaf=0.0, n_estimators=60, n_jobs=-1,            oob_score=False, random_state=None, verbose=0, warm_start=False), KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', metric_params=None, n_jobs=1, n_neighbors=16, p=3,          weights='uniform'), SVC(C=1, cache_size=200, class_weight=None, coef0=0.0, decision_function_shape=None, degree=3, gamma=0.25, kernel='rbf',   max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False), GaussianNB(), SVC(C=0.001, cache_size=200, class_weight=None, gamma='auto', kernel='linear') ]

	elif group == 'adulto':
		classifiers_agrad = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy',  max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=2, min_samples_split=16, min_weight_fraction_leaf=0.0, n_estimators=20, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False), KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', metric_params=None, n_jobs=1, n_neighbors=32, p=2, weights='uniform'), SVC(C=1, cache_size=200, class_weight=None, coef0=0.0, decision_function_shape=None, degree=3, gamma=0.25, kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False), GaussianNB(), SVC(C=0.001, cache_size=200, class_weight=None, gamma='auto', kernel='linear') ]
		classifiers_seg = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy', max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=32, min_samples_split=16, min_weight_fraction_leaf=0.0, n_estimators=40, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False), KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', metric_params=None, n_jobs=1, n_neighbors=32, p=2, weights='uniform'), SVC(C=1, cache_size=200, class_weight=None, coef0=0.0, decision_function_shape=None, degree=3, gamma=0.25, kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False), GaussianNB(), SVC(C=0.001, cache_size=200, class_weight=None, gamma='auto', kernel='linear') ]
	
	elif group == 'baixa':
		classifiers_agrad = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy', max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=8, min_samples_split=8, min_weight_fraction_leaf=0.0, n_estimators=60, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False), KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', metric_params=None, n_jobs=1, n_neighbors=16, p=2, weights='uniform'), SVC(C=1, cache_size=200, class_weight=None, coef0=0.0, decision_function_shape=None, degree=3, gamma=0.25, kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False), GaussianNB(), SVC(C=0.001, cache_size=200, class_weight=None, gamma='auto', kernel='linear') ]
		classifiers_seg = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy', max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=32, min_samples_split=4, min_weight_fraction_leaf=0.0, n_estimators=20, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False), KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', metric_params=None, n_jobs=1, n_neighbors=32, p=2, weights='uniform'), SVC(C=1, cache_size=200, class_weight=None, coef0=0.0, decision_function_shape=None, degree=3, gamma=0.25, kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False), GaussianNB(), SVC(C=0.001, cache_size=200, class_weight=None, gamma='auto', kernel='linear') ]

	elif group == 'media':
		classifiers_agrad = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy',  max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=8, min_samples_split=16, min_weight_fraction_leaf=0.0, n_estimators=20, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False), KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', metric_params=None, n_jobs=1, n_neighbors=8, p=2, weights='uniform'), SVC(C=1, cache_size=200, class_weight=None, coef0=0.0, decision_function_shape=None, degree=3, gamma=0.25, kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False), GaussianNB(), SVC(C=0.001, cache_size=200, class_weight=None, gamma='auto', kernel='linear') ]
		classifiers_seg = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy', max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=4, min_samples_split=8, min_weight_fraction_leaf=0.0, n_estimators=40, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False), KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', metric_params=None, n_jobs=1, n_neighbors=16, p=2, weights='uniform'), SVC(C=1, cache_size=200, class_weight=None, coef0=0.0, decision_function_shape=None, degree=3, gamma=0.25, kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False), GaussianNB(), SVC(C=0.001, cache_size=200, class_weight=None, gamma='auto', kernel='linear') ]

	elif group == 'solteiro':
		classifiers_agrad = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy', max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=2, min_samples_split=32, min_weight_fraction_leaf=0.0, n_estimators=60, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False), KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', metric_params=None, n_jobs=1, n_neighbors=8, p=3, weights='uniform'), SVC(C=1, cache_size=200, class_weight=None, coef0=0.0, decision_function_shape=None, degree=3, gamma=0.25, kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False), GaussianNB(), SVC(C=0.001, cache_size=200, class_weight=None, gamma='auto', kernel='linear') ]
		classifiers_seg = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy', max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=8, min_samples_split=4, min_weight_fraction_leaf=0.0, n_estimators=40, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False), KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', metric_params=None, n_jobs=1, n_neighbors=32, p=3, weights='uniform'), SVC(C=1, cache_size=200, class_weight=None, coef0=0.0, decision_function_shape=None, degree=3, gamma=0.25, kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False), GaussianNB(), SVC(C=0.001, cache_size=200, class_weight=None, gamma='auto', kernel='linear') ]
	
	elif group == 'casado':
		classifiers_agrad = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy', max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=4, min_samples_split=2, min_weight_fraction_leaf=0.0, n_estimators=20, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False), KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', metric_params=None, n_jobs=1, n_neighbors=32, p=2, weights='uniform'), SVC(C=1, cache_size=200, class_weight=None, coef0=0.0, decision_function_shape=None, degree=3, gamma=0.25, kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False), GaussianNB(), SVC(C=0.001, cache_size=200, class_weight=None, gamma='auto', kernel='linear') ]
		classifiers_seg = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy', max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=8, min_samples_split=2, min_weight_fraction_leaf=0.0, n_estimators=40, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False), KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski',  metric_params=None, n_jobs=1, n_neighbors=16, p=3, weights='uniform'), SVC(C=1, cache_size=200, class_weight=None, coef0=0.0, decision_function_shape=None, degree=3, gamma=0.25, kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False), GaussianNB(), SVC(C=0.001, cache_size=200, class_weight=None, gamma='auto', kernel='linear') ]

	elif group == "modal-80":#All users (more common param for each group)
		classifiers_agrad = [ ExtraTreesClassifier(class_weight=None, criterion='entropy', min_samples_leaf=8, min_samples_split=16, n_estimators=20, n_jobs=-1, oob_score=False) ]

		classifiers_seg = [ ExtraTreesClassifier(class_weight=None, criterion='entropy', min_samples_leaf=8, min_samples_split=4, n_estimators=40, n_jobs=-1, oob_score=False) ]

	elif group == "all":#80-20 best configuration for classifiers with all features in!
		classifiers_agrad = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy',           max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=8, min_samples_split=32,           min_weight_fraction_leaf=0.0, n_estimators=60, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False) ]

		classifiers_seg = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy',           max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=16, min_samples_split=2,            min_weight_fraction_leaf=0.0, n_estimators=60, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False) ]

	else:
		classifiers_agrad = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy',           max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=16, min_samples_split=32,           min_weight_fraction_leaf=0.0, n_estimators=60, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False) ]

		classifiers_seg = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy',           max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=8, min_samples_split=8,           min_weight_fraction_leaf=0.0, n_estimators=60, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False) ]

	return [classifiers_agrad, classifiers_seg]

def load_classifiers_lnl(group):
	#Building classifiers according to best configuration per group (FALTA LINEAR!)
	if group == 'masculino':
		classifiers_agrad = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy',
max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=8, min_samples_split=4,          min_weight_fraction_leaf=0.0, n_estimators=60, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False), KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', metric_params=None, n_jobs=1, n_neighbors=32, p=2,
weights='uniform'), SVC(C=1, cache_size=200, class_weight='balanced', coef0=0.0, decision_function_shape=None, degree=3, gamma=0.25, kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False), GaussianNB(), SVC(C=0.001, cache_size=200, class_weight=None, gamma='auto', kernel='linear') ]
		classifiers_seg = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy',
max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=32, min_samples_split=2, min_weight_fraction_leaf=0.0, n_estimators=40, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False), KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', metric_params=None, n_jobs=1, n_neighbors=32, p=3, weights='uniform'), SVC(C=1, cache_size=200, class_weight=None, coef0=0.0, decision_function_shape=None, degree=3, gamma=0.25, kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False), GaussianNB(), SVC(C=0.001, cache_size=200, class_weight=None, gamma='auto', kernel='linear') ]

	elif group == 'feminino':
		classifiers_agrad = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy',         max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=2, min_samples_split=2, min_weight_fraction_leaf=0.0, n_estimators=20, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False), KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', metric_params=None, n_jobs=1, n_neighbors=8, p=2, weights='uniform'), SVC(C=1, cache_size=200, class_weight=None, coef0=0.0, decision_function_shape=None, degree=3, gamma=0.25, kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False), GaussianNB(), SVC(C=0.001, cache_size=200, class_weight=None, gamma='auto', kernel='linear') ]
		classifiers_seg = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy',           max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=4, min_samples_split=2, min_weight_fraction_leaf=0.0, n_estimators=40, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False), KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', metric_params=None, n_jobs=1, n_neighbors=32, p=2, weights='uniform'), SVC(C=1, cache_size=200, class_weight='balanced', coef0=0.0, decision_function_shape=None, degree=3, gamma=0.25, kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False), GaussianNB(), SVC(C=0.001, cache_size=200, class_weight=None, gamma='auto', kernel='linear') ]

	elif group == 'jovem':
		classifiers_agrad = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy',           max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=2, min_samples_split=16, min_weight_fraction_leaf=0.0, n_estimators=40, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False), KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', metric_params=None, n_jobs=1, n_neighbors=16, p=3, weights='uniform'), SVC(C=1, cache_size=200, class_weight='balanced', coef0=0.0, decision_function_shape=None, degree=3, gamma=0.25, kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False), GaussianNB(), SVC(C=0.001, cache_size=200, class_weight=None, gamma='auto', kernel='linear') ]
		classifiers_seg = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy',           max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=4, min_samples_split=32, min_weight_fraction_leaf=0.0, n_estimators=60, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False), KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', metric_params=None, n_jobs=1, n_neighbors=32, p=3, weights='uniform'), SVC(C=0.001, cache_size=200, class_weight=None, coef0=0.0, decision_function_shape=None, degree=3, gamma=0.25, kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False), GaussianNB(), SVC(C=0.001, cache_size=200, class_weight=None, gamma='auto', kernel='linear') ]

	elif group == 'adulto':
		classifiers_agrad = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy',           max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=2, min_samples_split=8, min_weight_fraction_leaf=0.0, n_estimators=20, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False), KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', metric_params=None, n_jobs=1, n_neighbors=16, p=2, weights='uniform'), SVC(C=1, cache_size=200, class_weight='balanced', coef0=0.0, decision_function_shape=None, degree=3, gamma=0.25, kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False), GaussianNB(), SVC(C=0.001, cache_size=200, class_weight=None, gamma='auto', kernel='linear') ]
		classifiers_seg = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy',           max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=8, min_samples_split=32, min_weight_fraction_leaf=0.0, n_estimators=20, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False), KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', metric_params=None, n_jobs=1, n_neighbors=32, p=2, weights='uniform'), SVC(C=0.001, cache_size=200, class_weight=None, coef0=0.0, decision_function_shape=None, degree=3, gamma=0.25, kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False), GaussianNB(), SVC(C=0.001, cache_size=200, class_weight=None, gamma='auto', kernel='linear') ]
	
	elif group == 'baixa':
		classifiers_agrad = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy',           max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=8, min_samples_split=16, min_weight_fraction_leaf=0.0, n_estimators=60, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False), KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', metric_params=None, n_jobs=1, n_neighbors=16, p=2, weights='uniform'), SVC(C=1, cache_size=200, class_weight=None, coef0=0.0, decision_function_shape=None, degree=3, gamma=0.25, kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False), GaussianNB(), SVC(C=0.001, cache_size=200, class_weight=None, gamma='auto', kernel='linear') ]
		classifiers_seg = [ ExtraTreesClassifier(class_weight=None, criterion='entropy', min_samples_leaf=8, min_samples_split=2, n_estimators=40, n_jobs=-1, oob_score=False), KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', metric_params=None, n_jobs=1, n_neighbors=32, p=2, weights='uniform'), SVC(C=1, cache_size=200, class_weight=None, coef0=0.0, decision_function_shape=None, degree=3, gamma=0.25, kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False), GaussianNB(), SVC(C=0.001, cache_size=200, class_weight=None, gamma='auto', kernel='linear') ]

	elif group == 'media':
		classifiers_agrad = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy',           max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=4, min_samples_split=16, min_weight_fraction_leaf=0.0, n_estimators=40, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False), KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', metric_params=None, n_jobs=1, n_neighbors=32, p=2, weights='uniform'), SVC(C=1, cache_size=200, class_weight=None, coef0=0.0, decision_function_shape=None, degree=3, gamma=0.25, kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False), GaussianNB(), SVC(C=0.001, cache_size=200, class_weight=None, gamma='auto', kernel='linear') ]
		classifiers_seg = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy',            max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=8, min_samples_split=2, min_weight_fraction_leaf=0.0, n_estimators=20, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False), KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', metric_params=None, n_jobs=1, n_neighbors=32, p=2, weights='uniform'), SVC(C=1, cache_size=200, class_weight=None, coef0=0.0, decision_function_shape=None, degree=3, gamma=0.25, kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False), GaussianNB(), SVC(C=0.001, cache_size=200, class_weight=None, gamma='auto', kernel='linear') ]

	elif group == 'solteiro':
		classifiers_agrad = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy',           max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=4, min_samples_split=32, min_weight_fraction_leaf=0.0, n_estimators=40, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False), KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', metric_params=None, n_jobs=1, n_neighbors=8, p=2, weights='uniform'), SVC(C=1, cache_size=200, class_weight='balanced', coef0=0.0, decision_function_shape=None, degree=3, gamma=0.25, kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False), GaussianNB(), SVC(C=0.001, cache_size=200, class_weight=None, gamma='auto', kernel='linear') ]
		classifiers_seg = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy',           max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=16, min_samples_split=4, min_weight_fraction_leaf=0.0, n_estimators=40, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False), KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', metric_params=None, n_jobs=1, n_neighbors=16, p=2, weights='uniform'), SVC(C=1, cache_size=200, class_weight='balanced', coef0=0.0, decision_function_shape=None, degree=3, gamma=0.25, kernel='rbf',
  max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False), GaussianNB(), SVC(C=0.001, cache_size=200, class_weight=None, gamma='auto', kernel='linear') ]
	
	elif group == 'casado':
		classifiers_agrad = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy',           max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=8, min_samples_split=16, min_weight_fraction_leaf=0.0, n_estimators=60, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False), KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', metric_params=None, n_jobs=1, n_neighbors=32, p=2, weights='uniform'), SVC(C=1, cache_size=200, class_weight='balanced', coef0=0.0, decision_function_shape=None, degree=3, gamma=0.25, kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False), GaussianNB(), SVC(C=0.001, cache_size=200, class_weight=None, gamma='auto', kernel='linear') ]
		classifiers_seg = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy',           max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=4, min_samples_split=8, min_weight_fraction_leaf=0.0, n_estimators=40, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False), KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', metric_params=None, n_jobs=1, n_neighbors=32, p=2, weights='uniform'), SVC(C=1, cache_size=200, class_weight='balanced', coef0=0.0, decision_function_shape=None, degree=3, gamma=0.25, kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False), GaussianNB(), SVC(C=0.001, cache_size=200, class_weight=None, gamma='auto', kernel='linear') ]

	return [classifiers_agrad, classifiers_seg]

def load_classifiers_rnr(group):
	#Building classifiers according to best configuration per group (FALTA LINEAR!)

	if group == 'masculino':
		classifiers_agrad = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy', max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=8, min_samples_split=2, min_weight_fraction_leaf=0.0, n_estimators=20, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False), KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', metric_params=None, n_jobs=1, n_neighbors=32, p=2,           weights='uniform'), SVC(C=1, cache_size=200, class_weight='balanced', coef0=0.0, decision_function_shape=None, degree=3, gamma=0.25, kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False), GaussianNB(), SVC(C=0.001, cache_size=200, class_weight=None, gamma='auto', kernel='linear') ]
		classifiers_seg = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy',           max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=8, min_samples_split=8, min_weight_fraction_leaf=0.0, n_estimators=60, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False), KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', metric_params=None, n_jobs=1, n_neighbors=32, p=2, weights='uniform'), SVC(C=1, cache_size=200, class_weight=None, coef0=0.0, decision_function_shape=None, degree=3, gamma=0.25, kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False), GaussianNB(), SVC(C=0.001, cache_size=200, class_weight=None, gamma='auto', kernel='linear') ]

	elif group == 'feminino':
		classifiers_agrad = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy', max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=2, min_samples_split=16, min_weight_fraction_leaf=0.0, n_estimators=20, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False), KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', metric_params=None, n_jobs=1, n_neighbors=32, p=2, weights='uniform'), SVC(C=1, cache_size=200, class_weight='balanced', coef0=0.0, decision_function_shape=None, degree=3, gamma=0.25, kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False), GaussianNB(), SVC(C=0.001, cache_size=200, class_weight=None, gamma='auto', kernel='linear') ]
		classifiers_seg = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy', max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=4, min_samples_split=4, min_weight_fraction_leaf=0.0, n_estimators=60, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False), KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', metric_params=None, n_jobs=1, n_neighbors=32, p=2, weights='uniform'), SVC(C=1, cache_size=200, class_weight='balanced', coef0=0.0, decision_function_shape=None, degree=3, gamma=0.25, kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False), GaussianNB(), SVC(C=0.001, cache_size=200, class_weight=None, gamma='auto', kernel='linear') ]

	elif group == 'jovem':
		classifiers_agrad = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy', max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=4, min_samples_split=4, min_weight_fraction_leaf=0.0, n_estimators=60, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False), KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', metric_params=None, n_jobs=1, n_neighbors=4, p=2, weights='uniform'), SVC(C=1, cache_size=200, class_weight=None, coef0=0.0, decision_function_shape=None, degree=3, gamma=0.25, kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False), GaussianNB(), SVC(C=0.001, cache_size=200, class_weight=None, gamma='auto', kernel='linear') ]
		classifiers_seg = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy', max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=4, min_samples_split=8, min_weight_fraction_leaf=0.0, n_estimators=20, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False), KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', metric_params=None, n_jobs=1, n_neighbors=8, p=2, weights='uniform'), SVC(C=1, cache_size=200, class_weight=None, coef0=0.0, decision_function_shape=None, degree=3, gamma=0.25, kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False), GaussianNB(), SVC(C=0.001, cache_size=200, class_weight=None, gamma='auto', kernel='linear') ]

	elif group == 'adulto':
		classifiers_agrad = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy', max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=8, min_samples_split=8, min_weight_fraction_leaf=0.0, n_estimators=40, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False), KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', metric_params=None, n_jobs=1, n_neighbors=16, p=3, weights='uniform'), SVC(C=1, cache_size=200, class_weight=None, coef0=0.0, decision_function_shape=None, degree=3, gamma=0.25, kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False), GaussianNB(), SVC(C=0.001, cache_size=200, class_weight=None, gamma='auto', kernel='linear') ]
		classifiers_seg = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy', max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=8, min_samples_split=2, min_weight_fraction_leaf=0.0, n_estimators=20, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False), KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', metric_params=None, n_jobs=1, n_neighbors=32, p=2, weights='uniform'), SVC(C=1, cache_size=200, class_weight='balanced', coef0=0.0, decision_function_shape=None, degree=3, gamma=0.25, kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False), GaussianNB(), SVC(C=0.001, cache_size=200, class_weight=None, gamma='auto', kernel='linear') ]
	
	elif group == 'baixa':
		classifiers_agrad = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy', max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=4, min_samples_split=32, min_weight_fraction_leaf=0.0, n_estimators=40, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False), KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', metric_params=None, n_jobs=1, n_neighbors=32, p=2, weights='uniform'), SVC(C=1, cache_size=200, class_weight=None, coef0=0.0, decision_function_shape=None, degree=3, gamma=0.25, kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False), GaussianNB(), SVC(C=0.001, cache_size=200, class_weight=None, gamma='auto', kernel='linear') ]
		classifiers_seg = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy', max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=4, min_samples_split=4, min_weight_fraction_leaf=0.0, n_estimators=40, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False), KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', metric_params=None, n_jobs=1, n_neighbors=32, p=2, weights='uniform'), SVC(C=1, cache_size=200, class_weight='balanced', coef0=0.0, decision_function_shape=None, degree=3, gamma=0.25, kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False), GaussianNB(), SVC(C=0.001, cache_size=200, class_weight=None, gamma='auto', kernel='linear') ]

	elif group == 'media':
		classifiers_agrad = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy', max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=16, min_samples_split=4, min_weight_fraction_leaf=0.0, n_estimators=60, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False), KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', metric_params=None, n_jobs=1, n_neighbors=8, p=2, weights='uniform'), SVC(C=1, cache_size=200, class_weight='balanced', coef0=0.0, decision_function_shape=None, degree=3, gamma=0.25, kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False), GaussianNB(), SVC(C=0.001, cache_size=200, class_weight=None, gamma='auto', kernel='linear') ]
		classifiers_seg = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy', max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=8, min_samples_split=8, min_weight_fraction_leaf=0.0, n_estimators=60, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False), KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', metric_params=None, n_jobs=1, n_neighbors=16, p=2, weights='uniform'), SVC(C=1, cache_size=200, class_weight='balanced', coef0=0.0, decision_function_shape=None, degree=3, gamma=0.25, kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False), GaussianNB(), SVC(C=0.001, cache_size=200, class_weight=None, gamma='auto', kernel='linear') ]

	elif group == 'solteiro':
		classifiers_agrad = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy', max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=4, min_samples_split=16, min_weight_fraction_leaf=0.0, n_estimators=40, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False), KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', metric_params=None, n_jobs=1, n_neighbors=32, p=2, weights='uniform'), SVC(C=1, cache_size=200, class_weight='balanced', coef0=0.0, decision_function_shape=None, degree=3, gamma=0.25, kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False), GaussianNB(), SVC(C=0.001, cache_size=200, class_weight=None, gamma='auto', kernel='linear') ]
		classifiers_seg = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy', max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=8, min_samples_split=2, min_weight_fraction_leaf=0.0, n_estimators=20, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False), KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', metric_params=None, n_jobs=1, n_neighbors=16, p=2, weights='uniform'), SVC(C=1, cache_size=200, class_weight='balanced', coef0=0.0, decision_function_shape=None, degree=3, gamma=0.25, kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False), GaussianNB(), SVC(C=0.001, cache_size=200, class_weight=None, gamma='auto', kernel='linear') ]
	
	elif group == 'casado':
		classifiers_agrad = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy', max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=2, min_samples_split=4, min_weight_fraction_leaf=0.0, n_estimators=40, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False), KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', metric_params=None, n_jobs=1, n_neighbors=8, p=2, weights='uniform'), SVC(C=1, cache_size=200, class_weight='balanced', coef0=0.0, decision_function_shape=None, degree=3, gamma=0.25, kernel='rbf', max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False), GaussianNB(), SVC(C=0.001, cache_size=200, class_weight=None, gamma='auto', kernel='linear') ]
		classifiers_seg = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy', max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=2, min_samples_split=16, min_weight_fraction_leaf=0.0, n_estimators=60, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False), KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', metric_params=None, n_jobs=1, n_neighbors=8, p=2, weights='uniform'), SVC(C=1, cache_size=200, class_weight='balanced', coef0=0.0, decision_function_shape=None, degree=3, gamma=0.25, kernel='rbf',
  max_iter=-1, probability=False, random_state=None, shrinking=True, tol=0.001, verbose=False), GaussianNB(), SVC(C=0.001, cache_size=200, class_weight=None, gamma='auto', kernel='linear') ]

	return [classifiers_agrad, classifiers_seg]

def convertColumnsToDummy(df):
	""" Converts categorical features to dummy variables in the data frame """

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

def train_classifiers(question, predictors, answer, parameters_dic, classifiers_names, classifiers, group=""):
	""" Performs trainings with classifiers in order to discover the best configuration of each classifier """

	global classifiers_to_scale
	#Question being evaluated
	print ">>>>>> G " + group + " Q " + question

	i = 0
	predictors = np.array(predictors)
	answer = np.array(answer)

	selected_classifiers = []
	
	for classifier_index in range(0, len(classifiers)):

		print "### Classifier " + str(classifiers_names[classifier_index])
		if parameters_dic.has_key(classifiers_names[classifier_index]):
			parameters_to_optimize = parameters_dic[classifiers_names[classifier_index]]
			print "### Param to opt " + str(parameters_to_optimize)

			best = None
			best_f1 = 0

			for train, test in StratifiedKFold(answer, n_folds=5): #5folds

				scaling = StandardScaler()

				predictors_train = predictors[train]
				answer_train = answer[train]
				predictors_test = predictors[test]
				answer_test = answer[test]

				if classifiers_names[classifier_index] in classifiers_to_scale:#Some classifiers needs to scale input!
					scaling.fit(predictors_train)
					X_train_scaled = scaling.transform(predictors_train)
					X_test_scaled = scaling.transform(predictors_test)
				else:
					X_train_scaled = predictors_train
					X_test_scaled = predictors_test


				#if classifiers_names[classifier_index] in classifiers_to_scale:#Some classifiers needs to scale input!
	#				predictors = StandardScaler().fit_transform(predictors)
				
				classifier = GridSearchCV(classifiers[classifier_index], 
				      param_grid=parameters_to_optimize, cv=3)
				clf = classifier.fit(X_train_scaled, answer_train)

				i += 1
				print('Fold', i)
				print(clf.best_estimator_)
				print()
		
				y_pred = clf.predict(X_test_scaled)

				#Vamo ver o F1. To usando micro, pode ser o macro. No paper, tem que mostrar os 2 mesmo.
				f1_micro = f1_score(answer_test, y_pred, average='micro')
				f1_macro = f1_score(answer_test, y_pred, average='macro')
				print('F1 score no teste, nunca use isto para escolher parametros. ' + \
				  'Aceite o valor, tuning de parametros so antes com o grid search', f1_micro
				  , f1_macro)
				print()
				print()

				#Storing the best configuration
				if f1_micro > best_f1:
					best_f1 = f1_micro
					best = clf.best_estimator_

		selected_classifiers.append(best)

	print str(selected_classifiers)

def train_classifiers_leave_user_out(question, list_of_predictors, df, parameters_dic, classifiers_names, classifiers, group=""):
	""" Performs trainings with classifiers removing one user at a time and then calculates accuracy, micro and macro values """

	global classifiers_to_scale
	user_ids = df['userID'].unique()

	#Question being evaluated
	print ">>>>>> G " + group + " Q " + question

	history_micro = []
	history_macro = []
	history_acc = []
	history_features_importances = []
	importances_dic = {}

	for user_id in user_ids:#Remove each user sequentially
	
		current_df_train = df[(df.userID != user_id)]
		current_df_test = df[(df.userID == user_id)]

		predictors = np.array(current_df_train[list_of_predictors].values)
		answer = np.array(current_df_train['choice'])
		i = 0
	
		for classifier_index in range(0, len(classifiers)):

			print "### User " + str(user_id) + " Classifier " + str(classifiers_names[classifier_index])

			if parameters_dic.has_key(classifiers_names[classifier_index]):
				parameters_to_optimize = parameters_dic[classifiers_names[classifier_index]]

				best_clf = None
				best_f1 = []

				for train, test in StratifiedKFold(answer, n_folds=5): #5folds

					predictors_train = predictors[train]
					answer_train = answer[train]
					predictors_test = predictors[test]
					answer_test = answer[test]

					X_train_scaled = predictors_train #Only extra trees is currently being used!
					X_test_scaled = predictors_test

					classifier = GridSearchCV(classifiers[classifier_index], 
					      param_grid=parameters_to_optimize, cv=3)
					clf = classifier.fit(X_train_scaled, answer_train)

					i += 1
					#print('Fold', i)
					#print(clf.best_estimator_)
					#print()
		
					y_pred = clf.predict(X_test_scaled)

					#Check f1
					f1_micro = f1_score(answer_test, y_pred, average='micro')
					f1_macro = f1_score(answer_test, y_pred, average='macro')
					#print('F1 score no teste, nunca use isto para escolher parametros. ' + \
					#  'Aceite o valor, tuning de parametros so antes com o grid search', f1_micro
					#  , f1_macro)
					#print()
					#print()

					#Storing the best configuration
					if len(best_f1) == 0 or f1_micro > best_f1[0]:
						best_f1 = [f1_micro, f1_macro]
						best_clf = clf.best_estimator_
		
				#Test best classifier removing current user!
				X_train = np.array(current_df_train[list_of_predictors].values)
				y_train = np.array(current_df_train['choice'])
				X_test = np.array(current_df_test[list_of_predictors].values)
				y_test = np.array(current_df_test['choice'])							

				#Only extra trees is currently being used
				X_train_scaled = X_train
				X_test_scaled = X_test

				best_clf.fit(X_train_scaled, y_train)#Fitting for test

				accuracy = best_clf.score(X_test_scaled, y_test)#Accuracy
				y_pred = best_clf.predict(X_test_scaled)#Estimated values

				metrics_macro = precision_recall_fscore_support(y_test, y_pred, average='macro')#Calculates for each label and compute the mean!
				metrics_micro = precision_recall_fscore_support(y_test, y_pred, average='micro')#Total false positives, negatives and true positives -> more similar to accuracy
				history_micro.append(metrics_micro[0:3])
				history_macro.append(metrics_macro[0:3])
				history_acc.append(accuracy)

				history_features_importances.append(best_clf.feature_importances_)

				print "CONF " + str(best_clf.n_estimators) + "\t" + str(best_clf.max_features) + "\t" + str(best_clf.max_depth)+ "\t" + str(best_clf.min_samples_split)+ "\t" + str(best_clf.min_samples_leaf)
				
				#print ">>> Pos"
				#print str(history_acc)
				#print str(history_micro)
				#print str(history_macro)

	#print ">>> Final"
	#print str(history_acc)
	#print str(history_micro)
	#print str(history_macro)
	std_acc = np.std(np.array(history_acc), axis=0)
	mean_acc = np.mean(np.array(history_acc), axis=0)
	std_micro = np.std(np.array(history_micro), axis=0)
	mean_micro = np.mean(np.array(history_micro), axis=0)
	std_macro = np.std(np.array(history_macro), axis=0)
	mean_macro = np.mean(np.array(history_macro), axis=0)
	print ">>>>\tmean_acc\tstd_acc\tmeans_micro\tstds_micro\tmeans_macro\tstd_macro"
	print ">>>>\t" + str(mean_acc) + "\t" + str(std_acc) + "\t" + str(mean_micro) + "\t" + str(std_micro) + "\t" + str(mean_macro) + "\t" + str(std_macro)  

	#Features importances!
	std_importances = np.std(np.array(history_features_importances), axis=0)
	mean_importances = np.mean(np.array(history_features_importances), axis=0)
	for index in range(0, len(list_of_predictors)):
		importances_dic[list_of_predictors[index]] = [mean_importances[index], std_importances[index]]
	
	sorted_dic = sorted(importances_dic.items(), key=operator.itemgetter(1), reverse=True)
	print ">>>> Importances "
	print '\n'.join([str(tuple[0]) +  " " + str(tuple[1]) for tuple in sorted_dic])
				

def train_classifiers_leave_user_out2(question, list_of_predictors, df, group="", load_3classes=False):
	""" Consider modal train configuration and then calculates accuracy, micro and macro values leaving one user out per execution """

	global classifiers_to_scale
	user_ids = df['userID'].unique()

	#Question being evaluated
	print ">>>>>> G " + group + " Q " + question

	history_micro = []
	history_macro = []
	history_acc = []
	history_features_importances = []
	importances_dic = {}

	if load_3classes:
		classifiers = load_classifiers_3classes("")#Loading mean classifiers: modal
	else:
		classifiers = load_classifiers_wodraw("")

	if question == "Pleasantness":
		best_clf = classifiers[0][0]
	else:
		best_clf = classifiers[1][0]

	for user_id in user_ids:#Remove each user sequentially!
	
		current_df_train = df[(df.userID != user_id)]
		current_df_test = df[(df.userID == user_id)]

		predictors = np.array(current_df_train[list_of_predictors].values)
		answer = np.array(current_df_train['choice'])
		i = 0
	
		print "### User " + str(user_id) + " Classifier Extra" 

		#Test best classifier removing current user!
		X_train = np.array(current_df_train[list_of_predictors].values)
		y_train = np.array(current_df_train['choice'])
		X_test = np.array(current_df_test[list_of_predictors].values)
		y_test = np.array(current_df_test['choice'])							

		#Only extra trees is currently being used
		X_train_scaled = X_train
		X_test_scaled = X_test

		best_clf.fit(X_train_scaled, y_train)#Fitting for test

		accuracy = best_clf.score(X_test_scaled, y_test)#Accuracy
		y_pred = best_clf.predict(X_test_scaled)#Estimated values

		metrics_macro = precision_recall_fscore_support(y_test, y_pred, average='macro')#Calculates for each label and compute the mean!
		metrics_micro = precision_recall_fscore_support(y_test, y_pred, average='micro')#Total false positives, negatives and true positives -> more similar to accuracy
		history_micro.append(metrics_micro[0:3])
		history_macro.append(metrics_macro[0:3])
		history_acc.append(accuracy)

		history_features_importances.append(best_clf.feature_importances_)
		
	std_acc = np.std(np.array(history_acc), axis=0)
	mean_acc = np.mean(np.array(history_acc), axis=0)
	std_micro = np.std(np.array(history_micro), axis=0)
	mean_micro = np.mean(np.array(history_micro), axis=0)
	std_macro = np.std(np.array(history_macro), axis=0)
	mean_macro = np.mean(np.array(history_macro), axis=0)
	print ">>>>\tmean_acc\tstd_acc\tmeans_micro\tstds_micro\tmeans_macro\tstd_macro"
	print ">>>>\t" + str(mean_acc) + "\t" + str(std_acc) + "\t" + str(mean_micro) + "\t" + str(std_micro) + "\t" + str(mean_macro) + "\t" + str(std_macro)  

	#Features importances!
	std_importances = np.std(np.array(history_features_importances), axis=0)
	mean_importances = np.mean(np.array(history_features_importances), axis=0)
	for index in range(0, len(list_of_predictors)):
		importances_dic[list_of_predictors[index]] = [mean_importances[index], std_importances[index]]
	
	sorted_dic = sorted(importances_dic.items(), key=operator.itemgetter(1), reverse=True)
	print ">>>> Importances "
	print '\n'.join([str(tuple[0]) +  " " + str(tuple[1]) for tuple in sorted_dic])


def stripDataFrame(df):
	""" Removes unused chars from dataframes columns values """

	df['gender'] = [x.lstrip(' \t\n\r').rstrip(' \t\n\r') for x in df['gender']]
	df['marital'] = [x.lstrip(' \t\n\r').rstrip(' \t\n\r') for x in df['marital']]
	df['income'] = [x.lstrip(' \t\n\r').rstrip(' \t\n\r') for x in df['income']]
	df['graffiti1'] = [x.lstrip(' \t\n\r').rstrip(' \t\n\r') for x in df['graffiti1']]
	df['graffiti2'] = [x.lstrip(' \t\n\r').rstrip(' \t\n\r') for x in df['graffiti2']]
	df['bairro1'] = [x.lstrip(' \t\n\r').rstrip(' \t\n\r') for x in df['bairro1']]
	df['bairro2'] = [x.lstrip(' \t\n\r').rstrip(' \t\n\r') for x in df['bairro2']]

	return df

def plot_importances_from_file(importances_file, df, load_3classes):
	""" Plot features importances already existent in an output file """
	data = open(importances_file, "r").readlines()
	header_index = 0

	if load_3classes:
		answer_type = "3classes"
	else:
		answer_type = "wodraw"

	while header_index <= len(data):
		header = data[header_index].split(" ")
		group = header[2]
		question = header[4]

		#Compute group size!
		df_to_use = df[(df.gender == group)]
		group_size = len(df_to_use)
		
		importances_data = data[header_index+2:header_index+32]
		importances = []
		std = []
		features = []
		for line in importances_data:
			new_line = line.replace("[", "").replace("]", "").replace(",", "")
			line_data = new_line.split(" ")
			features.append(line_data[0])
			importances.append( float(line_data[1].strip(' \t\n\r')) )
			std.append( float(line_data[2].strip(' \t\n\r')) )
		
		indices = np.argsort(importances)[::-1]#Sorting from greater to lower importances

		#Compute confidence interval values to plot!
		print str(importances)
		print str(std)
		print str(group_size)
		if group_size >= 30:
			ci = stats.norm.interval(0.95, loc=importances, scale= std / np.sqrt(group_size) )
		else:
			ci = stats.t.interval(0.95, df=group_size-1, loc=importances, scale= std / np.sqrt(group_size) )
		#Calculating distances from mean!
		low_limit = ci[0]
		top_limit = ci[1]
		var = np.array([(top_limit[index]-low_limit[index])/2 for index in range(0, len(low_limit))])

		np_importances = np.array(importances)
		np_var = np.array(var)
		np_features = np.array(features)

		#Figure!
		print "IND " + str(indices)
		plt.figure()
		plt.title("Feature importances")
		plt.bar(indices, np_importances[indices],
			color="r", yerr=np_var[indices], align="center")
		plt.xticks(range(len(importances)), np_features[indices])
		plt.xticks(rotation=70)
		plt.xlim([-1, len(importances)])
	
		plt.savefig('importances_'+group+"_"+question+"_"+answer_type+'.png') 
		#plt.show()
		plt.close()

		#Updating index
		header_index = header_index + 32

def plot_importances(clf, pair, group):
	""" Plot features importances from a classifier """

	importances = clf.feature_importances_
	std = np.std([tree.feature_importances_ for tree in clf.estimators_],
		     axis=0)
	indices = np.argsort(importances)[::-1]

	#Compute confidence interval values to plot!
	if len(clf.estimators_) >= 30:
		ci = stats.norm.interval(0.95, loc=importances, scale= std / np.sqrt(len(clf.estimators_)) )
	else:
		ci = stats.t.interval(0.95, df=len(clf.estimators_)-1, loc=importances, scale= std / np.sqrt(len(clf.estimators_)) )
	#Calculating distances from mean!
	low_limit = ci[0]
	top_limit = ci[1]
	var = np.array([(top_limit[index]-low_limit[index])/2 for index in range(0, len(low_limit))])

	plt.figure()
	#fig, ax = plt.subplots()
	plt.title("Feature importances")
	plt.bar(range(pair[1].shape[1]), importances[indices],
		color="r", yerr=var[indices], align="center")
	#       color="r", yerr=std[indices], align="center")
	plt.xticks(range(pair[1].shape[1]), indices)
	plt.xlim([-1, pair[1].shape[1]])
	
	plt.savefig('importances_'+group+"_"+pair[0]+'.png') 
	plt.show()
	plt.close()

def test_features_importances(classifiers_names, predictors_agrad, answer_agrad, predictors_seg, answer_seg, list_of_predictors_agrad, list_of_predictors_seg, group="", load_3classes=False):
	""" Checks the importances of features considering the best configuration of classifiers previously tested """

	if load_3classes:
		#classifiers = load_classifiers_3classes(group)
		classifiers = load_classifiers_wodraw("modal-leave")
	else:
		#classifiers = load_classifiers_wodraw(group)
		classifiers = load_classifiers_wodraw("modal-leave")

	classifiers_agrad = [classifiers[0][0]]
	classifiers_seg = [classifiers[1][0]]

	for pair in [ ["Pleasantness", predictors_agrad, answer_agrad, classifiers_agrad, list_of_predictors_agrad], ["Safety", predictors_seg, answer_seg, classifiers_seg, list_of_predictors_seg] ]:
		list_of_predictors = pair[4]

		for classifier_index in range(0, len(pair[3])):
			clf = pair[3][classifier_index]
			clf_name = classifiers_names[classifier_index]

			#Training with all data!
			clf.fit(pair[1], pair[2])

			try:
				importances_dic = {}
				importances = clf.feature_importances_
				std = np.std([tree.feature_importances_ for tree in clf.estimators_], axis=0)
				#Compute confidence interval values 
				if len(clf.estimators_) >= 30:
					ci = stats.norm.interval(0.95, loc=importances, scale= std / np.sqrt(len(clf.estimators_)) )
				else:
					ci = stats.t.interval(0.95, df=len(clf.estimators_)-1, loc=importances, scale= std / np.sqrt(len(clf.estimators_)) )
				#Calculating distances from mean!
				low_limit = ci[0]
				top_limit = ci[1]
				for index in range(0, len(list_of_predictors)):
					importances_dic[list_of_predictors[index]] = [importances[index], std[index], low_limit[index], top_limit[index]]
				
				sorted_dic = sorted(importances_dic.items(), key=operator.itemgetter(1), reverse=True)
				print ">>>> G " + group + " Q " + pair[0] + " C " + clf_name
				#print str(sorted_dic)
				print '\n'.join([str(tuple[0]) +  " " + str(tuple[1]) for tuple in sorted_dic])
				#print "FEATURES " + str(", ".join(list_of_predictors))
				#print(clf.feature_importances_)
		
				plot_importances(clf, pair, group)

				# RECURSIVE! Create the RFE object and compute a cross-validated score.
				#svc = SVC(kernel="linear")
				#if pair[0] == "Pleasantness":
				#	svc = load_classifiers_wodraw(group)[0][0]
				#else:
				#	svc = load_classifiers_wodraw(group)[1][0]
				# The "accuracy" scoring is proportional to the number of correct classifications
				#rfecv = RFECV(estimator=svc, step=1, cv=StratifiedKFold(pair[2], 5),
				#	      scoring='accuracy')
				#rfecv.fit(pair[1], pair[2])

				#print("Optimal number of features : %d" % rfecv.n_features_)
				#print "Ranking " + str(rfecv.ranking_)

				#importances_dic = {}
				#importances = rfecv.ranking_
				#for index in range(0, len(list_of_predictors)):
				#	importances_dic[list_of_predictors[index]] = importances[index]
				#
				#sorted_dic = sorted(importances_dic.items(), key=operator.itemgetter(1))
				#print ">>>> G " + group + " Q " + pair[0] + " C " + clf_name
				##print str(sorted_dic)
				#print '\n'.join([str(tuple[0]) +  " " + str(tuple[1]) for tuple in sorted_dic])
				# RECURSIVE!

				#SELECT FROM MODEL! Quais as features?
				#print ">>>> G " + group + " Q " + pair[0] + " C " + clf_name
				#model = SelectFromModel(clf, prefit=True)
				#X_new = model.transform(pair[1])
				#print model.inverse_transform(X_new)
				#print X_new
				#SELECT FROM MODEL!
  
			except Exception as inst:
				print "Exception! "
				print type(inst) 
				print inst.args 
			except:
    				print "Unexpected error:", sys.exc_info()[0]
			

def plot_confusion_matrix(cm, title='Confusion matrix', cmap=plt.cm.Blues):
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(3)
    plt.xticks(tick_marks, [-1, 0, 1], rotation=45)
    plt.yticks(tick_marks, [-1, 0, 1])
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')


def test_random(predictors_agrad, answer_agrad, predictors_seg, answer_seg, group):
	""" Tests performance of a random classifier! """

	unique_answer_agrad = Set(answer_agrad)
	unique_answer_seg = Set(answer_seg)

	X_train, X_test, y_train, y_test = train_test_split(predictors_agrad, answer_agrad, test_size=.2)#Splitting into train and test sets!
	correct_predictions = 0
	wrong_predictions = 0
	for value in y_test:
		if value == random.sample(unique_answer_agrad, 1):
			correct_predictions = correct_predictions + 1
		else:
			wrong_predictions = wrong_predictions + 1
	print ">>> Acc_pleasantness\t" + group + "\t" + str( 1.0*correct_predictions / (correct_predictions + wrong_predictions) ) + "\t" + str(correct_predictions) + "\t" + str(wrong_predictions)

	X_train, X_test, y_train, y_test = train_test_split(predictors_seg, answer_seg, test_size=.2)#Splitting into train and test sets!
	correct_predictions = 0
	wrong_predictions = 0
	for value in y_test:
		if value == random.sample(unique_answer_seg, 1):
			correct_predictions = correct_predictions + 1
		else:
			wrong_predictions = wrong_predictions + 1
	print ">>> Acc_safety" + group + "\t" + str( 1.0*correct_predictions / (correct_predictions + wrong_predictions) ) + "\t" + str(correct_predictions) + "\t" + str(wrong_predictions)
	

def test_classifiers(classifiers_names, predictors_agrad, answer_agrad, predictors_seg, answer_seg, group="", load_3classes=False):
	""" Trains and tests classifiers considering the best configuration of classifiers previously tested """

	global classifiers_to_scale

	if load_3classes:
		classifiers = load_classifiers_3classes(group)
	else:
		classifiers = load_classifiers_wodraw(group)

	classifiers_agrad = classifiers[0]
	classifiers_seg = classifiers[1]

	print "Question\tClassifier\ttrain sample size\ttest sample size\tmean accuracy\t(precision,\trecall,\tf1)"
	for entry in [ ["Pleasantness", predictors_agrad, answer_agrad, classifiers_agrad], ["Safety", predictors_seg, answer_seg, classifiers_seg] ]:
		for classifier_index in range(0, len(entry[3])):
			clf = entry[3][classifier_index]
			clf_name = classifiers_names[classifier_index]

			X_train, X_test, y_train, y_test = train_test_split(entry[1], entry[2], test_size=.2)#Splitting into train and test sets!
			scaling = StandardScaler()

			if classifiers_names[classifier_index] in classifiers_to_scale:#Some classifiers needs to scale input!
				scaling.fit(X_train)
				X_train_scaled = scaling.transform(X_train)
				X_test_scaled = scaling.transform(X_test)
				answer = entry[2]
			else:
				predictors = entry[1]
				answer = entry[2]
				X_train_scaled = X_train
				X_test_scaled = X_test

	
			clf.fit(X_train_scaled, y_train)

        		score = clf.score(X_test_scaled, y_test)#Accuracy
			y_pred = clf.predict(X_test_scaled)#Estimated values

			metrics = precision_recall_fscore_support(y_test, y_pred, average='macro', labels=['1', '0', '-1'])#Calculates for each label and compute the mean!
			print ">>>> G " + group + " Q " + entry[0] + " " + clf_name + " " + str(len(X_train)) + " " + str(len(X_test)) + " " + str(score) + " MACRO " + str(metrics)
			metrics = precision_recall_fscore_support(y_test, y_pred, average='micro', labels=['1', '0', '-1'])#Total false positives, negatives and true positives -> more similar to accuracy
			print ">>>> G " + group + " Q " + entry[0] + " " + clf_name + " " + str(len(X_train)) + " " + str(len(X_test)) + " " + str(score) + " MICRO " + str(metrics)
	
			print "COUNTER TEST " + str(collections.Counter(y_test))
			cm = confusion_matrix(y_test, y_pred)
			print "MATRIX " + str(cm)
			#plt.figure()
			#plot_confusion_matrix(cm)
			#plt.show()


if __name__ == "__main__":
	if len(sys.argv) < 3:
		print "Uso: <file with photos preferences, photos data and user data> <phase - train-config, train-user-out, importances, importances-file, test or random> <filter, e.g., <gender, marital, age, income>-masculino>"
		sys.exit(1)

	input_file = sys.argv[1]
	phase = sys.argv[2].lower()

	#Using 3 classes or two classes as output
	if "3classes" in input_file.lower():
		load_3classes = True
	else:
		load_3classes = False

	if phase.lower() == "importances-file":#Plot features importances already computed!
		if len(sys.argv) != 4:
			print "Uso importances-file: <file with photos preferences, photos data and user data> <phase: importances-file> <importances file>"
			sys.exit(1)
		df = pd.read_table(input_file, sep='\t', encoding='utf8', header=0)
		importances_file = sys.argv[3]
		plot_importances_from_file(importances_file, df, load_3classes)

	else:#Train, test classifiers!
		df = pd.read_table(input_file, sep='\t', encoding='utf8', header=0)

		#Remove unecessary chars!
		df = stripDataFrame(df)

		#list_of_predictors = ['street_wid1', 'mov_cars1', 'park_cars1', 'mov_ciclyst1', 'landscape1', 'build_ident1', 'trees1', 'build_height1', 'diff_build1', 'people1', 'graffiti1_No', 'graffiti1_Yes', 'bairro1_catole', 'bairro1_centro', 'bairro1_liberdade', 'street_wid2', 'mov_cars2', 'park_cars2', 'mov_ciclyst2', 'landscape2', 'build_ident2', 'trees2', 'build_height2', 'diff_build2', 'people2', 'graffiti2_No', 'graffiti2_Yes', 'bairro2_catole', 'bairro2_centro', 'bairro2_liberdade']

		#Socio group to filter data
		if len(sys.argv) == 4:
			filter_group = sys.argv[3]
			group = filter_group.split("-")[1]
		else:
			filter_group = ""
			group = ""

		if len(filter_group) > 0:
			if 'gender' in filter_group:
				df_to_use = df[(df.gender == group)]
			elif 'marital' in filter_group:
				df_to_use = df[(df.marital == group)]
			elif 'income' in filter_group:
				if group == 'media':		
					df_to_use = df[(df.income == "media") | (df.income == "media alta")]
				elif group == 'baixa':
					df_to_use = df[(df.income == "baixa") | (df.income == "media baixa")]
			elif 'age' in filter_group:
				if group == 'adulto':
					df_to_use = df[(df.age >= 25)]
				elif group == 'jovem':
					df_to_use = df[(df.age <= 24)]
		else:
			df_to_use = df

		#Pleasantness and safety data
		list_of_predictors_agrad = ['age', 'masculino', 'feminino', 'baixa', 'media baixa', 'media', 'media alta', 'solteiro', 'casado', 'street_wid1', 'mov_cars1', 'park_cars1', 'mov_ciclyst1', 'landscape1', 'build_ident1', 'trees1', 'build_height1', 'diff_build1', 'people1', 'graffiti1_No', 'graffiti1_Yes', 'bairro1_catole', 'bairro1_centro', 'bairro1_liberdade', 'street_wid2', 'mov_cars2', 'park_cars2', 'mov_ciclyst2', 'landscape2', 'build_ident2', 'trees2', 'build_height2', 'diff_build2', 'people2', 'graffiti2_No', 'graffiti2_Yes', 'bairro2_catole', 'bairro2_centro', 'bairro2_liberdade']#, 'graduacao', 'mestrado', 'ensino medio'
		agrad_df = df_to_use[(df_to_use.question != "seguro?")]
		agrad_df = convertColumnsToDummy(agrad_df)
		for column in ['masculino', 'feminino', 'baixa', 'media baixa', 'media', 'media alta', 'solteiro', 'casado']:
			if not column in agrad_df.columns:
				list_of_predictors_agrad.remove(column)
		answer_agrad = agrad_df['choice']#Preferred images
		predictors_agrad = agrad_df[list_of_predictors_agrad].values #Predictors
	
		list_of_predictors_seg = ['age', 'masculino', 'feminino', 'baixa', 'media baixa', 'media', 'media alta', 'solteiro', 'casado', 'street_wid1', 'mov_cars1', 'park_cars1', 'mov_ciclyst1', 'landscape1', 'build_ident1', 'trees1', 'build_height1', 'diff_build1', 'people1', 'graffiti1_No', 'graffiti1_Yes', 'bairro1_catole', 'bairro1_centro', 'bairro1_liberdade', 'street_wid2', 'mov_cars2', 'park_cars2', 'mov_ciclyst2', 'landscape2', 'build_ident2', 'trees2', 'build_height2', 'diff_build2', 'people2', 'graffiti2_No', 'graffiti2_Yes', 'bairro2_catole', 'bairro2_centro', 'bairro2_liberdade']#, 'graduacao', 'mestrado', 'ensino medio'
		seg_df = df_to_use[(df_to_use.question == "seguro?")]
		seg_df = convertColumnsToDummy(seg_df)
		for column in ['masculino', 'feminino', 'baixa', 'media baixa', 'media', 'media alta', 'solteiro', 'casado']:
			if not column in seg_df.columns:
				list_of_predictors_seg.remove(column)
		answer_seg = seg_df['choice']#Preferred images
		predictors_seg = seg_df[list_of_predictors_seg].values #Predictors

		#Classifiers parameters to be tested
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
			'C' : [0.001, 0.1, 1, 10, 100, 1000],
			'class_weight' : ['balanced', None]
		},
		"RBF SVM" : {
			'C' : [0.001, 0.1, 1],
			#'gamma' : ['Auto', 'RS*'],
			'gamma' : [0.25, 0.5, 1, 2, 4],
			'class_weight' : ['balanced', None]
		}
		}
		classifiers_names = ["Extra Trees"]#, "Nearest Neighbors", "RBF SVM", "Naive Bayes", "Linear SVM"]
	
		if phase == 'train-config':
			classifiers = [ExtraTreesClassifier(n_jobs=-1, criterion='entropy')]#, KNeighborsClassifier(3), SVC(kernel="linear", C=0.025), SVC(gamma=2, C=1), GaussianNB()]
			train_classifiers("Pleasantness", predictors_agrad, answer_agrad, parameters_dic, classifiers_names, classifiers, group)
			train_classifiers("Safety", predictors_seg, answer_seg, parameters_dic, classifiers_names, classifiers, group)

		elif phase == 'train-user-out':
			classifiers = [ExtraTreesClassifier(n_jobs=-1, criterion='entropy')]
			train_classifiers_leave_user_out("Pleasantness", list_of_predictors_agrad, agrad_df, parameters_dic, classifiers_names, classifiers, group)
			#train_classifiers_leave_user_out("Safety", list_of_predictors_seg, seg_df, parameters_dic, classifiers_names, classifiers, group)
			#train_classifiers_leave_user_out2("Pleasantness", list_of_predictors_agrad, agrad_df, group, load_3classes)
			#train_classifiers_leave_user_out2("Safety", list_of_predictors_seg, seg_df, group, load_3classes)

		elif phase == 'importances':
			test_features_importances(classifiers_names, predictors_agrad, answer_agrad, predictors_seg, answer_seg, list_of_predictors_agrad, list_of_predictors_seg, group, load_3classes)
		
		elif phase == 'test':
			#list_of_predictors = ['landscape1']
			classifiers_names = ["Extra Trees", "Nearest Neighbors", "RBF SVM", "Naive Bayes"]#, "Linear SVM"]
			test_classifiers(classifiers_names, predictors_agrad, answer_agrad, predictors_seg, answer_seg, group, load_3classes)

		elif phase == 'random':
			test_random(predictors_agrad, answer_agrad, predictors_seg, answer_seg, group)

		else:
			print "Phase not selected correctly: train-config, train-user-out, importances, importances-file, test or random!"
			sys.exit(1)

