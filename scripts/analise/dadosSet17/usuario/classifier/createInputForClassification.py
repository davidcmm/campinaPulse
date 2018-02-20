# coding=utf-8
# Prepares tasks and users data for classification

import sys
from sets import Set
import random
import numpy
import json
import csv
import pandas as pd
import urllib, cStringIO

completeTie = 'equal'
left = 'left'
right = 'right'
notKnown = 'notknown'

def readTasksExecution(lines, tasksDefinitions, usersDefinitions, imagesDefinitions, output_file):

	#Header
	output_file.write("question\tphoto1\tphoto2\tchoice\tuserID\tage\tgender\tincome\teducation\tcity\tmarital\tstreet_wid1\tsidewalk_wid1\tlandscape1\tbuild_ident1\ttrees1\tstreet_wid2\tsidewalk_wid2\tlandscape2\tbuild_ident2\ttrees2\n")

	for line in lines:
		data = line.split("+")
		executionID = data[0].strip(' \t\n\r')
		taskID = data[3].strip(' \t\n\r"')
		userID = data[4].strip(' \t\n\r"')
		userAnswer = data[9].strip(' \t\n\r"')

		#print imagesDefinitions.keys()

		if usersDefinitions.has_key(userID):
			userInfo = usersDefinitions[userID]#Retrieving user data

			if executionID[0].lower() == 'n':#MaxDiff design
				answer = json.loads(userAnswer)
				question = answer['question'].strip(' \t\n\r"')
				photo1 = answer['theMost'].strip(' \t\n\r"')
				photo2 = answer['theLess'].strip(' \t\n\r"')

				taskDef = tasksDefinitions[taskID]
				photos = Set( [taskDef['url_c'].strip(' \t\n\r"'), taskDef['url_b'].strip(' \t\n\r"'), taskDef['url_a'].strip(' \t\n\r"'), taskDef['url_d'].strip(' \t\n\r"')] )

				if len(photo1) == 0 or len(photo2) == 0:#Error in persisting photos!
					print "Foto zerada! " + line
					continue

				if photo1 != completeTie:
					photos.remove(photo1)
					photos.remove(photo2)
				else:
					photo1 = photos.pop()
					photo2 = photos.pop()
			
				photo3 = photos.pop()
				photo4 = photos.pop()

				photo1Info = imagesDefinitions[photo1]			
				photo2Info = imagesDefinitions[photo2]
				photo3Info = imagesDefinitions[photo3]
				photo4Info = imagesDefinitions[photo4]

				#Saving votes from task-run
				if photo1 != completeTie:
					output_file.write(question + "\t" + urllib.quote(photo1.encode('utf8'), ':/') + "\t" + urllib.quote(photo2.encode('utf8'), ':/') + "\t" + "-1" + "\t" + userID + "\t" + "\t".join(userInfo) + "\t" + "\t".join(photo1Info).strip(' \t\n\r') + "\t" + "\t".join(photo2Info).strip(' \t\n\r') + "\n")
					output_file.write(question + "\t" + urllib.quote(photo1.encode('utf8'), ':/') + "\t" + urllib.quote(photo3.encode('utf8'), ':/') + "\t" + "-1" + "\t" + userID + "\t" + "\t".join(userInfo) + "\t" + "\t".join(photo1Info).strip(' \t\n\r') + "\t" + "\t".join(photo3Info).strip(' \t\n\r') + "\n")
					output_file.write(question + "\t" + urllib.quote(photo1.encode('utf8'), ':/') + "\t" + urllib.quote(photo4.encode('utf8'), ':/') + "\t" + "-1" + "\t" + userID + "\t" + "\t".join(userInfo) + "\t" + "\t".join(photo1Info).strip(' \t\n\r') + "\t" + "\t".join(photo4Info).strip(' \t\n\r') + "\n")
					output_file.write(question + "\t" + urllib.quote(photo2.encode('utf8'), ':/') + "\t" + urllib.quote(photo3.encode('utf8'), ':/') + "\t" + "1" + "\t" + userID + "\t" + "\t".join(userInfo) + "\t" + "\t".join(photo2Info).strip(' \t\n\r') + "\t" + "\t".join(photo3Info).strip(' \t\n\r') + "\n")
					output_file.write(question + "\t" + urllib.quote(photo2.encode('utf8'), ':/') + "\t" + urllib.quote(photo4.encode('utf8'), ':/') + "\t" + "1" + "\t" + userID + "\t" + "\t".join(userInfo) + "\t" + "\t".join(photo2Info).strip(' \t\n\r') + "\t" + "\t".join(photo4Info).strip(' \t\n\r') + "\n")
					output_file.write(question + "\t" + urllib.quote(photo3.encode('utf8'), ':/') + "\t" + urllib.quote(photo4.encode('utf8'), ':/') + "\t" + "1" + "\t" + userID + "\t" + "\t".join(userInfo) + "\t" + "\t".join(photo3Info).strip(' \t\n\r') + "\t" + "\t".join(photo4Info).strip(' \t\n\r') + "\n")
				else:
					output_file.write(question + "\t" + urllib.quote(photo1.encode('utf8'), ':/') + "\t" + urllib.quote(photo2.encode('utf8'), ':/') + "\t" + "0" + "\t" + userID + "\t" + "\t".join(userInfo) + "\t" + "\t".join(photo1Info).strip(' \t\n\r') + "\t" + "\t".join(photo2Info).strip(' \t\n\r') + "\n")
					output_file.write(question + "\t" + urllib.quote(photo1.encode('utf8'), ':/') + "\t" + urllib.quote(photo3.encode('utf8'), ':/') + "\t" + "0" + "\t" + userID + "\t" + "\t".join(userInfo) + "\t" + "\t".join(photo1Info).strip(' \t\n\r') + "\t" + "\t".join(photo3Info).strip(' \t\n\r') + "\n")
					output_file.write(question + "\t" + urllib.quote(photo1.encode('utf8'), ':/') + "\t" + urllib.quote(photo4.encode('utf8'), ':/') + "\t" + "0" + "\t" + userID + "\t" + "\t".join(userInfo) + "\t" + "\t".join(photo1Info).strip(' \t\n\r') + "\t" + "\t".join(photo4Info).strip(' \t\n\r') + "\n")
					output_file.write(question + "\t" + urllib.quote(photo2.encode('utf8'), ':/') + "\t" + urllib.quote(photo3.encode('utf8'), ':/') + "\t" + "0" + "\t" + userID + "\t" + "\t".join(userInfo) + "\t" + "\t".join(photo2Info).strip(' \t\n\r') + "\t" + "\t".join(photo3Info).strip(' \t\n\r') + "\n")
					output_file.write(question + "\t" + urllib.quote(photo2.encode('utf8'), ':/') + "\t" + urllib.quote(photo4.encode('utf8'), ':/') + "\t" + "0" + "\t" + userID + "\t" + "\t".join(userInfo) + "\t" + "\t".join(photo2Info).strip(' \t\n\r') + "\t" + "\t".join(photo4Info).strip(' \t\n\r') + "\n")
					output_file.write(question + "\t" + urllib.quote(photo3.encode('utf8'), ':/') + "\t" + urllib.quote(photo4.encode('utf8'), ':/') + "\t" + "0" + "\t" + userID + "\t" + "\t".join(userInfo) + "\t" + "\t".join(photo3Info).strip(' \t\n\r') + "\t" + "\t".join(photo4Info).strip(' \t\n\r') + "\n")
			
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

				photo1Info = imagesDefinitions[photo1]			
				photo2Info = imagesDefinitions[photo2]
		
				if answer.lower() == left:
					output_file.write(question + "\t" + urllib.quote(photo1.encode('utf8'), ':/') + "\t" + urllib.quote(photo2.encode('utf8'), ':/') + "\t" + "-1" + "\t" + userID + "\t" + "\t".join(userInfo) + "\t" + "\t".join(photo1Info).strip(' \t\n\r') + "\t" + "\t".join(photo2Info).strip(' \t\n\r') + "\n")
				elif answer.lower() == right:
					output_file.write(question + "\t" + urllib.quote(photo1.encode('utf8'), ':/') + "\t" + urllib.quote(photo2.encode('utf8'), ':/') + "\t" + "1" + "\t" + userID + "\t" + "\t".join(userInfo) + "\t" + "\t".join(photo1Info).strip(' \t\n\r') + "\t" + "\t".join(photo2Info).strip(' \t\n\r') + "\n")
				else:
					#print(photo1)
					#print(photo2)
					#print(" ".join(userInfo))
					#print(photo1Info)
					#print(" ".join(photo2Info))
					output_file.write(question + "\t" + photo1 + "\t" + photo2 + "\t" + "0" + "\t" + userID + "\t" + "\t".join(userInfo) + "\t" + "\t".join(photo1Info).strip(' \t\n\r') + "\t" + "\t".join(photo2Info).strip(' \t\n\r'))

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

