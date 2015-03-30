import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

#User profiles summary dictionaries
userAge = {}
userSex = {}
userClass = {}
userEduc = {}
userCity = {}
userTime = {}
userRel = {}
userNeig = {}


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
	for neig in userNeig.keys():
		if 'cen' in neig.lower():
			cen += 1
		if 'lib' in neig.lower():
			lib += 1
		if 'cat' in neig.lower():
			catol += 1

	labels = 'Centro', 'Liberdade', 'Catole'
	sizes = [cen, lib, catol]
	colors = ['yellowgreen', 'lightskyblue', 'lightcoral']
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

def writeOutput(usersTasks):
	outputFile = open("usersInfo.dat", "w")

	#Writing users profile information and tasks executed
	for userID in usersTasks.keys():
		userData = usersTasks[userID]
		outputFile.write(userID+"+"+str(userData[0])+"+"+str(userData[1])+"\n")
	outputFile.close()
	
	#Writing profile summary
	outputFile = open("usersInfoSummary.dat", "w")
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


def readUserData(lines, outputFileName):
	""" Reading user profile """
	
	usersTasks = {}

	#Reading from pybossa task-run CSV
	for line in lines:
		data = line.split("+")

		taskID = data[3]
		userID = data[4]
		userAnswer = data[9].strip(' \t\n\r"')
		
		if userID in usersTasks.keys():
			userExecutions = usersTasks[userID]
		else:
			userExecutions = ["", []]
		userExecutions[1].append(taskID)

		#In user answers that contain profile information, jump to comparison
		if userAnswer[0] == '{':
			index = userAnswer.find("}")
			if index == -1:
				raise Exception("Line with profile does not contain final delimiter: " + userAnswer)
			userAnswer = userAnswer[0:index+1]
			
			userExecutions[0] = userAnswer

			#Extracting profile
			userProfileData = userAnswer.split("|")
			age = userProfileData[0].split("=")[1]
			sex = userProfileData[1].split("=")[1]
			currentClass = userProfileData[2].split("=")[1]
			educ =  userProfileData[3].split("=")[1]
			city = userProfileData[4].split("=")[1]
			time = userProfileData[5].split("=")[1]
			rel = userProfileData[6].split("=")[1]
			neig = userProfileData[7].split("=")[1]
			neig = neig[0:len(neig)-1]

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

