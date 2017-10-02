# coding=utf-8
# Separates tasks execution according to a group of users

import sys
import pandas as pd

def selectTasks(lines, criteria):
	""" Selecting tasks according to user ids defined in criteria """

	for line in lines:#Reading from pybossa task-run CSV
		lineData = line.split("+")
		
		currentUserID = lineData[4]
		if currentUserID+"\n" in criteria:
			print line.strip()

def selectTasksToRemove(lines, criteria):
	""" Removing tasks according to user ids defined in criteria """

	for line in lines:#Reading from pybossa task-run CSV
		lineData = line.split("+")
		
		currentUserID = lineData[4]
		if not currentUserID+"\n" in criteria:
			print line.strip()


def selectTasksFromClassifierPredictions(predFile, criteria):
	data = pd.read_table(predFile, sep='\s+', encoding='utf8', header=0) 
	all_data = None
	for userID in criteria:
		id = userID.strip(' \t\n\r"')
		userData = data[(data.userID == int(id))]
		if all_data is None:
			all_data = userData
		else:
			all_data = all_data.append(userData)

	all_data.to_csv("run_pred_user.dat", sep = "\t")
		

if __name__ == "__main__":

	#print sys.argv

	if len(sys.argv) < 3:
		print "Uso: <arquivo com execuções das tarefas> <arquivos com usuarios a filtrar> <type: run, classifier or remove>"
		sys.exit(1)

	if len(sys.argv) >= 4:
		typeOfExecution = sys.argv[len(sys.argv)-1]
	else:
		typeOfExecution = ""

	#print typeOfExecution

	dataFile = open(sys.argv[1], 'r')
	lines = dataFile.readlines()

	if typeOfExecution.lower() == "remove":
		usersFile = open(sys.argv[2], 'r')
		criteria = usersFile.readlines()[1:]#skipping first line containing tasks id of intersection
		#print criteria

		if sys.argv[3] != "remove":
			usersFile = open(sys.argv[3], 'r')
			criteria.extend(usersFile.readlines()[1:])
	else:
		usersFile = open(sys.argv[2], 'r')
		criteria = usersFile.readlines()[1:]#skipping first line containing tasks id of intersection

	#print criteria
	#sys.exit(1)

	if len(typeOfExecution) == 0 or typeOfExecution == "run":
		selectTasks(lines, criteria)#FIXME: add tasksID
	elif typeOfExecution == "remove":
		selectTasksToRemove(lines, criteria)
	else:
		selectTasksFromClassifierPredictions(sys.argv[1], criteria)

	dataFile.close()
	usersFile.close()

