# coding=utf-8
# Calculates surprise values according to street scores
import sys
from sets import Set
import random
import numpy
import json
import csv
import pandas as pd
import numpy as np

def average_num(prop, i):
	#Average scores for current street point.
	sum = 0
	n = 0

	int_part = i/4

	for i in range(int_part * 4, (int_part+1) * 4):
		sum = sum + data[prop][i]
		n = n + 1

	return sum/n


def median_num(prop, i):
	#Median score for current street point.
	current_values = []
	int_part = i/4

	for i in range(int_part * 4, (int_part+1) * 4):
		current_values.append(data[prop][i]);
	
	return np.median(current_values)

def average_street(prop, num_of_points):
	#Average scores for current street.
	sum = 0
	n = 0
  
	for i in range(0, num_of_points):
		sum = sum + data[prop][i]
		n = n + 1
	return sum/n

def sumU_num(prop, i):
	#Sum scores for current street.
	sum = 0
	int_part = i/4

 	for i in range(int_part * 4, (int_part+1) * 4):
		sum = sum + data[prop][i]
	return sum

def sumU_street(prop, num_of_points):
	#Sum scores for current street.
	sum = 0
 	for i in range(0, num_of_points):
		sum = sum + data[prop][i]
	return sum

def KL(pmd,pm):
  return pmd * (np.log(pmd / pm) / np.log(2))


def deMoivre_funnel(all_points):
	std_error = np.std(all_points) / np.sqrt(len(all_points))
	
	

def calcSurprise(num_of_points):
  
  uniform_data = {}
  surprise_data = {}
  base_data = {}

  for prop in data:
	surprise_data[prop] = [0 for x in range(num_of_points)]
	uniform_data[prop] = [0 for x in range(num_of_points)]
	base_data[prop] = [0 for x in range(num_of_points)]

  #Start with equiprobably P(M)s
  #Initially, everything is equiprobable.
  pMs =[(1.0/3),(1.0/3),(1.0/3)]

  uniform_pM = [pMs[0]]
  boom_pM = [pMs[1]]
  bust_pM = [pMs[2]]
  
  pDMs = [0,0,0]
  pMDs = [0,0,0]
  avg = 0
  total = 0

  normal_fit = {"all" : [4.68814353, 0.64067694], u'R._Cristina_Proc\xf3pio_Silva' : [4.97966875, 0.71104919], u'R._Maciel_Pinheiro' : [4.77777896, 0.22856043], u'R._In\xe1cio_Marqu\xeas_da_Silva': [4.71353096, 0.54189458], u'R._Manoel_Pereira_de_Ara\xfajo': [3.67248457, 0.18353610], u'Av._Mal._Floriano_Peixoto': [ 4.95739065, 0.32222894], u'R._Ed\xe9sio_Silva': [4.71109467, 0.46001726]}
  
  #Bayesian surprise is the KL divergence from prior to posterior
  kl = 0
  diffs = [0,0,0]
  sum_diffs = [0,0,0]

  #Integration using python (for De moivre) - https://docs.scipy.org/doc/scipy/reference/tutorial/integrate.html

  for prop in data:

    sum_diffs = [0,0,0]

    for i in range(0, num_of_points):
    #Calculate per street surprise

      norm_data = normal_fit[prop]
      norm_estimate = np.random.normal(loc=norm_data[0], scale=norm_data[1])

      avg_street  = average_street(prop, num_of_points)#For whole street
      total_street = sumU_street(prop, num_of_points)
      avg_num = median_num(prop, i)#average_num;//For current point
      total_num = sumU_num(prop, i)
      
      #Estimate P(D|M) as 1 - |O - E|
      #uniform
      diffs[0] = ((data[prop][i]/total_street) - (avg_street/total_street))
      pDMs[0] = 1 - abs(diffs[0])
      #Average per num
      diffs[1] = ((data[prop][i]/total_street) - (avg_num/total_street))
      pDMs[1] = 1 - abs(diffs[1])
      #normal
      diffs[2] = ((data[prop][i]/total_street) - (norm_estimate/total_street))
      pDMs[2] = 1 - abs(diffs[2])
      
      #Estimate P(M|D)
      #uniform
      pMDs[0] = pMs[0]*pDMs[0];
      pMDs[1] = pMs[1]*pDMs[1];
      pMDs[2] = pMs[2]*pDMs[2];
      
      
      #Surprise is the sum of KL divergance across model space
      #Each model also gets a weighted "vote" on what the sign should be
      kl = 0
      voteSum = 0
      for j in range(0, len(pMDs)):
	if pMDs[j] != 0 and pMs[j] == 0:
		raise Exception("DKL is undefined que P(i) != 0 and Q(i) == 0")
	if pMDs[j] == 0:
		current_kl = 0.0
	else:
		current_kl = pMDs[j] * (np.log( pMDs[j] / pMs[j])/np.log(2))
        kl = kl + current_kl
        voteSum = voteSum + diffs[j]*pMs[j]
        sum_diffs[j] = sum_diffs[j] + abs(diffs[j])
      
      if voteSum >= 0:
	surprise_data[prop][i] = abs(kl) 
      else: 
	surprise_data[prop][i] = -1 * abs(kl)

      uniform_data[prop][i] = pMs[0]
      base_data[prop][i] = pMs[1]
    
    #Now lets globally update our model belief.
    for j in range(0, len(pMs)):
      pDMs[j] = 1 - 0.5 * sum_diffs[j]
      pMDs[j] = pMs[j] * pDMs[j]
      pMs[j] = pMDs[j]
    
    #Normalize
    summ = np.sum(pMs)
    for j in range(0, len(pMs)):
      pMs[j] = pMs[j] / summ
    
    uniform_pM.append(pMs[0])
    boom_pM.append(pMs[1])
    bust_pM.append(pMs[2])

  return [surprise_data, uniform_data, base_data]

