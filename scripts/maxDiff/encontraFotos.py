# coding=utf-8
# Searches for tasks definition from task.csv and builds a suggestion for a MaxDiff design

import sys
from sets import Set
import random

possibleQuestions = ["agrad%C3%A1vel?", "seguro?"]

tasksAgrad = {}
tasksSeg = {}

def readInput(lines):
	""" Reads all tasks definitions from input file lines"""
	for line in lines:
		lineData = line.split(",")
		data1 = lineData[7].strip("\"}{").split(":")[2].split("/")
		data2 = lineData[9].strip("\"}{").split(":")[2].split("/")
		photo1 = data1[5] + "/" + data1[6]
		photo2 = data2[5] + "/" + data2[6]

		if possibleQuestions[0] in line:
			tasks = tasksAgrad
		else:
			tasks = tasksSeg 
	
		if tasks.has_key(photo1):
			currentTasks1 = tasks[photo1]
		else:
			currentTasks1 = []
		currentTasks1.append(photo2)
		tasks[photo1] = currentTasks1

		if tasks.has_key(photo2):
			currentTasks2 = tasks[photo2]
		else:
			currentTasks2 = []
		currentTasks2.append(photo1)
		tasks[photo2] = currentTasks2

	#Checking if two maps are equal?
	print len(tasksAgrad.keys())
	for key in tasksAgrad.keys():
		if tasksSeg.has_key(key):
			#print len(tasksAgrad[key]) == len(tasksSeg[key])
			continue
		else:
			raise RuntimeError("Map Seg does not have key ", key)


#def checkEqualPhotos(photo1, photo2, photo3, photo4, photo):
def checkEqualPhotos(photo1, photo2, photo3, photo):
	""" Verifies if there is a pair of photos that are equal to each other"""
	if photo1 == photo2:
		raise RuntimeError("Equal photos: ", photo1, photo2)
	elif photo1 == photo3:
		raise RuntimeError("Equal photos: ", photo1, photo3)
	#elif photo1 == photo4:
	#	raise RuntimeError("Equal photos: ", photo1, photo4)
	elif photo1 == photo:
		raise RuntimeError("Equal photos: ", photo1, photo)
	elif photo2 == photo3:
		raise RuntimeError("Equal photos: ", photo2, photo3)
	#elif photo2 == photo4:
	#	raise RuntimeError("Equal photos: ", photo2, photo4)
	elif photo2 == photo:
		raise RuntimeError("Equal photos: ", photo2, photo)
	#elif photo3 == photo4:
	#	raise RuntimeError("Equal photos: ", photo3, photo4)
	elif photo3 == photo:
		raise RuntimeError("Equal photos: ", photo3, photo)
	#elif photo4 == photo:
	#	raise RuntimeError("Equal photos: ", photo4, photo)

def evaluateBasedOnControlGroup():
	""" Filter according to a control group in order to build MaxDiff design based tasks"""
	#controlPhoto = ["norte/centro/Avenida_Presidente_Getulio_Vargas__395__90.jpg", "norte/centro/Rua_Elias_Aforas__67__0.jpg", "oeste/liberdade/Rua_Odon_Bezerra__147_270.jpg", "norte/centro/Rua_Elias_Aforas__67__180.jpg", "oeste/liberdade/Rua_Riachuelo__930__0.jpg", "norte/centro/Rua_Manoel_P._de_Araujo__370_0.jpg", "norte/centro/Rua_Elias_Aforas__202_0.jpg", "norte/centro/Avenida_Barao_Rio_Branco__141_90.jpg", "norte/centro/Avenida_Presidente_Joao_Pessoa__128__90.jpg", "oeste/liberdade/Rua_Odon_Bezerra__306_270.jpg"]
