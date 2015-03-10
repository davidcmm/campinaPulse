#!/bin/bash

awk -F "," '{print $5, $NF}' test.csv > partial.csv
awk -F " " '{print $1, $3, $4, $5}' partial.csv > data.csv
rm partial.csv

#Analise geral
python analisaGeral.py data.csv > geral.dat

#Analise grupo
python analisaGrupo.py data.csv graduacao.csv > graduacao.dat

#Analise grupo
python analisaGrupo.py data.csv mestrado.csv > mestrado.dat

#Analise grupo
python analisaGrupo.py data.csv medio.csv > medio.dat

