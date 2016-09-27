import sys
import csv
from sets import Set

def parseFeaturesData(lines, group):
	""" Reading features data """

	if group == "g1":
		questions = ["question1", "question2__left_side", "question2__right_side", "question3"]
	elif group == "g2":
		questions = ["question1", "question2__left_side", "question2__right_side", "question3"]
	elif group == "g3":
		questions = ["question1__left_side", "question1__right_side", "question2__left_side", "question2__right_side", "question3__left_side", "question3__right_side"]
	elif group == "g4":
		questions = ["question1", "question2"]
	elif group == "g5":
		questions = ["question1", "your_answer_is"]
	elif group == "g6":
		questions = ["question1__left_side", "question1__right_side", "question2__left_side", "question2__right_side"]
	elif group == "g7":
		questions = ["question1", "question2", "question3__left_side", "question3__right_side"]
	elif group == "g8":
		questions = ["question1", "question2__left_side", "question2_right_side", "question3__left_side", "question3_right_side"]
	elif group == "g9":
		questions = ["question1__left_side", "question1__right_side"]
	elif group == "g10":
		questions = ["question1", "question2", "question3"]
	elif group == "g11":
		questions = ["question2__left_side", "question2__right_side", "question3__left_side", "question3__right_side"]
	elif group == "g12":
		questions = ["question1", "question2__left_side", "question2__right_side", "question3"]
	elif group == "g13":
		questions = ["question1__left_side", "question1__right_side", "question2__left_side", "question2__right_side"]

	featuresMatrix = {}
	allImages = Set([])

	usersTasksMatrixSeg = {}
	allTasksSeg = Set([])
	i = 0

	for line in lines:

		if i == 0:
			headers = line
			indexes = []
			questions.insert(0, "image_url")
			for quest in questions:
				indexes.append(headers.index(quest))
		else:
			data = line
			workerID = int(data[9])
			image_data = data[indexes[0]].split("/")
			if len(image_data) > 1:
				image_url = image_data[5]+"/"+image_data[6]
				answers = []

				for index in indexes[1:]:
					if len(data[index]) == 0:
						answers.append("NA")
					else:
						answers.append(data[index])

				allImages.add(image_url)
		
				#Checking if worker data already exists
				if workerID in featuresMatrix.keys():
					tasksInfo = featuresMatrix[workerID]
				else:
					tasksInfo = {}

				tasksInfo[image_url] = answers
				featuresMatrix[workerID] = tasksInfo

		i = i+1

	#Iterating through images in ascending order
	currentImages = list(allImages)
	currentImages.sort()

	for index in range(1, len(questions)):
		outputFile = open(group+"_"+questions[index]+".dat", 'w')	
		outputFile.write("workerID\t")

		print questions

		for index2 in range(0, len(currentImages)):
			outputFile.write("im"+str(index2)+"\t")
		outputFile.write("\n")
	
		for workerID in featuresMatrix.keys():
			outputFile.write(str(workerID)+"\t")
			for image in currentImages:
				if not image in featuresMatrix[workerID].keys():
					outputFile.write("NA\t")
				else:
					value = featuresMatrix[workerID][image]
					print value
					outputFile.write(str(value[index-1])+"\t")				
			outputFile.write("\n")
		outputFile.close()
	
if __name__ == "__main__":
	if len(sys.argv) < 3:
		print "Uso: <crowdflower file> <group>"
		sys.exit(1)

	dataFile = csv.reader(open(sys.argv[1], 'r'))
	group = sys.argv[2]	

	usersTasks = parseFeaturesData(dataFile, group)

