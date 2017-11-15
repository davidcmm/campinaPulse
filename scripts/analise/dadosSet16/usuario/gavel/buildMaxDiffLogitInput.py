# coding=utf-8
# Reads run.csv file and organizes respondents answers in a matrix with columns being all images and rows being images in the task and selected images as best and worst

import sys
from sets import Set
import random
import numpy
import json
import csv
import pandas as pd

#photos considered in comparisons
all_photos = Set([])

#possible questions
possibleQuestions = ["agrad%C3%A1vel?", "seguro?"]

#possible answers
left = 'Left'
right = 'Right'
notKnown = 'NotKnown'
completeTie = 'equal'


def readTasksDefinitions(lines_tasks):
	tasks_def = {}

	for line in lines_tasks:
		data = line.split("+")
		task_id = data[0].strip(' \t\n\r')
		current_def = json.loads(data[7].strip(' \t\n\r\"'))

		tasks_def[task_id] = current_def
		all_photos.add(current_def['url_a'].strip(' \t\n\r"'))
		all_photos.add(current_def['url_b'].strip(' \t\n\r"'))
		all_photos.add(current_def['url_c'].strip(' \t\n\r"'))
		all_photos.add(current_def['url_d'].strip(' \t\n\r"'))
	
	return tasks_def

def buildMaxDiffInput(lines, output_filename, tasks_def):
	#Reading from pybossa task-run CSV
	headers = list(all_photos)
	headers.sort()

	output = open(output_filename, 'w')
	output.write(','.join(headers)+"\n")

	for line in lines:
		lineData = line.split("+")

		executionID = lineData[0].strip(' \t\n\r"')
		taskID = lineData[3].strip(' \t\n\r"')
		userAnswer = lineData[9].strip(' \t\n\r"')

		#It is a new vote, read tasks definition from JSON!
		if executionID[0].lower() == 'n':
			data = json.loads(userAnswer)
			
			if "agrad" in data['question'].strip(' \t\n\r"'):
				question = possibleQuestions[0]
			else:
				question = possibleQuestions[1]

			photo1 = data['theMost'].strip(' \t\n\r"')
			photo2 = data['theLess'].strip(' \t\n\r"')

			taskDef = tasks_def[taskID]
			photos = Set( [taskDef['url_c'].strip(' \t\n\r"'), taskDef['url_b'].strip(' \t\n\r"'), taskDef['url_a'].strip(' \t\n\r"'), taskDef['url_d'].strip(' \t\n\r"')] )
			
			is_tie = photo1

			if photo1 != completeTie:
				photos.remove(photo1)
				photos.remove(photo2)
			else:
				photo1 = photos.pop()
				photo2 = photos.pop()
			
			photo3 = photos.pop()
			photo4 = photos.pop()
		
			#Finding index of items according to header
			index1 = headers.index(photo1)
			index2 = headers.index(photo2)
			index3 = headers.index(photo3)
			index4 = headers.index(photo4)
			answer_list = ["NA"] * 108
			#print "TASK > " + is_tie + "\t" + photo1 +"\t" + photo2+"\t" + str(index1) +"\t" + str(index2)

			#Saving votes from task-run
			if is_tie != completeTie:
				answer_list[index1] = "1"
				answer_list[index2] = "-1"
				answer_list[index3] = "0"
				answer_list[index4] = "0"
			#else:
			#	answer_list[index1] = "0"
			#	answer_list[index2] = "0"
			#	answer_list[index3] = "0"
			#	answer_list[index4] = "0"
			#print ">>> Linha atual " + ','.join(answer)
			output.write(','.join(answer_list)+"\n")

		else:#Old-fashioned way of capturing votes
			#In user answers that contain profile information, jump to comparison
			if userAnswer[0] == '{':
				index = userAnswer.find("Qual")
				if index == -1:
					raise Exception("Line with profile does not contain question: " + userAnswer)
				userAnswer = userAnswer[index:].split(" ")
			else:
				userAnswer = userAnswer.split(" ")

			question = userAnswer[5].strip(' \t\n\r"')
			answer = userAnswer[6].strip(' \t\n\r"')
			photo1 = userAnswer[7].strip(' \t\n\r"')
			photo2 = userAnswer[8].strip(' \t\n\r"')

			#Finding index of items according to header
			index1 = headers.index(photo1)
			index2 = headers.index(photo2)
			answer_list = ["NA"] * 108
			#print "TASK > " + answer + "\t" + photo1 +"\t" + photo2+"\t" + str(index1) +"\t" + str(index2)

			if answer == left:
				answer_list[index1] = "1"
				answer_list[index2] = "-1"
			elif answer == right:
				answer_list[index1] = "-1"
				answer_list[index2] = "1"
			#elif answer == notKnown:
			#	answer_list[index1] = "0"
			#	answer_list[index2] = "0"
			#print ">>> Linha atual " + ','.join(answer)
			output.write(','.join(answer_list)+"\n")	

	output.close()


if __name__ == "__main__":
	if len(sys.argv) < 3:
		print "Uso: <arquivo com execuções das tarefas> <tasks definition - V2>"
		sys.exit(1)

	dataFile = open(sys.argv[1], 'r')
	tasksFile = open(sys.argv[2], 'r')
	lines = dataFile.readlines()
	linesTasks = tasksFile.readlines()

	buildMaxDiffInput(lines, "maxdiff_rank_input_woties.dat", readTasksDefinitions(linesTasks))


