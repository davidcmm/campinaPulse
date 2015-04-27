#!/bin/bash

#Krippendorfs alpha for general data
python analisaUsuarios.py run.csv
python preparaConsenso.py usersInfoSummary.dat

Rscript krippMoran.R kripp > kripp.dat

#Separa grupos de usuarios
python selectRunPerUsers.py run.csv media.dat > runMedia.csv
python selectRunPerUsers.py run.csv baixa.dat > runBaixa.csv 
python selectRunPerUsers.py run.csv adulto.dat > runAdulto.csv 
python selectRunPerUsers.py run.csv jovem.dat > runJovem.csv  
python selectRunPerUsers.py run.csv solteiro.dat > runSolteiro.csv 
python selectRunPerUsers.py run.csv casado.dat > runCasado.csv 
python selectRunPerUsers.py run.csv feminino.dat > runFeminino.csv 
python selectRunPerUsers.py run.csv masculino.dat > runMasculino.csv

mv media.dat baixa.dat adulto.dat jovem.dat solteiro.dat casado.dat feminino.dat masculino.dat idsGrupos 

#Analisa QScores
python analisaQScore.py run.csv
mv first.dat first_vote.dat

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

sort -k 3 -r first_vote.dat > first_vote_ordenado.dat

sort -k 3 -r firstMedia.dat > firsMediaOrd.dat
sort -k 3 -r firstBaixa.dat > firsBaixaOrd.dat
sort -k 3 -r firstSolteiro.dat > firsSolteiroOrd.dat
sort -k 3 -r firstCasado.dat > firsCasadoOrd.dat
sort -k 3 -r firstFeminino.dat > firsFemininoOrd.dat
sort -k 3 -r firstMasculino.dat > firsMasculinoOrd.dat
sort -k 3 -r firstJovem.dat > firsJovemOrd.dat
sort -k 3 -r firstAdulto.dat > firsAdultoOrd.dat

#Calculating Moran I
python extractLatLongStreet.py first_vote.dat > newFirst.dat
./processInputLatLong.sh newFirst.dat
rm newFirst.dat

grep "agrad%C3%A1vel?" streetsQScoresLatLong.dat > streetsQScoresLatLongAgra.dat
grep "seguro?" streetsQScoresLatLong.dat > streetsQScoresLatLongSeg.dat

Rscript krippMoran.R moran streetsQScoresLatLongAgra.dat streetsQScoresLatLongSeg.dat > moran.dat

#Encontra interseccao entre qscores gerados
python encontraInterseccao.py firsBaixaOrd.dat firsMediaOrd.dat > intersectionBaixaMedia.dat 
python encontraInterseccao.py firsSolteiroOrd.dat firsCasadoOrd.dat > intersectionSolteiroCasado.dat
python encontraInterseccao.py firsFemininoOrd.dat firsMasculinoOrd.dat > intersectionFemininoMasculino.dat
python encontraInterseccao.py firsJovemOrd.dat firsAdultoOrd.dat > intersectionJovemAdulto.dat

#Prepara paginas html e arquivos de interseccao ordenados
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
Rscript analisaCorrelacao.R rgbQScoreAgradSolteiro.dat rgbQScoreSegSolteiro.dat > correlacaoSolteiro.dat
Rscript analisaCorrelacao.R rgbQScoreAgradCasado.dat rgbQScoreSegCasado.dat > correlacaoCasado.dat
Rscript analisaCorrelacao.R rgbQScoreAgradJovem.dat rgbQScoreSegJovem.dat > correlacaoJovem.dat
Rscript analisaCorrelacao.R rgbQScoreAgradAdulto.dat rgbQScoreSegAdulto.dat > correlacaoAdulto.dat
Rscript analisaCorrelacao.R rgbQScoreAgradFeminino.dat rgbQScoreSegFeminino.dat > correlacaoFeminino.dat
Rscript analisaCorrelacao.R rgbQScoreAgradMasculino.dat rgbQScoreSegMasculino.dat > correlacaoMasculino.dat

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

mv *.pdf regressao*.dat correlacao/

#Kendall tau distance
rm -f kendall.dat
echo " Cas x Solteiro Agrad" >> kendall.dat
grep "agrad" firsCasadoOrdInter.dat > ranking1.dat
grep "agrad" firsSolteiroOrdInter.dat > ranking2.dat
Rscript kendallDistance.R ranking1.dat ranking2.dat >> kendall.dat 

echo " Cas x Solteiro Seg" >> kendall.dat
grep "seg" firsCasadoOrdInter.dat > ranking1.dat
grep "seg" firsSolteiroOrdInter.dat > ranking2.dat
Rscript kendallDistance.R ranking1.dat ranking2.dat >> kendall.dat 

echo " Baixa x Media Agrad" >> kendall.dat
grep "agrad" firsBaixaOrdInter.dat > ranking1.dat
grep "agrad" firsMediaOrdInter.dat > ranking2.dat
Rscript kendallDistance.R ranking1.dat ranking2.dat >> kendall.dat 

echo " Baixa x Media Seg" >> kendall.dat
grep "seg" firsBaixaOrdInter.dat > ranking1.dat
grep "seg" firsMediaOrdInter.dat > ranking2.dat
Rscript kendallDistance.R ranking1.dat ranking2.dat >> kendall.dat

echo " Fem x Masc Agrad" >> kendall.dat
grep "agrad" firsFemininoOrdInter.dat > ranking1.dat
grep "agrad" firsMasculinoOrdInter.dat > ranking2.dat
Rscript kendallDistance.R ranking1.dat ranking2.dat >> kendall.dat 

echo " Fem x Masc Seg" >> kendall.dat
grep "seg" firsFemininoOrdInter.dat > ranking1.dat
grep "seg" firsMasculinoOrdInter.dat > ranking2.dat
Rscript kendallDistance.R ranking1.dat ranking2.dat >> kendall.dat

echo " Jov x Adu Agrad" >> kendall.dat
grep "agrad" firsJovemOrdInter.dat > ranking1.dat
grep "agrad" firsAdultoOrdInter.dat > ranking2.dat
Rscript kendallDistance.R ranking1.dat ranking2.dat >> kendall.dat 

echo " Jov x Adu Seg" >> kendall.dat
grep "seg" firsJovemOrdInter.dat > ranking1.dat
grep "seg" firsAdultoOrdInter.dat > ranking2.dat
Rscript kendallDistance.R ranking1.dat ranking2.dat >> kendall.dat

rm ranking1.dat ranking2.dat
mv kendall.dat correlacao/

#Analisa QScore por Bairro
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

rm temp.dat liberdade.dat catole.dat centro.dat


