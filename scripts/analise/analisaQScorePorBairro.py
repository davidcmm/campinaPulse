# coding=utf-8

import sys
from scipy import stats
import numpy as np

#possible questions
possibleQuestions = ["agrad%C3%A1vel?", "seguro?"]

#Calculates the mean and confidence interval of QScore per district
if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Uso: <arquivo com qscore>"
		sys.exit(1)

	qscores = open(sys.argv[1], "r")
	
	qscoreLines = qscores.readlines()

	#Reading qscores
	qscoreDic = {possibleQuestions[0]:{}, possibleQuestions[1]: {}}	
	for line in qscoreLines:
		data = line.split("\t")
		photo = data[1].split("/")[5]+"/"+data[1].split("/")[6]#Saving district and street
		qscore = data[2]

		qscoreDic[data[0].strip()][photo.strip()] = qscore.strip()
	
	#Calculating mean qscores per district
	districtDic = {possibleQuestions[0]:{}, possibleQuestions[1]: {}}
	for question in possibleQuestions:
		for photo in qscoreDic[question].keys():
			qscore = qscoreDic[question][photo]
			district = photo.split("/")[0].strip()
			
			if district in districtDic[question].keys():
				districtData = districtDic[question][district]
			else:
				districtData = []
			districtData.append(float(qscore))
			districtDic[question][district] = districtData


	#Writing outputFile with qscores and rgb
	#outputFile = open("meanQScoreAgrad.dat","w")
	#print "Agrad"
	#print "bairro\tmedia\tdesvio\tmenor\tmaior"
	for district in districtDic[possibleQuestions[0]].keys():
		qscores = districtDic[possibleQuestions[0]][district]
		mean = np.mean(qscores)
		stDeviation = np.std(qscores)
		conf_int = stats.norm.interval(0.95, loc=mean, scale=stDeviation)

		#print district+"\t"+str(mean)+"\t"+str(stDeviation)+"\t"+str(conf_int[0])+"\t"+str(conf_int[1])
		for qscore in qscores:		
			print "agra\t" + district + "\t" + str(qscore)
	#outputFile.close()

	#Writing outputFile with qscores and rgb
	#outputFile = open("meanQScoreSeg.dat","w")
	#print "Seg"
	#print "bairro\tmedia\tdesvio\tmenor\tmaior"
	for district in districtDic[possibleQuestions[1]].keys():
		qscores = districtDic[possibleQuestions[1]][district]
		mean = np.mean(qscores)
		stDeviation = np.std(qscores)
		conf_int = stats.norm.interval(0.95, loc=mean, scale=stDeviation)

		#print district+"\t"+str(mean)+"\t"+str(stDeviation)+"\t"+str(conf_int[0])+"\t"+str(conf_int[1])
		for qscore in qscores:
			print "seg\t"+district + "\t" + str(qscore)
	#outputFile.close(),


		
