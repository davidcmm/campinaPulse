#!/bin/python

import sys
from sets import Set
import random
import numpy
import json
import csv
import pandas as pd
import operator

def write_html(photos_differences, question, photos_info):

	outputFile = open("fotos_ordenadas_por_local_"+question+".html", "w")

	outputFile.write("<body style=\"overflow:scroll\">\n");
	counter = 0
	outputFile.write("<h2>"+question+"</h2>")
	
	outputFile.write("<table>\n")
	outputFile.write("<tr>\n")

	for item in sorted_diff:
		photo1 = item[0].split("+")[0]
		photo2 = item[0].split("+")[1]

		if "catole" in photo1 or "liberdade" in photo1:
			photo1_url = "https://contribua.org/bairros/oeste/"+photo1
		else:
			photo1_url = "https://contribua.org/bairros/norte/"+photo1

		if "catole" in photo2 or "liberdade" in photo2:
			photo2_url = "https://contribua.org/bairros/oeste/"+photo2
		else:
			photo2_url = "https://contribua.org/bairros/norte/"+photo2
			
		outputFile.write("<td><img src=\""+photo1_url+"\" width=\"400\" height=\"300\"></td>\n")
		outputFile.write("<td><img src=\""+photo2_url+"\" width=\"400\" height=\"300\"></td>\n")
		outputFile.write("<td>" + str(photo1) + " " + str(photos_info[photo1]) + " " + str(photo2) + " " + str(photos_info[photo2]) + " Diff: " + str(item[1]) + "</td>\n")
		counter += 1

		outputFile.write("</tr>\n")
		outputFile.write("<tr>\n")

	outputFile.write("</tr>\n")
	outputFile.write("</table>")
	outputFile.write("</body>\n")

	outputFile.close()	


if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Uso: <arquivo com Q-Scores>"
		sys.exit(1)

	data = pd.read_table(sys.argv[1], sep='\s+', encoding='utf8', header=0)
	images_dict = {"agrad%C3%A1vel?" : {}, "seguro?" : {}}

	#Reading qscores
	for index, row in data.iterrows():
		image =	row['V2']
		question = row['V1']
		qscore = row['V3']

		images_dict[question][image] = qscore


	for question in images_dict.keys():
		print(">>>>> Scores " + question)
		photos_info = images_dict[question]
		photos = photos_info.keys()
		photos.sort()#Sorting photos so that same places become close to each other!

		for photo in photos:
			print(str(photo)+"\t"+str(photos_info[photo]))

		#Computing Q-Scores differences for same places
		photos_diff = {}
		for i in range(0, len(photos)-1, 2):
			photo1 = photos[i]
			photo2 = photos[i+1]
			photos_diff[photo1+"+"+photo2] = abs(photos_info[photo1] - photos_info[photo2])

		print(">>>>> Diffs " + question)
		#Printing places according to sorted difference
		sorted_diff = sorted(photos_diff.items(), key=operator.itemgetter(1))
		for item in sorted_diff:
			print(str(item[0])+"\t"+str(item[1]))

		write_html(sorted_diff, question, photos_info)
		
