# coding=utf-8
# Prepares a HTML page containing the photos and their QScore per question, filtered according to an intersection file containing the set of photos to be considered or not, and prints the set of photos that will appear in the HTML page

import sys
from sets import Set

#possible questions
possibleQuestions = ["agrad%C3%A1vel?", "seguro?"]

mascFemFilter = {"agrad%C3%A1vel?" : ["https://contribua.org/bairros/norte/centro/Avenida_Presidente_Getulio_Vargas__395__270.jpg", "https://contribua.org/bairros/norte/centro/Rua_Elias_Aforas__67__0.jpg", "https://contribua.org/bairros/norte/centro/Rua_Felix_Araujo__48__270.jpg", "https://contribua.org/bairros/norte/centro/Avenida_Barao_Rio_Branco__141_90.jpg", "https://contribua.org/bairros/oeste/liberdade/Rua_Acre__635_90.jpg"], "seguro?" : ["https://contribua.org/bairros/norte/centro/Avenida_Presidente_Getulio_Vargas__395__90.jpg", "https://contribua.org/bairros/norte/centro/Rua_Manoel_P._de_Araujo__370_0.jpg", "https://contribua.org/bairros/oeste/liberdade/Rua_Odon_Bezerra__147_270.jpg", "https://contribua.org/bairros/oeste/catole/Rua_Honorio_de_Melo__240__270.jpg", "https://contribua.org/bairros/oeste/catole/Rua_Cristina_Procopio_da_Silva__62__270.jpg"]}
casaSoltFilter = {"agrad%C3%A1vel?" : ["https://contribua.org/bairros/norte/centro/Rua_Manoel_P._de_Araujo__370_0.jpg", "https://contribua.org/bairros/norte/centro/Rua_Pedro_Alvares_Cabral__129_180.jpg", "https://contribua.org/bairros/oeste/catole/Rua_Sebastiao_Vieira_da_Silva__1273__180.jpg", "https://contribua.org/bairros/oeste/liberdade/Rua_Riachuelo__455__0.jpg", "https://contribua.org/bairros/norte/centro/Rua_Coronel_Salvino_Figueiredo__251_270.jpg", "https://contribua.org/bairros/oeste/liberdade/Rua_Edesio_Silva__602__0.jpg 1.87155321469", "https://contribua.org/bairros/norte/centro/Avenida_Barao_Rio_Branco__141_90.jpg"], "seguro?" : ["https://contribua.org/bairros/norte/centro/Rua_Doutor_Severino_Cruz__411__270.jpg", "https://contribua.org/bairros/norte/centro/Rua_Pedro_Alvares_Cabral__129_180.jpg", "https://contribua.org/bairros/oeste/catole/Rua_Joao_Francisco_Mota__64__90.jpg", "https://contribua.org/bairros/oeste/liberdade/Rua_Edesio_Silva__602__180.jpg", "https://contribua.org/bairros/oeste/catole/Rua_Olegario_Mariano__139_90.jpg", "https://contribua.org/bairros/norte/centro/Avenida_Dom_Pedro_II__500_90.jpg"]}
jovAduFilter = {"agrad%C3%A1vel?" : [], "seguro?" : []}
medBaiFilter = {"agrad%C3%A1vel?" : [], "seguro?" : []}

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Uso: <arquivo com qscores ordenados> <arquivo de interseccao> <filter per score?>"
		sys.exit(1)
	
	dataFile = open(sys.argv[1], 'r')
	outputFile = open("question.html", 'w')
	outputFilter = open("questionFilter.html", 'w')
	
	if len(sys.argv) >= 3:
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

	if len(sys.argv) == 4:
		filterScore = bool(sys.argv[3])
	else:
		filterScore = False
		

	linesQScore = dataFile.readlines()

	results = {possibleQuestions[0]: [], possibleQuestions[1] : []}
	resultsFilter = {possibleQuestions[0]: [], possibleQuestions[1] : []}
	
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
				#print line.strip('\n')
		else:
			results[question].append(photo+" "+qscore)

		if filterScore:
			if photo in casaSoltFilter[question]:
				resultsFilter[question].append(photo+" "+qscore)
	
	#Writing html
	if filterScore:
		outputFilter.write("<body style=\"overflow:scroll\">\n");

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

	if filterScore:
		counter = 0
		for question, questionPhotos in resultsFilter.iteritems():
			outputFilter.write("<h2>"+question+"</h2>")
		
			outputFilter.write("<table>\n")
			outputFilter.write("<tr>\n")
			for data in questionPhotos:
				currentData = data.split(" ")
			
				outputFilter.write("<td><img src=\""+currentData[0]+"\" width=\"400\" height=\"300\"></td>\n")
				outputFilter.write("<td>"+currentData[0] + " " + currentData[1]+"</td>\n")
				counter += 1

				if counter % 3 == 0:
					outputFilter.write("</tr>\n")
					outputFilter.write("<tr>\n")

			outputFilter.write("</tr>\n")
			outputFilter.write("</table>")
	
	dataFile.close()
	outputFile.close()

	if filterScore:
		outputFilter.close()
