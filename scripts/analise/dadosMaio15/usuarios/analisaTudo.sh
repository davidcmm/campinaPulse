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
python selectRunPerUsers.py run.csv medio.dat > runMedio.csv
python selectRunPerUsers.py run.csv posgrad.dat > runPos.csv

python selectRunPerUsers.py run.csv catole.dat > runCatole.csv
python selectRunPerUsers.py run.csv centro.dat > runCentro.csv
python selectRunPerUsers.py run.csv liberdade.dat > runLiberdade.csv
python selectRunPerUsers.py run.csv notcatole.dat > runNotCatole.csv
python selectRunPerUsers.py run.csv notcentro.dat > runNotCentro.csv
python selectRunPerUsers.py run.csv notliberdade.dat > runNotLiberdade.csv

mv alta.dat baixa.dat adulto.dat jovem.dat solteiro.dat casado.dat feminino.dat masculino.dat medio.dat posgrad.dat catole.dat centro.dat liberdade.dat notcentro.dat notliberdade.dat notcatole.dat idsGrupos 

#Analisa QScores
python analisaQScore.py run.csv
mv first.dat first_vote.dat

python analisaQScore.py runAdulto.csv 100
mv first.dat firstAdulto.dat
mv all.dat allAdulto.dat
python analisaQScore.py runJovem.csv 100
mv first.dat firstJovem.dat
mv all.dat allJovem.dat
python analisaQScore.py runSolteiro.csv 100
mv first.dat firstSolteiro.dat
mv all.dat allSolteiro.dat
python analisaQScore.py runCasado.csv 100
mv first.dat firstCasado.dat
mv all.dat allCasado.dat
python analisaQScore.py runMedia.csv 100
mv first.dat firstMedia.dat
mv all.dat allMedia.dat
python analisaQScore.py runBaixa.csv 100
mv first.dat firstBaixa.dat
mv all.dat allBaixa.dat
python analisaQScore.py runFeminino.csv 100 
mv first.dat firstFeminino.dat
mv all.dat allFeminino.dat
python analisaQScore.py runMasculino.csv 100
mv first.dat firstMasculino.dat
mv all.dat allMasculino.dat
python analisaQScore.py runMedio.csv 100
mv first.dat firstMedio.dat
mv all.dat allMedio.dat
python analisaQScore.py runPos.csv 100
mv first.dat firstPos.dat
mv all.dat allPos.dat

python analisaQScore.py runCatole.csv 100
mv first.dat firstCatole.dat
mv all.dat allCatole.dat
python analisaQScore.py runCentro.csv 100
mv first.dat firstCentro.dat
mv all.dat allCentro.dat
python analisaQScore.py runLiberdade.csv 100
mv first.dat firstLiberdade.dat
mv all.dat allLiberdade.dat
python analisaQScore.py runNotCatole.csv 100
mv first.dat firstNotCatole.dat
mv all.dat allNotCatole.dat
python analisaQScore.py runNotCentro.csv 100
mv first.dat firstNotCentro.dat
mv all.dat allNotCentro.dat
python analisaQScore.py runNotLiberdade.csv 100
mv first.dat firstNotLiberdade.dat
mv all.dat allNotLiberdade.dat

sort -k 3 -r first_vote.dat > first_vote_ordenado.dat
sort -k 3 -r all.dat > all_ordenado.dat

sort -k 3 -r firstMedia.dat > firsMediaOrd.dat
sort -k 3 -r firstBaixa.dat > firsBaixaOrd.dat
sort -k 3 -r firstSolteiro.dat > firsSolteiroOrd.dat
sort -k 3 -r firstCasado.dat > firsCasadoOrd.dat
sort -k 3 -r firstFeminino.dat > firsFemininoOrd.dat
sort -k 3 -r firstMasculino.dat > firsMasculinoOrd.dat
sort -k 3 -r firstJovem.dat > firsJovemOrd.dat
sort -k 3 -r firstAdulto.dat > firsAdultoOrd.dat
sort -k 3 -r firstMedio.dat > firsMedioOrd.dat
sort -k 3 -r firstPost.dat > firsPosOrd.dat

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
sort -k 3 -r allMedio.dat > allMedioOrd.dat
sort -k 3 -r allPos.dat > allPosOrd.dat

sort -k 3 -r allCatole.dat > allCatoleOrd.dat
sort -k 3 -r allCentro.dat > allCentroOrd.dat
sort -k 3 -r allLiberdade.dat > allLiberdadeOrd.dat
sort -k 3 -r allNotCatole.dat > allNotCatoleOrd.dat
sort -k 3 -r allNotCentro.dat > allNotCentroOrd.dat
sort -k 3 -r allNotLiberdade.dat > allNotLiberdadeOrd.dat

#Calculating Moran I Geral(falta revisar)
./processInputLatLong.sh first_vote.dat
mv streetsQScoresLatLong.dat streetsQScoresLatLongFirst.dat
grep "agrad%C3%A1vel?" streetsQScoresLatLong.dat > streetsQScoresLatLongAgra.dat
grep "seguro?" streetsQScoresLatLong.dat > streetsQScoresLatLongSeg.dat
Rscript krippMoran.R moran streetsQScoresLatLongAgra.dat streetsQScoresLatLongSeg.dat > moran.dat

./processInputLatLong.sh all.dat
mv streetsQScoresLatLong.dat streetsQScoresLatLongAll.dat
grep "agrad%C3%A1vel?" streetsQScoresLatLongAll.dat > streetsQScoresLatLongAgraAll.dat
grep "seguro?" streetsQScoresLatLongAll.dat > streetsQScoresLatLongSegAll.dat
Rscript krippMoran.R moran streetsQScoresLatLongAgraAll.dat streetsQScoresLatLongSegAll.dat > moranAll.dat

#Por grupo
./processInputLatLong.sh allAdulto.dat
mv streetsQScoresLatLong.dat streetsQScoresLatLongAllAdulto.dat
grep "agrad%C3%A1vel?" streetsQScoresLatLongAllAdulto.dat > streetsQScoresLatLongAgraAllAdulto.dat
grep "seguro?" streetsQScoresLatLongAllAdulto.dat > streetsQScoresLatLongSegAllAdulto.dat
echo "Adulto" >> moranAll.dat
Rscript krippMoran.R moran streetsQScoresLatLongAgraAllAdulto.dat streetsQScoresLatLongSegAllAdulto.dat >> moranAll.dat


./processInputLatLong.sh allJovem.dat
mv streetsQScoresLatLong.dat streetsQScoresLatLongAllJovem.dat
grep "agrad%C3%A1vel?" streetsQScoresLatLongAllJovem.dat > streetsQScoresLatLongAgraAllJovem.dat
grep "seguro?" streetsQScoresLatLongAllJovem.dat > streetsQScoresLatLongSegAllJovem.dat
echo "Jovem" >> moranAll.dat
Rscript krippMoran.R moran streetsQScoresLatLongAgraAllJovem.dat streetsQScoresLatLongSegAllJovem.dat >> moranAll.dat


./processInputLatLong.sh allFeminino.dat
mv streetsQScoresLatLong.dat streetsQScoresLatLongAllFeminino.dat
grep "agrad%C3%A1vel?" streetsQScoresLatLongAllFeminino.dat > streetsQScoresLatLongAgraAllFeminino.dat
grep "seguro?" streetsQScoresLatLongAllFeminino.dat > streetsQScoresLatLongSegAllFeminino.dat
echo "Feminino" >> moranAll.dat
Rscript krippMoran.R moran streetsQScoresLatLongAgraAllFeminino.dat streetsQScoresLatLongSegAllFeminino.dat >> moranAll.dat


./processInputLatLong.sh allMasculino.dat
mv streetsQScoresLatLong.dat streetsQScoresLatLongAllMasculino.dat
grep "agrad%C3%A1vel?" streetsQScoresLatLongAllMasculino.dat > streetsQScoresLatLongAgraAllMasculino.dat
grep "seguro?" streetsQScoresLatLongAllMasculino.dat > streetsQScoresLatLongSegAllMasculino.dat
echo "Masculino" >> moranAll.dat
Rscript krippMoran.R moran streetsQScoresLatLongAgraAllMasculino.dat streetsQScoresLatLongSegAllMasculino.dat >> moranAll.dat

./processInputLatLong.sh allCasado.dat
mv streetsQScoresLatLong.dat streetsQScoresLatLongAllCasado.dat
grep "agrad%C3%A1vel?" streetsQScoresLatLongAllCasado.dat > streetsQScoresLatLongAgraAllCasado.dat
grep "seguro?" streetsQScoresLatLongAllCasado.dat > streetsQScoresLatLongSegAllCasado.dat
echo "Casado" >> moranAll.dat
Rscript krippMoran.R moran streetsQScoresLatLongAgraAllCasado.dat streetsQScoresLatLongSegAllCasado.dat >> moranAll.dat


./processInputLatLong.sh allSolteiro.dat
mv streetsQScoresLatLong.dat streetsQScoresLatLongAllSolteiro.dat
grep "agrad%C3%A1vel?" streetsQScoresLatLongAllSolteiro.dat > streetsQScoresLatLongAgraAllSolteiro.dat
grep "seguro?" streetsQScoresLatLongAllSolteiro.dat > streetsQScoresLatLongSegAllSolteiro.dat
echo "Solteiro" >> moranAll.dat
Rscript krippMoran.R moran streetsQScoresLatLongAgraAllSolteiro.dat streetsQScoresLatLongSegAllSolteiro.dat >> moranAll.dat


./processInputLatLong.sh allBaixa.dat
mv streetsQScoresLatLong.dat streetsQScoresLatLongAllBaixa.dat
grep "agrad%C3%A1vel?" streetsQScoresLatLongAllBaixa.dat > streetsQScoresLatLongAgraAllBaixa.dat
grep "seguro?" streetsQScoresLatLongAllBaixa.dat > streetsQScoresLatLongSegAllBaixa.dat
echo "Baixa" >> moranAll.dat
Rscript krippMoran.R moran streetsQScoresLatLongAgraAllBaixa.dat streetsQScoresLatLongSegAllBaixa.dat >> moranAll.dat

./processInputLatLong.sh allMedia.dat
mv streetsQScoresLatLong.dat streetsQScoresLatLongAllMedia.dat
grep "agrad%C3%A1vel?" streetsQScoresLatLongAllMedia.dat > streetsQScoresLatLongAgraAllMedia.dat
grep "seguro?" streetsQScoresLatLongAllMedia.dat > streetsQScoresLatLongSegAllMedia.dat
echo "Media" >> moranAll.dat
Rscript krippMoran.R moran streetsQScoresLatLongAgraAllMedia.dat streetsQScoresLatLongSegAllMedia.dat >> moranAll.dat

./processInputLatLong.sh allMedio.dat
mv streetsQScoresLatLong.dat streetsQScoresLatLongAllMedio.dat
grep "agrad%C3%A1vel?" streetsQScoresLatLongAllMedio.dat > streetsQScoresLatLongAgraAllMedio.dat
grep "seguro?" streetsQScoresLatLongAllMedio.dat > streetsQScoresLatLongSegAllMedio.dat
echo "Medio" >> moranAll.dat
Rscript krippMoran.R moran streetsQScoresLatLongAgraAllMedio.dat streetsQScoresLatLongSegAllMedio.dat >> moranAll.dat

