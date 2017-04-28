# coding=utf-8
# Calculates photos qscore from a set of tasks execution file

import sys
from sets import Set
import random
import numpy
import json
import csv
import pandas as pd
#import pdb

#photos considered in comparisons
allPhotos = Set([])

#possible questions
possibleQuestions = ["agrad%C3%A1vel?", "seguro?"]

#possible answers
left = 'Left'
right = 'Right'
notKnown = 'NotKnown'
completeTie = 'equal'

#dictionaries used to save photos comparisons results
winsPhotosPerQuestion = {possibleQuestions[0]:{}, possibleQuestions[1]:{}}
lossesPhotosPerQuestion = {possibleQuestions[0]:{}, possibleQuestions[1]:{}}

#dictionaries used to save photos win, loss and draw counters
winsPerQuestion = {possibleQuestions[0]:{}, possibleQuestions[1]:{}}
lossesPerQuestion = {possibleQuestions[0]:{}, possibleQuestions[1]:{}}
drawsPerQuestion = {possibleQuestions[0]:{}, possibleQuestions[1]:{}}

def resetCounters():
	winsPhotosPerQuestion = {possibleQuestions[0]:{}, possibleQuestions[1]:{}}
	lossesPhotosPerQuestion = {possibleQuestions[0]:{}, possibleQuestions[1]:{}}

	winsPerQuestion = {possibleQuestions[0]:{}, possibleQuestions[1]:{}}
	lossesPerQuestion = {possibleQuestions[0]:{}, possibleQuestions[1]:{}}
	drawsPerQuestion = {possibleQuestions[0]:{}, possibleQuestions[1]:{}}

def saveDraw(photo1, photo2, question):
	"""Computing photos comparison when there is no winner."""
	
	draws = drawsPerQuestion[question]
	if not draws.has_key(photo1):
		draws[photo1] = 0
			
	if not draws.has_key(photo2):
		draws[photo2] = 0

	draws[photo1] += 1
	draws[photo2] += 1

def saveWin(winPhoto, lossPhoto, question):
	"""Computing photos comparison when there is a winner."""
	#pdb.set_trace()
	#Saving that winPhoto won against lossPhoto and updating winPhoto counter
	winsPhotosDic = winsPhotosPerQuestion[question]	
	if not winsPhotosDic.has_key(winPhoto):	
		winsPhotosDic[winPhoto] = set([])
		
	winsPhotosDic[winPhoto].add(lossPhoto)
	
	winsCounterDic = winsPerQuestion[question]
	if not winsCounterDic.has_key(winPhoto):
		winsCounterDic[winPhoto] = 0
	winsCounterDic[winPhoto] += 1

	#Saving that lossPhoto lost against winPhoto and updating lossPhoto counter
	lossPhotosDic = lossesPhotosPerQuestion[question]	
	if not lossPhotosDic.has_key(lossPhoto):
		lossPhotosDic[lossPhoto] = set([])
	lossPhotosDic[lossPhoto].add(winPhoto)
	
	lossCounterDic = lossesPerQuestion[question]
	if not lossCounterDic.has_key(lossPhoto):
		lossCounterDic[lossPhoto] = 0
	lossCounterDic[lossPhoto] += 1


def calcWiu(photo, question):
	"""Computing Wiu component of QScore."""	
	#pdb.set_trace()
	if not winsPerQuestion[question].has_key(photo):
		wiu = 0
	else:
		wiu = winsPerQuestion[question][photo]

	if not lossesPerQuestion[question].has_key(photo):
		liu = 0
	else:
		liu = lossesPerQuestion[question][photo]

	if not drawsPerQuestion[question].has_key(photo):
		tiu = 0
	else:
		tiu = drawsPerQuestion[question][photo]
	
	#Computing Wi,u
	if wiu == 0 and liu == 0 and tiu == 0:
		return 0

	Wiu = ((1.0*wiu) / (wiu + liu + tiu))
	return Wiu

def calcLiu(photo, question):
	"""Computing Liu component of QScore."""	
	
	if not winsPerQuestion[question].has_key(photo):
		wiu = 0
	else:
		wiu = winsPerQuestion[question][photo]

	if not lossesPerQuestion[question].has_key(photo):
		liu = 0
	else:
		liu = lossesPerQuestion[question][photo]

	if not drawsPerQuestion[question].has_key(photo):
		tiu = 0
	else:
		tiu = drawsPerQuestion[question][photo]
	
	#Computing Li,u
	if wiu == 0 and liu == 0 and tiu == 0:
		return 0
	
	Liu = ((1.0*liu) / (wiu + liu + tiu))
	return Liu

