from gavel.models import *
from gavel.constants import *
import gavel.utils as utils
import gavel.crowd_bt as crowd_bt
from gavel.controllers.judge import *
from numpy.random import choice, random, shuffle
from functools import wraps
from datetime import datetime
import sys
import json
import csv
import pandas as pd

#possible questions
possibleQuestions = ["agrad%C3%A1vel?", "seguro?"]

#possible answers
left = 'Left'
right = 'Right'
notKnown = 'NotKnown'
completeTie = 'equal'


def readTasksDefinitions(linesTasks):
	""" Reading tasks definition for newer version (V2) of Como é Campina App"""
	tasksDef = {}

	for line in linesTasks:
		data = line.split("+")
		taskID = data[0].strip(' \t\n\r')
		currentDef = json.loads(data[7].strip(' \t\n\r\"'))

		tasksDef[taskID] = currentDef
	
	return tasksDef

def evaluateAllVotes(lines, outputFileName, tasksDefinitions):
	""" Reading Como é Campina csv run file and building annotators and items to check ranking according to CrowdBT. """

	#Create items dict
	items_agrad = {}
	items_seg = {}

	#Create annotators dict
	annotators = {}
	
	#Reading from pybossa task-run CSV
	for line in lines:
		lineData = line.split("+")

		executionID = lineData[0].strip(' \t\n\r"')
		taskID = lineData[3].strip(' \t\n\r"')
		annotatorID = lineData[4].strip(' \t\n\r"')
		userAnswer = lineData[9].strip(' \t\n\r"')

		#Checking and retrieving annotator
		if annotatorID in annotators.keys():
			annotator = annotators[annotatorID]
		else:
			annotator = Annotator(annotatorID, "testmail@gmail.com", annotatorID)
			annotators[annotatorID] = annotator

		#It is a new Como e Campina vote, read tasks definition from JSON!
		if executionID[0].lower() == 'n':
			data = json.loads(userAnswer)
			
			if data['question'].strip(' \t\n\r"') == "agradavel":
				question = possibleQuestions[0]
			else:
				question = possibleQuestions[1]

			photo1_name = data['theMost'].strip(' \t\n\r"')
			photo2_name = data['theLess'].strip(' \t\n\r"')

			taskDef = tasksDefinitions[taskID]
			photos = set( [taskDef['url_c'].strip(' \t\n\r"'), taskDef['url_b'].strip(' \t\n\r"'), taskDef['url_a'].strip(' \t\n\r"'), taskDef['url_d'].strip(' \t\n\r"')] )
			if photo1_name != completeTie:
				photos.remove(photo1_name)
				photos.remove(photo2_name)
			else:
				photo1_name = photos.pop()
				photo2_name = photos.pop()
			
			photo3_name = photos.pop()
			photo4_name = photos.pop()

			#Checking and retrieving photos information
			if question == possibleQuestions[0]:#Pleasantness
				items_map = items_agrad
			else:#Safety
				items_map = items_seg

			if photo1_name in items_map.keys():
				photo1 = items_map[photo1_name]
			else:
				photo1 = Item(photo1_name, "campina grande", photo1_name)				
				items_map[photo1_name] = photo1
			if photo2_name in items_map.keys():
				photo2 = items_map[photo2_name]
			else:
				photo2 = Item(photo2_name, "campina grande", photo2_name)				
				items_map[photo2_name] = photo2
			if photo3_name in items_map.keys():
				photo3 = items_map[photo3_name]
			else:
				photo3 = Item(photo3_name, "campina grande", photo3_name)				
				items_map[photo3_name] = photo3
			if photo4_name in items_map.keys():
				photo4 = items_map[photo4_name]
			else:
				photo4 = Item(photo4_name, "campina grande", photo4_name)				
				items_map[photo4_name] = photo4

			#Saving votes from task-run
			if photo1 != completeTie:
				#Vote 1
				annotator.prev = photo1
				annotator.next = photo2
				perform_vote(annotator, next_won=False)
				decision = Decision(annotator, winner=annotator.next, loser=annotator.prev)
				annotator.next.viewed.append(annotator)
				annotator.ignore.append(annotator.prev)

				#Vote 2
				annotator.prev = photo1
				annotator.next = photo3
				perform_vote(annotator, next_won=False)
				decision = Decision(annotator, winner=annotator.next, loser=annotator.prev)
				annotator.next.viewed.append(annotator)
				annotator.ignore.append(annotator.prev)

				#Vote 3
				annotator.prev = photo1
				annotator.next = photo4
				perform_vote(annotator, next_won=False)
				decision = Decision(annotator, winner=annotator.next, loser=annotator.prev)
				annotator.next.viewed.append(annotator)
				annotator.ignore.append(annotator.prev)

				#Vote 4
				annotator.prev = photo2
				annotator.next = photo3
				perform_vote(annotator, next_won=True)
				decision = Decision(annotator, winner=annotator.next, loser=annotator.prev)
				annotator.next.viewed.append(annotator)
				annotator.ignore.append(annotator.prev)

				#Vote 5
				annotator.prev = photo2
				annotator.next = photo4
				perform_vote(annotator, next_won=True)
				decision = Decision(annotator, winner=annotator.next, loser=annotator.prev)
				annotator.next.viewed.append(annotator)
				annotator.ignore.append(annotator.prev)

				#Vote 6
				annotator.prev = photo3
				annotator.next = photo4
				annotator.ignore.append(annotator.prev)
				annotator.ignore.append(annotator.next)

			else:
				#Vote 1
				annotator.prev = photo1
				annotator.next = photo2
				annotator.ignore.append(annotator.prev)
				annotator.ignore.append(annotator.next)

				#Vote 2
				annotator.prev = photo1
				annotator.next = photo3
				annotator.ignore.append(annotator.prev)
				annotator.ignore.append(annotator.next)

				#Vote 3
				annotator.prev = photo1
				annotator.next = photo4
				annotator.ignore.append(annotator.prev)
				annotator.ignore.append(annotator.next)

				#Vote 4
				annotator.prev = photo2
				annotator.next = photo3
				annotator.ignore.append(annotator.prev)
				annotator.ignore.append(annotator.next)

				#Vote 5
				annotator.prev = photo2
				annotator.next = photo4
				annotator.ignore.append(annotator.prev)
				annotator.ignore.append(annotator.next)

				#Vote 6
				annotator.prev = photo3
				annotator.next = photo4
				annotator.ignore.append(annotator.prev)
				annotator.ignore.append(annotator.next)

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
			photo1_name = userAnswer[7].strip(' \t\n\r"')
			photo2_name = userAnswer[8].strip(' \t\n\r"')

			#Checking and retrieving photos information
			if question == possibleQuestions[0]:#Pleasantness
				items_map = items_agrad
			else:#Safety
				items_map = items_seg

			if photo1_name in items_map.keys():
				photo1 = items_map[photo1_name]
			else:
				photo1 = Item(photo1_name, "campina grande", photo1_name)				
				items_map[photo1_name] = photo1
			if photo2_name in items_map.keys():
				photo2 = items_map[photo2_name]
			else:
				photo2 = Item(photo2_name, "campina grande", photo2_name)				
				items_map[photo2_name] = photo2
		

			#Saving votes from task-run
			annotator.prev = photo1
			annotator.next = photo2
			if answer == left:
				perform_vote(annotator, next_won=False)
				decision = Decision(annotator, winner=annotator.next, loser=annotator.prev)
				annotator.next.viewed.append(annotator)
				annotator.ignore.append(annotator.prev)
			elif answer == right:
				perform_vote(annotator, next_won=True)
				decision = Decision(annotator, winner=annotator.next, loser=annotator.prev)
				annotator.next.viewed.append(annotator)
				annotator.ignore.append(annotator.prev)
			elif answer == notKnown:
				annotator.ignore.append(annotator.prev)
				annotator.ignore.append(annotator.next)

	#Output file
	output = open(outputFileName, 'w')
	for item_name, item in items_agrad.items():
		output.write(possibleQuestions[0]+ "\t" + item_name+ "\t" + str(item.mu) + "\t" + str(item.sigma_sq)+'\n')
	for item_name, item in items_seg.items():
		output.write(possibleQuestions[1]+ "\t" + item_name+ "\t" + str(item.mu) + "\t" + str(item.sigma_sq)+'\n')
	output.close()

