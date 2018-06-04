# coding=utf-8
import sys
from sets import Set
import re

possibleIncomesOld = ["Baixa (at\u00e9 R$ 1.449,99)", "M\u00e9dia Baixa (R$ 1.450 a R$ 2.899,99)", "M\u00e9dia (R$ 2.900 a R$ 7.249,99)", "M\u00e9dia Alta (R$ 7.250 a R$ 14.499,99)", "Alta (R$ 14.500 ou mais)"]
possibleIncomesNew = ["baixa", "media baixa", "media", "media alta", "alta"]

def parseUserData(lines, not_local_ids, manual_gender_ids):
	""" Reading user data """
	feminine = Set([])
	tasks_fem = Set([])
	#fSeg = Set([])
	masculine = Set([])
	tasks_masc = Set([])
	#mSeg = Set([])

	single = Set([])
	tasks_single = Set([])
	#sSeg = Set([])
	married = Set([])
	tasks_married = Set([])
	#cSeg = Set([])

	low = Set([])
	tasks_low = Set([])
	high = Set([])
	tasks_high = Set([])
	
	young = Set([])
	tasks_young = Set([])
	old = Set([])
	tasks_old = Set([])

	highSchool = Set([])
	tasks_highSchool = Set([])
	posGrad = Set([])
	tasks_posgrad = Set([])
		
	centro = Set([])
	tasks_centro = Set([])
	notCentro = Set([])
	tasks_notcentro = Set([])

	catole = Set([])
	tasks_catole = Set([])
	notCatole = Set([])
	tasks_notcatole = Set([])

	liberdade = Set([])
	tasks_liberdade = Set([])
	notLiberdade = Set([])
	tasks_notliberdade = Set([])

	campina = Set([])
	tasks_campina = Set([])
	notCampina = Set([])
	tasks_notcampina = Set([])

	cities = []

	for line in lines:
		data = line.split("|")
		userID = int(data[0])
		profile = data[1].split("+")
		
		tasksIDAgra = eval(data[2])
		tasksIDSeg = eval(data[3])

		if len(data[1]) > 0:
			#Separating by age
			if len(profile[0]) > 0 and profile[0] != "None":
				age = int(profile[0].lower())
				if age <= 24 and age > 0:
					young.add(userID)
					tasks_young.update(tasksIDSeg)
					tasks_young.update(tasksIDAgra)
				#elif age >= 35 and age <= 44:
				elif age >= 25:
					old.add(userID)
					tasks_old.update(tasksIDSeg)
					tasks_old.update(tasksIDAgra)

			#Separating by sex
			#print str(profile)+"\t"+str(len(data[1]))
			if len(profile[1]) > 0 and profile[1] != "None":
				sex = profile[1].lower()
			elif str(userID) in manual_gender_ids:
				sex = manual_gender_ids[str(userID)]

			if sex[0] == 'f':
				feminine.add(userID)
				tasks_fem.update(tasksIDSeg)
				tasks_fem.update(tasksIDAgra)
			elif sex[0] =='m':
				masculine.add(userID)
				tasks_masc.update(tasksIDSeg)
				tasks_masc.update(tasksIDAgra)
				
		
			#Separating by income
			if len(profile[2]) > 0 and profile[2] != "None":
				income = profile[2]
				if income == possibleIncomesOld[0] or income == possibleIncomesOld[1] or income == possibleIncomesNew[0] or income == possibleIncomesNew[1]:
					low.add(userID)
					tasks_low.update(tasksIDSeg)
					tasks_low.update(tasksIDAgra)
				elif income == possibleIncomesOld[2] or income == possibleIncomesOld[3] or income == possibleIncomesNew[2] or income == possibleIncomesNew[3]:
					high.add(userID)
					tasks_high.update(tasksIDSeg)
					tasks_high.update(tasksIDAgra)
		
			#Separating by education degree
			if len(profile[3]) > 0 and profile[3] != "None":
				education = profile[3]
				if education[0].lower() == 'e':
					highSchool.add(userID)
					tasks_highSchool.update(tasksIDSeg)
					tasks_highSchool.update(tasksIDAgra)
				elif education[0].lower == 'm' or education[0].lower() == 'd':
					posGrad.add(userID)
					tasks_posgrad.update(tasksIDSeg)
					tasks_posgrad.update(tasksIDAgra)

			#Separating by being from Campina Grande or not
			if len(profile[4]) > 0 and profile[4] != "None":
				city = profile[4]
				city = re.sub(r'\s{2,}', " ", city)#Replacing 2 or more spaces that are together with a single space

				cities.append(city.strip(" \n"))
				knowcampina = profile[8].lower()
				howknowcampina = profile[9].lower()
				
				if (city.lower().find("campina grande") > -1 and city.lower().find("sul") == -1) or (str(userID) in not_local_ids):#City is exactly Campina Grande and not Campina Grande do Sul - PR
					campina.add(userID)
					tasks_campina.update(tasksIDSeg)
					tasks_campina.update(tasksIDAgra)
				else:
					if len(knowcampina) > 0 and len(howknowcampina) > 0 and "yes" in knowcampina and ("live" in howknowcampina or "study" in howknowcampina or "work" in howknowcampina):
						campina.add(userID)
						tasks_campina.update(tasksIDSeg)
						tasks_campina.update(tasksIDAgra)
					else:
						notCampina.add(userID)
						tasks_notcampina.update(tasksIDSeg)
						tasks_notcampina.update(tasksIDAgra)

			#Separating by relationship
			if len(profile[6]) > 0 and profile[6] != "None":
				rel = profile[6].lower()
				if rel[0] == 's':
					single.add(userID)
					tasks_single.update(tasksIDSeg)
					tasks_single.update(tasksIDAgra)
				elif rel[0] == 'c':
					married.add(userID)
					tasks_married.update(tasksIDSeg)
					tasks_married.update(tasksIDAgra)

			#Separating by known places
			if len(profile[7]) > 0 and profile[7] != "None":
				places = profile[7].lower()
				if len(places) > 0:
					if "cen" in places.strip():
						centro.add(userID)
						tasks_centro.update(tasksIDSeg)
						tasks_centro.update(tasksIDAgra)
					else:
						notCentro.add(userID)
						tasks_notcentro.update(tasksIDSeg)
						tasks_notcentro.update(tasksIDAgra)

					if "lib" in places.strip():
						liberdade.add(userID)
						tasks_liberdade.update(tasksIDSeg)
						tasks_liberdade.update(tasksIDAgra)
					else:
						notLiberdade.add(userID)
						tasks_notliberdade.update(tasksIDSeg)
						tasks_notliberdade.update(tasksIDAgra)

					if "cat" in places.strip():
						catole.add(userID)
						tasks_catole.update(tasksIDSeg)
						tasks_catole.update(tasksIDAgra)
					else:
						notCatole.add(userID)
						tasks_notcatole.update(tasksIDSeg)
						tasks_notcatole.update(tasksIDAgra)

	cities_file = open("cities.dat", "w")
	for city in cities:
		cities_file.write(str(city)+"\n")
	cities_file.close()

	single_file = open("solteiro.dat", "w")
	#single_file.write(str(list(tasks_single.intersection(tasks_married)))+"\n")
	single_file.write("[]\n")
	for userID in single:
		single_file.write(str(userID)+"\n")#FIXME: add tasksID
	single_file.close()
	married_file = open("casado.dat", "w")
	#married_file.write(str(list(tasks_single.intersection(tasks_married)))+"\n")
	married_file.write("[]\n")
	for userID in married:
		married_file.write(str(userID)+"\n")
	married_file.close()

	fem_file = open("feminino.dat", "w")
	#fem_file.write(str(list(tasks_fem.intersection(tasks_masc)))+"\n")
	fem_file.write("[]\n")
	for userID in feminine:
		fem_file.write(str(userID)+"\n")
	fem_file.close()
	mas_file = open("masculino.dat", "w")
	#mas_file.write(str(list(tasks_fem.intersection(tasks_masc)))+"\n")
	mas_file.write("[]\n")
	for userID in masculine:
		mas_file.write(str(userID)+"\n")
	mas_file.close()

	young_file = open("jovem.dat", "w")
