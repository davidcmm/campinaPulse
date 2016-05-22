
# coding: utf-8

# In[1]:

get_ipython().magic(u'matplotlib inline')
from __future__ import division, print_function

from scipy import stats as ss
from sklearn.preprocessing import MinMaxScaler
from statsmodels.stats import multitest
from statsmodels.regression.quantile_regression import QuantReg

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


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

from IPython.display import Image
Image(filename='ex1.png')


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

from IPython.display import Image
Image(filename='ex2.png')


# In[4]:

from IPython.display import Image
Image(filename='ex2.png')


# In[ ]:




# In[5]:

df = pd.read_csv('pleasantness.dat', sep=' ')
df['graffiti'] = np.array(df['graffiti'] == 'Yes', dtype='d')
features = ['mov_cars', 'park_cars', 'landscape', 
            'mov_ciclyst', 'street_wid', 'build_ident', 'trees', 
            'diff_build', 'people', 'build_height', 'graffiti']#, 'red', 'green', 'blue', 'debris']


# In[6]:

np.warnings.filterwarnings("ignore")
groups = [('Jovem', 'Adulto'), ('Masculino', 'Feminino'), ('Baixa', 'Media'), ('Casado', 'Solteiro')]
yLimits = {}
for first_min_second in groups:
    
    print('!!!!!!!!!!!!!!!')
    print(first_min_second)
    print('!!!!!!!!!!!!!!!')
    
    rankg1 = df['V3.%s' % first_min_second[0]].argsort()
    rankg2 = df['V3.%s' % first_min_second[1]].argsort()
    
    rankg1 = 107 - rankg1.values#Ascending order!
    rankg2 = 107 - rankg2.values
    
    response = np.array((rankg1 - rankg2), dtype='d')# ** 3

    #rankg1 = df['V3.%s' % first_min_second[0]].argsort().values#Increasing order!
    #rankg2 = df['V3.%s' % first_min_second[1]].argsort().values
    #response = np.array((rankg1 - rankg2), dtype='d')# ** 3
    #response = MinMaxScaler().fit_transform(response[:, None])[:, 0]
    response = pd.DataFrame(response, columns=['Rank%s-Rank%s' % first_min_second])
    
    explanatory = df[features].copy()
    #explanatory = pd.DataFrame(MinMaxScaler().fit_transform(explanatory.copy().values),
    #                      columns=explanatory.columns)
    #explanatory['intercept'] = np.ones(len(explanatory), dtype='d')
    explanatory['is_catole'] = np.array(df['bairro'] == 'catole', dtype='d')
    explanatory['is_centro'] = np.array(df['bairro'] == 'centro', dtype='d')
    explanatory['is_liberdade'] = np.array(df['bairro'] == 'liberdade', dtype='d')
    
    model = QuantReg(response, explanatory)
    max_left = 0.0
    max_left_q = 0
    max_right = 0.0
    max_right_q = 0
    
    rsqs = []
    qs = []
    util = []
    
    values = {}
    for name in explanatory.columns:
        values[name] = np.zeros(10)
        i = 0
        for q in np.linspace(0.05, 0.95, 10):
            values[name][i] = 0
            i += 1
            
    for i, q in enumerate(np.linspace(0.05, 0.95, 10)):
        fitted = model.fit(q=q)
        adjr2 = fitted.prsquared
        qs.append(q)
        rsqs.append(adjr2)
        
    	for name in fitted.params[fitted.pvalues < 0.05].index:
            if fitted.params[name] != 0:
		print(first_min_second[0]+"_"+first_min_second[1]+"\t"+name+"\t"+str(fitted.params[name])
                      +"\t"+str(q)+"\t"+str(fitted.pvalues[name]))
                values[name][i] = fitted.params[name]
            
        util.append(sum(fitted.pvalues < 0.05))
        
        if q > 0.5 and adjr2 > max_right:
            max_right = adjr2
            max_right_q = q
            
        if q < 0.5 and adjr2 > max_left:
            max_left = adjr2
            max_left_q = q
            
    fitted_left = model.fit(q=max_left_q)
    good_left = fitted_left.params[fitted_left.pvalues < 0.05]
    
    fitted_right = model.fit(q=max_right_q)
    good_right = fitted_right.params[fitted_right.pvalues < 0.05]    

    print('Looking into model quality. Extremes are better, indicating that it is where features matter')
    plt.title('<- %s ; %s ->' % (first_min_second[1], first_min_second[0]))
    plt.plot(qs, rsqs, 'wo')
    plt.xlabel('Quantile')
    plt.ylabel('Adjusted-R2')
    plt.show()
    
    print('Number of variables w p < 0.05 per quantile')
    plt.title('<- %s ; %s ->' % (first_min_second[1], first_min_second[0]))
    plt.plot(qs, util, 'wo')
    plt.xlabel('Quantile')
    plt.ylabel('Variables where p < 0.05')
    plt.show()
    
    print('Looking into important variables')
    if first_min_second[0] == 'Jovem':
        yLimits[first_min_second] = [-150, 150]
    elif first_min_second[0] == 'Masculino':
        yLimits[first_min_second] = [-160, 160]
    elif first_min_second[0] == 'Casado':
        yLimits[first_min_second] = [-160, 160]
    elif first_min_second[0] == 'Baixa':
        yLimits[first_min_second] = [-150, 150]
        
    
    plt.title('<- %s ; %s ->' % (first_min_second[1], first_min_second[0]))
    plt.xlabel('Quantile')
    plt.ylabel('Features\n <- %s ; %s ->' % (first_min_second[1], first_min_second[0]))
    axes = plt.gca()
    axes.set_xlim([0,1])
    axes.set_ylim(yLimits[first_min_second])

    use_colours = {"street_wid": "gray", "mov_cars": "red", "park_cars": "lightsalmon"
                   , "mov_ciclyst": "yellow", "landscape": "blue", "build_ident": "lightblue", 
                   "trees": "green", "build_height": "darkgray", "diff_build": "purple", 
                   "people": "orange", "graffiti": "black", "is_catole": "salmon", "is_centro": "springgreen",
                   "is_liberdade": "magenta"}

    for name in values:
        y = values[name]
        if y.any():
            #plt.title('<- %s ; %s ->' % (first_min_second[1], first_min_second[0]))
            #plt.plot(qs, y, 'ro')
            #plt.xlabel('Quantile')
            #plt.ylabel(name + '\n <- %s ; %s ->' % (first_min_second[1], first_min_second[0]))
            #axes = plt.gca()
            #axes.set_xlim([0,1])
            #axes.set_ylim(yLimits[first_min_second])
            #plt.show()

	    plt.figure(1) 
            #plt.plot(qs, y, 'ro')#plt.plot(qs, y, 'ro')
            plt.scatter(qs,y,c=[use_colours[name] for name in values],s=50)

    plt.show()
    