if __name__ == '__main__':

	if len(sys.argv) < 2:
		print("Uso: <arquivo com execuções das tarefas> <tasks definition - V2>")
		sys.exit(1)

	dataFile = open(sys.argv[1], 'r')
	tasksFile = open(sys.argv[2], 'r')

	lines = dataFile.readlines()
	linesTasks = tasksFile.readlines()

	evaluateAllVotes(lines, "allPairwiseComparison.dat", readTasksDefinitions(linesTasks))

	#Create items
	#items = {}
	#for i in range(1, 5):
	#	items["item"+str(i)] = Item("item"+str(i), "campina grande", "item"+str(i))

	#Create annotators
	#annotators = {}
	#for i in ["david", "jose", "pablo"]:
	#	annotators[i] = Annotator(i, "davcandeia@gmail.com", i)

	#Build relations and vote!
	#for annotator in annotators.values():
	#	for data in [ [items["item1"], items["item4"]], [items["item1"], items["item3"]], [items["item3"], items["item2"]] ]:
#
#
#			if annotator.name == "david" or annotator.name == "pablo":
#				annotator.prev = data[0]
#				annotator.next = data[1]
#			else:
#				annotator.prev = data[1]
#				annotator.next = data[0]
#			
#			#Choosing whether prev or next (left or right) won!
#			perform_vote(annotator, next_won=True)
#			decision = Decision(annotator, winner=annotator.next, loser=annotator.prev)
#			annotator.next.viewed.append(annotator)
#			#annotator.prev = annotator.next
#			annotator.ignore.append(annotator.prev)
#			#if request.form['action'] == 'Skip':
 #           		#	annotator.ignore.append(annotator.next)
#
#	#Showing results!
#	for item in items.values():
#		print("Item " + str(item.name) + " mu " + str(item.mu) + " sq " + str(item.sigma_sq) )
