# coding=utf-8
# Prepares a HTML page containing the photos and their QScore per question, filtered according to an intersection file containing the set of photos to be considered or not, and prints the set of photos that will appear in the HTML page

import sys
from sets import Set

controlPhoto = ["norte/centro/Avenida_Presidente_Getulio_Vargas__395__90.jpg", "norte/centro/Rua_Elias_Aforas__67__0.jpg", "oeste/liberdade/Rua_Odon_Bezerra__147_270.jpg", "norte/centro/Rua_Elias_Aforas__67__180.jpg", "oeste/liberdade/Rua_Riachuelo__930__0.jpg", "norte/centro/Rua_Manoel_P._de_Araujo__370_0.jpg", "norte/centro/Rua_Elias_Aforas__202_0.jpg", "norte/centro/Avenida_Barao_Rio_Branco__141_90.jpg", "norte/centro/Avenida_Presidente_Joao_Pessoa__128__90.jpg", "oeste/liberdade/Rua_Odon_Bezerra__306_270.jpg"]
otherPhotos = Set([])

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Uso: <arquivo com definições das tarefas>"
		sys.exit(1)

	dataFile = open(sys.argv[1], 'r')
	lines = dataFile.readlines()

	for line in lines:
		data = line.split(",")
		photo1 = data[7].strip("\"}{").split(":")[2]
		photo2 = data[9].strip("\"}{").split(":")[2]
		print photo1 + " " + photo2
		
		for photo in controlPhoto:
			if photo in photo1:
				otherPhotos.add(photo2)
			elif photo in photo2:
				otherPhotos.add(photo1)

	print str(otherPhotos) + " " + str(len(otherPhotos))
	for photo in otherPhotos:
		if controlPhoto[0] in photo:		
			print "True"

