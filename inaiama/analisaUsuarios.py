# -*- coding: utf-8 -*-

import sys
import matplotlib.pyplot as plt
import time as tm
import datetime
from matplotlib.backends.backend_pdf import PdfPages
from sets import Set
import json, urllib
import numpy as np

#User profiles summary dictionaries
user_age = {}
user_sex = {}
user_class = {}
user_educ = {}
user_live = {}
user_city = {}
user_time = {}
user_rel = {}
user_neig = {'cen' : 0, 'cat' : 0, 'lib' : 0}
empty = 0

#possible questions
#possibleQuestions = ["agrad%C3%A1vel?", "seguro?"]
possibleQuestions = ["agradavel?", "seguro"]

photosAnsweredPerQuestion = {possibleQuestions[0]:{}, possibleQuestions[1]:{}}

#Tasks definition
tasks_id_definition = {}

def countSummary(profileInfo):
	global empty

	if len(profileInfo) > 0:
		#Extracting profile
		userProfileData = profileInfo.split("+")
		#age = userProfileData[0].strip(' \t\n\r"')
		sex = userProfileData[0].strip(' \t\n\r"')
		#currentClass = userProfileData[2].strip(' \t\n\r"')
		educ =  userProfileData[1].strip(' \t\n\r"')
		live =  userProfileData[2].strip(' \t\n\r"')
		#city = userProfileData[4].strip(' \t\n\r"')
		#time = userProfileData[5].strip(' \t\n\r"')
		#rel = userProfileData[6].strip(' \t\n\r"')
		#neig = userProfileData[7].strip(' \t\n\r"')
		#neig = neig[0:len(neig)].strip(' \t\n\r"')

		#Saving occurrences of profiles
		#if len(age) > 0 and eval(age) != None:
		#	if int(age) > 0:
		#		if age in user_age.keys():
		#			user_age[age] = user_age[age] + 1
		#		else:
		#			user_age[age] = 1
		if len(sex) > 0:
			if sex in user_sex.keys():
				user_sex[sex] = user_sex[sex] + 1
			else:
				user_sex[sex] = 1
		if len(live) > 0:
			if live in user_live.keys():
				user_live[live] = user_live[live] + 1
			else:
				user_live[live] = 1	
	#	if len(currentClass) > 0:
	#		if currentClass in user_class.keys():
	#			user_class[currentClass] = user_class[currentClass] + 1
	#		else:
	#			user_class[currentClass] = 1
		if len(educ) > 0:
			if educ in user_educ.keys():
				user_educ[educ] = user_educ[educ] + 1
			else:
				user_educ[educ] = 1
	#	if len(city) > 0:
	#		if city in user_city.keys():
	#			user_city[city] = user_city[city] + 1
	#		else:
	#			user_city[city] = 1
	#	if len(time) > 0:
	#		if time in user_time.keys():
	#			user_time[time] = user_time[time] + 1
	#		else:
	#			user_time[time] = 1
	#	if len(rel) > 0:
	#		if rel in user_rel.keys():
	#			user_rel[rel] = user_rel[rel] + 1
	#		else:
	#			user_rel[rel] = 1