def computeQScores(allPhotos):
	"""Computing qscore of each photo used in experiment."""
	output = {possibleQuestions[0]:{}, possibleQuestions[1]:{}}
	
	#Calculate Q-Score for each question and each photo
	for question in possibleQuestions:
		for photo in allPhotos:
			
			#if photo == "floriano_3902.jpg" and question == unique:
				#pdb.set_trace()
				#if winsPhotosPerQuestion[question].has_key("floriano_3902.jpg"):
				#	print winsPhotosPerQuestion[beauty]["floriano_3902.jpg"]

			Wiu = calcWiu(photo, question)
			
			#Computing factors
			if winsPhotosPerQuestion[question].has_key(photo):
				niw = len(winsPhotosPerQuestion[question][photo])
				fac1 = 0
				for photoPreferredOver in winsPhotosPerQuestion[question][photo]:
					currentWiu = calcWiu(photoPreferredOver, question)
					fac1 += currentWiu
				fac1 = (1.0 * fac1) / niw
			else:
				fac1 = 0	
			
			if lossesPhotosPerQuestion[question].has_key(photo):
				nil = len(lossesPhotosPerQuestion[question][photo])
				fac2 = 0
				for photoNotPreferredOver in lossesPhotosPerQuestion[question][photo]:
					currentLiu = calcLiu(photoNotPreferredOver, question)
					fac2 += currentLiu
				fac2 = (1.0 * fac2) / nil
			else:
				fac2 = 0
			
			#Computing Q-score for photo related to question			
			if not (winsPhotosPerQuestion[question].has_key(photo) or lossesPhotosPerQuestion[question].has_key(photo) or drawsPerQuestion[question].has_key(photo)):
				Qiu = -1#Photo has not participated in any comparison!
			else:			
				Qiu = 10/3.0 * (Wiu + fac1 - fac2 + 1)

			output[question][photo] = Qiu

	return output

def evaluateFirstVote(lines, outputFileName):
	""" Considering only the first vote for each pair of photos """
	#pdb.set_trace()
	photosAlreadyComputed = {possibleQuestions[0]:set([]), possibleQuestions[1]:set([])}

	for line in lines:#Reading from pybossa task-run CSV
		lineData = line.split("+")
		userAnswer = lineData[9].strip(' \t\n\r"')

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
		
		if not photosAlreadyComputed[question].__contains__(photo1+" "+photo2):
			if answer == left:
				saveWin(photo1, photo2, question)
			elif answer == right:
				saveWin(photo2, photo1, question)
			elif answer == notKnown:
				saveDraw(photo1, photo2, question)

			allPhotos.add(photo1)
			allPhotos.add(photo2)
			photosAlreadyComputed[question].add(photo1+" "+photo2)

	output = open(outputFileName, 'w')
	outputData = computeQScores(allPhotos)
	for question, qDic in outputData.iteritems():
		for photo, qscore in qDic.iteritems():
			output.write(question.strip(' \t\n\r')+ "\t" + photo.strip(' \t\n\r')+ "\t" + str(qscore)+'\n')
	output.close()

def evaluateAllVotes(lines, outputFileName, amountOfSamples, tasksDefinitions, percentOfComparisonsToDeal=1):
	""" Considering all votes for each pair of photos and performing a simulation (bootstrap based)"""
	votes = {possibleQuestions[0]:{}, possibleQuestions[1]:{}}
	allQScores = {possibleQuestions[0]:{}, possibleQuestions[1]:{}}
	
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

	
	#print str(len(allPhotos))
	#print str(len(votes[possibleQuestions[0]]))
	#print str(len(votes[possibleQuestions[1]]))

	#Evaluating votes in order to choose winning photos or ties
	for i in range(0, amountOfSamples):
		resetCounters()

		for question, qDic in votes.iteritems():
			for photo1, photosDic in qDic.iteritems():
				value = random.random()
				if value <= percentOfComparisonsToDeal:
					for photo2, votesList in photosDic.iteritems():
						answer = random.sample(votesList, 1)[0]#Generating answer to consider
			
						if answer == left:
							saveWin(photo1, photo2, question)
						elif answer == right:
							saveWin(photo2, photo1, question)
						elif answer == notKnown:
							saveDraw(photo1, photo2, question)	

		qscores = computeQScores(allPhotos)
		for question, qDic in qscores.iteritems():
			for photo, qscore in qDic.iteritems():
				if not allQScores[question].has_key(photo):
					allQScores[question][photo] = []
				allQScores[question][photo].append(qscore)

	#Output file
	output = open(outputFileName, 'w')
	for question, qDic in allQScores.iteritems():
		for photo, qscoreList in qDic.iteritems():
			output.write(question.strip(' \t\n\r')+ "\t" + photo.strip(' \t\n\r')+ "\t" + str(numpy.mean(qscoreList))+"\t" + str(qscoreList).strip("[ ]").replace(",", "\t")+'\n')
	output.close()

