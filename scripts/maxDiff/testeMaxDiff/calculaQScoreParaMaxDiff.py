# coding=utf-8
#Faz a leitura da entrada utilizada para análise do MaxDiff e computa as relações de modo a se computar o QScore de cada alternativa

import sys
from sets import Set
from analisaQScore import *
import numpy

#possible questions
possibleQuestions = ["agrad%C3%A1vel?", "seguro?"]
left = 'Left'
right = 'Right'
notKnown = 'NotKnown'

votes = {possibleQuestions[0]:{}, possibleQuestions[1]:{}}

def saveVote(photo1, photo2):
	if not votes[possibleQuestions[0]].has_key(photo1):
		votes[possibleQuestions[0]][photo1] = {}
	if not votes[possibleQuestions[0]][photo1].has_key(photo2):
		votes[possibleQuestions[0]][photo1][photo2] = []
	votes[possibleQuestions[0]][photo1][photo2].append(left)

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Uso: <arquivo com respostas no formato do MaxDiff>"
		sys.exit(1)

	dataFile = open(sys.argv[1], 'r')
	lines = dataFile.readlines()

	allPhotos = set([])

	for line in lines:	
		lineData = line.split(",")	
		winner = ""
		loser = ""
		middle = []
		
		#print lineData

		for index in range(0, len(lineData)):
			allPhotos.add(index)

			opinion = lineData[index].strip("\n ")
			if opinion == "-1":
				loser = index
			elif opinion == "1":
				winner = index
			elif opinion == "0":
				middle.append(index)

		saveVote(winner, loser)

		for photo in middle:
			saveVote(winner, photo)
			saveVote(photo, loser)

	#Dealing with all answers for the same two photos and sampling the answer to consider at each iteration
	allQScores = {possibleQuestions[0]:{}}
	for samples in range(0, 10):
		resetCounters()

		for question, qDic in votes.iteritems():
			for photo1, photosDic in qDic.iteritems():
				for photo2, votesList in photosDic.iteritems():
					currentAnswers = votesList
					if qDic.has_key(photo2) and qDic[photo2].has_key(photo1):
						otherAnswers = qDic[photo2][photo1]
						for answer in otherAnswers:
							currentAnswers.append(right)

					answer = random.sample(currentAnswers, 1)[0]
					if answer == left:
						saveWin(photo1, photo2, question)
					elif answer == right:
						saveWin(photo2, photo1, question)
				

		qscores = computeQScores(allPhotos)
		for question, qDic in qscores.iteritems():
			if question == possibleQuestions[1]:
				continue
			for photo, qscore in qDic.iteritems():
				if not allQScores[question].has_key(photo):
					allQScores[question][photo] = []
				allQScores[question][photo].append(qscore)

	for question, qDic in allQScores.iteritems():
		for photo, qscoreList in qDic.iteritems():
			print(question.strip(' \t\n\r')+ "\t" + str(photo)+ "\t" + str(numpy.mean(qscoreList))+"\t" + str(qscoreList).strip("[ ]").replace(",", " ")+'\n')

