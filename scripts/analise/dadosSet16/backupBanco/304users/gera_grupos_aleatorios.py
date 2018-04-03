# coding=utf-8
# Get all users ids and creates two random groups

import sys
import pandas as pd
import numpy as np


if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Uso: usersInfo file"
		sys.exit(1)

	lines = open(sys.argv[1], "r").readlines()
	group_size = 100
	all_ids = []

	for line in lines:
		all_ids.append(line.split("|")[0])

	group1 = np.random.choice(all_ids, size=group_size, replace=False)
	group2 = np.random.choice(all_ids, size=group_size, replace=False)

	group1_file = open("random1.dat", "w")
	for id in group1:
		group1_file.write(str(id)+"\n")

	group2_file = open("random2.dat", "w")
	for id in group2:
		group2_file.write(str(id)+"\n")

	group1_file.close()
	group2_file.close()
