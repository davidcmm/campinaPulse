# -*- coding: utf-8 -*-

import random
import sys

if __name__ == "__main__":
	if len(sys.argv) < 4:
		print "Uso: <numero de tarefas a serem geradas> <arquivo A com lista de fotos> <arquivo B com lista de fotos>"
		sys.exit(1)

	num_tarefas = int(sys.argv[1])
	nome_arquivo_A = sys.argv[2]
	nome_arquivo_B = sys.argv[3]

	arquivo_A = open(nome_arquivo_A, 'r')
	arquivo_B = open(nome_arquivo_B, 'r')

	fotos_A = arquivo_A.readlines()
	fotos_B = arquivo_B.readlines()

	copy_A = list(fotos_A)
	copy_B = list(fotos_B)

	for iteration in  range(0, num_tarefas):
		choice_A = random.choice(copy_A)
		choice_B = random.choice(copy_B)

		copy_A.remove(choice_A)
		copy_B.remove(choice_B)

		if len(copy_A) == 0:
			copy_A =  list(fotos_A)
		if len(copy_B) == 0:
			copy_B =  list(fotos_B)

		print "seguro\t" + choice_A.strip(' \t\n\r') + "\t" + choice_B.strip(' \t\n\r')
	
