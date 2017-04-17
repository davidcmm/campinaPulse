# coding=utf-8
# Evaluates groups of ids for a certain group and randomizes ids according to the number of ids in the other group!

import sys
from sets import Set
import random
import numpy as np
import json
import csv
import pandas as pd


if __name__ == "__main__":
	if len(sys.argv) < 4:
		print "Uso: <arquivo de grupo cujos ids devem ser mantidos> <arquivo de grupo cujos ids devem ser sorteados> <numero de sorteios desejados>"
		sys.exit(1)

	base_file = sys.argv[1]
	file_to_random = sys.argv[2]
	num_of_randomizations = int(sys.argv[3])

	base_data = pd.read_table(base_file, sep='\s+', encoding='utf8', skiprows=0)
	base_data.columns = ['id']

	data_to_random = pd.read_table(file_to_random, sep='\s+', encoding='utf8', skiprows=1)
	data_to_random.columns = ['id']

	if len(base_data['id']) == len(data_to_random['id']):
		print "Data arrays are already of same length! Could not randomize different data!"
		sys.exit(1)
	elif len(base_data['id']) > len(data_to_random['id']):
		print "Array to randomize is smaller than base array, so randomization can not be perform to have both arrays with same length!"
	else:
		
		for i in range(0, num_of_randomizations):
			random_data = data_to_random.take(np.random.permutation(len(data_to_random))[:len(base_data)])

			group = file_to_random.split(".")[0]
			output_file = open(group+"_"+str(i)+".dat", "w")
			output_file.write("[]\n")

			for index, row in random_data.iterrows():
				output_file.write(str(row['id'])+"\n")		

			output_file.close()

