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
from sklearn.linear_model import LogisticRegressionCV
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

def explainClassification(headers, target_names, X_train_scaled, X_test_scaled, clf, index):
    #explainClassification(list_of_predictors, current_df['choice'].unique(), predictors_test, clf, index)

    #c = make_pipeline(vectorizer, clf)
    #headers = np.array(['age', 'gender', 'income', 'educ', 'marital', 'street_wid1', 'mov_cars1', 'park_cars1', 'mov_ciclyst1', 'landscape1', 'build_ident1', 'trees1', 'build_height1', 'diff_build1', 'people1', 'graffiti1', 'bairro1', 'street_wid2', 'mov_cars2', 'park_cars2', 'mov_ciclyst2', 'landscape2', 'build_ident2', 'trees2', 'build_height2', 'diff_build2', 'people2', 'graffiti2', 'bairro2'])
    targetNames = np.array(map(str, target_names))
    #TODO ERROR HERE! PRINT ALL
    
    #print("HEADERS " + str(headers) + " " + str(len(headers)))
    #print("TARGET " + str(target_names)+ " " + str(len(target_names)))
    #print("predi " + str(predictors[1:5]) + " " + str(len(predictors)))
    #print("answer " + str(answer)+ " " + str(len(answer)))
    #print("CLF " + str(clf))
    #print("INDEX " + str(answer[index]))
    #print("PROBA " + str(clf.predict_proba)+ " " + str(clf.predict_proba))

    explainer = LimeTabularExplainer(X_train_scaled, feature_names=headers, class_names=target_names, 
                                     discretize_continuous=True)
    exp = explainer.explain_instance(X_test_scaled[index], clf.predict_proba, num_features=len(headers), 
                                     top_labels=1)
    
    #exp.show_in_notebook(show_table=True, show_all=False)
    return exp


#Main!
input_file = 'classifier_input_wodraw.dat'

#Using 3 classes or two classes as output
if "3classes" in input_file.lower():
    load_3classes = True
else:
    load_3classes = False

df = pd.read_table(input_file, sep='\t', encoding='utf8', header=0)
#Remove unecessary chars!
df = stripDataFrame(df)

