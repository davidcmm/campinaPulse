#!/bin/bash

python analisaUsuarios.py run.csv

#Separa grupos de usuarios
python selectRunPerUsers.py run.csv media.dat > runMedia.csv
python selectRunPerUsers.py run.csv baixa.dat > runBaixa.csv 
python selectRunPerUsers.py run.csv adulto.dat > runAdulto.csv 
python selectRunPerUsers.py run.csv jovem.dat > runJovem.csv  
python selectRunPerUsers.py run.csv solteiro.dat > runSolteiro.csv 
python selectRunPerUsers.py run.csv casado.dat > runCasado.csv 
python selectRunPerUsers.py run.csv feminino.dat > runFeminino.csv 
python selectRunPerUsers.py run.csv masculino.dat > runMasculino.csv
python selectRunPerUsers.py run.csv catole.dat > runCatole.csv
python selectRunPerUsers.py run.csv centro.dat > runCentro.csv
python selectRunPerUsers.py run.csv liberdade.dat > runLiberdade.csv
python selectRunPerUsers.py run.csv notcatole.dat > runNotCatole.csv
python selectRunPerUsers.py run.csv notcentro.dat > runNotCentro.csv
python selectRunPerUsers.py run.csv notliberdade.dat > runNotLiberdade.csv

mv alta.dat baixa.dat adulto.dat jovem.dat solteiro.dat casado.dat feminino.dat masculino.dat catole.dat centro.dat liberdade.dat notcentro.dat notliberdade.dat notcatole.dat idsGrupos 

#Analisa QScores
python analisaQScore.py run.csv
mv first.dat first_vote.dat

python analisaQScore.py runAdulto.csv 
mv first.dat firstAdulto.dat
mv all.dat allAdulto.dat
python analisaQScore.py runJovem.csv 1000
mv first.dat firstJovem.dat
mv all.dat allJovem.dat
python analisaQScore.py runSolteiro.csv 1000
mv first.dat firstSolteiro.dat
mv all.dat allSolteiro.dat
python analisaQScore.py runCasado.csv 1000
mv first.dat firstCasado.dat
mv all.dat allCasado.dat
python analisaQScore.py runMedia.csv 1000
mv first.dat firstMedia.dat
mv all.dat allMedia.dat
python analisaQScore.py runBaixa.csv 1000
mv first.dat firstBaixa.dat
mv all.dat allBaixa.dat
python analisaQScore.py runFeminino.csv 1000 
mv first.dat firstFeminino.dat
mv all.dat allFeminino.dat
python analisaQScore.py runMasculino.csv 1000
mv first.dat firstMasculino.dat
mv all.dat allMasculino.dat
python analisaQScore.py runCatole.csv 1000
mv first.dat firstCatole.dat
mv all.dat allCatole.dat
python analisaQScore.py runCentro.csv 1000
mv first.dat firstCentro.dat
mv all.dat allCentro.dat
python analisaQScore.py runLiberdade.csv 1000
mv first.dat firstLiberdade.dat
mv all.dat allLiberdade.dat
python analisaQScore.py runNotCatole.csv 1000
mv first.dat firstNotCatole.dat
mv all.dat allNotCatole.dat
python analisaQScore.py runNotCentro.csv 1000
mv first.dat firstNotCentro.dat
mv all.dat allNotCentro.dat
python analisaQScore.py runNotLiberdade.csv 1000
mv first.dat firstNotLiberdade.dat
mv all.dat allNotLiberdade.dat

sort -k 3 -r first_vote.dat > first_vote_ordenado.dat

sort -k 3 -r firstMedia.dat > firsMediaOrd.dat
sort -k 3 -r firstBaixa.dat > firsBaixaOrd.dat
sort -k 3 -r firstSolteiro.dat > firsSolteiroOrd.dat
sort -k 3 -r firstCasado.dat > firsCasadoOrd.dat
sort -k 3 -r firstFeminino.dat > firsFemininoOrd.dat
sort -k 3 -r firstMasculino.dat > firsMasculinoOrd.dat
sort -k 3 -r firstJovem.dat > firsJovemOrd.dat
sort -k 3 -r firstAdulto.dat > firsAdultoOrd.dat
sort -k 3 -r firstCatole.dat > firsCatoleOrd.dat
sort -k 3 -r firstCentro.dat > firsCentroOrd.dat
sort -k 3 -r firstLiberdade.dat > firsLiberdadeOrd.dat
sort -k 3 -r firstNotCatole.dat > firsNotCatoleOrd.dat
sort -k 3 -r firstNotCentro.dat > firsNotCentroOrd.dat
sort -k 3 -r firstNotLiberdade.dat > firsNotLiberdadeOrd.dat

#Ordenando pelo valor médio
sort -k 3 -r allMedia.dat > allMediaOrd.dat
sort -k 3 -r allBaixa.dat > allBaixaOrd.dat
sort -k 3 -r allSolteiro.dat > allSolteiroOrd.dat
sort -k 3 -r allCasado.dat > allCasadoOrd.dat
sort -k 3 -r allFeminino.dat > allFemininoOrd.dat
sort -k 3 -r allMasculino.dat > allMasculinoOrd.dat
sort -k 3 -r allJovem.dat > allJovemOrd.dat
sort -k 3 -r allAdulto.dat > allAdultoOrd.dat
sort -k 3 -r allCatole.dat > allCatoleOrd.dat
sort -k 3 -r allCentro.dat > allCentroOrd.dat
sort -k 3 -r allLiberdade.dat > allLiberdadeOrd.dat
sort -k 3 -r allNotCatole.dat > allNotCatoleOrd.dat
sort -k 3 -r allNotCentro.dat > allNotCentroOrd.dat
sort -k 3 -r allNotLiberdade.dat > allNotLiberdadeOrd.dat

#Calculating Moran I (falta revisar)
python extractLatLongStreet.py first_vote.dat > newFirst.dat
./processInputLatLong.sh newFirst.dat
rm newFirst.dat

grep "agrad%C3%A1vel?" streetsQScoresLatLong.dat > streetsQScoresLatLongAgra.dat
grep "seguro?" streetsQScoresLatLong.dat > streetsQScoresLatLongSeg.dat

Rscript krippMoran.R moran streetsQScoresLatLongAgra.dat streetsQScoresLatLongSeg.dat > moran.dat

#TODO Adicionar krippMoran por grupo!

#Encontra interseccao entre qscores gerados
python encontraInterseccao.py firsBaixaOrd.dat firsMediaOrd.dat > intersectionBaixaMedia.dat 
python encontraInterseccao.py firsSolteiroOrd.dat firsCasadoOrd.dat > intersectionSolteiroCasado.dat
python encontraInterseccao.py firsFemininoOrd.dat firsMasculinoOrd.dat > intersectionFemininoMasculino.dat
python encontraInterseccao.py firsJovemOrd.dat firsAdultoOrd.dat > intersectionJovemAdulto.dat
python encontraInterseccao.py firsCentroOrd.dat firsNotCentroOrd.dat > intersectionCentro.dat
python encontraInterseccao.py firsLiberdadeOrd.dat firsNotLiberdadeOrd.dat > intersectionLiberdade.dat
python encontraInterseccao.py firsCatoleOrd.dat firsNotCatoleOrd.dat > intersectionCatole.dat

python encontraInterseccao.py allBaixaOrd.dat allMediaOrd.dat > intersectionAllBaixaMedia.dat 
python encontraInterseccao.py allSolteiroOrd.dat allCasadoOrd.dat > intersectionAllSolteiroCasado.dat
python encontraInterseccao.py allFemininoOrd.dat allMasculinoOrd.dat > intersectionAllFemininoMasculino.dat
python encontraInterseccao.py allJovemOrd.dat allAdultoOrd.dat > intersectionAllJovemAdulto.dat
python encontraInterseccao.py allCentroOrd.dat allNotCentroOrd.dat > intersectionAllCentro.dat
python encontraInterseccao.py allLiberdadeOrd.dat allNotLiberdadeOrd.dat > intersectionAllLiberdade.dat
python encontraInterseccao.py allCatoleOrd.dat allNotCatoleOrd.dat > intersectionAllCatole.dat

