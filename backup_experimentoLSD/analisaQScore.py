# coding=utf-8

import sys
#import pdb

#photos considered in comparisons
allPhotos = set([])

#questions aspects
#unique = "único".decode('utf-8')
#safe = "seguro"
#beauty = "bonito"
#rich = "rico"

unique = "3"
safe = "2"
beauty = "1"
rich = "4"

aspects = [unique, safe, beauty, rich]

#dictionaries used to save photos comparisons results
winsPhotosPerQuestion = {unique:{}, safe:{}, beauty:{}, rich:{}}
lossesPhotosPerQuestion = {unique:{}, safe:{}, beauty:{}, rich:{}}

#dictionaries used to save photos win, loss and draw counters
winsPerQuestion = {unique:{}, safe:{}, beauty:{}, rich:{}}
lossesPerQuestion = {unique:{}, safe:{}, beauty:{}, rich:{}}
drawsPerQuestion = {unique:{}, safe:{}, beauty:{}, rich:{}}

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
	winsPhotos = winsPhotosPerQuestion[question]	
	if not winsPhotos.has_key(winPhoto):	
		winsPhotos[winPhoto] = set([])		
	winsPhotos[winPhoto].add(lossPhoto)
	
	winsCounter = winsPerQuestion[question]
	if not winsCounter.has_key(winPhoto):
		winsCounter[winPhoto] = 0
	winsCounter[winPhoto] += 1

	#Saving that lossPhoto lost against winPhoto and updating lossPhoto counter
	lossPhotos = lossesPhotosPerQuestion[question]	
	if not lossPhotos.has_key(lossPhoto):
		lossPhotos[lossPhoto] = set([])
	lossPhotos[lossPhoto].add(winPhoto)
	
	lossCounter = lossesPerQuestion[question]
	if not lossCounter.has_key(lossPhoto):
		lossCounter[lossPhoto] = 0
	lossCounter[lossPhoto] += 1


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
	
	for question in aspects:
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
				for photo1 in winsPhotosPerQuestion[question][photo]:
					currentWiu = calcWiu(photo1, question)
					fac1 += currentWiu
				fac1 = (1.0 * fac1) / niw
			else:
				fac1 = 0	
			
			if lossesPhotosPerQuestion[question].has_key(photo):
				nil = len(lossesPhotosPerQuestion[question][photo])
				fac2 = 0
				for photo2 in lossesPhotosPerQuestion[question][photo]:
					currentLiu = calcLiu(photo2, question)
					fac2 += currentLiu
				fac2 = (1.0 * fac2) / nil
			else:
				fac2 = 0
			
			#Computing Q-score for photo related to question			
			if not winsPhotosPerQuestion[question].has_key(photo) and not lossesPhotosPerQuestion[question].has_key(photo) and not drawsPerQuestion[question].has_key(photo):
				Qiu = -1#Photo has not participated in any comparison!
			else:			
				Qiu = 10/3.0 * (Wiu + fac1 - fac2 + 1)

			print question.strip(' \t\n\r')+ "\t" + photo.strip(' \t\n\r')+ "\t" + str(Qiu)


if __name__ == "__main__":
	if len(sys.argv) < 1:
		print "Uso: <arquivo com dados>"
		sys.exit(1)
	dataFile = open(sys.argv[1], 'r')
	lines = dataFile.readlines()

	for line in lines:
		data = line.split("\t")
		
		question = data[1].strip(' \t\n\r')
		answer = data[2].strip(' \t\n\r')
		photo1 = data[3].strip(' \t\n\r')
		photo2 = data[4].strip(' \t\n\r')
			
		if answer == 'Left':
			saveWin(photo1, photo2, question)
		elif answer == 'Right':
			saveWin(photo2, photo1, question)
		elif answer == 'NotKnown':
			saveDraw(photo1, photo2, question)

		allPhotos.add(photo1)
		allPhotos.add(photo2)
	
	computeQScores(allPhotos)
	
