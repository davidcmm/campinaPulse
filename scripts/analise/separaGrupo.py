import sys
from sets import Set

def parseUserData(lines):
	""" Reading user data """
	fAgra = Set([])
	fSeg = Set([])
	mAgra = Set([])
	mSeg = Set([])

	sAgra = Set([])
	sSeg = Set([])
	cAgra = Set([])
	cSeg = Set([])

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
				fAgra.add(userID)
				fSeg.add(userID)
			else:
				#mTasksAgra.update(tasksIDAgra)
				#mTasksSeg.update(tasksIDSeg)
				mAgra.add(userID)
				mSeg.add(userID)
		
			#Separating by relationship
			if profile[6].lower()[0] == 's':
				#sTasksAgra.update(tasksIDAgra)
				#sTasksSeg.update(tasksIDSeg)
				sAgra.add(userID)
				sSeg.add(userID)
			elif profile[6].lower()[0] == 'c':
				#cTasksAgra.update(tasksIDAgra)
				#cTasksSeg.update(tasksIDSeg)
				cAgra.add(userID)
				cSeg.add(userID)

	#print("F x m\t" + str(list(fTasksAgra.intersection(mTasksAgra)))+"\t"+str(list(fTasksSeg.intersection(mTasksSeg)))+"\n")
	#print("S x c\t" + str(list(sTasksAgra.intersection(cTasksAgra)))+"\t"+str(list(sTasksSeg.intersection(cTasksSeg)))+"\n")
	solteiros = open("solteiro.dat", "w")
	for userID in sAgra:
		solteiros.write(str(userID)+"\n")#FIXME: add tasksID
	solteiros.close()
	casados = open("casado.dat", "w")
	for userID in cAgra:
		casados.write(str(userID)+"\n")
	casados.close()
	fem = open("feminino.dat", "w")
	for userID in fAgra:
		fem.write(str(userID)+"\n")
	fem.close()
	mas = open("masculino.dat", "w")
	for userID in mAgra:
		mas.write(str(userID)+"\n")
	mas.close()

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Uso: <arquivo com ids, tarefas e perfis dos usuarios>"
		sys.exit(1)
	dataFile = open(sys.argv[1], 'r')
	lines = dataFile.readlines()
	dataFile.close()

	usersTasks = parseUserData(lines)

