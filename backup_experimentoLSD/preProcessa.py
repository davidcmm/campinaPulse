import sys

if __name__ == "__main__":
	if len(sys.argv) < 1:
		print "Uso: <arquivo com dados>"
		sys.exit(1)
	
	inputFile = open(sys.argv[1], 'r')
	output = open('output.csv', 'w')
	lines = inputFile.readlines()

	for line in lines:
		data = line.split(",")
		if not data[0]:
			data[0] = '0'			
		#Fazer o parse para capturar a pergunta respondida, a foto vencedora, a foto da esquerda e a foto da direita		
		info = data[1][3:-4].split(" ")
		if len(info) == 4:
			#User id, question answered, answer, left photo, right photo
			output.write(data[0]+'\t'+info[0]+'\t'+info[1]+'\t'+info[2]+'\t'+info[3]+'\n')

	output.close()
	inputFile.close()
