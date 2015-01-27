import random
import sys
import glob
from get_images import get_photos_votes

def createCSV(photos):

    file = open("tarefas.csv", "w")
    file.write("question,url_a,url_c\n")
    question1 = "Qual local lhe parece mais seguro?"
    question2 = "Qual local lhe parece mais agradável?"

    index2 = len(photos)-1
    print "Init" + " " + str(index2)

    for index in range(0, len(photos)):
	file.write(question1+","+photos[index]['url_c']+","+photos[index]['url_a']+"\n")
	file.write(question2+","+photos[index2]['url_c']+","+photos[index2]['url_a']+"\n")
	
	print "Comp1: " + str(index) + " " + str(question1+","+photos[index]['url_c']+","+photos[index]['url_a']+"\n")
	print "Comp2: " + str(index2) + " " + str(question2+","+photos[index2]['url_c']+","+photos[index2]['url_a']+"\n")
	index2 = index2 - 1

    file.close()

if __name__ == "__main__":
    if len(sys.argv) < 1:
	print "Uso: <numero de tarefas a serem geradas>"
	sys.exit(1)

    #photos = get_photos_partial()
    photos = get_photos_votes()
    createCSV(photos)