./processInputLatLong.sh allPos.dat
mv streetsQScoresLatLong.dat streetsQScoresLatLongAllPos.dat
grep "agrad%C3%A1vel?" streetsQScoresLatLongAllPos.dat > streetsQScoresLatLongAgraAllPos.dat
grep "seguro?" streetsQScoresLatLongAllPos.dat > streetsQScoresLatLongSegAllPos.dat
echo "Pos" >> moranAll.dat
Rscript krippMoran.R moran streetsQScoresLatLongAgraAllPos.dat streetsQScoresLatLongSegAllPos.dat >> moranAll.dat

mkdir moran100
mv streetsQScoresLatLongAll*.dat streetsQScoresLatLongAgraAll* streetsQScoresLatLongSegAll* moranAll.dat moran100/

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
python encontraInterseccao.py allMedioOrd.dat allPosOrd.dat > intersectionAllMedioPos.dat

python encontraInterseccao.py allCentroOrd.dat allNotCentroOrd.dat > intersectionAllCentro.dat
python encontraInterseccao.py allLiberdadeOrd.dat allNotLiberdadeOrd.dat > intersectionAllLiberdade.dat
python encontraInterseccao.py allCatoleOrd.dat allNotCatoleOrd.dat > intersectionAllCatole.dat

#Prepara paginas html e arquivos de interseccao ordenados (revisar a partir daqui)
python preparaHTML.py first_vote_ordenado.dat
python preparaHTML.py all_ordenado.dat

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

python preparaHTML.py allMedioOrd.dat intersectionAllMedioPos.dat > allMedioOrdInter.dat 
mv question.html questionAllMedio.html
python preparaHTML.py allPosOrd.dat intersectionAllMedioPos.dat > allPosOrdInter.dat 
mv question.html questionAllPos.html

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

mkdir rankings100
mv question*.html rankings100

#Combina RGB, #Linhas e criterios
python combinaRGBQScoreLinhas.py rgb.dat first_vote_ordenado.dat lines.dat
mv rgbQScoreAgrad.dat rgbQScoreAgradFirst.dat
mv rgbQScoreSeg.dat rgbQScoreSegFirst.dat

python combinaRGBQScoreLinhas.py rgb.dat all_ordenado.dat lines.dat
mv rgbQScoreAgrad.dat rgbQScoreAgradAll.dat
mv rgbQScoreSeg.dat rgbQScoreSegAll.dat

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

python combinaRGBQScoreLinhas.py rgb.dat allMedioOrdInter.dat lines.dat
mv rgbQScoreAgrad.dat rgbQScoreAgradAllMedio.dat
mv rgbQScoreSeg.dat rgbQScoreSegAllMedio.dat
python combinaRGBQScoreLinhas.py rgb.dat allPosOrdInter.dat lines.dat
mv rgbQScoreAgrad.dat rgbQScoreAgradAllPos.dat
mv rgbQScoreSeg.dat rgbQScoreSegAllPos.dat

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

mkdir inputCorrelacaoRegressao100
mv rgbQScore*.dat inputCorrelacaoRegressao100/

#Analisa Correlacao
Rscript analisaCorrelacao.R inputCorrelacaoRegressao100/rgbQScoreAgradAll.dat inputCorrelacaoRegressao100/rgbQScoreSegAll.dat > correlacaoAll.dat

Rscript analisaCorrelacao.R inputCorrelacaoRegressao100/rgbQScoreAgradAllMedia.dat inputCorrelacaoRegressao100/rgbQScoreSegMedia.dat > correlacaoMedia.dat
Rscript analisaCorrelacao.R inputCorrelacaoRegressao100/rgbQScoreAgradAllBaixa.dat inputCorrelacaoRegressao100/rgbQScoreSegBaixa.dat > correlacaoBaixa.dat
Rscript analisaCorrelacao.R inputCorrelacaoRegressao100/rgbQScoreAgradAllSolteiro.dat inputCorrelacaoRegressao100/rgbQScoreSegAllSolteiro.dat > correlacaoSolteiro.dat
Rscript analisaCorrelacao.R inputCorrelacaoRegressao100/rgbQScoreAgradAllCasado.dat inputCorrelacaoRegressao100/rgbQScoreSegAllCasado.dat > correlacaoCasado.dat
Rscript analisaCorrelacao.R inputCorrelacaoRegressao100/rgbQScoreAgradAllJovem.dat inputCorrelacaoRegressao100/rgbQScoreSegJovem.dat > correlacaoAllJovem.dat
Rscript analisaCorrelacao.R inputCorrelacaoRegressao100/rgbQScoreAgradAllAdulto.dat inputCorrelacaoRegressao100/rgbQScoreSegAllAdulto.dat > correlacaoAdulto.dat
Rscript analisaCorrelacao.R inputCorrelacaoRegressao100/rgbQScoreAgradAllFeminino.dat inputCorrelacaoRegressao100/rgbQScoreSegAllFeminino.dat > correlacaoFeminino.dat
Rscript analisaCorrelacao.R inputCorrelacaoRegressao100/rgbQScoreAgradAllMasculino.dat inputCorrelacaoRegressao100/rgbQScoreSegAllMasculino.dat > correlacaoMasculino.dat
Rscript analisaCorrelacao.R inputCorrelacaoRegressao100/rgbQScoreAgradAllMedio.dat inputCorrelacaoRegressao100/rgbQScoreSegAllMedio.dat > correlacaoMedio.dat
Rscript analisaCorrelacao.R inputCorrelacaoRegressao100/rgbQScoreAgradAllPos.dat inputCorrelacaoRegressao100/rgbQScoreSegAllPos.dat > correlacaoPos.dat

#TODO adicionar conhecer bairros e arquivos com all

mv *.pdf correlacao*.dat correlacao100/

#Analisa Regressao
Rscript analisaRegressao.R inputCorrelacaoRegressao100/rgbQScoreAgradAll.dat inputCorrelacaoRegressao100/rgbQScoreSegAll.dat > regressaoAll.dat

Rscript analisaRegressao.R inputCorrelacaoRegressao100/rgbQScoreAgradAllMedia.dat inputCorrelacaoRegressao100/rgbQScoreSegAllMedia.dat > regressaoMedia.dat
Rscript analisaRegressao.R inputCorrelacaoRegressao100/rgbQScoreAgradAllBaixa.dat inputCorrelacaoRegressao100/rgbQScoreSegAllBaixa.dat > regressaoBaixa.dat
Rscript analisaRegressao.R inputCorrelacaoRegressao100/rgbQScoreAgradAllSolteiro.dat inputCorrelacaoRegressao100/rgbQScoreSegAllSolteiro.dat > regressaoSolteiro.dat
Rscript analisaRegressao.R inputCorrelacaoRegressao100/rgbQScoreAgradAllCasado.dat inputCorrelacaoRegressao100/rgbQScoreSegAllCasado.dat > regressaoCasado.dat
Rscript analisaRegressao.R inputCorrelacaoRegressao100/rgbQScoreAgradAllJovem.dat inputCorrelacaoRegressao100/rgbQScoreSegAllJovem.dat > regressaoJovem.dat
Rscript analisaRegressao.R inputCorrelacaoRegressao100/rgbQScoreAgradAllAdulto.dat inputCorrelacaoRegressao100/rgbQScoreSegAllAdulto.dat > regressaoAdulto.dat
Rscript analisaRegressao.R inputCorrelacaoRegressao100/rgbQScoreAgradAllFeminino.dat inputCorrelacaoRegressao100/rgbQScoreSegAllFeminino.dat > regressaoFeminino.dat
Rscript analisaRegressao.R inputCorrelacaoRegressao100/rgbQScoreAgradAllMasculino.dat inputCorrelacaoRegressao100/rgbQScoreSegAllMasculino.dat > regressaoMasculino.dat
Rscript analisaRegressao.R inputCorrelacaoRegressao100/rgbQScoreAgradAllMedio.dat inputCorrelacaoRegressao100/rgbQScoreSegAllMedio.dat > regressaoMedio.dat
Rscript analisaRegressao.R inputCorrelacaoRegressao100/rgbQScoreAgradAllPos.dat inputCorrelacaoRegressao100/rgbQScoreSegAllPos.dat > regressaoPos.dat

#TODO adicionar conhecer bairros e arquivos com all

mv *.pdf regressao*.dat regressao100/

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

Rscript analisaICPorFoto.R allMedioOrdInter.dat allPosOrdInter.dat medio pos
mv teste1.txt allICMedio.dat
mv teste2.txt allICPos.dat

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

python preparaConsenso.py usersInfo.dat masculino.dat
mv consenseMatrixAgra.dat consenseMatrixAgraMasculino.dat
mv consenseMatrixSeg.dat consenseMatrixSegMasculino.dat
echo "Masculino" >> krippAll.dat
Rscript krippMoran.R kripp consenseMatrixAgraMasculino.dat consenseMatrixSegMasculino.dat >> krippAll.dat

python preparaConsenso.py usersInfo.dat feminino.dat masculino.dat
mv consenseMatrixAgra.dat consenseMatrixAgraFemininoMasculino.dat
mv consenseMatrixSeg.dat consenseMatrixSegFemininoMasculino.dat
echo "Feminino e Masculino" >> krippAll.dat
Rscript krippMoran.R kripp consenseMatrixAgraFemininoMasculino.dat consenseMatrixSegFemininoMasculino.dat >> krippAll.dat

python preparaConsenso.py usersInfo.dat medio.dat
mv consenseMatrixAgra.dat consenseMatrixAgraMedio.dat
mv consenseMatrixSeg.dat consenseMatrixSegMedio.dat
echo "Medio" >> krippAll.dat
Rscript krippMoran.R kripp consenseMatrixAgraMedio.dat consenseMatrixSegMedio.dat >> krippAll.dat

python preparaConsenso.py usersInfo.dat posgrad.dat
mv consenseMatrixAgra.dat consenseMatrixAgraPos.dat
mv consenseMatrixSeg.dat consenseMatrixSegPos.dat
echo "Pos" >> krippAll.dat
Rscript krippMoran.R kripp consenseMatrixAgraPos.dat consenseMatrixSegPos.dat >> krippAll.dat

python preparaConsenso.py usersInfo.dat medio.dat posgrad.dat
mv consenseMatrixAgra.dat consenseMatrixAgraMedioPos.dat
mv consenseMatrixSeg.dat consenseMatrixSegMedioPos.dat
echo "Medio e Pos" >> krippAll.dat
Rscript krippMoran.R kripp consenseMatrixAgraMedioPos.dat consenseMatrixSegMedioPos.dat >> krippAll.dat

mkdir consense100 
mv consenseMatrix*.dat krippAll.dat kripp.dat consense100
mv alta.dat baixa.dat adulto.dat jovem.dat solteiro.dat casado.dat feminino.dat masculino.dat catole.dat centro.dat liberdade.dat notcentro.dat notliberdade.dat notcatole.dat idsGrupos 

#Kendall tau distance
rm -f kendall.dat kendalAll.dat

#grep "agrad" first_vote_ordenado.dat > agradGeral.dat #General ranking data
#grep "seg" first_vote_ordenado.dat > segGeral.dat
grep "agrad" all_ordenado.dat > agradGeralAll.dat #General ranking data
grep "seg" all_ordenado.dat > segGeralAll.dat

#echo "First" > kendall.dat
#Rscript kendallDistance.R agradGeral.dat segGeral.dat >> kendall.dat 

echo "All" >> kendall.dat
Rscript kendallDistance.R agradGeralAll.dat segGeralAll.dat >> kendallAll.dat

