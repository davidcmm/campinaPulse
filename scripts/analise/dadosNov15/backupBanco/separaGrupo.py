import sys
from sets import Set

possibleIncomesOld = ["Baixa (at\u00e9 R$ 1.449,99)", "M\u00e9dia Baixa (R$ 1.450 a R$ 2.899,99)", "M\u00e9dia (R$ 2.900 a R$ 7.249,99)", "M\u00e9dia Alta (R$ 7.250 a R$ 14.499,99)", "Alta (R$ 14.500 ou mais)"]
possibleIncomesNew = ["baixa", "media baixa", "media", "media alta", "alta"]

def parseUserData(lines):
	""" Reading user data """
	feminine = Set([])
	tasksFem = Set([])
	#fSeg = Set([])
	masculine = Set([])
	tasksMasc = Set([])
	#mSeg = Set([])

	single = Set([])
	tasksSingle = Set([])
	#sSeg = Set([])
	married = Set([])
	tasksMarried = Set([])
	#cSeg = Set([])

	low = Set([])
	tasksLow = Set([])
	high = Set([])
	tasksHigh = Set([])
	
	young = Set([])
	tasksYoung = Set([])
	old = Set([])
	tasksOld = Set([])

	highSchool = Set([])
	tasksHighSchool = Set([])
	posGrad = Set([])
	tasksPosGrad = Set([])
		
	centro = Set([])
	tasksCentro = Set([])
	notCentro = Set([])
	tasksNotCentro = Set([])

	catole = Set([])
	tasksCatole = Set([])
	notCatole = Set([])
	tasksNotCatole = Set([])

	liberdade = Set([])
	tasksLiberdade = Set([])
	notLiberdade = Set([])
	tasksNotLiberdade = Set([])

	for line in lines:
		data = line.split("|")
		userID = int(data[0])
		profile = data[1].split("+")
		
		tasksIDAgra = eval(data[2])
		tasksIDSeg = eval(data[3])

		if len(data[1]) > 0:#TODO: Add gender based on name?
			#Separating by age
			if len(profile[0]) > 0:
				age = int(profile[0].lower())
				print age
				if age <= 24:
					young.add(userID)
					tasksYoung.update(tasksIDSeg)
					tasksYoung.update(tasksIDAgra)
				#elif age >= 35 and age <= 44:
				elif age >= 25:
					old.add(userID)
					tasksOld.update(tasksIDSeg)
					tasksOld.update(tasksIDAgra)

			#Separating by sex
			#print str(profile)+"\t"+str(len(data[1]))
			if len(profile[1]) > 0:
				sex = profile[1].lower()
				if sex[0] == 'f':
					feminine.add(userID)
					tasksFem.update(tasksIDSeg)
					tasksFem.update(tasksIDAgra)
				else:
					masculine.add(userID)
					tasksMasc.update(tasksIDSeg)
					tasksMasc.update(tasksIDAgra)
		
			#Separating by income
			if len(profile[2]) > 0:
				income = profile[2]
				if income == possibleIncomesOld[0] or income == possibleIncomesOld[1] or income == possibleIncomesNew[0] or income == possibleIncomesNew[1]:
					low.add(userID)
					tasksLow.update(tasksIDSeg)
					tasksLow.update(tasksIDAgra)
				elif income == possibleIncomesOld[2] or income == possibleIncomesOld[3] or income == possibleIncomesNew[2] or income == possibleIncomesNew[3]:
					high.add(userID)
					tasksHigh.update(tasksIDSeg)
					tasksHigh.update(tasksIDAgra)
		
			#Separating by education degree
			if len(profile[3]) > 0:
				education = profile[3]
				if education[0].lower() == 'e':
					highSchool.add(userID)
					tasksHighSchool.update(tasksIDSeg)
					tasksHighSchool.update(tasksIDAgra)
				elif education[0].lower == 'm' or education[0].lower() == 'd':
					posGrad.add(userID)
					tasksPosGrad.update(tasksIDSeg)
					tasksPosGrad.update(tasksIDAgra)

			#Separating by relationship
			if len(profile[6]) > 0:
				rel = profile[6].lower()
				if rel[0] == 's':
					single.add(userID)
					tasksSingle.update(tasksIDSeg)
					tasksSingle.update(tasksIDAgra)
				elif rel[0] == 'c':
					married.add(userID)
					tasksMarried.update(tasksIDSeg)
					tasksMarried.update(tasksIDAgra)

			#Separating by known places
			if len(profile[7]) > 0:
				places = profile[7].lower()
				if len(places) > 0:
					if "cen" in places.strip():
						centro.add(userID)
						tasksCentro.update(tasksIDSeg)
						tasksCentro.update(tasksIDAgra)
					else:
						notCentro.add(userID)
						tasksNotCentro.update(tasksIDSeg)
						tasksNotCentro.update(tasksIDAgra)

					if "lib" in places.strip():
						liberdade.add(userID)
						tasksLiberdade.update(tasksIDSeg)
						tasksLiberdade.update(tasksIDAgra)
					else:
						notLiberdade.add(userID)
						tasksNotLiberdade.update(tasksIDSeg)
						tasksNotLiberdade.update(tasksIDAgra)

					if "cat" in places.strip():
						catole.add(userID)
						tasksCatole.update(tasksIDSeg)
						tasksCatole.update(tasksIDAgra)
					else:
						notCatole.add(userID)
						tasksNotCatole.update(tasksIDSeg)
						tasksNotCatole.update(tasksIDAgra)

	singleFile = open("solteiro.dat", "w")
	#singleFile.write(str(list(tasksSingle.intersection(tasksMarried)))+"\n")
	singleFile.write("[]\n")
	for userID in single:
		singleFile.write(str(userID)+"\n")#FIXME: add tasksID
	singleFile.close()
	marriedFile = open("casado.dat", "w")
	#marriedFile.write(str(list(tasksSingle.intersection(tasksMarried)))+"\n")
	marriedFile.write("[]\n")
	for userID in married:
		marriedFile.write(str(userID)+"\n")
	marriedFile.close()

	femFile = open("feminino.dat", "w")
	#femFile.write(str(list(tasksFem.intersection(tasksMasc)))+"\n")
	femFile.write("[]\n")
	for userID in feminine:
		femFile.write(str(userID)+"\n")
	femFile.close()
	masFile = open("masculino.dat", "w")
	#masFile.write(str(list(tasksFem.intersection(tasksMasc)))+"\n")
	masFile.write("[]\n")
	for userID in masculine:
		masFile.write(str(userID)+"\n")
	masFile.close()

	youngFile = open("jovem.dat", "w")
