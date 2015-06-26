import pandas as pd
import numpy as np

def abs_mean(data1, data2):
    argsrt_1 = data1.argsort()
    argsrt_2 = data2.argsort()
    return np.abs(argsrt_1 - argsrt_2).mean()

def abs_median(data1, data2):
    argsrt_1 = data1.argsort()
    argsrt_2 = data2.argsort()
    return np.median(np.abs(argsrt_1 - argsrt_2))

def top10_abs_mean_naza(data1, data2):
    argsrt_1 = data1.argsort()
    argsrt_2 = data2.argsort()

    abs_diff = np.abs(argsrt_1 - argsrt_2)
    top_10_1 = abs_diff[argsrt_1[-10:]]
    top_10_2 = abs_diff[argsrt_2[-10:]]
    
    result = (top_10_1.mean() + top_10_2.mean()) / 2
    return result 

def top10_abs_mean_old(data1, data2):
    argsrt_1 = data1.argsort()
    argsrt_2 = data2.argsort()
    abs_diff = np.abs(argsrt_1 - argsrt_2)
    top = abs_diff.argsort()[-10:]
    return abs_diff[top].mean()

def ptest(df, name_g1, name_g2, pergunta, bairro=None, num_permut=100000):
    df = df[df.values[:, 1] == pergunta]
    if bairro is not None:
        df = df[df['bairro'] == bairro]

    g1 = df[df['grupo'] == name_g1].values[:, 2]
    g2 = df[df['grupo'] == name_g2].values[:, 2]
    all_ = np.hstack((g1, g2))
    
    n_g1 = len(g1)
    n_g2 = len(g2)
    n_all =  len(all_)
    
    functions = [
            ('Mean', abs_mean),
            ('Median', abs_median),
            ('Top10-Mean-Old', top10_abs_mean_old),
            ('Top10-Mean-Naza', top10_abs_mean_naza)]
    
    actual = np.zeros(len(functions))
    for i in xrange(len(functions)):
        actual[i] = functions[i][1](g1, g2)
    
    P = np.tile(np.arange(n_all), num_permut).reshape(num_permut, n_all)
    P = np.apply_along_axis(np.random.permutation, 1, P)
    R = np.zeros(shape=(P.shape[0], len(functions)))
    permut_array = np.zeros(P.shape[0], dtype='f')
    for i in xrange(P.shape[0]):
        permut = P[i]
        new_data = all_[permut]
        new_g1 = new_data[:n_g1]
        new_g2 = new_data[n_g1:]
        
        for j in xrange(len(functions)):
            R[i][j] = functions[j][1](new_g1, new_g2)
    
    pvals = []
    for i in xrange(len(functions)):
        pvals.append(float((R[:, i] > actual[i]).sum()) / R.shape[0])
    
    return (name_g1, name_g2, pergunta), actual, np.array(pvals), functions

bairro = 'centro'

df = pd.read_csv('geral.dat', sep=' ', encoding='utf8')
df.drop(['red', 'green', 'blue', 'hor', 'vert', 'diag'], axis=1, inplace=True)

all_res = []

all_res.append(ptest(df, 'Masculino', 'Feminino', 'agradavel?', bairro=bairro))
all_res.append(ptest(df, 'Masculino', 'Feminino', 'seguro?', bairro=bairro))

all_res.append(ptest(df, 'Jovem', 'Adulto', 'agradavel?', bairro=bairro))
all_res.append(ptest(df, 'Jovem', 'Adulto', 'seguro?', bairro=bairro))

all_res.append(ptest(df, 'Solteiro', 'Casado', 'agradavel?', bairro=bairro))
all_res.append(ptest(df, 'Solteiro', 'Casado', 'seguro?', bairro=bairro))

all_res.append(ptest(df, 'Baixa', 'Media', 'agradavel?', bairro=bairro))
all_res.append(ptest(df, 'Baixa', 'Media', 'seguro?', bairro=bairro))

all_res.append(ptest(df, 'Medio', 'Pos', 'agradavel?', bairro=bairro))
all_res.append(ptest(df, 'Medio', 'Pos', 'seguro?', bairro=bairro))

for r in all_res:
    print r[0]
    for i, f in enumerate(r[-1]):
        print f[0], r[1][i]
        print 'pval', r[2][i]
        print
    print '--'