#Casados e Solteiros
#echo " Cas x Solteiro Agrad" >> kendall.dat
#grep "agrad" firsCasadoOrdInter.dat > ranking1.dat
#grep "agrad" firsSolteiroOrdInter.dat > ranking2.dat
#Rscript kendallDistance.R ranking1.dat ranking2.dat >> kendall.dat 

echo " Cas x Solteiro Agrad" >> kendallAll.dat
grep "agrad" allCasadoOrdInter.dat > kendallAgradAllCasado.dat
grep "agrad" allSolteiroOrdInter.dat > kendallAgradAllSolteiro.dat
Rscript kendallDistance.R kendallAgradAllCasado.dat kendallAgradAllSolteiro.dat >> kendallAll.dat

#Selecting photos from general ranking that were considered in current rankings
#echo " Cas x Geral Agrad" >> kendall.dat
#awk '{print $2}' ranking1.dat > temp.dat
#rm -f ranking3.dat
#while read photo ; do 
#	grep $photo agradGeral.dat >> ranking3.dat
#done < temp.dat
#sort -k 3 -r ranking3.dat > ranking3Ord.dat 
#Rscript kendallDistance.R ranking1.dat ranking3Ord.dat >> kendall.dat
#echo " Sol x Geral Agrad" >> kendall.dat
#Rscript kendallDistance.R ranking2.dat ranking3Ord.dat >> kendall.dat

echo " Cas x Geral Agrad" >> kendallAll.dat
awk '{print $2}' kendallAgradAllCasado.dat > temp.dat
rm -f ranking3.dat
while read photo ; do 
	grep $photo agradGeralAll.dat >> ranking3.dat
done < temp.dat
sort -k 3 -r ranking3.dat > kendallAgradAllGeralCasado.dat 
Rscript kendallDistance.R kendallAgradAllCasado.dat kendallAgradAllGeralCasado.dat >> kendallAll.dat
echo " Sol x Geral Agrad" >> kendallAll.dat
Rscript kendallDistance.R kendallAgradAllSolteiro.dat kendallAgradAllGeralCasado.dat >> kendallAll.dat

#echo " Cas x Solteiro Seg" >> kendall.dat
#grep "seg" firsCasadoOrdInter.dat > ranking1.dat
#grep "seg" firsSolteiroOrdInter.dat > ranking2.dat
#Rscript kendallDistance.R ranking1.dat ranking2.dat >> kendall.dat 

echo " Cas x Solteiro Seg" >> kendallAll.dat
grep "seg" allCasadoOrdInter.dat > kendallSegAllCasado.dat
grep "seg" allSolteiroOrdInter.dat > kendallSegAllSolteiro.dat
Rscript kendallDistance.R kendallSegAllCasado.dat kendallSegAllSolteiro.dat >> kendallAll.dat

#echo " Cas x Geral Seg" >> kendall.dat
#awk '{print $2}' kendallSegAllCasado.dat > temp.dat
#rm ranking3.dat
#while read photo ; do 
#	grep $photo segGeral.dat >> ranking3.dat
#done < temp.dat
#sort -k 3 -r ranking3.dat > kendallSegAllGeralCasado.dat 
#Rscript kendallDistance.R ranking1.dat ranking3Ord.dat >> kendall.dat
#echo " Sol x Geral Seg" >> kendall.dat
#Rscript kendallDistance.R ranking2.dat ranking3Ord.dat >> kendall.dat

echo " Cas x Geral Seg" >> kendallAll.dat
awk '{print $2}' kendallSegAllCasado.dat > temp.dat
rm ranking3.dat
while read photo ; do 
	grep $photo segGeralAll.dat >> ranking3.dat
done < temp.dat
sort -k 3 -r ranking3.dat > kendallSegAllGeralCasado.dat 
Rscript kendallDistance.R kendallSegAllCasado.dat kendallSegAllGeralCasado.dat >> kendallAll.dat
echo " Sol x Geral Seg" >> kendallAll.dat
Rscript kendallDistance.R kendallSegAllSolteiro.dat kendallSegAllGeralCasado.dat >> kendallAll.dat


#Baixa e Media
#echo " Baixa x Media Agrad" >> kendall.dat
#grep "agrad" firsBaixaOrdInter.dat > ranking1.dat
#grep "agrad" firsMediaOrdInter.dat > ranking2.dat
#Rscript kendallDistance.R ranking1.dat ranking2.dat >> kendall.dat 

echo " Baixa x Media Agrad" >> kendallAll.dat
grep "agrad" allBaixaOrdInter.dat > kendallAgradAllBaixa.dat
grep "agrad" allMediaOrdInter.dat > kendallAgradAllMedia.dat
Rscript kendallDistance.R kendallAgradAllBaixa.dat kendallAgradAllMedia.dat >> kendallAll.dat

#echo " Baixa x Geral Agrad" >> kendall.dat
#awk '{print $2}' ranking1.dat > temp.dat
#rm ranking3.dat
#while read photo ; do 
#	grep $photo agradGeral.dat >> ranking3.dat
#done < temp.dat
#sort -k 3 -r ranking3.dat > ranking3Ord.dat 
#Rscript kendallDistance.R ranking1.dat ranking3Ord.dat >> kendall.dat
#echo " Media x Geral Agrad" >> kendall.dat
#Rscript kendallDistance.R ranking2.dat ranking3Ord.dat >> kendall.dat

echo " Baixa x Geral Agrad" >> kendallAll.dat
awk '{print $2}' kendallAgradAllBaixa.dat > temp.dat
rm ranking3.dat
while read photo ; do 
	grep $photo agradGeralAll.dat >> ranking3.dat
done < temp.dat
sort -k 3 -r ranking3.dat > kendallAgradAllGeralBaixa.dat 
Rscript kendallDistance.R kendallAgradAllBaixa.dat kendallAgradAllGeralBaixa.dat >> kendallAll.dat
echo " Media x Geral Agrad" >> kendallAll.dat
Rscript kendallDistance.R kendallAgradAllMedia.dat kendallAgradAllGeralBaixa.dat >> kendallAll.dat

#echo " Baixa x Media Seg" >> kendall.dat
#grep "seg" firsBaixaOrdInter.dat > ranking1.dat
#grep "seg" firsMediaOrdInter.dat > ranking2.dat
#Rscript kendallDistance.R ranking1.dat ranking2.dat >> kendall.dat

echo " Baixa x Media Agrad" >> kendallAll.dat
grep "seg" allBaixaOrdInter.dat > kendallSegAllBaixa.dat
grep "seg" allMediaOrdInter.dat > kendallSegAllMedia.dat
Rscript kendallDistance.R kendallSegAllBaixa.dat kendallSegAllMedia.dat >> kendallAll.dat

#echo " Baixa x Geral Seg" >> kendall.dat
#awk '{print $2}' ranking1.dat > temp.dat
#rm ranking3.dat
#while read photo ; do 
#	grep $photo segGeral.dat >> ranking3.dat
#done < temp.dat
#sort -k 3 -r ranking3.dat > ranking3Ord.dat 
#Rscript kendallDistance.R ranking1.dat ranking3Ord.dat >> kendall.dat
#echo " Media x Geral Seg" >> kendall.dat
#Rscript kendallDistance.R ranking2.dat ranking3Ord.dat >> kendall.dat

echo " Baixa x Geral Seg" >> kendallAll.dat
awk '{print $2}' kendallSegAllBaixa.dat > temp.dat
rm ranking3.dat
while read photo ; do 
	grep $photo segGeralAll.dat >> ranking3.dat
done < temp.dat
sort -k 3 -r ranking3.dat > kendallSegAllGeralBaixa.dat 
Rscript kendallDistance.R kendallSegAllBaixa.dat kendallSegAllGeralBaixa.dat >> kendallAll.dat
echo " Media x Geral Seg" >> kendallAll.dat
Rscript kendallDistance.R kendallSegAllMedia.dat kendallSegAllGeralBaixa.dat >> kendallAll.dat

#Fem e Masc
#echo " Fem x Masc Agrad" >> kendall.dat
#grep "agrad" firsFemininoOrdInter.dat > ranking1.dat
#grep "agrad" firsMasculinoOrdInter.dat > ranking2.dat
#Rscript kendallDistance.R ranking1.dat ranking2.dat >> kendall.dat 

echo " Fem x Masc Agrad" >> kendallAll.dat
grep "agrad" allFemininoOrdInter.dat > kendallAgradAllFeminino.dat
grep "agrad" allMasculinoOrdInter.dat > kendallAgradAllMasculino.dat
Rscript kendallDistance.R kendallAgradAllFeminino.dat kendallAgradAllMasculino.dat >> kendallAll.dat

#echo " Fem x Geral Agrad" >> kendall.dat
#awk '{print $2}' ranking1.dat > temp.dat
#rm ranking3.dat
#while read photo ; do 
#	grep $photo agradGeral.dat >> ranking3.dat
#done < temp.dat
#sort -k 3 -r ranking3.dat > ranking3Ord.dat 
#Rscript kendallDistance.R ranking1.dat ranking3Ord.dat >> kendall.dat
#echo " Masc x Geral Agrad" >> kendall.dat
#Rscript kendallDistance.R ranking2.dat ranking3Ord.dat >> kendall.dat

echo " Fem x Geral Agrad" >> kendallAll.dat
awk '{print $2}' kendallAgradAllFeminino.dat > temp.dat
rm ranking3.dat
while read photo ; do 
	grep $photo agradGeralAll.dat >> ranking3.dat
done < temp.dat
sort -k 3 -r ranking3.dat > kendallAgradAllGeralFeminino.dat 
Rscript kendallDistance.R kendallAgradAllFeminino.dat kendallAgradAllGeralFeminino.dat >> kendallAll.dat
echo " Masc x Geral Agrad" >> kendallAll.dat
Rscript kendallDistance.R kendallAgradAllMasculino.dat kendallAgradAllGeralFeminino.dat >> kendallAll.dat

#echo " Fem x Masc Seg" >> kendall.dat
#grep "seg" firsFemininoOrdInter.dat > ranking1.dat
#grep "seg" firsMasculinoOrdInter.dat > ranking2.dat
#Rscript kendallDistance.R ranking1.dat ranking2.dat >> kendall.dat

echo " Fem x Masc Seg" >> kendallAll.dat
grep "seg" allFemininoOrdInter.dat > kendallSegAllFeminino.dat
grep "seg" allMasculinoOrdInter.dat > kendallSegAllMasculino.dat
Rscript kendallDistance.R kendallSegAllFeminino.dat kendallSegAllMasculino.dat >> kendallAll.dat

#echo " Fem x Geral Seg" >> kendall.dat
#awk '{print $2}' ranking1.dat > temp.dat
#rm ranking3.dat
#while read photo ; do 
#	grep $photo segGeral.dat >> ranking3.dat
#done < temp.dat
#sort -k 3 -r ranking3.dat > ranking3Ord.dat 
#Rscript kendallDistance.R ranking1.dat ranking3Ord.dat >> kendall.dat
#echo " Masc x Geral Seg" >> kendall.dat
#Rscript kendallDistance.R ranking2.dat ranking3Ord.dat >> kendall.dat

echo " Fem x Geral Seg" >> kendallAll.dat
awk '{print $2}' kendallSegAllFeminino.dat > temp.dat
rm ranking3.dat
while read photo ; do 
	grep $photo segGeralAll.dat >> ranking3.dat