#	young_file.write(str(list(tasks_young.intersection(tasks_old)))+"\n")
	young_file.write("\n")
	for userID in young:
		young_file.write(str(userID)+"\n")
	young_file.close()
	old_file = open("adulto.dat", "w")
#	old_file.write(str(list(tasks_young.intersection(tasks_old)))+"\n")
	old_file.write("[]\n")
	for userID in old:
		old_file.write(str(userID)+"\n")
	old_file.close()

	low_file = open("baixa.dat", "w")
	#low_file.write(str(list(tasks_low.intersection(tasks_high)))+"\n")
	low_file.write("[]\n")
	for userID in low:
		low_file.write(str(userID)+"\n")
	low_file.close()
	high_file = open("media.dat", "w")
#	high_file.write(str(list(tasks_low.intersection(tasks_high)))+"\n")
	high_file.write("[]\n")
	for userID in high:
		high_file.write(str(userID)+"\n")
	high_file.close()

	high_school_file = open("medio.dat", "w")
#	high_school_file.write(str(list(tasks_highSchool.intersection(tasks_posgrad)))+"\n")
	high_school_file.write("[]\n")
	for userID in highSchool:
		high_school_file.write(str(userID)+"\n")
	high_school_file.close()
	pos_grad_file = open("posgrad.dat", "w")
