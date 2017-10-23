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
user_city = {}
user_time = {}
user_rel = {}
user_neig = {}
empty = 0

#possible questions
#possibleQuestions = ["agrad%C3%A1vel?", "seguro?"]
possibleQuestions = ["agradavel?", "seguro?"]

photosAnsweredPerQuestion = {possibleQuestions[0]:{}, possibleQuestions[1]:{}}

#Tasks definition
tasks_id_definition = {}

def plotAge():
	pp = PdfPages('age.pdf')

	#Age levels
	lev0 = 0
	lev1 = 0
	lev2 = 0
	lev3 = 0
	lev4 = 0
	lev5 = 0
	lev6 = 0

	for age in user_age.keys():	
		if eval(age) != None and len(age) > 0:
			intAge = int(age)

			if intAge < 18:
				lev0 += 1 * user_age[age]
			elif intAge >= 18 and intAge <= 24:
				lev1 += 1 * user_age[age]
			elif intAge >= 25 and intAge <= 34:
				lev2 += 1 * user_age[age]
			elif intAge >= 35 and intAge <= 44:		
				lev3 += 1 * user_age[age]
			elif intAge >= 45 and intAge <= 54:		
				lev4 += 1 * user_age[age]
			elif intAge >= 55 and intAge <= 64:		
				lev5 += 1 * user_age[age]
		#else:
		#	lev6 += 1
	labels = '18l', '18a24', '25a34', '35a44', '45a54', '55a64'
	sizes = [lev0, lev1, lev2, lev3, lev4, lev5] 		

	colors = ['yellowgreen', 'green', 'gold', 'lightskyblue', 'blue', 'lightcoral', 'red']
	plt.figure()
	plt.clf()
	plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True)
	plt.axis('equal')
	pp.savefig()
	pp.close()

def plotSex():
	#Sex levels
	pp = PdfPages('sex.pdf')
	labels = []
	sizes = []
	for sex in user_sex.keys():
		if sex != None and len(sex) > 0:
			labels.append(sex)
			sizes.append(user_sex[sex])
	colors = ['lightcoral', 'lightskyblue']
	plt.figure()
	plt.clf()
	plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True)
	plt.axis('equal')
	pp.savefig()
	pp.close()

def plotClass():
	#Class levels
	pp = PdfPages('class.pdf')
	labels = []
	sizes = []
	for clas in user_class.keys():
		if clas != None and len(clas) > 0:
			labels.append(clas)
			sizes.append(user_class[clas])
	colors = ['yellowgreen', 'gold', 'lightskyblue', 'blue', 'lightcoral', 'red']
	plt.figure()
	plt.clf()
	plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True)
	plt.axis('equal')
	pp.savefig()
	pp.close()

def plotEduc():
	#Educational levels
	pp = PdfPages('educ.pdf')
	labels = []
	sizes = []
	for educ in user_educ.keys():
		if educ != None and len(educ) > 0:
			labels.append(educ)
			sizes.append(user_educ[educ])
	colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
	plt.figure()
	plt.clf()
	plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True)
	plt.axis('equal')
	pp.savefig()
	pp.close()

def plotCity():
#City levels
	pp = PdfPages('city.pdf')
	labels = []
	sizes = []
	campinaCounting = 0
	joaoPessoaCounting = 0
	for city in user_city.keys():
		if city != None and len(city) > 0:
			if 'campina' in city.lower():
				campinaCounting += user_city[city]
			elif 'pessoa' in city.lower():
				joaoPessoaCounting += user_city[city]
			else:
				labels.append(city[0:5])
				sizes.append(user_city[city])
	labels.append("Campina Grande")
	labels.append("Joao Pessoa")
	sizes.append(campinaCounting)
	sizes.append(joaoPessoaCounting)
	colors = ['yellowgreen', 'green', 'gold', 'lightskyblue', 'blue', 'lightcoral', 'red', 'black']
	#plt.figure()
	#plt.clf()
	#plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True)
	#plt.axis('equal')
	#pp.savefig()
	#pp.close()