def readUsersDefinitions(linesUsers, not_local_ids):
	usersDef = {}

	for line in linesUsers:
		data = line.split("|")
		#print data
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
				#print userInfo
				gender = ""
				if len(userInfo[1]) > 0:
					if userInfo[1][0].lower() == 'm':
						gender = "masculino"
					else:
						gender = "feminino"

				income = ""
				if len(userInfo[2]) > 0:
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
				if len(userInfo[3]) > 0:
					if userInfo[3][0].lower() == 'e':
						educ = "ensino medio"
					elif userInfo[3][0].lower() == 'g':
						educ = "graduacao"
					elif userInfo[3][0].lower() == 'm':
						educ = "mestrado"
					elif userInfo[3][0].lower() == 'd':
						educ = "doutorado"

				city = ""
				if len(userInfo[4]) > 0:
					city = userInfo[4]
					know_campina = userInfo[8]
					how_know_campina = userInfo[9].lower()

					if (city.lower().find("campina grande") > -1 and city.lower().find("sul") == -1) or (str(userID) in not_local_ids):
						city = "campina"
					elif len(know_campina) > 0 and len(how_know_campina) > 0 and "yes" in know_campina and ("live" in how_know_campina or "study" in how_know_campina or "work" in how_know_campina):
						city = "campina"
					else:
						city = "notcampina"					

				#User profile: age, gender, income, education, city, marital status
				usersDef[userID] = [userInfo[0].strip(' \t\n\r'), gender, income, educ, city, userInfo[6].lower()]
	
	return usersDef


