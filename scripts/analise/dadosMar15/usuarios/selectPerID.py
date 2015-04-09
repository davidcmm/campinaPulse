# coding=utf-8
# Separates tasks execution according to a group of users

import sys

def selectTasks(lines, criteria):
	""" Selecting tasks according to user ids defined in criteria """

	for line in lines:#Reading from pybossa task-run CSV
		lineData = line.split("+")
		
		currentUserID = lineData[4]
		if currentUserID+"\n" in criteria:
			print line.strip()

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print "Uso: <arquivo com execuções das tarefas> <arquivos com usuarios a filtrar>"
		sys.exit(1)
	dataFile = open(sys.argv[1], 'r')
	lines = dataFile.readlines()

	usersFile = open(sys.argv[2], 'r')
	criteria = usersFile.readlines()

	selectTasks(lines, criteria)#FIXME: add tasksID
	dataFile.close()
	usersFile.close()
