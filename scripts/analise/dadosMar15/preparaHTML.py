# coding=utf-8

import sys

#possible questions
possibleQuestions = ["agrad%C3%A1vel?", "seguro?"]

if __name__ == "__main__":
	if len(sys.argv) < 1:
		print "Uso: <arquivo com dados>"
		sys.exit(1)
	
	dataFile = open(sys.argv[1], 'r')
	outputFile = open("question.html", 'w')
	lines = dataFile.readlines()
	
	counter = 0

	results = {possibleQuestions[0]: [], possibleQuestions[1] : []}

	for line in lines:
		data = line.split("\t")

		question = data[0].strip(' \t\n\r')
		photo = data[1].strip(' \t\n\r')
		qscore = data[2].strip(' \t\n\r')
		
		results[question].append(photo+" "+qscore)
	
	outputFile.write("<body style=\"overflow:scroll\">\n");
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
