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
import scipy.integrate as integrate

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


def standard_normal(x):
	std = 1.0
	mean = 0.0
	return (1.0 / np.sqrt( 2.0 * np.pi * (std**2.0)) ) * np.exp(- ( (x - mean)**2.0/(2.0 * (std**2.0)) ) ) 

def deMoivre_funnel(current_val, i, data):
	values = []
	num_of_values = 0.0
	for prop in data:
		values.append(data[prop][i])
		num_of_values = num_of_values + 1.0

	std_error = np.std(values) / np.sqrt(num_of_values)
	zs = (current_val - np.mean(values)) / std_error
	
	integrate_result = integrate.quad(standard_normal, 0, zs)
	p_de_moivre = 1.0 - ( 2.0 * integrate_result[0] )
	#print str(std_error) + "\t" + str(zs) + "\t" + str(i) + "\t" + str(integrate_result) + "\t" + str(p_de_moivre)
	return p_de_moivre
	

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

  #normal_fit = {"all" : [4.68814353, 0.64067694], u'R._Cristina_Proc\xf3pio_Silva' : [4.97966875, 0.71104919], u'R._Maciel_Pinheiro' : [4.77777896, 0.22856043], u'R._In\xe1cio_Marqu\xeas_da_Silva': [4.71353096, 0.54189458], u'R._Manoel_Pereira_de_Ara\xfajo': [3.67248457, 0.18353610], u'Av._Mal._Floriano_Peixoto': [ 4.95739065, 0.32222894], u'R._Ed\xe9sio_Silva': [4.71109467, 0.46001726]}
  
  #Bayesian surprise is the KL divergence from prior to posterior
  kl = 0
  diffs = [0,0,0]
  sum_diffs = [0,0,0]

  #Integration using python (for De moivre) - https://docs.scipy.org/doc/scipy/reference/tutorial/integrate.html

  for i in range(0, num_of_points):

    sum_diffs = [0,0,0]

    #Calculate per state surprise
    for prop in data:

      #norm_data = normal_fit[prop]
      #norm_estimate = np.random.normal(loc=norm_data[0], scale=norm_data[1])

      #avg_street  = average_street(prop, num_of_points)#For whole street
      #total_street = sumU_street(prop, num_of_points)
      #avg_num = average_num(prop, i)#median_num;//For current point
      #total_num = sumU_num(prop, i)
      #print ">>> Evaluating " + prop + "\t" + str(i)
      #Estimate P(D|M) as 1 - |O - E|
      #uniform
      #diffs[0] = ((data[prop][i]/total_street) - (avg_street/total_street))
      #pDMs[0] = 1 - abs(diffs[0])
      pDMs[0] = 1.0 / num_of_points * ( num_of_points * deMoivre_funnel(data[prop][i], i, data) )
      #Average per num
      #diffs[1] = ((data[prop][i]/total_street) - (avg_num/total_street))
      pDMs[1] = 1.0 / num_of_points * ( num_of_points * deMoivre_funnel(data[prop][i], i, data) )
      #normal
      #diffs[2] = ((data[prop][i]/total_street) - (norm_estimate/total_street))
      pDMs[2] = 1.0 / num_of_points * ( num_of_points * deMoivre_funnel(data[prop][i], i, data) )

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
        kl = kl + pMDs[j] * (np.log( pMDs[j] / pMs[j])/np.log(2))
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

	if len(sys.argv) < 2:
		print "Uso: <arquivo de entrada>"
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

	data = {}
	num_of_points = 18
	for index, row in input_data.iterrows():
		 data[row['State']] = [row['1981'], row['1982'], row['1983'], row['1984'], row['1985'], row['1986'], row['1987'], row['1988'], row['1989'], row['1990'], row['1991'], row['1992'], row['1993'], row['1994'], row['1995'], row['1996'], row['1997'], row['1998']]

	#Creating variables to store values over iterations
	all_surprise = {}
	all_uniform = {}
	all_base = {}
	surprise_summary = {}
	uniform_summary = {}
	base_summary = {}

	for prop in input_data['State']:
		all_surprise[prop] = [[] for x in range(num_of_points)]
		all_uniform[prop] = [[] for x in range(num_of_points)]
		all_base[prop] = [[] for x in range(num_of_points)]

		surprise_summary[prop] = [[] for x in range(num_of_points)]
		uniform_summary[prop] = [[] for x in range(num_of_points)]
		base_summary[prop] = [[] for x in range(num_of_points)]


	#Calculations of surprise values and storing calculus results
	result = calcSurprise(num_of_points)
	#print str(result)
	surprise_data = result[0]
	uniform_data = result[1]
	base_data = result[2]

	print str(surprise_data)

	for prop in input_data['State']:
		for i in range(0, num_of_points):
			all_surprise[prop][i].append(surprise_data[prop][i])
			all_uniform[prop][i].append(uniform_data[prop][i])
			all_base[prop][i].append(base_data[prop][i])

	#Calculating summaries
	#for prop in input_data['State']:
	#	for i in range(0, num_of_points):
	#		surprise_summary[prop][i] = np.mean(all_surprise[prop][i])
	#		uniform_summary[prop][i] =  np.mean(all_uniform[prop][i])
	#		base_summary[prop][i] =  np.mean(all_base[prop][i])

	#Printing surprise values summaries
	for prop in surprise_data:
		print prop + "," + ','.join(str(i) for i in surprise_data[prop])

  

