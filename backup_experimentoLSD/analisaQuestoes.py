import sys

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Uso: <arquivo com dados> <id da questao a considerar>"
		sys.exit(1)

	inputFile = open(sys.argv[1], 'r')
	questionToConsider = sys.argv[2]	

	dataLines = inputFile.readlines()

	results = {}
	counter = {}
	totalComparisons = 0
	for line in dataLines:
		data = line.split("\t")
		
		question = data[1]
		if question == questionToConsider:
			answer = data[2]
			photo1 = data[3].split("/")[4].replace("\"", "").strip()
			photo2 = data[4].split("/")[4].replace("\"", "").strip()
		
			if not counter.has_key(photo1):
				counter[photo1] = 0
			if not counter.has_key(photo2):
				counter[photo2] = 0
		
			if answer == 'Left':
				if not results.has_key(photo1):
					results[photo1] = []		
				results[photo1].append(photo2)			
			elif answer == 'Right':
				if not results.has_key(photo2):
					results[photo2] = []
				results[photo2].append(photo1)

			counter[photo1] = counter[photo1] + 1
			counter[photo2] = counter[photo2] + 1
			totalComparisons = totalComparisons + 1

	print "Total de Comparacoes", totalComparisons
	for key in results:
		#print key, " ", len(results[key]), " ", counter[key], " ", results[key]
		print key, " ", len(results[key]), " ", counter[key], " "
