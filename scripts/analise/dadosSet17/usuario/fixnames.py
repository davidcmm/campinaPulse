# coding=utf-8
# This script receives a file with street names, qscores and lat/long and replaces street names whitespaces with _

import sys

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Uso: <arquivo com ruas, qscore e lat/long>"
		sys.exit(1)

	data_file = open(sys.argv[1], "r")
	lines = data_file.readlines()
	data_file.close()
	output_file = open(sys.argv[1], "w")
	
	for line in lines:
		data = line.split("+")
		question = data[0].strip(" \t")
		street = data[1].strip(" \t")
		qscore = data[2].strip(" \t")
		lat = data[3].strip(" \t")
		lon = data[4].strip(" \t")
		street_name = street.replace(" ", "_")

		output_file.write(question+"+"+street_name+"+"+qscore+"+"+lat+"+"+lon)

	output_file.close()		
