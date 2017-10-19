# -*- coding: utf-8 -*-

import sys
import matplotlib.pyplot as plt
import time as tm
import datetime
from matplotlib.backends.backend_pdf import PdfPages
from sets import Set
import json, urllib

#User profiles summary dictionaries
userAge = {}
userSex = {}
userClass = {}
userEduc = {}
userCity = {}
userTime = {}
userRel = {}
userNeig = {}
vazio = 0

#possible questions
#possibleQuestions = ["agrad%C3%A1vel?", "seguro?"]
possibleQuestions = ["agradavel?", "seguro?"]

photosAnsweredPerQuestion = {possibleQuestions[0]:{}, possibleQuestions[1]:{}}

#Tasks definition
tasksIDDefinition = {}

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

	for age in userAge.keys():	
		if eval(age) != None and len(age) > 0:
			intAge = int(age)

			if intAge < 18:
				lev0 += 1 * userAge[age]
			elif intAge >= 18 and intAge <= 24:
				lev1 += 1 * userAge[age]
			elif intAge >= 25 and intAge <= 34:
				lev2 += 1 * userAge[age]
			elif intAge >= 35 and intAge <= 44:		
				lev3 += 1 * userAge[age]
			elif intAge >= 45 and intAge <= 54:		
				lev4 += 1 * userAge[age]
			elif intAge >= 55 and intAge <= 64:		
				lev5 += 1 * userAge[age]
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
	for sex in userSex.keys():
		if sex != None and len(sex) > 0:
			labels.append(sex)
			sizes.append(userSex[sex])
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
	for clas in userClass.keys():
		if clas != None and len(clas) > 0:
			labels.append(clas)
			sizes.append(userClass[clas])
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
	for educ in userEduc.keys():
		if educ != None and len(educ) > 0:
			labels.append(educ)
			sizes.append(userEduc[educ])
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
	for city in userCity.keys():
		if city != None and len(city) > 0:
			if 'campina' in city.lower():
				campinaCounting += userCity[city]
			elif 'pessoa' in city.lower():
				joaoPessoaCounting += userCity[city]
			else:
				labels.append(city[0:5])
				sizes.append(userCity[city])
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
	for time in userTime.keys():
		if time != None and len(time) > 0:
			intTime = int(time)
			if intTime < 10:
				lev1 += 1 * userTime[time]
			elif intTime >=10 and intTime < 20:
				lev2 += 1 * userTime[time]
			elif intTime >= 20 and intTime < 30:		
				lev3 += 1 * userTime[time]
			elif intTime >=30 and intTime < 40:		
				lev4 += 1 * userTime[time]
			elif intTime >=40 and intTime < 50:		
				lev5 += 1 * userTime[time]
			else:
				lev6 += 1 * userTime[time]
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
	for rel in userRel.keys():
		if rel != None and len(rel) > 0:
			labels.append(rel)
			sizes.append(userRel[rel])
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
	cen = userNeig['cen']
	lib = userNeig['lib']
	catol = userNeig['cat'] 

	labels = 'Centro', 'Liberdade', 'Catole', 'Nao responderam ou Nao conhecem'
	sizes = [cen, lib, catol, vazio]
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
	global vazio

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
			if age in userAge.keys():
				userAge[age] = userAge[age] + 1
			else:
				userAge[age] = 1
		if len(sex) > 0:
			if sex in userSex.keys():
				userSex[sex] = userSex[sex] + 1
			else:
				userSex[sex] = 1
		if len(currentClass) > 0:
			if currentClass in userClass.keys():
				userClass[currentClass] = userClass[currentClass] + 1
			else:
				userClass[currentClass] = 1
		if len(educ) > 0:
			if educ in userEduc.keys():
				userEduc[educ] = userEduc[educ] + 1
			else:
				userEduc[educ] = 1
		if len(city) > 0:
			if city in userCity.keys():
				userCity[city] = userCity[city] + 1
			else:
				userCity[city] = 1
		if len(time) > 0:
			if time in userTime.keys():
				userTime[time] = userTime[time] + 1
			else:
				userTime[time] = 1
		if len(rel) > 0:
			if rel in userRel.keys():
				userRel[rel] = userRel[rel] + 1
			else:
				userRel[rel] = 1
		if len(neig) > 0:
			if neig in userNeig.keys():
				userNeig[neig] = userNeig[neig] + 1
			else:
				userNeig[neig] = 1
			if 'cen' in neig.lower():
				if 'cen' in userNeig.keys():
					userNeig['cen'] = userNeig['cen'] + 1
				else:
					userNeig['cen'] = 1
			if 'lib' in neig.lower():
				if 'lib' in userNeig.keys():
					userNeig['lib'] = userNeig['lib'] + 1
				else:
					userNeig['lib'] = 1
			if 'cat' in neig.lower():
				if 'cat' in userNeig.keys():
					userNeig['cat'] = userNeig['cat'] + 1
				else:
					userNeig['cat'] = 1
		if len(neig) == 0:
			vazio += 1


