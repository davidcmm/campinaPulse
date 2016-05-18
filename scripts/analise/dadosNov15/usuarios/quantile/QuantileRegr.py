
# coding: utf-8

# In[1]:

get_ipython().magic(u'matplotlib inline')
from __future__ import division, print_function

from scipy import stats as ss
from sklearn.preprocessing import StandardScaler
from statsmodels.stats import multitest
from statsmodels.regression.quantile_regression import QuantReg

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# In[2]:

df = pd.read_csv('pleasantness.dat', sep=' ')
features = ['mov_cars', 'park_cars', 'debris', 'landscape', 
            'mov_ciclyst', 'street_wid', 'build_ident', 'trees', 
            'diff_build', 'people', 'build_height', 'red', 'green', 'blue']
#for x in df.columns:
#    print(x)


# In[3]:

rank_jovem = df['V3.Jovem'].argsort()
rank_adulto = df['V3.Adulto'].argsort()
response = (rank_jovem - rank_adulto)


# In[4]:

orig = df[features].copy()
#import itertools
#for f1, f2 in itertools.combinations(orig.columns.copy(), 2):
#    prod = orig[f1].values * orig[f2].values
#    orig[f1 + '_times_' + f2] = prod

orig['is_catole'] = np.array(df['bairro'] == 'catole', dtype='d')
orig['is_centro'] = np.array(df['bairro'] == 'centro', dtype='d')
orig['is_liberdade'] = np.array(df['bairro'] == 'liberdade', dtype='d')

scaled = pd.DataFrame(StandardScaler().fit_transform(orig.copy().values),
                      columns=orig.columns)
print(orig.shape)
assert orig.shape == scaled.shape


# In[5]:

model = QuantReg(response, orig)


# In[6]:

for q in np.linspace(0.05, 0.95, 10):
    print(q)
    print(model.fit(q=q).summary())
    print()
    print()


# In[ ]:




# In[ ]:




# In[ ]:



