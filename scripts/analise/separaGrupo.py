import sys
from sets import Set

def parseUserData(lines):
	""" Reading user data """
	fem = Set([])
	femTasks = Set([])
	masc = Set([])
	mascTasks = Set([])

	solt = Set([])
	soltTasks = Set([])
	casa = Set([])
	casaTasks = Set([])

	for line in lines:
		data = line.split("|")
		userID = int(data[0])
		profile = data[1].split("+")
		
		tasksIDAgra = eval(data[2])
		tasksIDSeg = eval(data[3])

		if len(data[1]) > 0:
			#Separating by sex
			#print str(profile)+"\t"+str(len(data[1]))
			if profile[1].lower()[0] == 'f':
				#fTasksAgra.update(tasksIDAgra)
				#fTasksSeg.update(tasksIDSeg)
				fem.add(userID)
				femTasks.update(tasksIDAgra)
				femTasks.update(tasksIDSeg)
			else:
				#mTasksAgra.update(tasksIDAgra)
				#mTasksSeg.update(tasksIDSeg)
				masc.add(userID)
				mascTasks.update(tasksIDAgra)
				mascTasks.update(tasksIDSeg)
		
			#Separating by relationship
			if profile[6].lower()[0] == 's':
				#sTasksAgra.update(tasksIDAgra)
				#sTasksSeg.update(tasksIDSeg)
				solt.add(userID)
				soltTasks.update(tasksIDAgra)
				soltTasks.update(tasksIDSeg)
			elif profile[6].lower()[0] == 'c':
				#cTasksAgra.update(tasksIDAgra)
				#cTasksSeg.update(tasksIDSeg)
				casa.add(userID)
				casaTasks.update(tasksIDAgra)
				casaTasks.update(tasksIDSeg)
	
	#Intersection between married and single users tasks
	soltCasaTasks = soltTasks.intersection(casaTasks)
	soltFile = open("solteiro.dat", "w")
	soltFile.write(str(list(soltCasaTasks))+"\n")
	for userID in solt:
		soltFile.write(str(userID)+"\n")#FIXME: add tasksID
	soltFile.close()
	casaFile = open("casado.dat", "w")
	casaFile.write(str(list(soltCasaTasks))+"\n")
	for userID in casa:
		casaFile.write(str(userID)+"\n")
	casaFile.close()

	#Intersection between women and men users tasks
	femMascTasks = femTasks.intersection(mascTasks)
	femFile = open("feminino.dat", "w")
	femFile.write(str(list(femMascTasks))+"\n")
	for userID in fem:
		femFile.write(str(userID)+"\n")
	femFile.close()
	masFile = open("masculino.dat", "w")
	masFile.write(str(list(femMascTasks))+"\n")
	for userID in masc:
		masFile.write(str(userID)+"\n")
	masFile.close()

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Uso: <arquivo com ids, tarefas e perfis dos usuarios>"
		sys.exit(1)
	dataFile = open(sys.argv[1], 'r')
	lines = dataFile.readlines()
	dataFile.close()

	usersTasks = parseUserData(lines)