def evaluateAllVotesPredicted(data_wodraw, data_draws, outputFileName, amountOfSamples):
	""" Considering all predicted (classifiers) votes for each pair of photos and performing a simulation (bootstrap based)"""

	votes = {possibleQuestions[0]:{}, possibleQuestions[1]:{}}
	allQScores = {possibleQuestions[0]:{}, possibleQuestions[1]:{}}
	
	#Reading data without draws
	for index, row in data_wodraw.iterrows():

		raw_answer = row['prediction']
		if raw_answer == 1:#-1 mapped to 1, 1 mapped to 0
			answer = left
		else:
			answer = right

		raw_question = row['question'].strip(' \t\n\r"')
		photo1 = row['photo1'].strip(' \t\n\r"')
		photo2 = row['photo2'].strip(' \t\n\r"')

		if "agrad" in raw_question:
			question = possibleQuestions[0]
		else:
			question = possibleQuestions[1]
	
		#Creating votes dictionary
		if not votes[question].has_key(photo1):
			votes[question][photo1] = {}
		if not votes[question][photo1].has_key(photo2):
			votes[question][photo1][photo2] = set([])

		#Saving votes from task-run
		votes[question][photo1][photo2].add(answer)

		allPhotos.add(photo1)
		allPhotos.add(photo2)

	#Reading data with draws
	for index, row in data_draws.iterrows():

		answer = notKnown

		quest = row['question'].strip(' \t\n\r"')
		photo1 = row['photo1'].strip(' \t\n\r"')
		photo2 = row['photo2'].strip(' \t\n\r"')

		if "agrad" in quest:
			question = possibleQuestions[0]
		else:
			question = possibleQuestions[1]
	
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
	for i in range(0, amountOfSamples):
		resetCounters()

		for question, qDic in votes.iteritems():
			for photo1, photosDic in qDic.iteritems():
				for photo2, votesList in photosDic.iteritems():
					answer = random.sample(votesList, 1)[0]#Generating answer to consider
	
					if answer == left:
						saveWin(photo1, photo2, question)
					elif answer == right:
						saveWin(photo2, photo1, question)
					elif answer == notKnown:
						saveDraw(photo1, photo2, question)	

		qscores = computeQScores(allPhotos)
		for question, qDic in qscores.iteritems():
			for photo, qscore in qDic.iteritems():
				if not allQScores[question].has_key(photo):
					allQScores[question][photo] = []
				allQScores[question][photo].append(qscore)


	#Output file
	output = open(outputFileName, 'w')
	for question, qDic in allQScores.iteritems():
		for photo, qscoreList in qDic.iteritems():
			output.write( question.strip(' \t\n\r')+ "\t" + photo.strip(' \t\n\r')+ "\t" + str(numpy.mean(qscoreList))+"\t" + str(qscoreList).strip("[ ]").replace(",", "\t")+'\n' ) 
	output.close()


def evaluateVotesStreetSeen(lines, outputFileName):
	""" Considering all votes for each pair of photos"""
	votes = {possibleQuestions[1]:{}}
	allQScores = {possibleQuestions[1]:{}}
	
	#Reading from streetseen task-run CSV
	index = 0
	for line in lines:
		if index > 0:
			question = possibleQuestions[1]
			preferredPhoto = line[13]
			notPreferredPhoto = line[20]
	
			#Creating votes dictionary
			if not votes[question].has_key(preferredPhoto):
				votes[question][preferredPhoto] = {}
			if not votes[question][preferredPhoto].has_key(notPreferredPhoto):
				votes[question][preferredPhoto][notPreferredPhoto] = set([])

			#Saving votes from task-run
			votes[question][preferredPhoto][notPreferredPhoto].add(left)

			allPhotos.add(preferredPhoto)
			allPhotos.add(notPreferredPhoto)
		index = index + 1

	#print "All photos " + str(len(allPhotos))
	#differentTasks = 0
	
	#Evaluating votes in order to choose winning photos or ties
	for i in range(0, amountOfSamples):
		resetCounters()

		for question, qDic in votes.iteritems():
			for photo1, photosDic in qDic.iteritems():
				#print ">>>> KEY: " + photo1 + " " + str(len(photosDic.keys()))
				for photo2, votesList in photosDic.iteritems():
					answer = random.sample(votesList, 1)[0]#Generating answer to consider

					#if votes.has_key(photo2):
					#	if not votes[photo2].has_key(photo1):
					#		differentTasks = differentTasks + 1
					#else:
					#	differentTasks = differentTasks + 1
			
					if answer == left:
						saveWin(photo1, photo2, question)
					elif answer == right:
						saveWin(photo2, photo1, question)
					elif answer == notKnown:
						saveDraw(photo1, photo2, question)	

		qscores = computeQScores(allPhotos)
		for question, qDic in qscores.iteritems():
			if question == possibleQuestions[1]:
				for photo, qscore in qDic.iteritems():
					if not allQScores[question].has_key(photo):
						allQScores[question][photo] = []
					allQScores[question][photo].append(qscore)

	#print "Different tasks " + str(differentTasks)

	#Output file
	output = open(outputFileName, 'w')
	for question, qDic in allQScores.iteritems():
		for photo, qscoreList in qDic.iteritems():
			output.write(question.strip(' \t\n\r')+ "\t" + photo.strip(' \t\n\r')+ "\t" + str(numpy.mean(qscoreList))+"\t" + str(qscoreList).strip("[ ]").replace(",", " ")+'\n')
	output.close()

