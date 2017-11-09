# coding=utf-8
# A partir de uma lista de fotos de tamanho X (sem template par a par!) gera uma proposta de tarefas no formato MaxDiff de tamanho Y

import sys
import random
from sets import Set

#possible questions
possibleQuestions = ["agrad%C3%A1vel?", "seguro?"]
task_size = 4
photo_threshold = 13

def buildMaxDiff(photos_filename, user_question, output_filename):

	photos_file = open(photos_filename, "r")
	lines = photos_file.readlines()
	photos_file.close()

	output_file = open(output_filename, "w")

	allPhotos = set([])
	photo_count = {}

	if "agrad" in user_question:
		question = possibleQuestions[0]
	else:
		question = possibleQuestions[1]

	#Reading all photos
	for line in lines:
		photo = line.strip(' \t\n\r"')
		allPhotos.add(photo)
		photo_count[photo] = 0

	allPhotos_bkp = allPhotos.copy()

	#Building MaxDiff design with task_size photos per task
	all_tasks = []
	while len(allPhotos) > 0:
		currentPhotos = []

		photos = []
		#If there are less photos than task_size, add all remaining and repeat others!
		while len(photos) < task_size and set(photos) in all_tasks:
			photos = []
			if len(allPhotos) <= task_size:
				photos.extend(allPhotos)
				for i in range(0, task_size - len(photos)):#Retrieve remaining from bkp
					photo = random.sample(allPhotos_bkp, 1)[0]
					while photo in photos or photo in currentPhotos:
						photo = random.sample(allPhotos_bkp, 1)[0]
					photos.append(photo)
			#Otherwise, randomize task_size photos
			else:
				photos = random.sample( allPhotos, task_size )

		#Updating photos counters
		for photo in photos:
			if photo_count.has_key(photo):
				counter = photo_count.get(photo)
			else:
				print ">>> Error, photo not found! " + photo
				sys.exit(1)
			#if len(allPhotos) <= task_size:
			#	currentPhotos.append(photo)
			#	photo_count[photo] = photo_count[photo]+1
			#elif counter < photo_threshold:
			#	currentPhotos.append(photo)
			#	photo_count[photo] = photo_count[photo]+1
			currentPhotos.append(photo)
			photo_count[photo] = photo_count[photo]+1

		#Building current task
		all_tasks.append(set(currentPhotos))

		output_file.write(question)
		for i in range(0, len(currentPhotos)):
			output_file.write("\t" + currentPhotos[i])
		output_file.write("\n")
		
		#Checking if each photo reached threshold comparisons
		for photo in currentPhotos:
			if photo_count[photo] >= photo_threshold and photo in allPhotos:
				allPhotos.remove(photo)


	#Logging
	for photo in allPhotos:
		output_file.write("All photos remained with: " + photo + "\n")

	for photo in photo_count.keys():
		output_file.write("Counter for " + photo + "\t" + str(photo_count[photo])+"\n")
	output_file.close()	

def addMaxDiff(photos_filename, user_question, amount_new_photos, output_filename, new_output_filename, old_input_file):
	allPhotos = buildMaxDiff(photos_filename, user_question, output_filename)

	output_file = open(output_filename, "r")
	output_lines = output_file.readlines()
	output_file.close()

	photos_file = open(photos_filename, "r")
	input_lines = photos_file.readlines()
	photos_file.close()

	old_photos_file = open(old_input_file, "r")
	old_input_lines = old_photos_file.readlines()
	old_photos_file.close()

	#All photos from input file and selecting new photos
	allPhotos = []
	for line in input_lines:
		allPhotos.append(line.strip(' \t\n\r"'))
	new_photos = allPhotos[-amount_new_photos:]

	#All photos from previous list
	old_photos = set([])
	for line in old_input_lines:
		old_photos.add(line.strip(' \t\n\r"'))

	new_output_file = open(new_output_filename, "w")
	
	#Selecting new photos which tasks should be added and searching for tasks with them
	new_tasks = set([])
	for line in output_lines:
		for new_photo in new_photos:
			if new_photo in line:
				new_tasks.add(line.strip(' \t\n\r"')) 
				continue

	for task in new_tasks:
		if not "Counter" in task:
			task_data = task.split('\t')
			for index in range(1, len(task_data)):
				photo_data = task_data[index]
				if "foto_" in photo_data:
					old_photo = random.sample(old_photos, 1)[0]
					while old_photo in task_data:
						old_photo = random.sample(old_photos, 1)[0]
					task_data[index] = old_photo
			print str(task_data)
			new_output_file.write(task_data[0]+"\t"+task_data[1]+"\t"+task_data[2]+"\t"+task_data[3]+"\t"+task_data[4]+"\n")
		else:
			new_output_file.write(task+"\n")
	new_output_file.close()

	#Checking generated tasks
	new_output_file = open(new_output_filename, "r")
	for line in new_output_file.readlines():
		if (not "Cristina" in line) and (not "Floriano" in line):
			print ">>>>> ERROR! LINE " + str(line.strip(' \t\n\r"'))
		else:
			print ">>> LINE OK"
	

if __name__ == "__main__":
	if len(sys.argv) < 5:
		print "Uso: <arquivo com lista de fotos> <questao> <arquivo de saída> <adiciona ou novo> <amount of new lines> <arquivo de saída add> <arquivo com lista antiga>"
		sys.exit(1)

	output_filename = sys.argv[3]
	action = sys.argv[4]
	if action.lower() == "adiciona":
		amount = int(sys.argv[5])
		new_output_filename = sys.argv[6]
		old_input_file = sys.argv[7]
		addMaxDiff(sys.argv[1], sys.argv[2], amount, output_filename, new_output_filename, old_input_file)
	elif action.lower() == "novo":
		buildMaxDiff(sys.argv[1], sys.argv[2], output_filename)
	else:
		print ">>>> Error! Action not recognized, it must be <adiciona> or <novo> but you gave " + str(action)
		sys.exit(1) 
