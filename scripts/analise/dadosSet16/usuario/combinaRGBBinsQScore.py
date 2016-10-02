# coding=utf-8
# Combines RGB bins data and other data for images

import sys
import re

if __name__ == "__main__":
	if len(sys.argv) < 4:
		print "Uso: <arquivo com rgb bins> <arquivo com EHD> <arquivo com qscores e outros dados>"
		sys.exit(1)

	rgbs = open(sys.argv[1], "r")
	EHD = open(sys.argv[2], "r")
	qscores = open(sys.argv[3], "r")
	
	qscoreLines = qscores.readlines()
	EHDLines = EHD.readlines()
	rgbLines = rgbs.readlines()

	#Reading qscores
	qscoreDic = []
	for line in qscoreLines[1:]:
		qscoreDic.append(line)

	#Reading EHD data
	EHDDic = {}	
	for line in EHDLines:
		data = line.split(" ")
		#print data
		photo = data[0]
		
		EHDDic[photo.strip()] = str(data[1:])

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
			data = re.split(' |\t',line)
			#data = line.split(" \t")
			photo = data[0]

			rgb = rgbDic[photo.split("/")[1]].strip('[]')
			ehd = EHDDic[photo.split("/")[1]].strip('[]')
			outputFile.write(line+"\t"+rgb+"\t"+ehd+"\n")
	outputFile.close()


		
