import sys
import time as tm
import datetime
from sets import Set
import numpy as np

possibleQuestions = ["agradavel?", "seguro?"]

def count_users_tasks(lines, output_filename):

	output_file = open(output_filename, "w")
	for line in lines1:
		data = line.split("|")
		userID = data[0]
		tasks1 = eval(data[2])
		tasks2 = eval(data[3])

		output_file.write( userID + "\t" + str(len(tasks1) + len(tasks2))+"\n" )

	output_file.close()
		


if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Uso: <usersInfo.dat>"
		sys.exit(1)

	dataFile1 = open(sys.argv[1], 'r')
	lines1 = dataFile1.readlines()

	count_users_tasks(lines1, "users_tasks_counters.dat")
	dataFile1.close()
