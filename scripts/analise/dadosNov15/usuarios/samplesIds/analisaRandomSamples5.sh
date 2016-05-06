#!/bin/bash
#Receives files containing users ids per group, generates new samples of user ids per groups and calculates QScores for each sample!

for i in `seq 8001 10000`; do
    	Rscript sampleUserIds.R $i

	#python selectRunPerUsers.py run.csv media_${i}.dat > runMedia_${i}.csv
	#python selectRunPerUsers.py run.csv baixa_${i}.dat > runBaixa_${i}.csv 
	#python selectRunPerUsers.py run.csv adulto_${i}.dat > runAdulto_${i}.csv 
	#python selectRunPerUsers.py run.csv jovem_${i}.dat > runJovem_${i}.csv  
	#python selectRunPerUsers.py run.csv solteiro_${i}.dat > runSolteiro_${i}.csv 
	#python selectRunPerUsers.py run.csv casado_${i}.dat > runCasado_${i}.csv 
	#python selectRunPerUsers.py run.csv feminino_${i}.dat > runFeminino_${i}.csv 
	#python selectRunPerUsers.py run.csv masculino_${i}.dat > runMasculino_${i}.csv

	python selectRunPerUsers.py run.csv centro_${i}.dat > runCentro_${i}.csv
	python selectRunPerUsers.py run.csv notcentro_${i}.dat > runNotCentro_${i}.csv
	python selectRunPerUsers.py run.csv catole_${i}.dat > runCatole_${i}.csv
	python selectRunPerUsers.py run.csv notcatole_${i}.dat > runNotCatole_${i}.csv
	python selectRunPerUsers.py run.csv liberdade_${i}.dat > runLiberdade_${i}.csv
	python selectRunPerUsers.py run.csv notliberdade_${i}.dat > runNotLiberdade_${i}.csv

	#python analisaQScore.py runAdulto_${i}.csv 100 tasksDef.csv
	#mv all.dat allAdulto_${i}.dat
	#python analisaQScore.py runJovem_${i}.csv 100 tasksDef.csv
	#mv all.dat allJovem_${i}.dat
	#python analisaQScore.py runSolteiro_${i}.csv 100 tasksDef.csv
	#mv all.dat allSolteiro_${i}.dat
	#python analisaQScore.py runCasado_${i}.csv 100 tasksDef.csv
	#mv all.dat allCasado_${i}.dat
	#python analisaQScore.py runMedia_${i}.csv 100 tasksDef.csv
	#mv all.dat allMedia_${i}.dat
	#python analisaQScore.py runBaixa_${i}.csv 100 tasksDef.csv
	#mv all.dat allBaixa_${i}.dat
	#python analisaQScore.py runFeminino_${i}.csv 100  tasksDef.csv
	#mv all.dat allFeminino_${i}.dat
	#python analisaQScore.py runMasculino_${i}.csv 100 tasksDef.csv
	#mv all.dat allMasculino_${i}.dat

	python analisaQScore.py runCentro_${i}.csv 100 tasksDef.csv
	mv all.dat allCentro_${i}.dat
	python analisaQScore.py runNotCentro_${i}.csv 100 tasksDef.csv
	mv all.dat allNotCentro_${i}.dat
	python analisaQScore.py runCatole_${i}.csv 100 tasksDef.csv
	mv all.dat allCatole_${i}.dat
	python analisaQScore.py runNotCatole_${i}.csv 100 tasksDef.csv
	mv all.dat allNotCatole_${i}.dat
	python analisaQScore.py runLiberdade_${i}.csv 100 tasksDef.csv
	mv all.dat allLiberdade_${i}.dat
	python analisaQScore.py runNotLiberdade_${i}.csv 100 tasksDef.csv
	mv all.dat allNotLiberdade_${i}.dat

	#sort -k 3 -r allMedia_${i}.dat > allMediaOrd_${i}.dat
	#sort -k 3 -r allBaixa_${i}.dat > allBaixaOrd_${i}.dat
	#sort -k 3 -r allSolteiro_${i}.dat > allSolteiroOrd_${i}.dat
	#sort -k 3 -r allCasado_${i}.dat > allCasadoOrd_${i}.dat
	#sort -k 3 -r allFeminino_${i}.dat > allFemininoOrd_${i}.dat
	#sort -k 3 -r allMasculino_${i}.dat > allMasculinoOrd_${i}.dat
	#sort -k 3 -r allJovem_${i}.dat > allJovemOrd_${i}.dat
	#sort -k 3 -r allAdulto_${i}.dat > allAdultoOrd_${i}.dat

	sort -k 3 -r allCentro_${i}.dat > allCentroOrd_${i}.dat
	sort -k 3 -r allNotCentro_${i}.dat > allNotCentroOrd_${i}.dat
	sort -k 3 -r allCatole_${i}.dat > allCatoleOrd_${i}.dat
	sort -k 3 -r allNotCatole_${i}.dat > allNotCatoleOrd_${i}.dat
	sort -k 3 -r allLiberdade_${i}.dat > allLiberdadeOrd_${i}.dat
	sort -k 3 -r allNotLiberdade_${i}.dat > allNotLiberdadeOrd_${i}.dat

	#python encontraInterseccao.py allBaixaOrd_${i}.dat allMediaOrd_${i}.dat > intersectionAllBaixaMedia_${i}.dat 
	#python encontraInterseccao.py allSolteiroOrd_${i}.dat allCasadoOrd_${i}.dat > intersectionAllSolteiroCasado_${i}.dat
	#python encontraInterseccao.py allFemininoOrd_${i}.dat allMasculinoOrd_${i}.dat > intersectionAllFemininoMasculino_${i}.dat
	#python encontraInterseccao.py allJovemOrd_${i}.dat allAdultoOrd_${i}.dat > intersectionAllJovemAdulto_${i}.dat
	python encontraInterseccao.py allCentroOrd_${i}.dat allNotCentroOrd_${i}.dat > intersectionAllCentro_${i}.dat
	python encontraInterseccao.py allCatoleOrd_${i}.dat allNotCatoleOrd_${i}.dat > intersectionAllCatole_${i}.dat
	python encontraInterseccao.py allLiberdadeOrd_${i}.dat allNotLiberdadeOrd_${i}.dat > intersectionAllLiberdade_${i}.dat

	#python preparaHTML.py allMediaOrd_${i}.dat intersectionAllBaixaMedia_${i}.dat > allMediaOrdInter_${i}.dat 
	#python preparaHTML.py allBaixaOrd_${i}.dat intersectionAllBaixaMedia_${i}.dat > allBaixaOrdInter_${i}.dat 

	#python preparaHTML.py allFemininoOrd_${i}.dat intersectionAllFemininoMasculino_${i}.dat > allFemininoOrdInter_${i}.dat 
	#python preparaHTML.py allMasculinoOrd_${i}.dat intersectionAllFemininoMasculino_${i}.dat > allMasculinoOrdInter_${i}.dat 

	#python preparaHTML.py allCasadoOrd_${i}.dat intersectionAllSolteiroCasado_${i}.dat > allCasadoOrdInter_${i}.dat 
	#python preparaHTML.py allSolteiroOrd_${i}.dat intersectionAllSolteiroCasado_${i}.dat > allSolteiroOrdInter_${i}.dat 

	#python preparaHTML.py allJovemOrd_${i}.dat intersectionAllJovemAdulto_${i}.dat > allJovemOrdInter_${i}.dat 
	#python preparaHTML.py allAdultoOrd_${i}.dat intersectionAllJovemAdulto_${i}.dat > allAdultoOrdInter_${i}.dat

	python preparaHTML.py allCentroOrd_${i}.dat intersectionAllCentro_${i}.dat > allCentroOrdInter_${i}.dat
	python preparaHTML.py allNotCentroOrd_${i}.dat intersectionAllCentro_${i}.dat > allNotCentroOrdInter_${i}.dat
	python preparaHTML.py allCatoleOrd_${i}.dat intersectionAllCatole_${i}.dat > allCatoleOrdInter_${i}.dat
	python preparaHTML.py allNotCatoleOrd_${i}.dat intersectionAllCatole_${i}.dat > allNotCatoleOrdInter_${i}.dat
	python preparaHTML.py allLiberdadeOrd_${i}.dat intersectionAllLiberdade_${i}.dat > allLiberdadeOrdInter_${i}.dat
	python preparaHTML.py allNotLiberdadeOrd_${i}.dat intersectionAllLiberdade_${i}.dat > allNotLiberdadeOrdInter_${i}.dat

	Rscript combinaEntradas.R $i

	mkdir -p randomInputFiles
	mv centro_${i}* notcentro_${i}* catole_${i}* notcatole_${i}* liberdade_${i}* notliberdade_${i}* run*_${i}.csv all*_${i}.dat intersection*_${i}.dat randomInputFiles #masculino_* feminino_* jovem_* adulto_* media_* baixa_* casado_* solteiro_* run*_*.csv all*_${i}.dat intersection*.dat randomInputFiles 

done