def writeOutput(usersTasks):
	outputFile = open("usersInfo.dat", "w")
	answeredProfile = 0
	nAnsweredProfile = 0
	usersIDNAnsweredProfile = []
	finishTimeNAnswered = []

	#Writing users profile and tasks executed
	for userID in usersTasks.keys():
		userData = usersTasks[userID]
		print userID+"|"+str(userData[0])+"|"+str(userData[1])+"|"+str(userData[2])+"|"+str(userData[3])+"|"+str(userData[4])+"\n"
		outputFile.write(userID+"|"+str(userData[0])+"|"+str(userData[1])+"|"+str(userData[2])+"|"+str(userData[3])+"|"+str(userData[4])+"\n")
		countSummary(userData[0])
		
		if len(userData[0]) > 0:
			answeredProfile += 1
		else:
			nAnsweredProfile += 1
			usersIDNAnsweredProfile.append(userID)
			finishTimeNAnswered.append(userData[5])
	outputFile.close()
	
	#Writing profile summary
	outputFile = open("usersInfoSummary.dat", "w")
	outputFile.write("Answered\t" + str(answeredProfile) + "\t" + str(nAnsweredProfile) + "\t" + str(answeredProfile*1.0/(answeredProfile+nAnsweredProfile)) + "\t" + str(nAnsweredProfile*1.0/(answeredProfile+nAnsweredProfile)) + "\n")
	outputFile.write(str(userAge)+"\n")
	outputFile.write(str(userSex)+"\n")
	outputFile.write(str(userClass)+"\n")		
	outputFile.write(str(userEduc)+"\n")
	outputFile.write(str(userCity)+"\n")
	outputFile.write(str(userTime)+"\n")
	outputFile.write(str(userRel)+"\n")
	outputFile.write(str(userNeig)+"\n")
	outputFile.close()
	plotSummary()

	#Writing tasks definition
	outputFile = open("tasksDefinition.dat", "w")
	for taskID in tasksIDDefinition.keys():
		outputFile.write(taskID+"\t"+tasksIDDefinition[taskID].encode('utf-8')+"\n")
	outputFile.close()

	#Writing photos evaluated by user
	outputFile = open("usersPhotosAgrad.dat", "w")
	for userID in photosAnsweredPerQuestion[possibleQuestions[0]].keys():
		for photo in photosAnsweredPerQuestion[possibleQuestions[0]][userID]:
			outputFile.write(userID+"\t"+photo.encode('utf-8')+"\n")
	outputFile.close()

	#Writing photos evaluated by user
	outputFile = open("usersPhotosSeg.dat", "w")
	for userID in photosAnsweredPerQuestion[possibleQuestions[1]].keys():
		for photo in photosAnsweredPerQuestion[possibleQuestions[1]][userID]:
			outputFile.write(userID+"\t"+photo.encode('utf-8')+"\n")
	outputFile.close()

	#Writing users that did not answered profile
	outputFile = open("usersNAnswered.dat", "w")
	usersProfileFile = open("users.csv", "r")
	usersProfile = usersProfileFile.readlines()

	for index in range(0, len(usersIDNAnsweredProfile)):
		userID = usersIDNAnsweredProfile[index]
		for profile in usersProfile:
			data = profile.split(",")
			if data[0].strip() == userID:
				outputFile.write(userID+"\t"+data[2]+"\t"+str(finishTimeNAnswered[index])+"\n")
	outputFile.close()
	usersProfileFile.close()


