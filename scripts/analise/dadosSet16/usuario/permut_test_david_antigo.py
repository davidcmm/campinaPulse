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

def ptest(df, name_g1, name_g2, pergunta, bairro=None, setor=None, num_permut=100000):
    df = df[df.values[:, 1] == pergunta]

    if bairro is not None:
        df = df[df['bairro'] == bairro]
    if setor is not None:
        df = df[df['setor'] == int(setor)]

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

def ptestFromFiles(num_it, name_g1, name_g2, question, neig=None, sector=None):
    
    questionsMap = {'agradavel?' : 'agrad%C3%A1vel?', 'seguro?' : 'seguro?'}

    #Original data file
    dfOrig = pd.read_csv('geralSetoresAJ.dat', sep=' ', encoding='utf8')
    dfOrig = dfOrig.drop(['red', 'green', 'blue', 'hor', 'vert', 'diag'], axis=1)

    dfOrig = dfOrig[dfOrig.values[:, 1] == question]

    if neig is not None:
	dfOrig = dfOrig[dfOrig['bairro'] == neig]
    if sector is not None:
	dfOrig = dfOrig[dfOrig['setor'] == int(sector)]

    g1 = dfOrig[dfOrig['grupo'] == name_g1].values[:, 2]
    g2 = dfOrig[dfOrig['grupo'] == name_g2].values[:, 2]#Input files are sorted according to image names, so the order of QScores retrieved is paired for both groups

    functions = [
       ('Mean', abs_mean),
       ('Median', abs_median),
       ('Top10-Mean-Old', top10_abs_mean_old),
       ('Top10-Mean-Naza', top10_abs_mean_naza)]

    actual = np.zeros(len(functions))
    for i in xrange(len(functions)):
		actual[i] = functions[i][1](g1, g2)

    R = np.zeros(shape=(num_it, len(functions)))

    #Sampled users files
    newQuestion = questionsMap[question]
    for it in xrange(1, num_it+1):
	df = pd.read_csv('samplesIds/geralSetoresAJ_'+str(it)+'.dat', sep=' ', encoding='utf8')
    	df = df[df.values[:, 1] == newQuestion]

	if neig is not None:
		df = df[df['bairro'] == neig]
	if sector is not None:
		df = df[df['setor'] == int(sector)]

    	g1 = df[df['grupo'] == name_g1].values[:, 2]
    	g2 = df[df['grupo'] == name_g2].values[:, 2]
        
        for j in xrange(len(functions)):
            R[it-1][j] = functions[j][1](g1, g2)
    
    pvals = []
    for i in xrange(len(functions)):
        pvals.append(float((R[:, i] > actual[i]).sum()) / R.shape[0])
    
    return (name_g1, name_g2, question), actual, np.array(pvals), functions



#Using sample users files
num_it = 5
all_res = []

all_res.append(ptestFromFiles(num_it, 'Masculino', 'Feminino', 'agradavel?'))
all_res.append(ptestFromFiles(num_it, 'Masculino', 'Feminino', 'seguro?'))

all_res.append(ptestFromFiles(num_it, 'Jovem', 'Adulto', 'agradavel?'))
all_res.append(ptestFromFiles(num_it, 'Jovem', 'Adulto', 'seguro?'))

all_res.append(ptestFromFiles(num_it, 'Solteiro', 'Casado', 'agradavel?'))
all_res.append(ptestFromFiles(num_it, 'Solteiro', 'Casado', 'seguro?'))

all_res.append(ptestFromFiles(num_it, 'Baixa', 'Media', 'agradavel?'))
all_res.append(ptestFromFiles(num_it, 'Baixa', 'Media', 'seguro?'))

all_res.append(ptestFromFiles(num_it, 'Medio', 'Pos', 'agradavel?'))
all_res.append(ptestFromFiles(num_it, 'Medio', 'Pos', 'seguro?'))

print ">>>> General: "
for r in all_res:
  print r[0]
  for i, f in enumerate(r[-1]):
	print f[0], r[1][i]
	print 'pval', r[2][i]
	print
  print '--'

