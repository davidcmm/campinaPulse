#!/bin/bash

python analisaQScore.py runAdulto.csv 1000
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
sort -k 3 -r firstCatole.dat > firsCatoleOrd.dat
sort -k 3 -r firstCentro.dat > firsCentroOrd.dat
sort -k 3 -r firstLiberdade.dat > firsLiberdadeOrd.dat
sort -k 3 -r firstNotCatole.dat > firsNotCatoleOrd.dat
sort -k 3 -r firstNotCentro.dat > firsNotCentroOrd.dat
sort -k 3 -r firstNotLiberdade.dat > firsNotLiberdadeOrd.dat

sort -k 3 -r allMedia.dat > allMediaOrd.dat
sort -k 3 -r allBaixa.dat > allBaixaOrd.dat
sort -k 3 -r allSolteiro.dat > allSolteiroOrd.dat
sort -k 3 -r allCasado.dat > allCasadoOrd.dat
sort -k 3 -r allFeminino.dat > allFemininoOrd.dat
sort -k 3 -r allMasculino.dat > allMasculinoOrd.dat
sort -k 3 -r allJovem.dat > allJovemOrd.dat
sort -k 3 -r allCatole.dat > allCatoleOrd.dat
sort -k 3 -r allCentro.dat > allCentroOrd.dat
sort -k 3 -r allLiberdade.dat > allLiberdadeOrd.dat
sort -k 3 -r allNotCatole.dat > allNotCatoleOrd.dat
sort -k 3 -r allNotCentro.dat > allNotCentroOrd.dat
sort -k 3 -r allNotLiberdade.dat > allNotLiberdadeOrd.dat
