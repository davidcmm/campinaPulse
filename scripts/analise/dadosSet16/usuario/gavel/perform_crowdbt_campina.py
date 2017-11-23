# coding=utf-8

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
			is_tie = photo1_name

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
			if is_tie != completeTie:
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

def extract_all_items(tasks_def):
	items_map = {}
	for task_id in tasks_def.keys():
		taskDef = tasks_def[task_id]
		photo1_name = taskDef['url_a'].strip(' \t\n\r"')
		photo2_name = taskDef['url_b'].strip(' \t\n\r"')
		photo3_name = taskDef['url_c'].strip(' \t\n\r"')
		photo4_name = taskDef['url_d'].strip(' \t\n\r"')
		
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
	return items_map


def simulateCrowdBT(lines, output_filename, tasks_def, current_question):
	items_map = extract_all_items(tasks_def)
	
	#Create annotators dict
	annotators = {}
	annotators_exec = {}
	annotators_already_started = set([])

	#Building a dict, for each annotator, of photos compared and their answers
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
			
			if "agrad" in data['question'].strip(' \t\n\r"'):
				question = possibleQuestions[0]
			else:
				question = possibleQuestions[1]

			if current_question == question:

				photo1_name = data['theMost'].strip(' \t\n\r"')
				photo2_name = data['theLess'].strip(' \t\n\r"')
				is_tie = photo1_name

				taskDef = tasks_def[taskID]
				photos = set( [taskDef['url_c'].strip(' \t\n\r"'), taskDef['url_b'].strip(' \t\n\r"'), taskDef['url_a'].strip(' \t\n\r"'), taskDef['url_d'].strip(' \t\n\r"')] )
				if photo1_name != completeTie:
					photos.remove(photo1_name)
					photos.remove(photo2_name)
				else:
					photo1_name = photos.pop()
					photo2_name = photos.pop()
			
				photo3_name = photos.pop()
				photo4_name = photos.pop()

				if annotatorID not in annotators_already_started:#Suppose annotator start with photo1 and photo2
					#Simulating that these first two photos were recommended
					photo1 = items_map[photo1_name]
					photo2 = items_map[photo2_name]
					annotator.update_next(photo1)
					annotator.prev = annotator.next
					annotator.update_next(photo2)

					annotators_already_started.add(annotatorID)
	
				if annotatorID in annotators_exec:
					annotator_data = annotators_exec[annotatorID]
				else:
					annotator_data = {}

				#Saving votes from task-run
				if is_tie != completeTie:
					#Vote 1
					if photo1_name in annotator_data:
						photo_votes = annotator_data[photo1_name]
					else:
						photo_votes = {}
					if photo2_name in photo_votes:
						votes = photo_votes[photo2_name]
					else:
						votes = []
					votes.append(left)
					photo_votes[photo2_name] = votes
					annotator_data[photo1_name] = photo_votes
				
					#Vote 2
					if photo1_name in annotator_data:
						photo_votes = annotator_data[photo1_name]
					else:
						photo_votes = {}
					if photo3_name in photo_votes:
						votes = photo_votes[photo3_name]
					else:
						votes = []
					votes.append(left)
					photo_votes[photo3_name] = votes
					annotator_data[photo1_name] = photo_votes

					#Vote 3
					if photo1_name in annotator_data:
						photo_votes = annotator_data[photo1_name]
					else:
						photo_votes = {}
					if photo4_name in photo_votes:
						votes = photo_votes[photo4_name]
					else:
						votes = []
					votes.append(left)
					photo_votes[photo4_name] = votes
					annotator_data[photo1_name] = photo_votes

					#Vote 4
					if photo3_name in annotator_data:
						photo_votes = annotator_data[photo3_name]
					else:
						photo_votes = {}
					if photo2_name in photo_votes:
						votes = photo_votes[photo2_name]
					else:
						votes = []
					votes.append(left)
					photo_votes[photo2_name] = votes
					annotator_data[photo3_name] = photo_votes

					#Vote 5
					if photo4_name in annotator_data:
						photo_votes = annotator_data[photo4_name]
					else:
						photo_votes = {}
					if photo2_name in photo_votes:
						votes = photo_votes[photo2_name]
					else:
						votes = []
					votes.append(left)
					photo_votes[photo2_name] = votes
					annotator_data[photo4_name] = photo_votes

					#Vote 6
					if photo4_name in annotator_data:
						photo_votes = annotator_data[photo4_name]
					else:
						photo_votes = {}
					if photo3_name in photo_votes:
						votes = photo_votes[photo3_name]
					else:
						votes = []
					votes.append(completeTie)
					photo_votes[photo3_name] = votes
					annotator_data[photo4_name] = photo_votes

				else:
					#Vote 1
					if photo1_name in annotator_data:
						photo_votes = annotator_data[photo1_name]
					else:
						photo_votes = {}
					if photo2_name in photo_votes:
						votes = photo_votes[photo2_name]
					else:
						votes = []
					votes.append(completeTie)
					photo_votes[photo2_name] = votes
					annotator_data[photo1_name] = photo_votes

					#Vote 2
					if photo1_name in annotator_data:
						photo_votes = annotator_data[photo1_name]
					else:
						photo_votes = {}
					if photo3_name in photo_votes:
						votes = photo_votes[photo3_name]
					else:
						votes = []
					votes.append(completeTie)
					photo_votes[photo3_name] = votes
					annotator_data[photo1_name] = photo_votes

					#Vote 3
					if photo1_name in annotator_data:
						photo_votes = annotator_data[photo1_name]
					else:
						photo_votes = {}
					if photo4_name in photo_votes:
						votes = photo_votes[photo4_name]
					else:
						votes = []
					votes.append(completeTie)
					photo_votes[photo4_name] = votes
					annotator_data[photo1_name] = photo_votes

					#Vote 4
					if photo2_name in annotator_data:
						photo_votes = annotator_data[photo2_name]
					else:
						photo_votes = {}
					if photo3_name in photo_votes:
						votes = photo_votes[photo3_name]
					else:
						votes = []
					votes.append(completeTie)
					photo_votes[photo3_name] = votes
					annotator_data[photo2_name] = photo_votes

					#Vote 5
					if photo2_name in annotator_data:
						photo_votes = annotator_data[photo2_name]
					else:
						photo_votes = {}
					if photo4_name in photo_votes:
						votes = photo_votes[photo4_name]
					else:
						votes = []
					votes.append(completeTie)
					photo_votes[photo4_name] = votes
					annotator_data[photo2_name] = photo_votes

					#Vote 6
					if photo3_name in annotator_data:
						photo_votes = annotator_data[photo3_name]
					else:
						photo_votes = {}
					if photo4_name in photo_votes:
						votes = photo_votes[photo4_name]
					else:
						votes = []
					votes.append(completeTie)
					photo_votes[photo3_name] = votes
					annotator_data[photo4_name] = photo_votes

				annotators_exec[annotatorID] = 	annotator_data

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

			if "agrad" in question:
				question = possibleQuestions[0]
			else:
				question = possibleQuestions[1]

			if current_question == question:
				if annotatorID not in annotators_already_started:#Suppose annotator start with photo1 and photo2
					#Simulating that these first two photos were recommended
					photo1 = items_map[photo1_name]
					photo2 = items_map[photo2_name]
					annotator.update_next(photo1)
					annotator.prev = annotator.next
					annotator.update_next(photo2)

					annotators_already_started.add(annotatorID)

				if annotatorID in annotators_exec:
					annotator_data = annotators_exec[annotatorID]
				else:
					annotator_data = {}

				#Saving votes from task-run
				if answer == left:
					if photo1_name in annotator_data:
						photo_votes = annotator_data[photo1_name]
					else:
						photo_votes = {}
					if photo2_name in photo_votes:
						votes = photo_votes[photo2_name]
					else:
						votes = []
					votes.append(left)
					photo_votes[photo2_name] = votes
					annotator_data[photo1_name] = photo_votes	
				elif answer == right:
					if photo2_name in annotator_data:
						photo_votes = annotator_data[photo2_name]
					else:
						photo_votes = {}
					if photo1_name in photo_votes:
						votes = photo_votes[photo1_name]
					else:
						votes = []
					votes.append(left)
					photo_votes[photo1_name] = votes
					annotator_data[photo2_name] = photo_votes
				elif answer == notKnown:
					if photo1_name in annotator_data:
						photo_votes = annotator_data[photo1_name]
					else:
						photo_votes = {}
					if photo2_name in photo_votes:
						votes = photo_votes[photo2_name]
					else:
						votes = []
					votes.append(completeTie)
					photo_votes[photo2_name] = votes
					annotator_data[photo1_name] = photo_votes

				annotators_exec[annotatorID] = 	annotator_data

	#For each annotator simulate execution and recommendation of tasks
	success_comp = 0
	failed_comp = 0
	for annotatorID in annotators.keys():

		#Computing amount of comparisons performed by annotator
		total_counter = count_comparisons(annotators_exec[annotatorID])
		current_counter = 0
		continue_votes = True

		annotator = annotators[annotatorID]
	
		while current_counter < total_counter and continue_votes:
			photo1 = annotator.prev
			photo2 = annotator.next

			exec_data = annotators_exec[annotatorID]
			winner = None
			looser = None
			tie = False
			if photo1.name in exec_data.keys():
				photo_data = exec_data[photo1.name]
				if photo2.name in photo_data.keys():
					photo_vote = random.choice(photo_data[photo2.name])
					if photo_vote == left:
						winner = photo1
						looser = photo2
					elif photo_vote == right:
						winner = photo2
						looser = photo1
					else:
						tie = True
			elif photo2.name in exec_data.keys():
				photo_data = exec_data[photo2.name]
				if photo1.name in photo_data.keys():
					photo_vote = random.choice(photo_data[photo1.name])
					if photo_vote == left:
						winner = photo2
						looser = photo1
					elif photo_vote == right:
						winner = photo1
						looser = photo2
					else:
						tie = True	
			#Check if comparison occurred - account for comparisons that did not occurred
			if winner == None and looser == None and tie == False:
				failed_comp = failed_comp + 1
				print (">>> Failed\t"+photo1.name+"\t"+photo2.name)
			else:
				#Compute vote
				decision = Decision(annotator, winner=winner, loser=looser)
				if winner != None and winner.name == annotator.next.name:
					perform_vote(annotator, next_won=True)
				elif winner != None and winner.name == annotator.prev.name:
					perform_vote(annotator, next_won=False)
				else:
					annotator.ignore.append(annotator.prev)
					annotator.ignore.append(annotator.next)

				annotator.next.viewed.append(annotator)
				annotator.prev = annotator.next
				annotator.ignore.append(annotator.prev)
				success_comp = success_comp + 1

				#Select new next photo and iterate until n comparisons for annotator
				next_image = choose_image(annotator, items_map, annotators)
				if next_image == None or next_image == "":
					continue_votes = False
				else:
					annotator.update_next(next_image)
				

	#Output file
	output = open(output_filename, 'w')
	output.write(success_comp+"\t"+failed_comp+"\t"+(success_comp+failed_comp)+"\t"+success_comp/(success_comp+failed_comp)+"\n")
	for item_name, item in items_map.items():
		output.write(current_question+ "\t" + item_name+ "\t" + str(item.mu) + "\t" + str(item.sigma_sq)+'\n')
	output.close()

