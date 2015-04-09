#!/bin/bash

#Separa grupos de usuarios
python selectPerID.py run.csv media.dat > runMedia.csv
python selectPerID.py run.csv baixa.dat > runBaixa.csv 
python selectPerID.py run.csv adulto.dat > runAdulto.csv 
python selectPerID.py run.csv jovem.dat > runJovem.csv  
python selectPerID.py run.csv solteiro.dat > runSolteiro.csv 
python selectPerID.py run.csv casado.dat > runCasado.csv 
python selectPerID.py run.csv feminino.dat > runFeminino.csv 
python selectPerID.py run.csv masculino.dat > runMasculino.csv

mv media.dat baixa.dat adulto.dat jovem.dat solteiro.dat casado.dat feminino.dat masculino.dat idsGrupos 

#Analisa QScores
python analisaQScore.py runAdulto.csv
mv first.dat firstAdulto.dat
python analisaQScore.py runJovem.csv 
mv first.dat firstJovem.dat
python analisaQScore.py runSolteiro.csv 
mv first.dat firstSolteiro.dat
python analisaQScore.py runCasado.csv 
mv first.dat firstCasado.dat
python analisaQScore.py runMedia.csv 
mv first.dat firstMedia.dat
python analisaQScore.py runBaixa.csv 
mv first.dat firstBaixa.dat
python analisaQScore.py runFeminino.csv 
mv first.dat firstFeminino.dat
python analisaQScore.py runMasculino.csv
mv first.dat firstMasculino.dat

sort -k 3 -r firstMedia.dat > firsMediaOrd.dat
sort -k 3 -r firstBaixa.dat > firsBaixaOrd.dat
sort -k 3 -r firstSolteiro.dat > firsSolteiroOrd.dat
sort -k 3 -r firstCasado.dat > firsCasadoOrd.dat
sort -k 3 -r firstFeminino.dat > firsFemininoOrd.dat
sort -k 3 -r firstMasculino.dat > firsMasculinoOrd.dat
sort -k 3 -r firstJovem.dat > firsJovemOrd.dat
sort -k 3 -r firstAdulto.dat > firsAdultoOrd.dat

#Encontra interseccao entre qscores gerados
python encontraInterseccao.py firsBaixaOrd.dat firsMediaOrd.dat > intersectionBaixaMedia.dat 
python encontraInterseccao.py firsSolteiroOrd.dat firsCasadoOrd.dat > intersectionSolteiroCasado.dat
python encontraInterseccao.py firsFemininoOrd.dat firsMasculinoOrd.dat > intersectionFemininoMasculino.dat
python encontraInterseccao.py firsJovemOrd.dat firsAdultoOrd.dat > intersectionJovemAdulto.dat

#Prepara paginas html e arquivos de interseccao ordenados
python preparaHTML.py firsJovemOrd.dat intersectionJovemAdulto.dat > firsJovemOrdInter.dat 
mv question.html questionJovem.html
python preparaHTML.py firsAdultoOrd.dat intersectionJovemAdulto.dat > firsAdultoOrdInter.dat 
mv question.html questionAdulto.html

python preparaHTML.py firsMediaOrd.dat intersectionBaixaMedia.dat > firsMediaOrdInter.dat 
mv question.html questionMedia.html
python preparaHTML.py firsBaixaOrd.dat intersectionBaixaMedia.dat > firsBaixaOrdInter.dat 
mv question.html questionBaixa.html

python preparaHTML.py firsFemininoOrd.dat intersectionFemininoMasculino.dat > firsFemininoOrdInter.dat 
mv question.html questionFeminino.html
python preparaHTML.py firsMasculinoOrd.dat intersectionFemininoMasculino.dat > firsMasculinoOrdInter.dat 
mv question.html questionMasculino.html

python preparaHTML.py firsCasadoOrd.dat intersectionSolteiroCasado.dat > firsCasadoOrdInter.dat 
mv question.html questionCasado.html
python preparaHTML.py firsSolteiroOrd.dat intersectionSolteiroCasado.dat > firsSolteiroOrdInter.dat 
mv question.html questionSolteiro.html

mv question*.html rankings

#Combina RGB, #Linhas e criterios
python combinaRGBQScoreLinhas.py rgb.dat firsAdultoOrdInter.dat lines.dat
mv rgbQScoreAgrad.dat rgbQScoreAgradAdulto.dat
mv rgbQScoreSeg.dat rgbQScoreSegAdulto.dat
python combinaRGBQScoreLinhas.py rgb.dat firsJovemOrdInter.dat lines.dat
mv rgbQScoreAgrad.dat rgbQScoreAgradJovem.dat
mv rgbQScoreSeg.dat rgbQScoreSegJovem.dat

python combinaRGBQScoreLinhas.py rgb.dat firsMediaOrdInter.dat lines.dat
mv rgbQScoreAgrad.dat rgbQScoreAgradMedia.dat
mv rgbQScoreSeg.dat rgbQScoreSegMedia.dat
python combinaRGBQScoreLinhas.py rgb.dat firsBaixaOrdInter.dat lines.dat
mv rgbQScoreAgrad.dat rgbQScoreAgradBaixa.dat
mv rgbQScoreSeg.dat rgbQScoreSegBaixa.dat

python combinaRGBQScoreLinhas.py rgb.dat firsFemininoOrdInter.dat lines.dat
mv rgbQScoreAgrad.dat rgbQScoreAgradFeminino.dat
mv rgbQScoreSeg.dat rgbQScoreSegFeminino.dat
python combinaRGBQScoreLinhas.py rgb.dat firsMasculinoOrdInter.dat lines.dat
mv rgbQScoreAgrad.dat rgbQScoreAgradMasculino.dat
mv rgbQScoreSeg.dat rgbQScoreSegMasculino.dat

python combinaRGBQScoreLinhas.py rgb.dat firsCasadoOrdInter.dat lines.dat
mv rgbQScoreAgrad.dat rgbQScoreAgradCasado.dat
mv rgbQScoreSeg.dat rgbQScoreSegCasado.dat
python combinaRGBQScoreLinhas.py rgb.dat firsSolteiroOrdInter.dat lines.dat
mv rgbQScoreAgrad.dat rgbQScoreAgradSolteiro.dat
mv rgbQScoreSeg.dat rgbQScoreSegSolteiro.dat

#Analisa Correlacao
Rscript analisaCorrelacao.R rgbQScoreAgradMedia.dat rgbQScoreSegMedia.dat > correlacaoMedia.dat
Rscript analisaCorrelacao.R rgbQScoreAgradBaixa.dat rgbQScoreSegBaixa.dat > correlacaoBaixa.dat
Rscript analisaCorrelacao.R rgbQScoreAgradMedia.dat rgbQScoreSegMedia.dat > correlacaoMedia.dat
Rscript analisaCorrelacao.R rgbQScoreAgradMedia.dat rgbQScoreSegMedia.dat > correlacaoMedia.dat
Rscript analisaCorrelacao.R rgbQScoreAgradMedia.dat rgbQScoreSegMedia.dat > correlacaoMedia.dat
Rscript analisaCorrelacao.R rgbQScoreAgradMedia.dat rgbQScoreSegMedia.dat > correlacaoMedia.dat
Rscript analisaCorrelacao.R rgbQScoreAgradMedia.dat rgbQScoreSegMedia.dat > correlacaoMedia.dat
Rscript analisaCorrelacao.R rgbQScoreAgradMedia.dat rgbQScoreSegMedia.dat > correlacaoMedia.dat

Rscript analisaRegressao.R