#for groups_data in [("", "")]:
for groups_data in [ ("income-baixa", "baixa"), ("income-media", "media"), ("marital-solteiro", "solteiro"), ("marital-casado", "casado")]:

	filter_group = groups_data[0]
	group = groups_data[1]

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
	agrad_df = df_to_use[(df_to_use.question != "seguro?")]
	agrad_df = convertColumnsToDummy(agrad_df)
	list_of_predictors_agrad = ['age', 'masculino', 'feminino', 'baixa', 'media baixa', 'media', 'media alta', 
		              'solteiro', 'casado', 'street_wid1', 'mov_cars1', 'park_cars1', 'mov_ciclyst1', 
		              'landscape1', 'build_ident1', 'trees1', 'build_height1', 'diff_build1', 'people1', 
		              'graffiti1_No', 'graffiti1_Yes', 'bairro1_catole', 'bairro1_centro', 'bairro1_liberdade', 
		              'street_wid2', 'mov_cars2', 'park_cars2', 'mov_ciclyst2', 'landscape2', 'build_ident2', 
		              'trees2', 'build_height2', 'diff_build2', 'people2', 'graffiti2_No', 'graffiti2_Yes', 
		              'bairro2_catole', 'bairro2_centro', 'bairro2_liberdade']
	for column in ['masculino', 'feminino', 'baixa', 'media baixa', 'media', 'media alta', 'solteiro', 'casado']:
		if not column in agrad_df.columns:
			list_of_predictors_agrad.remove(column)
	answer_agrad = agrad_df['choice']#Preferred images
	predictors_agrad = agrad_df[list_of_predictors_agrad].values #Predictors

	seg_df = df_to_use[(df_to_use.question == "seguro?")]
	seg_df = convertColumnsToDummy(seg_df)
	list_of_predictors_seg = ['age', 'masculino', 'feminino', 'baixa', 'media baixa', 'media', 'media alta', 
		              'solteiro', 'casado', 'street_wid1', 'mov_cars1', 'park_cars1', 'mov_ciclyst1', 
		              'landscape1', 'build_ident1', 'trees1', 'build_height1', 'diff_build1', 'people1', 
		              'graffiti1_No', 'graffiti1_Yes', 'bairro1_catole', 'bairro1_centro', 'bairro1_liberdade', 
		              'street_wid2', 'mov_cars2', 'park_cars2', 'mov_ciclyst2', 'landscape2', 'build_ident2', 
		              'trees2', 'build_height2', 'diff_build2', 'people2', 'graffiti2_No', 'graffiti2_Yes', 
		              'bairro2_catole', 'bairro2_centro', 'bairro2_liberdade']
	for column in ['masculino', 'feminino', 'baixa', 'media baixa', 'media', 'media alta', 'solteiro', 'casado']:
		if not column in seg_df.columns:
			list_of_predictors_seg.remove(column)
	answer_seg = seg_df['choice']#Preferred images
	predictors_seg = seg_df[list_of_predictors_seg].values #Predictors

	#Loading classifiers
	classifiers_agrad = [LogisticRegressionCV()]
	classifiers_seg = [LogisticRegressionCV()]

	#Evaluate each data frame
	data_frames = [agrad_df, seg_df]
	for index_df in range(0, len(data_frames)):
	    current_df = data_frames[index_df]
	    current_df = current_df.sort_values(by='choice', ascending=True)
            user_ids = current_df['userID'].unique()#Selecting users
	    relevance_map_pro = {}
	    relevance_map_aga = {}
	    probabilities_map = {}

	    history_micro = []
    	    history_macro = []
  	    history_acc = []

	    if index_df == 0:#Selecting predictors
		list_of_predictors = list_of_predictors_agrad
	    else:
		list_of_predictors = list_of_predictors_seg

	    print( ">>> Question\t" + str(("Safety", "Pleasantness")[index_df == 0]) + "\t" + group )
	    
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
	
		if index_df == 0:#Selecting classifiers
			clf = classifiers_agrad[0]
	    	else:
			clf = classifiers_seg[0]
	
		#Fitting
		clf.fit(X_train_scaled, answer_train)

		accuracy = best_clf.score(X_test_scaled, answer_test)#Accuracy
		y_pred = best_clf.predict(X_test_scaled)#Estimated values
		metrics_macro = precision_recall_fscore_support(y_test, y_pred, average='macro')#Calculates for each label and compute the mean!
		metrics_micro = precision_recall_fscore_support(y_test, y_pred, average='micro')#Total false positives, negatives and true positives -> more similar to accuracy

		history_micro.append(metrics_micro[0:3])
		history_macro.append(metrics_macro[0:3])
		history_acc.append(accuracy)

		#LIME explanation!
		for index_answer in range(0, len(answer_test)):
    		    explanation = explainClassification(list_of_predictors, current_df['choice'].unique(), X_train_scaled, X_test_scaled, clf, index_answer)
		    
		    #Checking if prediction was correct!
		    current_answer = answer_test[index_answer]
		    predicted_answer = 0
		    predicted_answer_prob = 0
		    for index_exp in range(0, len(explanation.class_names)):#Most probable answer
		            if explanation.predict_proba[index_exp] > predicted_answer_prob:
		                predicted_answer_prob = explanation.predict_proba[index_exp]
		                predicted_answer = explanation.class_names[index_exp]

		    #If answer was correct consider features relevances
		    if int(current_answer) == int(predicted_answer):
			exp_map = explanation.as_map() 
			values = exp_map[exp_map.keys()[0]]
			for value in values:
			     if int(current_answer) > 0:
				     relevance_map = relevance_map_pro
			     else:
				     relevance_map = relevance_map_aga
			     if value[0] in relevance_map.keys():
				 relevance_map[value[0]].append(abs(value[1]))
			     else:
				 relevance_map[value[0]] = [abs(value[1])]
			for index_class in range(0, len(explanation.class_names)):
			     if explanation.class_names[index_class] in probabilities_map.keys():
				 probabilities_map[explanation.class_names[index_class]].append(explanation.predict_proba[index_class])
			     else:
				 probabilities_map[explanation.class_names[index_class]] = [explanation.predict_proba[index_class]]
	    
	    #Classifier statistics
	    std_acc = np.std(np.array(history_acc), axis=0)
	    mean_acc = np.mean(np.array(history_acc), axis=0)
	    std_micro = np.std(np.array(history_micro), axis=0)
	    mean_micro = np.mean(np.array(history_micro), axis=0)
	    std_macro = np.std(np.array(history_macro), axis=0)
	    mean_macro = np.mean(np.array(history_macro), axis=0)
	    print ">>>>\tmean_acc\tstd_acc\tmeans_micro\tstds_micro\tmeans_macro\tstd_macro"
	    print ">>>>\t" + str(mean_acc) + "\t" + str(std_acc) + "\t" + str(mean_micro) + "\t" + str(std_micro) + "\t" + str(mean_macro) + "\t" + str(std_macro)

	    #Printing statistics for data frame being evaluated
	    print ( "### PRO MAP" )
	    for key, value in relevance_map_pro.iteritems(): 
		mean = np.mean(value)
		std = np.std(value)
		print( str(key) + "\t" + list_of_predictors[key] + "\t" + str(mean) + "\t" + str(std) + "\t" + str(len(value)) )

	    print ( "### AGA MAP" )
	    for key, value in relevance_map_aga.iteritems(): 
		mean = np.mean(value)
		std = np.std(value)
		print( str(key) + "\t" + list_of_predictors[key] + "\t" + str(mean) + "\t" + str(std) + "\t" + str(len(value)) )