def count_comparisons(annotator_data):
	counter = 0
	for image in annotator_data.keys():
		image_data = annotator_data[image]
		for other_image in image_data.keys():
			votes = image_data[other_image]
			counter += len(votes)
	return counter

def preferred_items(annotator, items_map, annotators):
	'''
	Return a list of preferred items for the given annotator to look at next.

	This method uses a variety of strategies to try to select good candidate
	projects.
	'''
	items = []
	ignored_ids = {i.name for i in annotator.ignore}

	if ignored_ids:
		available_items = {item for item in items_map.values if item.name not in ignored_ids}
	else:
		available_items = {item for item in items_map.values}

	prioritized_items = [i for i in available_items if i.prioritized]

	items = prioritized_items if prioritized_items else available_items

	#annotators = Annotator.query.filter(
	#    (Annotator.active == True) & (Annotator.next != None) & (Annotator.updated != None)
	#).all()
	busy = {i.next.id for i in annotators.values() if \
	(datetime.utcnow() - i.updated).total_seconds() < settings.TIMEOUT * 60}
	nonbusy = [i for i in items if i.id not in busy]
	preferred = nonbusy if nonbusy else items

	less_seen = [i for i in preferred if len(i.viewed) < settings.MIN_VIEWS]

	return less_seen if less_seen else preferred