#Prepara paginas html e arquivos de interseccao ordenados (revisar a partir daqui)
mkdir rankings
python preparaHTML.py first_vote_ordenado.dat

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

python preparaHTML.py firsCentroOrd.dat intersectionCentro.dat > firsCentroOrdInter.dat 
grep "centro" firsCentroOrdInter.dat > tmp.dat
mv tmp.dat firsCentroOrdInter.dat
mv question.html questionCentro.html
python preparaHTML.py firsNotCentroOrd.dat intersectionCentro.dat > firsNotCentroOrdInter.dat 
grep "centro" firsNotCentroOrdInter.dat > tmp.dat
mv tmp.dat firsNotCentroOrdInter.dat
mv question.html questionNotCentro.html

python preparaHTML.py firsCatoleOrd.dat intersectionCatole.dat > firsCatoleOrdInter.dat 
grep "catole" firsCatoleOrdInter.dat > tmp.dat
mv tmp.dat firsCatoleOrdInter.dat
mv question.html questionCatole.html
python preparaHTML.py firsNotCatoleOrd.dat intersectionCatole.dat > firsNotCatoleOrdInter.dat 
grep "catole" firsNotCatoleOrdInter.dat > tmp.dat
mv tmp.dat firsNotCatoleOrdInter.dat
mv question.html questionNotCatole.html

python preparaHTML.py firsLiberdadeOrd.dat intersectionLiberdade.dat > firsLiberdadeOrdInter.dat 
grep "liberdade" firsLiberdadeOrdInter.dat > tmp.dat
mv tmp.dat firsLiberdadeOrdInter.dat
mv question.html questionLiberdade.html
python preparaHTML.py firsNotLiberdadeOrd.dat intersectionLiberdade.dat > firsNotLiberdadeOrdInter.dat
grep "liberdade" firsNotLiberdadeOrdInter.dat > tmp.dat
mv tmp.dat firsNotLiberdadeOrdInter.dat 
mv question.html questionNotLiberdade.html

#Considerando todos os votos (qscore médio)
python preparaHTML.py allJovemOrd.dat intersectionAllJovemAdulto.dat > allJovemOrdInter.dat 
mv question.html questionAllJovem.html
python preparaHTML.py allAdultoOrd.dat intersectionAllJovemAdulto.dat > allAdultoOrdInter.dat 
mv question.html questionAllAdulto.html

python preparaHTML.py allMediaOrd.dat intersectionAllBaixaMedia.dat > allMediaOrdInter.dat 
mv question.html questionAllMedia.html
python preparaHTML.py allBaixaOrd.dat intersectionAllBaixaMedia.dat > allBaixaOrdInter.dat 
mv question.html questionAllBaixa.html

python preparaHTML.py allFemininoOrd.dat intersectionAllFemininoMasculino.dat > allFemininoOrdInter.dat 
mv question.html questionAllFeminino.html
python preparaHTML.py allMasculinoOrd.dat intersectionAllFemininoMasculino.dat > allMasculinoOrdInter.dat 
mv question.html questionAllMasculino.html

python preparaHTML.py allCasadoOrd.dat intersectionAllSolteiroCasado.dat > allCasadoOrdInter.dat 
mv question.html questionAllCasado.html
python preparaHTML.py allSolteiroOrd.dat intersectionAllSolteiroCasado.dat > allSolteiroOrdInter.dat 
mv question.html questionAllSolteiro.html

python preparaHTML.py allCentroOrd.dat intersectionAllCentro.dat > allCentroOrdInter.dat 
grep "centro" allCentroOrdInter.dat > tmp.dat
mv tmp.dat allCentroOrdInter.dat
mv question.html questionAllCentro.html
python preparaHTML.py firsNotCentroOrd.dat intersectionAllCentro.dat > allNotCentroOrdInter.dat 
grep "centro" allNotCentroOrdInter.dat > tmp.dat
mv tmp.dat allNotCentroOrdInter.dat
mv question.html questionAllNotCentro.html

python preparaHTML.py allCatoleOrd.dat intersectionAllCatole.dat > allCatoleOrdInter.dat 
grep "catole" allCatoleOrdInter.dat > tmp.dat
mv tmp.dat allCatoleOrdInter.dat
mv question.html questionAllCatole.html
python preparaHTML.py allNotCatoleOrd.dat intersectionAllCatole.dat > allNotCatoleOrdInter.dat 
grep "catole" allNotCatoleOrdInter.dat > tmp.dat
mv tmp.dat allNotCatoleOrdInter.dat
mv question.html questionAllNotCatole.html

python preparaHTML.py allLiberdadeOrd.dat intersectionAllLiberdade.dat > allLiberdadeOrdInter.dat 
grep "liberdade" allLiberdadeOrdInter.dat > tmp.dat
mv tmp.dat allLiberdadeOrdInter.dat
mv question.html questionAllLiberdade.html
python preparaHTML.py allNotLiberdadeOrd.dat intersectionAllLiberdade.dat > allNotLiberdadeOrdInter.dat
grep "liberdade" allNotLiberdadeOrdInter.dat > tmp.dat
mv tmp.dat allNotLiberdadeOrdInter.dat 
mv question.html questionAllNotLiberdade.html

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

python combinaRGBQScoreLinhas.py rgb.dat firsLiberdadeOrdInter.dat lines.dat
mv rgbQScoreAgrad.dat rgbQScoreAgradLiberdade.dat
mv rgbQScoreSeg.dat rgbQScoreSegLiberdade.dat
python combinaRGBQScoreLinhas.py rgb.dat firsNotLiberdadeOrdInter.dat lines.dat
mv rgbQScoreAgrad.dat rgbQScoreAgradNotLiberdade.dat
mv rgbQScoreSeg.dat rgbQScoreSegNotLiberdade.dat

python combinaRGBQScoreLinhas.py rgb.dat firsCentroOrdInter.dat lines.dat
mv rgbQScoreAgrad.dat rgbQScoreAgradCentro.dat
mv rgbQScoreSeg.dat rgbQScoreSegCentro.dat
python combinaRGBQScoreLinhas.py rgb.dat firsNotCentroOrdInter.dat lines.dat
mv rgbQScoreAgrad.dat rgbQScoreAgradNotCentro.dat
mv rgbQScoreSeg.dat rgbQScoreSegNotCentro.dat

python combinaRGBQScoreLinhas.py rgb.dat firsCatoleOrdInter.dat lines.dat
mv rgbQScoreAgrad.dat rgbQScoreAgradCatole.dat
mv rgbQScoreSeg.dat rgbQScoreSegCatole.dat
python combinaRGBQScoreLinhas.py rgb.dat firsNotCatoleOrdInter.dat lines.dat
mv rgbQScoreAgrad.dat rgbQScoreAgradNotCatole.dat
mv rgbQScoreSeg.dat rgbQScoreSegNotCatole.dat

#Considerando todos os votos (qscore médio)
python combinaRGBQScoreLinhas.py rgb.dat allAdultoOrdInter.dat lines.dat
mv rgbQScoreAgrad.dat rgbQScoreAgradAllAdulto.dat
mv rgbQScoreSeg.dat rgbQScoreSegAllAdulto.dat
python combinaRGBQScoreLinhas.py rgb.dat allJovemOrdInter.dat lines.dat
mv rgbQScoreAgrad.dat rgbQScoreAgradAllJovem.dat
mv rgbQScoreSeg.dat rgbQScoreSegAllJovem.dat

python combinaRGBQScoreLinhas.py rgb.dat allMediaOrdInter.dat lines.dat
mv rgbQScoreAgrad.dat rgbQScoreAgradAllMedia.dat
mv rgbQScoreSeg.dat rgbQScoreSegAllMedia.dat
python combinaRGBQScoreLinhas.py rgb.dat allBaixaOrdInter.dat lines.dat
mv rgbQScoreAgrad.dat rgbQScoreAgradAllBaixa.dat
mv rgbQScoreSeg.dat rgbQScoreSegAllBaixa.dat

