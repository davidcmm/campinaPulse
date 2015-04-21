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

echo ">>>>>>>> Jovem" >> bairro.dat
python analisaQScorePorBairro.py firsJovemOrdInter.dat > temp.dat
grep "catole" temp.dat | grep "agra" > catole.dat
grep "centro" temp.dat | grep "agra" > centro.dat
grep "liberdade" temp.dat | grep "agra" > liberdade.dat
echo "Agra Cat x Centro" >> bairro.dat
Rscript  calculaTTest.R catole.dat centro.dat >> bairro.dat
echo "Agra Lib x Centro" >> bairro.dat
Rscript  calculaTTest.R liberdade.dat centro.dat >> bairro.dat
echo "Agra Cat x Liberdade" >> bairro.dat
Rscript  calculaTTest.R catole.dat liberdade.dat >> bairro.dat

grep "catole" temp.dat | grep "seg" > catole.dat
grep "centro" temp.dat | grep "seg" > centro.dat
grep "liberdade" temp.dat | grep "seg" > liberdade.dat
echo "Seg Cat x Centro" >> bairro.dat
Rscript  calculaTTest.R catole.dat centro.dat >> bairro.dat
echo "Seg Lib x Centro" >> bairro.dat 
Rscript  calculaTTest.R liberdade.dat centro.dat >> bairro.dat
echo "Seg Cat x Liberdade" >> bairro.dat
Rscript  calculaTTest.R catole.dat liberdade.dat >> bairro.dat



echo ">>>>>>> Adulto" >> bairro.dat
python analisaQScorePorBairro.py firsAdultoOrdInter.dat > temp.dat
grep "catole" temp.dat | grep "agra" > catole.dat
grep "centro" temp.dat | grep "agra" > centro.dat
grep "liberdade" temp.dat | grep "agra" > liberdade.dat
echo "Agra Cat x Centro" >> bairro.dat
Rscript  calculaTTest.R catole.dat centro.dat >> bairro.dat
echo "Agra Lib x Centro" >> bairro.dat
Rscript  calculaTTest.R liberdade.dat centro.dat >> bairro.dat
echo "Agra Cat x Liberdade" >> bairro.dat
Rscript  calculaTTest.R catole.dat liberdade.dat >> bairro.dat

grep "catole" temp.dat | grep "seg" > catole.dat
grep "centro" temp.dat | grep "seg" > centro.dat
grep "liberdade" temp.dat | grep "seg" > liberdade.dat
echo "Seg Cat x Centro" >> bairro.dat
Rscript  calculaTTest.R catole.dat centro.dat >> bairro.dat
echo "Seg Lib x Centro" >> bairro.dat 
Rscript  calculaTTest.R liberdade.dat centro.dat >> bairro.dat
echo "Seg Cat x Liberdade" >> bairro.dat
Rscript  calculaTTest.R catole.dat liberdade.dat >> bairro.dat


echo ">>>>>>>>>> Baixa" >> bairro.dat
python analisaQScorePorBairro.py firsBaixaOrdInter.dat > temp.dat
grep "catole" temp.dat | grep "agra" > catole.dat
grep "centro" temp.dat | grep "agra" > centro.dat
grep "liberdade" temp.dat | grep "agra" > liberdade.dat
echo "Agra Cat x Centro" >> bairro.dat
Rscript  calculaTTest.R catole.dat centro.dat >> bairro.dat
echo "Agra Lib x Centro" >> bairro.dat
Rscript  calculaTTest.R liberdade.dat centro.dat >> bairro.dat
echo "Agra Cat x Liberdade" >> bairro.dat
Rscript  calculaTTest.R catole.dat liberdade.dat >> bairro.dat

grep "catole" temp.dat | grep "seg" > catole.dat
grep "centro" temp.dat | grep "seg" > centro.dat
grep "liberdade" temp.dat | grep "seg" > liberdade.dat
echo "Seg Cat x Centro" >> bairro.dat
Rscript  calculaTTest.R catole.dat centro.dat >> bairro.dat
echo "Seg Lib x Centro" >> bairro.dat 
Rscript  calculaTTest.R liberdade.dat centro.dat >> bairro.dat
echo "Seg Cat x Liberdade" >> bairro.dat
Rscript  calculaTTest.R catole.dat liberdade.dat >> bairro.dat



echo ">>>>>>>>>> Media" >> bairro.dat
python analisaQScorePorBairro.py firsMediaOrdInter.dat > temp.dat
grep "catole" temp.dat | grep "agra" > catole.dat
grep "centro" temp.dat | grep "agra" > centro.dat
grep "liberdade" temp.dat | grep "agra" > liberdade.dat
echo "Agra Cat x Centro" >> bairro.dat
Rscript  calculaTTest.R catole.dat centro.dat >> bairro.dat
echo "Agra Lib x Centro" >> bairro.dat
Rscript  calculaTTest.R liberdade.dat centro.dat >> bairro.dat
echo "Agra Cat x Liberdade" >> bairro.dat
Rscript  calculaTTest.R catole.dat liberdade.dat >> bairro.dat

grep "catole" temp.dat | grep "seg" > catole.dat
grep "centro" temp.dat | grep "seg" > centro.dat
grep "liberdade" temp.dat | grep "seg" > liberdade.dat
echo "Seg Cat x Centro" >> bairro.dat
Rscript  calculaTTest.R catole.dat centro.dat >> bairro.dat
echo "Seg Lib x Centro" >> bairro.dat 
Rscript  calculaTTest.R liberdade.dat centro.dat >> bairro.dat
echo "Seg Cat x Liberdade" >> bairro.dat
Rscript  calculaTTest.R catole.dat liberdade.dat >> bairro.dat