done < temp.dat
sort -k 3 -r ranking3.dat > kendallSegAllGeralFeminino.dat 
Rscript kendallDistance.R kendallSegAllFeminino.dat kendallSegAllGeralFeminino.dat >> kendallAll.dat
echo " Masc x Geral Seg" >> kendallAll.dat
Rscript kendallDistance.R kendallSegAllMasculino.dat kendallSegAllGeralFeminino.dat >> kendallAll.dat

#Jovem e Adulto
#echo " Jov x Adu Agrad" >> kendall.dat
#grep "agrad" firsJovemOrdInter.dat > ranking1.dat
#grep "agrad" firsAdultoOrdInter.dat > ranking2.dat
#Rscript kendallDistance.R ranking1.dat ranking2.dat >> kendall.dat 

echo " Jovem x Adulto Agrad" >> kendallAll.dat
grep "agrad" allJovemOrdInter.dat > kendallAgradAllJovem.dat
grep "agrad" allAdultoOrdInter.dat > kendallAgradAllAdulto.dat
Rscript kendallDistance.R kendallAgradAllJovem.dat kendallAgradAllAdulto.dat >> kendallAll.dat

#echo " Jovem x Geral Agrad" >> kendall.dat
#awk '{print $2}' ranking1.dat > temp.dat
#rm ranking3.dat
#while read photo ; do 
#	grep $photo agradGeral.dat >> ranking3.dat
#done < temp.dat
#sort -k 3 -r ranking3.dat > ranking3Ord.dat 
#Rscript kendallDistance.R ranking1.dat ranking3Ord.dat >> kendall.dat
#echo " Adulto x Geral Agrad" >> kendall.dat
#Rscript kendallDistance.R ranking2.dat ranking3Ord.dat >> kendall.dat

echo " Jovem x Geral Agrad" >> kendallAll.dat
awk '{print $2}' kendallAgradAllJovem.dat > temp.dat
rm ranking3.dat
while read photo ; do 
	grep $photo agradGeralAll.dat >> ranking3.dat
done < temp.dat
sort -k 3 -r ranking3.dat > kendallAgradAllGeralJovem.dat 
Rscript kendallDistance.R kendallAgradAllJovem.dat kendallAgradAllGeralJovem.dat >> kendallAll.dat
echo " Adulto x Geral Agrad" >> kendallAll.dat
Rscript kendallDistance.R kendallAgradAllAdulto.dat kendallAgradAllGeralJovem.dat >> kendallAll.dat

#echo " Jov x Adu Seg" >> kendall.dat
#grep "seg" firsJovemOrdInter.dat > ranking1.dat
#grep "seg" firsAdultoOrdInter.dat > ranking2.dat
#Rscript kendallDistance.R ranking1.dat ranking2.dat >> kendall.dat

echo " Jovem x Adulto Seg" >> kendallAll.dat
grep "seg" allJovemOrdInter.dat > kendallSegAllJovem.dat
grep "seg" allAdultoOrdInter.dat > kendallSegAllAdulto.dat
Rscript kendallDistance.R kendallSegAllJovem.dat kendallSegAllAdulto.dat >> kendallAll.dat

#echo " Jovem x Geral Seg" >> kendall.dat
#awk '{print $2}' ranking1.dat > temp.dat
#rm ranking3.dat
#while read photo ; do 
#	grep $photo segGeral.dat >> ranking3.dat
#done < temp.dat
#sort -k 3 -r ranking3.dat > ranking3Ord.dat 
#Rscript kendallDistance.R ranking1.dat ranking3Ord.dat >> kendall.dat
#echo " Adulto x Geral Seg" >> kendall.dat
#Rscript kendallDistance.R ranking2.dat ranking3Ord.dat >> kendall.dat

echo " Jovem x Geral Seg" >> kendallAll.dat
awk '{print $2}' kendallSegAllJovem.dat > temp.dat
rm ranking3.dat
while read photo ; do 
	grep $photo segGeralAll.dat >> ranking3.dat
done < temp.dat
sort -k 3 -r ranking3.dat > kendallSegAllGeralJovem.dat 
Rscript kendallDistance.R kendallSegAllJovem.dat kendallSegAllGeralJovem.dat >> kendallAll.dat
echo " Adulto x Geral Seg" >> kendallAll.dat
Rscript kendallDistance.R kendallSegAllAdulto.dat kendallSegAllGeralJovem.dat >> kendallAll.dat

#Centro e Not Centro
#echo " Centro x Not Centro Agrad" >> kendall.dat
#grep "agrad" firsCentroOrdInter.dat > ranking1.dat
#grep "agrad" firsNotCentroOrdInter.dat > ranking2.dat
#Rscript kendallDistance.R ranking1.dat ranking2.dat >> kendall.dat 

echo " Medio x Pos Agrad" >> kendallAll.dat
grep "agrad" allMedioOrdInter.dat > kendallAgradAllMedio.dat
grep "agrad" allPosOrdInter.dat > kendallAgradAllPos.dat
Rscript kendallDistance.R kendallAgradAllMedio.dat kendallAgradAllPos.dat >> kendallAll.dat

echo " Medio x Geral Agrad" >> kendallAll.dat
awk '{print $2}' kendallAgradAllMedio.dat > temp.dat
rm ranking3.dat
while read photo ; do 
	grep $photo agradGeralAll.dat >> ranking3.dat
done < temp.dat
sort -k 3 -r ranking3.dat > kendallAgradAllGeralMedio.dat 
Rscript kendallDistance.R kendallAgradAllMedio.dat kendallAgradAllGeralMedio.dat >> kendallAll.dat
echo " Pos x Geral Agrad" >> kendallAll.dat
Rscript kendallDistance.R kendallAgradAllPos.dat kendallAgradAllGeralMedio.dat >> kendallAll.dat

echo " Medio x Pos Seg" >> kendallAll.dat
grep "seg" allMedioOrdInter.dat > kendallSegAllMedio.dat
grep "seg" allPosOrdInter.dat > kendallSegAllPos.dat
Rscript kendallDistance.R kendallSegAllMedio.dat kendallSegAllPos.dat >> kendallAll.dat

echo " Medio x Geral Seg" >> kendallAll.dat
awk '{print $2}' kendallSegAllMedio.dat > temp.dat
rm ranking3.dat
while read photo ; do 
	grep $photo segGeralAll.dat >> ranking3.dat
done < temp.dat
sort -k 3 -r ranking3.dat > kendallSegAllGeralMedio.dat 
Rscript kendallDistance.R kendallSegAllMedio.dat kendallSegAllGeralMedio.dat >> kendallAll.dat
echo " Pos x Geral Seg" >> kendallAll.dat
Rscript kendallDistance.R kendallSegAllPos.dat kendallSegAllGeralMedio.dat >> kendallAll.dat


echo " Centro x Not Centro Agrad" >> kendallAll.dat
grep "agrad" allCentroOrdInter.dat > kendallAgradAllCentro.dat
grep "agrad" allNotCentroOrdInter.dat > kendallAgradAllNotCentro.dat
Rscript kendallDistance.R kendallAgradAllCentro.dat kendallAgradAllNotCentro.dat >> kendallAll.dat

#echo " Centro x Not Centro Seg" >> kendall.dat
#grep "seg" firsCentroOrdInter.dat > ranking1.dat
#grep "seg" firsNotCentroOrdInter.dat > ranking2.dat
#Rscript kendallDistance.R ranking1.dat ranking2.dat >> kendall.dat

echo " Centro x Not Centro Seg" >> kendallAll.dat
grep "seg" allCentroOrdInter.dat > kendallSegAllCentro.dat
grep "seg" allNotCentroOrdInter.dat > kendallSegAllNotCentro.dat
Rscript kendallDistance.R kendallSegAllCentro.dat kendallSegAllNotCentro.dat >> kendallAll.dat

#Catole e Not Catole
#echo " Catole x Not Catole Agrad" >> kendall.dat
#grep "agrad" firsCatoleOrdInter.dat > ranking1.dat
#grep "agrad" firsNotCatoleOrdInter.dat > ranking2.dat
#Rscript kendallDistance.R ranking1.dat ranking2.dat >> kendall.dat 

echo " Catole x Not Catole Agrad" >> kendallAll.dat
grep "agrad" allCatoleOrdInter.dat > kendallAgradAllCatole.dat
grep "agrad" allNotCatoleOrdInter.dat > kendallAgradAllNotCatole.dat
Rscript kendallDistance.R kendallAgradAllCatole.dat kendallAgradAllNotCatole.dat >> kendallAll.dat

#echo " Catole x Not Catole Seg" >> kendall.dat
#grep "seg" firsCatoleOrdInter.dat > ranking1.dat
#grep "seg" firsNotCatoleOrdInter.dat > ranking2.dat
#Rscript kendallDistance.R ranking1.dat ranking2.dat >> kendall.dat

echo " Catole x Not Catole Seg" >> kendallAll.dat
grep "seg" allCatoleOrdInter.dat > kendallSegAllCatole.dat
grep "seg" allNotCatoleOrdInter.dat > kendallSegAllNotCatole.dat
Rscript kendallDistance.R kendallSegAllCatole.dat kendallSegAllNotCatole.dat >> kendallAll.dat

#Liberdade e Not Liberdade
#echo " Liberdade x Not Liberdade Agrad" >> kendall.dat
#grep "agrad" firsLiberdadeOrdInter.dat > ranking1.dat
#grep "agrad" firsNotLiberdadeOrdInter.dat > ranking2.dat
#Rscript kendallDistance.R ranking1.dat ranking2.dat >> kendall.dat

echo " Liberdade x Not Liberdade Agra" >> kendallAll.dat
grep "agrad" allLiberdadeOrdInter.dat > kendallAgraAllLiberdade.dat
grep "agrad" allNotLiberdadeOrdInter.dat > kendallAgraAllNotLiberdade.dat
Rscript kendallDistance.R kendallAgraAllLiberdade.dat kendallAgraAllNotLiberdade.dat >> kendallAll.dat 

#echo " Liberdade x Not Liberdade Agrad" >> kendall.dat
#grep "seg" firsLiberdadeOrdInter.dat > ranking1.dat
#grep "seg" firsNotLiberdadeOrdInter.dat > ranking2.dat
#Rscript kendallDistance.R ranking1.dat ranking2.dat >> kendall.dat

echo " Liberdade x Not Liberdade Seg" >> kendallAll.dat
grep "seg" allLiberdadeOrdInter.dat > kendallSegAllLiberdade.dat
grep "seg" allNotLiberdadeOrdInter.dat > kendallSegAllNotLiberdade.dat
Rscript kendallDistance.R kendallSegAllLiberdade.dat kendallSegAllNotLiberdade.dat >> kendallAll.dat 

rm -f ranking1.dat ranking2.dat ranking3.dat ranking3Ord.dat temp.dat
mkdir kendal100
mv agradGeral.dat segGeral.dat agradGeralAll.dat segGeralAll.dat agradGeralAll.dat segGeralAll.dat kendall*.dat kendall100/

#Analisa QScore por Bairro (TODO medio e pos)
rm -f bairro.dat bairroAll.dat

#echo ">>>>>>>> Geral" >> bairro.dat
#python analisaQScorePorBairro.py first_vote_ordenado.dat > temp.dat
#grep "catole" temp.dat | grep "agra" > catole.dat
#grep "centro" temp.dat | grep "agra" > centro.dat
#grep "liberdade" temp.dat | grep "agra" > liberdade.dat
#echo "Agra Cat x Centro" >> bairro.dat
#Rscript  calculaTTest.R catole.dat centro.dat "Catole Agra Ger" "Centro Agra Ger" "green">> bairro.dat
#echo "Agra Lib x Centro" >> bairro.dat
#Rscript  calculaTTest.R liberdade.dat centro.dat "Liberdade Agra Ger" "Centro Agra Ger" "green" >> bairro.dat
#echo "Agra Cat x Liberdade" >> bairro.dat
#Rscript  calculaTTest.R catole.dat liberdade.dat "Catole Agra Ger" "Liberdade Agra Ger" "green" >> bairro.dat