python combinaRGBQScoreLinhas.py rgb.dat allFemininoOrdInter.dat lines.dat
mv rgbQScoreAgrad.dat rgbQScoreAgradAllFeminino.dat
mv rgbQScoreSeg.dat rgbQScoreSegAllFeminino.dat
python combinaRGBQScoreLinhas.py rgb.dat allMasculinoOrdInter.dat lines.dat
mv rgbQScoreAgrad.dat rgbQScoreAgradAllMasculino.dat
mv rgbQScoreSeg.dat rgbQScoreSegAllMasculino.dat

python combinaRGBQScoreLinhas.py rgb.dat allCasadoOrdInter.dat lines.dat
mv rgbQScoreAgrad.dat rgbQScoreAgradAllCasado.dat
mv rgbQScoreSeg.dat rgbQScoreSegAllCasado.dat
python combinaRGBQScoreLinhas.py rgb.dat allSolteiroOrdInter.dat lines.dat
mv rgbQScoreAgrad.dat rgbQScoreAgradAllSolteiro.dat
mv rgbQScoreSeg.dat rgbQScoreSegAllSolteiro.dat

python combinaRGBQScoreLinhas.py rgb.dat allCentroOrdInter.dat lines.dat
mv rgbQScoreAgrad.dat rgbQScoreAgradAllCentro.dat
mv rgbQScoreSeg.dat rgbQScoreSegAllCentro.dat
python combinaRGBQScoreLinhas.py rgb.dat allNotCentroOrdInter.dat lines.dat
mv rgbQScoreAgrad.dat rgbQScoreAgradAllNotCentro.dat
mv rgbQScoreSeg.dat rgbQScoreSegAllNotCentro.dat

python combinaRGBQScoreLinhas.py rgb.dat allLiberdadeOrdInter.dat lines.dat
mv rgbQScoreAgrad.dat rgbQScoreAgradAllLiberdade.dat
mv rgbQScoreSeg.dat rgbQScoreSegAllLiberdade.dat
python combinaRGBQScoreLinhas.py rgb.dat allNotLiberdadeOrdInter.dat lines.dat
mv rgbQScoreAgrad.dat rgbQScoreAgradAllNotLiberdade.dat
mv rgbQScoreSeg.dat rgbQScoreSegAllNotLiberdade.dat

python combinaRGBQScoreLinhas.py rgb.dat allCatoleOrdInter.dat lines.dat
mv rgbQScoreAgrad.dat rgbQScoreAgradAllCatole.dat
mv rgbQScoreSeg.dat rgbQScoreSegAllCatole.dat
python combinaRGBQScoreLinhas.py rgb.dat allNotCatoleOrdInter.dat lines.dat
mv rgbQScoreAgrad.dat rgbQScoreAgradAllNotCatole.dat
mv rgbQScoreSeg.dat rgbQScoreSegAllNotCatole.dat

#Analisa Correlacao
Rscript analisaCorrelacao.R rgbQScoreAgradMedia.dat rgbQScoreSegMedia.dat > correlacaoMedia.dat
Rscript analisaCorrelacao.R rgbQScoreAgradBaixa.dat rgbQScoreSegBaixa.dat > correlacaoBaixa.dat
Rscript analisaCorrelacao.R rgbQScoreAgradSolteiro.dat rgbQScoreSegSolteiro.dat > correlacaoSolteiro.dat
Rscript analisaCorrelacao.R rgbQScoreAgradCasado.dat rgbQScoreSegCasado.dat > correlacaoCasado.dat
Rscript analisaCorrelacao.R rgbQScoreAgradJovem.dat rgbQScoreSegJovem.dat > correlacaoJovem.dat
Rscript analisaCorrelacao.R rgbQScoreAgradAdulto.dat rgbQScoreSegAdulto.dat > correlacaoAdulto.dat
Rscript analisaCorrelacao.R rgbQScoreAgradFeminino.dat rgbQScoreSegFeminino.dat > correlacaoFeminino.dat
Rscript analisaCorrelacao.R rgbQScoreAgradMasculino.dat rgbQScoreSegMasculino.dat > correlacaoMasculino.dat

#TODO adicionar conhecer bairros e arquivos com all

mv *.pdf correlacao*.dat correlacao/

#Analisa Regressao

Rscript analisaRegressao.R rgbQScoreAgradMedia.dat rgbQScoreSegMedia.dat > regressaoMedia.dat
Rscript analisaRegressao.R rgbQScoreAgradBaixa.dat rgbQScoreSegBaixa.dat > regressaoBaixa.dat
Rscript analisaRegressao.R rgbQScoreAgradSolteiro.dat rgbQScoreSegSolteiro.dat > regressaoSolteiro.dat
Rscript analisaRegressao.R rgbQScoreAgradCasado.dat rgbQScoreSegCasado.dat > regressaoCasado.dat
Rscript analisaRegressao.R rgbQScoreAgradJovem.dat rgbQScoreSegJovem.dat > regressaoJovem.dat
Rscript analisaRegressao.R rgbQScoreAgradAdulto.dat rgbQScoreSegAdulto.dat > regressaoAdulto.dat
Rscript analisaRegressao.R rgbQScoreAgradFeminino.dat rgbQScoreSegFeminino.dat > regressaoFeminino.dat
Rscript analisaRegressao.R rgbQScoreAgradMasculino.dat rgbQScoreSegMasculino.dat > regressaoMasculino.dat

#TODO adicionar conhecer bairros e arquivos com all

mv *.pdf regressao*.dat correlacao/

#Calcula ICs por ponto para cada grupo
Rscript analisaICPorFoto.R allSolteiroOrdInter.dat allCasadoOrdInter.dat solteiro casado
#head -n 1 teste1.txt > allICSolteiroCentro.dat
#head -n 1 teste1.txt > allICSolteiroLib.dat
#head -n 1 teste1.txt > allICSolteiroCat.dat
#grep "centro" teste1.txt >> allICSolteiroCentro.dat
#grep "liberdade" teste1.txt >> allICSolteiroLib.dat
#grep "catole" teste1.txt >> allICSolteiroCat.dat
#head -n 1 teste2.txt > allICCasadoCentro.dat
#head -n 1 teste2.txt > allICCasadoLib.dat
#head -n 1 teste2.txt > allICCasadoCat.dat
#grep "centro" teste2.txt >> allICCasadoCentro.dat
#grep "liberdade" teste2.txt >> allICCasadoLib.dat
#grep "catole" teste2.txt >> allICCasadoCat.dat
mv teste1.txt allICSolteiro.dat
mv teste2.txt allICCasado.dat
Rscript analisaICPorFoto.R allBaixaOrdInter.dat allMediaOrdInter.dat baixa media
#head -n 1 teste1.txt > allICBaixaCentro.dat
#head -n 1 teste1.txt > allICBaixaLib.dat
#head -n 1 teste1.txt > allICBaixaCat.dat
#grep "centro" teste1.txt >> allICBaixaCentro.dat
#grep "liberdade" teste1.txt >> allICBaixaLib.dat
#grep "catole" teste1.txt >> allICBaixaCat.dat
#head -n 1 teste2.txt > allICMediaCentro.dat
#head -n 1 teste2.txt > allICMediaLib.dat
#head -n 1 teste2.txt > allICMediaCat.dat
#grep "centro" teste2.txt >> allICMediaCentro.dat
#grep "liberdade" teste2.txt >> allICMediaLib.dat
#grep "catole" teste2.txt >> allICMediaCat.dat
mv teste1.txt allICBaixa.dat
mv teste2.txt allICMedia.dat
Rscript analisaICPorFoto.R allFemininoOrdInter.dat allMasculinoOrdInter.dat feminino masculino
#head -n 1 teste1.txt > allICFemininoCentro.dat
#head -n 1 teste1.txt > allICFemininoLib.dat
#head -n 1 teste1.txt > allICFemininoCat.dat
#grep "centro" teste1.txt >> allICFemininoCentro.dat
#grep "liberdade" teste1.txt >> allICFemininoLib.dat
#grep "catole" teste1.txt >> allICFemininoCat.dat
#head -n 1 teste2.txt > allICMasculinoCentro.dat
#head -n 1 teste2.txt > allICMasculinoLib.dat
#head -n 1 teste2.txt > allICMasculinoCat.dat
#grep "centro" teste2.txt >> allICMasculinoCentro.dat
#grep "liberdade" teste2.txt >> allICMasculinoLib.dat
#grep "catole" teste2.txt >> allICMasculinoCat.dat
mv teste1.txt allICFeminino.dat
mv teste2.txt allICMasculino.dat
Rscript analisaICPorFoto.R allAdultoOrdInter.dat allJovemOrdInter.dat adulto jovem
#head -n 1 teste1.txt > allICAdultoCentro.dat
#head -n 1 teste1.txt > allICAdultoLib.dat
#head -n 1 teste1.txt > allICAdultoCat.dat
#grep "centro" teste1.txt >> allICAdultoCentro.dat
#grep "liberdade" teste1.txt >> allICAdultoLib.dat
#grep "catole" teste1.txt >> allICAdultoCat.dat
#head -n 1 teste2.txt > allICJovemCentro.dat
#head -n 1 teste2.txt > allICJovemLib.dat
#head -n 1 teste2.txt > allICJovemCat.dat
#grep "centro" teste2.txt >> allICJovemCentro.dat
#grep "liberdade" teste2.txt >> allICJovemLib.dat
#grep "catole" teste2.txt >> allICJovemCat.dat
mv teste1.txt allICAdulto.dat
mv teste2.txt allICJovem.dat

