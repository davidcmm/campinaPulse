# coding=utf-8
# This script maps for each pair of photos evaluated the set of answers given to such pair

import sys
from sets import Set

#possible questions
possibleQuestions = ["agrad%C3%A1vel?", "seguro?"]

def mapAnswers(tasksExecution):
	answersDic = {possibleQuestions[0]: {},  possibleQuestions[1]: {}}

	for execution in tasksExecution:
		executionData = execution.split("+")
		userAnswer = executionData[9].strip(' \t\n\r"')

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

		photosDic = answersDic[question]
		if not photosDic.has_key(photo1):	
			photosDic[photo1] = {}
		if not photosDic[photo1].has_key(photo2):		
			photosDic[photo1][photo2] = set()

		taskAnswers = photosDic[photo1][photo2]	
		taskAnswers.add(answer)
		#print taskAnswers
		photosDic[photo1][photo2] = taskAnswers
	
	for question in answersDic.keys():
		photosDic = answersDic[question]
		for photo1 in photosDic.keys():
			photosCompared = photosDic[photo1]
			for photo2 in photosCompared.keys():
				#continue
				print photo1+"\t"+photo2+"\t"+str(len(photosCompared[photo2]))

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Uso: <arquivo com execucoes de tarefas para um grupo>"
		sys.exit(1)

	dataFile = open(sys.argv[1], 'r')
	lines = dataFile.readlines()
	dataFile.close()

	mapAnswers(lines)

