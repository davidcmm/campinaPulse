# coding=utf-8
# Prepares tasks and users data for classification

import sys
from sets import Set
import random
import numpy
import json
import csv

completeTie = 'equal'
left = 'left'
right = 'right'
notKnown = 'notknown'

def readTasksExecution(lines, tasksDefinitions, usersDefinitions, imagesDefinitions):

	#Header
	print "question\tphoto1\tphoto2\tchoice\tuserID\tage\tgender\tincome\teducation\tcity\tmarital\tstreet_wid1\tmov_cars1\tpark_cars1\tmov_ciclyst1\tlandscape1\tbuild_ident1\ttrees1\tbuild_height1\tdiff_build1\tpeople1\tgraffiti1\tbairro1\tstreet_wid2\tmov_cars2\tpark_cars2\tmov_ciclyst2\tlandscape2\tbuild_ident2\ttrees2\tbuild_height2\tdiff_build2\tpeople2\tgraffiti2\tbairro2"

	for line in lines:
		data = line.split("+")
		executionID = data[0].strip(' \t\n\r')
		taskID = data[3].strip(' \t\n\r"')
		userID = data[4].strip(' \t\n\r"')
		userAnswer = data[9].strip(' \t\n\r"')

		if usersDefinitions.has_key(userID):
			userInfo = usersDefinitions[userID]#Retrieving user data

			if executionID[0].lower() == 'n':#MaxDiff design
				answer = json.loads(userAnswer)
				question = answer['question'].strip(' \t\n\r"')
				photo1 = answer['theMost'].strip(' \t\n\r"')
				photo2 = answer['theLess'].strip(' \t\n\r"')

				taskDef = tasksDefinitions[taskID]
				photos = Set( [taskDef['url_c'].strip(' \t\n\r"'), taskDef['url_b'].strip(' \t\n\r"'), taskDef['url_a'].strip(' \t\n\r"'), taskDef['url_d'].strip(' \t\n\r"')] )

				if photo1 != completeTie:
					photos.remove(photo1)
					photos.remove(photo2)
				else:
					photo1 = photos.pop()
					photo2 = photos.pop()
			
				photo3 = photos.pop()
				photo4 = photos.pop()

				photo1Info = imagesDefinitions["/".join(photo1.split("/")[5:])]			
				photo2Info = imagesDefinitions["/".join(photo2.split("/")[5:])]
				photo3Info = imagesDefinitions["/".join(photo3.split("/")[5:])]
				photo4Info = imagesDefinitions["/".join(photo4.split("/")[5:])]

				#Saving votes from task-run
				if photo1 != completeTie:
					print(question + "\t" + photo1 + "\t" + photo2 + "\t" + "-1" + "\t" + userID + "\t" + "\t".join(userInfo) + "\t" + "\t".join(photo1Info).strip(' \t\n\r') + "\t" + "\t".join(photo2Info).strip(' \t\n\r'))
					print(question + "\t" + photo1 + "\t" + photo3 + "\t" + "-1" + "\t" + userID + "\t" + "\t".join(userInfo) + "\t" + "\t".join(photo1Info).strip(' \t\n\r') + "\t" + "\t".join(photo3Info).strip(' \t\n\r'))
					print(question + "\t" + photo1 + "\t" + photo4 + "\t" + "-1" + "\t" + userID + "\t" + "\t".join(userInfo) + "\t" + "\t".join(photo1Info).strip(' \t\n\r') + "\t" + "\t".join(photo4Info).strip(' \t\n\r'))
					print(question + "\t" + photo2 + "\t" + photo3 + "\t" + "1" + "\t" + userID + "\t" + "\t".join(userInfo) + "\t" + "\t".join(photo2Info).strip(' \t\n\r') + "\t" + "\t".join(photo3Info).strip(' \t\n\r'))
					print(question + "\t" + photo2 + "\t" + photo4 + "\t" + "1" + "\t" + userID + "\t" + "\t".join(userInfo) + "\t" + "\t".join(photo2Info).strip(' \t\n\r') + "\t" + "\t".join(photo4Info).strip(' \t\n\r'))
					print(question + "\t" + photo3 + "\t" + photo4 + "\t" + "1" + "\t" + userID + "\t" + "\t".join(userInfo) + "\t" + "\t".join(photo3Info).strip(' \t\n\r') + "\t" + "\t".join(photo4Info).strip(' \t\n\r'))
				else:
					print(question + "\t" + photo1 + "\t" + photo2 + "\t" + "0" + "\t" + userID + "\t" + "\t".join(userInfo) + "\t" + "\t".join(photo1Info).strip(' \t\n\r') + "\t" + "\t".join(photo2Info).strip(' \t\n\r'))
					print(question + "\t" + photo1 + "\t" + photo3 + "\t" + "0" + "\t" + userID + "\t" + "\t".join(userInfo) + "\t" + "\t".join(photo1Info).strip(' \t\n\r') + "\t" + "\t".join(photo3Info).strip(' \t\n\r'))
					print(question + "\t" + photo1 + "\t" + photo4 + "\t" + "0" + "\t" + userID + "\t" + "\t".join(userInfo) + "\t" + "\t".join(photo1Info).strip(' \t\n\r') + "\t" + "\t".join(photo4Info).strip(' \t\n\r'))
					print(question + "\t" + photo2 + "\t" + photo3 + "\t" + "0" + "\t" + userID + "\t" + "\t".join(userInfo) + "\t" + "\t".join(photo2Info).strip(' \t\n\r') + "\t" + "\t".join(photo3Info).strip(' \t\n\r'))
					print(question + "\t" + photo2 + "\t" + photo4 + "\t" + "0" + "\t" + userID + "\t" + "\t".join(userInfo) + "\t" + "\t".join(photo2Info).strip(' \t\n\r') + "\t" + "\t".join(photo4Info).strip(' \t\n\r'))
					print(question + "\t" + photo3 + "\t" + photo4 + "\t" + "0" + "\t" + userID + "\t" + "\t".join(userInfo) + "\t" + "\t".join(photo3Info).strip(' \t\n\r') + "\t" + "\t".join(photo4Info).strip(' \t\n\r'))
			
			else:#Pairwise comparison
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

				photo1Info = imagesDefinitions["/".join(photo1.split("/")[5:])]			
				photo2Info = imagesDefinitions["/".join(photo2.split("/")[5:])]
		
				if answer.lower() == left:
					print(question + "\t" + photo1 + "\t" + photo2 + "\t" + "-1" + "\t" + userID + "\t" + "\t".join(userInfo) + "\t" + "\t".join(photo1Info).strip(' \t\n\r') + "\t" + "\t".join(photo2Info).strip(' \t\n\r'))
				elif answer.lower() == right:
					print(question + "\t" + photo1 + "\t" + photo2 + "\t" + "1" + "\t" + userID + "\t" + "\t".join(userInfo) + "\t" + "\t".join(photo1Info).strip(' \t\n\r') + "\t" + "\t".join(photo2Info).strip(' \t\n\r'))
				else:
					#print(photo1)
					#print(photo2)
					#print(" ".join(userInfo))
					#print(photo1Info)
					#print(" ".join(photo2Info))
					print(question + "\t" + photo1 + "\t" + photo2 + "\t" + "0" + "\t" + userID + "\t" + "\t".join(userInfo) + "\t" + "\t".join(photo1Info).strip(' \t\n\r') + "\t" + "\t".join(photo2Info).strip(' \t\n\r'))

	return tasksDef