#Krippendorfs alpha for general data (falta revisar)
python preparaConsenso.py usersInfo.dat

Rscript krippMoran.R kripp consenseMatrixAgra.dat consenseMatrixSeg.dat > kripp.dat

#Kripp por grupo
python preparaConsenso.py usersInfo.dat adulto.dat
mv consenseMatrixAgra.dat consenseMatrixAgraAdulto.dat
mv consenseMatrixSeg.dat consenseMatrixSegAdulto.dat
echo "Adulto" >> krippAll.dat
Rscript krippMoran.R kripp consenseMatrixAgraAdulto.dat consenseMatrixSegAdulto.dat >> krippAll.dat

python preparaConsenso.py usersInfo.dat jovem.dat
mv consenseMatrixAgra.dat consenseMatrixAgraJovem.dat
mv consenseMatrixSeg.dat consenseMatrixSegJovem.dat
echo "Jovem" >> krippAll.dat
Rscript krippMoran.R kripp consenseMatrixAgraJovem.dat consenseMatrixSegJovem.dat >> krippAll.dat

python preparaConsenso.py usersInfo.dat jovem.dat adulto.dat
mv consenseMatrixAgra.dat consenseMatrixAgraJovemAdulto.dat
mv consenseMatrixSeg.dat consenseMatrixSegJovemAdulto.dat
echo "Jovem e Adulto" >> krippAll.dat
Rscript krippMoran.R kripp consenseMatrixAgraJovemAdulto.dat consenseMatrixSegJovemAdulto.dat >> krippAll.dat



python preparaConsenso.py usersInfo.dat casado.dat
mv consenseMatrixAgra.dat consenseMatrixAgraCasado.dat
mv consenseMatrixSeg.dat consenseMatrixSegCasado.dat
echo "Casado" >> krippAll.dat
Rscript krippMoran.R kripp consenseMatrixAgraCasado.dat consenseMatrixSegCasado.dat >> krippAll.dat

python preparaConsenso.py usersInfo.dat solteiro.dat
mv consenseMatrixAgra.dat consenseMatrixAgraSolteiro.dat
mv consenseMatrixSeg.dat consenseMatrixSegSolteiro.dat
echo "Solteiro" >> krippAll.dat
Rscript krippMoran.R kripp consenseMatrixAgraSolteiro.dat consenseMatrixSegSolteiro.dat >> krippAll.dat

python preparaConsenso.py usersInfo.dat casado.dat solteiro.dat
mv consenseMatrixAgra.dat consenseMatrixAgraCasadoSolteiro.dat
mv consenseMatrixSeg.dat consenseMatrixSegCasadoSolteiro.dat
echo "CAsado e Solteiro" >> krippAll.dat
Rscript krippMoran.R kripp consenseMatrixAgraCasadoSolteiro.dat consenseMatrixSegCasadoSolteiro.dat >> krippAll.dat


python preparaConsenso.py usersInfo.dat baixa.dat
mv consenseMatrixAgra.dat consenseMatrixAgraBaixa.dat
mv consenseMatrixSeg.dat consenseMatrixSegBaixa.dat
echo "Baixa" >> krippAll.dat
Rscript krippMoran.R kripp consenseMatrixAgraBaixa.dat consenseMatrixSegBaixa.dat >> krippAll.dat

python preparaConsenso.py usersInfo.dat media.dat
mv consenseMatrixAgra.dat consenseMatrixAgraMedia.dat
mv consenseMatrixSeg.dat consenseMatrixSegMedia.dat
echo "Media" >> krippAll.dat
Rscript krippMoran.R kripp consenseMatrixAgraMedia.dat consenseMatrixSegMedia.dat >> krippAll.dat

python preparaConsenso.py usersInfo.dat baixa.dat media.dat
mv consenseMatrixAgra.dat consenseMatrixAgraBaixaMedia.dat
mv consenseMatrixSeg.dat consenseMatrixSegBaixaMedia.dat
echo "Baixa e Media" >> krippAll.dat
Rscript krippMoran.R kripp consenseMatrixAgraBaixaMedia.dat consenseMatrixSegBaixaMedia.dat >> krippAll.dat


python preparaConsenso.py usersInfo.dat feminino.dat
mv consenseMatrixAgra.dat consenseMatrixAgraFeminino.dat
mv consenseMatrixSeg.dat consenseMatrixSegFeminino.dat
echo "Feminino" >> krippAll.dat
Rscript krippMoran.R kripp consenseMatrixAgraFeminino.dat consenseMatrixSegFeminino.dat >> krippAll.dat

python preparaConsenso.py usersInfo.dat media.dat
mv consenseMatrixAgra.dat consenseMatrixAgraMasculino.dat
mv consenseMatrixSeg.dat consenseMatrixSegMasculino.dat
echo "Masculino" >> krippAll.dat
Rscript krippMoran.R kripp consenseMatrixAgraMasculino.dat consenseMatrixSegMasculino.dat >> krippAll.dat

python preparaConsenso.py usersInfo.dat feminino.dat masculino.dat
mv consenseMatrixAgra.dat consenseMatrixAgraFemininoMasculino.dat
mv consenseMatrixSeg.dat consenseMatrixSegFemininoMasculino.dat
echo "Feminino e Masculino" >> krippAll.dat
Rscript krippMoran.R kripp consenseMatrixAgraFemininoMasculino.dat consenseMatrixSegFemininoMasculino.dat >> krippAll.dat


mkdir consense 
mv consenseMatrix*.dat krippAll.dat kripp.dat consense
mv alta.dat baixa.dat adulto.dat jovem.dat solteiro.dat casado.dat feminino.dat masculino.dat catole.dat centro.dat liberdade.dat notcentro.dat notliberdade.dat notcatole.dat idsGrupos 

#Kendall tau distance
rm -f kendall.dat

grep "agrad" first_vote_ordenado.dat > agradGeral.dat #General ranking data
grep "seg" first_vote_ordenado.dat > segGeral.dat

