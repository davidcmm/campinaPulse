# coding=utf-8
# This script receives a file containing streets and QScores in order to retrieve the streets name to search in Google Geocode

import sys

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Uso: <arquivo com ruas e qscore>"
		sys.exit(1)

	dataFile = open(sys.argv[1], "r")
	lines = dataFile.readlines()
	
	for line in lines:
		data = line.split("\t")
		street = data[1].split("/")[6]
		streetName = " "
		streetData = street.replace("_", " ").split(" ")
		for value in streetData:
			if len(value) > 0 and not ".jpg" in value:
				streetName += value + " "
		print data[0] + "+" + streetName + "+" + data[2].strip()
		
