# coding=utf-8
# Prepares a HTML page containing the photos and their QScore per question, filtered according to an intersection file containing the set of photos to be considered or not, and prints the set of photos that will appear in the HTML page

import sys
from sets import Set

#possible questions
possibleQuestions = ["agrad%C3%A1vel?", "seguro?"]

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Uso: <arquivo com qscores ordenados> <arquivo de interseccao>"
		sys.exit(1)
	
	dataFile = open(sys.argv[1], 'r')
	outputFile = open("question.html", 'w')
	if len(sys.argv) == 3:
		intersectionFile = open(sys.argv[2], 'r')
		linesInter = intersectionFile.readlines()

		data1 = linesInter[0].split("\t")
		question1 = data1[0].strip()
		set1 = eval(data1[2].strip())
		data2 = linesInter[1].split("\t")
		question2 = data2[0].strip()
		set2 = eval(data2[2].strip())

		photosToFilter = {question1 : set1, question2 : set2} 		
	else:
		photosToFilter = {}

	linesQScore = dataFile.readlines()

	results = {possibleQuestions[0]: [], possibleQuestions[1] : []}
	
	#Reading photos information
	for line in linesQScore:
		data = line.split("\t")

		question = data[0].strip(' \t\n\r')
		photo = data[1].strip(' \t\n\r')
		qscore = data[2].strip(' \t\n\r')
		
		if len(photosToFilter) > 0:
			currentFilter = photosToFilter[question]
			if photo in currentFilter:
				results[question].append(photo+" "+qscore)
				#print question+"\t"+photo+"\t"+qscore				
				print line.strip('\n')
		else:
			results[question].append(photo+" "+qscore)
	
	#Writing html
	outputFile.write("<body style=\"overflow:scroll\">\n");
	counter = 0
	for question, questionPhotos in results.iteritems():
		outputFile.write("<h2>"+question+"</h2>")
		
		outputFile.write("<table>\n")
		outputFile.write("<tr>\n")
		for data in questionPhotos:
			currentData = data.split(" ")
			
			outputFile.write("<td><img src=\""+currentData[0]+"\" width=\"400\" height=\"300\"></td>\n")
			outputFile.write("<td>"+currentData[0] + " " + currentData[1]+"</td>\n")
			counter += 1

			if counter % 3 == 0:
				outputFile.write("</tr>\n")
				outputFile.write("<tr>\n")

		outputFile.write("</tr>\n")
		outputFile.write("</table>")
	outputFile.write("</body>\n");	
	
	dataFile.close()
	outputFile.close()