#Casados e Solteiros
echo " Cas x Solteiro Agrad" >> kendall.dat
grep "agrad" firsCasadoOrdInter.dat > ranking1.dat
grep "agrad" firsSolteiroOrdInter.dat > ranking2.dat
Rscript kendallDistance.R ranking1.dat ranking2.dat >> kendall.dat 

echo " Cas x Solteiro Agrad" >> kendallAll.dat
grep "agrad" allCasadoOrdInter.dat > ranking1.dat
grep "agrad" allSolteiroOrdInter.dat > ranking2.dat
Rscript kendallDistance.R ranking1.dat ranking2.dat >> kendallAll.dat

#Selecting photos from general ranking that were considered in current rankings
echo " Cas x Geral Agrad" >> kendall.dat
awk '{print $2}' ranking1.dat > temp.dat
rm -f ranking3.dat
while read photo ; do 
	grep $photo agradGeral.dat >> ranking3.dat
done < temp.dat
sort -k 3 -r ranking3.dat > ranking3Ord.dat 
Rscript kendallDistance.R ranking1.dat ranking3Ord.dat >> kendall.dat
echo " Sol x Geral Agrad" >> kendall.dat
Rscript kendallDistance.R ranking2.dat ranking3Ord.dat >> kendall.dat

echo " Cas x Solteiro Seg" >> kendall.dat
grep "seg" firsCasadoOrdInter.dat > ranking1.dat
grep "seg" firsSolteiroOrdInter.dat > ranking2.dat
Rscript kendallDistance.R ranking1.dat ranking2.dat >> kendall.dat 

echo " Cas x Solteiro Seg" >> kendallAll.dat
grep "seg" allCasadoOrdInter.dat > ranking1.dat
grep "seg" allSolteiroOrdInter.dat > ranking2.dat
Rscript kendallDistance.R ranking1.dat ranking2.dat >> kendallAll.dat

echo " Cas x Geral Seg" >> kendall.dat
awk '{print $2}' ranking1.dat > temp.dat
rm ranking3.dat
while read photo ; do 
	grep $photo segGeral.dat >> ranking3.dat
done < temp.dat
sort -k 3 -r ranking3.dat > ranking3Ord.dat 
Rscript kendallDistance.R ranking1.dat ranking3Ord.dat >> kendall.dat
echo " Sol x Geral Seg" >> kendall.dat
Rscript kendallDistance.R ranking2.dat ranking3Ord.dat >> kendall.dat


#Baixa e Media
echo " Baixa x Media Agrad" >> kendall.dat
grep "agrad" firsBaixaOrdInter.dat > ranking1.dat
grep "agrad" firsMediaOrdInter.dat > ranking2.dat
Rscript kendallDistance.R ranking1.dat ranking2.dat >> kendall.dat 

echo " Baixa x Media Agrad" >> kendallAll.dat
grep "agrad" allBaixaOrdInter.dat > ranking1.dat
grep "agrad" allMediaOrdInter.dat > ranking2.dat
Rscript kendallDistance.R ranking1.dat ranking2.dat >> kendallAll.dat

echo " Baixa x Geral Agrad" >> kendall.dat
awk '{print $2}' ranking1.dat > temp.dat
rm ranking3.dat
while read photo ; do 
	grep $photo agradGeral.dat >> ranking3.dat
done < temp.dat
sort -k 3 -r ranking3.dat > ranking3Ord.dat 
Rscript kendallDistance.R ranking1.dat ranking3Ord.dat >> kendall.dat
echo " Media x Geral Agrad" >> kendall.dat
Rscript kendallDistance.R ranking2.dat ranking3Ord.dat >> kendall.dat

echo " Baixa x Media Seg" >> kendall.dat
grep "seg" firsBaixaOrdInter.dat > ranking1.dat
grep "seg" firsMediaOrdInter.dat > ranking2.dat
Rscript kendallDistance.R ranking1.dat ranking2.dat >> kendall.dat

echo " Baixa x Media Agrad" >> kendallAll.dat
grep "seg" allBaixaOrdInter.dat > ranking1.dat
grep "seg" allMediaOrdInter.dat > ranking2.dat
Rscript kendallDistance.R ranking1.dat ranking2.dat >> kendallAll.dat

echo " Baixa x Geral Seg" >> kendall.dat
awk '{print $2}' ranking1.dat > temp.dat
rm ranking3.dat
while read photo ; do 
	grep $photo segGeral.dat >> ranking3.dat
done < temp.dat
sort -k 3 -r ranking3.dat > ranking3Ord.dat 
Rscript kendallDistance.R ranking1.dat ranking3Ord.dat >> kendall.dat
echo " Media x Geral Seg" >> kendall.dat
Rscript kendallDistance.R ranking2.dat ranking3Ord.dat >> kendall.dat

#Fem e Masc
echo " Fem x Masc Agrad" >> kendall.dat
grep "agrad" firsFemininoOrdInter.dat > ranking1.dat
grep "agrad" firsMasculinoOrdInter.dat > ranking2.dat
Rscript kendallDistance.R ranking1.dat ranking2.dat >> kendall.dat 

echo " Fem x Masc Agrad" >> kendallAll.dat
grep "agrad" allFemininoOrdInter.dat > ranking1.dat
grep "agrad" allMasculinoOrdInter.dat > ranking2.dat
Rscript kendallDistance.R ranking1.dat ranking2.dat >> kendallAll.dat

echo " Fem x Geral Agrad" >> kendall.dat
awk '{print $2}' ranking1.dat > temp.dat
rm ranking3.dat
while read photo ; do 
	grep $photo agradGeral.dat >> ranking3.dat
done < temp.dat
sort -k 3 -r ranking3.dat > ranking3Ord.dat 
Rscript kendallDistance.R ranking1.dat ranking3Ord.dat >> kendall.dat
echo " Masc x Geral Agrad" >> kendall.dat
Rscript kendallDistance.R ranking2.dat ranking3Ord.dat >> kendall.dat

echo " Fem x Masc Seg" >> kendall.dat
grep "seg" firsFemininoOrdInter.dat > ranking1.dat
grep "seg" firsMasculinoOrdInter.dat > ranking2.dat
Rscript kendallDistance.R ranking1.dat ranking2.dat >> kendall.dat

echo " Fem x Masc Seg" >> kendallAll.dat
grep "seg" allFemininoOrdInter.dat > ranking1.dat
grep "seg" allMasculinoOrdInter.dat > ranking2.dat
Rscript kendallDistance.R ranking1.dat ranking2.dat >> kendallAll.dat

echo " Fem x Geral Seg" >> kendall.dat
awk '{print $2}' ranking1.dat > temp.dat
rm ranking3.dat
while read photo ; do 
	grep $photo segGeral.dat >> ranking3.dat
done < temp.dat
sort -k 3 -r ranking3.dat > ranking3Ord.dat 
Rscript kendallDistance.R ranking1.dat ranking3Ord.dat >> kendall.dat
echo " Masc x Geral Seg" >> kendall.dat
Rscript kendallDistance.R ranking2.dat ranking3Ord.dat >> kendall.dat

#Jovem e Adulto
echo " Jov x Adu Agrad" >> kendall.dat
grep "agrad" firsJovemOrdInter.dat > ranking1.dat
grep "agrad" firsAdultoOrdInter.dat > ranking2.dat
Rscript kendallDistance.R ranking1.dat ranking2.dat >> kendall.dat 

echo " Jovem x Adulto Agrad" >> kendallAll.dat
grep "agrad" allJovemOrdInter.dat > ranking1.dat
grep "agrad" allAdultoOrdInter.dat > ranking2.dat
Rscript kendallDistance.R ranking1.dat ranking2.dat >> kendallAll.dat

echo " Jovem x Geral Agrad" >> kendall.dat
awk '{print $2}' ranking1.dat > temp.dat
rm ranking3.dat
while read photo ; do 
	grep $photo agradGeral.dat >> ranking3.dat
