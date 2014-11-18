import sys

if __name__ == "__main__":
	if len(sys.argv) < 1:
		print "Uso: <arquivo com dados>"
		sys.exit(1)
	data = open(sys.argv[1], 'r')
	lines = data.readlines()

	results = {}
	counter = {}
	for line in lines:
		data = line.split(" ")
		
		answer = data[1]
		photo1 = data[2].split("/")[4].replace("\"", "").strip()
		photo2 = data[3].split("/")[4].replace("\"", "").strip()
		
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

	print "Total de Comparacoes", len(lines)
	for key in results:
		print key, " ", len(results[key]), " ", counter[key], " ", results[key]
