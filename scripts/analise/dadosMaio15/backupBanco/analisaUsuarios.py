import sys
import matplotlib.pyplot as plt
import time as tm
import datetime
from matplotlib.backends.backend_pdf import PdfPages
from sets import Set

#User profiles summary dictionaries
userAge = {}
userSex = {}
userClass = {}
userEduc = {}
userCity = {}
userTime = {}
userRel = {}
userNeig = {}

#possible questions
possibleQuestions = ["agrad%C3%A1vel?", "seguro?"]

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
		age = int(age)
		if age < 18:
			lev0 += 1
		elif age >= 18 and age <= 24:
			lev1 += 1
		elif age >= 25 and age <= 34:
			lev2 += 1
		elif age >= 35 and age <= 44:		
			lev3 += 1
		elif age >= 45 and age <= 54:		
			lev4 += 1
		elif age >= 55 and age <= 64:		
			lev5 += 1
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
		if 'campina' in city.lower():
			campinaCounting += userCity[city]
		elif 'pessoa' in city.lower():
			joaoPessoaCounting += userCity[city]
		else:
			labels.append(city)
			sizes.append(userCity[city])
	labels.append("Campina Grande")
	labels.append("Joao Pessoa")
	sizes.append(campinaCounting)
	sizes.append(joaoPessoaCounting)
	colors = ['yellowgreen', 'green', 'gold', 'lightskyblue', 'blue', 'lightcoral', 'red', 'black']
	plt.figure()
	plt.clf()
	plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True)
	plt.axis('equal')
	pp.savefig()
	pp.close()

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
		time = int(time)
		if time < 10:
			lev1 += 1
		elif time >=10 and time < 20:
			lev2 += 1
		elif time >= 20 and time < 30:		
			lev3 += 1
		elif time >=30 and time < 40:		
			lev4 += 1
		elif time >=40 and time < 50:		
			lev5 += 1
		else:
			lev6 += 1
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
	cen = 0
	lib = 0
	catol = 0
	vazio = 0
	for neig in userNeig.keys():
		if len(neig) == 0:
			vazio += 1
		else:		
			if 'cen' in neig.lower():
				cen += 1
			if 'lib' in neig.lower():
				lib += 1
			if 'cat' in neig.lower():
				catol += 1

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
	if len(profileInfo) > 0:
		#Extracting profile
		userProfileData = profileInfo.split("+")
		age = userProfileData[0]
		sex = userProfileData[1]
		currentClass = userProfileData[2]
		educ =  userProfileData[3]
		city = userProfileData[4]
		time = userProfileData[5]
		rel = userProfileData[6]
		neig = userProfileData[7]
		neig = neig[0:len(neig)]

		#Saving occurrences of profiles
		if age in userAge.keys():
			userAge[age] = userAge[age] + 1
		else:
			userAge[age] = 1
		if sex in userSex.keys():
			userSex[sex] = userSex[sex] + 1
		else:
			userSex[sex] = 1
		if currentClass in userClass.keys():
			userClass[currentClass] = userClass[currentClass] + 1
		else:
			userClass[currentClass] = 1
		if educ in userEduc.keys():
			userEduc[educ] = userEduc[educ] + 1
		else:
			userEduc[educ] = 1
		if city in userCity.keys():
			userCity[city] = userCity[city] + 1
		else:
			userCity[city] = 1
		if time in userTime.keys():
			userTime[time] = userTime[time] + 1
		else:
			userTime[time] = 1
		if rel in userRel.keys():
			userRel[rel] = userRel[rel] + 1
		else:
			userRel[rel] = 1
		if neig in userNeig.keys():
			userNeig[neig] = userNeig[neig] + 1
		else:
			userNeig[neig] = 1


def writeOutput(usersTasks):
	outputFile = open("usersInfo.dat", "w")
	answeredProfile = 0
	nAnsweredProfile = 0
	usersIDNAnsweredProfile = []
	finishTimeNAnswered = []

	#Writing users profile and tasks executed
	for userID in usersTasks.keys():
		userData = usersTasks[userID]
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
		outputFile.write(taskID+"\t"+tasksIDDefinition[taskID]+"\n")
	outputFile.close()

	#Writing photos evaluated by user
	outputFile = open("usersPhotosAgrad.dat", "w")
	for userID in photosAnsweredPerQuestion[possibleQuestions[0]].keys():
		for photo in photosAnsweredPerQuestion[possibleQuestions[0]][userID]:
			outputFile.write(userID+"\t"+photo+"\n")
	outputFile.close()

	#Writing photos evaluated by user
	outputFile = open("usersPhotosSeg.dat", "w")
	for userID in photosAnsweredPerQuestion[possibleQuestions[1]].keys():
		for photo in photosAnsweredPerQuestion[possibleQuestions[1]][userID]:
			outputFile.write(userID+"\t"+photo+"\n")
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


def readUserData(lines, outputFileName):
	""" Reading user profile """
	
	usersTasks = {}
	firstDate = datetime.date(1970, 6, 24)

	#Reading from pybossa task-run CSV
	for line in lines:
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
			age = userProfileData[0].split("=")[1]
			sex = userProfileData[1].split("=")[1]
			currentClass = userProfileData[2].split("=")[1]
			educ =  userProfileData[3].split("=")[1]
			city = userProfileData[4].split("=")[1]
			time = userProfileData[5].split("=")[1]
			rel = userProfileData[6].split("=")[1]
			neig = userProfileData[7].split("=")[1]
			neig = neig[0:len(neig)-1]

			userExecutions[0] = age+"+"+sex+"+"+currentClass+"+"+educ+"+"+city+"+"+time+"+"+rel+"+"+neig
			
		#Saving photos that user evaluated
		index = userAnswer.find("Qual")
		userAnswer = userAnswer[index:].split(" ")
 		
		question = userAnswer[5].strip(' \t\n\r"')
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
			print "Error! " + question

		if finish_time > userExecutions[5]:
			userExecutions[5] = finish_time

		#Saving task ID definition
		tasksIDDefinition[taskID] = photo1+"\t"+photo2

		usersTasks[userID] = userExecutions

	return usersTasks

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Uso: <arquivo com execucoes das tarefas e perfis dos usuarios>"
		sys.exit(1)
	dataFile = open(sys.argv[1], 'r')
	lines = dataFile.readlines()

	usersTasks = readUserData(lines, "users.dat")
	writeOutput(usersTasks)	
	dataFile.close()