#grep "catole" temp.dat | grep "seg" > catole.dat
#grep "centro" temp.dat | grep "seg" > centro.dat
#grep "liberdade" temp.dat | grep "seg" > liberdade.dat
#echo "Seg Cat x Centro" >> bairro.dat
#Rscript  calculaTTest.R catole.dat centro.dat "Catole Seg Ger" "Centro Seg Ger" "red" >> bairro.dat
#echo "Seg Lib x Centro" >> bairro.dat 
#Rscript  calculaTTest.R liberdade.dat centro.dat "Liberdade Seg Ger" "Centro Seg Ger" "red" >> bairro.dat
#echo "Seg Cat x Liberdade" >> bairro.dat
#Rscript  calculaTTest.R catole.dat liberdade.dat "Catole Seg Ger" "Liberdade Seg Ger" "red" >> bairro.dat

#Todos os votos
echo ">>>>>>>> Geral" >> bairroAll.dat
python analisaQScorePorBairro.py all_ordenado.dat > temp.dat
echo "### All Agra" >> bairroAll.dat
cat meanNeigAgra.dat >> bairroAll.dat
echo "### All Seg" >> bairroAll.dat
cat meanNeigSeg.dat >> bairroAll.dat
rm meanNeigAgra.dat meanNeigSeg.dat
grep "catole" temp.dat | grep "agra" > catoleAgradAll.dat
grep "centro" temp.dat | grep "agra" > centroAgradAll.dat
grep "liberdade" temp.dat | grep "agra" > liberdadeAgradAll.dat
echo "Agra Cat x Centro" >> bairroAll.dat
Rscript  calculaTTest.R catoleAgradAll.dat centroAgradAll.dat "Catole Agra Ger" "Centro Agra Ger" "green">> bairroAll.dat
echo "Agra Lib x Centro" >> bairroAll.dat
Rscript  calculaTTest.R liberdadeAgradAll.dat centroAgradAll.dat "Liberdade Agra Ger" "Centro Agra Ger" "green" >> bairroAll.dat
echo "Agra Cat x Liberdade" >> bairroAll.dat
Rscript  calculaTTest.R catoleAgradAll.dat liberdadeAgradAll.dat "Catole Agra Ger" "Liberdade Agra Ger" "green" >> bairroAll.dat

grep "catole" temp.dat | grep "seg" > catoleSegAll.dat
grep "centro" temp.dat | grep "seg" > centroSegAll.dat
grep "liberdade" temp.dat | grep "seg" > liberdadeSegAll.dat
echo "Seg Cat x Centro" >> bairroAll.dat
Rscript  calculaTTest.R catoleSegAll.dat centroSegAll.dat "Catole Seg Ger" "Centro Seg Ger" "red" >> bairroAll.dat
echo "Seg Lib x Centro" >> bairroAll.dat 
Rscript  calculaTTest.R liberdadeSegAll.dat centroSegAll.dat "Liberdade Seg Ger" "Centro Seg Ger" "red" >> bairroAll.dat
echo "Seg Cat x Liberdade" >> bairroAll.dat
Rscript  calculaTTest.R catoleSegAll.dat liberdadeSegAll.dat "Catole Seg Ger" "Liberdade Seg Ger" "red" >> bairroAll.dat

#Por grupo
#echo ">>>>>>>> Jovem" >> bairro.dat
#python analisaQScorePorBairro.py firsJovemOrdInter.dat > temp.dat
#grep "catole" temp.dat | grep "agra" > catole.dat
#grep "centro" temp.dat | grep "agra" > centro.dat
#grep "liberdade" temp.dat | grep "agra" > liberdade.dat
#echo "Agra Cat x Centro" >> bairro.dat
#Rscript  calculaTTest.R catole.dat centro.dat "Catole Agra Jov" "Centro Agra Jov" "green">> bairro.dat
#echo "Agra Lib x Centro" >> bairro.dat
#Rscript  calculaTTest.R liberdade.dat centro.dat "Liberdade Agra Jov" "Centro Agra Jov" "green" >> bairro.dat
#echo "Agra Cat x Liberdade" >> bairro.dat
#Rscript  calculaTTest.R catole.dat liberdade.dat "Catole Agra Jov" "Liberdade Agra Jov" "green" >> bairro.dat

#grep "catole" temp.dat | grep "seg" > catole.dat
#grep "centro" temp.dat | grep "seg" > centro.dat
#grep "liberdade" temp.dat | grep "seg" > liberdade.dat
#echo "Seg Cat x Centro" >> bairro.dat
#Rscript  calculaTTest.R catole.dat centro.dat "Catole Seg Jov" "Centro Seg Jov" "red" >> bairro.dat
#echo "Seg Lib x Centro" >> bairro.dat 
#Rscript  calculaTTest.R liberdade.dat centro.dat "Liberdade Seg Jov" "Centro Seg Jov" "red" >> bairro.dat
#echo "Seg Cat x Liberdade" >> bairro.dat
#Rscript  calculaTTest.R catole.dat liberdade.dat "Catole Seg Jov" "Liberdade Seg Jov" "red" >> bairro.dat

echo ">>>>>>>> Jovem" >> bairroAll.dat
python analisaQScorePorBairro.py allJovemOrdInter.dat > temp.dat
echo "### Jovem Agra" >> bairroAll.dat
cat meanNeigAgra.dat >> bairroAll.dat
echo "### Jovem Seg" >> bairroAll.dat
cat meanNeigSeg.dat >> bairroAll.dat
rm meanNeigAgra.dat meanNeigSeg.dat
grep "catole" temp.dat | grep "agra" > catoleAgradJovemAll.dat
grep "centro" temp.dat | grep "agra" > centroAgradJovemAll.dat
grep "liberdade" temp.dat | grep "agra" > liberdadeAgradJovemAll.dat
echo "Agra Cat x Centro" >> bairroAll.dat
Rscript  calculaTTest.R catoleAgradJovemAll.dat centroAgradJovemAll.dat "Catole Agra Jov" "Centro Agra Jov" "green">> bairroAll.dat
echo "Agra Lib x Centro" >> bairroAll.dat
Rscript  calculaTTest.R liberdadeAgradJovemAll.dat centroAgradJovemAll.dat "Liberdade Agra Jov" "Centro Agra Jov" "green" >> bairroAll.dat
echo "Agra Cat x Liberdade" >> bairroAll.dat
Rscript  calculaTTest.R catoleAgradJovemAll.dat liberdadeAgradJovemAll.dat "Catole Agra Jov" "Liberdade Agra Jov" "green" >> bairroAll.dat

grep "catole" temp.dat | grep "seg" > catoleSegJovemAll.dat
grep "centro" temp.dat | grep "seg" > centroSegJovemAll.dat
grep "liberdade" temp.dat | grep "seg" > liberdadeSegJovemAll.dat
echo "Seg Cat x Centro" >> bairroAll.dat
Rscript  calculaTTest.R catoleSegJovemAll.dat centroSegJovemAll.dat "Catole Seg Jov" "Centro Seg Jov" "red" >> bairroAll.dat
echo "Seg Lib x Centro" >> bairroAll.dat 
Rscript  calculaTTest.R liberdadeSegJovemAll.dat centroSegJovemAll.dat "Liberdade Seg Jov" "Centro Seg Jov" "red" >> bairroAll.dat
echo "Seg Cat x Liberdade" >> bairroAll.dat
Rscript  calculaTTest.R catoleSegJovemAll.dat liberdadeSegJovemAll.dat "Catole Seg Jov" "Liberdade Seg Jov" "red" >> bairroAll.dat



#echo ">>>>>>> Adulto" >> bairro.dat
#python analisaQScorePorBairro.py firsAdultoOrdInter.dat > temp.dat
#grep "catole" temp.dat | grep "agra" > catole.dat
#grep "centro" temp.dat | grep "agra" > centro.dat
#grep "liberdade" temp.dat | grep "agra" > liberdade.dat
#echo "Agra Cat x Centro" >> bairro.dat
#Rscript  calculaTTest.R catole.dat centro.dat "Catole Agra Adu" "Centro Agra Adu" "green">> bairro.dat
#echo "Agra Lib x Centro" >> bairro.dat
#Rscript  calculaTTest.R liberdade.dat centro.dat "Liberdade Agra Adu" "Centro Agra Adu" "green" >> bairro.dat
#echo "Agra Cat x Liberdade" >> bairro.dat
#Rscript  calculaTTest.R catole.dat liberdade.dat "Catole Agra Adu" "Liberdade Agra Adu" "green" >> bairro.dat

#grep "catole" temp.dat | grep "seg" > catole.dat
#grep "centro" temp.dat | grep "seg" > centro.dat
#grep "liberdade" temp.dat | grep "seg" > liberdade.dat
#echo "Seg Cat x Centro" >> bairro.dat
#Rscript  calculaTTest.R catole.dat centro.dat "Catole Seg Adu" "Centro Seg Adu" "red" >> bairro.dat
#echo "Seg Lib x Centro" >> bairro.dat 
#Rscript  calculaTTest.R liberdade.dat centro.dat "Liberdade Seg" "Centro Seg Adu" "red" >> bairro.dat
#echo "Seg Cat x Liberdade" >> bairro.dat
#Rscript  calculaTTest.R catole.dat liberdade.dat "Catole Seg Adu" "Liberdade Seg Adu" "red" >> bairro.dat

echo ">>>>>>> Adulto" >> bairroAll.dat
python analisaQScorePorBairro.py allAdultoOrdInter.dat > temp.dat
echo "### Adulto Agra" >> bairroAll.dat
cat meanNeigAgra.dat >> bairroAll.dat
echo "### Adulto Seg" >> bairroAll.dat
cat meanNeigSeg.dat >> bairroAll.dat
rm meanNeigAgra.dat meanNeigSeg.dat
grep "catole" temp.dat | grep "agra" > catoleAgradAdultoAll.dat
grep "centro" temp.dat | grep "agra" > centroAgradAdultoAll.dat
grep "liberdade" temp.dat | grep "agra" > liberdadeAgradAdultoAll.dat
echo "Agra Cat x Centro" >> bairroAll.dat
Rscript  calculaTTest.R catoleAgradAdultoAll.dat centroAgradAdultoAll.dat "Catole Agra Adu" "Centro Agra Adu" "green">> bairroAll.dat
echo "Agra Lib x Centro" >> bairroAll.dat
Rscript  calculaTTest.R liberdadeAgradAdultoAll.dat centroAgradAdultoAll.dat "Liberdade Agra Adu" "Centro Agra Adu" "green" >> bairroAll.dat
echo "Agra Cat x Liberdade" >> bairroAll.dat
Rscript  calculaTTest.R catoleAgradAdultoAll.dat liberdadeAgradAdultoAll.dat "Catole Agra Adu" "Liberdade Agra Adu" "green" >> bairroAll.dat

