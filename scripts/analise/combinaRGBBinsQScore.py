# coding=utf-8
# Combines RGB bins data and other data for images

import sys

#possible questions
possibleQuestions = ["agradavel?", "seguro?"]

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print "Uso: <arquivo com rgb bins> <arquivo com qscores e outros dados>"
		sys.exit(1)

	rgbs = open(sys.argv[1], "r")
	qscores = open(sys.argv[2], "r")
	
	qscoreLines = qscores.readlines()
	rgbLines = rgbs.readlines()

	#Reading qscores
	qscoreDic = []
	for line in qscoreLines[1:]:
		qscoreDic.append(line)

	#Reading rgb data
	rgbDic = {}	
	for line in rgbLines:
		data = line.split(" ")
		#print data
		photo = data[0]
		
		rgbDic[photo.strip()] = str(data[1:])

	#Writing outputFile with qscores and rgb
	outputFile = open("geralSetoresAJ_bins.dat","w")
	#outputFile.write("foto\tqscore\tred\tgreen\tblue\tdiag\thor\tvert\n")
	for line in qscoreDic:
			data = line.split(" ")
			photo = data[0]

			rgb = rgbDic[photo.split("/")[1]].strip('[]')
			outputFile.write(line+"\t"+rgb+"\n")
	outputFile.close()


		
