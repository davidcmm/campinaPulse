import sys
from sets import Set

possibleIncomes = ["Baixa (at\u00e9 R$ 1.449,99)", "M\u00e9dia Baixa (R$ 1.450 a R$ 2.899,99)", "M\u00e9dia (R$ 2.900 a R$ 7.249,99)", "M\u00e9dia Alta (R$ 7.250 a R$ 14.499,99)", "Alta (R$ 14.500 ou mais)"]

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

		if len(data[1]) > 0:
			#Separating by age
			age = int(profile[0].lower())
			if age <= 24:
				young.add(userID)
				tasksYoung.update(tasksIDSeg)
				tasksYoung.update(tasksIDAgra)
			elif age >=35 and age <=44:
				old.add(userID)
				tasksOld.update(tasksIDSeg)
				tasksOld.update(tasksIDAgra)

			#Separating by sex
			#print str(profile)+"\t"+str(len(data[1]))
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
			income = profile[2]
			if income == possibleIncomes[0] or income == possibleIncomes[1]:
				low.add(userID)
				tasksLow.update(tasksIDSeg)
				tasksLow.update(tasksIDAgra)
			elif income == possibleIncomes[2] or income == possibleIncomes[3]:
				high.add(userID)
				tasksHigh.update(tasksIDSeg)
				tasksHigh.update(tasksIDAgra)
		
			#Separating by education degree
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
	singleFile.write(str(list(tasksSingle.intersection(tasksMarried)))+"\n")
	for userID in single:
		singleFile.write(str(userID)+"\n")#FIXME: add tasksID
	singleFile.close()
	marriedFile = open("casado.dat", "w")
	marriedFile.write(str(list(tasksSingle.intersection(tasksMarried)))+"\n")
	for userID in married:
		marriedFile.write(str(userID)+"\n")
	marriedFile.close()

	femFile = open("feminino.dat", "w")
	femFile.write(str(list(tasksFem.intersection(tasksMasc)))+"\n")
	for userID in feminine:
		femFile.write(str(userID)+"\n")
	femFile.close()
	masFile = open("masculino.dat", "w")
	masFile.write(str(list(tasksFem.intersection(tasksMasc)))+"\n")
	for userID in masculine:
		masFile.write(str(userID)+"\n")
	masFile.close()

	youngFile = open("jovem.dat", "w")
	youngFile.write(str(list(tasksYoung.intersection(tasksOld)))+"\n")
	for userID in young:
		youngFile.write(str(userID)+"\n")
	youngFile.close()
	oldFile = open("adulto.dat", "w")
	oldFile.write(str(list(tasksYoung.intersection(tasksOld)))+"\n")
	for userID in old:
		oldFile.write(str(userID)+"\n")
	oldFile.close()

	lowFile = open("baixa.dat", "w")
	lowFile.write(str(list(tasksLow.intersection(tasksHigh)))+"\n")
	for userID in low:
		lowFile.write(str(userID)+"\n")
	lowFile.close()
	highFile = open("media.dat", "w")
	highFile.write(str(list(tasksLow.intersection(tasksHigh)))+"\n")
	for userID in high:
		highFile.write(str(userID)+"\n")
	highFile.close()

	highSchoolFile = open("medio.dat", "w")
	highSchoolFile.write(str(list(tasksHighSchool.intersection(tasksPosGrad)))+"\n")
	for userID in highSchool:
		highSchoolFile.write(str(userID)+"\n")
	highSchoolFile.close()
	posGradFile = open("posgrad.dat", "w")
	posGradFile.write(str(list(tasksHighSchool.intersection(tasksPosGrad)))+"\n")
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


if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Uso: <arquivo com ids dos usuarios, das tarefas e perfis dos usuarios>"
		sys.exit(1)
	dataFile = open(sys.argv[1], 'r')
	lines = dataFile.readlines()
	dataFile.close()

	usersTasks = parseUserData(lines)