def plotTime():
	#Time levels
	pp = PdfPages('time.pdf')
	lev1 = 0
	lev2 = 0
	lev3 = 0
	lev4 = 0
	lev5 = 0
	lev6 = 0
	for time in user_time.keys():
		if time != None and len(time) > 0:
			intTime = int(time)
			if intTime < 10:
				lev1 += 1 * user_time[time]
			elif intTime >=10 and intTime < 20:
				lev2 += 1 * user_time[time]
			elif intTime >= 20 and intTime < 30:		
				lev3 += 1 * user_time[time]
			elif intTime >=30 and intTime < 40:		
				lev4 += 1 * user_time[time]
			elif intTime >=40 and intTime < 50:		
				lev5 += 1 * user_time[time]
			else:
				lev6 += 1 * user_time[time]
	labels = '10-', '10-20', '20-30', '30-40', '40-50', '50+'
	sizes = [lev1, lev2, lev3, lev4, lev5, lev6] 		
	colors = ['yellowgreen', 'gold', 'lightskyblue', 'blue', 'lightcoral', 'red']
	plt.figure()
	plt.clf()
	plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True)
	plt.axis('equal')
	pp.savefig()
	pp.close()

def plotRel():
	#Relationship levels
	pp = PdfPages('rel.pdf')
	labels = []
	sizes = []
	for rel in user_rel.keys():
		if rel != None and len(rel) > 0:
			labels.append(rel)
			sizes.append(user_rel[rel])
	colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
	plt.figure()
	plt.clf()
	plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True)
	plt.axis('equal')
	pp.savefig()
	pp.close()

def plotNeig():
	#Neighborhood levels
	pp = PdfPages('neig.pdf')
	cen = user_neig['cen']
	lib = user_neig['lib']
	catol = user_neig['cat'] 

	labels = 'Centro', 'Liberdade', 'Catole', 'Nao responderam ou Nao conhecem'
	sizes = [cen, lib, catol, empty]
	colors = ['yellowgreen', 'green', 'lightskyblue', 'lightcoral']
	plt.figure()
	plt.clf()
	plt.pie(sizes, labels=labels, colors=colors,
		autopct='%1.1f%%', shadow=True)
	plt.axis('equal')
	pp.savefig()
	pp.close()



def plotSummary():
	plotAge()
	plotSex()
	plotEduc()
	plotClass()
	plotCity()
	plotTime()
	plotRel()
	plotNeig()

	#plt.pie(sizes, explode=explode, labels=labels, colors=colors,
	#	autopct='%1.1f%%', shadow=True)
	# Set aspect ratio to be equal so that pie is drawn as a circle.
	#plt.axis('equal')

	#plt.show()
	#plt.savefig(pp, format='pdf')

def countSummary(profileInfo):
	global empty

	if len(profileInfo) > 0:
		#Extracting profile
		userProfileData = profileInfo.split("+")
		age = userProfileData[0].strip(' \t\n\r"')
		sex = userProfileData[1].strip(' \t\n\r"')
		currentClass = userProfileData[2].strip(' \t\n\r"')
		educ =  userProfileData[3].strip(' \t\n\r"')
		city = userProfileData[4].strip(' \t\n\r"')
		time = userProfileData[5].strip(' \t\n\r"')
		rel = userProfileData[6].strip(' \t\n\r"')
		neig = userProfileData[7].strip(' \t\n\r"')
		neig = neig[0:len(neig)].strip(' \t\n\r"')

		#Saving occurrences of profiles
		if len(age) > 0:
			if age in user_age.keys():
				user_age[age] = user_age[age] + 1
			else:
				user_age[age] = 1
		if len(sex) > 0:
			if sex in user_sex.keys():
				user_sex[sex] = user_sex[sex] + 1
			else:
				user_sex[sex] = 1
		if len(currentClass) > 0:
			if currentClass in user_class.keys():
				user_class[currentClass] = user_class[currentClass] + 1
			else:
				user_class[currentClass] = 1
		if len(educ) > 0:
			if educ in user_educ.keys():
				user_educ[educ] = user_educ[educ] + 1
			else:
				user_educ[educ] = 1
		if len(city) > 0:
			if city in user_city.keys():
				user_city[city] = user_city[city] + 1
			else:
				user_city[city] = 1
		if len(time) > 0:
			if time in user_time.keys():
				user_time[time] = user_time[time] + 1
			else:
				user_time[time] = 1
		if len(rel) > 0:
			if rel in user_rel.keys():
				user_rel[rel] = user_rel[rel] + 1
			else:
				user_rel[rel] = 1
		if len(neig) > 0:
			if neig in user_neig.keys():
				user_neig[neig] = user_neig[neig] + 1
			else:
				user_neig[neig] = 1
			if 'cen' in neig.lower():
				if 'cen' in user_neig.keys():
					user_neig['cen'] = user_neig['cen'] + 1
				else:
					user_neig['cen'] = 1
			if 'lib' in neig.lower():
				if 'lib' in user_neig.keys():
					user_neig['lib'] = user_neig['lib'] + 1
				else:
					user_neig['lib'] = 1
			if 'cat' in neig.lower():
				if 'cat' in user_neig.keys():
					user_neig['cat'] = user_neig['cat'] + 1
				else:
					user_neig['cat'] = 1
		if len(neig) == 0:
			empty += 1