def writeOutput(users_tasks):
	output_file = open("usersInfo.dat", "w")
	answered_profile = 0
	nanswered_profile = 0
	users_id_nanswered_profile = []
	finish_time_nanswered = []

	#Writing users profile and tasks executed
	for user_id in users_tasks.keys():
		user_data = users_tasks[user_id]
		#user_profile = str(user_data[0]['age']) + "+" + str(user_data[0]['sex']) + "+" + str(user_data[0]['clas']) + "+" + str(user_data[0]['edu']) + "+" + str(user_data[0]['cit']) + "+" + str(user_data[0]['time']) + "+" + str(user_data[0]['rel']) + "+" + str(user_data[0]['nei']) + "+" + str(user_data[0]['knowcampina']) + "+" + str(user_data[0]['howknowcampina'])
		user_profile = str(user_data[0]['sex']) + "+" + str(user_data[0]['educ']) + "+" + str(user_data[0]['live'])
		
		output_file.write(str(user_id)+"|" + user_profile + "|" + str(user_data[1]) + "|" + str(user_data[2]) + "|" + str(user_data[3]) + "|" + str(user_data[4]) + "\n")
		countSummary(user_profile)
		
		if user_data[0]['age'] != -1 and len(user_data[0]['sex']) > 0 and len(user_data[0]['clas']) > 0 and len(user_data[0]['cit']) > 0:
			answered_profile += 1
		else:
			nanswered_profile += 1
			users_id_nanswered_profile.append(user_id)
			finish_time_nanswered.append(user_data[5])
	output_file.close()
	
	#Writing profile summary
	output_file = open("usersInfoSummary.dat", "w")
	output_file.write("Answered\t" + str(answered_profile) + "\t" + str(nanswered_profile) + "\t" + str(answered_profile*1.0/(answered_profile+nanswered_profile)) + "\t" + str(nanswered_profile*1.0/(answered_profile+nanswered_profile)) + "\n")
	#output_file.write(str(user_age)+"\n")
	#output_file.write(">> TOTAL RESPOSTAS " + str(np.sum(user_age.values()))+"\n")
	output_file.write(str(user_sex)+"\n")
	output_file.write(">> TOTAL RESPOSTAS " + str(np.sum(user_sex.values()))+"\n")
	#output_file.write(str(user_class)+"\n")		
	#output_file.write(">> TOTAL RESPOSTAS " + str(np.sum(user_class.values()))+"\n")
	output_file.write(str(user_educ)+"\n")
	output_file.write(">> TOTAL RESPOSTAS " + str(np.sum(user_educ.values()))+"\n")
	output_file.write(str(user_live)+"\n")
	output_file.write(">> TOTAL RESPOSTAS " + str(np.sum(user_live.values()))+"\n")
	#output_file.write(str(user_city)+"\n")
	#output_file.write(">> TOTAL RESPOSTAS " + str(np.sum(user_city.values()))+"\n")
	#output_file.write(str(user_time)+"\n")
	#output_file.write(">> TOTAL RESPOSTAS " + str(np.sum(user_time.values()))+"\n")
	#output_file.write(str(user_rel)+"\n")
	#output_file.write(">> TOTAL RESPOSTAS " + str(np.sum(user_rel.values()))+"\n")
	#output_file.write(str(user_neig)+"\n")
	#output_file.write(">> TOTAL RESPOSTAS " + str(np.sum(user_neig.values()))+"\n")
	#output_file.close()
	#plotSummary()

	#Writing tasks definition
	output_file = open("tasksDefinition.dat", "w")
	for task_id in tasks_id_definition.keys():
		output_file.write(task_id+"\t"+tasks_id_definition[task_id].encode('utf-8')+"\n")
	output_file.close()

	#Writing photos evaluated by user
	output_file = open("usersPhotosAgrad.dat", "w")
	for user_id in photosAnsweredPerQuestion[possibleQuestions[0]].keys():
		for photo in photosAnsweredPerQuestion[possibleQuestions[0]][user_id]:
			output_file.write(str(user_id)+"\t"+photo.encode('utf-8')+"\n")
	output_file.close()

	#Writing photos evaluated by user
	output_file = open("usersPhotosSeg.dat", "w")
	for user_id in photosAnsweredPerQuestion[possibleQuestions[1]].keys():
		for photo in photosAnsweredPerQuestion[possibleQuestions[1]][user_id]:
			output_file.write(str(user_id)+"\t"+photo.encode('utf-8')+"\n")
	output_file.close()

	#Writing users that did not answered profile
	#output_file = open("usersNAnswered.dat", "w")
	#users_profile_file = open("users.csv", "r")
	#users_profile = users_profile_file.readlines()

	#for index in range(0, len(users_id_nanswered_profile)):
	#	user_id = users_id_nanswered_profile[index]
	#	for profile in users_profile:
	#		data = profile.split(",")
	#		if data[0].strip() == user_id:
	#			output_file.write(user_id+"\t"+data[2]+"\t"+str(finish_time_nanswered[index])+"\n")
	#output_file.close()
	#users_profile_file.close()


