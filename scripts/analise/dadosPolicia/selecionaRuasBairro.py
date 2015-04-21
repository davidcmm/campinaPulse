# coding=utf-8

import sys

#Filters neighborhood and streets occurrences
if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Uso: <arquivo bairros e ruas>"
		sys.exit(1)

	dataFile = open(sys.argv[1], "r")
	lines = dataFile.readlines()

	occurrences = {"centro" : {}, "catole" : {}, "liberdade" : {}}

	#Saving amount of criminal occurrences in each street
	for line in lines:
		data = line.split("\t")

		if len(data) > 1:
			neig = data[0].strip().lower()
			street = data[1].strip().lower()
	
			if neig == "centro":
				if street in occurrences['centro'].keys():
					oldValue = occurrences['centro'][street]
					occurrences['centro'][street] = oldValue + 1
				else:
					occurrences['centro'][street] = 1
			elif 'cat' in neig[0:3]:
				if street in occurrences['catole'].keys():
					oldValue = occurrences['catole'][street]
					occurrences['catole'][street] = oldValue + 1
				else:
					occurrences['catole'][street] = 1
			elif neig == "liberdade":
				if street in occurrences['liberdade'].keys():
					oldValue = occurrences['liberdade'][street]
					occurrences['liberdade'][street] = oldValue + 1
				else:
					occurrences['liberdade'][street] = 1

	#Printing output
	for neig in occurrences.keys():
		neigOcc = occurrences[neig]
		for street in neigOcc.keys():
			amount =  neigOcc[street]
			print neig + "\t"  + street + "\t" + str(amount)