for neig in ['catole', 'centro', 'liberdade']:
	all_res = []

	all_res.append(ptestFromFiles(num_it, 'Masculino', 'Feminino', 'agradavel?', neig=neig))
	all_res.append(ptestFromFiles(num_it, 'Masculino', 'Feminino', 'seguro?', neig=neig))

	all_res.append(ptestFromFiles(num_it, 'Jovem', 'Adulto', 'agradavel?', neig=neig))
	all_res.append(ptestFromFiles(num_it, 'Jovem', 'Adulto', 'seguro?', neig=neig))

	all_res.append(ptestFromFiles(num_it, 'Solteiro', 'Casado', 'agradavel?', neig=neig))
	all_res.append(ptestFromFiles(num_it, 'Solteiro', 'Casado', 'seguro?', neig=neig))

	all_res.append(ptestFromFiles(num_it, 'Baixa', 'Media', 'agradavel?', neig=neig))
	all_res.append(ptestFromFiles(num_it, 'Baixa', 'Media', 'seguro?', neig=neig))

	all_res.append(ptestFromFiles(num_it, 'Medio', 'Pos', 'agradavel?', neig=neig))
	all_res.append(ptestFromFiles(num_it, 'Medio', 'Pos', 'seguro?', neig=neig))

#Files not created with these columns!
	#if neig == 'catole':
#		all_res.append(ptestFromFiles(num_it, 'CCatole', 'NCCatole', 'agradavel?', neig=neig))
#		all_res.append(ptestFromFiles(num_it, 'CCatole', 'NCCatole', 'seguro?', neig=neig))
#	elif neig == 'centro':
#		all_res.append(ptestFromFiles(num_it, 'CCentro', 'NCCentro', 'agradavel?', neig=neig))
#		all_res.append(ptestFromFiles(num_it, 'CCentro', 'NCCentro', 'seguro?', neig=neig))
#	else:
#		all_res.append(ptestFromFiles(num_it, 'CLiberdade', 'NCLiberdade', 'agradavel?', neig=neig))
#		all_res.append(ptestFromFiles(num_it, 'CLiberdade', 'NCLiberdade', 'seguro?', neig=neig))

	#all_res.append(ptestFromFiles(num_it, 'MenorMed', 'MaiorMed', 'agradavel?', neig=neig))
	#all_res.append(ptestFromFiles(num_it, 'MenorMed', 'MaiorMed', 'seguro?', neig=neig))

	print ">>>> Neighborhoods: ", neig
	for r in all_res:
	    print r[0]
	    for i, f in enumerate(r[-1]):
		print f[0], r[1][i]
		print 'pval', r[2][i]
		print
	    print '--'

for sector in ['25040090500004', '250400905000013', '250400905000060', '250400905000062', '250400905000095', '250400905000089']:
	all_res = []

	all_res.append(ptestFromFiles(num_it, 'Masculino', 'Feminino', 'agradavel?', sector=sector))
	all_res.append(ptestFromFiles(num_it, 'Masculino', 'Feminino', 'seguro?', sector=sector))

	all_res.append(ptestFromFiles(num_it, 'Jovem', 'Adulto', 'agradavel?', sector=sector))
	all_res.append(ptestFromFiles(num_it, 'Jovem', 'Adulto', 'seguro?', sector=sector))

	all_res.append(ptestFromFiles(num_it, 'Solteiro', 'Casado', 'agradavel?', sector=sector))
	all_res.append(ptestFromFiles(num_it, 'Solteiro', 'Casado', 'seguro?', sector=sector))

	all_res.append(ptestFromFiles(num_it, 'Baixa', 'Media', 'agradavel?', sector=sector))
	all_res.append(ptestFromFiles(num_it, 'Baixa', 'Media', 'seguro?', sector=sector))

	all_res.append(ptestFromFiles(num_it, 'Medio', 'Pos', 'agradavel?', sector=sector))
	all_res.append(ptestFromFiles(num_it, 'Medio', 'Pos', 'seguro?', sector=sector))