def readImagesDefinitions(lines):
	imagesDef = {}
	for line in lines:
		data = line.split(" ")
		imagesDef[urllib.unquote(data[0]).decode('utf8')] = data[1:]

	return imagesDef


def convertTo2Classes(input_3cl_file):
	input_3cl = pd.read_table(input_3cl_file, sep='\t', encoding='utf8', header=0)

	#Remove draws
	wodraw_input = input_3cl[(input_3cl.choice != 0)]
	wodraw_input.to_csv("classifier_input_wodraw.dat", sep = "\t", index = False)

	#Convert to left; not-left
	#left_input = input_3cl.copy()
	#new_data = left_input.choice.replace(0, 1)
	#left_input['choice'] = new_data
	#left_input.to_csv("classifier_input_lnl.dat", sep = "\t")

	#Convert to right; not-right
	#right_input = input_3cl.copy()
	#new_data = right_input.choice.replace(0, -1)
	#right_input['choice'] = new_data
	#right_input.to_csv("classifier_input_rnr.dat", sep = "\t")

if __name__ == "__main__":
	if len(sys.argv) < 4:
		print "Uso: <action: create or convert> <arquivo com execuções das tarefas> <arquivo com definicoes de tarefas> <arquivo com dados dos usuarios> <lista de usuários marcados como não locais sendo locais> <arquivos com dados das imagens>"
		sys.exit(1)

	output_file = open("classifier_input_wodraw.dat", "w")

	if sys.argv[1].lower() == 'create':
		tasksDef = readTasksDefinitions(open(sys.argv[3], 'r').readlines())
		not_local_ids_file = open(sys.argv[5], 'r')
		not_local_ids = []
		for id in not_local_ids_file.readlines():
			not_local_ids.append(id.strip(" \n"))
		not_local_ids_file.close()
		usersDef = readUsersDefinitions(open(sys.argv[4], 'r').readlines(), not_local_ids)
		imagesDef = readImagesDefinitions(open(sys.argv[6], 'r').readlines())

		tasksExecution = readTasksExecution(open(sys.argv[2], 'r').readlines(), tasksDef, usersDef, imagesDef, output_file)
	elif sys.argv[1].lower() == 'convert':
		convertTo2Classes("classifier_input_3classes.dat")

	output_file.close()