if __name__ == "__main__":

	if len(sys.argv) < 3:
		print "Uso: <arquivo com scores a considerar> <quantidade de pontos de coleta na rua>"
		sys.exit(1)

	#Init algorithm
	data = {}
	surprise_data = {}
	uniform = {}
	boom = {}
	bust = {}

	max_street = {}
	min_street = {}

	input_data = pd.read_table(sys.argv[1], sep=',', encoding='utf8', header=0)
	num_of_points = int(sys.argv[2])

	data = {}
	for index, row in input_data.iterrows():
		if num_of_points == 20:
			 data[row['street']] = [row['num1'], row['num2'], row['num3'], row['num4'], row['num5'], row['num6'], row['num7'], row['num8'], row['num9'], row['num10'], row['num11'], row['num12'], row['num13'], row['num14'], row['num15'], row['num16'], row['num17'], row['num18'], row['num19'], row['num20']]
		else:
			 data[row['street']] = [row['num1'], row['num2'], row['num3'], row['num4'], row['num5'], row['num6'], row['num7'], row['num8'], row['num9'], row['num10'], row['num11'], row['num12'], row['num13'], row['num14'], row['num15'], row['num16'], row['num17'], row['num18'], row['num19'], row['num20'], row['num21'], row['num22'], row['num23'], row['num24'], row['num25'], row['num26'], row['num27'], row['num28'], row['num29'], row['num30'], row['num31'], row['num32'], row['num33'], row['num34'], row['num35'], row['num36'], row['num37'], row['num38'], row['num39'], row['num40']]

	print str(data)

	#Creating variables to store values over iterations
	all_surprise = {}
	all_uniform = {}
	all_base = {}
	surprise_summary = {}
	uniform_summary = {}
	base_summary = {}

	for prop in input_data['street']:
		all_surprise[prop] = [[] for x in range(num_of_points)]
		all_uniform[prop] = [[] for x in range(num_of_points)]
		all_base[prop] = [[] for x in range(num_of_points)]

		surprise_summary[prop] = [[] for x in range(num_of_points)]
		uniform_summary[prop] = [[] for x in range(num_of_points)]
		base_summary[prop] = [[] for x in range(num_of_points)]


	#Multiple calculations of surprise values and storing calculus results
	for i in range(0, 10000):
	  result = calcSurprise(num_of_points)
	  #print str(result)
	  surprise_data = result[0]
	  uniform_data = result[1]
	  base_data = result[2]

	  for prop in input_data['street']:
		for i in range(0, num_of_points):
			all_surprise[prop][i].append(surprise_data[prop][i])
			all_uniform[prop][i].append(uniform_data[prop][i])
			all_base[prop][i].append(base_data[prop][i])

	#Calculating summaries
	for prop in input_data['street']:
		for i in range(0, num_of_points):
			surprise_summary[prop][i] = np.mean(all_surprise[prop][i])
			uniform_summary[prop][i] =  np.mean(all_uniform[prop][i])
			base_summary[prop][i] =  np.mean(all_base[prop][i])

	#Printing surprise values summaries
	for prop in surprise_summary:
		print prop + "," + ','.join(str(i) for i in surprise_summary[prop])

  

