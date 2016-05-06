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

def ptestFromFiles(num_it, question, neig=None, sector=None):
    
    questionsMap = {'agradavel?' : 'agrad%C3%A1vel?', 'seguro?' : 'seguro?'}

    #Original data file
    dfOrig = pd.read_csv('geralSetoresAJ.dat', sep=' ', encoding='utf8')
    dfOrig = dfOrig.drop(['red', 'green', 'blue', 'hor', 'vert', 'diag'], axis=1)

    dfOrig = dfOrig[dfOrig.values[:, 1] == question]

    if neig is not None:
	dfOrig = dfOrig[dfOrig['bairro'] == neig]
    if sector is not None:
	dfOrig = dfOrig[dfOrig['setor'] == int(sector)]

    #men = dfOrig[dfOrig['grupo'] == 'Masculino'].values[:, 2]#Input files are sorted according to image names, so the order of QScores retrieved is paired for all groups
    #wom = dfOrig[dfOrig['grupo'] == 'Feminino'].values[:, 2]
    #you = dfOrig[dfOrig['grupo'] == 'Jovem'].values[:, 2]
    #adu = dfOrig[dfOrig['grupo'] == 'Adulto'].values[:, 2]
    #low = dfOrig[dfOrig['grupo'] == 'Baixa'].values[:, 2]
    #hig = dfOrig[dfOrig['grupo'] == 'Media'].values[:, 2]
    #sin = dfOrig[dfOrig['grupo'] == 'Solteiro'].values[:, 2]
    #mar = dfOrig[dfOrig['grupo'] == 'Casado'].values[:, 2]
    #higS = dfOrig[dfOrig['grupo'] == 'Medio'].values[:, 2]
    #pos = dfOrig[dfOrig['grupo'] == 'Pos'].values[:, 2]

    knowCen = dfOrig[dfOrig['grupo'] == 'CCentro'].values[:, 2]
    nknowCen = dfOrig[dfOrig['grupo'] == 'NCCentro'].values[:, 2]
    knowLib = dfOrig[dfOrig['grupo'] == 'CLiberdade'].values[:, 2]
    nknowLib = dfOrig[dfOrig['grupo'] == 'NCLiberdade'].values[:, 2]
    knowCat = dfOrig[dfOrig['grupo'] == 'CCatole'].values[:, 2]
    nknowCat = dfOrig[dfOrig['grupo'] == 'NCCatole'].values[:, 2]

    functions = [
       ('Mean', abs_mean),
       ('Median', abs_median),
       ('Top10-Mean-Old', top10_abs_mean_old),
       ('Top10-Mean-Naza', top10_abs_mean_naza)]

    actual = np.zeros(len(functions)*3)#*5
    index = 0
    i = 0
    while index < len(actual):
		#actual[index] = functions[i][1](men, wom)
		#actual[index+1] = functions[i][1](you, adu)
		#actual[index+2] = functions[i][1](low, hig)
		#actual[index+3] = functions[i][1](sin, mar)
		#actual[index+4] = functions[i][1](higS, pos)
		#index = index + 5
		actual[index] = functions[i][1](knowCen, nknowCen)
		actual[index+1] = functions[i][1](knowLib, nknowLib)
		actual[index+2] = functions[i][1](knowCat, nknowCat)
		index = index + 3
		i = i + 1

    #R_gender = np.zeros(shape=(num_it, len(functions)))
    #R_marital = np.zeros(shape=(num_it, len(functions)))
    #R_age = np.zeros(shape=(num_it, len(functions)))
    #R_income = np.zeros(shape=(num_it, len(functions)))
    #R_educ = np.zeros(shape=(num_it, len(functions)))
    R_cen = np.zeros(shape=(num_it, len(functions)))
    R_lib = np.zeros(shape=(num_it, len(functions)))
    R_cat = np.zeros(shape=(num_it, len(functions)))

    #Sampled users files
    newQuestion = questionsMap[question]
    for it in xrange(1, num_it+1):
	df = pd.read_csv('samplesIds/geralSetoresAJ_'+str(it)+'.dat', sep=' ', encoding='utf8')
    	df = df[df.values[:, 1] == newQuestion]

	if neig is not None:
		df = df[df['bairro'] == neig]
	if sector is not None:
		df = df[df['setor'] == int(sector)]

