# coding=utf-8
# Prepares a HTML page the top and bottom 5 for regression residuals between groups

import sys
from sets import Set

def completeURL(photo):
	if 'liberdade' in photo or 'catole' in photo:
		return "https://contribua.org/bairros/oeste/"+photo
	else:
		return "https://contribua.org/bairros/norte/"+photo

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print "Uso: <arquivo com fotos e residuos> <questao>"
		sys.exit(1)

	dataFile = open(sys.argv[1], 'r')
	question = sys.argv[2]
	outputFile = open("topbot5.html", 'w')

	linesQScore = dataFile.readlines()
	header = linesQScore[0].split("\t")
	group1 = header[1]
	group2 = header[2]

	outputFile.write("<body style=\"overflow:scroll\">\n");
	outputFile.write("<h2>"+question + " " + group1 + " " + group2 +"</h2>")
	
	outputFile.write("<table>\n")
	outputFile.write("<tr>\n")
	counter = 0

	#Reading photos information
	for line in linesQScore[1:]:
		data = line.split("\t")
		print data
		
		question = data[0].strip(' \t\n\r')
		photoInfo = data[1].strip('\"\t\n\r')
		photo = completeURL(photoInfo)
		qscoreG1 = data[2].strip(' \t\n\r')
		qscoreG2 = data[3].strip(' \t\n\r')
		residual = data[4].strip(' \t\n\r')

		outputFile.write("<td><img src=\""+photo+"\" width=\"400\" height=\"300\"></td>\n")
		outputFile.write("<td>"+photoInfo + " " + qscoreG1 + " " + qscoreG2 + " " + residual +"</td>\n")
		counter += 1

		if counter % 3 == 0:
			outputFile.write("</tr>\n")
			outputFile.write("<tr>\n")

	outputFile.write("</tr>\n")
	outputFile.write("</table>")
	outputFile.write("</body>\n");	

