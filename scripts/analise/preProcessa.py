import sys

if __name__ == "__main__":
	if len(sys.argv) < 1:
		print "Uso: <arquivo com dados>"
		sys.exit(1)
	
	inputFile = open(sys.argv[1], 'r')
	output = open('output.csv', 'w')
	lines = inputFile.readlines()
	
	questionsMap = {1:"", 2:"", 3:"", 4:""}

	for line in lines:
		data = line.split(",")
		if not data[0]:
			data[0] = '0'			
		#Fazer o parse para capturar a pergunta respondida, a foto vencedora, a foto da esquerda e a foto da direita		
		info = data[1][3:-4].split(" ")
		if len(info) == 4:
			#User id, question answered, answer, left photo, right photo
			output.write(data[0]+'\t'+info[0]+'\t'+info[5].decode('utf-8')+'\t'+info[6].split("/")[4]+'\t'+info[7].split("/")[4]+'\n')

	output.close()
	inputFile.close()
