
# coding: utf-8

# In[2]:
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
import pandas as pd

#Lime 
from sklearn.pipeline import make_pipeline
from lime.lime_tabular import *


# Quantile Regression Results
# ===========================
# 
# Quantile regression is a interesting for our problem because it:
#    - Is robust to non non-normal errors and outliers
#    
#      http://fmwww.bc.edu/EC-C/S2013/823/EC823.S2013.nn04.slides.pdf     
#      http://www.econ.uiuc.edu/~roger/research/rq/QRJEP.pdf
#      
#    - Focuses on the conditional quantiles. Allows for better interpretation of effects
#      of variables. In a lot of cases, the effect is not on the conditional mean (OLS assumption)
#      
#      http://fmwww.bc.edu/EC-C/S2013/823/EC823.S2013.nn04.slides.pdf
#      http://www.econ.uiuc.edu/~roger/research/rq/QRJEP.pdf
#    
#    - Is robust to data representation (no need to normalize etc etc)
#    
#      http://www.econ.uiuc.edu/~roger/research/rq/QRJEP.pdf
#      
# Good ref for math mechanics: 
# http://www.jmlr.org/papers/volume7/meinshausen06a/meinshausen06a.pdf
# 
# Nice introduction for other fields: 
# http://www.econ.uiuc.edu/~roger/research/rq/QReco.pdf

# Quantile Regression Crash Course
# --------------------------------
# 
# Plots from: 
#  http://www.econ.uiuc.edu/~roger/research/rq/QReco.pdf
#  
#  Important ref!
# 
# http://ajbuckeconbikesail.net/Econ616/Quantile/JASA1999.pdf
#  https://www.jstor.org/stable/2669943
#  
#   (this ref provides intuiton on how to use the method, for now we can ignore the math)

# **First of, what do we mean by conditional quantiles**

# In[2]:

#from IPython.display import Image
#Image(filename='ex1.png')


# **First task**
# 
# Find out where the variables matter (left plot)
# 
# Left plot is a r-squared like value. Greater is best. But interpretation of variance does not exist.
# From this paper and others, I noticed that the ideia is less of trying to maximize this. It is a tool
# to interpret where the covariates matter.
# 
# ** Second task ** 
# 
# Look into the effect of covaritates (right plot)
# 
# ps: I don't fully understand the middle plot, it is similar to the right one but another quality measure.

# In[3]:

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

    elif group == "modal":#All users (more common param for each group)
        classifiers_agrad = [ ExtraTreesClassifier(class_weight=None, criterion='entropy', min_samples_leaf=8, min_samples_split=16, n_estimators=20, n_jobs=-1, oob_score=False) ]

        classifiers_seg = [ ExtraTreesClassifier(class_weight=None, criterion='entropy', min_samples_leaf=8, min_samples_split=4, n_estimators=40, n_jobs=-1, oob_score=False) ]

    elif group == "all":#80-20 best configuration for classifiers with all features in!
        classifiers_agrad = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy',           max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=8, min_samples_split=32,           min_weight_fraction_leaf=0.0, n_estimators=60, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False) ]

        classifiers_seg = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy',           max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=16, min_samples_split=2,            min_weight_fraction_leaf=0.0, n_estimators=60, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False) ]

    else:
        classifiers_agrad = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy',           max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=16, min_samples_split=32,           min_weight_fraction_leaf=0.0, n_estimators=60, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False) ]

        classifiers_seg = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy',           max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=8, min_samples_split=8,           min_weight_fraction_leaf=0.0, n_estimators=60, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False) ]

    return [classifiers_agrad, classifiers_seg]

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

    elif group == "modal":#All users (more common param for each group - Extra)
        classifiers_agrad = [ ExtraTreesClassifier(class_weight=None, criterion='entropy', min_samples_leaf=8, min_samples_split=2, n_estimators=60, n_jobs=-1, oob_score=False) ]

        classifiers_seg = [ ExtraTreesClassifier(class_weight=None, criterion='entropy', min_samples_leaf=4, min_samples_split=8, n_estimators=40, n_jobs=-1, oob_score=False) ]

    elif group == "all":#All features in best configuration 80-20
        classifiers_agrad = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy',           max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=2, min_samples_split=32,         min_weight_fraction_leaf=0.0, n_estimators=60, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False) ]

        classifiers_seg = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy',           max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=2, min_samples_split=4,           min_weight_fraction_leaf=0.0, n_estimators=60, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False) ]

    else:
        classifiers_agrad = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy',           max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=8, min_samples_split=8,          min_weight_fraction_leaf=0.0, n_estimators=60, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False) ]

        classifiers_seg = [ ExtraTreesClassifier(bootstrap=False, class_weight=None, criterion='entropy',           max_depth=None, max_features='auto', max_leaf_nodes=None, min_samples_leaf=8, min_samples_split=8,            min_weight_fraction_leaf=0.0, n_estimators=60, n_jobs=-1, oob_score=False, random_state=None, verbose=0, warm_start=False) ]


    return [classifiers_agrad, classifiers_seg]


