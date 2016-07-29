from sklearn import datasets
from sklearn.naive_bayes import GaussianNB
import sys
import numpy as np
import json
import random

def convertUserInfo(userInfo):
	genderDic = {"masculino" : 0, "feminino" : 1}
	incomeDic = {"baixa" : 0, "media baixa" : 1, "media" : 2, "media alta" : 3, "alta" : 4}
	educDic = {"ensino medio" : 0, "graduacao" : 1, "mestrado" : 2, "doutorado" : 3}
	maritalDic = {"solteiro" : 0, "casado" : 1, "divorciado" : 2, "vi\\u00favo" : 3}

	#age, gender, income, education, city, marital status
	age = userInfo[0].strip(' \t\n\r')
	gender = userInfo[1].strip(' \t\n\r')
	income = userInfo[2].strip(' \t\n\r')
	education = userInfo[3].strip(' \t\n\r')
	marital = userInfo[5].strip(' \t\n\r')

	return [int(age), genderDic[gender], incomeDic[income], educDic[education], maritalDic[marital]]

def convertImageInfo(imageInfo):
	neigDic = {"centro" : 0, "liberdade" : 1, "catole" : 2}
	graffitiDic = {"Yes" : 1, "No" : 0}
	
	newValues = []
	for i in range(0, len(imageInfo)):
		if i == 10 or i == 22:
			newValues.append(graffitiDic[imageInfo[i].strip(' \t\n\r')])
		elif i == 11 or i == 23:
			newValues.append(neigDic[imageInfo[i].strip(' \t\n\r')])
		else:
			newValues.append(float(imageInfo[i].strip(' \t\n\r')))

	return newValues

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Uso: <arquivo com dados das preferencias de fotos, dados das fotos e dos usuarios>"
		sys.exit(1)

	#Reading data for Como e Campina images!
	inputLines = open(sys.argv[1], 'r').readlines()
	answerAgrad = []
	predictorsAgrad = []
	answerSeg = []
	predictorsSeg = []

	for line in inputLines[1:]:
		lineData = line.split("\t")
		question = lineData[0]

		userInfoConverted = convertUserInfo(lineData[5:11])
		imageInfoConverted = convertImageInfo(lineData[11:])

		userInfoConverted.extend(imageInfoConverted)

		if 'agrad' in question.lower():
			answerAgrad.append(int(lineData[3]))#Preferred image
			predictorsAgrad.append(userInfoConverted)#Predictors
		else:
			answerSeg.append(int(lineData[3]))#Preferred image
			predictorsSeg.append(userInfoConverted)#Predictors

	#print str(len(predictorsAgrad))
	#print str(len(answerAgrad))
	#print str(np.array(predictorsAgrad))
	#print str(np.array(answerAgrad).astype(np.float))

	#Pleasantness
	indexesToTrain = random.sample( range(0,len(answerAgrad)), int(len(answerAgrad)*0.8) )#Separating training data and test data!
	indexesToTest = list( set(range(0, len(answerAgrad))) - set(indexesToTrain) )

	predictorsInput = np.array(predictorsAgrad)[indexesToTrain]
	answersInput = np.array(answerAgrad)[indexesToTrain]
	predictorsOutput = np.array(predictorsAgrad)[indexesToTest]
	answersOutput = np.array(answerAgrad)[indexesToTest]

	gnb = GaussianNB()
	y_pred = gnb.fit( predictorsInput, answersInput ).predict( predictorsOutput )

	print( "Number of mislabeled points out of a total %d points : %d" % (len(answersOutput), (answersOutput != y_pred).sum()) )

	#Safety
	indexesToTrain = random.sample( range(0,len(answerSeg)), int(len(answerSeg)*0.8) )#Separating training data and test data!
	indexesToTest = list( set(range(0, len(answerSeg))) - set(indexesToTrain) )

	predictorsInput = np.array(predictorsSeg)[indexesToTrain]
	answersInput = np.array(answerSeg)[indexesToTrain]
	predictorsOutput = np.array(predictorsSeg)[indexesToTest]
	answersOutput = np.array(answerSeg)[indexesToTest]

	gnb = GaussianNB()
	y_pred = gnb.fit( predictorsInput, answersInput ).predict( predictorsOutput )

	print( "Number of mislabeled points out of a total %d points : %d" % (len(answersOutput), (answersOutput != y_pred).sum()) )

	#iris = datasets.load_iris()
	#print str(iris.data) + " " + str(len(iris.data))
	#print str(iris.target) + " " + str(len(iris.target))

	#gnb = GaussianNB()
	#y_pred = gnb.fit(iris.data, iris.target).predict(iris.data)
	#print str(type(iris.data)) + " " + str(type(iris.target))

	#print("Number of mislabeled points out of a total %d points : %d" % (iris.data.shape[0],(iris.target != y_pred).sum()))


	