done < temp.dat
sort -k 3 -r ranking3.dat > ranking3Ord.dat 
Rscript kendallDistance.R ranking1.dat ranking3Ord.dat >> kendall.dat
echo " Adulto x Geral Agrad" >> kendall.dat
Rscript kendallDistance.R ranking2.dat ranking3Ord.dat >> kendall.dat

echo " Jov x Adu Seg" >> kendall.dat
grep "seg" firsJovemOrdInter.dat > ranking1.dat
grep "seg" firsAdultoOrdInter.dat > ranking2.dat
Rscript kendallDistance.R ranking1.dat ranking2.dat >> kendall.dat

echo " Jovem x Adulto Seg" >> kendallAll.dat
grep "seg" allJovemOrdInter.dat > ranking1.dat
grep "seg" allAdultoOrdInter.dat > ranking2.dat
Rscript kendallDistance.R ranking1.dat ranking2.dat >> kendallAll.dat

echo " Jovem x Geral Seg" >> kendall.dat
awk '{print $2}' ranking1.dat > temp.dat
rm ranking3.dat
while read photo ; do 
	grep $photo segGeral.dat >> ranking3.dat
done < temp.dat
sort -k 3 -r ranking3.dat > ranking3Ord.dat 
Rscript kendallDistance.R ranking1.dat ranking3Ord.dat >> kendall.dat
echo " Adulto x Geral Seg" >> kendall.dat
Rscript kendallDistance.R ranking2.dat ranking3Ord.dat >> kendall.dat

#Centro e Not Centro
echo " Centro x Not Centro Agrad" >> kendall.dat
grep "agrad" firsCentroOrdInter.dat > ranking1.dat
grep "agrad" firsNotCentroOrdInter.dat > ranking2.dat
Rscript kendallDistance.R ranking1.dat ranking2.dat >> kendall.dat 

echo " Centro x Not Centro Agrad" >> kendallAll.dat
grep "agrad" allCentroOrdInter.dat > ranking1.dat
grep "agrad" allNotCentroOrdInter.dat > ranking2.dat
Rscript kendallDistance.R ranking1.dat ranking2.dat >> kendallAll.dat

echo " Centro x Not Centro Seg" >> kendall.dat
grep "seg" firsCentroOrdInter.dat > ranking1.dat
grep "seg" firsNotCentroOrdInter.dat > ranking2.dat
Rscript kendallDistance.R ranking1.dat ranking2.dat >> kendall.dat

echo " Centro x Not Centro Seg" >> kendallAll.dat
grep "seg" allCentroOrdInter.dat > ranking1.dat
grep "seg" allNotCentroOrdInter.dat > ranking2.dat
Rscript kendallDistance.R ranking1.dat ranking2.dat >> kendallAll.dat

#Catole e Not Catole
echo " Catole x Not Catole Agrad" >> kendall.dat
grep "agrad" firsCatoleOrdInter.dat > ranking1.dat
grep "agrad" firsNotCatoleOrdInter.dat > ranking2.dat
Rscript kendallDistance.R ranking1.dat ranking2.dat >> kendall.dat 

echo " Catole x Not Catole Agrad" >> kendallAll.dat
grep "agrad" allCatoleOrdInter.dat > ranking1.dat
grep "agrad" allNotCatoleOrdInter.dat > ranking2.dat
Rscript kendallDistance.R ranking1.dat ranking2.dat >> kendallAll.dat

echo " Catole x Not Catole Seg" >> kendall.dat
grep "seg" firsCatoleOrdInter.dat > ranking1.dat
grep "seg" firsNotCatoleOrdInter.dat > ranking2.dat
Rscript kendallDistance.R ranking1.dat ranking2.dat >> kendall.dat

echo " Catole x Not Catole Seg" >> kendallAll.dat
grep "seg" allCatoleOrdInter.dat > ranking1.dat
grep "seg" allNotCatoleOrdInter.dat > ranking2.dat
Rscript kendallDistance.R ranking1.dat ranking2.dat >> kendallAll.dat

#Liberdade e Not Liberdade
echo " Liberdade x Not Liberdade Agrad" >> kendall.dat
grep "agrad" firsLiberdadeOrdInter.dat > ranking1.dat
grep "agrad" firsNotLiberdadeOrdInter.dat > ranking2.dat
Rscript kendallDistance.R ranking1.dat ranking2.dat >> kendall.dat

echo " Liberdade x Not Liberdade Agra" >> kendallAll.dat
grep "agrad" allLiberdadeOrdInter.dat > ranking1.dat
grep "agrad" allNotLiberdadeOrdInter.dat > ranking2.dat
Rscript kendallDistance.R ranking1.dat ranking2.dat >> kendallAll.dat 

echo " Liberdade x Not Liberdade Agrad" >> kendall.dat
grep "seg" firsLiberdadeOrdInter.dat > ranking1.dat
grep "seg" firsNotLiberdadeOrdInter.dat > ranking2.dat
Rscript kendallDistance.R ranking1.dat ranking2.dat >> kendall.dat

echo " Liberdade x Not Liberdade Seg" >> kendallAll.dat
grep "seg" allLiberdadeOrdInter.dat > ranking1.dat
grep "seg" allNotLiberdadeOrdInter.dat > ranking2.dat
Rscript kendallDistance.R ranking1.dat ranking2.dat >> kendallAll.dat 

rm ranking1.dat ranking2.dat ranking3.dat ranking3Ord.dat temp.dat agradGeral.dat segGeral.dat 
mv kendall*.dat correlacao/

#Analisa QScore por Bairro (adicionar All)
rm -f bairro.dat

echo ">>>>>>>> Geral" >> bairro.dat
python analisaQScorePorBairro.py first_vote_ordenado.dat > temp.dat
grep "catole" temp.dat | grep "agra" > catole.dat
grep "centro" temp.dat | grep "agra" > centro.dat
grep "liberdade" temp.dat | grep "agra" > liberdade.dat
echo "Agra Cat x Centro" >> bairro.dat
Rscript  calculaTTest.R catole.dat centro.dat "Catole Agra Ger" "Centro Agra Ger" "green">> bairro.dat
echo "Agra Lib x Centro" >> bairro.dat
Rscript  calculaTTest.R liberdade.dat centro.dat "Liberdade Agra Ger" "Centro Agra Ger" "green" >> bairro.dat
echo "Agra Cat x Liberdade" >> bairro.dat
Rscript  calculaTTest.R catole.dat liberdade.dat "Catole Agra Ger" "Liberdade Agra Ger" "green" >> bairro.dat

grep "catole" temp.dat | grep "seg" > catole.dat
grep "centro" temp.dat | grep "seg" > centro.dat
grep "liberdade" temp.dat | grep "seg" > liberdade.dat
echo "Seg Cat x Centro" >> bairro.dat
Rscript  calculaTTest.R catole.dat centro.dat "Catole Seg Ger" "Centro Seg Ger" "red" >> bairro.dat
echo "Seg Lib x Centro" >> bairro.dat 
Rscript  calculaTTest.R liberdade.dat centro.dat "Liberdade Seg Ger" "Centro Seg Ger" "red" >> bairro.dat
echo "Seg Cat x Liberdade" >> bairro.dat
Rscript  calculaTTest.R catole.dat liberdade.dat "Catole Seg Ger" "Liberdade Seg Ger" "red" >> bairro.dat

echo ">>>>>>>> Jovem" >> bairro.dat
python analisaQScorePorBairro.py firsJovemOrdInter.dat > temp.dat
grep "catole" temp.dat | grep "agra" > catole.dat
grep "centro" temp.dat | grep "agra" > centro.dat
grep "liberdade" temp.dat | grep "agra" > liberdade.dat
echo "Agra Cat x Centro" >> bairro.dat
Rscript  calculaTTest.R catole.dat centro.dat "Catole Agra Jov" "Centro Agra Jov" "green">> bairro.dat
echo "Agra Lib x Centro" >> bairro.dat
Rscript  calculaTTest.R liberdade.dat centro.dat "Liberdade Agra Jov" "Centro Agra Jov" "green" >> bairro.dat
echo "Agra Cat x Liberdade" >> bairro.dat
Rscript  calculaTTest.R catole.dat liberdade.dat "Catole Agra Jov" "Liberdade Agra Jov" "green" >> bairro.dat

