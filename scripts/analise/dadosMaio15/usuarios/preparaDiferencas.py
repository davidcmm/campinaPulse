# coding=utf-8
# Prepares a HTML page containing the photos and their QScore per question, filtered according to an intersection file containing the set of photos to be considered or not, and prints the set of photos that will appear in the HTML page

import sys
from sets import Set
import numpy

#possible questions
possibleQuestions = ["agrad%C3%A1vel?", "seguro?"]

def compare(item1, item2):
    info1 = abs(float(item1.split(" ")[2]) - float(item1.split(" ")[3]))
    info2 = abs(float(item2.split(" ")[2]) - float(item2.split(" ")[3]))
    if info1 < info2:
	return -1
    elif info1 > info2:
	return 1
    else:
	return 0

def completePhoto(photo):
	if 'liberdade' in photo or 'catole' in photo:
		#print photo+" oeste"
		return "oeste/"+photo
	if "centro" in photo:
		#print photo+" norte"
		return "norte/"+photo

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Uso: <arquivo com fotos, grupos, questoes e diferencas> <arquivo com qscores por grupos> <arquivo com fotos, questao, qscore e desvio>"
		sys.exit(1)
	
	dataFile = open(sys.argv[1], 'r')
	geralFile = open(sys.argv[2], 'r')
	dispersionFile = open(sys.argv[3], 'r')

	outputFile = open("questionDiferencas.html", 'w')
	outputFile2 = open("questionDiferencasPorVisao.html", 'w')
	outputFile3 = open("questionDiferencasPorDispersao.html", 'w')
	
	linesDiferences = dataFile.readlines()
	linesGeral = geralFile.readlines()
	linesDisp = dispersionFile.readlines()

	results = {'Hom\tMul\n' : [], 'Cas\tSol\n' : [], 'Med\tBaixa\n' : [], 'Jov\tAdu\n' : [], 'Medio\tPos\n' : []}
	groups = {'Masculino' : {}, 'Feminino' : {}, 'Media' : {}, 'Baixa' : {}, 'Jovem' : {}, 'Adulto' : {}, 'Medio' : {}, 'Pos' : {}, 'Geral' : {}}
	disp = {possibleQuestions[0] : {}, possibleQuestions[1]: {}}
	dispPhotosOrder = {possibleQuestions[0] : [], possibleQuestions[1]: []}	

	#Reading images qscore and sd per group and question 
	for i in range(0, len(linesDisp)):
		data = linesDisp[i].split(" ")
		question = data[1].strip("\" ")
		group = data[2].strip()
		photo = data[3].strip()
		qscore = data[4].strip()
		sd = data[5].strip()

		#disp[question][photo] = position + " "
		if group == "Feminino":
			disp[question][photo] = str(i) + " " + question + " " + group + " " + photo + " " + str(qscore) + " " + str(sd)
			dispPhotosOrder[question].append(photo)


	#Reading images general information and qscores
	for line in linesGeral[1:]:
		data = line.split(" ")
		photo = data[0].strip()
		question = data[1].strip()
		qscores = [float(x) for x in data[2:103]]
		group = data[103].strip()

		if group in groups.keys():
			if not groups[group].has_key(photo):
				groups[group][photo] = {}
			groups[group][photo][question] = qscores

		#Complementing dispersion info
		#if disp[question].has_key(photo) and group == "Geral":
		#	values = []
		#	for i in range(3, 103):
		#		values.append(float(data[i]))
		#	disp[question][photo] += str(qscore)+" "+str(numpy.std(values))+" "

	#Writing html for differences according to photo angle
	counter = 0
	outputFile2.write("<body style=\"overflow:scroll\">\n");
	for group in groups.keys():
		photos = groups[group].keys()
		photos.sort()

		outputFile2.write("<h2>"+group+"</h2>")

		questions = ["agrad%C3%A1vel?", "seguro?"]

		for question in questions:
			outputFile2.write("<h3>"+question+"</h3>")
			outputFile2.write("<table>\n")
			outputFile2.write("<tr>\n")
			writeDataList = []

			#Selecting photos to show!
			for i in range(0, len(photos)-1):
				current = ''.join(photos[i].replace("__", "+").replace("_", "+").split("+")[:-1])
				next = ''.join(photos[i+1].replace("__", "+").replace("_", "+").split("+")[:-1])

				if current == next:
					#for question in groups[group][photos[i]]:
						if groups[group][photos[i+1]].has_key(question) and groups[group][photos[i]].has_key(question):
							questionCurrent = groups[group][photos[i]][question][0]
							questionNext = groups[group][photos[i+1]][question][0]

							#Photos with qscore difference greater than 1.0
							if abs(questionCurrent - questionNext) > 1.0:
								sd = numpy.std(groups[group][photos[i]][question])
								sd2 = numpy.std(groups[group][photos[i+1]][question])
								writeDataList.append(photos[i]+" "+photos[i+1]+" "+str(questionCurrent) + " " + str(questionCurrent + (sd/100) * 1.959964) + " " + str(questionCurrent - (sd/100) * 1.959964) + " " + str(questionNext) + " " + str(questionNext + (sd2/100) * 1.959964) + " " + str(questionNext - (sd2/100) * 1.959964))

			#Building html elements to show photos			
			writeDataList = sorted(writeDataList, compare)	
			for i in range(0, len(writeDataList)-1):		
				data = writeDataList[i].split(" ")
				photoUrl = completePhoto(data[0])
				photoUrl2 = completePhoto(data[1])

				outputFile2.write("<td><img src=\"https://contribua.org/bairros/"+photoUrl+"\" width=\"400\" height=\"300\"></td>\n")
				outputFile2.write("<td><img src=\"https://contribua.org/bairros/"+photoUrl2+"\" width=\"400\" height=\"300\"></td>\n")
				outputFile2.write("<td>"+str(data)+"</td>\n")		
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
		line = linesDiferences[i]
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

	#Writing html for differences according groups differences
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

	#Writing html for differences according to photo qscores dispersion
	outputFile3.write("<body style=\"overflow:scroll\">\n");
	counter = 0
	for question in disp.keys():
		photosOfQuestion = disp[question].keys()
		outputFile3.write("<h2>"+question+"</h2>")
		
		outputFile3.write("<table>\n")
		outputFile3.write("<tr>\n")
		for photo in dispPhotosOrder[question]:
			if photo in photosOfQuestion:
				currentData = disp[question][photo]
				photoUrl = completePhoto(photo)
			
				outputFile3.write("<td><img src=\"https://contribua.org/bairros/"+photoUrl+"\" width=\"400\" height=\"300\"></td>\n")
				outputFile3.write("<td>"+ currentData +"</td>\n")
				counter += 1

				if counter % 3 == 0:
					outputFile3.write("</tr>\n")
					outputFile3.write("<tr>\n")

		outputFile3.write("</tr>\n")
		outputFile3.write("</table>")
	outputFile3.write("</body>\n")	

	dataFile.close()
	geralFile.close()
	dispersionFile.close()
	outputFile.close()
	outputFile2.close()
	outputFile3.close()
