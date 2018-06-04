# coding=utf-8
# Reads Q-Scores per photo and group them by street and by point in order to evaluate variations!


import sys
from sets import Set
import random
import numpy
import json
import csv
import pandas as pd


if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Uso: <arquivo com Q-Scores ordenados>"
		sys.exit(1)

	df = pd.read_table(sys.argv[1], sep='\s+', encoding='utf8', header=None)

	#Retrieving street name, number and angle of each photo
	def get_street_name(values):
		data = values.split("/")[6].split("_")[0:-2]
		return "_".join(data)
	
	def get_street_num(values):
		data = values.split("/")[6].split("_")[-2]
		return data

	def get_street_angle(values):
		data = values.split("/")[6].split("_")[-1].split(".")
		return data[0]

	df['rua'] = df[1].apply(get_street_name)
	df['numero'] = df[1].apply(get_street_num)
	df['angulo'] = df[1].apply(get_street_angle)

	#Updating numbers at Floriano street
	df.loc[(df['rua'] == "Av._Mal._Floriano_Peixoto") & (df['numero'] == "912"), 'numero'] = "913"
	df.loc[(df['rua'] == "Av._Mal._Floriano_Peixoto") & (df['numero'] == "826"), 'numero'] = "813"
	df.loc[(df['rua'] == "Av._Mal._Floriano_Peixoto") & (df['numero'] == "660"), 'numero'] = "691"
	df.loc[(df['rua'] == "Av._Mal._Floriano_Peixoto") & (df['numero'] == "580"), 'numero'] = "549"
	df.loc[(df['rua'] == "Av._Mal._Floriano_Peixoto") & (df['numero'] == "480"), 'numero'] = "445"

	#TO DO: Lidar com numero / Floriano Peixoto!
	#Group by street and then street, number to see summaries: http://pandas.pydata.org/pandas-docs/stable/groupby.html#applying-multiple-functions-at-once
	out_summary = open("qscores-df-summary.dat", "w")
	grouped = df.groupby('rua')
	out_summary.write(str(grouped[2].describe()))#Description of mean value of Q-Scores simulations per street
	out_summary.write("\n")

	grouped = df.groupby(['rua', 'numero'], as_index=False)
	out_summary.write(str(grouped[2].describe()))
	out_summary.write("\n")
	out_summary.close()

	#Output dataframe
	df.to_csv("./qscores-df.csv", index=False, header=['question', 'url', 'qscore', 'street', 'num', 'angle'], columns=[0, 1, 2, 'rua', 'numero', 'angulo'], encoding='utf-8')

	#Iterate through all streets, numbers!
	#all_streets = data.rua.unique()
	#def get_summary_per_street(current_df):
	#	all_numbers = current_df.numero.unique()
	#	
	#for street in all_streets:
	#	bool_street = (df.rua == street)
	#	street_df = df[bool_street]
#
#		get_summary_per_street(street_df)
		



