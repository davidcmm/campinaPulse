# coding=utf-8
# Prepares a HTML page containing the photos and their QScore per question, filtered according to an intersection file containing the set of photos to be considered or not, and prints the set of photos that will appear in the HTML page

import sys
from sets import Set

#possible questions
possibleQuestions = ["agrad%C3%A1vel?", "seguro?"]

def completePhoto(photo):
	if 'liberdade' in photo or 'catole' in photo:
		print photo+" oeste"
		return "oeste/"+photo
	if "centro" in photo:
		print photo+" norte"
		return "norte/"+photo

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Uso: <arquivo com fotos, grupos, questoes e diferencas> <arquivo com qscores por grupos>"
		sys.exit(1)
	
	dataFile = open(sys.argv[1], 'r')
	geralFile = open(sys.argv[2], 'r')

	outputFile = open("questionDiferencas.html", 'w')
	outputFile2 = open("questionDiferencasPorVisao.html", 'w')
	
	linesDiferencas = dataFile.readlines()
	linesGeral = geralFile.readlines()

	results = {'Hom\tMul\n' : [], 'Cas\tSol\n' : [], 'Med\tBaixa\n' : [], 'Jov\tAdu\n' : [], 'Medio\tPos\n' : []}
	groups = {'Masculino' : {}, 'Feminino' : {}, 'Media' : {}, 'Baixa' : {}, 'Jovem' : {}, 'Adulto' : {}, 'Medio' : {}, 'Pos' : {}}
	
	#Reading images with bigger differences, per group, for different visions
	for line in linesGeral[1:]:
		data = line.split(" ")
		photo = data[0]
		question = data[1]
		qscore = float(data[2])
		group = data[103]

		if group in groups.keys():
			if not groups[group].has_key(photo):
				groups[group][photo] = {}
			groups[group][photo][question] = qscore

	counter = 0
	outputFile2.write("<body style=\"overflow:scroll\">\n");
	for group in groups.keys():
		photos = groups[group].keys()
		photos.sort()

		outputFile2.write("<h2>"+group+"</h2>")
		outputFile2.write("<table>\n")
		outputFile2.write("<tr>\n")

		for i in range(0, len(photos)-1):
			current = ''.join(photos[i].replace("__", "+").replace("_", "+").split("+")[:-1])
			next = ''.join(photos[i+1].replace("__", "+").replace("_", "+").split("+")[:-1])

			if current == next:
			
				for question in groups[group][photos[i]]:
					if groups[group][photos[i+1]].has_key(question):
						questionCurrent = groups[group][photos[i]][question]
						questionNext = groups[group][photos[i+1]][question]	

						if abs(questionCurrent - questionNext) > 1.0:
							photoUrl = completePhoto(photos[i])
							photoUrl2 = completePhoto(photos[i+1])

							outputFile2.write("<td><img src=\"https://contribua.org/bairros/"+photoUrl+"\" width=\"400\" height=\"300\"></td>\n")
							outputFile2.write("<td><img src=\"https://contribua.org/bairros/"+photoUrl2+"\" width=\"400\" height=\"300\"></td>\n")
							outputFile2.write("<td>"+photos[i]+" "+photos[i+1]+" "+question+" "+str(questionCurrent)+" "+str(questionNext)+"</td>\n")		

							counter += 1

							if counter % 2 == 0:
								outputFile2.write("</tr>\n")
								outputFile2.write("<tr>\n")
		outputFile2.write("</tr>\n")
		outputFile2.write("</table>")

	outputFile2.write("</body>\n")

	#Reading images with bigger differences between groups
	counter = 0
	group = ""
	for i in range(0, 55):
		line = linesDiferencas[i]
		if counter == 11:
			counter = 0

		if counter == 0:
			group = line
			counter = counter + 1
		else:
			data = line.split(" ")

			photo = data[0].strip(' \t\n\r"')
			diferenca = data[6].strip(' \t\n\r')
			questao = data[9].strip(' \t\n\r"')
			results[group].append(photo+" "+diferenca+" "+questao)
			counter = counter + 1

	#Writing html
	outputFile.write("<body style=\"overflow:scroll\">\n");
	counter = 0
	for group, items in results.iteritems():
		#print str(group) + " " + str(items)
		outputFile.write("<h2>"+group+"</h2>")
		
		outputFile.write("<table>\n")
		outputFile.write("<tr>\n")
		for data in items:
			currentData = data.split(" ")
			
			outputFile.write("<td><img src=\"https://contribua.org/bairros/"+currentData[0]+"\" width=\"400\" height=\"300\"></td>\n")
			outputFile.write("<td>"+currentData[0] + " " + currentData[1]+" "+currentData[2]+"</td>\n")
			counter += 1

			if counter % 3 == 0:
				outputFile.write("</tr>\n")
				outputFile.write("<tr>\n")

		outputFile.write("</tr>\n")
		outputFile.write("</table>")
	outputFile.write("</body>\n")	

	dataFile.close()
	outputFile.close()
	outputFile2.close()
