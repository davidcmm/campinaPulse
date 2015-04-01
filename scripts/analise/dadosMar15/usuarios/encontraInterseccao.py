# coding=utf-8
#Analyses the intersection of two QScore rankings in order to find the amount of photos ranked in common

import sys
from sets import Set

possibleQuestions = ["agrad%C3%A1vel?", "seguro?"]

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print "Uso: <arquivo1 com ranking das fotos> <arquivo2 com ranking das fotos>"
		sys.exit(1)

	file1 = open(sys.argv[1], "r")
	file2 = open(sys.argv[2], "r")
	data1 = file1.readlines()
	data2 = file2.readlines()

	photos1 = {possibleQuestions[0]:Set([]), possibleQuestions[1]:Set([])}
	photos2 = {possibleQuestions[0]:Set([]), possibleQuestions[1]:Set([])}
	
	#First file
	for line in data1:
	     dados = line.split("\t")
	     if float(dados[2].strip()) != -1:#Checking if photo received a QScore
		photos1[dados[0]].add(dados[1])


	#Second file
	for line in data2:
	     dados = line.split("\t")
	     if float(dados[2].strip()) != -1:#Checking if photo received a QScore
		photos2[dados[0]].add(dados[1])

	for question in possibleQuestions:
		set1 = photos1[question]
		set2 = photos2[question]
		intersection = set1.intersection(set2)
		print question+"\t"+str(len(intersection)) + "\t" + str(intersection)
