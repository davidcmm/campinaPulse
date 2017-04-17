# coding=utf-8
# Given the randomized ids for a certain group and the whole set of ids for the group looks for the difference in ids in order to call script selectRunPerUsers to remove the corresponding ids of this difference

import sys
from sets import Set
import random
import numpy as np
import json
import csv
import pandas as pd
import os, fnmatch

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print "Uso: <grupo a considerar: masculino, feminino, adulto, jovem, media ou baixa> <arquivo de ids a considerar>"
		sys.exit(1)

	group = sys.argv[1]

	base_file = group + ".dat"
	base_data = pd.read_table(base_file, sep='\s+', encoding='utf8', skiprows=0)	
	base_data.columns = ['id']

	#selected_files = fnmatch.filter(os.listdir('.'), group+'_*.dat')
	#for filename in selected_files:
	filename = sys.argv[2]
	random_data = pd.read_table(filename, sep='\s+', encoding='utf8', skiprows=0)	
	random_data.columns = ['id']

	difference = list(set(base_data['id'].values) - set(random_data['id'].values))

	output_file = open("diff_"+group+"_"+filename.split("_")[1].split(".")[0]+".dat", "w")
	output_file.write("[]\n")

	for id in difference:
		output_file.write(str(id)+"\n")		

	output_file.close()
		
	