grep "catole" temp.dat | grep "seg" > catoleSegAdultoAll.dat
grep "centro" temp.dat | grep "seg" > centroSegAdultoAll.dat
grep "liberdade" temp.dat | grep "seg" > liberdadeSegAdultoAll.dat
echo "Seg Cat x Centro" >> bairroAll.dat
Rscript  calculaTTest.R catoleSegAdultoAll.dat centroSegAdultoAll.dat "Catole Seg Adu" "Centro Seg Adu" "red" >> bairroAll.dat
echo "Seg Lib x Centro" >> bairroAll.dat 
Rscript  calculaTTest.R liberdadeSegAdultoAll.dat centroSegAdultoAll.dat "Liberdade Seg" "Centro Seg Adu" "red" >> bairroAll.dat
echo "Seg Cat x Liberdade" >> bairroAll.dat
Rscript  calculaTTest.R catoleSegAdultoAll.dat liberdadeSegAdultoAll.dat "Catole Seg Adu" "Liberdade Seg Adu" "red" >> bairroAll.dat





#echo ">>>>>>>>>> Baixa" >> bairro.dat
#python analisaQScorePorBairro.py firsBaixaOrdInter.dat > temp.dat
#grep "catole" temp.dat | grep "agra" > catole.dat
#grep "centro" temp.dat | grep "agra" > centro.dat
#grep "liberdade" temp.dat | grep "agra" > liberdade.dat
#echo "Agra Cat x Centro" >> bairro.dat
#Rscript  calculaTTest.R catole.dat centro.dat "Catole Agra Bai" "Centro Agra Bai" "green">> bairro.dat
#echo "Agra Lib x Centro" >> bairro.dat
#Rscript  calculaTTest.R liberdade.dat centro.dat "Liberdade Agra Bai" "Centro Agra Bai" "green" >> bairro.dat
#echo "Agra Cat x Liberdade" >> bairro.dat
#Rscript  calculaTTest.R catole.dat liberdade.dat "Catole Agra Bai" "Liberdade Agra Bai" "green" >> bairro.dat

#grep "catole" temp.dat | grep "seg" > catole.dat
#grep "centro" temp.dat | grep "seg" > centro.dat
#grep "liberdade" temp.dat | grep "seg" > liberdade.dat
#echo "Seg Cat x Centro" >> bairro.dat
#Rscript  calculaTTest.R catole.dat centro.dat "Catole Seg Bai" "Centro Seg Bai" "red" >> bairro.dat
#echo "Seg Lib x Centro" >> bairro.dat 
#Rscript  calculaTTest.R liberdade.dat centro.dat "Liberdade Seg Bai" "Centro Seg Bai" "red" >> bairro.dat
#echo "Seg Cat x Liberdade" >> bairro.dat
#Rscript  calculaTTest.R catole.dat liberdade.dat "Catole Seg Bai" "Liberdade Seg Bai" "red" >> bairro.dat


echo ">>>>>>>>>> Baixa" >> bairroAll.dat
python analisaQScorePorBairro.py allBaixaOrdInter.dat > temp.dat
echo "### Baixa Agra" >> bairroAll.dat
cat meanNeigAgra.dat >> bairroAll.dat
echo "### Baixa Seg" >> bairroAll.dat
cat meanNeigSeg.dat >> bairroAll.dat
rm meanNeigAgra.dat meanNeigSeg.dat
grep "catole" temp.dat | grep "agra" > catoleAgradBaixaAll.dat
grep "centro" temp.dat | grep "agra" > centroAgradBaixaAll.dat
grep "liberdade" temp.dat | grep "agra" > liberdadeAgradBaixaAll.dat
echo "Agra Cat x Centro" >> bairroAll.dat
Rscript  calculaTTest.R catoleAgradBaixaAll.dat centroAgradBaixaAll.dat "Catole Agra Bai" "Centro Agra Bai" "green">> bairroAll.dat
echo "Agra Lib x Centro" >> bairroAll.dat
Rscript  calculaTTest.R liberdadeAgradBaixaAll.dat centroAgradBaixaAll.dat "Liberdade Agra Bai" "Centro Agra Bai" "green" >> bairroAll.dat
echo "Agra Cat x Liberdade" >> bairroAll.dat
Rscript  calculaTTest.R catoleAgradBaixaAll.dat liberdadeAgradBaixaAll.dat "Catole Agra Bai" "Liberdade Agra Bai" "green" >> bairroAll.dat

grep "catole" temp.dat | grep "seg" > catoleSegBaixaAll.dat
grep "centro" temp.dat | grep "seg" > centroSegBaixaAll.dat
grep "liberdade" temp.dat | grep "seg" > liberdadeSegBaixaAll.dat
echo "Seg Cat x Centro" >> bairroAll.dat
Rscript  calculaTTest.R catoleSegBaixaAll.dat centroSegBaixaAll.dat "Catole Seg Bai" "Centro Seg Bai" "red" >> bairroAll.dat
echo "Seg Lib x Centro" >> bairroAll.dat 
Rscript  calculaTTest.R liberdadeSegBaixaAll.dat centroSegBaixaAll.dat "Liberdade Seg Bai" "Centro Seg Bai" "red" >> bairroAll.dat
echo "Seg Cat x Liberdade" >> bairroAll.dat
Rscript  calculaTTest.R catoleSegBaixaAll.dat liberdadeSegBaixaAll.dat "Catole Seg Bai" "Liberdade Seg Bai" "red" >> bairroAll.dat


#echo ">>>>>>>>>> Media" >> bairro.dat
#python analisaQScorePorBairro.py firsMediaOrdInter.dat > temp.dat
#grep "catole" temp.dat | grep "agra" > catole.dat
#grep "centro" temp.dat | grep "agra" > centro.dat
#grep "liberdade" temp.dat | grep "agra" > liberdade.dat
#echo "Agra Cat x Centro" >> bairro.dat
#Rscript  calculaTTest.R catole.dat centro.dat "Catole Agra Med" "Centro Agra Med" "green">> bairro.dat
#echo "Agra Lib x Centro" >> bairro.dat
#Rscript  calculaTTest.R liberdade.dat centro.dat "Liberdade Agra Med" "Centro Agra Med" "green" >> bairro.dat
#echo "Agra Cat x Liberdade" >> bairro.dat
#Rscript  calculaTTest.R catole.dat liberdade.dat "Catole Agra Med" "Liberdade Agra Med" "green" >> bairro.dat

#grep "catole" temp.dat | grep "seg" > catole.dat
#grep "centro" temp.dat | grep "seg" > centro.dat
#grep "liberdade" temp.dat | grep "seg" > liberdade.dat
#echo "Seg Cat x Centro" >> bairro.dat
#Rscript  calculaTTest.R catole.dat centro.dat "Catole Seg Med" "Centro Seg Med" "red" >> bairro.dat
#echo "Seg Lib x Centro" >> bairro.dat 
#Rscript  calculaTTest.R liberdade.dat centro.dat "Liberdade Seg Med" "Centro Seg Med" "red" >> bairro.dat
#echo "Seg Cat x Liberdade" >> bairro.dat
#Rscript  calculaTTest.R catole.dat liberdade.dat "Catole Seg Med" "Liberdade Seg Med" "red" >> bairro.dat

echo ">>>>>>>>>> Media" >> bairroAll.dat
python analisaQScorePorBairro.py allMediaOrdInter.dat > temp.dat
echo "### Media Agra" >> bairroAll.dat
cat meanNeigAgra.dat >> bairroAll.dat
echo "### Media Seg" >> bairroAll.dat
cat meanNeigSeg.dat >> bairroAll.dat
rm meanNeigAgra.dat meanNeigSeg.dat
grep "catole" temp.dat | grep "agra" > catoleAgradMediaAll.dat
grep "centro" temp.dat | grep "agra" > centroAgradMediaAll.dat
grep "liberdade" temp.dat | grep "agra" > liberdadeAgradMediaAll.dat
echo "Agra Cat x Centro" >> bairroAll.dat
Rscript  calculaTTest.R catoleAgradMediaAll.dat centroAgradMediaAll.dat "Catole Agra Med" "Centro Agra Med" "green">> bairroAll.dat
echo "Agra Lib x Centro" >> bairroAll.dat
Rscript  calculaTTest.R liberdadeAgradMediaAll.dat centroAgradMediaAll.dat "Liberdade Agra Med" "Centro Agra Med" "green" >> bairroAll.dat
echo "Agra Cat x Liberdade" >> bairroAll.dat
Rscript  calculaTTest.R catoleAgradMediaAll.dat liberdadeAgradMediaAll.dat "Catole Agra Med" "Liberdade Agra Med" "green" >> bairroAll.dat

grep "catole" temp.dat | grep "seg" > catoleSegMediaAll.dat
grep "centro" temp.dat | grep "seg" > centroSegMediaAll.dat
grep "liberdade" temp.dat | grep "seg" > liberdadeSegMediaAll.dat
echo "Seg Cat x Centro" >> bairroAll.dat
Rscript  calculaTTest.R catoleSegMediaAll.dat centroSegMediaAll.dat "Catole Seg Med" "Centro Seg Med" "red" >> bairroAll.dat
echo "Seg Lib x Centro" >> bairroAll.dat 
Rscript  calculaTTest.R liberdadeSegMediaAll.dat centroSegMediaAll.dat "Liberdade Seg Med" "Centro Seg Med" "red" >> bairroAll.dat
echo "Seg Cat x Liberdade" >> bairroAll.dat
Rscript  calculaTTest.R catoleSegMediaAll.dat liberdadeSegMediaAll.dat "Catole Seg Med" "Liberdade Seg Med" "red" >> bairroAll.dat




#echo ">>>>>>>>>> Fem" >> bairro.dat
#python analisaQScorePorBairro.py firsFemininoOrdInter.dat > temp.dat
#grep "catole" temp.dat | grep "agra" > catole.dat
#grep "centro" temp.dat | grep "agra" > centro.dat
#grep "liberdade" temp.dat | grep "agra" > liberdade.dat
#echo "Agra Cat x Centro" >> bairro.dat
#Rscript  calculaTTest.R catole.dat centro.dat "Catole Agra Fem" "Centro Agra Fem" "green">> bairro.dat
#echo "Agra Lib x Centro" >> bairro.dat
#Rscript  calculaTTest.R liberdade.dat centro.dat "Liberdade Agra Fem" "Centro Agra Fem" "green" >> bairro.dat
#echo "Agra Cat x Liberdade" >> bairro.dat
#Rscript  calculaTTest.R catole.dat liberdade.dat "Catole Agra Fem" "Liberdade Agra Fem" "green" >> bairro.dat

#grep "catole" temp.dat | grep "seg" > catole.dat
#grep "centro" temp.dat | grep "seg" > centro.dat
#grep "liberdade" temp.dat | grep "seg" > liberdade.dat
#echo "Seg Cat x Centro" >> bairro.dat
#Rscript  calculaTTest.R catole.dat centro.dat "Catole Seg Fem" "Centro Seg Fem" "red" >> bairro.dat
#echo "Seg Lib x Centro" >> bairro.dat 
#Rscript  calculaTTest.R liberdade.dat centro.dat "Liberdade Seg Fem" "Centro Seg Fem" "red" >> bairro.dat
#echo "Seg Cat x Liberdade" >> bairro.dat
#Rscript  calculaTTest.R catole.dat liberdade.dat "Catole Seg Fem" "Liberdade Seg Fem" "red" >> bairro.dat

