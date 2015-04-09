# Uses users profile information in order to separate users in groups according to social aspects

import sys
from sets import Set

def parseUserData(lines):
	""" Reading user data """
	socialClasses = ["Baixa (at\u00e9 R$ 1.449,99)", "M\u00e9dia Baixa (R$ 1.450 a R$ 2.899,99)", "M\u00e9dia (R$ 2.900 a R$ 7.249,99)", "M\u00e9dia Alta (R$ 7.250 a R$ 14.499,99)", "Alta (R$ 14.500 ou mais)"]

	jovem = Set([]) 
	jovemTasks = Set([]) 
	adulto = Set([]) 
	adultoTasks = Set([]) 	

	baixa = Set([]) 
	baixaTasks = Set([])
	media = Set([])
	mediaTasks = Set([])
 
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
			#Separating by class
			print profile[2]
			if socialClasses[0] in profile[2] or socialClasses[1] in profile[2]:
				baixa.add(userID)
				baixaTasks.update(tasksIDAgra)
				baixaTasks.update(tasksIDSeg)
			elif socialClasses[2] in profile[2] or socialClasses[3] in profile[2]:
				media.add(userID)
				mediaTasks.update(tasksIDAgra)
				mediaTasks.update(tasksIDSeg)

			#Separating by age
			if int(profile[0]) <= 24:
				jovem.add(userID) 
				jovemTasks.update(tasksIDAgra)
				jovemTasks.update(tasksIDSeg)
			elif int(profile[0]) >= 35 and int(profile[0]) <= 54:
				adulto.add(userID) 
				adultoTasks.update(tasksIDAgra)
				adultoTasks.update(tasksIDSeg)

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
	
	
	#Intersection between young and adultolt tasks	
	jovemAdultoTasks = jovemTasks.intersection(adultoTasks)	
	jovemFile = open("jovem.dat", "w")
	jovemFile.write(str(list(jovemAdultoTasks))+"\n")
	for userID in jovem:
		jovemFile.write(str(userID)+"\n")#FIXME: add tasksID
	jovemFile.close()
	adultoFile = open("adulto.dat", "w")
	adultoFile.write(str(list(jovemAdultoTasks))+"\n")
	for userID in adulto:
		adultoFile.write(str(userID)+"\n")
	adultoFile.close()

	#Intersection between poor and medium classes	
	baixaMediaTasks = baixaTasks.intersection(mediaTasks)	
	baixaFile = open("baixa.dat", "w")
	baixaFile.write(str(list(baixaMediaTasks))+"\n")
	for userID in baixa:
		baixaFile.write(str(userID)+"\n")#FIXME: add tasksID
	baixaFile.close()
	mediaFile = open("media.dat", "w")
	mediaFile.write(str(list(baixaMediaTasks))+"\n")
	for userID in media:
		mediaFile.write(str(userID)+"\n")
	mediaFile.close()

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