#	men = df[df['grupo'] == 'Masculino'].values[:, 2]
#	wom = df[df['grupo'] == 'Feminino'].values[:, 2]
#	you = df[df['grupo'] == 'Jovem'].values[:, 2]
#	adu = df[df['grupo'] == 'Adulto'].values[:, 2]
#	low = df[df['grupo'] == 'Baixa'].values[:, 2]
#	hig = df[df['grupo'] == 'Media'].values[:, 2]
#	sin = df[df['grupo'] == 'Solteiro'].values[:, 2]
#	mar = df[df['grupo'] == 'Casado'].values[:, 2]
#	higS = df[df['grupo'] == 'Medio'].values[:, 2]
#	pos = df[df['grupo'] == 'Pos'].values[:, 2]

	knowCen = df[df['grupo'] == 'CCentro'].values[:, 2]
	nknowCen = df[df['grupo'] == 'NCCentro'].values[:, 2]
	knowLib = df[df['grupo'] == 'CLiberdade'].values[:, 2]
	nknowLib = df[df['grupo'] == 'NCLiberdade'].values[:, 2]
	knowCat = df[df['grupo'] == 'CCatole'].values[:, 2]
	nknowCat = df[df['grupo'] == 'NCCatole'].values[:, 2]
        
        for j in xrange(len(functions)):
            #R_gender[it-1][j] = functions[j][1](men, wom)
            #R_marital[it-1][j] = functions[j][1](sin, mar)
            #R_age[it-1][j] = functions[j][1](you, adu)
            #R_income[it-1][j] = functions[j][1](low, hig)
            #R_educ[it-1][j] = functions[j][1](higS, pos)
	    R_cen[it-1][j] = functions[j][1](knowCen, nknowCen)
	    R_lib[it-1][j] = functions[j][1](knowLib, nknowLib)
	    R_cat[it-1][j] = functions[j][1](knowCat, nknowCat)
    
#    pvals_gender = []
 #   pvals_age = []
  #  pvals_marital = []
   # pvals_income = []
    #pvals_educ = []
    pvals_cen = []
    pvals_lib = []
    pvals_cat = []
    index = 0
    i = 0

    while i < len(functions):
#	pvals_gender.append(float((R_gender[:, i] > actual[index]).sum()) / R_gender.shape[0])
#	pvals_age.append(float((R_age[:, i] > actual[index+1]).sum()) / R_age.shape[0])
#	pvals_income.append(float((R_income[:, i] > actual[index+2]).sum()) / R_income.shape[0])
#	pvals_marital.append(float((R_marital[:, i] > actual[index+3]).sum()) / R_marital.shape[0])
#	pvals_educ.append(float((R_educ[:, i] > actual[index+4]).sum()) / R_educ.shape[0])
	pvals_cen.append(float((R_cen[:, i] > actual[index]).sum()) / R_educ.shape[0])
	pvals_lib.append(float((R_lib[:, i] > actual[index+1]).sum()) / R_educ.shape[0])
	pvals_cat.append(float((R_cat[:, i] > actual[index+2]).sum()) / R_educ.shape[0])
	index = index + 3#5
	i = i + 1

    #gender = ('Masculino', 'Feminino', question), actual[0:len(actual):5], np.array(pvals_gender), functions
    #age = ('Jovem', 'Adulto', question), actual[1:len(actual):5], np.array(pvals_age), functions
    #income = ('Baixa', 'Media', question), actual[2:len(actual):5], np.array(pvals_income), functions
    #marital = ('Solteiro', 'Casado', question), actual[3:len(actual):5], np.array(pvals_marital), functions
    #educ = ('Medio', 'Pos', question), actual[4:len(actual):5], np.array(pvals_educ), functions
    centro = ('Centro', 'NCentro', question), actual[0:len(actual):3], np.array(pvals_cen), functions
    lib = ('Liberdade', 'NLiberdade', question), actual[0:len(actual):3], np.array(pvals_lib), functions
    cat = ('Catole', 'NCatole', question), actual[0:len(actual):3], np.array(pvals_cat), functions

    return centro, lib, cat #gender, age, marital, income, educ


#Using sample users files
num_it = 10000
all_res = []

#all_res.append(ptestFromFiles(num_it, 'agradavel?'))
#all_res.append(ptestFromFiles(num_it, 'seguro?'))

#print ">>>> General: "
#for r in all_res:
#for index in xrange(len(all_res)):
#  data = all_res[index]#All data for one question
 # for j in xrange(len(data)):
#	  r = all_res[index][j]
#	  print r[0]
#	  for i, f in enumerate(r[-1]):
#		print f[0], r[1][i]
#		print 'pval', r[2][i]
#		print
#	  print '--'

for neig in ['catole', 'centro', 'liberdade']:
	all_res = []

	all_res.append(ptestFromFiles(num_it, 'agradavel?', neig=neig))
	all_res.append(ptestFromFiles(num_it, 'seguro?', neig=neig))

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
	for index in xrange(len(all_res)):
	  data = all_res[index]#All data for one question
	  for j in xrange(len(data)):
		  r = all_res[index][j]
		  print r[0]
		  for i, f in enumerate(r[-1]):
			print f[0], r[1][i]
			print 'pval', r[2][i]
			print
		  print '--'

#for sector in ['25040090500004', '250400905000013', '250400905000060', '250400905000062', '250400905000095', '250400905000089']:
#	all_res = []
#
#	all_res.append(ptestFromFiles(num_it, 'agradavel?', sector=sector))
#	all_res.append(ptestFromFiles(num_it, 'seguro?', sector=sectorg))
#
#	print ">>>> Sector: ", sector
#	for index in xrange(len(all_res)):
#	  data = all_res[index]#All data for one question
#	  for j in xrange(len(data)):
#		  r = all_res[index][j]
#		  print r[0]
#		  for i, f in enumerate(r[-1]):
#			print f[0], r[1][i]
#			print 'pval', r[2][i]
#			print
#		  print '--'

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