#Photos with greater dispersion in Qscore per photo (> 0.1)
	controlPhoto = {"agrad%C3%A1vel?" : ["centro/Avenida_Barao_Rio_Branco__141_90.jpg", "centro/Avenida_Presidente_Getulio_Vargas__210__0.jpg", "centro/Avenida_Presidente_Getulio_Vargas__271__270.jpg", "centro/Avenida_Dom_Pedro_II__119_270.jpg", "centro/Rua_Augusto_Severo__71_0.jpg", "centro/Rua_Capitao_Joao_de_Sa__45__0.jpg", "centro/Rua_Felix_Araujo__132__270.jpg", "centro/Rua_Felix_Araujo__48__90.jpg", "centro/Rua_Joao_da_Mata__490_90.jpg", "centro/Rua_Manoel_P._de_Araujo__370_0.jpg", "centro/Rua_Pedro_Alvares_Cabral__129_180.jpg", "centro/Rua_Pedro_Alvares_Cabral__129_90.jpg", "centro/Rua_Quebra_Quilos__399__270.jpg", "catole/Rua_Aluisio_Cunha_Linha__50__90.jpg", "catole/Avenida_Prefeito_Severino_Bezerra_Cabral__218_0.jpg", "catole/Rua_Doutor_Antonio_Telha_-_Catole__Campina_Grande__270.jpg","catole/Rua_Honorio_de_Melo__240__270.jpg", "catole/Rua_Olegario_Mariano__139_90.jpg", "catole/Rua_Olegario_Mariano__139_180.jpg", "catole/Rua_Sebastiao_Vieira_da_Silva__1273__180.jpg", "liberdade/Rua_Acre__635_90.jpg", "liberdade/Rua_Edesio_Silva__602__180.jpg", "liberdade/Rua_Espirito_Santo__1288__0.jpg", "liberdade/Rua_Espirito_Santo__1288__180.jpg", "liberdade/Rua_Odon_Bezerra__388__270.jpg", "liberdade/Rua_Padre_Pedro_Serrao__353__270.jpg", "liberdade/Rua_Padre_Pedro_Serrao__353__90.jpg", "liberdade/Rua_Sergipe__1337_0.jpg"], "seguro?" : ["centro/Rua_Felix_Araujo__132__270.jpg", "centro/Rua_Joao_da_Mata__490_270.jpg", "centro/Rua_Manoel_P._de_Araujo__370_180.jpg", "catole/Rua_Aluisio_Cunha_Linha__50__270.jpg", "catole/Rua_Inacio_Marques_da_Silva__434_270.jpg", "catole/Rua_Inacio_Marques_da_Silva__434_90.jpg", "catole/Rua_Olegario_Mariano__139_90.jpg", "liberdade/Rua_Acre__635_270.jpg", "liberdade/Rua_Riachuelo__455__0.jpg", "liberdade/Rua_Padre_Pedro_Serrao__336__90.jpg"]}

	allTasksRelation = {"agrad%C3%A1vel?" : {}, "seguro?" : {}}

	#Selecting photos from control group
	counter = 0
	for question in controlPhoto.keys():
		photos = controlPhoto[question]
		currentPhotosToUpdate = set([])
		otherPhotos = set([])

		if possibleQuestions[0] == question:
			tasks = tasksAgrad
		else:
			tasks = tasksSeg

		#Selecting control group related photos
		for photo in photos:
			currentPhotosToUpdate.update(tasks[photo])
			otherPhotos.add(photo)
			counter = counter + 1

			currentRelations = allTasksRelation[question]
			currentRelations[photo] = tasks[photo]

		#Iterating through related photos
		while len(currentPhotosToUpdate) > 0:
			currentPhoto = currentPhotosToUpdate.pop()

			if not currentPhoto in otherPhotos:
				for photo in tasks[currentPhoto]:
					if not photo in otherPhotos:
						currentPhotosToUpdate.add(photo)
				otherPhotos.add(currentPhoto)

				currentRelations = allTasksRelation[question]
				currentRelations[currentPhoto] = tasks[currentPhoto]
				counter = counter + 1

	
	createMaxDiffDesign(allTasksRelation)