def readTasksDefinitions(linesTasks):
	tasksDef = {}

	for line in linesTasks:
		data = line.split("+")
		taskID = data[0].strip(' \t\n\r')
		currentDef = json.loads(data[7].strip(' \t\n\r\"'))

		tasksDef[taskID] = currentDef
	
	return tasksDef


possibleIncomesOld = ["Baixa (at\u00e9 R$ 1.449,99)", "M\u00e9dia Baixa (R$ 1.450 a R$ 2.899,99)", "M\u00e9dia (R$ 2.900 a R$ 7.249,99)", "M\u00e9dia Alta (R$ 7.250 a R$ 14.499,99)", "Alta (R$ 14.500 ou mais)"]
possibleIncomesNew = ["baixa", "media baixa", "media", "media alta", "alta"]

def readUsersDefinitions(linesUsers):
	usersDef = {}

	for line in linesUsers:
		data = line.split("|")
		userID = data[0].strip(' \t\n\r')
		userInfoData = data[1].strip(' \t\n\r')

		if len(userInfoData) == 0:
			#usersDef[userID] = ['', '', '', '', '', '', '', '[]']
			continue
		else:
			userInfo = userInfoData.split("+")
			if len(userInfo[0]) == 0 and  len(userInfo[1]) == 0 and len(userInfo[2]) == 0 and len(userInfo[3]) == 0 and len(userInfo[4]) == 0 and len(userInfo[5]) == 0 and len(userInfo[6]) == 0:
				#usersDef[userID] = ['', '', '', '', '', '', '', '[]']
				continue
			else:
				gender = ""
				if userInfo[1][0].lower() == 'm':
					gender = "masculino"
				else:
					gender = "feminino"

				income = ""
				if userInfo[2] == possibleIncomesOld[0] or userInfo[2] == possibleIncomesNew[0]:
					income = "baixa"
				elif userInfo[2] == possibleIncomesOld[1] or userInfo[2] == possibleIncomesNew[1]:
					income = "media baixa"
				elif userInfo[2] == possibleIncomesOld[2] or userInfo[2] == possibleIncomesNew[2]:
					income = "media"
				elif userInfo[2] == possibleIncomesOld[3] or userInfo[2] == possibleIncomesNew[3]:
					income = "media alta"
				elif userInfo[2] == possibleIncomesOld[4] or userInfo[2] == possibleIncomesNew[4]:
					income = "alta"

				educ = ""
				if userInfo[3][0].lower() == 'e':
					educ = "ensino medio"
				elif userInfo[3][0].lower() == 'g':
					educ = "graduacao"
				elif userInfo[3][0].lower() == 'm':
					educ = "mestrado"
				elif userInfo[3][0].lower() == 'd':
					educ = "doutorado"

				#User profile: age, gender, income, education, city, marital status
				usersDef[userID] = [userInfo[0].strip(' \t\n\r'), gender, income, educ, userInfo[4].lower(), userInfo[6].lower()]
	
	return usersDef


def readImagesDefinitions(lines):
	imagesDef = {}
	for line in lines:
		data = line.split(" ")
		imagesDef[data[0]] = data[1:]

	return imagesDef


if __name__ == "__main__":
	if len(sys.argv) < 4:
		print "Uso: <arquivo com execuções das tarefas> <arquivo com definicoes de tarefas> <arquivo com dados dos usuarios> <arquivos com dados das imagens>"
		sys.exit(1)

	tasksDef = readTasksDefinitions(open(sys.argv[2], 'r').readlines())
	usersDef = readUsersDefinitions(open(sys.argv[3], 'r').readlines())
	imagesDef = readImagesDefinitions(open(sys.argv[4], 'r').readlines())

	tasksExecution = readTasksExecution(open(sys.argv[1], 'r').readlines(), tasksDef, usersDef, imagesDef)