#	youngFile.write(str(list(tasksYoung.intersection(tasksOld)))+"\n")
	youngFile.write("\n")
	for userID in young:
		youngFile.write(str(userID)+"\n")
	youngFile.close()
	oldFile = open("adulto2.dat", "w")
#	oldFile.write(str(list(tasksYoung.intersection(tasksOld)))+"\n")
	oldFile.write("[]\n")
	for userID in old:
		oldFile.write(str(userID)+"\n")
	oldFile.close()

	lowFile = open("baixa.dat", "w")
	#lowFile.write(str(list(tasksLow.intersection(tasksHigh)))+"\n")
	lowFile.write("[]\n")
	for userID in low:
		lowFile.write(str(userID)+"\n")
	lowFile.close()
	highFile = open("media.dat", "w")
#	highFile.write(str(list(tasksLow.intersection(tasksHigh)))+"\n")
	highFile.write("[]\n")
	for userID in high:
		highFile.write(str(userID)+"\n")
	highFile.close()

	highSchoolFile = open("medio.dat", "w")
#	highSchoolFile.write(str(list(tasksHighSchool.intersection(tasksPosGrad)))+"\n")
	highSchoolFile.write("[]\n")
	for userID in highSchool:
		highSchoolFile.write(str(userID)+"\n")
	highSchoolFile.close()
	posGradFile = open("posgrad.dat", "w")
#	posGradFile.write(str(list(tasksHighSchool.intersection(tasksPosGrad)))+"\n")
	posGradFile.write("[]\n")
	for userID in high:
		posGradFile.write(str(userID)+"\n")
	posGradFile.close()

	
	centroFile = open("centro.dat", "w")
	centroFile.write("[]\n")
	for userID in centro:
		centroFile.write(str(userID)+"\n")
	centroFile.close()
	notCentroFile = open("notcentro.dat", "w")
	notCentroFile.write("[]\n")
	for userID in notCentro:
		notCentroFile.write(str(userID)+"\n")
	notCentroFile.close()

	liberdadeFile = open("liberdade.dat", "w")
	liberdadeFile.write("[]\n")
	for userID in liberdade:
		liberdadeFile.write(str(userID)+"\n")
	liberdadeFile.close()
	notLiberdadeFile = open("notliberdade.dat", "w")
	notLiberdadeFile.write("[]\n")
	for userID in notLiberdade:
		notLiberdadeFile.write(str(userID)+"\n")
	notLiberdadeFile.close()

	catoleFile = open("catole.dat", "w")
	catoleFile.write("[]\n")
	for userID in catole:
		catoleFile.write(str(userID)+"\n")
	catoleFile.close()
	notCatoleFile = open("notcatole.dat", "w")
	notCatoleFile.write("[]\n")
	for userID in notCatole:
		notCatoleFile.write(str(userID)+"\n")
	notCatoleFile.close()

def createOneFileWithAllProfiledUsers(inputFiles):
	usersWithProfile = Set([])
	for userFile in inputFiles:
		dataFile = open(userFile, 'r')
		lines = dataFile.readlines()[1:]#Removing tasks list in the beginning of the file

		for line in lines:
			usersWithProfile.add(line.strip(" \n"))

	usersWithProfileFile = open("usersWProfile.dat", "w")
	usersWithProfileFile.write("[]\n")
	for userID in usersWithProfile:
		usersWithProfileFile.write(str(userID)+"\n")


if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Uso: <arquivo com ids dos usuarios, das tarefas e perfis dos usuarios> ou <serie de arquivos com ids de usuarios>"
		sys.exit(1)
	
	if len(sys.argv) == 2:	#Parse input file with ids, tasks and profiles to separte per group!
		dataFile = open(sys.argv[1], 'r')
		lines = dataFile.readlines()
		dataFile.close()

		usersTasks = parseUserData(lines)
	else: #Mix files with users ids into only one file
		createOneFileWithAllProfiledUsers(sys.argv[1:])
