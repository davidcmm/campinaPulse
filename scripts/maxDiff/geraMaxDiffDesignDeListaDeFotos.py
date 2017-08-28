# coding=utf-8
# A partir de uma lista de fotos de tamanho X (sem template par a par!) gera uma proposta de tarefas no formato MaxDiff de tamanho Y

import sys
import random
from sets import Set

#possible questions
possibleQuestions = ["agrad%C3%A1vel?", "seguro?"]
task_size = 4
photo_threshold = 13

def buildMaxDiff(photos_filename, user_question):

	photos_file = open(photos_filename, "r")
	lines = photos_file.readlines()
	allPhotos = set([])
	photo_count = {}

	if "agrad" in user_question:
		question = possibleQuestions[0]
	else:
		question = possibleQuestions[1]

	#Reading all photos
	for line in lines:
		photo = line.strip(' \t\n\r"')
		allPhotos.add(photo)
		photo_count[photo] = 0

	allPhotos_bkp = allPhotos.copy()

	#Building MaxDiff design with task_size photos per task
	while len(allPhotos) > 0:
		currentPhotos = []

		photos = []
		#If there are less photos than task_size, add all remaining and repeat others!
		if len(allPhotos) <= task_size:
			photos.extend(allPhotos)
			for i in range(0, task_size - len(photos)):#Retrieve remaining from bkp
				photo = random.sample(allPhotos_bkp, 1)[0]
				while photo in photos or photo in currentPhotos:
					photo = random.sample(allPhotos_bkp, 1)[0]
				photos.append(photo)
		#Otherwise, randomize task_size photos
		else:
			photos = random.sample( allPhotos, task_size )

		#Updating photos counters
		for photo in photos:
			if photo_count.has_key(photo):
				counter = photo_count.get(photo)
			else:
				print ">>> Error, photo not found! " + photo
				sys.exit(1)
			if len(allPhotos) <= task_size:
				currentPhotos.append(photo)
				photo_count[photo] = photo_count[photo]+1
			elif counter < photo_threshold:
				currentPhotos.append(photo)
				photo_count[photo] = photo_count[photo]+1

		#Building current task
		sys.stdout.write(question)
		for i in range(0, len(currentPhotos)):
			sys.stdout.write("\t" + currentPhotos[i])
		sys.stdout.write("\n")
		
		#Checking if each photo reached threshold comparisons
		for photo in currentPhotos:
			if photo_count[photo] >= photo_threshold and photo in allPhotos:
				allPhotos.remove(photo)

	#Logging
	for photo in allPhotos:
		print "All photos remained with: " + photo

	for photo in photo_count.keys():
		print "Counter for " + photo + "\t" + str(photo_count[photo])	

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print "Uso: <arquivo com lista de fotos> <questao>"
		sys.exit(1)

	buildMaxDiff(sys.argv[1], sys.argv[2])
