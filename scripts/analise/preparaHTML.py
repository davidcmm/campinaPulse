# coding=utf-8

import sys

if __name__ == "__main__":
	if len(sys.argv) < 1:
		print "Uso: <arquivo com dados>"
		sys.exit(1)
	
	dataFile = open(sys.argv[1], 'r')
	outputFile = open("question.html", 'w')
	lines = dataFile.readlines()
	
	counter = 0
	outputFile.write("<table>\n")
	outputFile.write("<tr>\n")

	for line in lines[1:]:
		data = line.split(" ")

		question = data[1].strip(' \t\n\r')
		photo = data[2].strip(' \t\n\r')[1:-1]
		qscore = data[3].strip(' \t\n\r')

		if "almirante" in photo:
			folder = "http://socientize.lsd.ufcg.edu.br/almirante"
		elif "rodrigues" in photo:
			folder = "http://socientize.lsd.ufcg.edu.br/rodrigues"
		else:
			folder = "http://socientize.lsd.ufcg.edu.br/floriano"
		outputFile.write("<td><img src=\""+folder+"/"+photo+"\" width=\"400\" height=\"300\"></td>\n")
		outputFile.write("<td>"+photo + " " + qscore+"</td>\n")
		counter += 1

		if counter % 3 == 0:
			outputFile.write("</tr>\n")
			outputFile.write("<tr>\n")

	outputFile.write("</tr>\n")
	outputFile.write("</table>")

	dataFile.close()
	outputFile.close()