echo ">>>>>>>>>> Fem" >> bairro.dat
python analisaQScorePorBairro.py firsFemininoOrdInter.dat > temp.dat
grep "catole" temp.dat | grep "agra" > catole.dat
grep "centro" temp.dat | grep "agra" > centro.dat
grep "liberdade" temp.dat | grep "agra" > liberdade.dat
echo "Agra Cat x Centro" >> bairro.dat
Rscript  calculaTTest.R catole.dat centro.dat >> bairro.dat
echo "Agra Lib x Centro" >> bairro.dat
Rscript  calculaTTest.R liberdade.dat centro.dat >> bairro.dat
echo "Agra Cat x Liberdade" >> bairro.dat
Rscript  calculaTTest.R catole.dat liberdade.dat >> bairro.dat

grep "catole" temp.dat | grep "seg" > catole.dat
grep "centro" temp.dat | grep "seg" > centro.dat
grep "liberdade" temp.dat | grep "seg" > liberdade.dat
echo "Seg Cat x Centro" >> bairro.dat
Rscript  calculaTTest.R catole.dat centro.dat >> bairro.dat
echo "Seg Lib x Centro" >> bairro.dat 
Rscript  calculaTTest.R liberdade.dat centro.dat >> bairro.dat
echo "Seg Cat x Liberdade" >> bairro.dat
Rscript  calculaTTest.R catole.dat liberdade.dat >> bairro.dat




echo ">>>>>>>>> Masc" >> bairro.dat
python analisaQScorePorBairro.py firsMasculinoOrdInter.dat > temp.dat
grep "catole" temp.dat | grep "agra" > catole.dat
grep "centro" temp.dat | grep "agra" > centro.dat
grep "liberdade" temp.dat | grep "agra" > liberdade.dat
echo "Agra Cat x Centro" >> bairro.dat
Rscript  calculaTTest.R catole.dat centro.dat >> bairro.dat
echo "Agra Lib x Centro" >> bairro.dat
Rscript  calculaTTest.R liberdade.dat centro.dat >> bairro.dat
echo "Agra Cat x Liberdade" >> bairro.dat
Rscript  calculaTTest.R catole.dat liberdade.dat >> bairro.dat

grep "catole" temp.dat | grep "seg" > catole.dat
grep "centro" temp.dat | grep "seg" > centro.dat
grep "liberdade" temp.dat | grep "seg" > liberdade.dat
echo "Seg Cat x Centro" >> bairro.dat
Rscript  calculaTTest.R catole.dat centro.dat >> bairro.dat
echo "Seg Lib x Centro" >> bairro.dat 
Rscript  calculaTTest.R liberdade.dat centro.dat >> bairro.dat
echo "Seg Cat x Liberdade" >> bairro.dat
Rscript  calculaTTest.R catole.dat liberdade.dat >> bairro.dat




echo ">>>>>>>>>>>> Casado" >> bairro.dat
python analisaQScorePorBairro.py firsCasadoOrdInter.dat > temp.dat
grep "catole" temp.dat | grep "agra" > catole.dat
grep "centro" temp.dat | grep "agra" > centro.dat
grep "liberdade" temp.dat | grep "agra" > liberdade.dat
echo "Agra Cat x Centro" >> bairro.dat
Rscript  calculaTTest.R catole.dat centro.dat >> bairro.dat
echo "Agra Lib x Centro" >> bairro.dat
Rscript  calculaTTest.R liberdade.dat centro.dat >> bairro.dat
echo "Agra Cat x Liberdade" >> bairro.dat
Rscript  calculaTTest.R catole.dat liberdade.dat >> bairro.dat

grep "catole" temp.dat | grep "seg" > catole.dat
grep "centro" temp.dat | grep "seg" > centro.dat
grep "liberdade" temp.dat | grep "seg" > liberdade.dat
echo "Seg Cat x Centro" >> bairro.dat
Rscript  calculaTTest.R catole.dat centro.dat >> bairro.dat
echo "Seg Lib x Centro" >> bairro.dat 
Rscript  calculaTTest.R liberdade.dat centro.dat >> bairro.dat
echo "Seg Cat x Liberdade" >> bairro.dat
Rscript  calculaTTest.R catole.dat liberdade.dat >> bairro.dat




echo ">>>>>>>>>>>>>> Solteiro" >> bairro.dat
python analisaQScorePorBairro.py firsSolteiroOrdInter.dat > temp.dat
grep "catole" temp.dat | grep "agra" > catole.dat
grep "centro" temp.dat | grep "agra" > centro.dat
grep "liberdade" temp.dat | grep "agra" > liberdade.dat
echo "Agra Cat x Centro" >> bairro.dat
Rscript  calculaTTest.R catole.dat centro.dat >> bairro.dat
echo "Agra Lib x Centro" >> bairro.dat
Rscript  calculaTTest.R liberdade.dat centro.dat >> bairro.dat
echo "Agra Cat x Liberdade" >> bairro.dat
Rscript  calculaTTest.R catole.dat liberdade.dat >> bairro.dat

grep "catole" temp.dat | grep "seg" > catole.dat
grep "centro" temp.dat | grep "seg" > centro.dat
grep "liberdade" temp.dat | grep "seg" > liberdade.dat
echo "Seg Cat x Centro" >> bairro.dat
Rscript  calculaTTest.R catole.dat centro.dat >> bairro.dat
echo "Seg Lib x Centro" >> bairro.dat 
Rscript  calculaTTest.R liberdade.dat centro.dat >> bairro.dat
echo "Seg Cat x Liberdade" >> bairro.dat
Rscript  calculaTTest.R catole.dat liberdade.dat >> bairro.dat

rm temp.dat liberdade.dat catole.dat centro.dat
