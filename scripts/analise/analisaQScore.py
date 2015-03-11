# coding=utf-8

import sys
#import pdb

#photos considered in comparisons
allPhotos = set([])

#possible questions
possibleQuestions = ["agrad%C3%A1vel?", "seguro?"]

#possible answers
left = 'Left'
right = 'Right'
notKnown = 'NotKnown'

#dictionaries used to save photos comparisons results
winsPhotosPerQuestion = {possibleQuestions[0]:{}, possibleQuestions[1]:{}}
lossesPhotosPerQuestion = {possibleQuestions[0]:{}, possibleQuestions[1]:{}}

#dictionaries used to save photos win, loss and draw counters
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

def computeQScores(allPhotos, outputFileName):
	"""Computing qscore of each photo used in experiment."""
	outputFile = open(outputFileName, 'w')
	
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

			outputFile.write(question.strip(' \t\n\r')+ "\t" + photo.strip(' \t\n\r')+ "\t" + str(Qiu)+'\n')

	outputFile.close()


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

	computeQScores(allPhotos, outputFileName)

def evaluateAllVotes(lines, outputFileName):
	""" Considering all votes for each pair of photos """
	votes = {possibleQuestions[0]:{}, possibleQuestions[1]:{}}
	
	#Reading from pybossa task-run CSV
	for line in lines:
		data = line.split("+")
		answer = data[9].strip(' \t\n\r"').split(" ")
	
		question = answer[5].strip(' \t\n\r')
		answer = answer[6].strip(' \t\n\r')
		photo1 = answer[7].strip(' \t\n\r')
		photo2 = answer[8].strip(' \t\n\r')
		
		#Creating votes dictionary
		if not votes[question].has_key(photo1):
			votes[question][photo1] = {}
		if not votes[question][photo1].has_key(photo2):
			votes[question][photo1][photo2] = {left:0, right:0, notKnown: 0}
	
		#Saving votes from task-run
		if votes[question][photo1][photo2][left] + votes[question][photo1][photo2][right] + votes[question][photo1][photo2][notKnown] < 3: 
			if answer == left:
				votes[question][photo1][photo2][left] += 1
			elif answer == right:
				votes[question][photo1][photo2][right] += 1
			elif answer == notKnown:
				votes[question][photo1][photo2][notKnown] += 1
	
	#Evaluating votes in order to choose winning photos or ties
	for question, qDic in votes.iteritems():
		for photo1, photosDic in qdic.iteritems():
			for photo2, votesDic in photosdic.iteritems():
				leftCounter = votesDic[left]
				rightCounter = votesDic[right]
				tieCounter = votesDic[notKnown]	
			
				if leftCounter == rightCounter == tieCounter or tieCounter == 2:
					saveDraw(photo1, photo2, question)
				elif leftCounter == 2:
					saveWin(photo1, photo2, question)
				elif rightCounter == 2:
					saveWin(photo2, photo1, question)	
				else:
					print "Error! " + question + " " + photo1 + " " + photo2 + " " +leftCounter + " " + rightCounter + " " + tieCounter			
				allPhotos.add(photo1)
				allPhotos.add(photo2)

	computeQScores(allPhotos, outputFileName)


if __name__ == "__main__":
	if len(sys.argv) < 1:
		print "Uso: <arquivo com execuções das tarefas>"
		sys.exit(1)
	dataFile = open(sys.argv[1], 'r')
	lines = dataFile.readlines()

	evaluateFirstVote(lines, "first.dat")
	#evaluateAllVotes(lines, "all.dat")
	dataFile.close()
