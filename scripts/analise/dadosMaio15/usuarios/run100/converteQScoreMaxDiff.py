# coding=utf-8
#Converte a entrada de execução de tarefas no formato de análise do MaxDiff

import sys
from sets import Set

#possible questions
possibleQuestions = ["agrad%C3%A1vel?", "seguro?"]
left = 'Left'
right = 'Right'
notKnown = 'NotKnown'

votes = {possibleQuestions[0]:{}, possibleQuestions[1]:{}}

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Uso: <arquivo com execução das tarefas>"
		sys.exit(1)

	dataFile = open(sys.argv[1], 'r')
	lines = dataFile.readlines()
	allPhotos = set([])

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
			votes[question][photo1][photo2] = set([])

		allPhotos.add(photo1)
		allPhotos.add(photo2)
	
		#Saving votes from task-run
		votes[question][photo1][photo2].add(answer)


	allPhotosList = list(allPhotos)
	allPhotosList.sort()

	print str(len(allPhotosList))

	outputFile1 = open("agradMaxDiff.csv", "w")
	outputFile2 = open("segMaxDiff.csv", "w")

	for question, qDic in votes.iteritems():
		result = ""
		counter = 0
		for photo1, photosDic in qDic.iteritems():
			for photo2, votesList in photosDic.iteritems():
				answer = list(votesList)[0]#Answer to consider

				index1 = allPhotosList.index(photo1)
				index2 = allPhotosList.index(photo2)
				minimumIndex = min(index1, index2)
				maximumIndex = max(index1, index2)

				#print str(photo1) + " " + str(photo2) + " " + answer

				currentResult = ""
				counter = counter + 1

				print str(minimumIndex) + " " + str(maximumIndex)

				if answer == left:
					#print ">>> L"
					for i in range(0, minimumIndex):
						currentResult = currentResult + "a" + ','
					#print currentResult	
					currentResult = currentResult + "1,"
					for i in range(minimumIndex, maximumIndex):
						currentResult =  currentResult + "a" + ','	
					currentResult = currentResult + "-1,"
					for i in range(maximumIndex, len(allPhotosList)):
						currentResult = currentResult +  "a" + ','
					result = result + currentResult
				elif answer == right:
					#print ">>> R"
					for i in range(0, minimumIndex):
						currentResult =  currentResult + "a" + ','
					currentResult = currentResult + "-1,"
					for i in range(minimumIndex, maximumIndex):
						currentResult =  currentResult + "a" + ','	
					currentResult = currentResult + "1,"
					for i in range(maximumIndex, len(allPhotosList)):
						currentResult =  currentResult + "a" + ','
					result = result + currentResult
				elif answer == notKnown:
					#print ">>> L"
					for i in range(0, minimumIndex):
						currentResult =  currentResult + "a" + ','
					currentResult = currentResult + "0,"
					for i in range(minimumIndex, maximumIndex):
						currentResult =  currentResult + "a" + ','	
					currentResult = currentResult + "0,"
					for i in range(maximumIndex, len(allPhotosList)):
						currentResult =  currentResult + "a" + ','
					result = result + currentResult
				if question == "seguro?":
					outputFile2.write(currentResult+"\n")
				else:
					outputFile1.write(currentResult+"\n")
		
		if question == "seguro?":
			outputFile2.write(str(counter)+"\n")					
			#outputFile2.write(result[:-1])
			outputFile2.close()
		else:
			outputFile1.write(str(counter)+"\n")					
			#outputFile1.write(result[:-1])
			outputFile1.close()

#No R vetor = as.vector(t(seg[,1:110]))