grep "catole" temp.dat | grep "seg" > catole.dat
grep "centro" temp.dat | grep "seg" > centro.dat
grep "liberdade" temp.dat | grep "seg" > liberdade.dat
echo "Seg Cat x Centro" >> bairro.dat
Rscript  calculaTTest.R catole.dat centro.dat "Catole Seg Jov" "Centro Seg Jov" "red" >> bairro.dat
echo "Seg Lib x Centro" >> bairro.dat 
Rscript  calculaTTest.R liberdade.dat centro.dat "Liberdade Seg Jov" "Centro Seg Jov" "red" >> bairro.dat
echo "Seg Cat x Liberdade" >> bairro.dat
Rscript  calculaTTest.R catole.dat liberdade.dat "Catole Seg Jov" "Liberdade Seg Jov" "red" >> bairro.dat



echo ">>>>>>> Adulto" >> bairro.dat
python analisaQScorePorBairro.py firsAdultoOrdInter.dat > temp.dat
grep "catole" temp.dat | grep "agra" > catole.dat
grep "centro" temp.dat | grep "agra" > centro.dat
grep "liberdade" temp.dat | grep "agra" > liberdade.dat
echo "Agra Cat x Centro" >> bairro.dat
Rscript  calculaTTest.R catole.dat centro.dat "Catole Agra Adu" "Centro Agra Adu" "green">> bairro.dat
echo "Agra Lib x Centro" >> bairro.dat
Rscript  calculaTTest.R liberdade.dat centro.dat "Liberdade Agra Adu" "Centro Agra Adu" "green" >> bairro.dat
echo "Agra Cat x Liberdade" >> bairro.dat
Rscript  calculaTTest.R catole.dat liberdade.dat "Catole Agra Adu" "Liberdade Agra Adu" "green" >> bairro.dat

grep "catole" temp.dat | grep "seg" > catole.dat
grep "centro" temp.dat | grep "seg" > centro.dat
grep "liberdade" temp.dat | grep "seg" > liberdade.dat
echo "Seg Cat x Centro" >> bairro.dat
Rscript  calculaTTest.R catole.dat centro.dat "Catole Seg Adu" "Centro Seg Adu" "red" >> bairro.dat
echo "Seg Lib x Centro" >> bairro.dat 
Rscript  calculaTTest.R liberdade.dat centro.dat "Liberdade Seg" "Centro Seg Adu" "red" >> bairro.dat
echo "Seg Cat x Liberdade" >> bairro.dat
Rscript  calculaTTest.R catole.dat liberdade.dat "Catole Seg Adu" "Liberdade Seg Adu" "red" >> bairro.dat


echo ">>>>>>>>>> Baixa" >> bairro.dat
python analisaQScorePorBairro.py firsBaixaOrdInter.dat > temp.dat
grep "catole" temp.dat | grep "agra" > catole.dat
grep "centro" temp.dat | grep "agra" > centro.dat
grep "liberdade" temp.dat | grep "agra" > liberdade.dat
echo "Agra Cat x Centro" >> bairro.dat
Rscript  calculaTTest.R catole.dat centro.dat "Catole Agra Bai" "Centro Agra Bai" "green">> bairro.dat
echo "Agra Lib x Centro" >> bairro.dat
Rscript  calculaTTest.R liberdade.dat centro.dat "Liberdade Agra Bai" "Centro Agra Bai" "green" >> bairro.dat
echo "Agra Cat x Liberdade" >> bairro.dat
Rscript  calculaTTest.R catole.dat liberdade.dat "Catole Agra Bai" "Liberdade Agra Bai" "green" >> bairro.dat

grep "catole" temp.dat | grep "seg" > catole.dat
grep "centro" temp.dat | grep "seg" > centro.dat
grep "liberdade" temp.dat | grep "seg" > liberdade.dat
echo "Seg Cat x Centro" >> bairro.dat
Rscript  calculaTTest.R catole.dat centro.dat "Catole Seg Bai" "Centro Seg Bai" "red" >> bairro.dat
echo "Seg Lib x Centro" >> bairro.dat 
Rscript  calculaTTest.R liberdade.dat centro.dat "Liberdade Seg Bai" "Centro Seg Bai" "red" >> bairro.dat
echo "Seg Cat x Liberdade" >> bairro.dat
Rscript  calculaTTest.R catole.dat liberdade.dat "Catole Seg Bai" "Liberdade Seg Bai" "red" >> bairro.dat



echo ">>>>>>>>>> Media" >> bairro.dat
python analisaQScorePorBairro.py firsMediaOrdInter.dat > temp.dat
grep "catole" temp.dat | grep "agra" > catole.dat
grep "centro" temp.dat | grep "agra" > centro.dat
grep "liberdade" temp.dat | grep "agra" > liberdade.dat
echo "Agra Cat x Centro" >> bairro.dat
Rscript  calculaTTest.R catole.dat centro.dat "Catole Agra Med" "Centro Agra Med" "green">> bairro.dat
echo "Agra Lib x Centro" >> bairro.dat
Rscript  calculaTTest.R liberdade.dat centro.dat "Liberdade Agra Med" "Centro Agra Med" "green" >> bairro.dat
echo "Agra Cat x Liberdade" >> bairro.dat
Rscript  calculaTTest.R catole.dat liberdade.dat "Catole Agra Med" "Liberdade Agra Med" "green" >> bairro.dat

grep "catole" temp.dat | grep "seg" > catole.dat
grep "centro" temp.dat | grep "seg" > centro.dat
grep "liberdade" temp.dat | grep "seg" > liberdade.dat
echo "Seg Cat x Centro" >> bairro.dat
Rscript  calculaTTest.R catole.dat centro.dat "Catole Seg Med" "Centro Seg Med" "red" >> bairro.dat
echo "Seg Lib x Centro" >> bairro.dat 
Rscript  calculaTTest.R liberdade.dat centro.dat "Liberdade Seg Med" "Centro Seg Med" "red" >> bairro.dat
echo "Seg Cat x Liberdade" >> bairro.dat
Rscript  calculaTTest.R catole.dat liberdade.dat "Catole Seg Med" "Liberdade Seg Med" "red" >> bairro.dat




echo ">>>>>>>>>> Fem" >> bairro.dat
python analisaQScorePorBairro.py firsFemininoOrdInter.dat > temp.dat
grep "catole" temp.dat | grep "agra" > catole.dat
grep "centro" temp.dat | grep "agra" > centro.dat
grep "liberdade" temp.dat | grep "agra" > liberdade.dat
echo "Agra Cat x Centro" >> bairro.dat
Rscript  calculaTTest.R catole.dat centro.dat "Catole Agra Fem" "Centro Agra Fem" "green">> bairro.dat
echo "Agra Lib x Centro" >> bairro.dat
Rscript  calculaTTest.R liberdade.dat centro.dat "Liberdade Agra Fem" "Centro Agra Fem" "green" >> bairro.dat
echo "Agra Cat x Liberdade" >> bairro.dat
Rscript  calculaTTest.R catole.dat liberdade.dat "Catole Agra Fem" "Liberdade Agra Fem" "green" >> bairro.dat

grep "catole" temp.dat | grep "seg" > catole.dat
grep "centro" temp.dat | grep "seg" > centro.dat
grep "liberdade" temp.dat | grep "seg" > liberdade.dat
echo "Seg Cat x Centro" >> bairro.dat
Rscript  calculaTTest.R catole.dat centro.dat "Catole Seg Fem" "Centro Seg Fem" "red" >> bairro.dat
echo "Seg Lib x Centro" >> bairro.dat 
Rscript  calculaTTest.R liberdade.dat centro.dat "Liberdade Seg Fem" "Centro Seg Fem" "red" >> bairro.dat
echo "Seg Cat x Liberdade" >> bairro.dat
Rscript  calculaTTest.R catole.dat liberdade.dat "Catole Seg Fem" "Liberdade Seg Fem" "red" >> bairro.dat




