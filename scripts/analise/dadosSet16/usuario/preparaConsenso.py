import sys
from sets import Set

def parseUserData(lines, filterLines, outputFileNameAgra, outputFileNameSeg):
	""" Reading user data """
	
	usersTasksMatrixAgra = {}
	usersTasksMatrixSeg = {}
	allTasksAgra = Set([])
	allTasksSeg = Set([])

	for line in lines:
		data = line.split("|")
		userID = int(data[0])
		tasksIDAgra = eval(data[2])
		tasksIDSeg = eval(data[3])
		tasksAnswerAgra = eval(data[4])
		tasksAnswerSeg = eval(data[5])
			
		allTasksAgra.update(tasksIDAgra)
		allTasksSeg.update(tasksIDSeg)
		
		#Agra
		if userID in usersTasksMatrixAgra.keys():
			tasksInfo = usersTasksMatrixAgra[userID]
		else:
			tasksInfo = {}
		if (len(filterLines) > 0 and str(userID)+"\n" in filterLines) or (len(filterLines) == 0):
			for i in range(0, len(tasksIDAgra)):
				tasksInfo[tasksIDAgra[i]] = tasksAnswerAgra[i]
			usersTasksMatrixAgra[userID] = tasksInfo

		#Seg
		if userID in usersTasksMatrixSeg.keys():
			tasksInfo = usersTasksMatrixSeg[userID]
		else:
			tasksInfo = {}
		if (len(filterLines) > 0 and str(userID)+"\n" in filterLines) or (len(filterLines) == 0):
			for i in range(0, len(tasksIDSeg)):
				tasksInfo[tasksIDSeg[i]] = tasksAnswerSeg[i]
			usersTasksMatrixSeg[userID] = tasksInfo

	#Iterating through users and tasks in ascending order of IDs. Tasks Agradable
	currentTasks = list(allTasksAgra)
	currentTasks.sort()
	outputFile = open(outputFileNameAgra, 'w')	

	outputFile.write("userID\t")
	for task in currentTasks:
		outputFile.write(task+"\t")
	outputFile.write("\n")
	
	for userID in usersTasksMatrixAgra.keys():
		outputFile.write(str(userID)+"\t")
		for task in currentTasks:
			if not task in usersTasksMatrixAgra[userID].keys():
				outputFile.write("NA\t")
			else:
				value = usersTasksMatrixAgra[userID][task]
				if value == 'NotKnown':
					outputFile.write(str("NotKnown")+"\t")				
				elif value == 'Left':
					outputFile.write(str("Left")+"\t")				
				elif value == 'Right':
					outputFile.write(str("Right")+"\t")
		outputFile.write("\n")
	outputFile.close()
	
	#Iterating through users and tasks in ascending order of IDs. Tasks Secure
	currentTasks = list(allTasksSeg)
	currentTasks.sort()
	outputFile = open(outputFileNameSeg, 'w')	

	outputFile.write("userID\t")
	for task in currentTasks:
		outputFile.write(task+"\t")
	outputFile.write("\n")
	
	for userID in usersTasksMatrixSeg.keys():
		outputFile.write(str(userID)+"\t")
		for task in currentTasks:
			if not task in usersTasksMatrixSeg[userID].keys():
				outputFile.write("NA\t")
			else:
				value = usersTasksMatrixSeg[userID][task]
				if value == 'NotKnown':
					outputFile.write(str("NotKnown")+"\t")				
				elif value == 'Left':
					outputFile.write(str("Left")+"\t")				
				elif value == 'Right':
					outputFile.write(str("Right")+"\t")
		outputFile.write("\n")
	outputFile.close()

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Uso: <arquivo com ids, tarefas e perfis dos usuarios> <usuarios a filtrar>"
		sys.exit(1)
	dataFile = open(sys.argv[1], 'r')
	lines = dataFile.readlines()
	dataFile.close()

	if len(sys.argv) > 2:
		filterFile = open(sys.argv[2], 'r')
		filterLines = filterFile.readlines()
		filterFile.close()

		if len(sys.argv) > 3:
			filterFile2 = open(sys.argv[3], 'r')
			filterLines2 = filterFile2.readlines()
			filterFile2.close()

			filterLines.extend(filterLines2[1:])
	else:
		filterLines = []

	usersTasks = parseUserData(lines, filterLines[1:], "consenseMatrixAgra.dat", "consenseMatrixSeg.dat")

