from sklearn.cross_validation import LeaveOneLabelOut

from sklearn.grid_search import GridSearchCV
from sklearn.linear_model import LogisticRegressionCV

from sklearn.ensemble import ExtraTreesClassifier

from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import precision_recall_fscore_support
from sklearn.preprocessing import StandardScaler

import numpy as np
import pandas as pd
import statsmodels.api as sm


# In[2]:

def scale_and_combine(df, scaler, cols_to_scale, cols_to_combine):
    df_new = df.copy()
    df_new[cols_to_scale] = scaler.transform(df[cols_to_scale].copy())
    for u_col in cols_to_combine:
        for o_col in cols_to_scale:
            new_name = u_col + ':' + o_col
            df_new[new_name] = df[u_col] * df_new[o_col]
    for u_col in cols_to_combine:
        del df_new[u_col]
    return df_new


# In[3]:

def train_test_scale(df, y, users, cols_to_scale, cols_to_combine):
    for train, test in LeaveOneLabelOut(users):
        scaler = StandardScaler().fit(df.iloc[train][cols_to_scale].copy())
        df_new_train = scale_and_combine(df.iloc[train], scaler, cols_to_scale, cols_to_combine)
        df_new_test = scale_and_combine(df.iloc[test], scaler, cols_to_scale, cols_to_combine)
        yield df_new_train, df_new_test, y.iloc[train], y.iloc[test]


# In[4]:

fpath = 'seg.dat'
df_orig = pd.read_csv(fpath, sep=' ')
df_user = pd.get_dummies(df_orig, columns=['age_cat', 'gender', 'inc_cat'], drop_first=False, prefix='user')
df_user_bairro = pd.get_dummies(df_user, columns=['bair_cat'], drop_first=False, prefix='bairro')
user_ids = df_user_bairro['userID'].copy()
del df_user_bairro['userID']
del df_user_bairro['bairro_mesmo']
del df_user_bairro['user_jovem']
del df_user_bairro['user_feminino']
del df_user_bairro['user_baixa']
df_user_bairro = sm.add_constant(df_user_bairro)
y = pd.read_csv('y_' + fpath)


# In[5]:

user_cols = [x for x in df_user_bairro.columns if x.startswith('user_')]
bairro_cols = [x for x in df_user_bairro.columns if x.startswith('bairro_')]
other_cols = [x for x in df_user_bairro.columns if x.startswith('d_')]


# In[6]:

scaler = StandardScaler().fit(df_user_bairro[other_cols].copy())
df_david = scale_and_combine(df_user_bairro, scaler, other_cols, user_cols)
#model = sm.Logit(y, df_david)
#fitted = model.fit()
#fitted.summary()


# In[7]:

#fitted.params[fitted.pvalues < 0.05]


# In[22]:

def do_class(df, y, user_ids, cols_to_scale, cols_to_combine):
    y_pred_all = []
    y_true_all = []
    for df_train, df_test, y_train, y_test in train_test_scale(df, y, user_ids, cols_to_scale, cols_to_combine):
	print "### One more user"
        model = GridSearchCV(ExtraTreesClassifier(n_jobs=-1), param_grid = {'min_samples_split': [2, 4, 8, 16, 32, 64, 128],
                      'min_samples_leaf': [2, 4, 8, 16, 32, 64, 128],
                      'n_estimators': [1, 2, 4, 16, 32, 64, 128]}, \
            cv=2)
        model.fit(df_train.values, y_train.values[:, 0])
	
	print "CONF " + str(model.n_estimators) + "\t" + str(model.max_features) + "\t" + str(model.max_depth)+ "\t" + str(model.min_samples_split)+ "\t" + str(model.min_samples_leaf)

        y_pred = model.predict(df_test.values)
        #model = sm.Logit(y_train, df_train)
        #fitted = model.fit()
        #y_pred = fitted.predict(df_test) >= 0.5
        y_pred_all.extend(y_pred)
        y_true_all.extend(y_test.values[:, 0])
    
    print(y_true_all)
    print(y_pred_all)
    print(classification_report(y_true_all, y_pred_all))
    print(accuracy_score(y_true_all, y_pred_all))


do_class(df_user_bairro, y, user_ids, other_cols, user_cols)

