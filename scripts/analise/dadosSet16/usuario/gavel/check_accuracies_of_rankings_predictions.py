# coding=utf-8
# Test predictions on testing data for each ranking strategy

import csv
import math

import sys
from sets import Set
import random
import numpy
import json
import pandas as pd

threshold = 0.01
possibleQuestions = ["agrad%C3%A1vel?", "seguro?"]
left = 'Left'
right = 'Right'
notKnown = 'NotKnown'
completeTie = 'equal'

def build_qscore_rankings(index):
	data = pd.read_table("ranking_predictions/all_qscore_80_"+str(index)+".dat", sep='\s+', encoding='utf8', header=None)
	pleasant = data[data.loc[:,0] == "agrad%C3%A1vel?"].sort(columns=[2], ascending=True).reset_index(drop=True)
	safe = data[data.loc[:,0] == "seguro?"].sort(columns=[2], ascending=True).reset_index(drop=True)

	#print("QScore " + str(pleasant.shape) + "\t" + str(safe.shape))

	return {possibleQuestions[0] : pleasant, possibleQuestions[1] : safe}

def build_maxdiff_rankings(index):
	data = pd.read_table("ranking_predictions/all.dat-maxdiff_80_"+str(index), sep='\s+', encoding='utf8', header=None)
	pleasant = data[data.loc[:,0] == "agrad%C3%A1vel?"].sort(columns=[2], ascending=True).reset_index(drop=True)
	safe = data[data.loc[:,0] == "seguro?"].sort(columns=[2], ascending=True).reset_index(drop=True)

	#print("Maxdiff " + str(pleasant.shape) + "\t" + str(safe.shape))

	return {possibleQuestions[0] : pleasant, possibleQuestions[1] : safe}

def build_elo_rankings(index):
	data = pd.read_table("ranking_predictions/all_elo_80_10_"+str(index)+".dat", sep='\s+', encoding='utf8', header=None)
	pleasant_10 = data[data.loc[:,0] == "agrad%C3%A1vel?"].sort(columns=[2], ascending=True).reset_index(drop=True)
	safe_10 = data[data.loc[:,0] == "seguro?"].sort(columns=[2], ascending=True).reset_index(drop=True)

	#print("Elo " + str(pleasant_10.shape) + "\t" + str(safe_10.shape))

	data = pd.read_table("ranking_predictions/all_elo_80_20_"+str(index)+".dat", sep='\s+', encoding='utf8', header=None)
	pleasant_20 = data[data.loc[:,0] == "agrad%C3%A1vel?"].sort(columns=[2], ascending=True).reset_index(drop=True)
	safe_20 = data[data.loc[:,0] == "seguro?"].sort(columns=[2], ascending=True).reset_index(drop=True)

	#print("Elo " + str(pleasant_20.shape) + "\t" + str(safe_20.shape))

	data = pd.read_table("ranking_predictions/all_elo_80_40_"+str(index)+".dat", sep='\s+', encoding='utf8', header=None)
	pleasant_40 = data[data.loc[:,0] == "agrad%C3%A1vel?"].sort(columns=[2], ascending=True).reset_index(drop=True)
	safe_40 = data[data.loc[:,0] == "seguro?"].sort(columns=[2], ascending=True).reset_index(drop=True)

	#print("Elo " + str(pleasant_40.shape) + "\t" + str(safe_40.shape))

	return {"10" : {possibleQuestions[0] : pleasant_10, possibleQuestions[1] : safe_10}, "20" :  {possibleQuestions[0] : pleasant_20, possibleQuestions[1] : safe_20}, "40" : {possibleQuestions[0] : pleasant_40, possibleQuestions[1] : safe_40}}
	
