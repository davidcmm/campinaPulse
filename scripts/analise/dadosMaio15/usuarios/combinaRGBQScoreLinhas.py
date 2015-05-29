# coding=utf-8
# Combines RGB, QScore and amount of lines for each photo according to input data

import sys

#possible questions
possibleQuestions = ["agrad%C3%A1vel?", "seguro?"]
possibleIncomes = ["Baixa (at\u00e9 R$ 1.449,99)", "M\u00e9dia Baixa (R$ 1.450 a R$ 2.899,99)", "M\u00e9dia (R$ 2.900 a R$ 7.249,99)", "M\u00e9dia Alta (R$ 7.250 a R$ 14.499,99)", "Alta (R$ 14.500 ou mais)"]

if __name__ == "__main__":
	if len(sys.argv) < 4:
		print "Uso: <arquivo com rgb> <arquivo com qscore> <arquivo com linhas> <com perfil?>"
		sys.exit(1)

	if len(sys.argv) > 4:
		withProfile = bool(sys.argv[4])
	else:
		withProfile = False

	rgbs = open(sys.argv[1], "r")
	qscores = open(sys.argv[2], "r")
	linesCounting = open(sys.argv[3], "r")
	
	if withProfile:#Reading user profile data from file
		usersProfileLines = open("usersInfo.dat", "r").readlines()
		userProfile = {}

		for line in usersProfileLines:
			data = line.split("|")
			userID = data[0].strip()
			profile = data[1].split("+")
			#age, sex, income, education, lives, time, civil status, knows
			if len(profile) > 1:
				userProfile[userID] = [int(profile[0]), profile[1], profile[2], profile[3], profile[4], int(profile[5]), profile[6], profile[7]]
			else:
				userProfile[userID] = []

	qscoreLines = qscores.readlines()
	rgbLines = rgbs.readlines()
	linesCountingLines = linesCounting.readlines()	

	#Reading qscores
	qscoreDic = {possibleQuestions[0]:{}, possibleQuestions[1]: {}}	
	usersDic = {possibleQuestions[0]:{}, possibleQuestions[1]: {}}	
	for line in qscoreLines:
		data = line.split("\t")
		photo = data[1].split("/")[5]+"/"+data[1].split("/")[6]#Saving district and street
		qscore = data[2]

		qscoreDic[data[0].strip()][photo.strip()] = qscore.strip()

		if withProfile:
			usersDic[data[0].strip()][photo.strip()] = []
			for ID in data[3:]:
				#print str(ID)+"\t"+photo+"\t"+data[0]
				usersDic[data[0].strip()][photo.strip()].append(ID.strip("\n").strip("'"))
	
	#print str(usersDic)

	#Reading rgb data
	rgbDic = {}	
	for line in rgbLines:
		data = line.split(" ")
		#print data
		photo = data[0]
		red = data[1]
		green = data[2]
		blue = data[3]
		
		rgbDic[photo.strip()] = (red.strip(), green.strip(), blue.strip())


	#Reading lines counting data
	linesCountingDic = {}	
	for line in linesCountingLines:
		data = line.split("\t")
		#print data
		photo = data[0]
		diagonal = data[1]
		horizontal = data[2]
		vertical = data[3]
		
		linesCountingDic[photo.strip()] = (diagonal.strip(), horizontal.strip(), vertical.strip())

	#Writing outputFile with qscores and rgb
	outputFile = open("rgbQScoreAgrad.dat","w")
	if withProfile:
		outputFile.write("foto\tqscore\tred\tgreen\tblue\tdiag\thor\tvert\thasYoung\thasOld\thasFemale\thasMale\thasLowClass\thasMLowClass\thasMClass\thasMHighClass\thasHighClass\thasGraduated\thasHighSchool\thasMaster\thasPHD\thasSingle\thasDivorced\thasWidower\thasMarried\tknowsCenter\tknowsLiberdade\tknowsCatole\n")
	else:
		outputFile.write("foto\tqscore\tred\tgreen\tblue\tdiag\thor\tvert\n")
	for photo in qscoreDic[possibleQuestions[0]].keys():
		rgb = rgbDic[photo.split("/")[1]]
		lines = linesCountingDic[photo.split("/")[1]]
		qscore = qscoreDic[possibleQuestions[0]][photo]
		if not withProfile:
			outputFile.write(photo+"\t"+qscore+"\t"+rgb[0]+"\t"+rgb[1]+"\t"+rgb[2]+"\t"+lines[0]+"\t"+lines[1]+"\t"+lines[2]+"\n")
		else:
			users = usersDic[possibleQuestions[0]][photo]
			hasYoung = False
			hasOld = False
			hasMale = False
			hasFemale = False
			hasMarried = False
			hasLowClass = False
			hasMLowClass = False
			hasMClass = False
			hasMHighClass = False
			hasHighClass = False
			hasGraduated = False
			hasHighSchool = False
			hasMaster = False
			hasPHD = False
			hasSingle = False
			hasDivorced = False
			hasWidower = False
			knowsCenter = False
			knowsCatole = False
			knowsLiberdade = False

			for ID in users:
				#age, sex, income, education, lives, time, civil status, knows
				#print str(ID.strip())
				if userProfile.has_key(ID.strip()):
					profile = userProfile[ID.strip()]
					#print str(ID) + "\t" + str(photo) + str(profile)
					print str(profile)

					if len(profile) > 0:
						if profile[0] <= 24:
							hasYoung = True
						elif profile[0] >=35 and profile[0] <=44:
							hasOld = True

						if profile[1].lower()[0] == 'f':
							hasFemale = True
						elif profile[1].lower()[0] == 'm':
							hasMale = True

						if profile[2] == possibleIncomes[0]:
							hasLowClass = True
						elif profile[2] == possibleIncomes[1]:
							hasMLowClass = True
						elif profile[2] == possibleIncomes[2]:
							hasMClass = True
						elif profile[2] == possibleIncomes[3]:
							hasMHighClass = True
						elif profile[2] == possibleIncomes[4]:
							hasHighClass = True

						if profile[3].lower()[0] == "g":
							hasGraduated = True
						elif profile[3].lower()[0] == "e":
							hasHighSchoool = True
						elif profile[3].lower()[0] == "m":
							hasMaster = True
						elif profile[3].lower()[0] == "d":
							hasPHD = True

						if profile[6].lower()[0] == 's':
							hasSingle = True
						elif profile[6].lower()[0] == 'd':
							hasDivorced = True
						elif profile[6].lower()[0] == 'v':
							hasWidower = True
						elif profile[6].lower()[0] == 'c':
							hasMarried = True

						if 'cen' in profile[7]:
							knowsCenter = True
						if 'lib' in profile[7]: 
							knowsLiberdade = True
						if 'cat' in profile[7]:
							knowsCatole = True
			outputFile.write(photo+"\t"+qscore+"\t"+rgb[0]+"\t"+rgb[1]+"\t"+rgb[2]+"\t"+lines[0]+"\t"+lines[1]+"\t"+lines[2]+"\t"+str(hasYoung)+"\t"+str(hasOld)+"\t"+str(hasFemale)+"\t"+str(hasMale)+"\t"+str(hasLowClass)+"\t"+str(hasMLowClass)+"\t"+str(hasMClass)+"\t"+str(hasMHighClass)+"\t"+str(hasHighClass)+"\t"+str(hasGraduated)+"\t"+str(hasHighSchool)+"\t"+str(hasMaster)+"\t"+str(hasPHD)+"\t"+str(hasSingle)+"\t"+str(hasDivorced)+"\t"+str(hasWidower)+"\t"+str(hasMarried)+"\t"+str(knowsCenter)+"\t"+str(knowsLiberdade)+"\t"+str(knowsCatole)+"\n")

	#Writing outputFile with qscores and rgb
	outputFile = open("rgbQScoreSeg.dat","w")
	if withProfile:
		outputFile.write("foto\tqscore\tred\tgreen\tblue\tdiag\thor\tvert\thasYoung\thasOld\thasFemale\thasMale\thasLowClass\thasMLowClass\thasMClass\thasMHighClass\thasHighClass\thasGraduated\thasHighSchool\thasMaster\thasPHD\thasSingle\thasDivorced\thasWidower\thasMarried\tknowsCenter\tknowsLiberdade\tknowsCatole\n")
	else:
		outputFile.write("foto\tqscore\tred\tgreen\tblue\tdiag\thor\tvert\n")
	for photo in qscoreDic[possibleQuestions[1]].keys():
		rgb = rgbDic[photo.split("/")[1]]
		lines = linesCountingDic[photo.split("/")[1]]
		qscore = qscoreDic[possibleQuestions[1]][photo]

		if not withProfile:
			outputFile.write(photo+"\t"+qscore+"\t"+rgb[0]+"\t"+rgb[1]+"\t"+rgb[2]+"\t"+lines[0]+"\t"+lines[1]+"\t"+lines[2]+"\n")
		else:
			users = usersDic[possibleQuestions[1]][photo]
			hasYoung = False
			hasOld = False
			hasMale = False
			hasFemale = False
			hasMarried = False
			hasLowClass = False
			hasMLowClass = False
			hasMClass = False
			hasMHighClass = False
			hasHighClass = False
			hasGraduated = False
			hasHighSchool = False
			hasMaster = False
			hasPHD = False
			hasSingle = False
			hasDivorced = False
			hasWidower = False
			knowsCenter = False
			knowsCatole = False
			knowsLiberdade = False

			for ID in users:
				#age, sex, income, education, lives, time, civil status, knows
				if userProfile.has_key(ID.strip()):
					profile = userProfile[ID.strip()]
				
					if len(profile) > 0:
						if profile[0] <= 24:
							hasYoung = True
						elif profile[0] >=35 and profile[0] <=44:
							hasOld = True

						if profile[1].lower()[0] == 'f':
							hasFemale = True
						elif profile[1].lower()[0] == 'm':
							hasMale = True

						if profile[2] == possibleIncomes[0]:
							hasLowClass = True
						elif profile[2] == possibleIncomes[1]:
							hasMLowClass = True
						elif profile[2] == possibleIncomes[2]:
							hasMClass = True
						elif profile[2] == possibleIncomes[3]:
							hasMHighClass = True
						elif profile[2] == possibleIncomes[4]:
							hasHighClass = True

						if profile[3].lower()[0] == "g":
							hasGraduated = True
						elif profile[3].lower()[0] == "e":
							hasHighSchoool = True
						elif profile[3].lower()[0] == "m":
							hasMaster = True
						elif profile[3].lower()[0] == "d":
							hasPHD = True

						if profile[6].lower()[0] == 's':
							hasSingle = True
						elif profile[6].lower()[0] == 'd':
							hasDivorced = True
						elif profile[6].lower()[0] == 'v':
							hasWidower = True
						elif profile[6].lower()[0] == 'c':
							hasMarried = True

						if 'cen' in profile[7]:
							knowsCenter = True
						if 'lib' in profile[7]: 
							knowsLiberdade = True
						if 'cat' in profile[7]:
							knowsCatole = True
			outputFile.write(photo+"\t"+qscore+"\t"+rgb[0]+"\t"+rgb[1]+"\t"+rgb[2]+"\t"+lines[0]+"\t"+lines[1]+"\t"+lines[2]+"\t"+str(hasYoung)+"\t"+str(hasOld)+"\t"+str(hasFemale)+"\t"+str(hasMale)+"\t"+str(hasLowClass)+"\t"+str(hasMLowClass)+"\t"+str(hasMClass)+"\t"+str(hasMHighClass)+"\t"+str(hasHighClass)+"\t"+str(hasGraduated)+"\t"+str(hasHighSchool)+"\t"+str(hasMaster)+"\t"+str(hasPHD)+"\t"+str(hasSingle)+"\t"+str(hasDivorced)+"\t"+str(hasWidower)+"\t"+str(hasMarried)+"\t"+str(knowsCenter)+"\t"+str(knowsLiberdade)+"\t"+str(knowsCatole)+"\n")
	outputFile.close()


		