#Files not created with these columns!
	#if sector == '250400905000060' or sector == '250400905000062':
	#	all_res.append(ptestFromFiles(num_it, 'CCatole', 'NCCatole', 'agradavel?', sector=sector))
	#	all_res.append(ptestFromFiles(num_it, 'CCatole', 'NCCatole', 'seguro?', sector=sector))
	#elif sector == '25040090500004' or sector == '250400905000013':
	#	all_res.append(ptestFromFiles(num_it, 'CCentro', 'NCCentro', 'agradavel?', sector=sector))
	#	all_res.append(ptestFromFiles(num_it, 'CCentro', 'NCCentro', 'seguro?', sector=sector))
	#else:
	#	all_res.append(ptestFromFiles(num_it, 'CLiberdade', 'NCLiberdade', 'agradavel?', sector=sector))
	#	all_res.append(ptestFromFiles(num_it, 'CLiberdade', 'NCLiberdade', 'seguro?', sector=sector))

        #all_res.append(ptestFromFiles(num_it, 'MenorMed', 'MaiorMed', 'agradavel?', sector=sector))
       #all_res.append(ptestFromFiles(num_it, 'MenorMed', 'MaiorMed', 'agradavel?', sector=sector))

	print ">>>> Sector: ", sector
	for r in all_res:
	    print r[0]
	    for i, f in enumerate(r[-1]):
		print f[0], r[1][i]
		print 'pval', r[2][i]
		print
	    print '--'




#sampling qscores from single file
#df = pd.read_csv('geralRankAJ.dat', sep=' ', encoding='utf8')
#df = df.drop(['red', 'green', 'blue', 'hor', 'vert', 'diag'], axis=1)
#
#all_res = []
#
#all_res.append(ptest(df, 'Masculino', 'Feminino', 'agradavel?'))
#all_res.append(ptest(df, 'Masculino', 'Feminino', 'seguro?'))
#
#all_res.append(ptest(df, 'Jovem', 'Adulto', 'agradavel?'))
#all_res.append(ptest(df, 'Jovem', 'Adulto', 'seguro?'))
#
#all_res.append(ptest(df, 'Solteiro', 'Casado', 'agradavel?'))
#all_res.append(ptest(df, 'Solteiro', 'Casado', 'seguro?'))
#
#all_res.append(ptest(df, 'Baixa', 'Media', 'agradavel?'))
#all_res.append(ptest(df, 'Baixa', 'Media', 'seguro?'))
#
#all_res.append(ptest(df, 'Medio', 'Pos', 'agradavel?'))
#all_res.append(ptest(df, 'Medio', 'Pos', 'seguro?'))

