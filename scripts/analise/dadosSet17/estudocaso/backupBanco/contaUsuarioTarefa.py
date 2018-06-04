# coding=utf-8
#Script to estimate user contributions per image
import sys
import time as tm
import datetime
from sets import Set
import json
import numpy as np
from collections import Counter

def readUserData(lines, tasks_def, output_filename):
	""" Reading user profile """
	
	users_best_counter = {}
	users_worst_counter = {}
	agrad_dic = {"agradavel?" : "agrad%C3%A1vel?", "agrad%C3%A1vel?" : "agradavel?"}

	#Reading from pybossa task-run CSV and tasks definitions in order to count users contributions per image
	for line in lines:
		data = line.split("+")

		task_id = data[3]
		user_id = data[4]
		user_answer = data[9].strip(' \t\n\r"')

		answer_data = json.loads(user_answer)
		photo_most = answer_data['theMost'].strip(' \t\n\r"')
		photo_less = answer_data['theLess'].strip(' \t\n\r"')	

		task_def = tasks_def[task_id]

		if user_id in users_best_counter.keys():
			best_counters = users_best_counter[user_id]
			wost_counters = users_worst_counter[user_id]
		else:
			best_counters = {}
			worst_counters = {}

		photos_selected = [photo_most, photo_less]

		#Persisting user contributions as best and worst images
		if photo_most != "equal" and photo_less != "equal" and len(photo_most) > 0 and len(photo_less) > 0:
			for index in range(0, 2):
				if index == 0:
					user_counters = best_counters
				else:
					user_counters = worst_counters

				image = photos_selected[index]
				if image in user_counters:
					image_counter = user_counters[image]
				else:
					image_counter = 0

				image_counter = image_counter + 1
				user_counters[image] = image_counter	

		#Persisting user contributions for all evaluated images
		#for key in ['url_a', 'url_b', 'url_c', 'url_d']:
		#	image = task_def[key]
		#	if image in user_counters:
		#		image_counter = user_counters[image]
		#	else:
		#		image_counter = 0
#
#			image_counter = image_counter + 1
#			user_counters[image] = image_counter

		users_best_counter[user_id] = best_counters
		users_worst_counter[user_id] = worst_counters

	output_file = open(output_filename, "w")
	all_values = []
	for user_id in users_best_counter.keys():
		user_counters = users_best_counter[user_id]
		for image in user_counters.keys():
			counter = user_counters[image]
			output_file.write(str(user_id)+"\tbest\t"+str(image.encode("utf8"))+"\t"+str(counter)+"\n")
			all_values.append(counter)
	output_file.write(str(Counter(all_values))+"\n")

	all_values = []
	for user_id in users_worst_counter.keys():
		user_counters = users_worst_counter[user_id]
		for image in user_counters.keys():
			counter = user_counters[image]
			output_file.write(str(user_id)+"\tworst\t"+str(image.encode("utf8"))+"\t"+str(counter)+"\n")
			all_values.append(counter)

	output_file.write(str(Counter(all_values))+"\n")
	output_file.close()




def readTasksDefinitions(linesTasks):
	tasksDef = {}

	for line in linesTasks:
		data = line.split("+")	
		#print data
		taskID = data[0].strip(' \t\n\r')
		currentDef = json.loads(data[7].strip(' \t\n\r\"'))

		tasksDef[taskID] = currentDef
	
	return tasksDef

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print "Uso: <arquivo com execucoes das tarefas e perfis dos usuarios - V2> <arquivo com definicoes das tarefas>"
		sys.exit(1)

	data_file1 = open(sys.argv[1], 'r')
	data_file2 = open(sys.argv[2], 'r')
	
	lines_task_run = data_file1.readlines()
	lines_tasks_def = data_file2.readlines()
	
	tasks_def = readTasksDefinitions(lines_tasks_def)

	usersTasks = readUserData(lines_task_run, tasks_def, "users-tasks.dat")
	data_file1.close()
	data_file2.close()
