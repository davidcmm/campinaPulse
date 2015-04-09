# coding=utf-8

import sys

#possible questions
possibleQuestions = ["agrad%C3%A1vel?", "seguro?"]

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Uso: <arquivo com rgb> <arquivo com qscore>"
		sys.exit(1)

	rgbs = open(sys.argv[1], "r")
	qscores = open(sys.argv[2], "r")
	
	qscoreLines = qscores.readlines()
	rgbLines = rgbs.readlines()

	#Reading qscores
	qscoreDic = {possibleQuestions[0]:{}, possibleQuestions[1]: {}}	
	for line in qscoreLines:
		data = line.split("\t")
		photo = data[1].split("/")[6]
		qscore = data[2]

		qscoreDic[data[0].strip()][photo.strip()] = qscore.strip()

	#Reading rgb data
	rgbDic = {}	
	for line in rgbLines:
		data = line.split(" ")
		print data
		photo = data[0]
		red = data[1]
		green = data[2]
		blue = data[3]
		
		rgbDic[photo.strip()] = (red.strip(), green.strip(), blue.strip())

	#Writing outputFile with qscores and rgb
	outputFile = open("rgbQScoreAgrad.dat","w")
	for photo in rgbDic.keys():
		rgb = rgbDic[photo]
		qscore = qscoreDic[possibleQuestions[0]][photo]

		outputFile.write(photo+"\t"+qscore+"\t"+rgb[0]+"\t"+rgb[1]+"\t"+rgb[2]+"\n")
	outputFile.close()

	#Writing outputFile with qscores and rgb
	outputFile = open("rgbQScoreSeg.dat","w")
	for photo in rgbDic.keys():
		rgb = rgbDic[photo]
		qscore = qscoreDic[possibleQuestions[1]][photo]

		outputFile.write(photo+"\t"+qscore+"\t"+rgb[0]+"\t"+rgb[1]+"\t"+rgb[2]+"\n")
	outputFile.close(),


		
