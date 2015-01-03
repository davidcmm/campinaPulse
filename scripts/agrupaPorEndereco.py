#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from sets import *

nomeSaida = "tarefasModificadasAgrupadas.csv"

def agregaTarefas(nomeArquivo):
   arquivo = open(nomeArquivo, "r")
   linhas = arquivo.readlines()
   tarefas = {"Qual local lhe parece mais agradável?" : {}, "Qual local lhe parece mais seguro?" : {}}

   #Criando mapas, por pergunta, contendo as relacoes entre todas as fotos
   for linha in linhas[1:]:
	dados = linha.split("\t")

	mapa = tarefas.get(dados[0])
	comparacoes = []	
	comparacoes2 = []

    	if mapa.has_key(dados[1].strip()):
		comparacoes = mapa.get(dados[1].strip())
	
	if mapa.has_key(dados[2].strip()):
		comparacoes2 = mapa.get(dados[2].strip())

	comparacoes.append(dados[2].strip())
	comparacoes2.append(dados[1].strip())

	mapa[dados[1].strip()] = comparacoes
	mapa[dados[2].strip()] = comparacoes2

   tarefasAgradavel = tarefas.get("Qual local lhe parece mais agradável?")
   tarefasSeguro = tarefas.get("Qual local lhe parece mais seguro?")

   percorridosAgradavel = []
   percorridosSeguro = []

   fotosAgradavel = tarefasAgradavel.keys()
   #print ">>>> Agradavel "+ str(len(fotosAgradavel))
   #for key in fotosAgradavel:
	#print str(key) + "\t" + str(len(tarefasAgradavel[key]))
   fotoAAtual = fotosAgradavel[0]

   fotosSeguro = tarefasSeguro.keys()
   #print ">>>> Seguro "+ str(len(fotosSeguro))
   #for key in fotosSeguro:
	#print str(key) + "\t" + str(len(tarefasSeguro[key]))
   fotoSAtual = fotosSeguro[0]

   resultadoAgradavel = []
   resultadoSeguro = []
   
   #Criando as tarefas de comparacoes entre fotos
   montaCombinacoes("Qual local lhe parece mais agradável?", resultadoAgradavel, fotoAAtual, tarefasAgradavel, percorridosAgradavel)
   montaCombinacoes("Qual local lhe parece mais seguro?", resultadoSeguro, fotoSAtual, tarefasSeguro, percorridosSeguro)

   #print len(resultadoAgradavel)
   #print len(resultadoSeguro)

   #Criando arquivo de saida
   saida = open(nomeSaida, "w")
   i2 = len(resultadoSeguro)-1
   saida.write("question\turl_a\turl_c\n")

   for i in range(0, len(resultadoAgradavel)):
	saida.write(resultadoAgradavel[i]+"\n")
	saida.write(resultadoSeguro[i2]+"\n")
	i2 = i2 - 1
   saida.close()
   arquivo.close()

   verificaArquivo(nomeArquivo, nomeSaida)

#Verifica se todas as tarefas existentes na entrada estao presentes no arquivo de saida
def verificaArquivo(entrada, saida):
    arquivoE = open(entrada, "r")
    arquivoS = open(saida, "r")
  
    linhasE = arquivoE.readlines()
    linhasS = arquivoS.readlines()

    if len(linhasE) != len(linhasS):
	print "## Erro! tamanhos diferentes"

    for ind in range(0, len(linhasE)):
	linha = linhasE[ind]
	if not linha in linhasS:
		dados = linha.split("\t")
		novoTexto = dados[0].strip()+"\t"+dados[2].strip()+"\t"+dados[1].strip()+"\n"
		if not novoTexto in linhasS:
			print "## Erro! Linha "+str(ind)+" "+novoTexto

#Cria as tarefas para cada combinacao de fotos evitando duplicacao de tarefas
def montaCombinacoes(questao, resultado, fotoatual, tarefas, percorridos):
   if fotoatual in percorridos:
	return

   fotoa1 = fotoatual
   fotosa1 = tarefas[fotoa1]
   for foto in fotosa1:
	if not foto in percorridos:
		if fotoa1 == foto:
			print ">>>> Erro! " + fotoa1 + foto
			return
		resultado.append(questao+"\t"+fotoa1+"\t"+foto)
   percorridos.append(fotoa1)  

   for foto in fotosa1:
	if not foto in percorridos:
		montaCombinacoes(questao, resultado, foto, tarefas, percorridos)	
		percorridos.append(foto)

if __name__ == "__main__":
   if len(sys.argv) < 2:
	print "Uso: <arquivo de tarefas ordenadas>"
	sys.exit(1)

   agregaTarefas(sys.argv[1])
	    