def build_crowdbt_rankings(index):
	data = pd.read_table("ranking_predictions/all_crowdbt_80-lam01-gam01_"+str(index)+".dat", sep='\s+', encoding='utf8', header=None)
	pleasant_01 = data[data.loc[:,0] == "agrad%C3%A1vel?"].sort(columns=[2], ascending=True).reset_index(drop=True)
	safe_01 = data[data.loc[:,0] == "seguro?"].sort(columns=[2], ascending=True)

	#print("gavel " + str(pleasant_01.shape) + "\t" + str(safe_01.shape))

	data = pd.read_table("ranking_predictions/all_crowdbt_80-lam1-gam01_"+str(index)+".dat", sep='\s+', encoding='utf8', header=None)
	pleasant_1 = data[data.loc[:,0] == "agrad%C3%A1vel?"].sort(columns=[2], ascending=True).reset_index(drop=True)
	safe_1 = data[data.loc[:,0] == "seguro?"].sort(columns=[2], ascending=True)

	#print("gavel " + str(pleasant_1.shape) + "\t" + str(safe_1.shape))

	return {"01" : {possibleQuestions[0] : pleasant_01, possibleQuestions[1] : safe_01}, "1" :  {possibleQuestions[0] : pleasant_1, possibleQuestions[1] : safe_1}}

def check_ranking_prediction(current_ranking, photo1, photo2, counters, tie=False):
	index1 = current_ranking.loc[current_ranking.loc[:,1] == photo1].index[0]
	index2 = current_ranking.loc[current_ranking.loc[:,1] == photo2].index[0]

	#if abs(current_ranking.loc[current_ranking.loc[:,1] == photo1][1] - current_ranking.loc[current_ranking.loc[:,1] == photo2][2]) > threshold:
	#print(photo1+"\t"+photo2+"\t"+str(index1)+"\t"+str(index2))
	if tie:
		print ">>>> Não estamos considerando empates agora"	
	else:
		if index1 > index2: 
			counters[0] = counters[0] + 1
		elif index1 < index2:
			counters[3] = counters[3] + 1
	#else:
	#	if tie:
	#		counters[0] = counters[0] + 1
	#	else:
	#		counters[3] = counters[3] + 1
		
	return counters

def read_test_data(tasksDefinitions, elo, maxdiff, qscore, crowdbt, qscore_counters, maxdiff_counters, crowdbt_counters, elo_counters, index):
	lines = open("../../backupBanco/ranking_predictions/run_20_"+str(index)+".csv", "r").readlines()

	#Reading from pybossa task-run CSV
	for line in lines:
		lineData = line.split("+")

		executionID = lineData[0].strip(' \t\n\r"')
		taskID = lineData[3].strip(' \t\n\r"')
		userAnswer = lineData[9].strip(' \t\n\r"')

		#It is a new vote, read tasks definition from JSON!
		if executionID[0].lower() == 'n':
			data = json.loads(userAnswer)
			
			if data['question'].strip(' \t\n\r"') == "agradavel":
				question = possibleQuestions[0]
			else:
				question = possibleQuestions[1]

			photo1 = data['theMost'].strip(' \t\n\r"')
			photo2 = data['theLess'].strip(' \t\n\r"')
			is_tie = photo1

			taskDef = tasksDefinitions[taskID]
			photos = Set( [taskDef['url_c'].strip(' \t\n\r"'), taskDef['url_b'].strip(' \t\n\r"'), taskDef['url_a'].strip(' \t\n\r"'), taskDef['url_d'].strip(' \t\n\r"')] )
			if is_tie != completeTie:#Review this!
				photos.remove(photo1)
				photos.remove(photo2)
			else:
				photo1 = photos.pop()
				photo2 = photos.pop()
			
			photo3 = photos.pop()
			photo4 = photos.pop()

			#Comparing votes!
			if is_tie != completeTie:
				#Photo1 x Photo2
				#print(">>>> Photo1 x Photo2")
				#print("Max diff")
				current_ranking = maxdiff[question]
				counters = maxdiff_counters[question]
				maxdiff_counters[question] = check_ranking_prediction(current_ranking, photo1, photo2, counters)	

				#print("Qscore")
				current_ranking = qscore[question]
				counters = qscore_counters[question]
				qscore_counters[question] = check_ranking_prediction(current_ranking, photo1, photo2, counters)
	
				#print("Elo 10")
				current_ranking = elo["10"][question]
				counters = elo_counters["10"][question]
				elo_counters["10"][question] = check_ranking_prediction(current_ranking, photo1, photo2, counters)
				#print("Elo 20")
				current_ranking = elo["20"][question]
				counters = elo_counters["20"][question]
				elo_counters["20"][question] = check_ranking_prediction(current_ranking, photo1, photo2, counters)
				#print("Elo 40")
				current_ranking = elo["40"][question]
				counters = elo_counters["40"][question]
				elo_counters["40"][question] = check_ranking_prediction(current_ranking, photo1, photo2, counters)

				#print("Crowdbt 01")
				current_ranking = crowdbt["01"][question]
				counters = crowdbt_counters["01"][question]
				crowdbt_counters["01"][question] = check_ranking_prediction(current_ranking, photo1, photo2, counters)				
				#print("Crowdbt 1")
				current_ranking = crowdbt["1"][question]
				counters = crowdbt_counters["1"][question]
				crowdbt_counters["1"][question] = check_ranking_prediction(current_ranking, photo1, photo2, counters)	

				#Photo1 x Photo3
				current_ranking = maxdiff[question]
				counters = maxdiff_counters[question]
				maxdiff_counters[question] = check_ranking_prediction(current_ranking, photo1, photo3, counters)	

				current_ranking = qscore[question]
				counters = qscore_counters[question]
				qscore_counters[question] = check_ranking_prediction(current_ranking, photo1, photo3, counters)
	
				current_ranking = elo["10"][question]
				counters = elo_counters["10"][question]
				elo_counters["10"][question] = check_ranking_prediction(current_ranking, photo1, photo3, counters)
				current_ranking = elo["20"][question]
				counters = elo_counters["20"][question]
				elo_counters["20"][question] = check_ranking_prediction(current_ranking, photo1, photo3, counters)
				current_ranking = elo["40"][question]
				counters = elo_counters["40"][question]
				elo_counters["40"][question] = check_ranking_prediction(current_ranking, photo1, photo3, counters)

				current_ranking = crowdbt["01"][question]
				counters = crowdbt_counters["01"][question]
				crowdbt_counters["01"][question] = check_ranking_prediction(current_ranking, photo1, photo3, counters)				
				current_ranking = crowdbt["1"][question]
				counters = crowdbt_counters["1"][question]
				crowdbt_counters["1"][question] = check_ranking_prediction(current_ranking, photo1, photo3, counters)

				#Photo1 x Photo4
				current_ranking = maxdiff[question]
				counters = maxdiff_counters[question]
				maxdiff_counters[question] = check_ranking_prediction(current_ranking, photo1, photo4, counters)	

				current_ranking = qscore[question]
				counters = qscore_counters[question]
				qscore_counters[question] = check_ranking_prediction(current_ranking, photo1, photo4, counters)
	
				current_ranking = elo["10"][question]
				counters = elo_counters["10"][question]
				elo_counters["10"][question] = check_ranking_prediction(current_ranking, photo1, photo4, counters)
				current_ranking = elo["20"][question]
				counters = elo_counters["20"][question]
				elo_counters["20"][question] = check_ranking_prediction(current_ranking, photo1, photo4, counters)
				current_ranking = elo["40"][question]
				counters = elo_counters["40"][question]
				elo_counters["40"][question] = check_ranking_prediction(current_ranking, photo1, photo4, counters)

				current_ranking = crowdbt["01"][question]
				counters = crowdbt_counters["01"][question]
				crowdbt_counters["01"][question] = check_ranking_prediction(current_ranking, photo1, photo4, counters)				
				current_ranking = crowdbt["1"][question]
				counters = crowdbt_counters["1"][question]
				crowdbt_counters["1"][question] = check_ranking_prediction(current_ranking, photo1, photo4, counters)

				#Photo2 x Photo3
				current_ranking = maxdiff[question]
				counters = maxdiff_counters[question]
				maxdiff_counters[question] = check_ranking_prediction(current_ranking, photo3, photo2, counters)	

				current_ranking = qscore[question]
				counters = qscore_counters[question]
				qscore_counters[question] = check_ranking_prediction(current_ranking, photo3, photo2, counters)
	
				current_ranking = elo["10"][question]
				counters = elo_counters["10"][question]
				elo_counters["10"][question] = check_ranking_prediction(current_ranking, photo3, photo2, counters)
				current_ranking = elo["20"][question]
				counters = elo_counters["20"][question]
				elo_counters["20"][question] = check_ranking_prediction(current_ranking, photo3, photo2, counters)
				current_ranking = elo["40"][question]
				counters = elo_counters["40"][question]
				elo_counters["40"][question] = check_ranking_prediction(current_ranking, photo3, photo2, counters)

				current_ranking = crowdbt["01"][question]
				counters = crowdbt_counters["01"][question]
				crowdbt_counters["01"][question] = check_ranking_prediction(current_ranking, photo3, photo2, counters)				
				current_ranking = crowdbt["1"][question]
				counters = crowdbt_counters["1"][question]
				crowdbt_counters["1"][question] = check_ranking_prediction(current_ranking, photo3, photo2, counters)

				#Photo2 x Photo4
				current_ranking = maxdiff[question]
				counters = maxdiff_counters[question]
				maxdiff_counters[question] = check_ranking_prediction(current_ranking, photo4, photo2, counters)	

				current_ranking = qscore[question]
				counters = qscore_counters[question]
				qscore_counters[question] = check_ranking_prediction(current_ranking, photo4, photo2, counters)
	
				current_ranking = elo["10"][question]
				counters = elo_counters["10"][question]
				elo_counters["10"][question] = check_ranking_prediction(current_ranking, photo4, photo2, counters)
				current_ranking = elo["20"][question]
				counters = elo_counters["20"][question]
				elo_counters["20"][question] = check_ranking_prediction(current_ranking, photo4, photo2, counters)
				current_ranking = elo["40"][question]
				counters = elo_counters["40"][question]
				elo_counters["40"][question] = check_ranking_prediction(current_ranking, photo4, photo2, counters)

				current_ranking = crowdbt["01"][question]
				counters = crowdbt_counters["01"][question]
				crowdbt_counters["01"][question] = check_ranking_prediction(current_ranking, photo4, photo2, counters)				
				current_ranking = crowdbt["1"][question]
				counters = crowdbt_counters["1"][question]
				crowdbt_counters["1"][question] = check_ranking_prediction(current_ranking, photo4, photo2, counters)

				#Photo3 x Photo4
				current_ranking = maxdiff[question]
				counters = maxdiff_counters[question]
				maxdiff_counters[question] = check_ranking_prediction(current_ranking, photo4, photo3, counters, True)	

				current_ranking = qscore[question]
				counters = qscore_counters[question]
				qscore_counters[question] = check_ranking_prediction(current_ranking, photo4, photo3, counters, True)
	
				current_ranking = elo["10"][question]
				counters = elo_counters["10"][question]
				elo_counters["10"][question] = check_ranking_prediction(current_ranking, photo4, photo3, counters, True)
				current_ranking = elo["20"][question]
				counters = elo_counters["20"][question]
				elo_counters["20"][question] = check_ranking_prediction(current_ranking, photo4, photo3, counters, True)
				current_ranking = elo["40"][question]
				counters = elo_counters["40"][question]
				elo_counters["40"][question] = check_ranking_prediction(current_ranking, photo4, photo3, counters, True)

				current_ranking = crowdbt["01"][question]
				counters = crowdbt_counters["01"][question]
				crowdbt_counters["01"][question] = check_ranking_prediction(current_ranking, photo4, photo3, counters, True)				
				current_ranking = crowdbt["1"][question]
				counters = crowdbt_counters["1"][question]
				crowdbt_counters["1"][question] = check_ranking_prediction(current_ranking, photo4, photo3, counters, True)

			else:
				print(">>>>> Empates não considerados por enquanto")
				#votes[question][photo1][photo2].add(notKnown)
				#votes[question][photo1][photo3].add(notKnown)
				#votes[question][photo1][photo4].add(notKnown)
				#votes[question][photo2][photo3].add(notKnown)
				#votes[question][photo2][photo4].add(notKnown)
				#votes[question][photo3][photo4].add(notKnown)
				
		else:#Old-fashioned way of capturing votes
			#In user answers that contain profile information, jump to comparison
			if userAnswer[0] == '{':
				index = userAnswer.find("Qual")
				if index == -1:
					raise Exception("Line with profile does not contain question: " + userAnswer)
				userAnswer = userAnswer[index:].split(" ")
			else:
				userAnswer = userAnswer.split(" ")

			question = userAnswer[5].strip(' \t\n\r"')
			answer = userAnswer[6].strip(' \t\n\r"')
			photo1 = userAnswer[7].strip(' \t\n\r"')
			photo2 = userAnswer[8].strip(' \t\n\r"')

			#Checking answers
			if answer == left:
				#Photo1 x Photo2
				current_ranking = maxdiff[question]
				counters = maxdiff_counters[question]
				maxdiff_counters[question] = check_ranking_prediction(current_ranking, photo1, photo2, counters)	

				current_ranking = qscore[question]
				counters = qscore_counters[question]
				qscore_counters[question] = check_ranking_prediction(current_ranking, photo1, photo2, counters)
	
				current_ranking = elo["10"][question]
				counters = elo_counters["10"][question]
				elo_counters["10"][question] = check_ranking_prediction(current_ranking, photo1, photo2, counters)
				current_ranking = elo["20"][question]
				counters = elo_counters["20"][question]
				elo_counters["20"][question] = check_ranking_prediction(current_ranking, photo1, photo2, counters)
				current_ranking = elo["40"][question]
				counters = elo_counters["40"][question]
				elo_counters["40"][question] = check_ranking_prediction(current_ranking, photo1, photo2, counters)

				current_ranking = crowdbt["01"][question]
				counters = crowdbt_counters["01"][question]
				crowdbt_counters["01"][question] = check_ranking_prediction(current_ranking, photo1, photo2, counters)				
				current_ranking = crowdbt["1"][question]
				counters = crowdbt_counters["1"][question]
				crowdbt_counters["1"][question] = check_ranking_prediction(current_ranking, photo1, photo2, counters)

			elif answer == right:
				#Photo1 x Photo2
				current_ranking = maxdiff[question]
				counters = maxdiff_counters[question]
				maxdiff_counters[question] = check_ranking_prediction(current_ranking, photo2, photo1, counters)	

				current_ranking = qscore[question]
				counters = qscore_counters[question]
				qscore_counters[question] = check_ranking_prediction(current_ranking, photo2, photo1, counters)
	
				current_ranking = elo["10"][question]
				counters = elo_counters["10"][question]
				elo_counters["10"][question] = check_ranking_prediction(current_ranking, photo2, photo1, counters)
				current_ranking = elo["20"][question]
				counters = elo_counters["20"][question]
				elo_counters["20"][question] = check_ranking_prediction(current_ranking, photo2, photo1, counters)
				current_ranking = elo["40"][question]
				counters = elo_counters["40"][question]
				elo_counters["40"][question] = check_ranking_prediction(current_ranking, photo2, photo1, counters)

				current_ranking = crowdbt["01"][question]
				counters = crowdbt_counters["01"][question]
				crowdbt_counters["01"][question] = check_ranking_prediction(current_ranking, photo2, photo1, counters)				
				current_ranking = crowdbt["1"][question]
				counters = crowdbt_counters["1"][question]
				crowdbt_counters["1"][question] = check_ranking_prediction(current_ranking, photo2, photo1, counters)
			else:
				print(">>>>> Empates não considerados por enquanto")


def readTasksDefinitions(linesTasks):
	tasksDef = {}

	for line in linesTasks:
		data = line.split("+")
		taskID = data[0].strip(' \t\n\r')
		currentDef = json.loads(data[7].strip(' \t\n\r\"'))

		tasksDef[taskID] = currentDef
	
	return tasksDef


if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Uso: <tasks definition file>"
		sys.exit(1)

	tasksFile = open(sys.argv[1], 'r')
	linesTasks = tasksFile.readlines()
	tasksDefinitions = readTasksDefinitions(linesTasks)

	qscore_acc = {possibleQuestions[0]: [], possibleQuestions[1]: []}
	maxdiff_acc = {possibleQuestions[0]: [], possibleQuestions[1]: []}
	crowdbt_acc = {"01" : {possibleQuestions[0]: [], possibleQuestions[1]: []}, "1": {possibleQuestions[0]: [], possibleQuestions[1]: []}}
	elo_acc = {"10":{possibleQuestions[0]: [], possibleQuestions[1]: []}, "20":{possibleQuestions[0]: [], possibleQuestions[1]: []}, "40":{possibleQuestions[0]: [], possibleQuestions[1]: []}}
	for i in range(0,500):
		qscore_counters = {possibleQuestions[0]: [0,0,0,0], possibleQuestions[1]: [0,0,0,0]}#positives, negatives, false positives, false negatives
		maxdiff_counters = {possibleQuestions[0]: [0,0,0,0], possibleQuestions[1]: [0,0,0,0]}
		crowdbt_counters = {"01" : {possibleQuestions[0]: [0,0,0,0], possibleQuestions[1]: [0,0,0,0]}, "1": {possibleQuestions[0]: [0,0,0,0], possibleQuestions[1]: [0,0,0,0]}}
		elo_counters = {"10":{possibleQuestions[0]: [0,0,0,0], possibleQuestions[1]: [0,0,0,0]}, "20":{possibleQuestions[0]: [0,0,0,0], possibleQuestions[1]: [0,0,0,0]}, "40":{possibleQuestions[0]: [0,0,0,0], possibleQuestions[1]: [0,0,0,0]}}

		elo = build_elo_rankings(i)
		maxdiff = build_maxdiff_rankings(i)
		qscore = build_qscore_rankings(i)
		crowdbt = build_crowdbt_rankings(i)
	
		read_test_data(tasksDefinitions, elo, maxdiff, qscore, crowdbt, qscore_counters, maxdiff_counters, crowdbt_counters, elo_counters, i)

		#Calculating accuracies for each ranking strategy
		qscore_acc[possibleQuestions[0]].append(qscore_counters[possibleQuestions[0]][0] / (qscore_counters[possibleQuestions[0]][0]+qscore_counters[possibleQuestions[0]][3]))
		qscore_acc[possibleQuestions[1]].append(qscore_counters[possibleQuestions[1]][0] / (qscore_counters[possibleQuestions[1]][0]+qscore_counters[possibleQuestions[1]][3]))

		maxdiff_acc[possibleQuestions[0]].append(maxdiff_counters[possibleQuestions[0]][0] / (maxdiff_counters[possibleQuestions[0]][0]+maxdiff_counters[possibleQuestions[0]][3]))
		maxdiff_acc[possibleQuestions[1]].append(maxdiff_counters[possibleQuestions[1]][0] / (maxdiff_counters[possibleQuestions[1]][0]+maxdiff_counters[possibleQuestions[1]][3]))

		elo_acc["10"][possibleQuestions[0]].append(elo_counters["10"][possibleQuestions[0]][0] / (elo_counters["10"][possibleQuestions[0]][0]+elo_counters["10"][possibleQuestions[0]][3]))
		elo_acc["10"][possibleQuestions[1]].append(elo_counters["10"][possibleQuestions[1]][0] / (elo_counters["10"][possibleQuestions[1]][0]+elo_counters["10"][possibleQuestions[1]][3]))
		elo_acc["20"][possibleQuestions[0]].append(elo_counters["20"][possibleQuestions[0]][0] / (elo_counters["20"][possibleQuestions[0]][0]+elo_counters["20"][possibleQuestions[0]][3]))
		elo_acc["20"][possibleQuestions[1]].append(elo_counters["20"][possibleQuestions[1]][0] / (elo_counters["20"][possibleQuestions[1]][0]+elo_counters["20"][possibleQuestions[1]][3]))
		elo_acc["40"][possibleQuestions[0]].append(elo_counters["40"][possibleQuestions[0]][0] / (elo_counters["40"][possibleQuestions[0]][0]+elo_counters["40"][possibleQuestions[0]][3]))
		elo_acc["40"][possibleQuestions[1]].append(elo_counters["40"][possibleQuestions[1]][0] / (elo_counters["40"][possibleQuestions[1]][0]+elo_counters["40"][possibleQuestions[1]][3]))
		
		crowdbt_acc["01"][possibleQuestions[0]].append(crowdbt_counters["01"][possibleQuestions[0]][0] / (crowdbt_counters["01"][possibleQuestions[0]][0]+crowdbt_counters["01"][possibleQuestions[0]][3]))
		crowdbt_acc["01"][possibleQuestions[1]].append(crowdbt_counters["01"][possibleQuestions[1]][0] / (crowdbt_counters["01"][possibleQuestions[1]][0]+crowdbt_counters["01"][possibleQuestions[1]][3]))
		crowdbt_acc["1"][possibleQuestions[0]].append(crowdbt_counters["1"][possibleQuestions[0]][0] / (crowdbt_counters["1"][possibleQuestions[0]][0]+crowdbt_counters["1"][possibleQuestions[0]][3]))
		crowdbt_acc["1"][possibleQuestions[1]].append(crowdbt_counters["1"][possibleQuestions[1]][0] / (crowdbt_counters["1"][possibleQuestions[1]][0]+crowdbt_counters["1"][possibleQuestions[1]][3]))

	#Printing confidence intervals of accuracies for each ranking strategy
	for key in qscore_acc:
		values = qscore_acc[key]
		std = numpy.std(values)
		print("QScore\t" + key + "\t" + numpy.mean(values) + "\t [" + (numpy.mean(values) - std * 1.96 / sqrt(len(values))) + "," + (numpy.mean(values) + std * 1.96 / sqrt(len(values))) + "]" +"\n" )

	for key in maxdiff_acc:
		values = maxdiff_acc[key]
		print("MaxDiff\t" + key + "\t" + numpy.mean(values) + "\t [" + (numpy.mean(values) - std * 1.96 / sqrt(len(values))) + "," + (numpy.mean(values) + std * 1.96 / sqrt(len(values))) + "]" +"\n" )

	for key in crowdbt_acc:
		for value in crowdbt_acc[key]:
			values = crowdbt_acc[key][value]
			print("Crowdbt-" + str(value) + "\t" + key + "\t" + numpy.mean(values) + "\t [" + (numpy.mean(values) - std * 1.96 / sqrt(len(values))) + "," + (numpy.mean(values) + std * 1.96 / sqrt(len(values))) + "]" +"\n" )
			
	for key in elo_acc:
		for value in elo_acc[key]:
			values = elo_acc[key][value]
			print("Elo-" + str(value) + "\t" + key + "\t" + numpy.mean(values) + "\t [" + (numpy.mean(values) - std * 1.96 / sqrt(len(values))) + "," + (numpy.mean(values) + std * 1.96 / sqrt(len(values))) + "]" +"\n" )