def readUserData(lines1, lines2, outputFileName, tasksDef):
	""" Reading user profile """
	
	users_tasks = {}
	firstDate = datetime.date(1970, 6, 24)
	agrad_dic = {"agradavel?" : "agrad%C3%A1vel?", "agrad%C3%A1vel?" : "agradavel?"}

	#Reading from pybossa task-run CSV - V1
	for line in lines1:
		print ">>>> Deprecated"

	index = 0
	vit_A = 0
	vit_B = 0
	user_id = 0
	#Reading from pybossa task-run CSV - V2
	for line in lines2:
		#print ">>> Mais uma linha " + str(index)
		index = index + 1

		data = line.split("+")

		task_id = data[3]
		user_id = user_id + 1#data[4]
		user_ip = data[5]
		timeInfo = data[6].split("T")[0].split("-")#2015-02-17T18:19:52.589591
		finish_time = datetime.date(int(timeInfo[0]), int(timeInfo[1]), int(timeInfo[2]))
		
		user_answer = data[9].strip(' \t\n\r"')
		
		if user_id in users_tasks.keys():
			user_executions = users_tasks[user_id]
		else:
			user_executions = [{'age': -1, 'sex': "", 'clas': "", 'educ': "", 'cit': "", "time": "", 'rel': "", 'nei': "", 'knowcampina': "", 'howknowcampina': "", 'live': "", }, [], [], [], [], firstDate]#Tasks for Agradavel e Seguro and their respective answers

		#In user answers that contain profile information extract profile: {"userProfile": {"city": "Campina Grande - State of Para\u00edba, Brazil", "age": 33, "sex": "M", "rel": "casado", "educ": "doutorado", "neig": ["cen"], "clas": "media alta"}, "question": "agradavel", "theLess": "https://contribua.org/bairros/oeste/liberdade/Rua_Edesio_Silva__602__180.jpg", "theMost": "https://contribua.org/bairros/norte/centro/Avenida_Presidente_Getulio_Vargas__395__270.jpg"}
		user_answer_data = json.loads(user_answer)

		if user_answer_data.has_key('userProfile'):
			#Extracting profile
			user_profile_data = user_answer_data['userProfile']

			if 'age' in user_profile_data:
				age = user_profile_data['age']
			else:
				age = -1
			sex = user_profile_data['sex'].encode('utf-8').strip(' \t\n\r"')
			#currentClass = user_profile_data['clas'].encode('utf-8').strip(' \t\n\r"')
			educ =  user_profile_data['educ'].encode('utf-8').strip(' \t\n\r"')
			live =  user_profile_data['live'].encode('utf-8').strip(' \t\n\r"')
			#city = user_profile_data['city'].encode('utf-8').strip(' \t\n\r"')
			#time = userProfileData['time'].strip(' \t\n\r"')
			#rel = user_profile_data['rel'].encode('utf-8').strip(' \t\n\r"')
			#neig = user_profile_data['neig']
			#know =  user_profile_data['knowcampina'].strip(' \t\n\r"')
			#howknow =  user_profile_data['howknowcampina'].strip(' \t\n\r"')

			if len(city) == 0:
				if len(user_ip) > 0:
					response = urllib.urlopen("http://ip-api.com/json/"+user_ip)
					ip_data = json.loads(response.read())
					city =  ip_data['city'].encode('utf-8') + "," + ip_data['country'].encode('utf-8')

			#if user_executions[0]['age'] == -1:
			#	user_executions[0]['age'] = age
			if len(user_executions[0]['sex'].strip(' \t\n\r"')) == 0:
				user_executions[0]['sex'] = sex
			if len(user_executions[0]['educ'].strip(' \t\n\r"')) == 0:
				user_executions[0]['educ'] = educ
			if len(user_executions[0]['live'].strip(' \t\n\r"')) == 0:
				user_executions[0]['live'] = live

			#if len(user_executions[0]['clas'].strip(' \t\n\r"')) == 0:
			#	user_executions[0]['clas'] = currentClass
			#if len(user_executions[0]['cit'].strip(' \t\n\r"')) == 0:
			#	user_executions[0]['cit'] = city
			#if len(user_executions[0]['rel'].strip(' \t\n\r"')) == 0:
			#	user_executions[0]['rel'] = rel
			#if len(user_executions[0]['nei'].strip(' \t\n\r"')) == 0:
			#	user_executions[0]['nei'] = str(neig)
			#if len(user_executions[0]['knowcampina'].strip(' \t\n\r"')) == 0:
			#	user_executions[0]['knowcampina'] = know
			#if len(user_executions[0]['howknowcampina'].strip(' \t\n\r"')) == 0:
			#	user_executions[0]['howknowcampina'] = howknow
		else:
			if len(user_ip) > 0:
				if len(user_executions[0]['cit'].strip(' \t\n\r"')) == 0:
					response = urllib.urlopen("http://ip-api.com/json/"+user_ip)
					ip_data = json.loads(response.read())
					city =  ip_data['city'].encode('utf-8') + "," + ip_data['country'].encode('utf-8')
					user_executions[0]['cit'] = city
			
		#Saving photos that user evaluated
		question = user_answer_data['question'].strip(' \t\n\r"')
		if 'agrad' in question and question == "agrad%C3%A1vel?":
			question = agrad_dic[question]

		answer = "Left*"
		photo1 = user_answer_data['theMost'].strip(' \t\n\r"')
		photo2 = user_answer_data['theLess'].strip(' \t\n\r"')

		#Counting wins for each side
		if photo1 == "equal":
			task_def = tasksDef[task_id]
			print "eq-"+task_def['url_a']+"\t"+task_def['url_b']
		else:
			if "Centro A" in photo1:
				vit_A = vit_A + 1
			else:
				vit_B = vit_B + 1
			print photo1 + "\t" + photo2

		#print str(photosAnsweredPerQuestion.keys())	
		if user_id in photosAnsweredPerQuestion[question].keys():
			photos = photosAnsweredPerQuestion[question][user_id]
		else:
			photos = Set([])
		photos.add(photo1)
		photos.add(photo2)
		photosAnsweredPerQuestion[question][user_id] = photos

		#Saving user answer near task ID
		if question == possibleQuestions[0]:#Agra
			user_executions[1].append(task_id)
			user_executions[3].append(answer)
		elif question == possibleQuestions[1]:#Seg
			user_executions[2].append(task_id)
			user_executions[4].append(answer)
		else:
			print "Error! " + question

		if finish_time > user_executions[5]:
			user_executions[5] = finish_time

		#Saving task ID definition
		tasks_id_definition[task_id] = photo1+"\t"+photo2

		users_tasks[user_id] = user_executions

	print ">>> Vitórias Lado A " + str(vit_A)
	print ">>> Vitórias Lado B " + str(vit_B)

	return users_tasks

def readTasksDefinitions(linesTasks):
	tasksDef = {}

	for line in linesTasks:
		data = line.split("+")	
		#print data
		taskID = data[0].strip(' \t\n\r')
		currentDef = json.loads(data[7].strip(' \t\n\r\"'))

		tasksDef[taskID] = currentDef
	return tasksDef

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print "Uso: <arquivo com execucoes das tarefas e perfis dos usuarios - V1> <arquivo com execucoes das tarefas e perfis dos usuarios - V2> <arquivo com definicoes de tarefas>"
		sys.exit(1)

	dataFile1 = ""#open(sys.argv[1], 'r')
	dataFile2 = open(sys.argv[2], 'r')
	dataFile3 = open(sys.argv[3], 'r')
	
	lines1 = []#dataFile1.readlines() - This file does not exist for this version of app!
	lines2 = dataFile2.readlines()
	lines3 = dataFile3.readlines()

	users_tasks = readUserData(lines1, lines2, "users.dat", readTasksDefinitions(lines3))
	writeOutput(users_tasks)	
	#dataFile1.close()
	dataFile2.close()