def writeOutput(users_tasks):
	output_file = open("usersInfo.dat", "w")
	answered_profile = 0
	nanswered_profile = 0
	users_id_nanswered_profile = []
	finish_time_nanswered = []

	#Writing users profile and tasks executed
	for user_id in users_tasks.keys():
		user_data = users_tasks[user_id]
		user_profile = str(user_data[0]['age']) + "+" + str(user_data[0]['sex']) + "+" + str(user_data[0]['clas']) + "+" + str(user_data[0]['edu']) + "+" + str(user_data[0]['cit']) + "+" + str(user_data[0]['time']) + "+" + str(user_data[0]['rel']) + "+" + str(user_data[0]['nei'])
		
		output_file.write(user_id+"|" + user_profile + "|" + str(user_data[1]) + "|" + str(user_data[2]) + "|" + str(user_data[3]) + "|" + str(user_data[4]) + "\n")
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
	output_file.write(str(user_age)+"\n")
	output_file.write(">> TOTAL RESPOSTAS " + str(np.sum(user_age.values()))+"\n")
	output_file.write(str(user_sex)+"\n")
	output_file.write(">> TOTAL RESPOSTAS " + str(np.sum(user_sex.values()))+"\n")
	output_file.write(str(user_class)+"\n")		
	output_file.write(">> TOTAL RESPOSTAS " + str(np.sum(user_class.values()))+"\n")
	output_file.write(str(user_educ)+"\n")
	output_file.write(">> TOTAL RESPOSTAS " + str(np.sum(user_educ.values()))+"\n")
	output_file.write(str(user_city)+"\n")
	output_file.write(">> TOTAL RESPOSTAS " + str(np.sum(user_city.values()))+"\n")
	output_file.write(str(user_time)+"\n")
	output_file.write(">> TOTAL RESPOSTAS " + str(np.sum(user_time.values()))+"\n")
	output_file.write(str(user_rel)+"\n")
	output_file.write(">> TOTAL RESPOSTAS " + str(np.sum(user_rel.values()))+"\n")
	output_file.write(str(user_neig)+"\n")
	output_file.write(">> TOTAL RESPOSTAS " + str(np.sum(user_neig.values()))+"\n")
	output_file.close()
	plotSummary()

	#Writing tasks definition
	output_file = open("tasksDefinition.dat", "w")
	for task_id in tasks_id_definition.keys():
		output_file.write(task_id+"\t"+tasks_id_definition[task_id].encode('utf-8')+"\n")
	output_file.close()

	#Writing photos evaluated by user
	output_file = open("usersPhotosAgrad.dat", "w")
	for user_id in photosAnsweredPerQuestion[possibleQuestions[0]].keys():
		for photo in photosAnsweredPerQuestion[possibleQuestions[0]][user_id]:
			output_file.write(user_id+"\t"+photo.encode('utf-8')+"\n")
	output_file.close()

	#Writing photos evaluated by user
	output_file = open("usersPhotosSeg.dat", "w")
	for user_id in photosAnsweredPerQuestion[possibleQuestions[1]].keys():
		for photo in photosAnsweredPerQuestion[possibleQuestions[1]][user_id]:
			output_file.write(user_id+"\t"+photo.encode('utf-8')+"\n")
	output_file.close()

	#Writing users that did not answered profile
	output_file = open("usersNAnswered.dat", "w")
	users_profile_file = open("users.csv", "r")
	users_profile = users_profile_file.readlines()

	for index in range(0, len(users_id_nanswered_profile)):
		user_id = users_id_nanswered_profile[index]
		for profile in users_profile:
			data = profile.split(",")
			if data[0].strip() == user_id:
				output_file.write(user_id+"\t"+data[2]+"\t"+str(finish_time_nanswered[index])+"\n")
	output_file.close()
	users_profile_file.close()


