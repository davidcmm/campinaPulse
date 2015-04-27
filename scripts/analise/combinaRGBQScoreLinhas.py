# coding=utf-8
# Combines RGB, QScore and amount of lines for each photo according to input data

import sys

#possible questions
possibleQuestions = ["agrad%C3%A1vel?", "seguro?"]

if __name__ == "__main__":
	if len(sys.argv) < 4:
		print "Uso: <arquivo com rgb> <arquivo com qscore> <arquivo com linhas>"
		sys.exit(1)

	rgbs = open(sys.argv[1], "r")
	qscores = open(sys.argv[2], "r")
	linesCounting = open(sys.argv[3], "r")
	
	qscoreLines = qscores.readlines()
	rgbLines = rgbs.readlines()
	linesCountingLines = linesCounting.readlines()	

	#Reading qscores
	qscoreDic = {possibleQuestions[0]:{}, possibleQuestions[1]: {}}	
	for line in qscoreLines:
		data = line.split("\t")
		photo = data[1].split("/")[5]+"/"+data[1].split("/")[6]#Saving district and street
		qscore = data[2]

		qscoreDic[data[0].strip()][photo.strip()] = qscore.strip()

	#Reading rgb data
	rgbDic = {}	
	for line in rgbLines:
		data = line.split(" ")
		#print data
		photo = data[0]
		red = data[1]
		green = data[2]
		blue = data[3]
		
		rgbDic[photo.strip()] = (red.strip(), green.strip(), blue.strip())


	#Reading lines counting data
	linesCountingDic = {}	
	for line in linesCountingLines:
		data = line.split("\t")
		#print data
		photo = data[0]
		diagonal = data[1]
		horizontal = data[2]
		vertical = data[3]
		
		linesCountingDic[photo.strip()] = (diagonal.strip(), horizontal.strip(), vertical.strip())

	#Writing outputFile with qscores and rgb
	outputFile = open("rgbQScoreAgrad.dat","w")
	outputFile.write("foto\tqscore\tred\tgreen\tblue\tdiag\thor\tvert\n")
	for photo in qscoreDic[possibleQuestions[0]].keys():
		rgb = rgbDic[photo.split("/")[1]]
		lines = linesCountingDic[photo.split("/")[1]]
		qscore = qscoreDic[possibleQuestions[0]][photo]

		outputFile.write(photo+"\t"+qscore+"\t"+rgb[0]+"\t"+rgb[1]+"\t"+rgb[2]+"\t"+lines[0]+"\t"+lines[1]+"\t"+lines[2]+"\n")
	outputFile.close()

	#Writing outputFile with qscores and rgb
	outputFile = open("rgbQScoreSeg.dat","w")
	outputFile.write("foto\tqscore\tred\tgreen\tblue\tdiag\thor\tvert\n")
	for photo in qscoreDic[possibleQuestions[1]].keys():
		rgb = rgbDic[photo.split("/")[1]]
		lines = linesCountingDic[photo.split("/")[1]]
		qscore = qscoreDic[possibleQuestions[1]][photo]

		outputFile.write(photo+"\t"+qscore+"\t"+rgb[0]+"\t"+rgb[1]+"\t"+rgb[2]+"\t"+lines[0]+"\t"+lines[1]+"\t"+lines[2]+"\n")
	outputFile.close(),


		
