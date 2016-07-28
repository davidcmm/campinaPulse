# coding=utf-8
# Prepares tasks and users data for classification

import sys
from sets import Set
import random
import numpy
import json
import csv

completeTie = 'equal'
left = 'Left'
right = 'Right'
notKnown = 'NotKnown'

def readTasksExecution(lines, tasksDefinitions, usersDefinitions, imagesDefinitions):

	for line in lines:
		data = line.split("+")
		executionID = data[0].strip(' \t\n\r')
		taskID = lineData[3].strip(' \t\n\r"')
		userID = lineData[4].strip(' \t\n\r"')
		userAnswer = lineData[9].strip(' \t\n\r"')

		userInfo = usersDefinitions[userID]#Retrieving user data

		if executionID[0].lower() == 'n':#MaxDiff design
			answer = json.loads(userAnswer)
			photo1 = answer['theMost'].strip(' \t\n\r"')
			photo2 = answer['theLess'].strip(' \t\n\r"')

			taskDef = tasksDefinitions[taskID]
			photos = Set( [taskDef['url_c'].strip(' \t\n\r"'), taskDef['url_b'].strip(' \t\n\r"'), taskDef['url_a'].strip(' \t\n\r"'), taskDef['url_d'].strip(' \t\n\r"')] )
			if(photo1 != completeTie ){
				photos.remove(photo1)
				photos.remove(photo2)
			}else{
				photo1 = photos.pop()
				photo2 = photos.pop()
			}
			photo3 = photos.pop()
			photo4 = photos.pop()

			photo1Info = imagesDefinitions["/".join(photo1.split("/")[5:])]			
			photo2Info = imagesDefinitions["/".join(photo2.split("/")[5:])]
			photo3Info = imagesDefinitions["/".join(photo3.split("/")[5:])]
			photo4Info = imagesDefinitions["/".join(photo4.split("/")[5:])]

			#Saving votes from task-run
			if (photo1 != completeTie){
				print(photo1 + "\t" + photo2 + "\t" + "-1" + "\t" + " ".join(userInfo) + "\t" + " ".join(photo1Info) + "\t" + str(photo2Info) + "\t")
				print(photo1 + "\t" + photo3 + "\t" + "-1" + "\t" + " ".join(userInfo) + "\t" + " ".join(photo1Info) + "\t" + " ".join((photo3Info) + "\t")
				print(photo1 + "\t" + photo4 + "\t" + "-1" + "\t" + " ".join(userInfo) + "\t" + " ".join(photo1Info) + "\t" + " ".join((photo4Info) + "\t")
				print(photo2 + "\t" + photo3 + "\t" + "1" + "\t" + " ".join(userInfo) + "\t" + " ".join(photo2Info) + "\t" + " ".join(photo3Info) + "\t")
				print(photo2 + "\t" + photo4 + "\t" + "1" + "\t" + " ".join(userInfo) + "\t" + " ".join(photo2Info) + "\t" + " ".join(photo4Info) + "\t")
				print(photo3 + "\t" + photo4 + "\t" + "1" + "\t" + " ".join(userInfo) + "\t" + " ".join(photo3Info) + "\t" + " ".join(photo4Info) + "\t")
			}else{
				print(photo1 + "\t" + photo2 + "\t" + "0" + "\t" + " ".join(userInfo) + "\t" + " ".join(photo1Info) + "\t" + " ".join(photo2Info) + "\t")
				print(photo1 + "\t" + photo3 + "\t" + "0" + "\t" + " ".join(userInfo) + "\t" + " ".join(photo1Info) + "\t" + " ".join(photo3Info) + "\t")
				print(photo1 + "\t" + photo4 + "\t" + "0" + "\t" + " ".join(userInfo) + "\t" + " ".join(photo1Info) + "\t" + " ".join(photo4Info) + "\t")
				print(photo2 + "\t" + photo3 + "\t" + "0" + "\t" + " ".join(userInfo) + "\t" + " ".join(photo2Info) + "\t" + " ".join(photo3Info) + "\t")
				print(photo2 + "\t" + photo4 + "\t" + "0" + "\t" + " ".join(userInfo) + "\t" + " ".join(photo2Info) + "\t" + " ".join(photo4Info) + "\t")
				print(photo3 + "\t" + photo4 + "\t" + "0" + "\t" + " ".join(userInfo) + "\t" + " ".join(photo3Info) + "\t" + " ".join(photo4Info) + "\t")
			}
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
				print(photo1 + "\t" + photo2 + "\t" + "-1" + "\t" + " ".join(userInfo) + "\t" + " ".join(photo1Info) + "\t" + " ".join(photo2Info) + "\t")
			else if answer.lower() == right:
				print(photo1 + "\t" + photo2 + "\t" + "1" + "\t" + " ".join(userInfo) + "\t" + " ".join(photo1Info) + "\t" + " ".join(photo2Info) + "\t")
			else:
				print(photo1 + "\t" + photo2 + "\t" + "0" + "\t" + " ".join(userInfo) + "\t" + " ".join(photo1Info) + "\t" + " ".join(photo2Info) + "\t")

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
	
		#18+Masculino+Baixa (at\u00e9 R$ 1.449,99)+Gradua\u00e7\u00e3o+Campina Grande - Para\u00edba, Brasil+18+Solteiro+
		#20+M+baixa+ensino medio+Campina Grande - PB, Brasil++solteiro+[u'cen', u'lib', u'cat']
		if len(userInfoData) == 0:
			usersDef[userID] = ['', '', '', '', '', '', '', '[]']
		else:
			userInfo = userInfoData.split("+")

			income = ""
			if userInfo[2] == possibleIncomesOld[0] or userInfo[2] == possibleIncomesNew[0]:
				income = "baixa"
			else if userInfo[2] == possibleIncomesOld[1] or userInfo[2] == possibleIncomesNew[1]:
				income = "media baixa"
			else if userInfo[2] == possibleIncomesOld[2] or userInfo[2] == possibleIncomesNew[2]:
				income = "media"
			else if userInfo[2] == possibleIncomesOld[3] or userInfo[2] == possibleIncomesNew[3]:
				income = "media alta"
			else if userInfo[2] == possibleIncomesOld[4] or userInfo[2] == possibleIncomesNew[4]:
				income = "alta"

			educ = ""
			if userInfo[3].lower() == 'e':
				educ = "ensino medio"
			else if userInfo[3].lower() == 'g':
				educ = "graduacao"
			else if userInfo[3].lower() == 'm':
				educ = "mestrado"
			else if userInfo[3].lower() == 'd':
				educ = "doutorado"

			#age, gender, income, education, city, marital status
			usersDef[userID] = [userInfo[0], userInfo[1][0].lower(), income, educ, userInfo[4].lower(), userInfo[6].lower()]
	return usersDef


def readImagesDefinitions(lines):
	#TODO! image_url,  street_wid, mov_cars, park_cars, mov_ciclyst, landscape, build_ident, trees, build_height, diff_build, people, graffiti, bairro)
	imagesDef = {}
	for line in lines:
		data = line.split(" ")
		imagesDef[data[0]] = [data[1:]]

	return imagesDef


if __name__ == "__main__":
	if len(sys.argv) < 4:
		print "Uso: <arquivo com execuções das tarefas> <arquivo com definicoes de tarefas> <arquivo com dados dos usuarios> <arquivos com dados das imagens>"
		sys.exit(1)

	tasksDef = readTasksDefinitions(open(sys.argv[2], 'r').readlines())
	usersDef = readUsersDefinitions(open(sys.argv[3], 'r').readlines())
	imagesDef = readImagesDefinitions(open(sys.argv[4], 'r').readlines())

	tasksExecution = readTasksExecution(open(sys.argv[1], 'r').readlines(), tasksDef, usersDef, imagesDef)
