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
	if len(sys.argv) < 5:
		print "Uso: <method:igual, desb> <outros dados>"
		print "igual -> <arquivo de grupo cujos ids devem ser mantidos> <arquivo de grupo cujos ids devem ser sorteados> <numero de sorteios desejados>"
		print "desb -> <tamanho grupo 1> <tamanho grupo 2> <arquivo grupo 1> <arquivo grupo 2> <numero de sorteios desejados>"
		sys.exit(1)

	method = sys.argv[1]

	if method == "igual":
		base_file = sys.argv[2]
		file_to_random = sys.argv[3]
		num_of_randomizations = int(sys.argv[4])

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

	elif method == "desb":
		group1_size = int(sys.argv[2])		
		group2_size = int(sys.argv[3])

		group1_file = sys.argv[4]
		group2_file = sys.argv[5]

		num_of_randomizations = int(sys.argv[6])

		g1_data = pd.read_table(group1_file, sep='\s+', encoding='utf8', skiprows=0)
		g1_data.columns = ['id']

		g2_data = pd.read_table(group2_file, sep='\s+', encoding='utf8', skiprows=0)
		g2_data.columns = ['id']

		group1 = group1_file.split(".")[0]
		group2 = group2_file.split(".")[0]

		print str(g1_data)

		for i in range(0, num_of_randomizations):
			#random_g1 = g1_data.take(np.random.permutation(len(g1_data))[:group1_size])
			#random_g2 = g2_data.take(np.random.permutation(len(g2_data))[:group2_size])

			random_g1 = np.random.choice(g1_data['id'], size=group1_size, replace=True)
			random_g2 = np.random.choice(g2_data['id'], size=group2_size, replace=True)

			output_file1 = open(group1+"_"+str(i)+".dat", "w")
			output_file1.write("[]\n")

			output_file2 = open(group2+"_"+str(i)+".dat", "w")
			output_file2.write("[]\n")

			#for index, row in random_g1.iterrows():
			for value in random_g1:
				output_file1.write(str(value)+"\n")	

			#for index, row in random_g2.iterrows():
			for value in random_g2:
				output_file2.write(str(value)+"\n")	

			output_file1.close()
			output_file2.close()

	else:
		print "ERROR! Invalid method used!"
		sys.exit(1)
		