def choose_image(annotator, items_map):
	pref_items = preferred_items(annotator, items_map)

	shuffle(pref_items) # useful for argmax case as well in the case of ties
	if pref_items:
		if random() < crowd_bt.EPSILON:
		    return pref_items[0]
		else:
		    return crowd_bt.argmax(lambda i: crowd_bt.expected_information_gain(
			annotator.alpha,
			annotator.beta,
			annotator.prev.mu,
			annotator.prev.sigma_sq,
			i.mu,
			i.sigma_sq), pref_items)
	else:
		return None



if __name__ == '__main__':

	if len(sys.argv) < 4:
		print("Uso: <arquivo com execuções das tarefas> <tasks definition -V2> <simulation or ranking>")
		sys.exit(1)

	dataFile = open(sys.argv[1], 'r')
	tasksFile = open(sys.argv[2], 'r')
	mode = sys.argv[3]

	lines = dataFile.readlines()
	linesTasks = tasksFile.readlines()
	tasks_def = readTasksDefinitions(linesTasks)

	if mode.lower() == "ranking":
		evaluateAllVotes(lines, "allPairwiseComparison.dat", tasks_def)
	elif mode.lower() == "simulation":
		simulateCrowdBT(lines, "allPairwiseComparison-sim-agrad.dat", tasks_def, possibleQuestions[0])
		simulateCrowdBT(lines, "allPairwiseComparison-sim-seg.dat", tasks_def, possibleQuestions[1])

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