def createMaxDiffDesign():
	""" Creating new tasks design according to MaxDiff """
	allTasksRelation = {"agrad%C3%A1vel?" : tasksAgrad, "seguro?" : tasksSeg}
	totalOfOtherPhotosInGroup = 3

	#for question in allTasksRelation.keys():
	currentQuestionData = allTasksRelation[possibleQuestions[0]]
	photosCounter = {}
	photosLeft = {}

	allPhotos = currentQuestionData.keys()

	for photo in allPhotos:
		relatedPhotos = currentQuestionData[photo]
		relatedPhotosCopy = list(relatedPhotos)

		photosLeft[photo] = []
		
		#while total of related photos is a multiple of 3 photos, try to build 11 subgroups of 3 photos
		while len(relatedPhotos) / totalOfOtherPhotosInGroup > 0:
			choosedPhotos = []
	
			#Building a random group of 3 photos
			while len(choosedPhotos) < totalOfOtherPhotosInGroup and len(relatedPhotos) > 0:
				index = random.randint(0, len(relatedPhotos)-1)
				currentPhoto = relatedPhotos.pop(index)

				if (photosCounter.has_key(currentPhoto) and photosCounter[currentPhoto] <= 11) or not (photosCounter.has_key(currentPhoto)):
					choosedPhotos.append(currentPhoto)

					if len(choosedPhotos) == totalOfOtherPhotosInGroup :
						photo1  = choosedPhotos[0]
						photo2  = choosedPhotos[1]
						photo3  = choosedPhotos[2]
						#photo4  = choosedPhotos[3]

						#checkEqualPhotos(photo1, photo2, photo3, photo4, photo)
						checkEqualPhotos(photo1, photo2, photo3, photo)
						#print question + " " + photo + " " + photo1 + " " + photo2 + " " + photo3 + " " + photo4
						print possibleQuestions[0] + " " + photo + " " + photo1 + " " + photo2 + " " + photo3
						print possibleQuestions[1] + " " + photo + " " + photo1 + " " + photo2 + " " + photo3

						if photosCounter.has_key(photo):
							photosCounter[photo] = photosCounter[photo] + 1
						else:
							photosCounter[photo] = 1

						if photosCounter.has_key(photo1):
							photosCounter[photo1] = photosCounter[photo1] + 1
						else:
							photosCounter[photo1] = 1

						if photosCounter.has_key(photo2):
							photosCounter[photo2] = photosCounter[photo2] + 1
						else:
							photosCounter[photo2] = 1

						if photosCounter.has_key(photo3):
							photosCounter[photo3] = photosCounter[photo3] + 1
						else:
							photosCounter[photo3] = 1

		#One photo left, creating other comparisons!
		if len(relatedPhotos) == 1:
			allPhotosSet = Set(allPhotos)
			allPhotosSet.remove(photo)

			otherPhotos = list(allPhotosSet.difference(Set(relatedPhotosCopy)))
			choosedPhotos = [relatedPhotos[0]]

			#Second other photo
			index = random.randint(0, len(otherPhotos)-1)
			currentPhoto = otherPhotos.pop(index)
			choosedPhotos.append(currentPhoto)

			#Third other photo
			index = random.randint(0, len(otherPhotos)-1)
			currentPhoto = otherPhotos.pop(index)
			choosedPhotos.append(currentPhoto)

			photo1  = choosedPhotos[0]
			photo2  = choosedPhotos[1]
			photo3  = choosedPhotos[2]
			checkEqualPhotos(photo1, photo2, photo3, photo)

			print possibleQuestions[0] + " " + photo + " " + photo1 + " " + photo2 + " " + photo3
			print possibleQuestions[1] + " " + photo + " " + photo1 + " " + photo2 + " " + photo3

			if photosCounter.has_key(photo):
				photosCounter[photo] = photosCounter[photo] + 1
			else:
				photosCounter[photo] = 1
			if photosCounter.has_key(photo1):
				photosCounter[photo1] = photosCounter[photo1] + 1
			else:
				photosCounter[photo1] = 1
			if photosCounter.has_key(photo2):
				photosCounter[photo2] = photosCounter[photo2] + 1
			else:
				photosCounter[photo2] = 1
			if photosCounter.has_key(photo3):
				photosCounter[photo3] = photosCounter[photo3] + 1
			else:
				photosCounter[photo3] = 1
			

	print str(photosLeft)						
	print str(photosCounter)

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Uso: <arquivo com definições das tarefas>"
		sys.exit(1)

	dataFile = open(sys.argv[1], 'r')
	lines = dataFile.readlines()

	readInput(lines)
	#evaluateBasedOnControlGroup()
	createMaxDiffDesign()
