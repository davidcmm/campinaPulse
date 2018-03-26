# coding=utf-8
import sys
from sets import Set
import re
import random

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Uso: <run.csv>"
		sys.exit(1)

	filename = sys.argv[1]
	data_file = open(filename, 'r')
	lines = data_file.readlines()

	output_file = open("run_08.csv", "w")
	
	for line in lines:
		random_val = random.random()
		if random_val <= 0.8:
			output_file.write(line)

	output_file.close()
	data_file.close()	
		
	