def evaluateVotePerIteration(lines, outputFileNames):
	""" Considering votes per replica iteration for each pair of photos"""
	votes = {possibleQuestions[0]:{}, possibleQuestions[1]:{}}
	votesUsers = {possibleQuestions[0]:{}, possibleQuestions[1]:{}}

	allQScores = {possibleQuestions[0]:{}, possibleQuestions[1]:{}}
	
	#Reading from pybossa task-run CSV
	for iteration in  range(0, 3):
		resetCounters()

		for line in lines:
			lineData = line.split("+")
			userID = lineData[4]		
			userAnswer = lineData[9].strip(' \t\n\r"')

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
				votes[question][photo1][photo2] = 0

			#Creating users control dictionary
			if not votesUsers[question].has_key(photo1):
				votesUsers[question][photo1] = Set([])
			if not votesUsers[question].has_key(photo2):
				votesUsers[question][photo2] = Set([])


			if (iteration == 0 and votes[question][photo1][photo2] == 0) or (iteration == 1 and votes[question][photo1][photo2] == 1) or (iteration == 2 and votes[question][photo1][photo2] == 2):
				if answer == left:
					saveWin(photo1, photo2, question)
				elif answer == right:
					saveWin(photo2, photo1, question)
				elif answer == notKnown:
					saveDraw(photo1, photo2, question)

				allPhotos.add(photo1)
				allPhotos.add(photo2)

				votes[question][photo1][photo2] += 1
				votesUsers[question][photo1].add(userID)
				votesUsers[question][photo2].add(userID)
	
		qscores = computeQScores(allPhotos)
		for question, qDic in qscores.iteritems():
			for photo, qscore in qDic.iteritems():
				if not allQScores[question].has_key(photo):
					allQScores[question][photo] = []
				allQScores[question][photo].append(qscore)
		#??? Como colocar userID + profile se cada QScore é computador com base em várias opiniões? Já colocar o binário por perfil?
		#Output file
		output = open(outputFileNames[iteration], 'w')
		for question, qDic in allQScores.iteritems():
			for photo, qscoreList in qDic.iteritems():
				output.write(question.strip(' \t\n\r')+ "\t" + photo.strip(' \t\n\r')+ "\t" + str(qscoreList[0])+"\t" + str(votesUsers[question][photo]).strip("Set( )").strip("[ ]").replace(",", "\t").replace("'", "")+'\n')
		output.close()


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
		print "Uso: <arquivo com execuções das tarefas> <# bootstrap samples - used in all votes> <tasks definition - V2> <project type: campina, streetseen or pred-campina>"
		sys.exit(1)
	
	if len(sys.argv) > 3:
		amountOfSamples = int(sys.argv[2])

	if len(sys.argv) > 4:
		projectType = sys.argv[4]
	else:
		projectType = "campina"

	if projectType == "campina":
		dataFile = open(sys.argv[1], 'r')
		tasksFile = open(sys.argv[3], 'r')
		lines = dataFile.readlines()
		linesTasks = tasksFile.readlines()

		#evaluateFirstVote(lines, "first.dat")
		evaluateAllVotes(lines, "all.dat", amountOfSamples, readTasksDefinitions(linesTasks), 1)
		#evaluateVotePerIteration(lines, ["qscoresPerIteration0.dat", "qscoresPerIteration1.dat", "qscoresPerIteration2.dat"])

		dataFile.close()
	elif projectType == "streetseen":
		lines = csv.reader(open(sys.argv[1], 'r'))

		evaluateVotesStreetSeen(lines, "all_street_seen.dat")

	else:
		data_wodraw = pd.read_table(sys.argv[1], sep='\s+', encoding='utf8', header=0)#wodraw
		data_3classes = pd.read_table(sys.argv[3], sep='\t', encoding='utf8', header=0)#3classes
		draws = data_3classes[(data_3classes.choice == 0)]

		evaluateAllVotesPredicted(data_wodraw, draws, "all_predicted.dat", amountOfSamples)

		
