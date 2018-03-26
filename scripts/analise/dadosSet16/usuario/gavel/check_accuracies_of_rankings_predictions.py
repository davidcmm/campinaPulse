# coding=utf-8
# Test predictions on testing data for each ranking strategy

import csv
import math

import sys
from sets import Set
import random
import numpy
import json
import pandas as pd

def build_qscore_rankings():
	data = pd.read_table("../all100/all_80.dat", sep='\s+', encoding='utf8', header=false)
	pleasant = data[data.loc[:,0] == "agrad%C3%A1vel?"].sort(columns=[2], ascending=True)
	safe = data[data.loc[:,0] == "seguro?"].sort(columns=[2], ascending=True)

	return {"pleasant" : pleasant, "safe" : safe}

def build_elo_rankings():
	data = pd.read_table("all_elo_80_10.dat", sep='\s+', encoding='utf8', header=false)
	pleasant_10 = data[data.loc[:,0] == "agrad%C3%A1vel?"].sort(columns=[2], ascending=True)
	safe_10 = data[data.loc[:,0] == "seguro?"].sort(columns=[2], ascending=True)

	data = pd.read_table("all_elo_80_20.dat", sep='\s+', encoding='utf8', header=false)
	pleasant_20 = data[data.loc[:,0] == "agrad%C3%A1vel?"].sort(columns=[2], ascending=True)
	safe_20 = data[data.loc[:,0] == "seguro?"].sort(columns=[2], ascending=True)

	data = pd.read_table("all_elo_80_40.dat", sep='\s+', encoding='utf8', header=false)
	pleasant_40 = data[data.loc[:,0] == "agrad%C3%A1vel?"].sort(columns=[2], ascending=True)
	safe_40 = data[data.loc[:,0] == "seguro?"].sort(columns=[2], ascending=True)

	return {"10" : {"pleasant" : pleasant_10, "safe" : safe_10}, "20" :  {"pleasant" : pleasant_20, "safe" : safe_20}, "40" : {"pleasant" : pleasant_40, "safe" : safe_40}}

def build_crowdbt_rankings():
	data = pd.read_table("allPairwiseComparison_80-lam01-gam01.dat", sep='\s+', encoding='utf8', header=false)
	pleasant_01 = data[data.loc[:,0] == "agrad%C3%A1vel?"].sort(columns=[2], ascending=True)
	safe_01 = data[data.loc[:,0] == "seguro?"].sort(columns=[2], ascending=True)

	data = pd.read_table("allPairwiseComparison_80-lam1-gam01.dat", sep='\s+', encoding='utf8', header=false)
	pleasant_1 = data[data.loc[:,0] == "agrad%C3%A1vel?"].sort(columns=[2], ascending=True)
	safe_1 = data[data.loc[:,0] == "seguro?"].sort(columns=[2], ascending=True)

	return {"01" : {"pleasant" : pleasant_01, "safe" : safe_01}, "1" :  {"pleasant" : pleasant_1, "safe" : safe_1}}

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Uso: <run with testing data>"
		sys.exit(1)

	elo = build_elo_rankings()
	build_maxdiff_rankings()
	qscore = build_qscore_rankings()
	gavel = build_crowdbt_rankings()