#	pos_grad_file.write(str(list(tasks_highSchool.intersection(tasks_posgrad)))+"\n")
	pos_grad_file.write("[]\n")
	for userID in high:
		pos_grad_file.write(str(userID)+"\n")
	pos_grad_file.close()


	campina_file = open("campina.dat", "w")
	campina_file.write("[]\n")
	for userID in campina:
		campina_file.write(str(userID)+"\n")
	campina_file.close()

	notcampina_file = open("notcampina.dat", "w")
	notcampina_file.write("[]\n")
	for userID in notCampina:
		notcampina_file.write(str(userID)+"\n")
	notcampina_file.close()

	centro_file = open("centro.dat", "w")
	centro_file.write("[]\n")
	for userID in centro:
		centro_file.write(str(userID)+"\n")
	centro_file.close()
	notcentro_file = open("notcentro.dat", "w")
	notcentro_file.write("[]\n")
	for userID in notCentro:
		notcentro_file.write(str(userID)+"\n")
	notcentro_file.close()

	liberdade_file = open("liberdade.dat", "w")
	liberdade_file.write("[]\n")
	for userID in liberdade:
		liberdade_file.write(str(userID)+"\n")
	liberdade_file.close()
	notliberdade_file = open("notliberdade.dat", "w")
	notliberdade_file.write("[]\n")
	for userID in notLiberdade:
		notliberdade_file.write(str(userID)+"\n")
	notliberdade_file.close()

	catole_file = open("catole.dat", "w")
	catole_file.write("[]\n")
	for userID in catole:
		catole_file.write(str(userID)+"\n")
	catole_file.close()
	notcatole_file = open("notcatole.dat", "w")
	notcatole_file.write("[]\n")
	for userID in notCatole:
		notcatole_file.write(str(userID)+"\n")
	notcatole_file.close()

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
	if len(sys.argv) < 4:
		print "Uso: separa <arquivo com ids dos usuarios, das tarefas e perfis dos usuarios> <lista de usuários marcados como não locais sendo locais> <lista de usuários com sexo> ou mix <serie de arquivos com ids de usuarios>"
		sys.exit(1)

	mode = sys.argv[1]
	
	if mode.lower() == "separa":	#Parse input file with ids, tasks and profiles to separte per group!
		dataFile = open(sys.argv[2], 'r')
		lines = dataFile.readlines()
		dataFile.close()

		not_local_ids_file = open(sys.argv[3], 'r')
		not_local_ids = []
		for id in not_local_ids_file.readlines():
			not_local_ids.append(id.strip(" \n"))
		not_local_ids_file.close()

		manual_gender_ids_file = open(sys.argv[4], 'r')
		manual_gender_ids = {}
		for id in manual_gender_ids_file.readlines():
			data = id.strip(" \n").split(":")
			manual_gender_ids[data[0]] = data[1].lower()
		manual_gender_ids_file.close() 

		usersTasks = parseUserData(lines, not_local_ids, manual_gender_ids)
	else: #Mix files with users ids into only one file
		createOneFileWithAllProfiledUsers(sys.argv[2:])
