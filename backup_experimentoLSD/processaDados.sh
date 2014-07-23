#!/bin/bash

#rm *.dat

#Pre-processamento para considerar como id 0 os usuários que não fizeram login
#python preProcessa.py test3.csv

#awk -F "," '{print $5, $NF}' output.csv > partial.csv
#awk -F " " '{print $1, $3, $4, $5}' partial.csv > data.csv
#rm partial.csv

#Analisa dados de acordo com Q-Score do PlacePulse
python analisaQScore.py output.csv > qscore_test3.dat
awk '{if ($1 == 1) print $0}' qscore_test3.dat > question1.dat
awk '{if ($1 == 2) print $0}' qscore_test3.dat > question2.dat
awk '{if ($1 == 3) print $0}' qscore_test3.dat > question3.dat
awk '{if ($1 == 4) print $0}' qscore_test3.dat > question4.dat

Rscript ordenaDados.R question1.dat
mv questionSorted.dat question1Sorted.dat
Rscript ordenaDados.R question2.dat
mv questionSorted.dat question2Sorted.dat
Rscript ordenaDados.R question3.dat
mv questionSorted.dat question3Sorted.dat
Rscript ordenaDados.R question4.dat
mv questionSorted.dat question4Sorted.dat

python preparaHTML.py question1Sorted.dat
mv question.html question1.html
python preparaHTML.py question2Sorted.dat
mv question.html question2.html
python preparaHTML.py question3Sorted.dat
mv question.html question3.html
python preparaHTML.py question4Sorted.dat
mv question.html question4.html

#Separa resultados gerais das comparacoes apenas pela contagem do número de imagens das quais ganhou
#python analisaGeral.py output.csv > geral.dat

#Separa resultados das comparacoes por formação dos usuários pela contagem do número de imagens das quais ganhou
#python analisaUsuario.py output.csv graduacao.csv > graduacao.dat
#python analisaUsuario.py output.csv mestrado.csv > mestrado.dat
#python analisaUsuario.py output.csv medio.csv > medio.dat

#Separa resultados das comparacoes por questões pela contagem do número de imagens das quais ganhou
#python analisaQuestoes.py output.csv 1 > question1.dat
#python analisaQuestoes.py output.csv 2 > question2.dat
#python analisaQuestoes.py output.csv 3 > question3.dat
#python analisaQuestoes.py output.csv 4 > question4.dat

#Gera percentuais de vitórias das fotos no geral
#Rscript analisaComparacoes.R geral.dat
#mv percentualGeralPorTotalDeComparacoes.dat pGeralTotalComparacoes.dat
#mv percentualGeralPorComparacoes.dat pGeralComparacoes.dat

#Gera percentuais de vitórias das fotos por grau de instrução
#Rscript analisaComparacoes.R graduacao.dat
#mv percentualGeralPorTotalDeComparacoes.dat pGraduacaoTotalComparacoes.dat
#mv percentualGeralPorComparacoes.dat pGraduacaoComparacoes.dat

#Rscript analisaComparacoes.R mestrado.dat
#mv percentualGeralPorTotalDeComparacoes.dat pMestradoTotalComparacoes.dat
#mv percentualGeralPorComparacoes.dat pMestradoComparacoes.dat

#Rscript analisaComparacoes.R medio.dat
#mv percentualGeralPorTotalDeComparacoes.dat pMedioTotalComparacoes.dat
#mv percentualGeralPorComparacoes.dat pMedioComparacoes.dat

#Gera percentuais de vitórias das fotos por questao
#Rscript analisaComparacoes.R question1.dat
#mv percentualGeralPorTotalDeComparacoes.dat pQuestao1TotalComparacoes.dat
#mv percentualGeralPorComparacoes.dat pQuestao1Comparacoes.dat

#Rscript analisaComparacoes.R question2.dat
#mv percentualGeralPorTotalDeComparacoes.dat pQuestao2TotalComparacoes.dat
#mv percentualGeralPorComparacoes.dat pQuestao2Comparacoes.dat

#Rscript analisaComparacoes.R question3.dat
#mv percentualGeralPorTotalDeComparacoes.dat pQuestao3TotalComparacoes.dat
#mv percentualGeralPorComparacoes.dat pQuestao3Comparacoes.dat

#Rscript analisaComparacoes.R question4.dat
#mv percentualGeralPorTotalDeComparacoes.dat pQuestao4TotalComparacoes.dat
#mv percentualGeralPorComparacoes.dat pQuestao4Comparacoes.dat