echo ">>>>>>>>>> Fem" >> bairroAll.dat
python analisaQScorePorBairro.py allFemininoOrdInter.dat > temp.dat
echo "### Fem Agra" >> bairroAll.dat
cat meanNeigAgra.dat >> bairroAll.dat
echo "### Fem Seg" >> bairroAll.dat
cat meanNeigSeg.dat >> bairroAll.dat
rm meanNeigAgra.dat meanNeigSeg.dat
grep "catole" temp.dat | grep "agra" > catoleAgradFemininoAll.dat
grep "centro" temp.dat | grep "agra" > centroAgradFemininoAll.dat
grep "liberdade" temp.dat | grep "agra" > liberdadeAgradFemininoAll.dat
echo "Agra Cat x Centro" >> bairroAll.dat
Rscript  calculaTTest.R catoleAgradFemininoAll.dat centroAgradFemininoAll.dat "Catole Agra Fem" "Centro Agra Fem" "green">> bairroAll.dat
echo "Agra Lib x Centro" >> bairroAll.dat
Rscript  calculaTTest.R liberdadeAgradFemininoAll.dat centroAgradFemininoAll.dat "Liberdade Agra Fem" "Centro Agra Fem" "green" >> bairroAll.dat
echo "Agra Cat x Liberdade" >> bairroAll.dat
Rscript  calculaTTest.R catoleAgradFemininoAll.dat liberdadeAgradFemininoAll.dat "Catole Agra Fem" "Liberdade Agra Fem" "green" >> bairroAll.dat

grep "catole" temp.dat | grep "seg" > catoleSegFemininoAll.dat
grep "centro" temp.dat | grep "seg" > centroSegFemininoAll.dat
grep "liberdade" temp.dat | grep "seg" > liberdadeSegFemininoAll.dat
echo "Seg Cat x Centro" >> bairroAll.dat
Rscript  calculaTTest.R catoleSegFemininoAll.dat centroSegFemininoAll.dat "Catole Seg Fem" "Centro Seg Fem" "red" >> bairroAll.dat
echo "Seg Lib x Centro" >> bairroAll.dat 
Rscript  calculaTTest.R liberdadeSegFemininoAll.dat centroSegFemininoAll.dat "Liberdade Seg Fem" "Centro Seg Fem" "red" >> bairroAll.dat
echo "Seg Cat x Liberdade" >> bairroAll.dat
Rscript  calculaTTest.R catoleSegFemininoAll.dat liberdadeSegFemininoAll.dat "Catole Seg Fem" "Liberdade Seg Fem" "red" >> bairroAll.dat




#echo ">>>>>>>>> Masc" >> bairro.dat
#python analisaQScorePorBairro.py firsMasculinoOrdInter.dat > temp.dat
#grep "catole" temp.dat | grep "agra" > catole.dat
#grep "centro" temp.dat | grep "agra" > centro.dat
#grep "liberdade" temp.dat | grep "agra" > liberdade.dat
#echo "Agra Cat x Centro" >> bairro.dat
#Rscript  calculaTTest.R catole.dat centro.dat "Catole Agra Mas" "Centro Agra Mas" "green">> bairro.dat
#echo "Agra Lib x Centro" >> bairro.dat
#Rscript  calculaTTest.R liberdade.dat centro.dat "Liberdade Agra Mas" "Centro Agra Mas" "green" >> bairro.dat
#echo "Agra Cat x Liberdade" >> bairro.dat
#Rscript  calculaTTest.R catole.dat liberdade.dat "Catole Agra Mas" "Liberdade Agra Mas" "green" >> bairro.dat

#grep "catole" temp.dat | grep "seg" > catole.dat
#grep "centro" temp.dat | grep "seg" > centro.dat
#grep "liberdade" temp.dat | grep "seg" > liberdade.dat
#echo "Seg Cat x Centro" >> bairro.dat
#Rscript  calculaTTest.R catole.dat centro.dat "Catole Seg Mas" "Centro Seg Mas" "red" >> bairro.dat
#echo "Seg Lib x Centro" >> bairro.dat 
#Rscript  calculaTTest.R liberdade.dat centro.dat "Liberdade Seg Mas" "Centro Seg Mas" "red" >> bairro.dat
#echo "Seg Cat x Liberdade" >> bairro.dat
#Rscript  calculaTTest.R catole.dat liberdade.dat "Catole Seg Mas" "Liberdade Seg Mas" "red" >> bairro.dat

echo ">>>>>>>>> Masc" >> bairroAll.dat
python analisaQScorePorBairro.py allMasculinoOrdInter.dat > temp.dat
echo "### Masc Agra" >> bairroAll.dat
cat meanNeigAgra.dat >> bairroAll.dat
echo "### Masc Seg" >> bairroAll.dat
cat meanNeigSeg.dat >> bairroAll.dat
rm meanNeigAgra.dat meanNeigSeg.dat
grep "catole" temp.dat | grep "agra" > catoleAgradMasculinoAll.dat
grep "centro" temp.dat | grep "agra" > centroAgradMasculinoAll.dat
grep "liberdade" temp.dat | grep "agra" > liberdadeAgradMasculinoAll.dat
echo "Agra Cat x Centro" >> bairroAll.dat
Rscript  calculaTTest.R catoleAgradMasculinoAll.dat centroAgradMasculinoAll.dat "Catole Agra Mas" "Centro Agra Mas" "green">> bairroAll.dat
echo "Agra Lib x Centro" >> bairroAll.dat
Rscript  calculaTTest.R liberdadeAgradMasculinoAll.dat centroAgradMasculinoAll.dat "Liberdade Agra Mas" "Centro Agra Mas" "green" >> bairroAll.dat
echo "Agra Cat x Liberdade" >> bairroAll.dat
Rscript  calculaTTest.R catoleAgradMasculinoAll.dat liberdadeAgradMasculinoAll.dat "Catole Agra Mas" "Liberdade Agra Mas" "green" >> bairroAll.dat

grep "catole" temp.dat | grep "seg" > catoleSegMasculinoAll.dat
grep "centro" temp.dat | grep "seg" > centroSegMasculinoAll.dat
grep "liberdade" temp.dat | grep "seg" > liberdadeSegMasculinoAll.dat
echo "Seg Cat x Centro" >> bairroAll.dat
Rscript  calculaTTest.R catoleSegMasculinoAll.dat centroSegMasculinoAll.dat "Catole Seg Mas" "Centro Seg Mas" "red" >> bairroAll.dat
echo "Seg Lib x Centro" >> bairroAll.dat 
Rscript  calculaTTest.R liberdadeSegMasculinoAll.dat centroSegMasculinoAll.dat "Liberdade Seg Mas" "Centro Seg Mas" "red" >> bairroAll.dat
echo "Seg Cat x Liberdade" >> bairroAll.dat
Rscript  calculaTTest.R catoleSegMasculinoAll.dat liberdadeSegMasculinoAll.dat "Catole Seg Mas" "Liberdade Seg Mas" "red" >> bairroAll.dat




#echo ">>>>>>>>>>>> Casado" >> bairro.dat
#python analisaQScorePorBairro.py firsCasadoOrdInter.dat > temp.dat
#grep "catole" temp.dat | grep "agra" > catole.dat
#grep "centro" temp.dat | grep "agra" > centro.dat
#grep "liberdade" temp.dat | grep "agra" > liberdade.dat
#echo "Agra Cat x Centro" >> bairro.dat
#Rscript  calculaTTest.R catole.dat centro.dat "Catole Agra Cas" "Centro Agra Cas" "green">> bairro.dat
#echo "Agra Lib x Centro" >> bairro.dat
#Rscript  calculaTTest.R liberdade.dat centro.dat "Liberdade Agra Cas" "Centro Agra Cas" "green" >> bairro.dat
#echo "Agra Cat x Liberdade" >> bairro.dat
#Rscript  calculaTTest.R catole.dat liberdade.dat "Catole Agra Cas" "Liberdade Agra Cas" "green" >> bairro.dat

#grep "catole" temp.dat | grep "seg" > catole.dat
#grep "centro" temp.dat | grep "seg" > centro.dat
#grep "liberdade" temp.dat | grep "seg" > liberdade.dat
#echo "Seg Cat x Centro" >> bairro.dat
#Rscript  calculaTTest.R catole.dat centro.dat "Catole Seg Cas" "Centro Seg Cas" "red" >> bairro.dat
#echo "Seg Lib x Centro" >> bairro.dat 
#Rscript  calculaTTest.R liberdade.dat centro.dat "Liberdade Seg Cas" "Centro Seg Cas" "red" >> bairro.dat
#echo "Seg Cat x Liberdade" >> bairro.dat
#Rscript  calculaTTest.R catole.dat liberdade.dat "Catole Seg Cas" "Liberdade Seg Cas" "red" >> bairro.dat

echo ">>>>>>>>>>>> Casado" >> bairroAll.dat
python analisaQScorePorBairro.py allCasadoOrdInter.dat > temp.dat
echo "### Casado Agra" >> bairroAll.dat
cat meanNeigAgra.dat >> bairroAll.dat
echo "### Casado Seg" >> bairroAll.dat
cat meanNeigSeg.dat >> bairroAll.dat
rm meanNeigAgra.dat meanNeigSeg.dat
grep "catole" temp.dat | grep "agra" > catoleAgradCasadoAll.dat
grep "centro" temp.dat | grep "agra" > centroAgradCasadoAll.dat
grep "liberdade" temp.dat | grep "agra" > liberdadeAgradCasadoAll.dat
echo "Agra Cat x Centro" >> bairroAll.dat
Rscript  calculaTTest.R catoleAgradCasadoAll.dat centroAgradCasadoAll.dat "Catole Agra Cas" "Centro Agra Cas" "green">> bairroAll.dat
echo "Agra Lib x Centro" >> bairroAll.dat
Rscript  calculaTTest.R liberdadeAgradCasadoAll.dat centroAgradCasadoAll.dat "Liberdade Agra Cas" "Centro Agra Cas" "green" >> bairroAll.dat
echo "Agra Cat x Liberdade" >> bairroAll.dat
Rscript  calculaTTest.R catoleAgradCasadoAll.dat liberdadeAgradCasadoAll.dat "Catole Agra Cas" "Liberdade Agra Cas" "green" >> bairroAll.dat

grep "catole" temp.dat | grep "seg" > catoleSegCasadoAll.dat
grep "centro" temp.dat | grep "seg" > centroSegCasadoAll.dat
grep "liberdade" temp.dat | grep "seg" > liberdadeSegCasadoAll.dat
echo "Seg Cat x Centro" >> bairroAll.dat
Rscript  calculaTTest.R catoleSegCasadoAll.dat centroSegCasadoAll.dat "Catole Seg Cas" "Centro Seg Cas" "red" >> bairroAll.dat
echo "Seg Lib x Centro" >> bairroAll.dat 
Rscript  calculaTTest.R liberdadeSegCasadoAll.dat centroSegCasadoAll.dat "Liberdade Seg Cas" "Centro Seg Cas" "red" >> bairroAll.dat
echo "Seg Cat x Liberdade" >> bairroAll.dat
Rscript  calculaTTest.R catoleSegCasadoAll.dat liberdadeSegCasadoAll.dat "Catole Seg Cas" "Liberdade Seg Cas" "red" >> bairroAll.dat



