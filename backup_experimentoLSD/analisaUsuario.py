import sys

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Uso: <arquivo com dados> <arquivo com ids de usuarios a considerar>"
		sys.exit(1)

	dataInput = open(sys.argv[1], 'r')
	users = open(sys.argv[2], 'r')
	
	dataLines = dataInput.readlines()
	dataUsers = users.readlines()

	usersIDs = []
	for userID in dataUsers:
		usersIDs.append(userID.strip())

	results = {}
	counter = {}
	totalComparisons = 0
	for line in dataLines:
		data = line.split("\t")
		
		userID = data[0]
		if not userID in usersIDs:
			continue
		
		question = data[1]		
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
