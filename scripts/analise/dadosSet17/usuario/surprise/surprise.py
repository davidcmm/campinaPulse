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

def average_street(prop):
	#Average scores for current street.
	sum = 0
	n = 0
  
	for i in range(0, 20):
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

def sumU_street(prop):
	#Sum scores for current street.
	sum = 0
 	for i in range(0, 20):
		sum = sum + data[prop][i]
	return sum

def KL(pmd,pm):
  return pmd * (np.log(pmd / pm) / np.log(2))


def calcSurprise():
  
  uniformData = {}
  surpriseData = {}
  baseData = {}

  for prop in data:
	surpriseData[prop] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	uniformData[prop] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	baseData[prop] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

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

  normal_fit = {"all" : [4.68088452, 0.62863384], u'R._Cristina_Proc\xf3pio_Silva' : [4.92394878, 0.62351231], u'R._Maciel_Pinheiro' : [4.84016850, 0.28028584], u'R._In\xe1cio_Marqu\xeas_da_Silva': [4.84231882, 0.46291311], u'R._Manoel_Pereira_de_Ara\xfajo': [3.65700904, 0.19215810], u'Av._Mal._Floriano_Peixoto': [ 5.04950088, 0.34203741], u'R._Ed\xe9sio_Silva': [4.77236112, 0.48215430]}
  
  #Bayesian surprise is the KL divergence from prior to posterior
  kl = 0
  diffs = [0,0,0]
  sumDiffs = [0,0,0]

  for i in range(0, 20):

    sumDiffs = [0,0,0]

    #Calculate per state surprise
    for prop in data:

      norm_data = normal_fit[prop]
      norm_estimate = np.random.normal(loc=norm_data[0], scale=norm_data[1])

      avg_street  = average_street(prop)#For whole street
      total_street = sumU_street(prop)
      avg_num = median_num(prop, i)#average_num(prop, i);//For current point
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
        kl = kl + pMDs[j] * (np.log( pMDs[j] / pMs[j])/np.log(2))
        voteSum = voteSum + diffs[j]*pMs[j]
        sumDiffs[j] = sumDiffs[j] + abs(diffs[j])
      
      if voteSum >= 0:
	surpriseData[prop][i] = abs(kl) 
      else: 
	surpriseData[prop][i] = -1 * abs(kl)

      uniformData[prop][i] = pMs[0]
      baseData[prop][i] = pMs[1]
    
    #Now lets globally update our model belief.
    for j in range(0, len(pMs)):
      pDMs[j] = 1 - 0.5 * sumDiffs[j]
      pMDs[j] = pMs[j] * pDMs[j]
      pMs[j] = pMDs[j]
    
    #Normalize
    summ = np.sum(pMs)
    for j in range(0, len(pMs)):
      pMs[j] = pMs[j] / summ
    
    uniform_pM.append(pMs[0])
    boom_pM.append(pMs[1])
    bust_pM.append(pMs[2])

  return [surpriseData, uniformData, baseData]


#Init algorithm
data = {}
surpriseData = {}
uniform = {}
boom = {}
bust = {}

max_street = {}
min_street = {}

input_data = pd.read_table("street_scores.csv", sep=',', encoding='utf8', header=0)
data = {}
for index, row in input_data.iterrows():
	 data[row['street']] = [row['num1'], row['num2'], row['num3'], row['num4'], row['num5'], row['num6'], row['num7'], row['num8'], row['num9'], row['num10'], row['num11'], row['num12'], row['num13'], row['num14'], row['num15'], row['num16'], row['num17'], row['num18'], row['num19'], row['num20']]

print str(data)

#Creating variables to store values over iterations
allSurprise = {}
allUniform = {}
allBase = {}
surpriseSummary = {}
uniformSummary = {}
baseSummary = {}

for prop in input_data['street']:
	allSurprise[prop] = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [] ]
	allUniform[prop] = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [] ]
	allBase[prop] = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [] ]

	surpriseSummary[prop] = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [] ]
	uniformSummary[prop] = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [] ]
	baseSummary[prop] = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [] ]


#Multiple calculations of surprise values and storing calculus results
for i in range(0,500):
  result = calcSurprise()
  surpriseData = result[0]
  uniformData = result[1]
  baseData = result[2]

  for prop in input_data['street']:
	for i in range(0,20):
		allSurprise[prop][i].append(surpriseData[prop][i])
		allUniform[prop][i].append(uniformData[prop][i])
		allBase[prop][i].append(baseData[prop][i])

#Calculating summaries
for prop in input_data['street']:
	for i in range(0,20):
		surpriseSummary[prop][i] = np.mean(allSurprise[prop][i])
		uniformSummary[prop][i] =  np.mean(allUniform[prop][i])
		baseSummary[prop][i] =  np.mean(allBase[prop][i])

#Printing surprise values summaries
for prop in surpriseSummary:
	print prop + "," + ','.join(str(i) for i in surpriseSummary[prop])

  