echo ">>>>>>>>> Masc" >> bairro.dat
python analisaQScorePorBairro.py firsMasculinoOrdInter.dat > temp.dat
grep "catole" temp.dat | grep "agra" > catole.dat
grep "centro" temp.dat | grep "agra" > centro.dat
grep "liberdade" temp.dat | grep "agra" > liberdade.dat
echo "Agra Cat x Centro" >> bairro.dat
Rscript  calculaTTest.R catole.dat centro.dat "Catole Agra Mas" "Centro Agra Mas" "green">> bairro.dat
echo "Agra Lib x Centro" >> bairro.dat
Rscript  calculaTTest.R liberdade.dat centro.dat "Liberdade Agra Mas" "Centro Agra Mas" "green" >> bairro.dat
echo "Agra Cat x Liberdade" >> bairro.dat
Rscript  calculaTTest.R catole.dat liberdade.dat "Catole Agra Mas" "Liberdade Agra Mas" "green" >> bairro.dat

grep "catole" temp.dat | grep "seg" > catole.dat
grep "centro" temp.dat | grep "seg" > centro.dat
grep "liberdade" temp.dat | grep "seg" > liberdade.dat
echo "Seg Cat x Centro" >> bairro.dat
Rscript  calculaTTest.R catole.dat centro.dat "Catole Seg Mas" "Centro Seg Mas" "red" >> bairro.dat
echo "Seg Lib x Centro" >> bairro.dat 
Rscript  calculaTTest.R liberdade.dat centro.dat "Liberdade Seg Mas" "Centro Seg Mas" "red" >> bairro.dat
echo "Seg Cat x Liberdade" >> bairro.dat
Rscript  calculaTTest.R catole.dat liberdade.dat "Catole Seg Mas" "Liberdade Seg Mas" "red" >> bairro.dat




echo ">>>>>>>>>>>> Casado" >> bairro.dat
python analisaQScorePorBairro.py firsCasadoOrdInter.dat > temp.dat
grep "catole" temp.dat | grep "agra" > catole.dat
grep "centro" temp.dat | grep "agra" > centro.dat
grep "liberdade" temp.dat | grep "agra" > liberdade.dat
echo "Agra Cat x Centro" >> bairro.dat
Rscript  calculaTTest.R catole.dat centro.dat "Catole Agra Cas" "Centro Agra Cas" "green">> bairro.dat
echo "Agra Lib x Centro" >> bairro.dat
Rscript  calculaTTest.R liberdade.dat centro.dat "Liberdade Agra Cas" "Centro Agra Cas" "green" >> bairro.dat
echo "Agra Cat x Liberdade" >> bairro.dat
Rscript  calculaTTest.R catole.dat liberdade.dat "Catole Agra Cas" "Liberdade Agra Cas" "green" >> bairro.dat

grep "catole" temp.dat | grep "seg" > catole.dat
grep "centro" temp.dat | grep "seg" > centro.dat
grep "liberdade" temp.dat | grep "seg" > liberdade.dat
echo "Seg Cat x Centro" >> bairro.dat
Rscript  calculaTTest.R catole.dat centro.dat "Catole Seg Cas" "Centro Seg Cas" "red" >> bairro.dat
echo "Seg Lib x Centro" >> bairro.dat 
Rscript  calculaTTest.R liberdade.dat centro.dat "Liberdade Seg Cas" "Centro Seg Cas" "red" >> bairro.dat
echo "Seg Cat x Liberdade" >> bairro.dat
Rscript  calculaTTest.R catole.dat liberdade.dat "Catole Seg Cas" "Liberdade Seg Cas" "red" >> bairro.dat




echo ">>>>>>>>>>>>>> Solteiro" >> bairro.dat
python analisaQScorePorBairro.py firsSolteiroOrdInter.dat > temp.dat
grep "catole" temp.dat | grep "agra" > catole.dat
grep "centro" temp.dat | grep "agra" > centro.dat
grep "liberdade" temp.dat | grep "agra" > liberdade.dat
echo "Agra Cat x Centro" >> bairro.dat
Rscript  calculaTTest.R catole.dat centro.dat "Catole Agra Sol" "Centro Agra Sol" "green">> bairro.dat
echo "Agra Lib x Centro" >> bairro.dat
Rscript  calculaTTest.R liberdade.dat centro.dat "Liberdade Agra Sol" "Centro Agra Sol" "green" >> bairro.dat
echo "Agra Cat x Liberdade" >> bairro.dat
Rscript  calculaTTest.R catole.dat liberdade.dat "Catole Agra Sol" "Liberdade Agra Sol" "green" >> bairro.dat

grep "catole" temp.dat | grep "seg" > catole.dat
grep "centro" temp.dat | grep "seg" > centro.dat
grep "liberdade" temp.dat | grep "seg" > liberdade.dat
echo "Seg Cat x Centro" >> bairro.dat
Rscript  calculaTTest.R catole.dat centro.dat "Catole Seg Sol" "Centro Seg Sol" "red" >> bairro.dat
echo "Seg Lib x Centro" >> bairro.dat 
Rscript  calculaTTest.R liberdade.dat centro.dat "Liberdade Seg Sol" "Centro Seg Sol" "red" >> bairro.dat
echo "Seg Cat x Liberdade" >> bairro.dat
Rscript  calculaTTest.R catole.dat liberdade.dat "Catole Seg Sol" "Liberdade Seg Sol" "red" >> bairro.dat


echo ">>>>>>>>>>>>>> Conhece" >> bairro.dat
python analisaQScorePorBairro.py firsCentroOrdInter.dat > temp.dat
python analisaQScorePorBairro.py firsCatoleOrdInter.dat >> temp.dat
python analisaQScorePorBairro.py firsLiberdadeOrdInter.dat >> temp.dat
grep "catole" temp.dat | grep "agra" > catole.dat
grep "centro" temp.dat | grep "agra" > centro.dat
grep "liberdade" temp.dat | grep "agra" > liberdade.dat
echo "Agra Cat x Centro" >> bairro.dat
Rscript  calculaTTest.R catole.dat centro.dat "Catole Agra Sol" "Centro Agra Sol" "green">> bairro.dat
echo "Agra Lib x Centro" >> bairro.dat
Rscript  calculaTTest.R liberdade.dat centro.dat "Liberdade Agra Sol" "Centro Agra Sol" "green" >> bairro.dat
echo "Agra Cat x Liberdade" >> bairro.dat
Rscript  calculaTTest.R catole.dat liberdade.dat "Catole Agra Sol" "Liberdade Agra Sol" "green" >> bairro.dat

echo ">>>>>>>>>>>>>> Não Conhece" >> bairro.dat
python analisaQScorePorBairro.py firsNotCentroOrdInter.dat > temp.dat
python analisaQScorePorBairro.py firsNotCatoleOrdInter.dat >> temp.dat
python analisaQScorePorBairro.py firsNotLiberdadeOrdInter.dat >> temp.dat
grep "catole" temp.dat | grep "agra" > catole.dat
grep "centro" temp.dat | grep "agra" > centro.dat
grep "liberdade" temp.dat | grep "agra" > liberdade.dat
echo "Agra Cat x Centro" >> bairro.dat
Rscript  calculaTTest.R catole.dat centro.dat "Catole Agra Sol" "Centro Agra Sol" "green">> bairro.dat
echo "Agra Lib x Centro" >> bairro.dat
Rscript  calculaTTest.R liberdade.dat centro.dat "Liberdade Agra Sol" "Centro Agra Sol" "green" >> bairro.dat
echo "Agra Cat x Liberdade" >> bairro.dat
Rscript  calculaTTest.R catole.dat liberdade.dat "Catole Agra Sol" "Liberdade Agra Sol" "green" >> bairro.dat

rm temp.dat liberdade.dat catole.dat centro.dat