# In[4]:

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


# In[5]:

def explainClassification(headers, target_names, predictors, answer, clf, index):
    #c = make_pipeline(vectorizer, clf)
    #headers = np.array(['age', 'gender', 'income', 'educ', 'marital', 'street_wid1', 'mov_cars1', 'park_cars1', 'mov_ciclyst1', 'landscape1', 'build_ident1', 'trees1', 'build_height1', 'diff_build1', 'people1', 'graffiti1', 'bairro1', 'street_wid2', 'mov_cars2', 'park_cars2', 'mov_ciclyst2', 'landscape2', 'build_ident2', 'trees2', 'build_height2', 'diff_build2', 'people2', 'graffiti2', 'bairro2'])
    #targetNames = np.array(['1', '0', '-1'])
    #TODO ERROR HERE! PRINT ALL
    #explainClassification(list_of_predictors, ['-1', '0', '1'], 
                              #predictors_test, answer_test, clf, 0)
    
    #print("HEADERS " + str(headers) + " " + str(len(headers)))
    #print("TARGET " + str(target_names)+ " " + str(len(target_names)))
    #print("predi " + str(predictors[1:5]) + " " + str(len(predictors)))
    #print("answer " + str(answer)+ " " + str(len(answer)))
    #print("CLF " + str(clf))
    #print("INDEX " + str(answer[index]))
    #print("PROBA " + str(clf.predict_proba)+ " " + str(clf.predict_proba))

    explainer = LimeTabularExplainer(predictors, feature_names=headers, class_names=target_names, 
                                     discretize_continuous=True)
    exp = explainer.explain_instance(predictors[index], clf.predict_proba, num_features=len(headers), 
                                     top_labels=1)
    
    #exp.show_in_notebook(show_table=True, show_all=False)
    return exp


# In[6]:

input_file = 'classifier_input_wodraw.dat'

#Using 3 classes or two classes as output
if "3classes" in input_file.lower():
    load_3classes = True
else:
    load_3classes = False

df = pd.read_table(input_file, sep='\t', encoding='utf8', header=0)

#Remove unecessary chars!
df = stripDataFrame(df)

list_of_predictors = ['age', 'masculino', 'feminino', 'baixa', 'media baixa', 'media', 'media alta', 
                      'solteiro', 'casado', 'street_wid1', 'mov_cars1', 'park_cars1', 'mov_ciclyst1', 
                      'landscape1', 'build_ident1', 'trees1', 'build_height1', 'diff_build1', 'people1', 
                      'graffiti1_No', 'graffiti1_Yes', 'bairro1_catole', 'bairro1_centro', 'bairro1_liberdade', 
                      'street_wid2', 'mov_cars2', 'park_cars2', 'mov_ciclyst2', 'landscape2', 'build_ident2', 
                      'trees2', 'build_height2', 'diff_build2', 'people2', 'graffiti2_No', 'graffiti2_Yes', 
                      'bairro2_catole', 'bairro2_centro', 'bairro2_liberdade']
filter_group = ""
group = ""