#     print('=====================')
#     print('What if we consider the "peak" models')
#     print('======================================')
          
#     print('What causes a good impression for %s' %first_min_second[0])
#     print(good_right[good_right > 0])
#     for name in good_right[good_right > 0].index:
#         plt.plot(explanatory[name], response, 'wo')
#         idx = explanatory[name].values.argsort()
#         plt.plot(explanatory[name][idx], fitted_right.predict()[idx], 'r-')
#         plt.xlabel('Value for - %s' % name)
#         plt.ylabel('Difference in Ranking')
#         plt.show()
    
#     print()
#     print('Bad impression')
#     print(good_right[good_right < 0])
#     for name in good_right[good_right < 0].index:
#         plt.plot(explanatory[name], response, 'wo')
#         idx = explanatory[name].values.argsort()
#         plt.plot(explanatory[name][idx], fitted_right.predict()[idx], 'r-')
        
#         plt.xlabel('Value for - %s' % name)
#         plt.ylabel('Difference in Ranking')
#         plt.show()
        
#     print()
#     print('The model for %s' %first_min_second[0])
#     print(fitted_right.summary())
#     print()
#     print()
    
#     print('What causes a good impression for %s' %first_min_second[1])
#     print(good_left[good_left < 0])
#     for name in good_left[good_left < 0].index:
#         plt.plot(explanatory[name], response, 'wo')
#         idx = explanatory[name].values.argsort()
#         plt.plot(explanatory[name][idx], fitted_left.predict()[idx], 'b-')
#         plt.xlabel('Value for - %s' % name)
#         plt.ylabel('Difference in Ranking')
#         plt.show()
        
#     print()
#     print('Bad impression')
#     print(good_left[good_left > 0])
#     for name in good_left[good_left > 0].index:
#         plt.plot(explanatory[name], response, 'wo')
#         idx = explanatory[name].values.argsort()
#         plt.plot(explanatory[name][idx], fitted_left.predict()[idx], 'b-')
#         plt.xlabel('Value for - %s' % name)
#         plt.ylabel('Difference in Ranking')
#         plt.show()
        
#     print()
#     print('The model for %s' %first_min_second[1])
#     print(fitted_left.summary())
#     print()
#     print()


# In[ ]:




# In[ ]:




