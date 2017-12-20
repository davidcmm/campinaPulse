# coding=utf-8
# Computes Elo ratings according to pairwise comparisons of images in Como é Campina?

import csv
import math

import sys
from sets import Set
import random
import numpy
import json
import pandas as pd

#possible questions
possibleQuestions = ["agrad%C3%A1vel?", "seguro?"]
allPhotos = Set([])

#possible answers
left = 'Left'
right = 'Right'
notKnown = 'NotKnown'
completeTie = 'equal'

initial_rating = 1500#Elo initial rating
K = 40#10, 20, 40?


def readTasksDefinitions(linesTasks):
	tasksDef = {}

	for line in linesTasks:
		data = line.split("+")	
		#print data
		taskID = data[0].strip(' \t\n\r')
		currentDef = json.loads(data[7].strip(' \t\n\r\"'))

		tasksDef[taskID] = currentDef
	return tasksDef

def resetCounters(allPhotos):
	photos_ratings = {possibleQuestions[0] : {}, possibleQuestions[1] : {}}
	for photo in allPhotos:
		photos_ratings[possibleQuestions[0]][photo] = initial_rating
		photos_ratings[possibleQuestions[1]][photo] = initial_rating
	return photos_ratings


def evaluate_ELO(lines, outputFileName, tasksDefinitions, samples):
	votes = {possibleQuestions[0]:{}, possibleQuestions[1]:{}}

	#Reading from pybossa task-run CSV
	for line in lines:
		lineData = line.split("+")

		executionID = lineData[0].strip(' \t\n\r"')
		taskID = lineData[3].strip(' \t\n\r"')
		userAnswer = lineData[9].strip(' \t\n\r"')

		#It is a new vote, read tasks definition from JSON!
		if executionID[0].lower() == 'n':
			data = json.loads(userAnswer)

			if data['question'].strip(' \t\n\r"') == "agradavel?" or data['question'].strip(' \t\n\r"') == possibleQuestions[0]:
				question = possibleQuestions[0]
			else:
				question = possibleQuestions[1]

			photo1 = data['theMost'].strip(' \t\n\r"')
			photo2 = data['theLess'].strip(' \t\n\r"')

			if len(photo1) == 0 or len(photo2) == 0:#Error in persisting photos!
				print "Foto zerada! " + line
				continue

			taskDef = tasksDefinitions[taskID]
			photos = Set( [taskDef['url_c'].strip(' \t\n\r"'), taskDef['url_b'].strip(' \t\n\r"'), taskDef['url_a'].strip(' \t\n\r"'), taskDef['url_d'].strip(' \t\n\r"')] )
			if photo1 != completeTie:
				photos.remove(photo1)
				photos.remove(photo2)
			else:
				photo1 = photos.pop()
				photo2 = photos.pop()
			
			photo3 = photos.pop()
			photo4 = photos.pop()

			#Creating votes dictionary
			if not votes[question].has_key(photo1):
				votes[question][photo1] = {}
			if not votes[question][photo1].has_key(photo2):
				votes[question][photo1][photo2] = set([])
			if not votes[question][photo1].has_key(photo3):
				votes[question][photo1][photo3] = set([])
			if not votes[question][photo1].has_key(photo4):
				votes[question][photo1][photo4] = set([])
			if not votes[question].has_key(photo2):
				votes[question][photo2] = {}
			if not votes[question][photo2].has_key(photo3):
				votes[question][photo2][photo3] = set([])
			if not votes[question][photo2].has_key(photo4):
				votes[question][photo2][photo4] = set([])
			if not votes[question].has_key(photo3):
				votes[question][photo3] = {}
			if not votes[question][photo3].has_key(photo4):
				votes[question][photo3][photo4] = set([])

			#Saving votes from task-run
			if photo1 != completeTie:
				votes[question][photo1][photo2].add(left)
				votes[question][photo1][photo3].add(left)
				votes[question][photo1][photo4].add(left)
				votes[question][photo2][photo3].add(right)
				votes[question][photo2][photo4].add(right)
				votes[question][photo3][photo4].add(notKnown)
			else:
				votes[question][photo1][photo2].add(notKnown)
				votes[question][photo1][photo3].add(notKnown)
				votes[question][photo1][photo4].add(notKnown)
				votes[question][photo2][photo3].add(notKnown)
				votes[question][photo2][photo4].add(notKnown)
				votes[question][photo3][photo4].add(notKnown)

			allPhotos.add(photo1)
			allPhotos.add(photo2)
			allPhotos.add(photo3)
			allPhotos.add(photo4)

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
		
			#Creating votes dictionary
			if not votes[question].has_key(photo1):
				votes[question][photo1] = {}
			if not votes[question][photo1].has_key(photo2):
				votes[question][photo1][photo2] = set([])

			#Saving votes from task-run
			votes[question][photo1][photo2].add(answer)

			allPhotos.add(photo1)
			allPhotos.add(photo2)

	#Evaluating votes in order to choose winning photos or ties
	allRatings = {possibleQuestions[0]: {}, possibleQuestions[1]: {}}
	for i in range(0, samples):
		photos_ratings = resetCounters(allPhotos)

		for question, qDic in votes.iteritems():
			for photo1, photosDic in qDic.iteritems():
				for photo2, votesList in photosDic.iteritems():
					answer = random.sample(votesList, 1)[0]#Generating answer to consider

					points_1 = 0		
					points_2 = 0		
					if answer == left:
						points_1 = 1
						points_2 = 0
					elif answer == right:
						points_1 = 0
						points_2 = 1
					elif answer == notKnown:
						points_1 = 0.5
						points_2 = 0.5

					expected_1 = 1 / ( 1+10**( (photos_ratings[question][photo2] - photos_ratings[question][photo1])/400 ) )
					expected_2 = 1 / ( 1+10**( (photos_ratings[question][photo1] - photos_ratings[question][photo2])/400 ) )

					photos_ratings[question][photo1] = photos_ratings[question][photo1] + K * (points_1 - expected_1)
					photos_ratings[question][photo2] = photos_ratings[question][photo2] + K * (points_2 - expected_2)

		for question, qDic in photos_ratings.iteritems():
			for photo, rating in qDic.iteritems():
				if not allRatings[question].has_key(photo):
					allRatings[question][photo] = []
				allRatings[question][photo].append(rating)
	#Output file
	output = open(outputFileName, 'w')
	for question, qDic in allRatings.iteritems():
		for photo, ratingList in qDic.iteritems():
			output.write(question.strip(' \t\n\r')+ "\t" + photo.strip(' \t\n\r').encode("utf-8")+ "\t" + str(numpy.mean(ratingList))+"\t" + str(ratingList).strip("[ ]").replace(",", "\t")+'\n')
	output.close()




if __name__ == "__main__":
	if len(sys.argv) < 4:
		print "Uso: <arquivo com execuções das tarefas> <tasks definition - V2> <amount of samples>"
		sys.exit(1)

	dataFile = open(sys.argv[1], 'r')
	tasksFile = open(sys.argv[2], 'r')
	samples = int(sys.argv[3])

	lines = dataFile.readlines()
	linesTasks = tasksFile.readlines()

	evaluate_ELO(lines, "all_elo.dat", readTasksDefinitions(linesTasks), samples)