#echo ">>>>>>>>>>>>>> Solteiro" >> bairro.dat
#python analisaQScorePorBairro.py firsSolteiroOrdInter.dat > temp.dat
#grep "catole" temp.dat | grep "agra" > catole.dat
#grep "centro" temp.dat | grep "agra" > centro.dat
#grep "liberdade" temp.dat | grep "agra" > liberdade.dat
#echo "Agra Cat x Centro" >> bairro.dat
#Rscript  calculaTTest.R catole.dat centro.dat "Catole Agra Sol" "Centro Agra Sol" "green">> bairro.dat
#echo "Agra Lib x Centro" >> bairro.dat
#Rscript  calculaTTest.R liberdade.dat centro.dat "Liberdade Agra Sol" "Centro Agra Sol" "green" >> bairro.dat
#echo "Agra Cat x Liberdade" >> bairro.dat
#Rscript  calculaTTest.R catole.dat liberdade.dat "Catole Agra Sol" "Liberdade Agra Sol" "green" >> bairro.dat

#grep "catole" temp.dat | grep "seg" > catole.dat
#grep "centro" temp.dat | grep "seg" > centro.dat
#grep "liberdade" temp.dat | grep "seg" > liberdade.dat
#echo "Seg Cat x Centro" >> bairro.dat
#Rscript  calculaTTest.R catole.dat centro.dat "Catole Seg Sol" "Centro Seg Sol" "red" >> bairro.dat
#echo "Seg Lib x Centro" >> bairro.dat 
#Rscript  calculaTTest.R liberdade.dat centro.dat "Liberdade Seg Sol" "Centro Seg Sol" "red" >> bairro.dat
#echo "Seg Cat x Liberdade" >> bairro.dat
#Rscript  calculaTTest.R catole.dat liberdade.dat "Catole Seg Sol" "Liberdade Seg Sol" "red" >> bairro.dat

echo ">>>>>>>>>>>>>> Solteiro" >> bairroAll.dat
python analisaQScorePorBairro.py allSolteiroOrdInter.dat > temp.dat
echo "### Solteiro Agra" >> bairroAll.dat
cat meanNeigAgra.dat >> bairroAll.dat
echo "### Solteiro Seg" >> bairroAll.dat
cat meanNeigSeg.dat >> bairroAll.dat
rm meanNeigAgra.dat meanNeigSeg.dat
grep "catole" temp.dat | grep "agra" > catoleAgradSolteiroAll.dat
grep "centro" temp.dat | grep "agra" > centroAgradSolteiroAll.dat
grep "liberdade" temp.dat | grep "agra" > liberdadeAgradSolteiroAll.dat
echo "Agra Cat x Centro" >> bairroAll.dat
Rscript  calculaTTest.R catoleAgradSolteiroAll.dat centroAgradSolteiroAll.dat "Catole Agra Sol" "Centro Agra Sol" "green">> bairroAll.dat
echo "Agra Lib x Centro" >> bairroAll.dat
Rscript  calculaTTest.R liberdadeAgradSolteiroAll.dat centroAgradSolteiroAll.dat "Liberdade Agra Sol" "Centro Agra Sol" "green" >> bairroAll.dat
echo "Agra Cat x Liberdade" >> bairroAll.dat
Rscript  calculaTTest.R catoleAgradSolteiroAll.dat liberdadeAgradSolteiroAll.dat "Catole Agra Sol" "Liberdade Agra Sol" "green" >> bairroAll.dat

grep "catole" temp.dat | grep "seg" > catoleSegSolteiroAll.dat
grep "centro" temp.dat | grep "seg" > centroSegSolteiroAll.dat
grep "liberdade" temp.dat | grep "seg" > liberdadeSegSolteiroAll.dat
echo "Seg Cat x Centro" >> bairroAll.dat
Rscript  calculaTTest.R catoleSegSolteiroAll.dat centroSegSolteiroAll.dat "Catole Seg Sol" "Centro Seg Sol" "red" >> bairroAll.dat
echo "Seg Lib x Centro" >> bairroAll.dat 
Rscript  calculaTTest.R liberdadeSegSolteiroAll.dat centroSegSolteiroAll.dat "Liberdade Seg Sol" "Centro Seg Sol" "red" >> bairroAll.dat
echo "Seg Cat x Liberdade" >> bairroAll.dat
Rscript  calculaTTest.R catoleSegSolteiroAll.dat liberdadeSegSolteiroAll.dat "Catole Seg Sol" "Liberdade Seg Sol" "red" >> bairroAll.dat


#echo ">>>>>>>>>>>>>> Conhece" >> bairro.dat
#python analisaQScorePorBairro.py firsCentroOrdInter.dat > temp.dat
#python analisaQScorePorBairro.py firsCatoleOrdInter.dat >> temp.dat
#python analisaQScorePorBairro.py firsLiberdadeOrdInter.dat >> temp.dat
#grep "catole" temp.dat | grep "agra" > catole.dat
#grep "centro" temp.dat | grep "agra" > centro.dat
#grep "liberdade" temp.dat | grep "agra" > liberdade.dat
#echo "Agra Cat x Centro" >> bairro.dat
#Rscript  calculaTTest.R catole.dat centro.dat "Catole Agra Sol" "Centro Agra Sol" "green">> bairro.dat
#echo "Agra Lib x Centro" >> bairro.dat
#Rscript  calculaTTest.R liberdade.dat centro.dat "Liberdade Agra Sol" "Centro Agra Sol" "green" >> bairro.dat
#echo "Agra Cat x Liberdade" >> bairro.dat
#Rscript  calculaTTest.R catole.dat liberdade.dat "Catole Agra Sol" "Liberdade Agra Sol" "green" >> bairro.dat

echo ">>>>>>>>>>>>>> Conhece" >> bairroAll.dat
python analisaQScorePorBairro.py allCentroOrdInter.dat > temp.dat
python analisaQScorePorBairro.py allCatoleOrdInter.dat >> temp.dat
python analisaQScorePorBairro.py allLiberdadeOrdInter.dat >> temp.dat
grep "catole" temp.dat | grep "agra" > catoleAgradConheceAll.dat
grep "centro" temp.dat | grep "agra" > centroAgradConheceAll.dat
grep "liberdade" temp.dat | grep "agra" > liberdadeAgradConheceAll.dat
echo "Agra Cat x Centro" >> bairroAll.dat
Rscript  calculaTTest.R catoleAgradConheceAll.dat centroAgradConheceAll.dat "Catole Agra Con" "Centro Agra Con" "green">> bairroAll.dat
echo "Agra Lib x Centro" >> bairroAll.dat
Rscript  calculaTTest.R liberdadeAgradConheceAll.dat centroAgradConheceAll.dat "Liberdade Agra Con" "Centro Agra Con" "green" >> bairroAll.dat
echo "Agra Cat x Liberdade" >> bairroAll.dat
Rscript  calculaTTest.R catoleAgradConheceAll.dat liberdadeAgradConheceAll.dat "Catole Agra Con" "Liberdade Agra Con" "green" >> bairroAll.dat

grep "catole" temp.dat | grep "seg" > catoleSegConheceAll.dat
grep "centro" temp.dat | grep "seg" > centroSegConheceAll.dat
grep "liberdade" temp.dat | grep "seg" > liberdadeSegConheceAll.dat
echo "Seg Cat x Centro" >> bairroAll.dat
Rscript  calculaTTest.R catoleSegConheceAll.dat centroSegConheceAll.dat "Catole Seg Con" "Centro Seg Con" "green">> bairroAll.dat
echo "Seg Lib x Centro" >> bairroAll.dat
Rscript  calculaTTest.R liberdadeSegConheceAll.dat centroSegConheceAll.dat "Liberdade Seg Con" "Centro Seg Con" "green" >> bairroAll.dat
echo "Seg Cat x Liberdade" >> bairroAll.dat
Rscript  calculaTTest.R catoleSegConheceAll.dat liberdadeSegConheceAll.dat "Catole Seg Con" "Liberdade Seg Con" "green" >> bairroAll.dat

#echo ">>>>>>>>>>>>>> Não Conhece" >> bairro.dat
#python analisaQScorePorBairro.py firsNotCentroOrdInter.dat > temp.dat
#python analisaQScorePorBairro.py firsNotCatoleOrdInter.dat >> temp.dat
#python analisaQScorePorBairro.py firsNotLiberdadeOrdInter.dat >> temp.dat
#grep "catole" temp.dat | grep "agra" > catole.dat
#grep "centro" temp.dat | grep "agra" > centro.dat
#grep "liberdade" temp.dat | grep "agra" > liberdade.dat
#echo "Agra Cat x Centro" >> bairro.dat
#Rscript  calculaTTest.R catole.dat centro.dat "Catole Agra Sol" "Centro Agra Sol" "green">> bairro.dat
#echo "Agra Lib x Centro" >> bairro.dat
#Rscript  calculaTTest.R liberdade.dat centro.dat "Liberdade Agra Sol" "Centro Agra Sol" "green" >> bairro.dat
#echo "Agra Cat x Liberdade" >> bairro.dat
#Rscript  calculaTTest.R catole.dat liberdade.dat "Catole Agra Sol" "Liberdade Agra Sol" "green" >> bairro.dat

echo ">>>>>>>>>>>>>> Não Conhece" >> bairroAll.dat
python analisaQScorePorBairro.py allNotCentroOrdInter.dat > temp.dat
python analisaQScorePorBairro.py allNotCatoleOrdInter.dat >> temp.dat
python analisaQScorePorBairro.py allNotLiberdadeOrdInter.dat >> temp.dat
grep "catole" temp.dat | grep "agra" > catoleAgradNConheceAll.dat
grep "centro" temp.dat | grep "agra" > centroAgradNConheceAll.dat
grep "liberdade" temp.dat | grep "agra" > liberdadeAgradNConheceAll.dat
echo "Agra Cat x Centro" >> bairroAll.dat
Rscript  calculaTTest.R catoleAgradNConheceAll.dat centroAgradNConheceAll.dat "Catole Agra NCon" "Centro Agra NCon" "green">> bairroAll.dat
echo "Agra Lib x Centro" >> bairroAll.dat
Rscript  calculaTTest.R liberdadeAgradNConheceAll.dat centroAgradNConheceAll.dat "Liberdade Agra NCon" "Centro Agra NCon" "green" >> bairroAll.dat
echo "Agra Cat x Liberdade" >> bairroAll.dat
Rscript  calculaTTest.R catoleAgradNConheceAll.dat liberdadeAgradNConheceAll.dat "Catole Agra NCon" "Liberdade Agra NCon" "green" >> bairroAll.dat

grep "catole" temp.dat | grep "seg" > catoleSegNConheceAll.dat
grep "centro" temp.dat | grep "seg" > centroSegNConheceAll.dat
grep "liberdade" temp.dat | grep "seg" > liberdadeSegNConheceAll.dat
echo "Seg Cat x Centro" >> bairroAll.dat
Rscript  calculaTTest.R catoleSegNConheceAll.dat centroSegNConheceAll.dat "Catole Seg NCon" "Centro Seg NCon" "green">> bairroAll.dat
echo "Seg Lib x Centro" >> bairroAll.dat
Rscript  calculaTTest.R liberdadeSegNConheceAll.dat centroSegNConheceAll.dat "Liberdade Seg NCon" "Centro Seg NCon" "green" >> bairroAll.dat
echo "Seg Cat x Liberdade" >> bairroAll.dat
Rscript  calculaTTest.R catoleSegNConheceAll.dat liberdadeSegNConheceAll.dat "Catole Seg NCon" "Liberdade Seg NCon" "green" >> bairroAll.dat

mkdir bairros100
rm -f temp.dat
mv bairroAll.dat catole*.dat centro*.dat liberdade*.dat boxplot\ *.pdf norm\ *.pdf bairros100/