def readUserData(lines1, lines2, outputFileName):
	""" Reading user profile """
	
	users_tasks = {}
	firstDate = datetime.date(1970, 6, 24)
	agrad_dic = {"agradavel?" : "agrad%C3%A1vel?", "agrad%C3%A1vel?" : "agradavel?"}

	#Reading from pybossa task-run CSV - V1
	for line in lines1:
		print ">>>> Deprecated"

	index = 0
	#Reading from pybossa task-run CSV - V2
	for line in lines2:
		print ">>> Mais uma linha " + str(index)
		index = index + 1

		data = line.split("+")

		task_id = data[3]
		user_id = data[4]
		user_ip = data[5]
		timeInfo = data[6].split("T")[0].split("-")#2015-02-17T18:19:52.589591
		finish_time = datetime.date(int(timeInfo[0]), int(timeInfo[1]), int(timeInfo[2]))
		
		user_answer = data[9].strip(' \t\n\r"')
		
		if user_id in users_tasks.keys():
			user_executions = users_tasks[user_id]
		else:
			user_executions = [{'age': -1, 'sex': "", 'clas': "", 'edu': "", 'cit': "", "time": "", 'rel': "", 'nei': ""}, [], [], [], [], firstDate]#Tasks for Agradavel e Seguro and their respective answers

		#In user answers that contain profile information extract profile: {"userProfile": {"city": "Campina Grande - State of Para\u00edba, Brazil", "age": 33, "sex": "M", "rel": "casado", "educ": "doutorado", "neig": ["cen"], "clas": "media alta"}, "question": "agradavel", "theLess": "https://contribua.org/bairros/oeste/liberdade/Rua_Edesio_Silva__602__180.jpg", "theMost": "https://contribua.org/bairros/norte/centro/Avenida_Presidente_Getulio_Vargas__395__270.jpg"}
		user_answer_data = json.loads(user_answer)

		if user_answer_data.has_key('userProfile'):
			#Extracting profile
			user_profile_data = user_answer_data['userProfile']

			age = user_profile_data['age']
			sex = user_profile_data['sex'].encode('utf-8').strip(' \t\n\r"')
			currentClass = user_profile_data['clas'].encode('utf-8').strip(' \t\n\r"')
			educ =  user_profile_data['educ'].encode('utf-8').strip(' \t\n\r"')
			city = user_profile_data['city'].encode('utf-8').strip(' \t\n\r"')
			#time = userProfileData['time'].strip(' \t\n\r"')
			rel = user_profile_data['rel'].encode('utf-8').strip(' \t\n\r"')
			neig = user_profile_data['neig'] 

			if len(city) == 0:
				if len(user_ip) > 0:
					response = urllib.urlopen("http://ip-api.com/json/"+user_ip)
					ip_data = json.loads(response.read())
					city =  ip_data['city'].encode('utf-8') + "," + ip_data['country'].encode('utf-8')

			if user_executions[0]['age'] == -1:
				user_executions[0]['age'] = age
			if len(user_executions[0]['sex'].strip(' \t\n\r"')) == 0:
				user_executions[0]['sex'] = sex
			if len(user_executions[0]['clas'].strip(' \t\n\r"')) == 0:
				user_executions[0]['clas'] = currentClass
			if len(user_executions[0]['edu'].strip(' \t\n\r"')) == 0:
				user_executions[0]['edu'] = educ
			if len(user_executions[0]['cit'].strip(' \t\n\r"')) == 0:
				user_executions[0]['cit'] = city
			if len(user_executions[0]['rel'].strip(' \t\n\r"')) == 0:
				user_executions[0]['rel'] = rel
			if len(user_executions[0]['nei'].strip(' \t\n\r"')) == 0:
				user_executions[0]['nei'] = str(neig)
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

	return users_tasks

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print "Uso: <arquivo com execucoes das tarefas e perfis dos usuarios - V1> <arquivo com execucoes das tarefas e perfis dos usuarios - V2>"
		sys.exit(1)

	dataFile1 = ""#open(sys.argv[1], 'r')
	dataFile2 = open(sys.argv[2], 'r')
	
	lines1 = []#dataFile1.readlines() - This file does not exist for this version of app!
	lines2 = dataFile2.readlines()

	users_tasks = readUserData(lines1, lines2, "users.dat")
	writeOutput(users_tasks)	
	#dataFile1.close()
	dataFile2.close()