if len(filter_group) > 0:

    if 'gender' in filter_group:
        df_to_use = df[(df.gender == group)]
        if group == 'masculino':
            list_of_predictors.remove('feminino')
        else:
            list_of_predictors.remove('masculino')
    elif 'marital' in filter_group:
        df_to_use = df[(df.marital == group)]
        if group == 'casado':
            list_of_predictors.remove('solteiro')
        else:
            list_of_predictors.remove('casado')
    elif 'income' in filter_group:
        if group == 'media':		
            df_to_use = df[(df.income == "media") | (df.income == "media alta")]
            list_of_predictors.remove('baixa')
            list_of_predictors.remove('media baixa')
        elif group == 'baixa':
            df_to_use = df[(df.income == "baixa") | (df.income == "media baixa")]
            list_of_predictors.remove('media')
            list_of_predictors.remove('media alta')
    elif 'age' in filter_group:
        if group == 'adulto':
            df_to_use = df[(df.age >= 25)]
            list_of_predictors.remove('jovem')
        elif group == 'jovem':
            df_to_use = df[(df.age <= 24)]
            list_of_predictors.remove('adulto')
else:
    df_to_use = df
    
#Pleasantness and safety data
agrad_df = df_to_use[(df_to_use.question != "seguro?")]
agrad_df = convertColumnsToDummy(agrad_df)
answer_agrad = agrad_df['choice']#Preferred images
predictors_agrad = agrad_df[list_of_predictors].values #Predictors

seg_df = df_to_use[(df_to_use.question == "seguro?")]
seg_df = convertColumnsToDummy(seg_df)
answer_seg = seg_df['choice']#Preferred images
predictors_seg = seg_df[list_of_predictors].values #Predictors

if load_3classes:
    classifiers = load_classifiers_3classes("modal")
else:
    classifiers = load_classifiers_wodraw("modal")
classifiers_agrad = classifiers[0]
classifiers_seg = classifiers[1]

#Filtering per user
user_ids = df['userID'].unique()
#print ("IDS " + str(user_ids))

data_frames = [agrad_df, seg_df]#add seg_df
for index_df in range(0, len(data_frames)):
    current_df = data_frames[index_df]
    current_df = current_df.sort_values(by='choice', ascending=True)
    
    relevance_map = {}
    probabilities_map = {}

    print( ">>> Question\t" + str(("Safety", "Pleasantness")[index_df == 0]) )
    
    for user_id in user_ids:#Remove each user sequentially
        print("User\t" + str(user_id))
      
        current_df_train = current_df[(current_df.userID != user_id)]
        current_df_test = current_df[(current_df.userID == user_id)]

        predictors_train = np.array(current_df_train[list_of_predictors].values)
        predictors_test = np.array(current_df_test[list_of_predictors].values)
        X_train_scaled = predictors_train #Only extra trees is currently being used!
        X_test_scaled = predictors_test
        answer_train = np.array(current_df_train['choice'])
        answer_test = np.array(current_df_test['choice'])

        clf = classifiers_agrad[0]

        #Fitting
        clf.fit(X_train_scaled, answer_train)

        #Testing!
        #explainClassification(headers, target_names, predictors, answer, clf, index):
        for index in range(0, len(answer_test)):
            explanation = explainClassification(list_of_predictors, current_df['choice'].unique(),
                              predictors_test, answer_test, clf, index)
            
            #Checking if prediction was correct!
            current_answer = answer_test[index]
            predicted_answer = 0
            predicted_answer_prob = 0
            for index in range(0, len(explanation.class_names)):
                    if explanation.predict_proba[index] > predicted_answer_prob:
                        predicted_answer_prob = explanation.predict_proba[index]
                        predicted_answer = explanation.class_names[index]
            if current_answer == predicted_answer:
                #print ( str(exp.as_map()) )
                #print ( str(exp.class_names) )
                #print ( str(exp.predict_proba) )
                exp_map = explanation.as_map() 
                values = exp_map[exp_map.keys()[0]]
                if len(relevance_map) == 0:
                    for value in values:
                        relevance_map[value[0]] = [value[1]]
                    for index in range(0, len(explanation.class_names)):
                        probabilities_map[explanation.class_names[index]] = [explanation.predict_proba[index]]
                else:
                    for value in values:
                        relevance_map[value[0]].append(value[1])
                    for index in range(0, len(explanation.class_names)):
                        probabilities_map[explanation.class_names[index]].append(explanation.predict_proba[index])
    
    #Printing statistics
    for key, value in relevance_map.iteritems(): 
        mean = np.mean(value)
        std = np.std(value)
        print( str(key) + "\t" + list_of_predictors[key] + "\t" + str(mean) + "\t" + str(std))
        
# In[4]:




# In[5]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