def readUserData(lines1, lines2, outputFileName):
	""" Reading user profile """
	
	usersTasks = {}
	firstDate = datetime.date(1970, 6, 24)
	agrad_dic = {"agradavel?" : "agrad%C3%A1vel?", "agrad%C3%A1vel?" : "agradavel?"}

	#Reading from pybossa task-run CSV - V1
	for line in lines1:
		data = line.split("+")

		taskID = data[3]
		userID = data[4]
		timeInfo = data[6].split("T")[0].split("-")#2015-02-17T18:19:52.589591
		finish_time = datetime.date(int(timeInfo[0]), int(timeInfo[1]), int(timeInfo[2]))
		
		userAnswer = data[9].strip(' \t\n\r"')
		
		if userID in usersTasks.keys():
			userExecutions = usersTasks[userID]
		else:
			userExecutions = ["", [], [], [], [], firstDate]#Tasks for Agradavel e Seguro and their respective answers

		#In user answers that contain profile information extract profile
		if userAnswer[0] == '{':
			index = userAnswer.find("}")
			if index == -1:
				raise Exception("Line with profile does not contain final delimiter: " + userAnswer)
			currentAnswer = userAnswer[0:index+1]
			
			#Extracting profile
			userProfileData = currentAnswer.split("|")
			age = userProfileData[0].split("=")[1].encode('utf-8')
			sex = userProfileData[1].split("=")[1].encode('utf-8')
			currentClass = userProfileData[2].split("=")[1].encode('utf-8')
			educ =  userProfileData[3].split("=")[1].encode('utf-8')
			city = userProfileData[4].split("=")[1].encode('utf-8')
			time = userProfileData[5].split("=")[1].encode('utf-8')
			rel = userProfileData[6].split("=")[1].encode('utf-8')
			neig = userProfileData[7].split("=")[1]
			neig = neig[0:len(neig)-1]

			userExecutions[0] = age+"+"+sex+"+"+currentClass+"+"+educ+"+"+city+"+"+time+"+"+rel+"+"+neig
			
		#Saving photos that user evaluated
		index = userAnswer.find("Qual")
		userAnswer = userAnswer[index:].split(" ")
 		
		question = userAnswer[5].strip(' \t\n\r"')
		if 'agrad' in question and question == "agrad%C3%A1vel?":
			question = agrad_dic[question]
		answer = userAnswer[6].strip(' \t\n\r"')
		photo1 = userAnswer[7].strip(' \t\n\r"')
		photo2 = userAnswer[8].strip(' \t\n\r"')

		if userID in photosAnsweredPerQuestion[question].keys():
			photos = photosAnsweredPerQuestion[question][userID]
		else:
			photos = Set([])
		photos.add(photo1)
		photos.add(photo2)
		photosAnsweredPerQuestion[question][userID] = photos

		#Saving user answer near task ID
		if question == possibleQuestions[0]:#Agra
			userExecutions[1].append(taskID)
			userExecutions[3].append(answer)
		elif question == possibleQuestions[1]:#Seg
			userExecutions[2].append(taskID)
			userExecutions[4].append(answer)
		else:
			print "Error! " + question + " " + possibleQuestions[0] + " " + possibleQuestions[1]

		if finish_time > userExecutions[5]:
			userExecutions[5] = finish_time

		#Saving task ID definition
		tasksIDDefinition[taskID] = photo1+"\t"+photo2

		usersTasks[userID] = userExecutions

	#Reading from pybossa task-run CSV - V2
	for line in lines2:
		data = line.split("+")

		taskID = data[3]
		userID = data[4]
		userIP = data[5]
		timeInfo = data[6].split("T")[0].split("-")#2015-02-17T18:19:52.589591
		finish_time = datetime.date(int(timeInfo[0]), int(timeInfo[1]), int(timeInfo[2]))
		
		userAnswer = data[9].strip(' \t\n\r"')
		
		if userID in usersTasks.keys():
			userExecutions = usersTasks[userID]
		else:
			userExecutions = ["", [], [], [], [], firstDate]#Tasks for Agradavel e Seguro and their respective answers

		#In user answers that contain profile information extract profile: {"userProfile": {"city": "Campina Grande - State of Para\u00edba, Brazil", "age": 33, "sex": "M", "rel": "casado", "educ": "doutorado", "neig": ["cen"], "clas": "media alta"}, "question": "agradavel", "theLess": "https://contribua.org/bairros/oeste/liberdade/Rua_Edesio_Silva__602__180.jpg", "theMost": "https://contribua.org/bairros/norte/centro/Avenida_Presidente_Getulio_Vargas__395__270.jpg"}
		data = json.loads(userAnswer)

		if data.has_key('userProfile'):
			#Extracting profile
			userProfileData = data['userProfile']

			age = userProfileData['age']
			sex = userProfileData['sex'].encode('utf-8').strip(' \t\n\r"')
			currentClass = userProfileData['clas'].encode('utf-8').strip(' \t\n\r"')
			educ =  userProfileData['educ'].encode('utf-8').strip(' \t\n\r"')
			city = userProfileData['city'].encode('utf-8').strip(' \t\n\r"')
			#time = userProfileData['time'].strip(' \t\n\r"')
			rel = userProfileData['rel'].encode('utf-8').strip(' \t\n\r"')
			neig = userProfileData['neig']

			if len(city) == 0:
				if len(userIP) > 0:
					response = urllib.urlopen("http://ip-api.com/json/"+userIP)
					data = json.loads(response.read())
					city =  data['city'] + "," + data['country']

			userExecutions[0] = str(age)+"+"+sex+"+"+currentClass+"+"+educ+"+"+city+"+"+""+"+"+rel+"+"+str(neig)
		else:
			if len(userIP) > 0:
				response = urllib.urlopen("http://ip-api.com/json/"+userIP)
				data = json.loads(response.read())
				city =  data['city'] + "," + data['country']
				userExecutions[0] = ""+"+"+""+"+"+""+"+"+""+"+"+city+"+"+""+"+"+""+"+"+""
			
		#Saving photos that user evaluated
		question = data['question'].strip(' \t\n\r"')
		if 'agrad' in question and question == "agrad%C3%A1vel?":
			question = agrad_dic[question]

		answer = "Left*"
		photo1 = data['theMost'].strip(' \t\n\r"')
		photo2 = data['theLess'].strip(' \t\n\r"')

		#print str(photosAnsweredPerQuestion.keys())	
		if userID in photosAnsweredPerQuestion[question].keys():
			photos = photosAnsweredPerQuestion[question][userID]
		else:
			photos = Set([])
		photos.add(photo1)
		photos.add(photo2)
		photosAnsweredPerQuestion[question][userID] = photos

		#Saving user answer near task ID
		if question == possibleQuestions[0]:#Agra
			userExecutions[1].append(taskID)
			userExecutions[3].append(answer)
		elif question == possibleQuestions[1]:#Seg
			userExecutions[2].append(taskID)
			userExecutions[4].append(answer)
		else:
			print "Error! " + question

		if finish_time > userExecutions[5]:
			userExecutions[5] = finish_time

		#Saving task ID definition
		tasksIDDefinition[taskID] = photo1+"\t"+photo2

		usersTasks[userID] = userExecutions

	return usersTasks

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print "Uso: <arquivo com execucoes das tarefas e perfis dos usuarios - V1> <arquivo com execucoes das tarefas e perfis dos usuarios - V2>"
		sys.exit(1)

	dataFile1 = ""#open(sys.argv[1], 'r')
	dataFile2 = open(sys.argv[2], 'r')
	
	lines1 = []#dataFile1.readlines() - This file does not exist for this version of app!
	lines2 = dataFile2.readlines()

	usersTasks = readUserData(lines1, lines2, "users.dat")
	writeOutput(usersTasks)	
	#dataFile1.close()
	dataFile2.close()