#for bairro in ['catole', 'centro', 'liberdade']:
#	all_res = []
#
#	all_res.append(ptest(df, 'Masculino', 'Feminino', 'agradavel?', bairro=bairro))
#	all_res.append(ptest(df, 'Masculino', 'Feminino', 'seguro?', bairro=bairro))
#
#	all_res.append(ptest(df, 'Jovem', 'Adulto', 'agradavel?', bairro=bairro))
#	all_res.append(ptest(df, 'Jovem', 'Adulto', 'seguro?', bairro=bairro))
#
#	all_res.append(ptest(df, 'Solteiro', 'Casado', 'agradavel?', bairro=bairro))
#	all_res.append(ptest(df, 'Solteiro', 'Casado', 'seguro?', bairro=bairro))
#
#	all_res.append(ptest(df, 'Baixa', 'Media', 'agradavel?', bairro=bairro))
#	all_res.append(ptest(df, 'Baixa', 'Media', 'seguro?', bairro=bairro))
#
#	all_res.append(ptest(df, 'Medio', 'Pos', 'agradavel?', bairro=bairro))
#	all_res.append(ptest(df, 'Medio', 'Pos', 'seguro?', bairro=bairro))
#
#	if bairro == 'catole':
#		all_res.append(ptest(df, 'CCatole', 'NCCatole', 'agradavel?', bairro=bairro))
#		all_res.append(ptest(df, 'CCatole', 'NCCatole', 'seguro?', bairro=bairro))
#	elif bairro == 'centro':
#		all_res.append(ptest(df, 'CCentro', 'NCCentro', 'agradavel?', bairro=bairro))
#		all_res.append(ptest(df, 'CCentro', 'NCCentro', 'seguro?', bairro=bairro))
#	else:
#		all_res.append(ptest(df, 'CLiberdade', 'NCLiberdade', 'agradavel?', bairro=bairro))
#		all_res.append(ptest(df, 'CLiberdade', 'NCLiberdade', 'seguro?', bairro=bairro))
#
#	all_res.append(ptest(df, 'MenorMed', 'MaiorMed', 'agradavel?', bairro=bairro))
#	all_res.append(ptest(df, 'MenorMed', 'MaiorMed', 'seguro?', bairro=bairro))
#
#	print ">>>> Bairro: ", bairro
#	for r in all_res:
#	    print r[0]
#	    for i, f in enumerate(r[-1]):
#		print f[0], r[1][i]
#		print 'pval', r[2][i]
#		print
#	    print '--'
#
#df = pd.read_csv('geralSetoresAJ.dat', sep=' ', encoding='utf8')
#df = df.drop(['red', 'green', 'blue', 'hor', 'vert', 'diag'], axis=1)
#for setor in ['25040090500004', '250400905000013', '250400905000060', '250400905000062', '250400905000095', '250400905000089']:
#	all_res = []
#
#	all_res.append(ptest(df, 'Masculino', 'Feminino', 'agradavel?', setor=setor))
#	all_res.append(ptest(df, 'Masculino', 'Feminino', 'seguro?', setor=setor))
#
#	all_res.append(ptest(df, 'Jovem', 'Adulto', 'agradavel?', setor=setor))
#	all_res.append(ptest(df, 'Jovem', 'Adulto', 'seguro?', setor=setor))
#
#	all_res.append(ptest(df, 'Solteiro', 'Casado', 'agradavel?', setor=setor))
#	all_res.append(ptest(df, 'Solteiro', 'Casado', 'seguro?', setor=setor))
#
#	all_res.append(ptest(df, 'Baixa', 'Media', 'agradavel?', setor=setor))
#	all_res.append(ptest(df, 'Baixa', 'Media', 'seguro?', setor=setor))
#
#	all_res.append(ptest(df, 'Medio', 'Pos', 'agradavel?', setor=setor))
#	all_res.append(ptest(df, 'Medio', 'Pos', 'seguro?', setor=setor))
#
#	if setor == '250400905000060' or setor == '250400905000062':
#		all_res.append(ptest(df, 'CCatole', 'NCCatole', 'agradavel?', setor=setor))
#		all_res.append(ptest(df, 'CCatole', 'NCCatole', 'seguro?', setor=setor))
#	elif setor == '25040090500004' or setor == '250400905000013':
#		all_res.append(ptest(df, 'CCentro', 'NCCentro', 'agradavel?', setor=setor))
#		all_res.append(ptest(df, 'CCentro', 'NCCentro', 'seguro?', setor=setor))
#	else:
#		all_res.append(ptest(df, 'CLiberdade', 'NCLiberdade', 'agradavel?', setor=setor))
#		all_res.append(ptest(df, 'CLiberdade', 'NCLiberdade', 'seguro?', setor=setor))
#
        #all_res.append(ptest(df, 'MenorMed', 'MaiorMed', 'agradavel?', setor=setor))
       #all_res.append(ptest(df, 'MenorMed', 'MaiorMed', 'agradavel?', setor=setor))
#
#
#	print ">>>> Setor: ", setor
#	for r in all_res:
#	    print r[0]
#	    for i, f in enumerate(r[-1]):
#		print f[0], r[1][i]
#		print 'pval', r[2][i]
#		print
#	    print '--'
