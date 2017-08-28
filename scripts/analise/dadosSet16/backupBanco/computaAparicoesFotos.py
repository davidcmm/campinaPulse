# coding=utf-8
# Le as definicoes de tarefas de acordo com MaxDiff para calcular a quantidade de tarefas em que cada foto aparece

import sys
import random
import json
import csv
import pandas as pd

possibleQuestions = ["agrad%C3%A1vel?", "seguro?"]
counters = { possibleQuestions[0] : {}, possibleQuestions[1]: {} }

def count_photos_appearances(dataFile):
	lines = dataFile.readlines()
	for line in lines:
		lineData = line.split("+")

		definition = lineData[7].strip(' \t\n\r"')
		data = json.loads(definition)

		if data['question'].strip(' \t\n\r"') == "agradavel":
			question = possibleQuestions[0]
		else:
			question = possibleQuestions[1]

		photos = [data['url_a'], data['url_b'], data['url_c'], data['url_d']]
		current_counters = counters[question]
		for photo in photos:
			if photo in current_counters.keys():
				counter = current_counters[photo]
			else:
				counter = 0
			current_counters[photo] = counter + 1

	#Showing appearances
	for question in counters.keys():
		question_data = counters[question]
		for photo in question_data.keys():
			photo_counter = question_data[photo]
			print (question + "\t" + str(photo) + "\t" + str(photo_counter))			 

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print ("Uso: <arquivo com definicoes das tarefas>")
		sys.exit(1)

	dataFile = open(sys.argv[1], 'r')
	count_photos_appearances(dataFile)


