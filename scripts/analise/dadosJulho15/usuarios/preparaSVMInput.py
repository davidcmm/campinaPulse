# coding=utf-8
# This script receives a file containing QScores, rgb and lines data and convert it to SVM input format
import sys

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Uso: <arquivo com ruas, qscore, rgb e linhas>"
		sys.exit(1)

	dataFile = open(sys.argv[1], "r")
	lines = dataFile.readlines()

	for line in lines[1:]:
		data = line.split("\t")
		qscore = data[1].strip()
		red = data[2].strip()
		green = data[3].strip()
		blue = data[4].strip()
		diag = data[5].strip()	
		hor = data[6].strip()
		vert = data[7].strip()
		
		print qscore+"\t"+"1:"+red+"\t"+"2:"+green+"\t"+"3:"+blue+"\t"+"4:"+diag+"\t"+"5:"+hor+"\t"+"6:"+vert
